"""What a reader can take away: a tutorial as one HTML file that opens from
disk, a zip of a series or of a whole course, and the Notebook as a folder
that runs with no network.

`build()` in main.py calls the `write_*` functions here after the pages are
written. This module takes the build's own helpers from main.py, which
imports it last.
"""

from __future__ import annotations

from pathlib import Path
import base64
import html
import json
import re
import shutil
import source_map
import zipfile

from builder.config import cfg
from builder.main import (
    BuildError,
    LOAD_CALL,
    Tutorial,
    _reference_index_for_bundle,
    data_index,
    say,
    standalone_data,
    versioned,
    write_data_index,
)


PYODIDE_CLASSIC = (
    '<script src="https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js"></script>'
)


FONT_URL_RE = re.compile(r"url\((?P<quote>['\"]?)fonts/(?P<name>[\w.-]+\.woff2)(?P=quote)\)")


def inline_katex_css() -> str:
    """KaTeX's stylesheet with its fonts folded in as data.

    Only the woff2 files it actually names, which is what keeps this to a few
    hundred kilobytes rather than the whole family.
    """
    css = (cfg.ASSETS / "vendor" / "katex.min.css").read_text()

    def one(match: re.Match) -> str:
        font = cfg.ASSETS / "vendor" / "fonts" / match.group("name")
        if not font.is_file():
            return match.group(0)
        data = base64.b64encode(font.read_bytes()).decode("ascii")
        return f"url(data:font/woff2;base64,{data})"

    return FONT_URL_RE.sub(one, css)


def inline_accessible_fonts_css() -> str:
    """The two accessible reading fonts' stylesheet, with its own fonts
    folded in as data — same shape as inline_katex_css() above, and able
    to reuse its FONT_URL_RE unchanged because vendor-src/build-vendor.mjs
    writes these woff2 files flat into vendor/fonts/ beside KaTeX's own
    rather than into a subfolder of their own.
    """
    css = (cfg.ASSETS / "vendor" / "accessible-fonts.css").read_text()

    def one(match: re.Match) -> str:
        font = cfg.ASSETS / "vendor" / "fonts" / match.group("name")
        if not font.is_file():
            return match.group(0)
        data = base64.b64encode(font.read_bytes()).decode("ascii")
        return f"url(data:font/woff2;base64,{data})"

    return FONT_URL_RE.sub(one, css)


def replace_once(page: str, needle: str, replacement: str, what: str) -> str:
    """Substitute, and fail if there was nothing to substitute.

    `str.replace` with no match is a silent no-op, which is how a downloadable
    copy can come out missing its stylesheet and look fine to the build. Every
    replacement here is against markup this same file wrote moments earlier, so
    a miss means the two have drifted apart and the export is wrong.
    """
    if needle not in page:
        raise BuildError(
            f"the downloadable copy could not find {what} in the built page. "
            "shell.html and build.py have drifted apart."
        )
    return page.replace(needle, replacement, 1)


def standalone_html(tutorial: Tutorial, page: str) -> str:
    """Turn a built page into one file that works from a student's disk."""
    # A copy to keep has nothing to edit, so it carries none of the source map
    # or of the Settings section and loader that start editing.
    page = source_map.ATTR_RE.sub("", page)
    page = re.sub(r"<!--dl-edit:start-->.*?<!--dl-edit:end-->", "", page, flags=re.DOTALL)
    # The same prefixes build.py wrote into the page's own references: `up`
    # for anything under assets/, `root` for the site root itself.
    root = "../" * tutorial.depth
    up = root + "assets/"
    style = (cfg.ASSETS / "tutorial-style.css").read_text()
    bundle = (cfg.ASSETS / "vendor" / "standalone.bundle.js").read_text()
    tools = (cfg.ASSETS / "tutorial_tools.py").read_text()

    page = replace_once(
        page,
        f'<link rel="stylesheet" href="{versioned(up, "vendor/katex.min.css")}">',
        f"<style>{inline_katex_css()}</style>" if tutorial.has_math else "",
        "the maths stylesheet",
    )
    page = replace_once(
        page,
        f'<link rel="stylesheet" href="{versioned(up, "vendor/accessible-fonts.css")}">',
        f"<style>{inline_accessible_fonts_css()}</style>",
        "the accessible-fonts stylesheet",
    )
    page = replace_once(
        page,
        f'<link rel="stylesheet" href="{versioned(up, "tutorial-style.css")}">',
        f"<style>{style}</style>",
        "the stylesheet",
    )

    # The runtime, as a classic script, behind Pyodide's classic loader.
    page = replace_once(
        page,
        f'<script type="module" src="{versioned(up, "tutorial-runtime.js")}"></script>',
        PYODIDE_CLASSIC + "\n<script>" + bundle + "</script>",
        "the runtime",
    )

    page = replace_once(
        page, f'<script src="{root}coi-serviceworker.js"></script>\n', "", "the isolation shim"
    )

    page = replace_once(
        page, f'<script type="module" src="{versioned(up, "search.js")}"></script>\n',
        "", "the search script",
    )

    # The Python tools, which cannot be fetched from a file.
    marker = '<script type="application/json" id="dewlab-manifest">'
    start = page.index(marker) + len(marker)
    end = page.index("</script>", start)
    manifest = json.loads(page[start:end])
    manifest["toolsSource"] = tools
    manifest["standalone"] = True
    if tutorial.datasets:
        manifest["dataIndex"], manifest["dataFiles"] = standalone_data(tutorial)
    manifest.pop("versions", None)
    page = page[:start] + json.dumps(manifest).replace("<", "\\u003c") + page[end:]

    page = re.sub(r"<nav class=\"dl-nav[^\"]*\">.*?</nav>", "", page, flags=re.DOTALL)
    # The search line (nav_search_html()) finds other pages by fetching the
    # site's index, and neither the index nor those pages are on a student's
    # disk, so it goes with the rest of the cross-file navigation. Its own
    # widget is the one nested div, so the first </div></div> closes it.
    page = re.sub(r'<div class="dl-nav-search">.*?</div></div>', "", page, flags=re.DOTALL)
    # The where-you-are tree links to other modules, series and tutorials —
    # exactly the cross-file navigation this function already strips above,
    # just built by crumb_trail_html() instead of nav_for(). The page's own
    # rung is its contents, whose links point inside this file and work
    # from a student's disk, so that one rung stays — minus its practice
    # and context lines, which point at other files.
    def keep_contents(match: re.Match) -> str:
        contents = re.search(
            r'<details class="dl-crumb-level dl-crumb-level-4">.*?</details>',
            match.group(0), re.DOTALL,
        )
        if not contents:
            return ""
        own = re.sub(r'<div role="listitem" class="dl-crumb-(?:practice|context)">.*?</div>', "", contents.group(0), flags=re.DOTALL)
        return f'<nav class="dl-crumbtrail" aria-label="Contents">{own}</nav>'
    page = re.sub(r"<nav class=\"dl-crumbtrail\".*?</nav>", keep_contents, page, flags=re.DOTALL)
    page = re.sub(
        r'(<section class="dl-settings-section" id="dl-settings-download">).*?(</section>)',
        r"\1\2",
        page,
        flags=re.DOTALL,
    )
    page = page.replace(f'href="{root}index.html"', 'href="#" onclick="return false"')
    return page


def write_standalone(tutorial: Tutorial, page: str) -> Path:
    """Writes one tutorial's downloadable, self-contained copy (the
    single-file version a student can save and reopen offline) into the
    `site/download/` folder. `page` is the already-built standalone HTML
    string from `standalone_html()` — this function's own job is just
    figuring out where that string should be saved and doing a
    build-time check (the note about web addresses right below) that
    only makes sense for this particular kind of output.
    """
    # A load by web address that data/ keeps no copy of still needs the
    # network, which a reader offline does not have (#324).
    addresses = {entry["live"]["url"] for entry in data_index().values()
                 if entry.get("address")}
    for cell in tutorial.cells:
        for match in LOAD_CALL.finditer(cell.code):
            name = match.group("name")
            if name.startswith(("http://", "https://")) and name not in addresses:
                say(f"note: {tutorial.path.relative_to(cfg.ROOT)} loads {name}, which "
                      "data/ keeps no copy of, so its downloaded copy needs the "
                      "network for that cell")

    target = cfg.OUT / "download" / f"{tutorial.slug}.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(standalone_html(tutorial, page))
    return target


SERIES_SLUG_RE = re.compile(r"[^a-z0-9]+")


def series_slug(course: str, series: str) -> str:
    """A filename for a whole series: the course id and the series key."""
    slug = SERIES_SLUG_RE.sub("-", f"{course}-{series}".lower()).strip("-")
    return slug or "tutorials"


def zip_sequence(
    members: list[Tutorial], practice: dict[str, list[Tutorial]]
) -> list[Tutorial]:
    """Reading order, with each tutorial's own practice page right after it.

    `series_of()` deliberately keeps practice off the reading order used for
    prev/next navigation (putting it on the route would double the length of
    every series) — but a downloaded folder is not a route through a page at
    a time, it is a stack of files a person opens by number, and there the
    practice page belongs right after the tutorial it tests, not omitted.
    """
    sequence: list[Tutorial] = []
    for tutorial in members:
        sequence.append(tutorial)
        sequence.extend(practice.get(tutorial.slug, []))
    return sequence


def zip_entry_name(index: int, width: int, slug: str) -> str:
    """A sortable filename a file browser lists in the order to open them —
    the same reason build.py's own generated pages sort no particular way,
    but a downloaded folder is judged by its listing, not by clicking
    through a nav bar."""
    return f"{index:0{width}d}-{slug}.html"


def start_here_html(title: str, sections: list[tuple[str | None, list[tuple[str, Tutorial]]]]) -> str:
    """The one file every downloaded folder needs and no individual
    standalone copy can provide for another: standalone_html() deliberately
    strips each page's cross-file navigation (prev/next, the where-you-are tree),
    since a single tutorial downloaded on its own has no siblings to point
    at (see its own docstring). Bundled into a zip, those siblings exist —
    this page is what tells a reader they are there, and in what order.
    Plain and self-contained on purpose: it opens straight from disk, next
    to files that do the same, with no server and nothing else to fetch.
    """
    body = []
    next_number = 1
    for heading, entries in sections:
        if heading:
            body.append(f"<h2>{html.escape(heading)}</h2>")
        body.append(f'<ol start="{next_number}">')
        for name, member in entries:
            tag = ' <span class="practice">practice</span>' if member.is_practice else ""
            body.append(
                f'<li><a href="{html.escape(name)}">{html.escape(member.title)}</a>{tag}</li>'
            )
        body.append("</ol>")
        next_number += len(entries)
    body_html = "\n".join(body)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Start here — {html.escape(title)}</title>
<style>
:root {{ color-scheme: light dark; }}
body {{
  margin: 0; padding: 2.5rem 1.25rem 4rem; max-width: 38rem; margin-inline: auto;
  font: 1rem/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #fdfcfa; color: #1a1a1a;
}}
h1 {{ font-size: 1.5rem; margin: 0 0 0.6rem; }}
h2 {{ font-size: 1.05rem; margin: 2rem 0 0.5rem; border-top: 1px solid #ddd7cd; padding-top: 1.5rem; }}
p.lede {{ color: #5f6b7a; }}
ol {{ padding-left: 1.4rem; }}
li {{ margin: 0.4rem 0; }}
a {{ color: #d4692a; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.practice {{ font-size: 0.82rem; color: #5f6b7a; }}
@media (prefers-color-scheme: dark) {{
  body {{ background: #14181f; color: #e6e3dd; }}
  h2 {{ border-color: #2f3743; }}
  p.lede, .practice {{ color: #98a2b3; }}
}}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<p class="lede">Numbered in the order to open them — a tutorial's practice sits
right after it. Start with 01.</p>
{body_html}
</body>
</html>"""


def write_zip_entries(
    archive: zipfile.ZipFile, folder: str, sequence: list[Tutorial], width: int, start: int = 1
) -> list[tuple[str, Tutorial]]:
    """Write one section's standalone copies into `archive` under `folder`,
    numbered from `start`, zero-padded to `width`. `width` is a parameter
    rather than worked out from this one section, so every section in a
    multi-series module archive pads to the same width as the archive's own
    total — the point at which a count would need another digit rarely falls
    exactly on a section boundary. Returns the (entry name, tutorial) pairs
    written, for start_here_html() to link to."""
    entries = []
    for offset, member in enumerate(sequence):
        name = zip_entry_name(start + offset, width, member.slug)
        archive.write(cfg.OUT / "download" / f"{member.slug}.html", f"{folder}/{name}")
        entries.append((name, member))
    return entries


def write_series_zip(
    course: str,
    series: str,
    members: list[Tutorial],
    practice: dict[str, list[Tutorial]],
    series_title: str,
) -> Path:
    """Every downloadable copy in one series, gathered into one archive,
    numbered tutorial-then-its-practice in reading order, with a
    0-start-here.html a reader lands on first after unzipping.

    A student takes one tutorial. Somebody setting up a room, or filling a
    memory stick for a class with no reliable connection, wants the set. The
    archive holds the very files the download links point at, so there is no
    second copy to keep in step with anything.
    """
    folder = series_slug(course, series)
    target = cfg.OUT / "download" / f"{folder}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    sequence = zip_sequence(members, practice)
    width = max(2, len(str(len(sequence))))
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        entries = write_zip_entries(archive, folder, sequence, width)
        archive.writestr(
            f"{folder}/0-start-here.html", start_here_html(series_title, [(None, entries)])
        )
    return target


def write_course_zip(
    course: str,
    title: str,
    series_in_order: list[tuple[str, str, list[Tutorial]]],
    practice: dict[str, list[Tutorial]],
    mixed_pages: list[Tutorial],
) -> Path:
    """Every series in a course, and its mixed problem sets, in one archive —
    the whole course a room or a memory stick wants, not one series of it.

    `series_in_order` is `(series, series_title, members)`, in the same order
    the contents page already lists that course's series in. Numbering runs
    once across the whole archive, not restarting per series, so the folder
    reads as one sequence top to bottom rather than several that happen to
    share a listing.
    """
    target = cfg.OUT / "download" / f"{course}-all.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    show_headings = len(series_in_order) > 1

    series_sequences = [
        (series_title, zip_sequence(members, practice))
        for _, series_title, members in series_in_order
    ]
    total = sum(len(seq) for _, seq in series_sequences) + len(mixed_pages)
    width = max(2, len(str(total)))

    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        sections: list[tuple[str | None, list[tuple[str, Tutorial]]]] = []
        next_index = 1
        for series_title, sequence in series_sequences:
            entries = write_zip_entries(archive, course, sequence, width, start=next_index)
            next_index += len(sequence)
            sections.append((series_title if show_headings else None, entries))
        if mixed_pages:
            entries = write_zip_entries(archive, course, mixed_pages, width, start=next_index)
            sections.append(("Mixed problems", entries))
        archive.writestr(
            f"{course}/0-start-here.html", start_here_html(title, sections)
        )
    return target


def zip_directory(source_dir: Path, target_zip: Path) -> Path:
    """Every file under `source_dir`, archived under its own name at the
    zip's root — so unzipping drops one `source_dir.name` folder next to
    wherever the student put the zip, not its contents loose."""
    target_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir.parent))
    return target_zip


SERVE_SCRIPT = '''#!/usr/bin/env python3
"""Run this — `python3 serve.py` — to actually open this folder.

Double-clicking the .html file directly shows a blank, broken page: this
app's own JavaScript is split across several files that import each
other, and a browser only allows that kind of import from a page loaded
over http:// or https://, never from a file opened straight off disk.
This script is the fix — it serves this folder to your own browser at a
localhost address, which satisfies that requirement, using nothing this
computer doesn't already have if it can run this script at all.
"""
import functools
import http.server
import socketserver
import webbrowser

PORT = 8756


def main():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=".")
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        url = f"http://127.0.0.1:{PORT}/"
        print(f"Serving this folder at {url}")
        print("Leave this window open. Press Ctrl+C here to stop.")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
'''


DEWMINI_ASSET_FILES = (
    "pyodide-engine.js",
    "pyodide-worker.js",
    # Imported by both of the two above, so a bundle without it has an
    # engine that cannot start.
    "module-watch.js",
    # Imported by pyodide-engine.js: what a cell's widgets hold, and its
    # sliders.
    "cell-widgets.js",
    # Imported by both engine files: how input() waits for a typed line.
    "input-wait.js",
    # Imported by dewmini.js for its Library search — the one idea of
    # word matching every search box shares.
    "search-words.js",
    "tutorial_tools.py",
    "tutorial-style.css",
    "vendor/codemirror.bundle.js",
    "vendor/katex.min.css",
    "vendor/katex.bundle.js",
    "vendor/accessible-fonts.css",
    "examples/sql-owid.ipynb",
    "examples/data-investigation.ipynb",
    "examples/math-and-charts.ipynb",
    "examples/word-frequency.ipynb",
)


# compose/'s pages at their old addresses, from before dewmini and dewmini
# web were renamed the Notebook and the Workspace: small hand-written
# redirects rather than lines in courses/redirects.yaml, because they keep a
# query string and a #hash, and because compose/ is copied wholesale rather
# than written page by page (write_redirects() only sends an old address to
# a page the build wrote).
COMPOSE_REDIRECTS = ("dewmini.html", "dewminiweb.html")


def write_dewmini_bundle() -> Path | None:
    """The downloadable Notebook (download/notebook/, zipped as
    download/notebook.zip): a folder a student or teacher can save and
    open with no internet at all, once assets/vendor/pyodide/ exists to
    include. The Notebook's code is still called dewmini, hence this
    function's name.

    It still needs a local server to open, though: dewmini.js imports
    dewmini-fs.js and pyodide-engine.js with real `import` statements,
    and a browser only allows that kind of cross-file import from
    http(s)://, never a file opened straight off disk. `index.html` below
    checks for this rather than assuming a downloader read a README first,
    and SERVE_SCRIPT is copied in as this bundle's own serve.py.

    The bundle mirrors the hosted site's actual folder shape — compose/,
    assets/, and data/ as siblings, exactly what compose/notebook.html's own
    relative references already assume — so nothing in it needs rewriting
    to work unhosted, beyond layering in the DEWLAB_PYODIDE_BASE override.
    The tiny top-level `index.html` exists so opening the downloaded folder
    means finding one obvious file rather than knowing to look inside
    compose/ first.

    assets/vendor/pyodide/ is gitignored; populate it with:

        python3 dev/fetch_pyodide.py --out assets/vendor/pyodide \\
            --packages numpy pandas matplotlib sqlite3 Pillow jedi pyodide-http

    (jedi and parso are needed regardless of DM_PACKAGES, for
    autocomplete.) A build run without that first still produces a working
    bundle, just one that falls back to the CDN on first run.
    """
    notebook_html = cfg.COMPOSE / "notebook.html"
    if not notebook_html.exists():
        return None

    target = cfg.OUT / "download" / "notebook"
    shutil.rmtree(target, ignore_errors=True)
    (target / "assets" / "vendor").mkdir(parents=True, exist_ok=True)

    pyodide_vendored = (cfg.ASSETS / "vendor" / "pyodide").is_dir()

    # The two old-address redirects (compose/dewmini.html and
    # compose/dewminiweb.html) are for bookmarks into the hosted site; a
    # fresh download has none to keep.
    shutil.copytree(cfg.COMPOSE, target / "compose",
                    ignore=shutil.ignore_patterns(*COMPOSE_REDIRECTS))
    html = (target / "compose" / "notebook.html").read_text()
    if pyodide_vendored:
        html = html.replace(
            "<head>",
            '<head>\n<script>window.DEWLAB_PYODIDE_BASE = "../assets/vendor/pyodide/";</script>',
            1,
        )
        (target / "compose" / "notebook.html").write_text(html)

    for rel in DEWMINI_ASSET_FILES:
        src = cfg.ASSETS / rel
        if not src.exists():
            say(f"note: dewmini bundle is missing {src.relative_to(cfg.ROOT)}")
            continue
        dest = target / "assets" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    if cfg.DATA.is_dir():
        shutil.copytree(cfg.DATA, target / "data")
        write_data_index(target / "data")

    fonts_dir = cfg.ASSETS / "vendor" / "fonts"
    if fonts_dir.is_dir():
        shutil.copytree(fonts_dir, target / "assets" / "vendor" / "fonts")

    if pyodide_vendored:
        shutil.copytree(cfg.ASSETS / "vendor" / "pyodide", target / "assets" / "vendor" / "pyodide")
    else:
        say("note: assets/vendor/pyodide/ not found (see "
            "write_dewmini_bundle()'s docstring for the fetch command) — "
            "the dewmini bundle will still boot Python from the CDN on "
            "first run rather than fully offline")

    coi_src = cfg.ASSETS / "vendor" / "coi-serviceworker.js"
    if coi_src.exists():
        shutil.copy2(coi_src, target / "coi-serviceworker.js")

    _reference_index_for_bundle(target)

    # serve.py — see SERVE_SCRIPT's own docstring for why a bundle needs it.
    (target / "serve.py").write_text(SERVE_SCRIPT)

    (target / "index.html").write_text(
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<title>dewlab Notebook</title>\n"
        "<style>body{font:15px/1.5 sans-serif;max-width:34rem;margin:3rem auto;padding:0 1rem;}"
        "code{background:#eee;padding:0.1rem 0.35rem;border-radius:3px;}</style>\n"
        "</head>\n"
        "<body>\n"
        '<div id="file-warning" hidden>\n'
        "<h1>One more step</h1>\n"
        "<p>Opening this file directly shows a blank page — the Notebook's own "
        "JavaScript needs a real (if entirely local) web server to load, "
        "which a browser won't do for a file opened straight off disk.</p>\n"
        "<p>Open a terminal in this folder and run:</p>\n"
        "<p><code>python3 serve.py</code></p>\n"
        "<p>That opens a browser tab with the Notebook in it. Leave the "
        "terminal window open while you use it.</p>\n"
        "</div>\n"
        "<script>\n"
        "if (window.location.protocol === \"file:\") {\n"
        '  document.getElementById("file-warning").hidden = false;\n'
        "} else {\n"
        '  window.location.replace("compose/notebook.html");\n'
        "}\n"
        "</script>\n"
        "<noscript><p>JavaScript is off, so this can't check what's needed automatically: "
        "run <code>python3 serve.py</code> in this folder from a terminal, then open the "
        "browser tab it starts, or (with JavaScript back on) open "
        '<a href="compose/notebook.html">the Notebook</a> directly once this is being served.</p></noscript>\n'
        "</body>\n"
        "</html>\n"
    )

    return target


def readable_size(path: Path) -> str:
    """A size a person can act on, rather than a byte count."""
    size = path.stat().st_size
    if size >= 1_000_000:
        return f"{size / 1_000_000:.0f} MB"
    return f"{max(size // 1000, 1)} KB"
