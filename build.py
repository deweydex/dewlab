#!/usr/bin/env python3
"""Turn the markdown in tutorials/ into the hosted HTML series in site/.

The shape of the job, from BUILD_PLAN.md Phase 1: read a tutorial's frontmatter
and body, turn its `exec`-tagged fences into cell objects, expand include
directives into the setup code they name, resolve cross-tutorial links to real
relative hrefs and fail on any that do not resolve, then render the result into
assets/shell.html.

Maths and illustrative code are lifted out of the source before the markdown
converter ever sees them, for the same reason cells are: `$a_i$` would otherwise
come back with the subscript turned into emphasis. Both are marked for the
runtime to finish — KaTeX for the maths, a read-only CodeMirror for the code —
rather than rendered here (DECISIONS_LOG 1.8).

The markup this emits for a cell, and the manifest it writes into the page, are
the contract the runtime reads (DECISIONS_LOG 0.23), and what the browser tests
in tests/e2e/ drive.

    python3 build.py            build into site/
    python3 build.py --clean    remove site/ first
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent
TUTORIALS = ROOT / "tutorials"
SETUP = ROOT / "setup"
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
SHELL = ASSETS / "shell.html"
OUT = ROOT / "site"

REQUIRED_FRONTMATTER = ("title", "slug", "module", "year", "series", "order", "version")

# ```python exec — the tag that makes a fence a live cell. An untagged fence is
# ordinary illustrative code and markdown renders it as it always would.
FENCE_RE = re.compile(r"^(?P<indent> *)```(?P<info>[^\n]*)\n(?P<body>.*?)^ *```[ \t]*$",
                      re.MULTILINE | re.DOTALL)
HEADER_RE = re.compile(r"^\s*(id|hint)\s*:\s*(.*)$")
INCLUDE_RE = re.compile(r"\{\{\s*include\s*:\s*(?P<path>[^}]+?)\s*\}\}")
# A list written directly under a line of prose, with no blank line between.
# Most markdown an author has written before — in a notebook, on GitHub — treats
# that as a list. This converter does not, and silently runs the items together
# into the paragraph instead, which is the kind of mistake nobody notices until
# a student is reading it. The blank line is inserted for them.
TIGHT_LIST_RE = re.compile(
    r"(?m)^(?P<prose>(?![ \t]*(?:[-*+]|\d+[.)])\s)(?![ \t]*#)(?![ \t]*>)[^\n]*\S[^\n]*)\n"
    r"(?P<item>[ \t]*(?:[-*+]|\d+[.)])\s+\S)"
)
TUTORIAL_HREF_RE = re.compile(r'href="tutorial:(?P<slug>[^"#]+)(?:#(?P<anchor>[^"]*))?"')
ID_RE = re.compile(r'\bid="([^"]+)"')
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ALT_RE = re.compile(r"\balt\s*=", re.IGNORECASE)

# Maths, matched only against prose — every fence is already out of the way by
# the time these run. Display first so $$…$$ is never read as two inline spans.
# Inline maths may not span a line, and may not open or close against a space,
# which is what keeps "it cost $5 or $6" out of it.
DISPLAY_MATH_RE = re.compile(r"\$\$(?P<tex>.+?)\$\$", re.DOTALL)
INLINE_MATH_RE = re.compile(r"\$(?!\s)(?P<tex>[^$\n]+?)(?<!\s)\$")
ESCAPED_DOLLAR = "\x00dldollar\x00"


class BuildError(Exception):
    """Something in the source is wrong. The build stops and says where."""


@dataclass
class Cell:
    id: str
    hint: str | None
    code: str


@dataclass
class CodeBlock:
    """An untagged fence: read-only, illustrative, no Run button."""

    language: str
    code: str


@dataclass
class Math:
    tex: str
    display: bool


@dataclass
class Tutorial:
    path: Path
    meta: dict
    cells: list[Cell]
    body_html: str
    has_math: bool = False
    anchors: set[str] = field(default_factory=set)

    @property
    def slug(self) -> str:
        return str(self.meta["slug"])

    @property
    def module(self) -> str:
        return str(self.meta["module"])

    @property
    def out_path(self) -> Path:
        return OUT / "tutorials" / self.module / f"{self.slug}.html"

    @property
    def module_title(self) -> str:
        """What a student sees. The slug is a folder name, not a course name.

        Optional, and any tutorial in the module may carry it — the first one
        that does, wins. Without it the slug is shown, which is honest but
        rarely what you would put in front of a class.
        """
        return str(self.meta.get("module_title") or self.module)

    @property
    def series(self) -> str:
        return str(self.meta["series"])

    @property
    def title(self) -> str:
        return str(self.meta["title"])

    @property
    def order(self) -> int:
        try:
            return int(self.meta["order"])
        except (TypeError, ValueError):
            fail(self.path, f"order must be a whole number, not {self.meta['order']!r}")
            raise  # unreachable; fail() always raises

    @property
    def depth(self) -> int:
        """How many directories deep the built page sits under site/."""
        return len(self.out_path.relative_to(OUT).parts) - 1


def fail(path: Path, message: str) -> None:
    raise BuildError(f"{path.relative_to(ROOT)}: {message}")


# ------------------------------------------------------------------ parsing


def split_frontmatter(text: str, path: Path) -> tuple[dict, str]:
    if not text.startswith("---"):
        fail(path, "no YAML frontmatter — the file must open with a --- line")
    end = text.find("\n---", 3)
    if end == -1:
        fail(path, "frontmatter is never closed with a --- line")
    raw, body = text[3:end], text[end + 4 :]
    try:
        meta = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        fail(path, f"frontmatter is not valid YAML: {exc}")
    if not isinstance(meta, dict):
        fail(path, "frontmatter must be a mapping of fields")
    missing = [f for f in REQUIRED_FRONTMATTER if f not in meta]
    if missing:
        fail(path, f"frontmatter is missing {', '.join(missing)}")
    return meta, body.lstrip("\n")


def loosen_tight_lists(body: str) -> str:
    """Give a list that starts straight after a paragraph the blank line it needs."""
    previous = None
    while previous != body:
        previous = body
        body = TIGHT_LIST_RE.sub(lambda m: f"{m.group('prose')}\n\n{m.group('item')}", body)
    return body


def expand_includes(code: str, path: Path) -> str:
    """Replace {{include: setup/x.py}} with the contents of that file.

    De-duplicates the source, not the runtime: the expanded cell still executes
    on every page load (CONTENT_AND_FILE_ARCHITECTURE.md).
    """

    def one(match: re.Match) -> str:
        rel = match.group("path").strip()
        target = (ROOT / rel).resolve()
        if not str(target).startswith(str(ROOT)):
            fail(path, f"include escapes the repository: {rel}")
        if not target.is_file():
            fail(path, f"include names a file that does not exist: {rel}")
        return target.read_text().strip("\n")

    return INCLUDE_RE.sub(one, code)


def parse_cell(body: str, path: Path) -> Cell:
    """Read `id:` and optional `hint:` off the top of an exec fence."""
    lines = body.split("\n")
    header: dict[str, str] = {}
    while lines:
        match = HEADER_RE.match(lines[0])
        if not match or match.group(1) in header:
            break
        header[match.group(1)] = match.group(2).strip()
        lines.pop(0)
    if "id" not in header:
        fail(path, "an exec cell has no `id:` line — ids are what saved progress matches on")
    code = expand_includes("\n".join(lines).strip("\n"), path)
    return Cell(id=header["id"], hint=header.get("hint") or None, code=code)


def extract_blocks(body: str, path: Path) -> tuple[str, list[Cell], list[CodeBlock]]:
    """Pull every fence out, leaving a comment placeholder markdown will keep.

    An `exec` fence becomes a cell; any other fence becomes an illustrative,
    read-only block. Both leave the source before the markdown converter runs,
    so nothing inside either can be reinterpreted as markup.
    """
    cells: list[Cell] = []
    blocks: list[CodeBlock] = []

    def one(match: re.Match) -> str:
        info = match.group("info").strip().split()
        indent = match.group("indent")
        if "exec" in info:
            cells.append(parse_cell(match.group("body"), path))
            return f"{indent}<!--dewlab-cell-{len(cells) - 1}-->"
        language = info[0] if info else ""
        blocks.append(CodeBlock(language=language, code=match.group("body").strip("\n")))
        return f"{indent}<!--dewlab-code-{len(blocks) - 1}-->"

    rewritten = FENCE_RE.sub(one, body)
    seen: set[str] = set()
    for cell in cells:
        if cell.id in seen:
            fail(path, f"two exec cells share the id {cell.id!r}")
        seen.add(cell.id)
    return rewritten, cells, blocks


def extract_math(body: str) -> tuple[str, list[Math]]:
    """Lift $…$ and $$…$$ out, leaving a token markdown will not touch.

    The placeholder is a bare alphanumeric word on purpose: an HTML comment
    works for a block-level fence but not mid-sentence, where markdown's inline
    pass can reach it.
    """
    found: list[Math] = []
    body = body.replace("\\$", ESCAPED_DOLLAR)

    def take(display: bool):
        def one(match: re.Match) -> str:
            found.append(Math(tex=match.group("tex").strip(), display=display))
            return f"dlmath{len(found) - 1}z"

        return one

    body = DISPLAY_MATH_RE.sub(take(True), body)
    body = INLINE_MATH_RE.sub(take(False), body)
    return body.replace(ESCAPED_DOLLAR, "$"), found


# ----------------------------------------------------------------- rendering


def render_cell(cell: Cell) -> str:
    """The markup the runtime binds an editor, a Run button and an output area to."""
    safe_id = html.escape(cell.id, quote=True)
    hint_markup = ""
    if cell.hint:
        hint_markup = (
            '<span class="dl-hint">'
            f'<button type="button" class="dl-hint-icon" aria-label="Hint for {safe_id}">?</button>'
            f'<span class="dl-hint-text" role="tooltip">{html.escape(cell.hint)}</span>'
            "</span>"
        )
    return (
        f'<div class="dl-cell" data-cell-id="{safe_id}">'
        '<div class="dl-cell-bar">'
        f'<span class="dl-cell-id">{safe_id}</span>'
        '<span class="dl-cell-spacer"></span>'
        f"{hint_markup}"
        '<button type="button" class="dl-btn dl-btn-reset">reset</button>'
        '<button type="button" class="dl-btn dl-btn-run" disabled>…</button>'
        "</div>"
        '<div class="dl-editor"></div>'
        '<div class="dl-output"></div>'
        "</div>"
    )


def render_code_block(block: CodeBlock) -> str:
    """Illustrative code. The runtime swaps in a read-only CodeMirror over it.

    The escaped source stays in the markup rather than travelling in the
    manifest, so a reader with no JavaScript still sees the code, correctly
    escaped, instead of an empty box.
    """
    lang = html.escape(block.language, quote=True)
    attr = f' data-lang="{lang}"' if lang else ""
    return f'<pre class="dl-static"{attr}><code>{html.escape(block.code)}</code></pre>'


def render_math(item: Math) -> str:
    """A marked span. KaTeX replaces its contents in the browser.

    Until then — and permanently, without JavaScript — the span holds the
    source TeX, which is a far better fallback than a blank gap.
    """
    classes = "dl-math dl-math-display" if item.display else "dl-math"
    return f'<span class="{classes}">{html.escape(item.tex)}</span>'


def to_html(body: str) -> str:
    converter = markdown.Markdown(extensions=["extra", "sane_lists", "toc"])
    return converter.convert(body)


def place_blocks(
    page_html: str, cells: list[Cell], blocks: list[CodeBlock], maths: list[Math]
) -> str:
    for index, cell in enumerate(cells):
        placeholder = f"<!--dewlab-cell-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"cell {cell.id!r} was lost during markdown conversion")
        page_html = page_html.replace(placeholder, render_cell(cell))
    for index, block in enumerate(blocks):
        page_html = page_html.replace(f"<!--dewlab-code-{index}-->", render_code_block(block))
    for index, item in enumerate(maths):
        page_html = page_html.replace(f"dlmath{index}z", render_math(item))
    return page_html


# -------------------------------------------------------------- navigation


def series_of(tutorials: list[Tutorial]) -> dict[tuple[str, str], list[Tutorial]]:
    """Group tutorials into the series a student actually works through.

    A series is per module: two modules may both have a series called
    `fundamentals` without being the same sequence.
    """
    groups: dict[tuple[str, str], list[Tutorial]] = {}
    for tutorial in tutorials:
        groups.setdefault((tutorial.module, tutorial.series), []).append(tutorial)
    for members in groups.values():
        # Title breaks a tie, so the sequence is at least stable and repeatable.
        # Two tutorials sharing a position is worth mentioning but not worth
        # stopping for: the pages still build and still link to each other, the
        # author just did not choose which came first. That is a different kind
        # of mistake from a dead link, and deserves a different response.
        members.sort(key=lambda t: (t.order, t.title))
        seen: dict[int, Tutorial] = {}
        for member in members:
            if member.order in seen:
                print(
                    f"note: {member.path.relative_to(ROOT)} and "
                    f"{seen[member.order].path.name} are both order {member.order}; "
                    "ordering them by title",
                    file=sys.stderr,
                )
            seen.setdefault(member.order, member)
    return groups


def link_between(here: Tutorial, there: Tutorial) -> str:
    return os.path.relpath(there.out_path, here.out_path.parent)


def nav_for(tutorial: Tutorial, members: list[Tutorial]) -> str:
    """Previous and next within the series, and the way back to the contents."""
    index = members.index(tutorial)
    parts = []
    if index > 0:
        previous = members[index - 1]
        parts.append(
            f'<a class="dl-nav-prev" href="{link_between(tutorial, previous)}">'
            f"{html.escape(previous.title)}</a>"
        )
    up = "../" * tutorial.depth
    parts.append(f'<a class="dl-nav-up" href="{up}index.html">All tutorials</a>')
    parts.append(
        f'<a class="dl-download" href="{up}download/{tutorial.slug}.html" download>'
        "Download this tutorial</a>"
    )
    if index < len(members) - 1:
        following = members[index + 1]
        parts.append(
            f'<a class="dl-nav-next" href="{link_between(tutorial, following)}">'
            f"{html.escape(following.title)}</a>"
        )
    return "".join(parts)


def render_index(
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path] | None = None,
) -> str:
    """The contents page: every module, every series, in order.

    `archives` maps a series to its zip of downloadable copies, when the build
    wrote them. Without it the page simply carries no whole-series link, which
    is what a quick local build wants.
    """
    archives = archives or {}
    if not groups:
        return "<p>No tutorials have been written yet.</p>"

    names = {}
    for (module, _), members in groups.items():
        for member in members:
            if member.meta.get("module_title"):
                names.setdefault(module, member.module_title)

    out = ["<h1>Tutorials</h1>"]
    for module in sorted({module for module, _ in groups}):
        out.append(f"<h2>{html.escape(names.get(module, module))}</h2>")
        for (owner, series), members in sorted(groups.items()):
            if owner != module:
                continue
            if len({s for m, s in groups if m == module}) > 1:
                out.append(f'<h3>{html.escape(series)}</h3>')
            out.append('<ol class="dl-contents">')
            for member in members:
                href = member.out_path.relative_to(OUT).as_posix()
                out.append(
                    f'<li><a href="{href}">{html.escape(member.title)}</a></li>'
                )
            out.append("</ol>")
            archive = archives.get((owner, series))
            if archive is not None:
                count = len(members)
                out.append(
                    '<p class="dl-series">'
                    f'<a class="dl-download" href="download/{archive.name}" download>'
                    f"Download all {count} as single files"
                    f" ({readable_size(archive)})</a></p>"
                )
    return "\n".join(out)


# ------------------------------------------------------------------- checks


def check_alt_text(tutorial: Tutorial) -> None:
    """Every image declares alt. An explicit alt="" marks a decorative one."""
    for tag in IMG_RE.findall(tutorial.body_html):
        if not ALT_RE.search(tag):
            fail(tutorial.path, f"image has no alt attribute: {tag}")


def resolve_links(tutorial: Tutorial, registry: dict[str, Tutorial]) -> str:
    """Rewrite tutorial:slug#anchor into a real relative href, or fail."""

    def one(match: re.Match) -> str:
        slug, anchor = match.group("slug"), match.group("anchor")
        target = registry.get(slug)
        if target is None:
            known = ", ".join(sorted(registry)) or "none"
            fail(tutorial.path, f"link to unknown tutorial {slug!r} (built: {known})")
        if anchor and anchor not in target.anchors:
            fail(
                tutorial.path,
                f"link to {slug}#{anchor} — that tutorial has no anchor {anchor!r}",
            )
        href = os.path.relpath(target.out_path, tutorial.out_path.parent)
        return f'href="{href}#{anchor}"' if anchor else f'href="{href}"'

    return TUTORIAL_HREF_RE.sub(one, tutorial.body_html)


# -------------------------------------------------------------------- build


def load(path: Path) -> Tutorial:
    meta, body = split_frontmatter(path.read_text(), path)
    stripped, cells, blocks = extract_blocks(body, path)
    stripped, maths = extract_math(stripped)
    stripped = loosen_tight_lists(stripped)
    body_html = place_blocks(to_html(stripped), cells, blocks, maths)
    anchors = set(ID_RE.findall(body_html)) | {c.id for c in cells}
    return Tutorial(
        path=path,
        meta=meta,
        cells=cells,
        body_html=body_html,
        has_math=bool(maths),
        anchors=anchors,
    )


def write(tutorial: Tutorial, shell: str, body_html: str, nav: str = "") -> Path:
    up = "../" * tutorial.depth
    manifest: dict[str, object] = {
        "slug": tutorial.slug,
        "version": tutorial.meta["version"],
        "assetBase": f"{up}assets/",
        "dataBase": f"{up}data/",
        "cells": [{"id": c.id, "hint": c.hint, "code": c.code} for c in tutorial.cells],
    }
    if tutorial.has_math:
        # The runtime fetches the 266 KB KaTeX bundle only when this is set, so
        # a tutorial with no maths never pays for it.
        manifest["math"] = True
    packages = tutorial.meta.get("packages")
    if packages:
        manifest["packages"] = list(packages)

    tokens = {
        "{{TITLE}}": html.escape(str(tutorial.meta["title"])),
        "{{VERSION}}": html.escape(str(tutorial.meta["version"]), quote=True),
        "{{SLUG}}": html.escape(tutorial.slug, quote=True),
        "{{MODULE}}": html.escape(tutorial.module, quote=True),
        "{{YEAR}}": html.escape(str(tutorial.meta["year"]), quote=True),
        "{{SERIES}}": html.escape(str(tutorial.meta["series"]), quote=True),
        "{{ASSET_BASE}}": f"{up}assets/",
        "{{ROOT_BASE}}": up,
        "{{CRUMBS}}": html.escape(f"{tutorial.module_title} · {tutorial.meta['year']}"),
        "{{NAV_PREV_NEXT}}": nav,
        "{{BODY}}": body_html,
        # `<` escaped so nothing in a cell can close the surrounding <script>.
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(f"shell template has tokens build.py does not fill: {leftover}")

    tutorial.out_path.parent.mkdir(parents=True, exist_ok=True)
    tutorial.out_path.write_text(page)
    return tutorial.out_path


# --------------------------------------------------------------- standalone

# A page opened from a file cannot load an ES module, fetch a neighbouring
# file, or resolve a relative link to a page that is not there. A standalone
# export therefore carries everything inside it and drops what it cannot honour.
PYODIDE_CLASSIC = (
    '<script src="https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js"></script>'
)
FONT_URL_RE = re.compile(r"url\((?P<quote>['\"]?)fonts/(?P<name>[\w.-]+\.woff2)(?P=quote)\)")


def inline_katex_css() -> str:
    """KaTeX's stylesheet with its fonts folded in as data.

    Only the woff2 files it actually names, which is what keeps this to a few
    hundred kilobytes rather than the whole family.
    """
    css = (ASSETS / "vendor" / "katex.min.css").read_text()

    def one(match: re.Match) -> str:
        font = ASSETS / "vendor" / "fonts" / match.group("name")
        if not font.is_file():
            return match.group(0)
        data = base64.b64encode(font.read_bytes()).decode("ascii")
        return f"url(data:font/woff2;base64,{data})"

    return FONT_URL_RE.sub(one, css)


def standalone_html(tutorial: Tutorial, page: str) -> str:
    """Turn a built page into one file that works from a student's disk."""
    # The same prefix build.py wrote into the page's own asset references.
    up = "../" * tutorial.depth + "assets/"
    style = (ASSETS / "tutorial-style.css").read_text()
    bundle = (ASSETS / "vendor" / "standalone.bundle.js").read_text()
    tools = (ASSETS / "tutorial_tools.py").read_text()

    # The stylesheets, inlined. KaTeX's only travels with a page that has maths.
    page = page.replace(
        f'<link rel="stylesheet" href="{up}vendor/katex.min.css">',
        f"<style>{inline_katex_css()}</style>" if tutorial.has_math else "",
    )
    page = page.replace(
        f'<link rel="stylesheet" href="{up}tutorial-style.css">',
        f"<style>{style}</style>",
    )

    # The runtime, as a classic script, behind Pyodide's classic loader.
    page = page.replace(
        f'<script type="module" src="{up}tutorial-runtime.js"></script>',
        PYODIDE_CLASSIC + "\n<script>" + bundle + "</script>",
    )

    # The Python tools, which cannot be fetched from a file.
    marker = '<script type="application/json" id="dewlab-manifest">'
    start = page.index(marker) + len(marker)
    end = page.index("</script>", start)
    manifest = json.loads(page[start:end])
    manifest["toolsSource"] = tools
    manifest["standalone"] = True
    page = page[:start] + json.dumps(manifest).replace("<", "\\u003c") + page[end:]

    # Navigation points at pages that are not beside this file, and the offer to
    # download it is already taken. Both go rather than break.
    page = re.sub(r"<nav class=\"dl-nav[^\"]*\">.*?</nav>", "", page, flags=re.DOTALL)
    page = re.sub(r'<a class="dl-download".*?</a>', "", page, flags=re.DOTALL)
    root = "../" * tutorial.depth
    page = page.replace(f'href="{root}index.html"', 'href="#" onclick="return false"')
    return page


def write_standalone(tutorial: Tutorial, page: str) -> Path:
    # A standalone file carries the page but not the /data/ folder beside it, so
    # a tutorial that loads a dataset at runtime will read fine and fail at that
    # cell. Better said at build time than discovered by a student.
    if any("load_csv" in cell.code for cell in tutorial.cells):
        print(
            f"note: {tutorial.path.relative_to(ROOT)} loads a dataset, which its "
            "downloadable copy cannot reach — that cell will fail when the file "
            "is opened from disk",
            file=sys.stderr,
        )

    target = OUT / "download" / f"{tutorial.slug}.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(standalone_html(tutorial, page))
    return target


SERIES_SLUG_RE = re.compile(r"[^a-z0-9]+")


def series_slug(module: str, series: str) -> str:
    """A filename for a whole series, out of names that were written for people."""
    slug = SERIES_SLUG_RE.sub("-", f"{module}-{series}".lower()).strip("-")
    return slug or "tutorials"


def write_series_zip(module: str, series: str, members: list[Tutorial]) -> Path:
    """Every downloadable copy in one series, gathered into one archive.

    A student takes one tutorial. Somebody setting up a room, or filling a
    memory stick for a class with no reliable connection, wants the set. The
    archive holds the very files the download links point at, so there is no
    second copy to keep in step with anything.
    """
    folder = series_slug(module, series)
    target = OUT / "download" / f"{folder}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for member in members:
            archive.write(
                OUT / "download" / f"{member.slug}.html", f"{folder}/{member.slug}.html"
            )
    return target


def readable_size(path: Path) -> str:
    """A size a person can act on, rather than a byte count."""
    size = path.stat().st_size
    if size >= 1_000_000:
        return f"{size / 1_000_000:.0f} MB"
    return f"{max(size // 1000, 1)} KB"


def write_index(
    shell: str,
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path] | None = None,
) -> Path:
    """The contents page at the site root, which every page's masthead links to."""
    manifest = {"slug": "index", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": []}
    tokens = {
        "{{TITLE}}": "Tutorials",
        "{{VERSION}}": "1",
        "{{SLUG}}": "index",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": "contents",
        "{{ASSET_BASE}}": "assets/",
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": "",
        "{{BODY}}": render_index(groups, archives),
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(f"shell template has tokens the index does not fill: {leftover}")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "index.html"
    target.write_text(page)
    return target


def build(clean: bool = False, standalone: bool = False) -> list[Path]:
    """Build the site. `standalone` also writes the downloadable single files,
    which need the real assets on disk and are the slow part of a build."""
    if not SHELL.is_file():
        raise BuildError(f"no shell template at {SHELL.relative_to(ROOT)}")
    if clean and OUT.exists():
        shutil.rmtree(OUT)

    sources = sorted(TUTORIALS.rglob("*.md"))
    tutorials = [load(p) for p in sources]

    registry: dict[str, Tutorial] = {}
    for tutorial in tutorials:
        if tutorial.slug in registry:
            fail(tutorial.path, f"slug {tutorial.slug!r} is already used by "
                                f"{registry[tutorial.slug].path.relative_to(ROOT)}")
        registry[tutorial.slug] = tutorial

    shell = SHELL.read_text()
    groups = series_of(tutorials)
    written: list[Path] = []
    for tutorial in tutorials:
        check_alt_text(tutorial)
        members = groups[(tutorial.module, tutorial.series)]
        page_path = write(
            tutorial, shell, resolve_links(tutorial, registry), nav_for(tutorial, members)
        )
        written.append(page_path)
        if standalone:
            written.append(write_standalone(tutorial, page_path.read_text()))

    archives: dict[tuple[str, str], Path] = {}
    if standalone:
        for key, members in groups.items():
            archives[key] = write_series_zip(key[0], key[1], members)
        written.extend(archives.values())

    if tutorials:
        written.append(write_index(shell, groups, archives))

    OUT.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(OUT / "assets", ignore_errors=True)
    shutil.copytree(ASSETS, OUT / "assets", ignore=shutil.ignore_patterns("shell.html"))
    if DATA.is_dir():
        shutil.rmtree(OUT / "data", ignore_errors=True)
        shutil.copytree(DATA, OUT / "data")
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--clean", action="store_true", help="remove site/ before building")
    parser.add_argument(
        "--no-standalone",
        action="store_true",
        help="skip the downloadable single-file copies, which are the slow part",
    )
    args = parser.parse_args()
    try:
        written = build(clean=args.clean, standalone=not args.no_standalone)
    except BuildError as exc:
        print(f"build failed — {exc}", file=sys.stderr)
        return 1
    if not written:
        print("nothing to build: tutorials/ holds no .md files")
        return 0
    for path in written:
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"{len(written)} page{'s' if len(written) != 1 else ''} into {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
