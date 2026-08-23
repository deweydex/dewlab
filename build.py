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
import hashlib
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

REQUIRED_FRONTMATTER = ("title", "slug", "module", "year", "series", "version")

# What a tutorial is for. `live` is the normal state and the default, so nothing
# already written has to say anything. `archived` means superseded: still built,
# still reachable, still holding whatever a student saved in it, but out of the
# reading order and marked as no longer part of the course.
#
# This exists because deleting the file was the only way to retire a tutorial,
# and deleting it strands every student who saved work in it — their work sits
# in local storage keyed to a page that no longer exists, with no way back and
# no trace it was ever there (planning/VERSIONS.md).
STATUSES = ("draft", "beta", "live", "archived")

# A version is a release, not a save: the date a cohort could first see it,
# plus which release of that day it was. The date is the whole identity — "3"
# means nothing to a student and "September" means a good deal
# (planning/VERSIONS.md).
VERSION_RE = re.compile(r"^(?P<y>\d{4})\.(?P<m>\d{2})\.(?P<d>\d{2})\.(?P<n>\d+)$")

# `order` used to live here. It moved into one file per series, so a tutorial
# that still carries it is half-migrated — and the half that is not migrated is
# the half that would be silently ignored.
MOVED_FRONTMATTER = {
    "order": "the series' .order.yaml file, which lists slugs in reading order",
}

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
DETAILS_RE = re.compile(r"<details\b[^>]*>", re.IGNORECASE)
# The two folds a page may use. A hint offers the steps; an answer gives the
# answer. Both are styled from their class, so a fold without one renders as a
# bare browser triangle in the middle of the prose.
FOLD_CLASSES = ("dl-hint", "dl-answer")

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
    toc: list = field(default_factory=list)
    # Where this sits in its series. Not from the frontmatter — the order file
    # decides it, and series_of() fills it in once the series is assembled.
    order: int = 0
    # Whether this is the version the unversioned URL serves. Set by
    # versions_of() once every version of a tutorial has been read, because it
    # cannot be known from one file alone.
    is_default: bool = True

    @property
    def slug(self) -> str:
        return str(self.meta["slug"])

    @property
    def module(self) -> str:
        return str(self.meta["module"])

    # Whether this is the version the unversioned URL serves. Set by
    # versions_of() once every version of a tutorial has been read, because it
    # cannot be known from one file alone.
    @property
    def out_path(self) -> Path:
        """The default sits at the tutorial's own URL; other versions sit under
        it. So every link written before versions existed — in a tutorial, on
        the topic tree, in a student's bookmarks — keeps working and keeps
        meaning "the current one"."""
        here = OUT / "tutorials" / self.module
        if self.is_default:
            return here / f"{self.slug}.html"
        return here / self.slug / f"v{self.version}.html"

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
    def status(self) -> str:
        return str(self.meta.get("status", "live"))

    @property
    def archived(self) -> bool:
        return self.status == "archived"

    @property
    def practice_for(self) -> str:
        """The slug of the tutorial this page sets problems on, or "".

        A practice page is a tutorial in every mechanical sense — same
        frontmatter, same cells, same saved work — and belongs to a tutorial
        rather than to a series. So it is built and reachable and linked, and it
        is not on the reading order, which is the same shape an archived
        tutorial already has.
        """
        return str(self.meta.get("practice_for") or "")

    @property
    def practice_across(self) -> tuple[str, ...]:
        """The slugs a mixed problem set draws on, or ().

        Most practice belongs to one tutorial. Some does not: a set of problems
        that is only worth doing once several tutorials are behind you has no
        single owner, and giving it one would be a lie about what it needs.

        Mechanically it is the same shape as `practice_for` — off the reading
        order, no coverage of its own, linked to what it draws on — except that
        it points at several tutorials and none of them points back. A tutorial
        has one companion page of problems; a mixed set is not it.
        """
        value = self.meta.get("practice_across") or []
        if isinstance(value, str):
            value = [value]
        return tuple(str(s) for s in value)

    @property
    def is_practice(self) -> bool:
        """Whether this page sets problems rather than teaching."""
        return bool(self.practice_for or self.practice_across)

    @property
    def version(self) -> str:
        return str(self.meta["version"])

    @property
    def released(self) -> tuple[int, int, int, int]:
        """The version as something sortable. Numbers, not the string, so
        2026.09.02.1 sorts before 2026.09.15.1 rather than after it."""
        m = VERSION_RE.match(self.version)
        return tuple(int(m.group(g)) for g in ("y", "m", "d", "n"))

    @property
    def date(self) -> str:
        """What a student reads: 15 September 2026."""
        year, month, day, _ = self.released
        months = ("January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December")
        return f"{day} {months[month - 1]} {year}"

    @property
    def title(self) -> str:
        return str(self.meta["title"])

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
    for field_name, moved_to in MOVED_FRONTMATTER.items():
        if field_name in meta:
            fail(path, f"{field_name} no longer belongs in frontmatter — it moved "
                       f"to {moved_to}")
    status = meta.get("status", "live")
    if status not in STATUSES:
        fail(path, f"status {status!r} is not one of {', '.join(STATUSES)}")
    version = str(meta.get("version", ""))
    if not VERSION_RE.match(version):
        fail(path, f"version {version!r} is not a release date — it should look "
                   "like 2026.09.15.1 (year, month, day, which release of that day)")
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


def to_html(body: str) -> tuple[str, list]:
    """The page's HTML, and the heading tree the `toc` extension collected.

    The tree comes free — the extension is already here to give headings their
    ids, which is what makes `tutorial:slug#anchor` links and the curriculum
    map's section links possible. Taking its tokens as well means the contents
    list on the page is built from the same headings the anchors came from,
    rather than from a second pass that could disagree with them.
    """
    converter = markdown.Markdown(extensions=["extra", "sane_lists", "toc"])
    html_out = converter.convert(body)
    return html_out, list(getattr(converter, "toc_tokens", []))


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


ORDER_SUFFIX = ".order.yaml"


MODULE_ORDER_FILE = "modules.yaml"


def module_order() -> list[str]:
    """The order modules appear in, from `tutorials/modules.yaml`.

    Optional: without it the contents page falls back to alphabetical, which is
    what it did before and is at least stable.

    The path is worked out here rather than held in a constant beside TUTORIALS,
    because the tests point TUTORIALS at a temporary directory and a constant
    computed at import time would still be looking at the real one.
    """
    path = TUTORIALS / MODULE_ORDER_FILE
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text()) or {}
    listed = data.get("order") or []
    if not isinstance(listed, list) or not all(isinstance(m, str) for m in listed):
        fail(path, "a module order file needs `order:` as a list of module names")
    return listed


def order_files() -> dict[tuple[str, str], list[str]]:
    """The reading order of each series, read from one file per series.

    Order used to live in every tutorial's own frontmatter, which meant
    inserting one in the middle was an edit to every file after it. In one list
    per series, moving a tutorial is moving a line and inserting one is adding
    a line — which is what makes reordering something an editor can do, and
    something a person can still do by hand in the GitHub web editor.
    """
    found: dict[tuple[str, str], list[str]] = {}
    for path in sorted(TUTORIALS.rglob(f"*{ORDER_SUFFIX}")):
        data = yaml.safe_load(path.read_text()) or {}
        module = path.parent.name
        series = path.name[: -len(ORDER_SUFFIX)]
        # `order:` with nothing under it is a series whose every tutorial has
        # been archived. That is a real state and should not force somebody to
        # delete the file as well — but `order:` missing altogether is still a
        # broken file, so the two are told apart rather than both allowed.
        if "order" not in data:
            fail(path, "an order file needs `order:` as a list of slugs")
        order = data.get("order") or []
        if not isinstance(order, list) or not all(isinstance(s, str) for s in order):
            fail(path, "an order file needs `order:` as a list of slugs")
        if len(set(order)) != len(order):
            duplicates = sorted({s for s in order if order.count(s) > 1})
            fail(path, f"lists {', '.join(duplicates)} more than once")
        found[(module, series)] = order
    return found


def series_titles() -> dict[tuple[str, str], str]:
    """What each series is called, from the `series:` line in its order file.

    The slug is a filename. "reflections-and-review" is fine in a path and
    wrong in a heading, and until a module had two series nobody saw the
    heading at all.
    """
    titles: dict[tuple[str, str], str] = {}
    for path in sorted(TUTORIALS.rglob(f"*{ORDER_SUFFIX}")):
        data = yaml.safe_load(path.read_text()) or {}
        name = data.get("series")
        if isinstance(name, str) and name.strip():
            titles[(path.parent.name, path.name[: -len(ORDER_SUFFIX)])] = name.strip()
    return titles


def versions_of(tutorials: list[Tutorial]) -> list[Tutorial]:
    """Group every file by the tutorial it is a version of, and decide which
    version the unversioned URL serves.

    **The default is the newest `live` version.** Usually that is the only
    version there is. Where it is not, the rule does the work the beta workflow
    needs with no extra machinery: freeze the current release, mark the working
    copy `beta`, and students keep getting the frozen live one until the beta is
    promoted.

    Returns everything that gets built, with `is_default` set. Drafts are gone
    by the time this runs — see `load_all`.
    """
    families: dict[tuple[str, str], list[Tutorial]] = {}
    for tutorial in tutorials:
        families.setdefault((tutorial.module, tutorial.slug), []).append(tutorial)

    built: list[Tutorial] = []
    for (module, slug), versions in sorted(families.items()):
        seen = {}
        for version in versions:
            if version.version in seen:
                fail(version.path, f"is version {version.version} of {slug}, and so "
                                   f"is {seen[version.version].path.relative_to(ROOT)}. "
                                   "Two releases cannot share a date and a number.")
            seen[version.version] = version

        newest_live = max(
            (v for v in versions if v.status == "live"), key=lambda v: v.released,
            default=None,
        )
        # Nothing live: a tutorial that is entirely beta, or entirely archived.
        # The newest of what there is still answers the unversioned URL, because
        # a link that 404s is worse than a link to something marked clearly.
        default = newest_live or max(versions, key=lambda v: v.released)
        for version in versions:
            version.is_default = version is default
        built.extend(versions)
    return built


def practice_pairs(
    tutorials: list[Tutorial], registry: dict[tuple[str, str], Tutorial]
) -> dict[tuple[str, str], Tutorial]:
    """Each tutorial's page of problems, by the tutorial it belongs to.

    A practice page names its tutorial with `practice_for:`. Both directions are
    checked here rather than being discovered by a reader following a link that
    goes nowhere: the tutorial has to exist, it has to be in the same module,
    and no two practice pages may claim the same one.

    A practice page also declares no coverage. It sets problems on what its
    tutorial taught, and counting it would report the same outcome as taught
    twice — see `planning/EXERCISES.md`.
    """
    pairs: dict[tuple[str, str], Tutorial] = {}
    for page in tutorials:
        target = page.practice_for
        if target and page.practice_across:
            fail(page.path, "sets both practice_for and practice_across. A page "
                            "of problems either belongs to one tutorial or "
                            "draws on several; it cannot do both.")
        if not target or not page.is_default:
            continue
        if page.meta.get("covers"):
            fail(page.path, "is a practice page and declares `covers:`. It sets "
                            "problems on what its tutorial taught; saying so "
                            "twice would report one outcome as covered by two "
                            "pages.")
        if target == page.slug:
            fail(page.path, f"has practice_for: {target}, which is itself.")
        owner = registry.get((page.module, target))
        if owner is None:
            fail(page.path, f"has practice_for: {target}, and no tutorial in "
                            f"{page.module} has that slug.")
        if owner.practice_for:
            fail(page.path, f"has practice_for: {target}, which is itself a "
                            "practice page. Problems about problems is not a "
                            "shape this supports.")
        key = (page.module, target)
        if key in pairs:
            fail(page.path, f"has practice_for: {target}, and so does "
                            f"{pairs[key].path.relative_to(ROOT)}. A tutorial "
                            "has one page of problems.")
        pairs[key] = page
    return pairs


def mixed_practice(
    tutorials: list[Tutorial], registry: dict[tuple[str, str], Tutorial]
) -> dict[str, list[Tutorial]]:
    """Problem sets that draw on several tutorials, per module, in title order.

    Checked the same way as `practice_for`: every slug it names has to exist, be
    in the same module, and be a tutorial rather than another page of problems.
    A set naming one tutorial is an error rather than an eccentricity — that is
    what `practice_for` is, and having two ways to say it would mean a tutorial
    could quietly acquire a second companion page.
    """
    out: dict[str, list[Tutorial]] = {}
    for page in tutorials:
        across = page.practice_across
        if not across or not page.is_default:
            continue
        if page.meta.get("covers"):
            fail(page.path, "is a practice page and declares `covers:`. It sets "
                            "problems on what its tutorials taught; saying so "
                            "twice would report one outcome as covered by two "
                            "pages.")
        if len(across) < 2:
            fail(page.path, "has practice_across naming one tutorial. That is "
                            "what practice_for is for.")
        if len(set(across)) != len(across):
            repeated = sorted({s for s in across if across.count(s) > 1})
            fail(page.path, f"names {', '.join(repeated)} in practice_across "
                            "more than once.")
        for slug in across:
            if slug == page.slug:
                fail(page.path, f"has practice_across naming {slug}, which is "
                                "itself.")
            owner = registry.get((page.module, slug))
            if owner is None:
                fail(page.path, f"has practice_across naming {slug}, and no "
                                f"tutorial in {page.module} has that slug.")
            if owner.is_practice:
                fail(page.path, f"has practice_across naming {slug}, which is "
                                "itself a page of problems.")
        out.setdefault(page.module, []).append(page)
    for members in out.values():
        members.sort(key=lambda t: t.title)
    return out


def archived_of(tutorials: list[Tutorial]) -> dict[str, list[Tutorial]]:
    """Retired tutorials, per module, newest title order.

    Kept apart from the series rather than filtered out of it, because they are
    still built and still reachable — a student who saved work in one can still
    get to it. They simply are not part of the course any more.
    """
    out: dict[str, list[Tutorial]] = {}
    for tutorial in tutorials:
        if tutorial.archived and tutorial.is_default:
            out.setdefault(tutorial.module, []).append(tutorial)
    for members in out.values():
        members.sort(key=lambda t: t.title)
    return out


def series_of(tutorials: list[Tutorial]) -> dict[tuple[str, str], list[Tutorial]]:
    """Group the live tutorials into the series a student works through.

    A series is per module: two modules may both have a series called
    `fundamentals` without being the same sequence.

    Archived tutorials are not here. A reading order is a route through the
    course, and a retired tutorial is not on the route — so it is not listed in
    the order file, and listing it is an error rather than a no-op.
    """
    orders = order_files()
    groups: dict[tuple[str, str], list[Tutorial]] = {}
    for tutorial in tutorials:
        # Only the current, live version of each tutorial is on the route. A
        # superseded release is still readable; it is not part of the course.
        if tutorial.status != "live" or not tutorial.is_default:
            continue
        # A practice page hangs off its tutorial rather than sitting between two
        # others. Putting it on the route would double the length of every
        # series and put a page of problems between a reader and the next thing
        # they are meant to learn.
        if tutorial.is_practice:
            continue
        groups.setdefault((tutorial.module, tutorial.series), []).append(tutorial)

    # The contradictory case, caught by name so the message can say which.
    for tutorial in tutorials:
        if not tutorial.archived or not tutorial.is_default:
            continue
        listed = orders.get((tutorial.module, tutorial.series)) or []
        if tutorial.slug in listed:
            fail(
                TUTORIALS / tutorial.module / f"{tutorial.series}{ORDER_SUFFIX}",
                f"lists {tutorial.slug}, which is archived. An archived tutorial "
                "is not part of the reading order — remove the line, or take "
                "`status: archived` out of the tutorial.",
            )

    for key, members in groups.items():
        module, series = key
        listed = orders.get(key)
        if listed is None:
            fail(
                members[0].path,
                f"series {series!r} in {module} has no "
                f"{series}{ORDER_SUFFIX} beside it. That file is what decides "
                "the reading order.",
            )

        position = {slug: index for index, slug in enumerate(listed)}
        for member in members:
            if member.slug not in position:
                fail(
                    member.path,
                    f"is not listed in {series}{ORDER_SUFFIX}, so nothing knows "
                    "where it goes. Add its slug to that file.",
                )
        # A slug listed with no tutorial behind it is the more dangerous
        # direction: the order file looks complete and the series is short.
        missing = [slug for slug in listed if slug not in {m.slug for m in members}]
        if missing:
            fail(
                TUTORIALS / module / f"{series}{ORDER_SUFFIX}",
                f"lists {', '.join(missing)}, which no tutorial in this series "
                "has as its slug",
            )
        members.sort(key=lambda t: position[t.slug])
        for index, member in enumerate(members, start=1):
            member.order = index
    return groups


def link_between(here: Tutorial, there: Tutorial) -> str:
    return os.path.relpath(there.out_path, here.out_path.parent)


def nav_for(tutorial: Tutorial, members: list[Tutorial]) -> str:
    """Previous and next within the series, and the way back to the contents.

    A tutorial that is not among `members` — an archived one — gets the way back
    and nothing else, which is the honest shape: there is nowhere in the series
    it comes before or after.
    """
    index = members.index(tutorial) if tutorial in members else -1
    parts = []
    if index == -1:
        up = "../" * tutorial.depth
        return f'<a class="dl-nav-up" href="{up}index.html">All tutorials</a>' 
    if index > 0:
        previous = members[index - 1]
        parts.append(
            f'<a class="dl-nav-prev" href="{link_between(tutorial, previous)}">'
            f"{html.escape(previous.title)}</a>"
        )
    up = "../" * tutorial.depth
    parts.append(f'<a class="dl-nav-up" href="{up}index.html">All tutorials</a>')
    if index < len(members) - 1:
        following = members[index + 1]
        parts.append(
            f'<a class="dl-nav-next" href="{link_between(tutorial, following)}">'
            f"{html.escape(following.title)}</a>"
        )
    return "".join(parts)


def render_toc(tutorial: Tutorial) -> str:
    """A contents list for one page, nested one level.

    Closed by default: a reader arriving at a tutorial should meet the tutorial,
    not a list of its parts. Open, it is the fastest way back to a section they
    half-remember, which on a long page is the thing that is otherwise hard.

    Sub-headings nest under the section they belong to rather than sitting in
    one flat list, because the flat version of an eight-section tutorial with
    "Your turn" under half of them is unreadable.
    """
    def at_level(entries: list, level: int) -> list:
        """The headings at one level, wherever the tree happens to nest them.

        The `toc` extension hangs everything under the page's single `#`
        heading, so the sections are grandchildren rather than children.
        Searching by level rather than by depth means the shape of a tutorial's
        headings cannot break this.
        """
        found = []
        for entry in entries:
            if entry.get("level") == level:
                found.append(entry)
            else:
                found.extend(at_level(entry.get("children") or [], level))
        return found

    sections = at_level(tutorial.toc, 2)
    if len(sections) < 2:
        # One section, or none. A contents list for a single heading is furniture.
        return ""

    # Sub-headings that repeat cannot be told apart in a list, so they are worse
    # than useless there: "Your turn" appears five times in some tutorials, and
    # a contents entry a reader cannot choose between is noise. They keep their
    # anchors — only the listing drops them.
    names = [str(s.get("name", "")) for s in at_level(tutorial.toc, 3)]
    ambiguous = {name for name in names if names.count(name) > 1}

    def item(entry: dict, depth: int) -> list[str]:
        text = html.escape(str(entry.get("name", "")))
        out = [f'<li><a href="#{html.escape(str(entry["id"]), quote=True)}">{text}</a>']
        children = [
            child for child in entry.get("children") or []
            if child.get("level") == 3 and str(child.get("name", "")) not in ambiguous
        ]
        if children and depth == 0:
            out.append("<ul>")
            for child in children:
                out.extend(item(child, depth + 1))
            out.append("</ul>")
        out.append("</li>")
        return out

    parts = [
        '<details class="dl-toc">',
        f"<summary>Contents<span class=\"dl-toc-count\">"
        f"{len(sections)} sections</span></summary>",
        '<nav aria-label="Sections of this tutorial"><ul>',
    ]
    for section in sections:
        parts.extend(item(section, 0))
    parts += ["</ul></nav>", "</details>"]
    return "".join(parts)


def download_section(tutorial: Tutorial) -> str:
    """The settings panel's offer to take this tutorial away.

    Written here rather than in the shell because only build.py knows where a
    tutorial's downloadable copy ended up, and because the contents page — which
    shares the shell — has no single tutorial to offer.
    """
    up = "../" * tutorial.depth
    return (
        "<h3>This tutorial</h3>"
        f'<a class="dl-download" href="{up}download/{tutorial.module}/'
        f'{tutorial.slug}.html" download>Download to keep</a>'
        '<p class="dl-panel-note">One file with the reading and the cells inside '
        "it. It needs an internet connection the first time you open it, and "
        "then it is yours.</p>"
    )


# ------------------------------------------------------------ the topic tree

TOPIC_DATA = ROOT / "planning" / "curriculum" / "topics.yaml"
SCOPE_DATA = ROOT / "planning" / "curriculum" / "out-of-scope.yaml"

# One node is a comfortable tap target with room for a two-line name.
TOPIC_W, TOPIC_H = 178, 66
# How many topics a tier fits before it wraps onto another line. Five keeps the
# whole tree about a thousand pixels wide, which a phone can zoom to fit.
TREE_COLUMNS = 5
TIER_GAP, ROW_GAP = 56, 22
BAND_GAP = 34
TREE_PAD = 40


def load_topics() -> dict:
    """The glossary: what each topic is, where it is used, what it needs first.

    Optional, like the outcome data — the site has to build from the tutorials
    alone, and without this there is simply no topic tree.
    """
    if not TOPIC_DATA.is_file():
        return {}
    return (yaml.safe_load(TOPIC_DATA.read_text()) or {}).get("topics") or {}


def load_out_of_scope() -> set[str]:
    """Outcomes we have decided not to teach. Shown, and shown as decided."""
    if not SCOPE_DATA.is_file():
        return set()
    data = yaml.safe_load(SCOPE_DATA.read_text()) or {}
    return {entry["code"] for entry in data.get("outcomes") or []}


def taught_where(tutorials: list[Tutorial]) -> dict[str, dict]:
    """Outcome code to the tutorial section that teaches it.

    Read from each tutorial's own `covers:` frontmatter, so a topic's link
    cannot point somewhere the tutorial does not claim.
    """
    where: dict[str, dict] = {}
    for tutorial in tutorials:
        # An archived tutorial taught what it taught, but a student picking a
        # topic today cannot be sent there. Counting it would make the map say
        # an outcome is covered when nothing on the course covers it — which is
        # exactly the lie the map exists to prevent.
        # The current live version only. A superseded release claims the same
        # coverage as the one that replaced it, and counting both would make
        # one outcome look taught by four things.
        if tutorial.archived or tutorial.status != "live" or not tutorial.is_default:
            continue
        for anchor, claim in (tutorial.meta.get("covers") or {}).items():
            for code in claim.get("covers") or []:
                where.setdefault(code, {
                    "title": tutorial.title,
                    "href": f"tutorials/{tutorial.module}/{tutorial.slug}.html#{anchor}",
                })
    return where


def topic_tiers(topics: dict) -> dict[str, int]:
    """How much you need to know before a topic — its column in the tree.

    A topic with no prerequisites is tier 0; anything else is one past the
    deepest thing it needs. The glossary's tests guarantee no cycles, so this
    always terminates.
    """
    tier: dict[str, int] = {}

    def depth(code: str) -> int:
        if code in tier:
            return tier[code]
        needs = [n for n in (topics[code].get("needs") or []) if n in topics]
        tier[code] = 0 if not needs else 1 + max(depth(n) for n in needs)
        return tier[code]

    for code in topics:
        depth(code)
    return tier


def topic_layout(topics: dict, strands: dict[str, str]) -> tuple[dict, float, float]:
    """Where every topic sits: one row per tier, reading downwards.

    **Top to bottom is dependency.** Nothing in the top row needs anything, and
    nothing ever points upwards, so how far down a topic sits is how much has to
    come first. That is the one thing the layout has to make obvious.

    Vertical because that is how a page scrolls. The first attempt at this gave
    each subject its own column, which is the direct flip of the old horizontal
    tree — and measured 5854px wide against 756px tall, which is a horizontal
    tree wearing a hat. With twelve subjects there is no width to spare, so
    subject stops being an axis and becomes a sort: a tier wider than
    ``TREE_COLUMNS`` wraps onto more lines, and within a tier topics are grouped
    by subject so like still sits beside like.

    Lines are centred, which is what makes it read as a tree rather than a
    left-aligned list — a narrow tier looks like a narrow tier.
    """
    tier = topic_tiers(topics)
    rows: dict[int, list[str]] = {}
    for code in topics:
        rows.setdefault(tier[code], []).append(code)

    span = TOPIC_W + ROW_GAP
    width = TREE_PAD * 2 + TREE_COLUMNS * span - ROW_GAP

    place: dict[str, dict] = {}
    y = TREE_PAD
    for level in sorted(rows):
        members = sorted(
            rows[level], key=lambda c: (strands.get(c, "other"), topics[c]["name"])
        )
        lines = [members[i:i + TREE_COLUMNS] for i in range(0, len(members), TREE_COLUMNS)]
        top = y
        for line in lines:
            left = (width - (len(line) * span - ROW_GAP)) / 2
            for column, code in enumerate(line):
                place[code] = {
                    "x": left + column * span,
                    "y": y,
                    "tier": level,
                    "strand": strands.get(code, "other"),
                }
            y += TOPIC_H + ROW_GAP
        place[f"band:{level}"] = {"y": top, "height": y - top - ROW_GAP}
        y += TIER_GAP

    return place, width, y - TIER_GAP + TREE_PAD


def tier_label(level: int) -> str:
    """What a tier stripe says, in words a student can act on.

    "Tier 3" is a number about the data structure. "Three layers down" is a
    number about how much has to come first, which is the only reason anybody
    is reading the stripe.
    """
    if level == 0:
        return "start anywhere here"
    words = ["", "one", "two", "three", "four", "five", "six", "seven", "eight"]
    count = words[level] if level < len(words) else str(level)
    return f"{count} layer{'' if level == 1 else 's'} down"


def tree_data(tutorials: list[Tutorial]) -> dict:
    """Everything the topic tree page needs, as one blob of data.

    Assembled here rather than fetched by the page, because the page is static
    and a fetch would be one more thing to fail on a school network.
    """
    topics = load_topics()
    if not topics:
        return {}
    strands = load_strands()
    # A topic may name its own strand, which is the only way a topic that is not
    # an outcome can have one at all.
    for code, topic in topics.items():
        if topic.get("strand"):
            strands[code] = str(topic["strand"])
    excluded = load_out_of_scope()
    taught = taught_where(tutorials)
    place, width, height = topic_layout(topics, strands)

    nodes = []
    for code, topic in sorted(topics.items()):
        at = place[code]
        where = taught.get(code)
        # Groundwork is not an outcome, so no tutorial can claim it in `covers:`
        # and it would otherwise sit on the map forever marked "planned". It is
        # not planned; it is assumed, and picked up in passing wherever it is
        # first needed.
        if code.startswith("PRE-"):
            state = "groundwork"
        elif code in excluded:
            state = "excluded"
        else:
            state = "taught" if where else "planned"
        nodes.append({
            "code": code,
            "name": topic["name"],
            "plain": " ".join(topic["plain"].split()),
            "uses": [" ".join(u.split()) for u in topic.get("uses") or []],
            "needs": [n for n in (topic.get("needs") or []) if n in topics],
            "strand": at["strand"],
            "tier": at["tier"],
            "x": at["x"],
            "y": at["y"],
            "state": state,
            "where": where,
        })

    # One stripe per tier, labelled by what it means rather than by its number:
    # a student reading the map should not have to work out that "tier 0" is the
    # place to start.
    bands = [
        {
            "tier": int(key[5:]),
            "label": tier_label(int(key[5:])),
            "y": value["y"],
            "height": value["height"],
        }
        for key, value in place.items() if key.startswith("band:")
    ]
    return {
        "nodes": nodes,
        "bands": sorted(bands, key=lambda b: b["y"]),
        "width": width,
        "height": height,
        "node": {"w": TOPIC_W, "h": TOPIC_H},
    }


# ------------------------------------------------------- the knowledge map

OUTCOME_DATA = ROOT / "planning" / "curriculum" / "outcomes.yaml"

# Nodes wide enough for two short lines of title, spaced so an arrow between
# them is visibly an arrow rather than a join.
NODE_W, NODE_H = 132, 46
GAP_X, GAP_Y = 34, 30
LANE_LABEL_W = 96
MAP_PAD = 14


def strand_of(codes: list[str], outcomes: dict[str, str]) -> str:
    """The strand a tutorial mostly belongs to.

    Mostly, not only: a tutorial that teaches four algorithm outcomes and one
    programming one belongs on the algorithms row, and putting it in both would
    make a diagram nobody can follow. Ties break alphabetically, which is
    arbitrary but stable — and a genuine tie is worth noticing in itself, since
    it usually means the tutorial is about two things.
    """
    counts: dict[str, int] = {}
    for code in codes:
        strand = outcomes.get(code)
        if strand:
            counts[strand] = counts.get(strand, 0) + 1
    if not counts:
        return "other"
    best = max(counts.values())
    return sorted(s for s, n in counts.items() if n == best)[0]


def load_strands() -> dict[str, str]:
    """Outcome code to strand, from the curriculum data if it is there.

    Optional on purpose: the site has to build without the planning folder, so
    a missing file means a map without lanes rather than a failed build.
    """
    if not OUTCOME_DATA.is_file():
        return {}
    data = yaml.safe_load(OUTCOME_DATA.read_text()) or {}
    return {e["code"]: e["strand"] for e in data.get("outcomes") or []}


def map_rows(members: list[Tutorial], strands: dict[str, str]) -> list[tuple[str, list]]:
    """Tutorials grouped into strand bands, bands in teaching order.

    A band is broken and started again if the series leaves it and comes back —
    programming runs 1 to 4, goes away for algorithms and probability, and
    returns at 17. Drawing that as one row would put an arrow across the whole
    diagram and suggest a continuity that is not there.
    """
    rows: list[tuple[str, list]] = []
    for tutorial in members:
        declared = (tutorial.meta.get("covers") or {}).values()
        covered = [c for claim in declared for c in (claim.get("covers") or [])]
        touched = [c for claim in declared for c in (claim.get("touches") or [])]
        strand = strand_of(covered or touched, strands)
        if rows and rows[-1][0] == strand:
            rows[-1][1].append(tutorial)
        else:
            rows.append((strand, [tutorial]))
    return rows


def render_knowledge_map(members: list[Tutorial], strands: dict[str, str]) -> str:
    """The series as nodes and arrows: what follows what, and what leans on what.

    A contents list says what order to read in. It does not say that Tutorial 17
    leans on five earlier ones, or that the course spends four tutorials on
    programming before mathematics appears. The map is for the reader deciding
    where they are and what they need first.
    """
    if len(members) < 3:
        return ""

    rows = map_rows(members, strands)
    widest = max(len(row) for _, row in rows)
    width = LANE_LABEL_W + widest * NODE_W + (widest - 1) * GAP_X + MAP_PAD * 2
    height = len(rows) * NODE_H + (len(rows) - 1) * GAP_Y + MAP_PAD * 2

    place: dict[str, tuple[float, float]] = {}
    for index, (_, row) in enumerate(rows):
        y = MAP_PAD + index * (NODE_H + GAP_Y)
        for column, tutorial in enumerate(row):
            place[tutorial.slug] = (LANE_LABEL_W + column * (NODE_W + GAP_X), y)

    parts = [
        f'<svg class="dl-map" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Map of the tutorials, grouped by subject, '
        f'with arrows for what follows what">',
        '<defs><marker id="dl-arrow" viewBox="0 0 8 8" refX="7" refY="4" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L8 4 L0 8 z" fill="currentColor"/></marker>'
        '<marker id="dl-arrow-back" viewBox="0 0 8 8" refX="7" refY="4" '
        'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
        '<path d="M0 0 L8 4 L0 8 z" fill="currentColor"/></marker></defs>',
    ]

    # Edges first so the nodes sit on top of them. A long arrow crossing the
    # diagram passes behind the boxes it crosses, which is what stops it
    # reading as though it touched them.
    for tutorial in members:
        for fan, target in enumerate(back_links(tutorial, members)):
            parts.append(
                arrow_between(place, tutorial.slug, target, "dl-map-back", fan)
            )
    for before, after in zip(members, members[1:]):
        parts.append(arrow_between(place, before.slug, after.slug, "dl-map-next"))

    for index, (strand, row) in enumerate(rows):
        y = MAP_PAD + index * (NODE_H + GAP_Y)
        parts.append(
            f'<text class="dl-map-lane" x="{MAP_PAD}" y="{y + NODE_H / 2 + 4}">'
            f"{html.escape(strand)}</text>"
        )
        for tutorial in row:
            x, _ = place[tutorial.slug]
            href = tutorial.out_path.relative_to(OUT).as_posix()
            label = tutorial.title.split(":", 1)[-1].strip()
            parts.append(
                f'<a class="dl-map-node" href="{href}">'
                f'<title>{html.escape(tutorial.title)}</title>'
                f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="5"/>'
                f'<text x="{x + NODE_W / 2}" y="{y + NODE_H / 2 + 4}">'
                f"{html.escape(shorten(label))}</text></a>"
            )

    parts.append("</svg>")
    return "".join(p for p in parts if p)


def shorten(label: str, limit: int = 22) -> str:
    """Node labels are one line. A title that will not fit is cut at a word."""
    if len(label) <= limit:
        return label
    cut = label[:limit].rsplit(" ", 1)[0]
    return (cut or label[:limit]) + "…"


def back_links(tutorial: Tutorial, members: list[Tutorial]) -> list[str]:
    """Earlier tutorials this one names in its own text, skipping its neighbour.

    By title rather than by number, because the numbers are gone — and because
    a title is what a tutorial would say anyway. Evidence rather than intention:
    nobody maintains this list, it is found by reading. The tutorial immediately
    before is left out, since the reading-order arrow already says that one.
    """
    text = tutorial.body_html
    return [
        earlier.slug
        for earlier in members
        if 0 < earlier.order < tutorial.order - 1
        and len(earlier.title) > 6
        and earlier.title in text
    ]


def arrow_between(place: dict, a: str, b: str, css: str, fan: int = 0) -> str:
    """One arrow, routed so it can be told apart from the others.

    `fan` separates several arrows leaving the same node. Tutorial 17 names five
    earlier tutorials, and without this they would all leave the same point,
    travel the same column and arrive as one thick unreadable line. Each is bowed
    a little further out than the last.
    """
    if a not in place or b not in place:
        return ""
    (ax, ay), (bx, by) = place[a], place[b]

    if ay == by:
        # Same row: straight across, edge to edge.
        x1, x2 = (ax + NODE_W, bx) if ax < bx else (ax, bx + NODE_W)
        y = ay + NODE_H / 2
        return f'<path class="{css}" d="M{x1} {y} L{x2} {y}"/>'

    # Different rows: leave the side nearer the destination and arrive on the
    # matching side, bowed outwards so the path is a curve rather than a spine.
    going_up = by < ay
    y1 = ay if going_up else ay + NODE_H
    y2 = by + NODE_H if going_up else by
    x1, x2 = ax + NODE_W / 2, bx + NODE_W / 2
    reach = abs(y2 - y1) / 2 + fan * 22
    side = NODE_W * 0.7 + fan * 26 if going_up else 0
    return (
        f'<path class="{css}" d="M{x1} {y1} '
        f"C{x1 + side} {y1 - reach if going_up else y1 + reach}, "
        f"{x2 + side} {y2 + reach if going_up else y2 - reach}, "
        f'{x2} {y2}"/>'
    )


def render_index(
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path] | None = None,
    retired: dict[str, list[Tutorial]] | None = None,
    practice: dict[tuple[str, str], Tutorial] | None = None,
    mixed: dict[str, list[Tutorial]] | None = None,
) -> str:
    """The contents page: every module, every series, in order.

    `archives` maps a series to its zip of downloadable copies, when the build
    wrote them. Without it the page simply carries no whole-series link, which
    is what a quick local build wants.
    """
    archives = archives or {}
    retired = retired or {}
    practice = practice or {}
    mixed = mixed or {}
    if not groups:
        return "<p>No tutorials have been written yet.</p>"

    names = {}
    for members in list(groups.values()) + list(retired.values()):
        for member in members:
            if member.meta.get("module_title"):
                names.setdefault(member.module, member.module_title)

    # An introduction rather than a diagram. The map moved to its own page,
    # where it can have the whole window; this page's job is to say what dewlab
    # is to somebody who has just arrived, and then get out of the way of the
    # list they came for.
    out = [
        "<h1>Tutorials</h1>",
        '<div class="dl-intro">',
        "<p>Everything here runs in this browser. There is nothing to install, "
        "nothing to sign into, and no way to break anything — the Python you "
        "write runs on your own machine, inside this page, and never leaves "
        "it.</p>",
        "<p>The material covers two QQI Level 5 modules — <strong>Maths for "
        "Information Technology</strong> (5N18396) and <strong>Programming and Design "
        "Principles</strong> (5N2927) — taught together rather than side by "
        "side, because most of the maths is easier to see once you can make a "
        "computer do it. Everything on your course is in here somewhere.</p>",
        "<p>Every tutorial is a page of reading with code you can change and "
        "run as you go. Your work is saved automatically in this browser, so "
        "you can close the tab and come back. Each one can be downloaded as a "
        "single file to keep.</p>",
        '<p class="dl-intro-tree">New here, or not sure where a topic fits? '
        'The <a href="tree.html">topic tree</a> shows everything the course '
        "covers and what has to come first.</p>",
        "</div>",
    ]

    titles = series_titles()
    listed = module_order()
    everywhere = {module for module, _ in groups} | set(retired)
    # Listed modules in the order given, then anything else alphabetically, so
    # adding a module lands it at the end rather than breaking the page.
    ordered = [m for m in listed if m in everywhere] + sorted(everywhere - set(listed))
    for module in ordered:
        out.append(f"<h2>{html.escape(names.get(module, module))}</h2>")
        for (owner, series), members in sorted(groups.items()):
            if owner != module:
                continue
            if len({s for m, s in groups if m == module}) > 1:
                name = titles.get((owner, series), series)
                out.append(f'<h3>{html.escape(name)}</h3>')
            out.append('<ol class="dl-contents">')
            for member in members:
                href = member.out_path.relative_to(OUT).as_posix()
                # Beside the tutorial rather than under it as a second numbered
                # item: a practice page is not the next thing to read, it is the
                # other half of this one.
                also = practice.get((member.module, member.slug))
                extra = ""
                if also is not None:
                    where = also.out_path.relative_to(OUT).as_posix()
                    extra = (f' <a class="dl-contents-practice" href="{where}">'
                             "practice</a>")
                out.append(
                    f'<li><a href="{href}">{html.escape(member.title)}</a>{extra}</li>'
                )
            out.append("</ol>")
            archive = archives.get((owner, series))
            if archive is not None:
                count = len(members)
                # A series of one is a real case now that reflections live in
                # their own section, and "Download all 1 as single files" is
                # not a sentence anybody wrote on purpose.
                what = ("this one as a single file" if count == 1
                        else f"all {count} as single files")
                out.append(
                    '<p class="dl-series">'
                    f'<a class="dl-download" href="download/{archive.name}" download>'
                    f"Download {what}"
                    f" ({readable_size(archive)})</a></p>"
                )
        # After the series and before the archive. A mixed set is part of the
        # course and belongs to no series in it, so there is nowhere else it
        # could go — and it is the only kind of page nothing else links to.
        for member in mixed.get(module, []):
            if member is mixed[module][0]:
                out.append('<h3 class="dl-mixed-head">Mixed problems</h3>')
                out.append(
                    '<p class="dl-mixed-note">Problems drawing on several '
                    "tutorials at once. Worth doing once the tutorials they "
                    "name are behind you.</p>"
                )
                out.append('<ul class="dl-contents dl-mixed">')
            href = member.out_path.relative_to(OUT).as_posix()
            out.append(f'<li><a href="{href}">{html.escape(member.title)}</a></li>')
            if member is mixed[module][-1]:
                out.append("</ul>")

        # Last, and marked, because it is not part of the course any more — but
        # present, because a student who worked in one has to be able to find it.
        for member in retired.get(module, []):
            if member is retired[module][0]:
                out.append('<h3 class="dl-archive-head">Archive</h3>')
                out.append(
                    '<p class="dl-archive-note">No longer part of the course. '
                    "Kept so that saved work is still reachable and old links "
                    "still work.</p>"
                )
                out.append('<ul class="dl-contents dl-archive">')
            href = member.out_path.relative_to(OUT).as_posix()
            out.append(f'<li><a href="{href}">{html.escape(member.title)}</a></li>')
            if member is retired[module][-1]:
                out.append("</ul>")
    return "\n".join(out)


# ------------------------------------------------------------------- checks


def check_alt_text(tutorial: Tutorial) -> None:
    """Every image declares alt. An explicit alt="" marks a decorative one."""
    for tag in IMG_RE.findall(tutorial.body_html):
        if not ALT_RE.search(tag):
            fail(tutorial.path, f"image has no alt attribute: {tag}")


def check_folds(tutorial: Tutorial) -> None:
    """Every `<details>` names a fold this project styles.

    Cheap, and it catches the one mistake this markup invites: writing a bare
    `<details><summary>` because that is what HTML documents show. The class is
    where the styling and the marker come from, so a fold without one is
    invisible as a fold — it renders as a browser default triangle that does not
    look like part of the page.
    """
    for tag in DETAILS_RE.findall(tutorial.body_html):
        if not any(name in tag for name in FOLD_CLASSES):
            fail(tutorial.path,
                 f"a fold names no style: {tag} — use "
                 f'class="dl-hint" for steps or class="dl-answer" for an answer')


def resolve_links(tutorial: Tutorial, registry: dict[tuple[str, str], Tutorial]) -> str:
    """Rewrite tutorial:slug#anchor into a real relative href, or fail.

    A slug is looked for in this tutorial's own module first, which is what
    makes a cross-module name clash harmless: `tutorial:first-steps` in a
    maths tutorial means the maths one. Outside the module it still resolves,
    but only when exactly one other module has that slug — anything else is
    ambiguous and stops the build rather than guessing.
    """

    def one(match: re.Match) -> str:
        slug, anchor = match.group("slug"), match.group("anchor")
        target = registry.get((tutorial.module, slug))
        if target is None:
            elsewhere = [t for (module, s), t in registry.items() if s == slug]
            if len(elsewhere) == 1:
                target = elsewhere[0]
            elif len(elsewhere) > 1:
                modules = ", ".join(sorted(t.module for t in elsewhere))
                fail(
                    tutorial.path,
                    f"link to {slug!r} is ambiguous — it exists in {modules}, "
                    "and not in this module",
                )
        if target is None:
            known = ", ".join(sorted(s for _, s in registry)) or "none"
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
    converted, toc = to_html(stripped)
    body_html = place_blocks(converted, cells, blocks, maths)
    anchors = set(ID_RE.findall(body_html)) | {c.id for c in cells}
    return Tutorial(
        path=path,
        meta=meta,
        cells=cells,
        body_html=body_html,
        has_math=bool(maths),
        anchors=anchors,
        toc=toc,
    )


# ------------------------------------------------------------ asset versions

_ASSET_VERSIONS: dict[str, str] = {}


def asset_version(name: str) -> str:
    """A short hash of an asset's contents, for the end of its URL.

    Without one, a browser that has the site cached keeps serving the stylesheet
    and runtime it downloaded the first time, however many times we publish. The
    page is new and the CSS is old, which does not look like a caching problem —
    it looks like the page is broken, and only for the people who have been here
    before. A student on a school machine is exactly that person.

    Hashed per file rather than one version for everything, so editing the
    stylesheet does not also force a fresh download of the 266 KB maths bundle.
    """
    # Keyed by the full path, not the name: the tests build several repositories
    # in one process, and a cache keyed by "tutorial-style.css" alone would hand
    # the second one the first one's hash.
    path = ASSETS / name
    key = str(path)
    if key not in _ASSET_VERSIONS:
        _ASSET_VERSIONS[key] = (
            hashlib.sha256(path.read_bytes()).hexdigest()[:8] if path.is_file()
            else "missing"
        )
    return _ASSET_VERSIONS[key]


def versioned(base: str, name: str) -> str:
    return f"{base}{name}?v={asset_version(name)}"


def page_notice(tutorial: Tutorial, default: Tutorial | None = None) -> str:
    """What a page says about itself when it is not the ordinary case.

    Three of them, and each has to be impossible to read past, because all three
    describe a page that still works perfectly — it runs, it holds saved work,
    it looks like every other tutorial. Nothing about the page itself would tell
    a student they are in the wrong place.
    """
    up = "../" * tutorial.depth
    here = f'<a href="{up}index.html">all tutorials</a>'

    if tutorial.archived:
        return (
            '<div class="dl-archived" role="note">'
            "<strong>This tutorial is no longer part of the course.</strong> "
            "It is kept here so that anything you saved in it is still yours, and "
            "so nothing that linked to it is broken. It still runs. For what "
            f"replaced it, see {here}."
            "</div>"
        )

    if tutorial.status == "beta":
        return (
            '<div class="dl-archived" role="note">'
            "<strong>This is a draft, not the tutorial your course uses.</strong> "
            "It is here to be looked at and argued with. Anything you write in "
            "it is saved separately from the real one, and it may change or "
            f"disappear without warning. The one to work through is in {here}."
            "</div>"
        )

    if not tutorial.is_default and default is not None:
        current = os.path.relpath(default.out_path, tutorial.out_path.parent)
        return (
            '<div class="dl-archived" role="note">'
            f"<strong>This is the {tutorial.date} version of this tutorial.</strong> "
            f'There is a newer one — <a href="{current}">{html.escape(default.date)}</a>. '
            "This one is kept so that work saved against it still opens, and so "
            "a link to it still lands somewhere."
            "</div>"
        )
    return ""


def version_manifest(tutorial: Tutorial, family: list[Tutorial]) -> list[dict]:
    """Every release of this tutorial a reader could move to, newest first.

    Carries each one's cell ids, so the page can say *before* a student switches
    how much of their work will still be there — "six of your eight answers
    carry over" rather than "it should be fine, back up first". The whole list
    is a few hundred bytes beside a manifest that already holds every cell's
    code.

    Empty when there is only one release, which is most tutorials most of the
    time: a picker with one entry is furniture.
    """
    if len(family) < 2:
        return []
    # Two releases on one day read as the same option in the picker, because a
    # reader sees the date and not the sequence number. Found the first time a
    # tutorial was released twice in an afternoon. The number is added only
    # where it is needed, so the ordinary case stays a plain date.
    same_day = {
        version.date for version in family
        if sum(1 for other in family if other.date == version.date) > 1
    }
    return [
        {
            "version": other.version,
            "date": (f"{other.date} ({other.released[3]})"
                     if other.date in same_day else other.date),
            "status": other.status,
            "isDefault": other.is_default,
            "url": os.path.relpath(other.out_path, tutorial.out_path.parent),
            "cells": [cell.id for cell in other.cells],
        }
        for other in sorted(family, key=lambda t: t.released, reverse=True)
    ]


def canonical_link(tutorial: Tutorial, default: Tutorial | None) -> str:
    """Where search should send somebody who finds an older release.

    At the page the plain URL serves, which is the one a reader should land on
    unless they have a reason to be elsewhere. Nothing on the default itself:
    it is already the canonical page, and a link pointing at itself says
    nothing the URL does not.
    """
    if tutorial.is_default or default is None:
        return ""
    here = os.path.relpath(default.out_path, tutorial.out_path.parent)
    return f'<link rel="canonical" href="{html.escape(here, quote=True)}">'


def practice_link(tutorial: Tutorial, practice: Tutorial | None,
                  registry: dict[tuple[str, str], Tutorial] | None = None,
                  also: list[Tutorial] | None = None) -> str:
    """The link between a tutorial and its problems, in both directions.

    On the tutorial it sits at the end, because that is when a reader wants it.
    On the practice page it sits at the top, because somebody who has arrived
    there and cannot do the first question needs the way back before they need
    anything else.

    `also` is the mixed sets that name this tutorial. They are listed after its
    own page and described as needing more than this tutorial, so that a reader
    who has just finished it knows which of the two is for them now.
    """
    if tutorial.practice_across:
        links = []
        for slug in tutorial.practice_across:
            owner = (registry or {}).get((tutorial.module, slug))
            if owner is None:
                continue
            where = os.path.relpath(owner.out_path, tutorial.out_path.parent)
            links.append(f'<a href="{where}">{html.escape(owner.title)}</a>')
        if not links:
            return ""
        named = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " and " + links[-1]
        return (
            '<p class="dl-practice-back">Problems drawing on '
            f"{named}. Nothing here needs anything those tutorials did not "
            "cover, and every answer is on this page behind a fold.</p>"
        )
    if tutorial.practice_for:
        owner = (registry or {}).get((tutorial.module, tutorial.practice_for))
        if owner is None:
            return ""
        where = os.path.relpath(owner.out_path, tutorial.out_path.parent)
        return (
            '<p class="dl-practice-back">Problems on '
            f'<a href="{where}">{html.escape(owner.title)}</a>. '
            "Everything here is answerable from that tutorial, and every answer "
            "is on this page behind a fold.</p>"
        )
    also = also or []
    if practice is None and not also:
        return ""
    parts = ['<div class="dl-practice-link">']
    if practice is not None:
        where = os.path.relpath(practice.out_path, tutorial.out_path.parent)
        parts.append(
            f'<p><a href="{where}">Practice problems for this tutorial</a> — '
            "worth doing when you have finished reading, with the answers beside "
            "the questions, and steps to follow where a question is hard.</p>"
        )
    for page in also:
        where = os.path.relpath(page.out_path, tutorial.out_path.parent)
        others = [
            registry[(page.module, slug)].title
            for slug in page.practice_across
            if slug != tutorial.slug and (page.module, slug) in (registry or {})
        ]
        with_what = ""
        if others:
            named = (others[0] if len(others) == 1
                     else ", ".join(others[:-1]) + " and " + others[-1])
            with_what = f" It also draws on {html.escape(named)}."
        parts.append(
            f'<p class="dl-practice-mixed"><a href="{where}">'
            f"{html.escape(page.title)}</a> — for later, once more of the "
            f"course is behind you.{with_what}</p>"
        )
    parts.append("</div>")
    return "".join(parts)


def write(tutorial: Tutorial, shell: str, body_html: str, nav: str = "",
          default: Tutorial | None = None, family: list[Tutorial] | None = None,
          practice: Tutorial | None = None,
          registry: dict[tuple[str, str], Tutorial] | None = None,
          also: list[Tutorial] | None = None) -> Path:
    up = "../" * tutorial.depth
    manifest: dict[str, object] = {
        "slug": tutorial.slug,
        # The module, because a slug is only unique within one. Saved work is
        # keyed on this pair — without the module, both modules' `first-steps`
        # would share one key and a student's answers would appear in the wrong
        # tutorial.
        "module": tutorial.module,
        "version": tutorial.meta["version"],
        "assetBase": f"{up}assets/",
        # The runtime fetches these itself, so they need their own versions —
        # a page can only cache-bust what its own markup names.
        "assetVersions": {"tutorial_tools.py": asset_version("tutorial_tools.py")},
        "dataBase": f"{up}data/",
        "cells": [{"id": c.id, "hint": c.hint, "code": c.code} for c in tutorial.cells],
    }
    versions = version_manifest(tutorial, family or [tutorial])
    if versions:
        manifest["versions"] = versions
    if tutorial.has_math:
        # The runtime fetches the 266 KB KaTeX bundle only when this is set, so
        # a tutorial with no maths never pays for it.
        manifest["math"] = True
    packages = tutorial.meta.get("packages")
    if packages:
        manifest["packages"] = list(packages)

    tokens = {
        "{{TITLE}}": html.escape(str(tutorial.meta["title"])),
        "{{CANONICAL}}": canonical_link(tutorial, default),
        "{{VERSION}}": html.escape(str(tutorial.meta["version"]), quote=True),
        "{{SLUG}}": html.escape(tutorial.slug, quote=True),
        "{{MODULE}}": html.escape(tutorial.module, quote=True),
        "{{YEAR}}": html.escape(str(tutorial.meta["year"]), quote=True),
        "{{SERIES}}": html.escape(str(tutorial.meta["series"]), quote=True),
        "{{ASSET_BASE}}": f"{up}assets/",
        "{{STYLE_URL}}": versioned(f"{up}assets/", "tutorial-style.css"),
        "{{KATEX_CSS_URL}}": versioned(f"{up}assets/", "vendor/katex.min.css"),
        "{{RUNTIME_URL}}": versioned(f"{up}assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": up,
        "{{CRUMBS}}": html.escape(f"{tutorial.module_title} · {tutorial.meta['year']}"),
        "{{NAV_PREV_NEXT}}": nav,
        "{{PAGE_SCRIPT}}": "",
        "{{DOWNLOAD}}": download_section(tutorial),
        "{{TOC}}": render_toc(tutorial),
        "{{BODY}}": (
            page_notice(tutorial, default)
            + (practice_link(tutorial, practice, registry, also)
               if tutorial.is_practice else "")
            + body_html
            + (practice_link(tutorial, practice, registry, also)
               if not tutorial.is_practice else "")
        ),
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
    # The same prefix build.py wrote into the page's own asset references.
    up = "../" * tutorial.depth + "assets/"
    style = (ASSETS / "tutorial-style.css").read_text()
    bundle = (ASSETS / "vendor" / "standalone.bundle.js").read_text()
    tools = (ASSETS / "tutorial_tools.py").read_text()

    # The stylesheets, inlined. KaTeX's only travels with a page that has maths.
    # Matched on the versioned URLs the page actually carries: a file inlined
    # into the page has no URL to cache, so the version simply goes with it.
    page = replace_once(
        page,
        f'<link rel="stylesheet" href="{versioned(up, "vendor/katex.min.css")}">',
        f"<style>{inline_katex_css()}</style>" if tutorial.has_math else "",
        "the maths stylesheet",
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

    # The Python tools, which cannot be fetched from a file.
    marker = '<script type="application/json" id="dewlab-manifest">'
    start = page.index(marker) + len(marker)
    end = page.index("</script>", start)
    manifest = json.loads(page[start:end])
    manifest["toolsSource"] = tools
    manifest["standalone"] = True
    # Only the default version gets a downloadable copy, and the other releases
    # are not beside it on disk. A picker offering to move to files that are not
    # there is worse than no picker, so the whole list goes and the runtime
    # removes the section that would have shown it.
    manifest.pop("versions", None)
    page = page[:start] + json.dumps(manifest).replace("<", "\\u003c") + page[end:]

    # Navigation points at pages that are not beside this file, and the offer to
    # download it is already taken — this is the download. Both go rather than
    # break: the runtime hides the emptied section.
    page = re.sub(r"<nav class=\"dl-nav[^\"]*\">.*?</nav>", "", page, flags=re.DOTALL)
    page = re.sub(
        r'(<section class="dl-settings-section" id="dl-settings-download">).*?(</section>)',
        r"\1\2",
        page,
        flags=re.DOTALL,
    )
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

    # Under the module, like the page it came from. Slugs are unique within a
    # module and not across the site, so a flat download folder would let two
    # modules' "first-steps" overwrite each other — silently, since the loser
    # simply never appears.
    target = OUT / "download" / tutorial.module / f"{tutorial.slug}.html"
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
                OUT / "download" / member.module / f"{member.slug}.html",
                f"{folder}/{member.slug}.html",
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
    retired: dict[str, list[Tutorial]] | None = None,
    practice: dict[tuple[str, str], Tutorial] | None = None,
    mixed: dict[str, list[Tutorial]] | None = None,
) -> Path:
    """The contents page at the site root, which every page's masthead links to."""
    manifest = {"slug": "index", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "Tutorials",
        "{{VERSION}}": "1",
        "{{SLUG}}": "index",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": "contents",
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": "",
        "{{PAGE_SCRIPT}}": "",
        # The contents page is not a tutorial and has nothing to download; the
        # runtime hides the empty section rather than showing a bare heading.
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        # The contents page is a contents page. It does not need one of its own.
        "{{TOC}}": "",
        "{{BODY}}": render_index(groups, archives, retired, practice, mixed),
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


def strand_key(data: dict) -> str:
    """The colour on each node, said out loud.

    Every node carries its subject as a coloured edge and, until this, the only
    way to find out what a colour meant was to choose a topic and read the
    panel — which is the wrong way round for a key. Generated from the strands
    actually on the tree, so it cannot list a colour nothing uses or miss one
    that is there.
    """
    strands = sorted({node["strand"] for node in data.get("nodes") or []})
    if not strands:
        return ""
    items = "".join(
        f'<span class="dl-tree-key-strand">'
        f'<span class="dl-tree-hue" data-strand="{html.escape(strand)}"></span>'
        f"{html.escape(strand)}</span>"
        for strand in strands
    )
    return (
        '<details class="dl-tree-strands"><summary>What the colours mean</summary>'
        '<p class="dl-tree-strands-note">The stripe down the left of every topic '
        "is its subject. Subjects are not laid out in columns — depth is — so "
        "the colour is how you follow one thread down the tree.</p>"
        f'<p class="dl-tree-key-list">{items}</p></details>'
    )


def write_tree_page(shell: str, tutorials: list[Tutorial]) -> Path | None:
    """The topic tree: every topic in both descriptors, and what needs what.

    Its own page rather than part of the contents, because it wants the whole
    window and the contents page wants to be a list. It uses the same shell, so
    it gets the masthead, the settings panel and the reader's theme for free —
    which is most of what "light and dark" would otherwise cost.
    """
    data = tree_data(tutorials)
    if not data:
        return None

    body = (
        '<h1>The topic tree</h1>'
        '<p class="dl-tree-intro">Everything both modules cover, and what has to '
        "come before what. <strong>It reads downwards.</strong> Nothing in the top "
        "row needs anything, so any of it can be started today; the further down a "
        "topic sits, the more has to come first. Drag to move around it, scroll to "
        "zoom, and choose any topic to find out what it is, where it turns up in "
        "computing, and where it is taught.</p>"
        '<div class="dl-tree-layout">'
        '<div class="dl-tree-main">'
        # Above the frame rather than floating inside it. Floating, they sat on
        # top of whichever topics happened to land under them and swallowed the
        # clicks — the tree is taller now, so which topics those were changed
        # with the layout.
        '<div class="dl-tree-controls">'
        '<button type="button" id="dl-tree-out" aria-label="Zoom out">−</button>'
        '<button type="button" id="dl-tree-fit" aria-label="Fit the width and return to the top">fit</button>'
        '<button type="button" id="dl-tree-in" aria-label="Zoom in">+</button>'
        "</div>"
        '<div class="dl-tree-frame" id="dl-tree">'
        '<div class="dl-tree-canvas" id="dl-tree-canvas"></div>'
        "</div>"
        '<p class="dl-tree-key">'
        '<span class="dl-tree-swatch" data-state="taught"></span>taught here'
        '<span class="dl-tree-swatch" data-state="planned"></span>planned'
        '<span class="dl-tree-swatch" data-state="groundwork"></span>groundwork'
        '<span class="dl-tree-swatch" data-state="excluded"></span>not on this course'
        "</p>"
        + strand_key(data)
        + "</div>"
        '<aside class="dl-tree-detail" id="dl-tree-detail" aria-live="polite"></aside>'
        "</div>"
    )

    # The tutorial map underneath, because it answers a different question. The
    # tree says what a topic needs; this says what order the tutorials come in
    # and which ones lean on which — and that second part is found by reading
    # the tutorials, so it exists nowhere else.
    strands = load_strands()
    for (_, _), members in sorted(series_of(tutorials).items()):
        svg = render_knowledge_map(members, strands)
        if svg:
            body += (
                '<h2 class="dl-tree-second">How the tutorials relate</h2>'
                '<figure class="dl-map-figure">' + svg +
                "<figcaption>The reading order, in solid arrows. A dashed arrow "
                "means the later tutorial builds on the earlier one and says so "
                "in its own text. Any box takes you there.</figcaption></figure>"
            )
            break

    manifest = {"slug": "tree", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "The topic tree",
        "{{VERSION}}": "1",
        "{{SLUG}}": "tree",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": "topic tree",
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="index.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": (
            '<script type="application/json" id="dewlab-tree">'
            + json.dumps(data).replace("<", "\\u003c")
            + "</script>\n"
            + f'<script type="module" src="{versioned("assets/", "tree.js")}"></script>'
        ),
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{TOC}}": "",
        "{{BODY}}": body,
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(f"shell template has tokens the tree page does not fill: {leftover}")

    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "tree.html"
    target.write_text(page)
    return target


def write_editor_page(shell: str) -> Path:
    """The editor: reorder a series, insert a tutorial, and edit what is in one.

    It edits the repository through the GitHub API rather than anything this
    build produces, so it needs no data from here — only the shell, so that it
    looks like the rest of the site and inherits the reader's theme.

    Not linked from anywhere a student goes. It is a tool for the two people
    who write the tutorials, and it holds a token.
    """
    body = (
        "<h1>Editor</h1>"
        '<p class="dl-editor-intro">Reorder a series by dragging, insert a '
        "tutorial between two others, start a new one, or open any tutorial and "
        "edit its text and its runnable cells. Nothing here touches the live "
        "site: every change becomes one commit on a new branch and a draft pull "
        "request, which you then read before merging.</p>"
        '<div id="dl-editor"></div>'
    )
    manifest = {"slug": "editor", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "Editor",
        "{{VERSION}}": "1",
        "{{SLUG}}": "editor",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": "editor",
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="index.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": (
            f'<script type="module" src="{versioned("assets/", "editor.js")}"></script>'
        ),
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{TOC}}": "",
        "{{BODY}}": body,
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(f"shell template has tokens the editor does not fill: {leftover}")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "editor.html"
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
    # A draft is in the repository and not on the internet. The site is static
    # and public, so there is no other way to have one: anything built has a
    # URL, and a URL is public (planning/VERSIONS.md).
    everything = [load(p) for p in sources]
    tutorials = versions_of([t for t in everything if t.status != "draft"])

    # Unique within a module, not across the whole site. The built path already
    # carries the module, so two modules may each have a "first-steps" without
    # any ambiguity about which page is which — and forcing them apart would
    # mean naming tutorials around a constraint that does not exist.
    # One entry per tutorial, holding its default version: a `tutorial:` link
    # means "the current one", the same as the unversioned URL it resolves to.
    registry: dict[tuple[str, str], Tutorial] = {
        (t.module, t.slug): t for t in tutorials if t.is_default
    }

    families: dict[tuple[str, str], list[Tutorial]] = {}
    for tutorial in tutorials:
        families.setdefault((tutorial.module, tutorial.slug), []).append(tutorial)

    practice = practice_pairs(tutorials, registry)
    mixed = mixed_practice(tutorials, registry)

    shell = SHELL.read_text()
    groups = series_of(tutorials)
    retired = archived_of(tutorials)
    written: list[Path] = []
    for tutorial in tutorials:
        check_alt_text(tutorial)
        check_folds(tutorial)
        # An archived tutorial belongs to no reading order, so there is no
        # previous and no next — only the way back.
        members = groups.get((tutorial.module, tutorial.series), [])
        page_path = write(
            tutorial, shell, resolve_links(tutorial, registry), nav_for(tutorial, members),
            default=registry.get((tutorial.module, tutorial.slug)),
            family=families.get((tutorial.module, tutorial.slug)),
            practice=practice.get((tutorial.module, tutorial.slug)),
            also=[page for page in mixed.get(tutorial.module, [])
                  if tutorial.slug in page.practice_across],
            registry=registry,
        )
        written.append(page_path)
        # 0.7MB against 19KB for the hosted page, so only the version students
        # are actually being given is worth building forty times over.
        if standalone and tutorial.is_default:
            written.append(write_standalone(tutorial, page_path.read_text()))

    archives: dict[tuple[str, str], Path] = {}
    if standalone:
        for key, members in groups.items():
            archives[key] = write_series_zip(key[0], key[1], members)
        written.extend(archives.values())

    if tutorials:
        written.append(write_index(shell, groups, archives, retired, practice, mixed))
        tree = write_tree_page(shell, tutorials)
        if tree is not None:
            written.append(tree)
        written.append(write_editor_page(shell))

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
