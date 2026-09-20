#!/usr/bin/env python3
"""Turn the markdown in tutorials/ into the hosted HTML series in site/.

The shape of the job: read a tutorial's frontmatter and body, turn its
`exec`-tagged fences into cell objects, expand include directives into the
setup code they name, resolve cross-tutorial links to real relative hrefs and
fail on any that do not resolve, then render the result into assets/shell.html.

Maths and illustrative code are lifted out of the source before the markdown
converter ever sees them, for the same reason cells are: `$a_i$` would otherwise
come back with the subscript turned into emphasis. Both are marked for the
runtime to finish — KaTeX for the maths, a read-only CodeMirror for the code —
rather than rendered here.

The markup this emits for a cell, and the manifest it writes into the page, are
the contract the runtime reads, and what the browser tests in tests/e2e/
drive.

    python3 build.py            build into site/
    python3 build.py --clean    remove site/ first
"""

from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import html
import json
import os
import re
import shutil
import sys
import urllib.parse
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import markdown
import yaml


class _NoDuplicateKeysLoader(yaml.SafeLoader):
    """A YAML loader that refuses a mapping with the same key twice.

    Plain `yaml.safe_load` silently keeps the last value for a repeated key,
    which is how a botched merge once overwrote `topics.yaml`'s PDP-LO12
    entry and quietly dropped CMPS-LO13's real prerequisite — no error, no
    warning, just a fact that stopped being true. Curriculum data is hand
    and bundle-edited often enough that this is worth catching at load time
    rather than trusting the next reviewer to notice.
    """

    def construct_mapping(self, node, deep=False):
        """Overrides PyYAML's own mapping-building step to add one extra
        check before it does its normal work: walk the raw key/value pairs
        first, and raise if any key appears twice. `super().construct_mapping(...)`
        at the end is the actual, unmodified PyYAML behaviour — this method
        only adds a guard in front of it, rather than reimplementing YAML
        parsing itself.
        """
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=True)
            if key in seen:
                raise yaml.YAMLError(f"duplicate key {key!r} at {node.start_mark}")
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


def load_yaml_no_duplicate_keys(text: str):
    """Parses YAML text using the stricter loader above, in place of a
    plain `yaml.safe_load(text)` call — every place in this file that
    reads a `.yaml` file (topics, curriculum data, series ordering) goes
    through this function rather than PyYAML directly, so the whole
    codebase gets the duplicate-key protection consistently.
    """
    return yaml.load(text, Loader=_NoDuplicateKeysLoader)


# One parse per YAML file per build, for the files read over and over.
# A tutorial's reference accumulates its whole series chain, so a glossary
# early in a course is read again for every tutorial after it; the
# redirects file, the two Basics files and the feedback switch are each
# read fresh on every call, by design, so that a test's temporary ROOT is
# seen. Three quarters of a build was going into re-parsing the same
# bytes.
#
# The key carries the file's modification time and size as well as its
# path, so reading fresh still happens whenever the file has changed, and
# a temporary ROOT is a different path anyway. Nothing here is mutated by
# its callers: each one reads the parsed data and builds its own result.
_YAML_CACHE: dict[tuple[str, int, int, bool], object] = {}


def read_yaml(path: Path, *, strict: bool = True):
    """The contents of a `.yaml` file, parsed once per build.

    `strict` chooses the loader: `load_yaml_no_duplicate_keys()`, which is
    what most of this file wants, or PyYAML's own `safe_load()` for the
    couple of places that read a plain mapping and have never asked for
    the duplicate-key check.
    """
    stat = path.stat()
    key = (str(path), stat.st_mtime_ns, stat.st_size, strict)
    if key not in _YAML_CACHE:
        text = path.read_text()
        _YAML_CACHE[key] = (
            load_yaml_no_duplicate_keys(text) if strict else yaml.safe_load(text)
        )
    return _YAML_CACHE[key]

ROOT = Path(__file__).resolve().parent
TUTORIALS = ROOT / "tutorials"
COURSES = ROOT / "courses"
SETUP = ROOT / "setup"
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
COMPOSE = ROOT / "compose"
DEWMARK_WORKBENCH = ROOT / "dewmark" / "workbench"
TOPIC_GAME = ROOT / "topic_tree_game"
TOPIC_EDITOR = ROOT / "topic_editor"
SHELL = ASSETS / "shell.html"
OUT = ROOT / "site"
PAGES = ROOT / "pages"

REQUIRED_FRONTMATTER = ("title", "year", "version")

STATUSES = ("draft", "beta", "live", "archived")

VERSION_RE = re.compile(r"^(?P<y>\d{4})\.(?P<m>\d{2})\.(?P<d>\d{2})\.(?P<n>\d+)$")

# Fields a tutorial used to carry and no longer may. Where a tutorial sits is
# not the tutorial's own business any more: a course file under courses/
# lists it, and the folder name is its id (DECISIONS_LOG 7.172).
MOVED_FRONTMATTER = {
    "order": "the course file under courses/ lists ids in reading order",
    "slug": "the folder name is the tutorial's id",
    "module": "the course file under courses/ that lists this tutorial says which course it is on",
    "module_title": "the course file's own title: line names the course",
    "series": "a series is a heading in the course file under courses/",
}

# A frozen release, `v2026.09.15.1.md`, beside the tutorial's own file.
VERSION_FILE_RE = re.compile(r"^v\d{4}\.\d{2}\.\d{2}\.\d+$")

FENCE_RE = re.compile(r"^(?P<indent> *)```(?P<info>[^\n]*)\n(?P<body>.*?)^ *```[ \t]*$",
                      re.MULTILINE | re.DOTALL)
HEADER_RE = re.compile(r"^\s*(id|hint|expect|name)\s*:\s*(.*)$")
# The only two words that can open an exec fence today. Anything else fails
# the build with a clear message rather than silently becoming a Python cell.
CELL_TYPES = {"python", "sql"}

SITE_LANGS = {"html", "css", "js"}
SITE_HEADER_RE = re.compile(r"^\s*(id|site)\s*:\s*(.*)$")
HINT_HEADER_RE = re.compile(r"^\s*(for|after|title)\s*:\s*(.*)$")
CARD_HEADER_RE = re.compile(r"^\s*(url|status|meta|wide)\s*:\s*(.*)$")
# A ```question fence's own header: flat headers, the same loop
# CARD_HEADER_RE's own caller (parse_card) already uses, then ordinary
# markdown.
QUESTION_HEADER_RE = re.compile(r"^\s*(id|type|correct)\s*:\s*(.*)$")
QUESTION_TYPES = {"multiple-choice", "fill-in-the-blank"}
# One flat level of {...} — a gap with no "|" is a typing box, one with
# "|" a dropdown, the first item either way the expected answer.
GAP_RE = re.compile(r"\{([^{}]*)\}")
# "- an option" / "* an option" / "+ an option" — the same three markers
# Python-Markdown's own sane_lists extension accepts.
OPTION_LINE_RE = re.compile(r"^[ \t]*[-*+]\s+(.*\S)\s*$")
# `html app`/`css app`/`js app` — a full-stack module's own fence kind
# (DECISIONS_LOG.md 7.180). Same three languages as a site pane, on
# purpose, but a separate pair of constants: site fences and app fences
# are read by two different branches in extract_blocks(), and nothing
# here should make changing one silently change the other.
APP_LANGS = {"html", "css", "js"}
APP_HEADER_RE = re.compile(r"^\s*(id|app)\s*:\s*(.*)$")
# A page's own way to point at infrastructure it can never author directly —
# the site-wide search box, say. A bracketed marker rather than an HTML
# comment, so a future markdown editor renders it as a real, visible line
# rather than an invisible comment node.
GENERATED_BLOCK_RE = re.compile(r"^\[\[(?P<name>[a-z-]+)\]\]\s*$", re.MULTILINE)
TRIGGER_KEYS = {
    "errors": "errors", "error": "errors",
    "identical errors": "same-errors", "identical error": "same-errors",
    "same errors": "same-errors", "same error": "same-errors",
    "same-error": "same-errors", "same-errors": "same-errors",
    "identical-errors": "same-errors",
    "unchanged runs": "unchanged", "unchanged run": "unchanged", "unchanged": "unchanged",
    "runs": "runs", "run": "runs",
    "failed checks": "check-fails", "failed check": "check-fails",
    "check-fails": "check-fails", "failed-checks": "check-fails",
    "empty results": "empty-results", "empty result": "empty-results",
    "empty-results": "empty-results", "empty-result": "empty-results",
    "minutes": "minutes", "minute": "minutes",
}
TRIGGER_TERM_RE = re.compile(
    r"^(?:(?P<n1>\d+)\s+(?P<k1>[a-z][a-z -]*[a-z])|(?P<k2>[a-z][a-z-]*)\s*:\s*(?P<n2>\d+))$"
)
DEFAULT_HINT_AFTER = "errors:5"
DEFAULT_HINT_TITLE = "Let\u2019s slow down a moment\u2026"
INCLUDE_RE = re.compile(r"\{\{\s*include\s*:\s*(?P<path>[^}]+?)\s*\}\}")
TIGHT_LIST_RE = re.compile(
    r"(?m)^(?P<prose>(?![ \t]*(?:[-*+]|\d+[.)])\s)(?![ \t]*#)(?![ \t]*>)[^\n]*\S[^\n]*)\n"
    r"(?P<item>[ \t]*(?:[-*+]|\d+[.)])\s+\S)"
)
TUTORIAL_HREF_RE = re.compile(r'href="tutorial:(?P<slug>[^"#]+)(?:#(?P<anchor>[^"]*))?"')
ID_RE = re.compile(r'\bid="([^"]+)"')
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ALT_RE = re.compile(r"\balt\s*=", re.IGNORECASE)
DETAILS_RE = re.compile(r"<details\b[^>]*>", re.IGNORECASE)
FOLD_CLASSES = ("dl-hint", "dl-answer")
NOTE_RE = re.compile(
    r'<aside class="dl-note" id="(?P<id>[^"]+)">\s*(?P<html>.*?)\s*</aside>\n?',
    re.DOTALL,
)

DISPLAY_MATH_RE = re.compile(r"\$\$(?P<tex>.+?)\$\$", re.DOTALL)
INLINE_MATH_RE = re.compile(r"\$(?!\s)(?P<tex>[^$\n]+?)(?<!\s)\$")
ESCAPED_DOLLAR = "\x00dldollar\x00"

# The wrappers an author writes by hand and then writes markdown inside:
# a practice page's hint or answer fold, and a page's own section or list
# wrapper. Python-Markdown treats a raw HTML block as opaque through to its
# closing tag, so the `md_in_html` extension (part of `extra`) needs telling
# which ones to look inside — see mark_markdown_wrappers(). Scoped to these
# known tag/class pairs rather than to any element a page happens to write.
MARKDOWN_WRAPPER_RE = re.compile(
    r'<details class="(?:dl-hint|dl-answer)">'
    r'|<(?:div|ul) class="(?:dl-hero|dl-audience|dl-attribution|dl-feature-list)">'
    r'|<aside class="dl-note" id="[^"]+">'
)
# A run of one or more adjacent card placeholders — see place_page_cards().
CARD_RUN_RE = re.compile(r"<!--dewlab-page-card-\d+-->(?:\n\n<!--dewlab-page-card-\d+-->)*")


class BuildError(Exception):
    """Something in the source is wrong. The build stops and says where."""


@dataclass
class Cell:
    id: str
    hint: str | None
    code: str
    expect: str | None = None
    name: str | None = None
    type: str = "python"


@dataclass
class StagedHint:
    """A ```hint fence, before it becomes a fold — see extract_blocks()."""

    cell: str
    after: str
    title: str
    body: str
    # Which of its cell's hints this is, in source order — the fold's id.
    index: int = 0


@dataclass
class CodeBlock:
    """An untagged fence: read-only, illustrative, no Run button."""

    language: str
    code: str


@dataclass
class PageCard:
    """A ```card fence — see extract_page_cards(). Not a tutorial cell: a
    hand-written page's own way to write a clickable tile, the markup
    render_index() used to hardcode six times over for the home page."""

    url: str
    heading: str
    body_html: str
    status: str | None = None
    meta: str | None = None
    wide: bool = False


@dataclass
class Question:
    """A ```question fence — see extract_blocks(). `prompt` and, for
    multiple-choice, each entry in `options` are raw markdown, converted at render time
    (render_question()) rather than here — the same split parse_hint()/
    render_staged_hint() already make, so the checks below read source
    text, not converted HTML. `correct` is a multiple-choice option's
    1-based position in `options`; unused (0) for fill-in-the-blank,
    where the expected answer for each {...} gap is read straight out
    of `prompt` at render time instead."""

    id: str
    type: str
    prompt: str
    options: list[str] = field(default_factory=list)
    correct: int = 0


@dataclass
class SitePane:
    """One `html site`/`css site`/`js site` fence — see extract_blocks()."""

    id: str
    site: str
    language: str
    code: str


@dataclass
class SiteEditor:
    """The live HTML/CSS/JS editor one or more consecutive `SitePane`s with
    the same `site:` name become. `panes` is keyed by language rather than
    a plain list because a page never has two panes of the same language
    in one editor (extract_blocks() fails the build if it finds one), and
    a dict makes "does this editor have a JS pane" a lookup rather than a
    search — render_site_editor() and the manifest both ask that question."""

    name: str
    panes: dict[str, SitePane]


@dataclass
class AppPane:
    """One `html app`/`css app`/`js app` fence — see extract_blocks()."""

    id: str
    app: str
    language: str
    code: str


@dataclass
class AppCell:
    """A full-stack module's own cell kind: one or more consecutive
    `AppPane`s with the same `app:` name. Shares `SitePane`/`SiteEditor`'s shape — `panes` is keyed by
    language for the same reason — but is a separate cell kind rather
    than a third site-pane language, because its JavaScript is meant to
    reach the page's own shared `db`, which a site editor's sandboxed
    iframe exists specifically to stop a reader's script from doing. See
    `render_app_cell()`'s own docstring for the rendering side of that
    difference."""

    name: str
    panes: dict[str, AppPane]


@dataclass
class Math:
    tex: str
    display: bool


@dataclass
class Note:
    """A pedagogical note. Authored inline as an HTML aside, the same
    trick the hint/answer fold already uses, but surfaced in the
    reference panel rather than staying inline — see extract_notes()."""

    id: str
    html: str


@dataclass(frozen=True)
class Placement:
    """One place a page is listed: a course, a series in it (by key — see
    series_key()), and a 1-based position in that series. A mixed problem
    set listed under a course's `mixed:` has series "" and position 0."""

    course: str
    series: str
    position: int


def id_of(path: Path) -> str:
    """A page's id, from where its file is and nothing else.

    A tutorial is `tutorials/<id>/<id>.md`, so the id is the file's stem —
    which is also the folder name. A practice page is `<id>-practice.md` in
    the same folder, and its id is `<id>-practice`. A frozen release,
    `v<version>.md`, is a version of the folder's tutorial, so it takes the
    folder's name. Nothing is read from the frontmatter: the id is the
    address of the page and the key every reader's saved work lives under,
    and a field that could disagree with the folder would be a way to
    break both.
    """
    if VERSION_FILE_RE.match(path.stem):
        return path.parent.name
    return path.stem


@dataclass
class Tutorial:
    """One tutorial page, fully parsed and ready to render — everything
    `load()` further down builds and everything the rest of this file
    reads to write out the finished HTML.

    Most of what's declared below the raw fields is a `@property` —
    Python's way of writing a method (`def slug(self): ...`) that gets
    *read* like a plain attribute (`tutorial.slug`, no parentheses)
    rather than called like a function. A lot of these properties are one
    line pulling a value out of `self.meta` (the tutorial's own
    frontmatter dictionary) and converting it to the right type — those
    stay uncommented individually where the name already says everything
    (`slug` returns the slug); a property gets its own docstring here
    only where there's a real "why" behind what it does, not just "what."
    """

    path: Path
    meta: dict
    cells: list[Cell]
    body_html: str
    has_math: bool = False
    has_sql: bool = False
    # A page's live HTML/CSS/JS editors, in source order — usually empty;
    # only the web-authoring module has any yet.
    site_editors: list[SiteEditor] = field(default_factory=list)
    # A page's full-stack cells, in source order — usually empty; only the
    # full-stack module has any yet.
    app_cells: list[AppCell] = field(default_factory=list)
    anchors: set[str] = field(default_factory=set)
    toc: list = field(default_factory=list)
    notes: list[Note] = field(default_factory=list)
    # Where this page sits: every course that lists it, in courses/index.yaml
    # order, each with the series and the position. Not from the frontmatter —
    # the course files decide it, and place_tutorials() fills it in once
    # every tutorial is loaded. Empty for a page no course lists.
    placements: list[Placement] = field(default_factory=list)
    # Its position in the series of its default course — the first placement
    # — or 0 off the reading order (archived, practice, unplaced).
    order: int = 0
    is_default: bool = True

    @property
    def slug(self) -> str:
        """The tutorial's id, which is its folder name — see id_of()."""
        return id_of(self.path)

    @property
    def folder(self) -> str:
        """The folder this page's file sits in, which is where its assets
        are: the tutorial's id, for a practice page too."""
        return self.path.parent.name

    @property
    def course(self) -> str:
        """The course this page is drawn in by default: the first course in
        courses/index.yaml order that lists it, or "" when none does. The
        page carries this course's tree and previous/next; a reader on
        another course that lists it gets that course's from the runtime."""
        return self.placements[0].course if self.placements else ""

    @property
    def series(self) -> str:
        """The series key of the default placement, or ""."""
        return self.placements[0].series if self.placements else ""

    @property
    def courses(self) -> list[str]:
        """Every course that lists this page, default first, each once."""
        seen: list[str] = []
        for placement in self.placements:
            if placement.course not in seen:
                seen.append(placement.course)
        return seen

    @property
    def out_path(self) -> Path:
        """The default sits at the tutorial's own URL; other versions sit under
        it. So every link written before versions existed — in a tutorial, on
        the topic tree, in a student's bookmarks — keeps working and keeps
        meaning "the current one"."""
        here = OUT / "tutorials"
        if self.is_default:
            return here / f"{self.slug}.html"
        return here / self.slug / f"v{self.version}.html"

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
    def datasets(self) -> tuple[str, ...]:
        """The names this tutorial's cells load via `load_csv()` or
        `load_text()` — declared, not scraped, the same reasoning
        `covers:`/`practice_for` already use."""
        value = self.meta.get("datasets") or []
        if isinstance(value, str):
            value = [value]
        return tuple(str(s) for s in value)

    @property
    def version(self) -> str:
        return str(self.meta["version"])

    @property
    def released(self) -> tuple[int, int, int, int]:
        """The version as something sortable. Numbers, not the string: the
        date parts are zero-padded, so text order agrees with them, but the
        release number is not, and as text 2026.09.15.10 would sort before
        2026.09.15.9."""
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
    """Raises a `BuildError` naming which file the problem is in, using a
    path relative to the repository root rather than a full absolute path
    — shorter, and the same no matter whose computer the build runs on.
    Every validation check throughout this file calls this instead of
    raising directly, so every build failure reads in the same
    "file: what's wrong" shape.
    """
    raise BuildError(f"{path.relative_to(ROOT)}: {message}")


def split_frontmatter(text: str, path: Path) -> tuple[dict, str]:
    """Splits one tutorial's raw file into its frontmatter (the YAML
    block between the two `---` lines, holding title/slug/module/version
    and so on) and its body (everything after). Also does the up-front
    validation for that frontmatter — every required field is present,
    nothing that moved elsewhere still lingers, the status and version
    are both recognizable — so a broken tutorial file fails loudly right
    here, with a specific reason, rather than causing a stranger error
    somewhere deep in rendering.
    """
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
    for field_name, where_now in MOVED_FRONTMATTER.items():
        if field_name in meta:
            fail(path, f"{field_name} no longer belongs in frontmatter — "
                       f"{where_now}. Delete the line.")
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

    De-duplicates the source, not the runtime: the expanded cell still
    executes on every page load.
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


def parse_cell(body: str, path: Path, cell_type: str = "python") -> Cell:
    """Read `id:` and optional `hint:`/`expect:`/`name:` off the top of an
    exec fence. `cell_type` is the fence's own language word ("python" or
    "sql") — the header grammar underneath it is identical either way."""
    lines = body.split("\n")
    header: dict[str, str] = {}
    while lines:
        match = HEADER_RE.match(lines[0])
        if not match or match.group(1) in header:
            break
        if match.group(1) == "name" and "=" in match.group(2):
            break
        header[match.group(1)] = match.group(2).strip()
        lines.pop(0)
    if "id" not in header:
        fail(path, "an exec cell has no `id:` line — ids are what saved progress matches on")
    code = expand_includes("\n".join(lines).strip("\n"), path)
    return Cell(
        id=header["id"],
        hint=header.get("hint") or None,
        code=code,
        expect=header.get("expect") or None,
        name=header.get("name") or None,
        type=cell_type,
    )


def parse_site_pane(body: str, path: Path, language: str) -> SitePane:
    """Read `id:`/`site:` off the top of an `html site`/`css site`/`js
    site` fence. `language` is the fence's own first word; the rest of the
    fence is the pane's own HTML, CSS or JavaScript, unwrapped — a site
    pane's code is never Python and never runs through expand_includes(),
    since {{include: ...}} is a Python-cell convenience with nothing to
    say about a stylesheet."""
    lines = body.split("\n")
    header: dict[str, str] = {}
    while lines:
        match = SITE_HEADER_RE.match(lines[0])
        if not match or match.group(1) in header:
            break
        header[match.group(1)] = match.group(2).strip()
        lines.pop(0)
    if "id" not in header:
        fail(path, "a site pane has no `id:` line — ids are what saved progress matches on")
    if "site" not in header:
        fail(path, "a site pane has no `site:` line naming which editor it belongs to")
    return SitePane(
        id=header["id"], site=header["site"], language=language,
        code="\n".join(lines).strip("\n"),
    )


def parse_app_pane(body: str, path: Path, language: str) -> AppPane:
    """Read `id:`/`app:` off the top of an `html app`/`css app`/`js app`
    fence — the same header loop `parse_site_pane()` uses, on its own
    pair of header words. A full-stack cell's code is never Python and
    never runs through `expand_includes()`, the same reasoning
    `parse_site_pane()` gives."""
    lines = body.split("\n")
    header: dict[str, str] = {}
    while lines:
        match = APP_HEADER_RE.match(lines[0])
        if not match or match.group(1) in header:
            break
        header[match.group(1)] = match.group(2).strip()
        lines.pop(0)
    if "id" not in header:
        fail(path, "an app pane has no `id:` line — ids are what saved progress matches on")
    if "app" not in header:
        fail(path, "an app pane has no `app:` line naming which cell it belongs to")
    return AppPane(
        id=header["id"], app=header["app"], language=language,
        code="\n".join(lines).strip("\n"),
    )


def parse_trigger(text: str, path: Path) -> str:
    """Turn an `after:` line into the runtime's `key:number` form.

    `5 errors`, `3 identical errors and 2 minutes`, `errors:5, minutes:2` all
    parse; the first two become the third. Every term must be one the
    runtime knows (`TRIGGER_KEYS`), so a typo fails the build here rather
    than producing a hint that never appears.
    """
    terms = []
    for raw in re.split(r"\s*(?:,|\band\b|&)\s*", text.strip().lower()):
        if not raw:
            continue
        match = TRIGGER_TERM_RE.match(raw)
        if not match:
            fail(path, f"a hint's after: line has a term I cannot read: {raw!r} "
                       f"— write it like `5 errors` or `errors:5`")
        key = match.group("k1") or match.group("k2")
        count = int(match.group("n1") or match.group("n2"))
        canonical = TRIGGER_KEYS.get(key.strip())
        if canonical is None:
            fail(path, f"a hint's after: line names a signal the runtime does not "
                       f"track: {key!r} — one of errors, identical errors, "
                       f"unchanged runs, runs, failed checks, empty results, minutes")
        if count < 1:
            fail(path, f"a hint's after: count must be at least 1, not {count}")
        terms.append(f"{canonical}:{count}")
    if not terms:
        fail(path, "a hint's after: line is empty")
    return " ".join(terms)


# A footnote reference or definition: `[^label]`, optionally followed by a
# colon. Used to keep one out of a fence body — see no_footnotes_in().
FOOTNOTE_TOKEN_RE = re.compile(r"\[\^[^\]\s]+\]")
# Inline code, blanked before that check, so a regex character class in a
# hint's `[^aeiou]` example is not mistaken for a footnote. A fence body
# cannot hold a nested ``` block (FENCE_RE stops at the first closing
# line), so inline spans are the only code a fence body can carry — bar a
# four-space indented block, where the check would refuse a character
# class and the message says how to escape it.
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def no_footnotes_in(text: str, path: Path, what: str) -> None:
    """Fail the build on a footnote written inside a fence body.

    A ```hint, ```question or ```card fence is converted on its own, by
    its own `markdown.Markdown` instance — see convert_prose_with_math().
    The `footnotes` extension collects a document's definitions at the end
    of the document it is converting, so a fence body is its own document
    for that purpose, and neither half of a footnote can cross the edge of
    one:

    - a reference here, with its definition in the page's prose, reaches
      the page as the literal text `[^label]`, because this converter
      never saw the definition;
    - a reference and its definition both here render, but as their own
      rule and numbered list, inside the hint box or the question rather
      than at the foot of the page, numbered from one again.

    Both are silent: the build succeeds and the page looks wrong. So the
    fence bodies are the one place a footnote is refused outright. Prose,
    a `dl-hint`/`dl-answer` fold and a `dl-note` aside are all part of the
    page's own single conversion pass (mark_markdown_wrappers()), so a
    footnote works in any of those.
    """
    if FOOTNOTE_TOKEN_RE.search(INLINE_CODE_RE.sub("``", text)):
        fail(path, f"{what} has a footnote in it. A fence is converted on its own, "
                   "so a footnote written here cannot reach the foot of the page — "
                   "put it in the page's own prose instead, or write `\\[^` to mean "
                   "a literal bracket")


def parse_hint(body: str, path: Path, previous_cell: str | None) -> StagedHint:
    """Read `for:`, `after:` and `title:` off the top of a ```hint fence.

    Everything after the header lines is the hint's own markdown. With no
    `for:` the hint belongs to the exec cell just above it in the source,
    which is where nearly every hint will sit.
    """
    lines = body.split("\n")
    header: dict[str, str] = {}
    while lines:
        match = HINT_HEADER_RE.match(lines[0])
        if not match or match.group(1) in header:
            break
        header[match.group(1)] = match.group(2).strip()
        lines.pop(0)
    cell = header.get("for") or previous_cell
    if not cell:
        fail(path, "a hint fence has no exec cell above it and no `for:` line "
                   "naming one")
    text = "\n".join(lines).strip("\n")
    if not text.strip():
        fail(path, f"the hint for cell {cell!r} has no text in it")
    no_footnotes_in(text, path, f"the hint for cell {cell!r}")
    return StagedHint(
        cell=cell,
        after=parse_trigger(header.get("after") or DEFAULT_HINT_AFTER, path),
        title=header.get("title") or DEFAULT_HINT_TITLE,
        body=text,
    )


def render_staged_hint(hint: StagedHint, maths: list[Math]) -> str:
    """The fold a ```hint fence becomes.

    Its body is converted on its own, the same way extract_notes() converts a
    pedagogical note: Python-Markdown treats a `<details>` block and
    everything up to its closing tag as raw HTML, so a body left inside the
    tags in the source would come out as literal text — which is also why the
    hand-written folds on the practice pages keep to plain sentences. Maths
    goes through extract_math() first, appending to the *page's* list so its
    tokens are numbered after the prose's and place_blocks() renders them in
    the same pass. `hidden` is what the runtime removes when the trigger
    fires; with JavaScript off the fold stays hidden, as a cell stays
    unrunnable.
    """
    stripped, _ = extract_math(hint.body, maths)
    body_html, _ = to_html(loosen_tight_lists(stripped))
    safe_cell = html.escape(hint.cell, quote=True)
    return (
        f'<details class="dl-hint dl-hint-staged" '
        f'id="dl-staged-{safe_cell}-{hint.index}" '
        f'data-cell="{safe_cell}" data-after="{html.escape(hint.after, quote=True)}" hidden>'
        f"<summary>{html.escape(hint.title)}</summary>\n"
        f"{body_html}\n"
        f"</details>"
    )


def place_hints(page_html: str, hints: list[StagedHint], maths: list[Math]) -> str:
    """Swap each hint's placeholder comment for its rendered fold — the
    hint half of place_blocks(), run before it so the maths tokens a hint's
    body adds to `maths` are still there to be rendered."""
    for index, hint in enumerate(hints):
        placeholder = f"<!--dewlab-hint-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"the hint for cell {hint.cell!r} was lost during markdown conversion")
        page_html = page_html.replace(placeholder, render_staged_hint(hint, maths))
    return page_html


def _split_multiple_choice(text: str) -> tuple[str, list[str]]:
    """The prompt, and the options under it: the prose before the first
    list is the question, the list is the options. The first line that
    reads as a bullet starts the options; every bullet line from there
    on is one option, in source order, whatever else sits between them."""
    lines = text.split("\n")
    start = len(lines)
    for index, line in enumerate(lines):
        if OPTION_LINE_RE.match(line):
            start = index
            break
    prompt = "\n".join(lines[:start]).strip()
    options = [m.group(1) for line in lines[start:] for m in [OPTION_LINE_RE.match(line)] if m]
    return prompt, options


def _check_balanced_gaps(text: str, path: Path, question_id: str) -> None:
    """Every `{` in a fill-in-the-blank question's text closes, and every
    `}` closes one that opened. Gaps are one flat level (GAP_RE), so a
    depth counter is all this needs; it is not checking that `{...}`
    nests correctly, only that it closes at all.
    """
    depth = 0
    for char in text:
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                fail(path, f"question {question_id!r} has a }} with no matching {{")
    if depth > 0:
        fail(path, f"question {question_id!r} has an unclosed {{")


def parse_question(body: str, path: Path) -> Question:
    """Read `id:`, `type:` and `correct:` off the top of a ```question
    fence — the same header loop parse_cell() and parse_hint() use.
    Everything after the header lines is the question's own markdown:
    the prompt (and, for multiple-choice, the options after it) or the
    sentence with its {...} gaps for a fill-in-the-blank one.
    """
    lines = body.split("\n")
    header: dict[str, str] = {}
    while lines:
        match = QUESTION_HEADER_RE.match(lines[0])
        if not match or match.group(1) in header:
            break
        header[match.group(1)] = match.group(2).strip()
        lines.pop(0)
    if "id" not in header:
        fail(path, "a question fence has no `id:` line — ids are what saved answers match on")
    question_id = header["id"]
    if "type" not in header:
        fail(path, f"question {question_id!r} has no `type:` line")
    question_type = header["type"]
    if question_type not in QUESTION_TYPES:
        fail(path, f"question {question_id!r}'s type is {question_type!r}, "
                   f"not one of {sorted(QUESTION_TYPES)}")
    text = "\n".join(lines).strip("\n")
    if not text.strip():
        fail(path, f"question {question_id!r} has no text in it")
    no_footnotes_in(text, path, f"question {question_id!r}")

    if question_type == "multiple-choice":
        prompt, options = _split_multiple_choice(text)
        if not prompt:
            fail(path, f"question {question_id!r} has options but no question above them")
        if len(options) < 2:
            fail(path, f"question {question_id!r} has fewer than two options")
        raw_correct = header.get("correct")
        if not raw_correct:
            fail(path, f"question {question_id!r} is multiple-choice and has no `correct:` line")
        if not raw_correct.isdigit() or not (1 <= int(raw_correct) <= len(options)):
            fail(path, f"question {question_id!r}'s `correct: {raw_correct}` does not "
                       f"name one of its {len(options)} options")
        return Question(id=question_id, type=question_type, prompt=prompt,
                         options=options, correct=int(raw_correct))

    _check_balanced_gaps(text, path, question_id)
    if not GAP_RE.search(text):
        fail(path, f"question {question_id!r} is fill-in-the-blank and has no {{...}} gap in it")
    return Question(id=question_id, type=question_type, prompt=text)


def render_question(question: Question) -> str:
    """The markup `buildQuestions()` (tutorial-runtime.js) binds a Check
    button and its feedback to.

    Correctness lives in the markup itself, on the option or gap it
    belongs to (`data-correct="true"`, or a typing gap's own
    `data-expected`), rather than in a separate manifest entry: a reader
    who opens the page's source can read the answer, which is the right
    trade for a self-check and the wrong one for an exam. Marking the
    answer instead of its position is also what lets the runtime shuffle
    the options it draws without a second, parallel record of which one
    moved where.

    Both types share the same outer shell (a prompt, a Check button, a
    closed feedback slot) and differ only in what sits between: a column
    of option buttons for multiple-choice, or the prompt's own sentence
    with each {...} gap already turned into a real control for
    fill-in-the-blank.
    """
    safe_id = html.escape(question.id, quote=True)
    if question.type == "multiple-choice":
        prompt_html = convert_prose_with_math(question.prompt)
        option_items = []
        for position, option_text in enumerate(question.options, start=1):
            option_html = convert_prose_with_math(option_text)
            # A single paragraph's own <p>...</p>, unwrapped: an option is
            # inline content sitting on a button, not a block of its own.
            if option_html.startswith("<p>") and option_html.endswith("</p>"):
                option_html = option_html[len("<p>"):-len("</p>")]
            correct_attr = ' data-correct="true"' if position == question.correct else ""
            option_items.append(
                f'<button type="button" class="dl-question-option" '
                f'data-option="{position}"{correct_attr}>{option_html}</button>'
            )
        options_html = (
            '<div class="dl-question-options" role="group" '
            f'aria-label="Choose one">{"".join(option_items)}</div>'
        )
    else:
        def gap_widget(raw: str) -> str:
            choices = [c.strip() for c in raw.split("|")] if "|" in raw else None
            if choices is not None:
                option_tags = "".join(
                    (f'<option data-correct="true">{html.escape(choice)}</option>' if i == 0
                     else f"<option>{html.escape(choice)}</option>")
                    for i, choice in enumerate(choices)
                )
                return f'<select class="dl-question-gap-select">{option_tags}</select>'
            expected = raw.strip()
            return (
                '<input type="text" class="dl-question-gap-input" '
                f'data-expected="{html.escape(expected, quote=True)}" '
                f'size="{max(len(expected), 3)}">'
            )

        # {...} is protected from Markdown the same way $...$ maths is
        # (extract_math): a bare alphanumeric token — the same shape as
        # extract_math's own "dlmath0z" — stands in for each gap while
        # the sentence around it is converted, then the real widget is
        # spliced back in. A gap can sit mid-sentence, where a fence's
        # own placeholder comment would not survive Markdown's inline
        # pass the way it survives a block fence.
        #
        # Gaps are tokenised first, math second (inside
        # convert_prose_with_math): a dollar sign that happens to sit
        # inside a gap's own {...} — a price as one of the choices, say
        # — is already gone from the text convert_prose_with_math sees,
        # so it is never mistaken for the start of a maths span.
        gaps = GAP_RE.findall(question.prompt)
        tokenised = GAP_RE.sub(lambda m: f"dlgap{len(GAP_RE.findall(question.prompt[:m.start()]))}z", question.prompt)
        prompt_html = convert_prose_with_math(tokenised)
        for index, raw in enumerate(gaps):
            prompt_html = prompt_html.replace(f"dlgap{index}z", gap_widget(raw))
        options_html = ""
    return (
        f'<div class="dl-question" id="dl-question-{safe_id}" '
        f'data-question-id="{safe_id}" data-question-type="{question.type}">'
        f'<div class="dl-question-prompt">{prompt_html}</div>'
        f"{options_html}"
        '<button type="button" class="dl-btn dl-question-check" disabled>Check</button>'
        '<div class="dl-question-feedback" hidden></div>'
        "</div>"
    )


def extract_blocks(
    body: str, path: Path,
) -> tuple[str, list[Cell], list[CodeBlock], list[StagedHint], list[SiteEditor], list[Question],
           list[AppCell]]:
    """Pull every fence out, leaving a comment placeholder markdown will keep.

    An `exec` fence becomes a cell; a `hint` fence becomes a staged hint;
    an `html site`/`css site`/`js site` fence
    becomes one pane of a `SiteEditor`, grouped with any of the same
    `site:` name immediately before or after it; a `question` fence
    becomes a `Question`; an `html app`/
    `css app`/`js app` fence becomes one pane of an `AppCell`, grouped
    the same way by its `app:` name; any other fence becomes an
    illustrative, read-only block.
    All six leave the source before the markdown converter runs, so
    nothing inside any of them can be reinterpreted as markup.
    """
    cells: list[Cell] = []
    blocks: list[CodeBlock] = []
    hints: list[StagedHint] = []
    site_editors: list[SiteEditor] = []
    questions: list[Question] = []
    app_cells: list[AppCell] = []
    hints_per_cell: dict[str, int] = {}
    used_site_names: set[str] = set()
    current_site: SiteEditor | None = None
    last_site_pane_end = -1
    used_app_names: set[str] = set()
    current_app: AppCell | None = None
    last_app_pane_end = -1

    def one(match: re.Match) -> str:
        nonlocal current_site, last_site_pane_end, current_app, last_app_pane_end
        info = match.group("info").strip().split()
        indent = match.group("indent")
        if "exec" in info:
            cell_type = info[0] if info[0] != "exec" else "python"
            if cell_type not in CELL_TYPES:
                fail(path, f"an exec cell's fence starts with {cell_type!r}, "
                           f"not one of {sorted(CELL_TYPES)}")
            cells.append(parse_cell(match.group("body"), path, cell_type))
            return f"{indent}<!--dewlab-cell-{len(cells) - 1}-->"
        if info and info[0] == "hint":
            hint = parse_hint(match.group("body"), path, cells[-1].id if cells else None)
            hint.index = hints_per_cell.get(hint.cell, 0)
            hints_per_cell[hint.cell] = hint.index + 1
            hints.append(hint)
            return f"{indent}<!--dewlab-hint-{len(hints) - 1}-->"
        if len(info) >= 2 and info[1] == "site":
            language = info[0]
            if language not in SITE_LANGS:
                fail(path, f"a site pane's fence starts with {language!r}, "
                           f"not one of {sorted(SITE_LANGS)}")
            pane = parse_site_pane(match.group("body"), path, language)
            adjacent = (
                current_site is not None
                and current_site.name == pane.site
                and not body[last_site_pane_end:match.start()].strip()
            )
            last_site_pane_end = match.end()
            if adjacent:
                if pane.language in current_site.panes:
                    fail(path, f"the {pane.site!r} site editor has two "
                               f"{pane.language} panes")
                current_site.panes[pane.language] = pane
                return ""
            if pane.site in used_site_names:
                fail(path, f"site editor blocks named {pane.site!r} are not "
                           "consecutive — keep every html/css/js pane for "
                           "one site together")
            used_site_names.add(pane.site)
            current_site = SiteEditor(name=pane.site, panes={pane.language: pane})
            site_editors.append(current_site)
            return f"{indent}<!--dewlab-site-{len(site_editors) - 1}-->"
        if info and info[0] == "question":
            questions.append(parse_question(match.group("body"), path))
            return f"{indent}<!--dewlab-question-{len(questions) - 1}-->"
        if len(info) >= 2 and info[1] == "app":
            language = info[0]
            if language not in APP_LANGS:
                fail(path, f"an app pane's fence starts with {language!r}, "
                           f"not one of {sorted(APP_LANGS)}")
            pane = parse_app_pane(match.group("body"), path, language)
            adjacent = (
                current_app is not None
                and current_app.name == pane.app
                and not body[last_app_pane_end:match.start()].strip()
            )
            last_app_pane_end = match.end()
            if adjacent:
                if pane.language in current_app.panes:
                    fail(path, f"the {pane.app!r} full-stack cell has two "
                               f"{pane.language} panes")
                current_app.panes[pane.language] = pane
                return ""
            if pane.app in used_app_names:
                fail(path, f"full-stack cell blocks named {pane.app!r} are not "
                           "consecutive — keep every html/css/js pane for "
                           "one cell together")
            used_app_names.add(pane.app)
            current_app = AppCell(name=pane.app, panes={pane.language: pane})
            app_cells.append(current_app)
            return f"{indent}<!--dewlab-app-{len(app_cells) - 1}-->"
        language = info[0] if info else ""
        blocks.append(CodeBlock(language=language, code=match.group("body").strip("\n")))
        return f"{indent}<!--dewlab-code-{len(blocks) - 1}-->"

    rewritten = FENCE_RE.sub(one, body)
    seen: set[str] = set()
    for cell in cells:
        if cell.id in seen:
            fail(path, f"two exec cells share the id {cell.id!r}")
        seen.add(cell.id)
    for editor in site_editors:
        for pane in editor.panes.values():
            if pane.id in seen:
                fail(path, f"two cells share the id {pane.id!r}")
            seen.add(pane.id)
    for hint in hints:
        if hint.cell not in seen:
            fail(path, f"a hint names a cell this tutorial does not have: {hint.cell!r}")
    for question in questions:
        # Ids are unique across a page, questions and cells together —
        # both are keys into the one saved-work record (saveNow(),
        # tutorial-runtime.js), and a page cannot save two things under
        # the same key.
        if question.id in seen:
            fail(path, f"question {question.id!r} shares its id with a cell "
                       "or another question on this page")
        seen.add(question.id)
    for cell in app_cells:
        if "js" not in cell.panes:
            fail(path, f"the {cell.name!r} full-stack cell has no js pane — "
                       "a cell with nothing to run is not a cell")
        for pane in cell.panes.values():
            if pane.id in seen:
                fail(path, f"two cells share the id {pane.id!r}")
            seen.add(pane.id)
    return rewritten, cells, blocks, hints, site_editors, questions, app_cells


def extract_math(body: str, found: list[Math] | None = None) -> tuple[str, list[Math]]:
    """Lift $…$ and $$…$$ out, leaving a token markdown will not touch.

    The placeholder is a bare alphanumeric word on purpose: an HTML comment
    works for a block-level fence but not mid-sentence, where markdown's inline
    pass can reach it.

    `found` lets a second piece of text — a staged hint's body, converted on
    its own — number its tokens after the page's, so place_blocks() renders
    both from the one list.
    """
    if found is None:
        found = []
    body = body.replace("\\$", ESCAPED_DOLLAR)

    def take(display: bool):
        def one(match: re.Match) -> str:
            found.append(Math(tex=match.group("tex").strip(), display=display))
            return f"dlmath{len(found) - 1}z"

        return one

    body = DISPLAY_MATH_RE.sub(take(True), body)
    body = INLINE_MATH_RE.sub(take(False), body)
    return body.replace(ESCAPED_DOLLAR, "$"), found


def icon_button(css_class: str, icon: str, label: str, **attrs: str) -> str:
    """A button that can read as icon-only, label-only, or both, at the
    reader's own choice (Settings → "Cell buttons", `dewlab:button-labels`)
    — one shared shape for every cell-chrome button on both this page and
    dewmini's own `iconButton()` (`compose/dewmini.js`), so a setting
    flipped on one means the same thing on both. `icon` is markup already
    (an entity or a nested span), never escaped again here; `label` is
    plain text, escaped once. CSS hides whichever span the setting says
    not to show; nothing here decides that.
    """
    attr_str = "".join(f' {key}="{html.escape(str(value), quote=True)}"' for key, value in attrs.items())
    return (
        f'<button type="button" class="dl-btn {css_class}"{attr_str}>'
        f'<span class="dl-btn-icon" aria-hidden="true">{icon}</span>'
        f'<span class="dl-btn-label">{html.escape(label)}</span>'
        "</button>"
    )


def render_cell(cell: Cell, number: int, page: str = "", version: str = "") -> str:
    """The markup the runtime binds an editor, a Run button and an output area to.

    Three rows, top to bottom: a header (the numbered pill, an optional
    `cell.name`, Duplicate); the code, with a collapse triangle beside it;
    a footer (Run, Reset, the run-line, the "Run above/below" menu) sitting
    between the code and its output, so Run is where a reader's hand
    already is. `number` is the cell's fixed 1-based position on the page —
    an authored cell never reorders at runtime, unlike a reader's own
    custom cells. No drag handle, for the same reason.

    Reset restores this cell's *starter code*, not just its output — an
    authored cell has a fixed starting point to return to, so it gets a
    different icon from a plain Clear.

    `code` and `output` are left blank here and filled in by
    `tutorial-runtime.js` once the reader has actually run something; the
    run-line and the "Run above/below" menu are likewise empty shells it
    wires up. `.dl-cell-collapsed-summary` is filled the same way by
    `setCellCollapsed()`, once the cell is actually collapsed.

    Duplicate copies this cell's current code into a new custom cell
    dropped right after it, reusing the insertion seam
    `initCustomCellsSection()` already places after every real cell — the
    original stays the tutorial's own fixed content; the copy is the
    reader's to edit or delete.

    The report icon toggles a plain block after the cell, the same pattern
    as the hint icon beside it, and only appears when `page` is set and
    feedback is enabled — a custom cell (the reader's own) never gets one,
    since there's nothing to report about code nobody but the reader wrote.
    `updateCellReportLinks()` in `tutorial-runtime.js` fills in its actual
    link once the panel opens.
    """
    safe_id = html.escape(cell.id, quote=True)
    hint_markup = ""
    if cell.hint:
        hint_markup = (
            f'<button type="button" class="dl-hint-icon" aria-expanded="false" '
            f'aria-controls="dl-hint-{safe_id}" aria-label="Hint for {safe_id}">?</button>'
        )
    hint_text = ""
    if cell.hint:
        hint_text = (
            f'<div class="dl-hint-text" id="dl-hint-{safe_id}" hidden>'
            f"{html.escape(cell.hint)}</div>"
        )
    report_markup = ""
    report_box = ""
    if page and feedback_enabled():
        report_markup = (
            f'<button type="button" class="dl-report-icon" aria-expanded="false" '
            f'aria-controls="dl-report-{safe_id}" '
            f'aria-label="Give feedback on Cell {number}" '
            f'title="Give feedback on this cell">&#9873;</button>'
        )
        report_box = (
            f'<div class="dl-report-doors dl-cell-report-doors" '
            f'id="dl-report-{safe_id}" hidden>'
            f"{report_doors_links(page, version, cell=cell.id)}"
            "</div>"
        )
    name_markup = ""
    if cell.name:
        name_markup = f'<span class="dl-cell-name">{html.escape(cell.name)}</span>'
    type_label = "SQL" if cell.type == "sql" else "Python"
    return (
        f'<div class="dl-cell" data-cell-id="{safe_id}">'
        '<div class="dl-cell-head">'
        '<span class="dl-cell-pill">'
        f'<span class="dl-cell-pill-num">Cell {number}</span>'
        f'<span class="dl-cell-pill-type" data-type="{cell.type}">{type_label}</span>'
        "</span>"
        f"{name_markup}"
        '<span class="dl-cell-spacer"></span>'
        '<div class="dl-cell-header-end">'
        f"{hint_markup}"
        f"{report_markup}"
        + icon_button("dl-btn-duplicate", "&#10697;", "Duplicate",
                      title="Copy this cell into your own, right below it")
        + "</div>"
        "</div>"
        '<div class="dl-cell-body-row">'
        '<div class="dl-cell-collapse-col">'
        '<button type="button" class="dl-collapse-toggle" aria-expanded="true" '
        'title="Collapse this cell">'
        '<span class="dl-collapse-caret" aria-hidden="true">&#8250;</span>'
        "</button>"
        "</div>"
        '<div class="dl-cell-content"><div class="dl-editor"></div></div>'
        '<div class="dl-cell-collapsed-summary" role="button" tabindex="0" hidden></div>'
        "</div>"
        '<div class="dl-cell-footbar">'
        + icon_button("dl-btn-run", "&#9654;", "Loading…", disabled="disabled")
        + icon_button("dl-btn-reset", "&#8634;", "Reset",
                      title="Clear this cell's output")
        + icon_button("dl-btn-clear", "&#8635;", "Clear",
                      title="Put this cell's starter code back, and clear its output")
        + '<div class="dl-cell-more">'
        + icon_button("dl-btn-more", "&#8943;", "More",
                      **{"aria-haspopup": "true", "aria-expanded": "false",
                         "title": "More ways to run this cell"})
        + '<div class="dl-cell-run-menu" role="menu" hidden>'
        '<button type="button" class="dl-cell-run-menu-item" role="menuitem" '
        'data-run-menu="above">Run this cell and all above</button>'
        '<button type="button" class="dl-cell-run-menu-item" role="menuitem" '
        'data-run-menu="below">Run this cell and all below</button>'
        "</div>"
        "</div>"
        '<span class="dl-cell-spacer"></span>'
        '<span class="dl-hint-marker" hidden aria-hidden="true" '
        'title="A hint has appeared below this cell"></span>'
        '<span class="dl-cell-runline"></span>'
        "</div>"
        '<div class="dl-output"></div>'
        f"{hint_text}"
        f"{report_box}"
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


def render_site_editor(editor: SiteEditor, index: int) -> str:
    """The markup a live HTML/CSS/JS editor and its preview mount onto.

    Each pane present in `editor.panes` gets an empty `.dl-editor`, the
    same convention `render_cell()` uses for a Python or SQL cell: the
    pane's actual starting source travels in the manifest, not the DOM,
    and `tutorial-runtime.js` fills the editor in and mounts the live
    preview using `assets/site-relay.js`'s `mountSitePreview()`
    the moment the page is ready — there is no
    meaningful no-JavaScript fallback for a live preview the way
    `render_code_block()`'s escaped `<pre>` is one for a read-only
    example. A pane absent from `editor.panes` gets no box at all, unlike
    dewmini's own Site tab, which always shows three regardless — most of
    dewstack's own web-authoring pages are HTML+CSS only, and an
    HTML-only page with two permanently empty boxes beside it would look
    broken rather than minimal.

    `index` is this editor's plain 1-based position among the page's site
    editors, the same role `render_cell()`'s `number` plays for cells; it
    also makes the preview-width slider's own `id` unique when a page has
    more than one editor, so its `<label for=...>` still points at the
    right control.

    The preview-width slider itself (`.dl-site-preview-controls`, a
    30%-100% range setting `.dl-site-frame`'s own inline width) is a
    media-query lesson's actual apparatus, not decoration — a page that
    asks a reader to "drag the preview narrower" needs a preview that can
    get narrower, and a fixed-width iframe alone cannot demonstrate that
    (found porting `media-queries` and three other `web-authoring`
    tutorials that assume it; `dewminiweb.js` already carries the
    identical control for its own workspace, wired here the same way).
    """
    safe_name = html.escape(editor.name, quote=True)
    labels = {"html": "HTML", "css": "CSS", "js": "JavaScript"}
    panes_markup = []
    for lang in ("html", "css", "js"):
        if lang not in editor.panes:
            continue
        run_markup = (
            icon_button("dl-btn-site-run", "&#9654;", "Run",
                        title="Run this script (Ctrl+Enter or Cmd+Enter in the pane)")
            if lang == "js" else ""
        )
        panes_markup.append(
            f'<div class="dl-site-pane" data-lang="{lang}">'
            '<div class="dl-site-pane-head">'
            f'<span class="dl-web-pane-label">{labels[lang]}</span>'
            f"{run_markup}"
            "</div>"
            '<div class="dl-editor"></div>'
            "</div>"
        )
    console_markup = ""
    if "js" in editor.panes:
        console_markup = (
            '<div class="dl-site-console">'
            '<div class="dl-web-pane-label">Console</div>'
            '<div class="dl-site-console-output" aria-live="polite"></div>'
            "</div>"
        )
    width_id = f"dl-site-width-{index}"
    return (
        f'<div class="dl-site-editor" data-site-name="{safe_name}">'
        '<div class="dl-site-head">'
        + icon_button("dl-btn-site-clear", "&#8635;", "Clear",
                      title="Put this editor's starter code back, in every pane")
        + "</div>"
        '<div class="dl-site-split">'
        f'<div class="dl-site-editors">{"".join(panes_markup)}</div>'
        '<div class="dl-site-preview">'
        '<div class="dl-site-preview-controls">'
        f'<label for="{width_id}">Preview width</label>'
        f'<input type="range" id="{width_id}" class="dl-site-width" '
        'min="30" max="100" step="5" value="100" '
        'aria-label="Preview width, as a percentage">'
        f'<output for="{width_id}">100%</output>'
        "</div>"
        f'<iframe class="dl-site-frame" sandbox="allow-scripts" '
        f"title=\"{safe_name}'s preview\"></iframe>"
        f"{console_markup}"
        "</div>"
        "</div>"
        "</div>"
    )


def render_app_cell(cell: AppCell, index: int) -> str:
    """The markup a full-stack cell's panes, preview and error box mount
    onto.

    Shares `render_site_editor()`'s own shape — panes over a result area,
    a head-level Clear, a per-pane Run button on the JS pane only, HTML
    and CSS live without pressing Run — but the result area is not an
    iframe: HTML and CSS render straight into `.dl-app-preview`, and the
    JS pane's code runs as a real `<script>` element appended to the
    page (`buildAppCells()`, `assets/tutorial-runtime.js`). That is the
    one deliberate difference from a site editor, and it is a difference
    for a reason: a full-stack cell's whole point is a query's own
    result becoming what a reader sees, and a site editor's sandboxed
    iframe exists specifically to stop a reader's script reaching
    anything else on the page — exactly the channel this needs, to read
    the page's own shared SQL connection through `_query_rows()`.

    `index` plays the same role `render_site_editor()`'s own `index`
    does — this cell's 1-based position among the page's app cells, used
    only to keep this function's own element ids from colliding across
    more than one app cell on a page.
    """
    safe_name = html.escape(cell.name, quote=True)
    labels = {"html": "HTML", "css": "CSS", "js": "JavaScript"}
    panes_markup = []
    for lang in ("html", "css", "js"):
        if lang not in cell.panes:
            continue
        run_markup = (
            icon_button("dl-btn-app-run", "&#9654;", "Run",
                        title="Run this script (Ctrl+Enter or Cmd+Enter in the pane)")
            if lang == "js" else ""
        )
        panes_markup.append(
            f'<div class="dl-app-pane" data-lang="{lang}">'
            '<div class="dl-app-pane-head">'
            f'<span class="dl-web-pane-label">{labels[lang]}</span>'
            f"{run_markup}"
            "</div>"
            '<div class="dl-editor"></div>'
            "</div>"
        )
    preview_id = f"dl-app-preview-{index}"
    error_id = f"dl-app-error-{index}"
    return (
        f'<div class="dl-app-cell" data-app-name="{safe_name}">'
        '<div class="dl-app-head">'
        + icon_button("dl-btn-app-clear", "&#8635;", "Clear",
                      title="Put this cell's starter code back, in every pane")
        + "</div>"
        '<div class="dl-app-split">'
        f'<div class="dl-app-panes">{"".join(panes_markup)}</div>'
        '<div class="dl-app-result">'
        f'<div class="dl-app-preview" id="{preview_id}"></div>'
        f'<pre class="dl-app-error" id="{error_id}" aria-live="polite"></pre>'
        "</div>"
        "</div>"
        "</div>"
    )


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
    converter = markdown.Markdown(
        extensions=["extra", "sane_lists", "toc",
                    "pymdownx.tilde", "pymdownx.tasklist"],
        # `tilde` gives `~~struck out~~` as `<del>`, and would also give a
        # single `~2~` as a subscript. Subscript is off: a lone tilde is
        # already prose here — "~1,000", "after ~5 minutes", a CSS
        # `:checked ~ .toggle` selector — and two of those on nearby lines
        # would pair up into a subscript spanning them.
        extension_configs={"pymdownx.tilde": {"subscript": False}},
    )
    html_out = converter.convert(mark_markdown_wrappers(body))
    return html_out, list(getattr(converter, "toc_tokens", []))


def mark_markdown_wrappers(body: str) -> str:
    """Adds `markdown="1"` to each wrapper listed in MARKDOWN_WRAPPER_RE.

    Python-Markdown treats a raw HTML block as opaque: it swallows the
    whole element through to its closing tag and never looks inside, so a
    heading, a numbered list or a backtick span written inside a fold or a
    section wrapper would reach the page as literal text. `md_in_html`
    (already here, inside `extra`) parses the children of any element
    carrying `markdown="1"`, choosing block or inline per child, and
    strips the attribute from the output. Adding it here rather than
    asking authors to write it keeps the source plain, and keeps which
    elements get parsed a decision this file makes.

    A `<ul class="dl-feature-list">` needs no special case: `md_in_html`
    already knows a `<ul>` holds `<li>` children, so a markdown bullet
    list inside one becomes those items rather than a second nested
    `<ul>`.

    A `<aside class="dl-note">` is marked here too, even though it never
    stays on the page: `extract_notes()` pulls it out of the converted
    body afterwards, and its contents are already HTML by then.
    """
    return MARKDOWN_WRAPPER_RE.sub(lambda m: f'{m.group(0)[:-1]} markdown="1">', body)


def convert_prose_with_math(text: str) -> str:
    """Markdown to HTML, with `$…$`/`$$…$$` typeset via KaTeX.

    The tutorial's own body gets this for free: `load()` runs
    `extract_math()` once, up front, and hands the shared list to
    `place_blocks()` to resolve once everything else has been placed.
    Everything else that converts a piece of author markdown on its own
    — a card's body, a question's prompt and options, a pedagogical
    note, a hand-written practice-page fold, a page's own prose or one
    of its section wrappers — has no such shared list to append to, and
    no guarantee it runs before whatever *would* resolve one. So this is
    the same two-step `extract_math()`/`render_math()` dance, self-
    contained: a fresh list, numbered from zero, extracted and resolved
    in the one call, which is what makes it safe to use anywhere,
    independent of where in the build's pipeline that call happens to
    sit.

    A footnote cannot cross this edge. Each call converts its text as a
    document of its own, and the `footnotes` extension collects a
    document's definitions at the end of that document — so a reference
    here never finds a definition in the page's prose, and a pair written
    here renders its own rule and numbered list where it sits. The three
    fence parsers refuse one outright rather than let either happen
    quietly; see no_footnotes_in().
    """
    stripped, maths = extract_math(text)
    html_out, _ = to_html(stripped)
    for index, item in enumerate(maths):
        html_out = html_out.replace(f"dlmath{index}z", render_math(item))
    return html_out


def parse_card(fence_body: str, path: Path) -> PageCard:
    """A ```card fence's body: `url:`/`status:`/`meta:`/`wide:` header lines
    (dewlab's own header-line idiom — see HEADER_RE, SITE_HEADER_RE,
    HINT_HEADER_RE — applied to a fourth fence kind), then a markdown
    heading and, optionally, a paragraph or two underneath it.
    """
    lines = fence_body.split("\n")
    header: dict[str, str] = {}
    index = 0
    while index < len(lines):
        match = CARD_HEADER_RE.match(lines[index])
        if not match:
            break
        header[match.group(1)] = match.group(2).strip()
        index += 1
    rest = "\n".join(lines[index:]).strip("\n")
    if "url" not in header:
        fail(path, "a card fence has no url: header line")
    no_footnotes_in(rest, path, f"the card linking to {header['url']!r}")
    first_line, _, remainder = rest.partition("\n")
    heading_match = re.match(r"^#{1,6}\s*(?P<heading>.+?)\s*#*$", first_line)
    if not heading_match:
        fail(path, "a card fence's body must open with a markdown heading")
    body_html = convert_prose_with_math(remainder.strip("\n")) if remainder.strip() else ""
    return PageCard(
        url=header["url"],
        heading=heading_match.group("heading"),
        body_html=body_html,
        status=header.get("status") or None,
        meta=header.get("meta") or None,
        wide=header.get("wide", "").lower() in ("true", "yes"),
    )


def render_card(card: PageCard) -> str:
    """The exact `.dl-module-card` markup `render_index()` used to hand-write
    six times over — now built once, from a `PageCard` either dialect of
    fence parsing hands it.
    """
    classes = "dl-module-card dl-module-card-wide" if card.wide else "dl-module-card"
    badge = (
        f'<span class="dl-module-card-badge" data-status="{html.escape(card.status, quote=True)}">'
        f"{html.escape(card.status.capitalize())}</span>"
        if card.status else ""
    )
    meta = (
        f'<span class="dl-module-card-meta">{html.escape(card.meta)}</span>'
        if card.meta else ""
    )
    return (
        f'<a class="{classes}" href="{html.escape(card.url, quote=True)}">'
        f"<h3>{html.escape(card.heading)}{badge}</h3>{meta}{card.body_html}</a>"
    )


def extract_page_cards(body: str, path: Path) -> tuple[str, list[PageCard]]:
    """Pulls every ```card fence out of a page's markdown, leaving an HTML
    comment placeholder — the same fence-to-placeholder convention
    `extract_blocks()` uses for a tutorial's own cells, so a card's contents
    never gets a chance to be reinterpreted as prose. A fence tagged
    anything else is left exactly as it was.
    """
    cards: list[PageCard] = []

    def one(match: re.Match) -> str:
        if match.group("info").strip() != "card":
            return match.group(0)
        cards.append(parse_card(match.group("body"), path))
        return f"{match.group('indent')}<!--dewlab-page-card-{len(cards) - 1}-->"

    return FENCE_RE.sub(one, body), cards


def place_page_cards(page_html: str, cards: list[PageCard]) -> str:
    """Replaces each card placeholder with its rendered `.dl-module-card`
    tile, first wrapping every run of one or more adjacent placeholders in
    a single `.dl-module-grid` — the same "adjacent fences of a kind become
    one enclosing structure" rule `extract_blocks()` already applies to a
    site editor's consecutive html/css/js panes, so a page's own markdown
    never has to spell the grid wrapper out by hand.
    """
    page_html = CARD_RUN_RE.sub(lambda m: f'<div class="dl-module-grid">{m.group(0)}</div>', page_html)
    for index, card in enumerate(cards):
        placeholder = f"<!--dewlab-page-card-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"a card linking to {card.url!r} was lost during markdown conversion")
        page_html = page_html.replace(placeholder, render_card(card))
    return page_html


# Infrastructure a page's markdown can point at with a [[name]] marker but
# never author directly — each a page-independent, no-argument HTML
# renderer already defined elsewhere in this file. A lambda, not the
# function itself, since GENERATED_BLOCKS is built before render_search_box
# exists in this module's namespace, and only needs to by the time a page
# actually asks for one.
GENERATED_BLOCKS: dict[str, Callable[[], str]] = {
    "search-box": lambda: render_search_box(
        "Search by topic — e.g. loops, probability, sorting…", big=True, hint=False),
    "course-cards": lambda: render_course_cards(),
}


def extract_generated_blocks(body: str, path: Path) -> tuple[str, list[str]]:
    names: list[str] = []

    def one(match: re.Match) -> str:
        name = match.group("name")
        if name not in GENERATED_BLOCKS:
            fail(path, f"[[{name}]] is not a generated block dewlab knows — "
                       f"one of {sorted(GENERATED_BLOCKS)}")
        names.append(name)
        return f"<!--dewlab-generated-{len(names) - 1}-->"

    return GENERATED_BLOCK_RE.sub(one, body), names


def place_generated_blocks(page_html: str, names: list[str]) -> str:
    for index, name in enumerate(names):
        page_html = page_html.replace(f"<!--dewlab-generated-{index}-->", GENERATED_BLOCKS[name]())
    return page_html


def read_page(name: str) -> tuple[dict, str]:
    """Reads `pages/<name>.md`: a hand-written site page, not a tutorial.

    A page has no module, series, or version — it isn't part of the
    curriculum, so `split_frontmatter()`'s validation (which demands all
    of those) doesn't apply. Frontmatter here is only ever `title`, and the
    body converts through the same `to_html()` every tutorial's prose does,
    so a page reads like the rest of the site rather than needing its own
    rendering rules. A ```card fence, a `[[name]]` generated-block marker,
    and a `<div class="dl-hero">`/`<div class="dl-audience">`/`<ul
    class="dl-feature-list">` section or list wrapper are the three things
    a page can have that ordinary prose doesn't — the first two extracted
    before conversion and placed back after, the same extract-then-place
    shape `place_blocks()` uses for a tutorial's cells; the third marked
    for `md_in_html` by `mark_markdown_wrappers()`, the same way a
    `<details>` fold is. Returns the frontmatter mapping and the rendered body
    — never the raw markdown.
    """
    path = PAGES / f"{name}.md"
    if not path.is_file():
        fail(path, "does not exist — every page under pages/ needs a file")
    text = path.read_text()
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
    if not isinstance(meta, dict) or "title" not in meta:
        fail(path, "frontmatter is missing title")
    body = body.lstrip("\n")
    body, cards = extract_page_cards(body, path)
    body, generated = extract_generated_blocks(body, path)
    body_html = convert_prose_with_math(body)
    body_html = place_page_cards(body_html, cards)
    body_html = place_generated_blocks(body_html, generated)
    return meta, body_html


def place_blocks(
    page_html: str, cells: list[Cell], blocks: list[CodeBlock], maths: list[Math],
    site_editors: list[SiteEditor] | None = None, questions: list[Question] | None = None,
    app_cells: list[AppCell] | None = None, page: str = "", version: str = "",
) -> str:
    """Puts cells, illustrative code blocks, site editors, questions, app
    cells, and maths back into the page after the Markdown converter has run.
    `extract_blocks`/`extract_math` earlier in the pipeline replaced each
    of these with a plain placeholder string before handing the body to
    the Markdown library — this is the matching second half, swapping
    each placeholder back out for its real rendered HTML. Doing it this
    way (rather than rendering cells and maths inline, before Markdown
    sees them) is what protects their content from Markdown's own
    text-formatting rules — see `extract_math`'s own comment for a
    concrete example of what goes wrong otherwise.

    `page` and `version` are only for `render_cell()`'s own report panel
    — passed straight through, since this
    function runs from `load()`, before the file has become a `Tutorial`
    object with a `.slug` of its own (`page` is `id_of(path)`).
    """
    for index, cell in enumerate(cells):
        placeholder = f"<!--dewlab-cell-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"cell {cell.id!r} was lost during markdown conversion")
        page_html = page_html.replace(
            placeholder, render_cell(cell, index + 1, page, version)
        )
    for index, block in enumerate(blocks):
        page_html = page_html.replace(f"<!--dewlab-code-{index}-->", render_code_block(block))
    for index, editor in enumerate(site_editors or []):
        placeholder = f"<!--dewlab-site-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"site editor {editor.name!r} was lost during markdown conversion")
        page_html = page_html.replace(placeholder, render_site_editor(editor, index + 1))
    for index, question in enumerate(questions or []):
        placeholder = f"<!--dewlab-question-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"question {question.id!r} was lost during markdown conversion")
        page_html = page_html.replace(placeholder, render_question(question))
    for index, app_cell in enumerate(app_cells or []):
        placeholder = f"<!--dewlab-app-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"full-stack cell {app_cell.name!r} was lost during markdown conversion")
        page_html = page_html.replace(placeholder, render_app_cell(app_cell, index + 1))
    for index, item in enumerate(maths):
        page_html = page_html.replace(f"dlmath{index}z", render_math(item))
    return page_html


def extract_notes(body_html: str, path: Path) -> tuple[str, list[Note]]:
    """Pull every pedagogical note out of the page body and into its own
    list. A note is authored as an HTML aside (`NOTE_RE`), the same
    reuse-over-invention trick the hint/answer fold already established,
    but unlike a fold it does not stay inline: it surfaces in the
    reference panel instead, so the aside is removed from the body once
    its id and content are captured.
    """
    notes: list[Note] = []
    seen: set[str] = set()

    def one(match: re.Match) -> str:
        note_id = match.group("id")
        if note_id in seen:
            fail(path, f"two notes share the id {note_id!r}")
        seen.add(note_id)
        note_html = match.group("html")
        notes.append(Note(id=note_id, html=note_html))
        return ""

    return NOTE_RE.sub(one, body_html), notes



COURSE_INDEX_FILE = "index.yaml"
REDIRECTS_FILE = "redirects.yaml"
COURSE_STATUSES = ("draft", "beta", "live")


@dataclass
class Series:
    """One heading in a course file, and the ids under it in reading order.
    `key` is the heading as a filename (series_key()); it is what a zip
    is named after and what the page's series meta carries."""

    key: str
    title: str
    ids: list[str]


@dataclass
class Course:
    """One file under courses/: everything a course page, a front-page card
    and a tree's course rung need, and the reading order of every series."""

    id: str
    path: Path
    title: str
    code: str
    status: str
    card: str
    description: list[str]
    contents: list[Series]
    mixed: list[str]

    @property
    def keys(self) -> list[str]:
        return [series.key for series in self.contents]

    def series_title(self, key: str) -> str:
        for series in self.contents:
            if series.key == key:
                return series.title
        return key


SERIES_KEY_RE = re.compile(r"[^a-z0-9]+")


def series_key(title: str) -> str:
    """A heading, as something that can name a file and sit in a URL:
    "Python fundamentals" becomes python-fundamentals. Two headings in one
    course that come out the same are refused (courses())."""
    return SERIES_KEY_RE.sub("-", title.lower()).strip("-")


def paragraphs(text: str) -> list[str]:
    """A YAML string's blank-line-separated paragraphs, each on one line."""
    return [" ".join(part.split()) for part in re.split(r"\n\s*\n", text or "") if part.strip()]


_COURSES_CACHE: tuple[tuple, dict[str, Course]] | None = None


def _courses_stamp() -> tuple:
    if not COURSES.is_dir():
        return (str(COURSES),)
    return tuple(
        (str(path), path.stat().st_mtime_ns, path.stat().st_size)
        for path in sorted(COURSES.glob("*.yaml"))
    )


def courses() -> dict[str, Course]:
    """Every course, in `courses/index.yaml` order, from `courses/*.yaml`.

    This is the one place placement is read from. A course file says what
    the course is called, which QQI code it carries, what its front-page
    card says, and — under `contents:` — its series, each a heading with
    the ids of its tutorials in reading order. A tutorial's own file says
    nothing about any of this, which is what lets one tutorial sit on two
    courses without a second copy of anything.

    Read fresh whenever the files change and cached otherwise, because
    most of the rendering below asks for it once per page: the cache is
    keyed on the files' own timestamps and sizes, so a test that writes a
    course file and calls straight in sees its own file rather than the
    last build's. The path is worked out on each call rather than held in
    a constant, for the reason module-level globals are monkeypatched in
    tests: a constant computed at import time would still point at the
    real folder.

    Optional as a whole: with no `courses/` at all, every tutorial builds
    at its address and none is on a reading order, which is what a quick
    fixture build wants.
    """
    global _COURSES_CACHE
    stamp = _courses_stamp()
    if _COURSES_CACHE is not None and _COURSES_CACHE[0] == stamp:
        return _COURSES_CACHE[1]

    found: dict[str, Course] = {}
    if COURSES.is_dir():
        for path in sorted(COURSES.glob("*.yaml")):
            if path.name in (COURSE_INDEX_FILE, REDIRECTS_FILE):
                continue
            found[path.stem] = read_course(path)

    order: list[str] = []
    index = COURSES / COURSE_INDEX_FILE
    if index.is_file():
        data = yaml.safe_load(index.read_text()) or {}
        order = data.get("order") or []
        if not isinstance(order, list) or not all(isinstance(c, str) for c in order):
            fail(index, "needs `order:` as a list of course ids, one per line")
        for name in order:
            if name not in found:
                fail(index, f"lists {name}, and there is no courses/{name}.yaml")
    # Listed courses in the order given, then any other alphabetically, so a
    # new course file lands at the end rather than breaking the page.
    ordered = [c for c in order if c in found] + sorted(c for c in found if c not in order)
    result = {name: found[name] for name in ordered}
    _COURSES_CACHE = (stamp, result)
    return result


def read_course(path: Path) -> Course:
    """One course file, checked for shape. What the ids it lists refer to is
    checked later, by place_tutorials(), once every tutorial is loaded."""
    data = load_yaml_no_duplicate_keys(path.read_text()) or {}
    if not isinstance(data, dict):
        fail(path, "a course file is a mapping: title, code, status, card, description, contents")
    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        fail(path, "needs a `title:` line — what the course is called on the site")
    status = str(data.get("status", "live"))
    if status not in COURSE_STATUSES:
        fail(path, f"status {status!r} is not one of {', '.join(COURSE_STATUSES)}")
    contents = data.get("contents")
    if contents is None:
        contents = []
    if not isinstance(contents, list):
        fail(path, "`contents:` is a list of series, each with a title and its tutorials")
    series: list[Series] = []
    listed: dict[str, str] = {}
    for entry in contents:
        if not isinstance(entry, dict) or not isinstance(entry.get("title"), str):
            fail(path, "each series under `contents:` needs a `title:` line")
        ids = entry.get("tutorials")
        if ids is None:
            ids = []
        if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids):
            fail(path, f'the series "{entry["title"]}" needs `tutorials:` as a list of ids')
        key = series_key(entry["title"])
        if not key:
            fail(path, f'the series title {entry["title"]!r} has no letters or digits in it')
        if key in {s.key for s in series}:
            fail(path, f'two series are both called "{entry["title"]}" (or differ only in '
                       "punctuation). Give one of them another title.")
        for ident in ids:
            if ident in listed:
                fail(path, f'lists {ident} twice — under "{listed[ident]}" and under '
                           f'"{entry["title"]}". A tutorial sits in one place on a course.')
            listed[ident] = entry["title"]
        series.append(Series(key=key, title=entry["title"].strip(), ids=list(ids)))
    mixed = data.get("mixed")
    if mixed is None:
        mixed = []
    if not isinstance(mixed, list) or not all(isinstance(i, str) for i in mixed):
        fail(path, "`mixed:` is a list of ids of mixed problem sets")
    for ident in mixed:
        if ident in listed:
            fail(path, f'lists {ident} under `mixed:` and under "{listed[ident]}"')
    return Course(
        id=path.stem,
        path=path,
        title=title.strip(),
        code=str(data.get("code") or "").strip(),
        status=status,
        card=str(data.get("card") or "").strip(),
        description=paragraphs(str(data.get("description") or "")),
        contents=series,
        mixed=list(mixed),
    )


def course_title(course: str) -> str:
    """What a course is called, or its id when there is no file for it —
    honest, if rarely what you would put in front of a class."""
    found = courses().get(course)
    return found.title if found else course


def legacy_ids() -> dict[str, str]:
    """For every page that had an address before courses/ existed, its old
    `module:slug` — the key its readers' saved work was stored under, which
    the runtime renames on the first visit (migrateStorage() in
    tutorial-runtime.js). Read from `courses/redirects.yaml`, since the old
    address already says both halves; a tutorial written after the change
    has no line there and no legacy id."""
    path = COURSES / REDIRECTS_FILE
    if not path.is_file():
        return {}
    data = read_yaml(path, strict=False) or {}
    legacy: dict[str, str] = {}
    old_re = re.compile(r"^tutorials/(?P<module>[^/]+)/(?P<slug>[^/]+)\.html$")
    new_re = re.compile(r"^tutorials/(?P<id>[^/]+)\.html$")
    for old, new in data.items():
        was, now = old_re.match(str(old)), new_re.match(str(new))
        if was and now:
            legacy.setdefault(now.group("id"), f"{was.group('module')}:{was.group('slug')}")
    return legacy


def place_tutorials(tutorials: list[Tutorial], registry: dict[str, Tutorial]) -> None:
    """Fill in every page's `placements` from the course files, and check
    every id a course file names.

    An id with no tutorial behind it stops the build: the course file looks
    complete and the course is short, which nothing else would ever say. A
    draft is the one exception, skipped with a note, so a course can list
    next week's tutorial before it is finished. A practice page cannot be
    listed at all — it is reached from its tutorial — and an archived one
    may be, but sits in the course's Archive rather than on the route.

    Practice pages are placed afterwards, by practice_pairs() and
    mixed_practice(), from the tutorial they belong to.
    """
    for course in courses().values():
        for series in course.contents:
            for position, ident in enumerate(series.ids, start=1):
                member = registry.get(ident)
                if member is None:
                    if (TUTORIALS / ident / f"{ident}.md").is_file():
                        print(f"note: {course.path.relative_to(ROOT)} lists {ident}, "
                              "which is a draft, so it is not on the course yet",
                              file=sys.stderr)
                        continue
                    fail(course.path, f'the series "{series.title}" lists {ident}, but '
                                      f"there is no folder tutorials/{ident}/")
                if member.is_practice:
                    fail(course.path, f'the series "{series.title}" lists {ident}, which is '
                                      "a page of problems. A practice page is reached from "
                                      "its tutorial; list the tutorial instead.")
                member.placements.append(Placement(course.id, series.key, position))
        for ident in course.mixed:
            member = registry.get(ident)
            if member is None:
                fail(course.path, f"lists {ident} under `mixed:`, but there is no folder "
                                  f"tutorials/{ident}/")
            if not member.practice_across:
                fail(course.path, f"lists {ident} under `mixed:`, and it is not a mixed "
                                  "problem set (it has no practice_across line)")
            member.placements.append(Placement(course.id, "", 0))
    # The route position: where the page sits in the series of its default
    # course. A page on no route keeps 0 (nav_for() reads that honestly).
    for tutorial in tutorials:
        if tutorial.placements and tutorial.status == "live" and tutorial.is_default:
            tutorial.order = tutorial.placements[0].position


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
    families: dict[str, list[Tutorial]] = {}
    for tutorial in tutorials:
        families.setdefault(tutorial.slug, []).append(tutorial)

    built: list[Tutorial] = []
    for slug, versions in sorted(families.items()):
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
        default = newest_live or max(versions, key=lambda v: v.released)
        for version in versions:
            version.is_default = version is default
        built.extend(versions)
    return built


def practice_pairs(
    tutorials: list[Tutorial], registry: dict[str, Tutorial]
) -> dict[str, Tutorial]:
    """Each tutorial's page of problems, by the id of the tutorial it belongs to.

    A practice page names its tutorial with `practice_for:`. Both directions are
    checked here rather than being discovered by a reader following a link that
    goes nowhere: the tutorial has to exist, and no two practice pages may
    claim the same one. The page then sits wherever its tutorial sits — it
    takes the tutorial's placements, so its tree and its course are the
    tutorial's own.

    A practice page also declares no coverage. It sets problems on what its
    tutorial taught, and counting it would report the same outcome as taught
    twice — see `planning/EXERCISES.md`.
    """
    pairs: dict[str, Tutorial] = {}
    for page in tutorials:
        target = page.practice_for
        if target and page.practice_across:
            fail(page.path, "sets both practice_for and practice_across. A page "
                            "of problems either belongs to one tutorial or "
                            "draws on several; it cannot do both.")
        if not target:
            continue
        if page.meta.get("covers"):
            fail(page.path, "is a practice page and declares `covers:`. It sets "
                            "problems on what its tutorial taught; saying so "
                            "twice would report one outcome as covered by two "
                            "pages.")
        if target == page.slug:
            fail(page.path, f"has practice_for: {target}, which is itself.")
        owner = registry.get(target)
        if owner is None:
            fail(page.path, f"has practice_for: {target}, and there is no folder "
                            f"tutorials/{target}/.")
        if owner.practice_for:
            fail(page.path, f"has practice_for: {target}, which is itself a "
                            "practice page. Problems about problems is not a "
                            "shape this supports.")
        page.placements = list(owner.placements)
        if not page.is_default:
            continue
        if target in pairs:
            fail(page.path, f"has practice_for: {target}, and so does "
                            f"{pairs[target].path.relative_to(ROOT)}. A tutorial "
                            "has one page of problems.")
        pairs[target] = page
    return pairs


def mixed_practice(
    tutorials: list[Tutorial], registry: dict[str, Tutorial]
) -> dict[str, list[Tutorial]]:
    """Problem sets that draw on several tutorials, per course, in title order.

    Checked the same way as `practice_for`: every id it names has to exist and
    be a tutorial rather than another page of problems. A set naming one
    tutorial is an error rather than an eccentricity — that is what
    `practice_for` is, and having two ways to say it would mean a tutorial
    could quietly acquire a second companion page.

    Which course lists a set is the course file's business, under `mixed:`
    (place_tutorials() reads that). A set no course file mentions goes with
    the default course of the first tutorial it names, so that writing one
    needs no more than the page itself.
    """
    out: dict[str, list[Tutorial]] = {}
    for page in tutorials:
        across = page.practice_across
        if not across:
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
            owner = registry.get(slug)
            if owner is None:
                fail(page.path, f"has practice_across naming {slug}, and there "
                                f"is no folder tutorials/{slug}/.")
            if owner.is_practice:
                fail(page.path, f"has practice_across naming {slug}, which is "
                                "itself a page of problems.")
        if not page.placements:
            first = registry[across[0]]
            if first.course:
                page.placements = [Placement(first.course, "", 0)]
        if not page.is_default:
            continue
        for course in page.courses:
            out.setdefault(course, []).append(page)
    for members in out.values():
        members.sort(key=lambda t: t.title)
    return out


def archived_of(tutorials: list[Tutorial]) -> dict[str, list[Tutorial]]:
    """Retired tutorials, per course, in title order.

    Kept apart from the series rather than filtered out of it, because they are
    still built and still reachable — a student who saved work in one can still
    get to it. They simply are not part of the course any more: a course file
    may still list one, and it lands here rather than on the route.
    """
    out: dict[str, list[Tutorial]] = {}
    for tutorial in tutorials:
        if not (tutorial.archived and tutorial.is_default):
            continue
        for course in tutorial.courses:
            out.setdefault(course, []).append(tutorial)
    for members in out.values():
        members.sort(key=lambda t: t.title)
    return out


def series_of(tutorials: list[Tutorial]) -> dict[tuple[str, str], list[Tutorial]]:
    """Group the live tutorials into the series a student works through,
    keyed by (course, series key), each in the course file's order.

    A series is per course: two courses may both have a series called
    "Fundamentals" without being the same sequence — and one tutorial may
    be in both, since a placement is a line in a course file rather than
    anything the tutorial owns.

    Only the current, live version of each tutorial is on a route. A
    superseded release is still readable; an archived tutorial is still
    built; a practice page hangs off its tutorial. None of them is here.
    """
    groups: dict[tuple[str, str], list[Tutorial]] = {}
    for tutorial in tutorials:
        if tutorial.status != "live" or not tutorial.is_default or tutorial.is_practice:
            continue
        for placement in tutorial.placements:
            groups.setdefault((placement.course, placement.series), []).append(tutorial)
    for (course, series), members in groups.items():
        def position(member: Tutorial) -> int:
            for placement in member.placements:
                if placement.course == course and placement.series == series:
                    return placement.position
            return 0
        members.sort(key=position)
    return groups


def courses_present(
    groups: dict[tuple[str, str], list[Tutorial]],
    *more: dict[str, list[Tutorial]],
) -> list[str]:
    """Every course with something to show, in courses/index.yaml order."""
    everywhere = {course for course, _ in groups}
    for mapping in more:
        everywhere |= set(mapping)
    return [course for course in courses() if course in everywhere]


def link_between(here: Tutorial, there: Tutorial) -> str:
    """Works out the relative link (`../other-tutorial.html`, not an
    absolute one like `/module/other-tutorial.html`) from one built page
    to another. Relative links are what let the whole site, and every
    tutorial's own downloadable standalone copy, work the same way
    whether it's opened from a real web server or straight off disk.
    `os.path.relpath` is the standard-library function that does the
    actual "how do I get from this folder to that file" math.
    """
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
        return f'<a class="dl-nav-up" href="{up}all-tutorials.html">All tutorials</a>'
    if index > 0:
        previous = members[index - 1]
        parts.append(
            f'<a class="dl-nav-prev" href="{link_between(tutorial, previous)}">'
            f"{html.escape(previous.title)}</a>"
        )
    up = "../" * tutorial.depth
    parts.append(f'<a class="dl-nav-up" href="{up}all-tutorials.html">All tutorials</a>')
    if index < len(members) - 1:
        following = members[index + 1]
        parts.append(
            f'<a class="dl-nav-next" href="{link_between(tutorial, following)}">'
            f"{html.escape(following.title)}</a>"
        )
    return "".join(parts)


def contents_items_html(tutorial: Tutorial) -> tuple[str, int]:
    """This page's own sections, as the list behind the tree's own-page rung
    (crumb_trail_html()) — what the in-page "Contents" list used to be
    before the tree absorbed it, so a reader finds every level of "where am
    I" in one place, down to the section. Returns the list markup and how
    many sections it holds.

    Sub-headings nest under the section they belong to rather than sitting
    in one flat list, because the flat version of an eight-section tutorial
    with "Your turn" under half of them is unreadable — and a sub-heading
    that repeats ("Your turn" five times) is left out, since five entries
    reading the same is a list nobody can choose from. Empty for a page
    with fewer than two sections: a contents list for a single heading is
    furniture.
    """
    def at_level(entries: list, level: int) -> list:
        # The `toc` extension hangs everything under the page's single `#`
        # heading, so sections are grandchildren rather than children;
        # searching by level rather than depth means a tutorial's heading
        # shape cannot break this.
        found = []
        for entry in entries:
            if entry.get("level") == level:
                found.append(entry)
            else:
                found.extend(at_level(entry.get("children") or [], level))
        return found

    sections = at_level(tutorial.toc, 2)
    if len(sections) < 2:
        return "", 0
    names = [str(s.get("name", "")) for s in at_level(tutorial.toc, 3)]
    ambiguous = {name for name in names if names.count(name) > 1}

    def item(entry: dict) -> str:
        text = html.escape(str(entry.get("name", "")))
        href = html.escape(str(entry["id"]), quote=True)
        children = [
            child for child in entry.get("children") or []
            if child.get("level") == 3 and str(child.get("name", "")) not in ambiguous
        ]
        nested = ""
        if children:
            nested = '<div role="list">' + "".join(
                f'<div role="listitem"><a href="#{html.escape(str(c["id"]), quote=True)}">'
                f'{html.escape(str(c.get("name", "")))}</a></div>'
                for c in children
            ) + "</div>"
        return f'<div role="listitem"><a href="#{href}">{text}</a>{nested}</div>'

    return "".join(item(s) for s in sections), len(sections)


def crumb_trail_html(
    tutorial: Tutorial,
    groups: dict[tuple[str, str], list[Tutorial]],
    members: list[Tutorial],
    up: str,
    practice: Tutorial | None = None,
    registry: dict[str, Tutorial] | None = None,
    also: list[Tutorial] | None = None,
) -> str:
    """Where this page sits — all tutorials, then this tutorial's own
    course, then its series, then the page itself, opening onto its own
    sections — as stacked, independently collapsible levels rather than
    one line of plain text. Each level is a native `<details>`, the same
    reasoning `nav_search_html()` already gives for its own popover: the
    caret and the expand/collapse behaviour need no JavaScript at all.

    `groups` is `series_of(tutorials)` — already keyed by (course, series)
    with everything this needs already grouped — so a sibling list at any
    level is just filtering or indexing into it, not a second pass over
    the site. `practice`, `registry` and `also` are what `write()` already
    holds for `practice_link()`: a tutorial's own page of problems (listed
    at the end of its own rung, since the problems are part of it), and
    the way back from a page of problems to the tutorial it belongs to
    (in whose series rung this page then sits, one level under it).

    The course and series rungs are the default course's — the first that
    lists this page. A page on more than one course says so on the nav
    (`data-courses`), and the runtime redraws these two rungs for the
    course the reader is following (tutorial-runtime.js, drawCourseChrome).
    A page no course lists has only the first rung and its own.
    """
    if tutorial.is_practice and tutorial.practice_for and registry:
        owner = registry.get(tutorial.practice_for)
        if owner is not None:
            members = groups.get((owner.course, owner.series), members)
    else:
        owner = None
    catalog = courses()
    course = catalog.get(tutorial.course)

    # Plain divs with list/listitem roles, not <ul>/<li> — the same choice
    # report_doors_links() already made and explains why: this markup
    # reaches every tutorial page, and a real <li> here silently inflates
    # any test elsewhere that counts a page's own list items.
    courses_items = "".join(
        f'<div role="listitem"><a href="{up}{html.escape(c, quote=True)}.html">'
        f"{html.escape(catalog[c].title)}</a></div>"
        for c in courses_present(groups)
    )

    series_items = ""
    if course is not None:
        series_items = "".join(
            f'<div role="listitem"><a href="{link_between(tutorial, groups[(course.id, key)][0])}">'
            f"{html.escape(course.series_title(key))}</a></div>"
            for key in course.keys if (course.id, key) in groups
        )

    # The page's own line in the series list is the rung that opens onto its
    # sections and its practice — the title itself carries the caret, so
    # the name is not printed twice (once bold in the list, once as a rung
    # of its own beneath). It starts closed: a reader arriving at a
    # tutorial should meet the tutorial, not a list of its parts. A page
    # with nothing behind its own name — too few sections for a contents
    # list (contents_items_html()), no practice — gets a plain bold line
    # rather than a caret with nothing behind it.
    contents, count = contents_items_html(tutorial)
    # A practice page's own title already says what it is ("First Steps —
    # Practice", "Mixed Problems — Programming"), so the line is the title
    # and nothing more; the colour marks it as a different kind of page.
    extra = [
        f'<div role="listitem" class="dl-crumb-practice">'
        f'<a href="{link_between(tutorial, problems)}">{html.escape(problems.title)}</a></div>'
        for problems in ([practice] if practice is not None else []) + list(also or [])
    ]
    own = html.escape(tutorial.title)
    if contents or extra:
        count_html = f'<span class="dl-crumb-count">{count} sections</span>' if count else ""
        own_rung = (
            '<div role="listitem">'
            '<details class="dl-crumb-level dl-crumb-level-4">'
            f'<summary aria-current="page">{own}{count_html}</summary>'
            f'<div role="list">{contents}{"".join(extra)}</div>'
            "</details></div>"
        )
    else:
        own_rung = (
            '<div class="dl-crumb-current dl-crumb-level-4" role="listitem" '
            f'aria-current="page">{own}</div>'
        )

    # An archived tutorial or a practice page has no reading-order position
    # (nav_for() uses the same honest shape for that case) — members will
    # not include it, so it gets a list of just itself rather than an empty
    # series level with no current page marked at all.
    here = owner or tutorial
    tutorial_items = []
    for member in (members if here in members else [tutorial]):
        title = html.escape(member.title)
        link = f'<a href="{link_between(tutorial, member)}">{title}</a>'
        if member is tutorial:
            tutorial_items.append(own_rung)
        elif member is owner:
            # A page of problems belongs to its tutorial, so it sits one
            # level under it — the tutorial stays a plain link back to
            # itself, and the page of problems is the bold line beneath.
            tutorial_items.append(
                f'<div role="listitem">{link}<div role="list">{own_rung}</div></div>'
            )
        else:
            tutorial_items.append(f'<div role="listitem">{link}</div>')

    # Only the series level opens by default, showing exactly where this
    # page sits. All tutorials and the course start collapsed: every level
    # open at once made the tree tall enough to push the stack below it off
    # the bottom of a shorter screen.
    on_courses = html.escape(" ".join(tutorial.courses), quote=True)
    levels = [
        '<details class="dl-crumb-level">'
        "<summary>All tutorials</summary>"
        f'<div role="list">{courses_items}</div>'
        "</details>"
    ]
    if course is not None:
        levels.append(
            '<details class="dl-crumb-level dl-crumb-level-2">'
            f"<summary>{html.escape(course.title)}</summary>"
            f'<div role="list">{series_items}</div>'
            "</details>"
        )
    if course is not None and tutorial.series:
        levels.append(
            '<details class="dl-crumb-level dl-crumb-level-3" open>'
            f"<summary>{html.escape(course.series_title(tutorial.series))}</summary>"
            f'<div role="list">{"".join(tutorial_items)}</div>'
            "</details>"
        )
    else:
        # No series to open onto: the page's own rung stands on its own.
        levels.append(f'<div role="list">{"".join(tutorial_items)}</div>')
    return (
        f'<nav class="dl-crumbtrail" aria-label="Where this page sits" data-courses="{on_courses}">'
        + "".join(levels)
        + "</nav>"
    )


GLOSSARY_KINDS = ("concept", "function", "operator", "formula", "keyword")


def glossary_path(tutorial: Tutorial) -> Path:
    """Where a tutorial's own glossary file lives — beside the tutorial's own
    markdown, in the tutorial's folder.

    Derived from the source file's own location rather than rebuilt from
    the id, which is what makes it right for every version of a
    tutorial at once: each release sits in the same folder, so each finds the
    one glossary. What a tutorial teaches does not change release to release
    the way its prose might, and one file per tutorial is what says so.
    """
    return tutorial.path.parent / f"{tutorial.slug}.glossary.yaml"


def own_glossary(tutorial: Tutorial) -> list[dict]:
    """This tutorial's own contribution — what it introduces, not what it
    inherits from earlier in its series. A missing file means none written
    yet, not an error: that is what lets this feature ship before every
    tutorial has one."""
    path = glossary_path(tutorial)
    if not path.is_file():
        return []
    data = read_yaml(path) or {}
    entries = data.get("entries") or []
    for entry in entries:
        if entry.get("kind") not in GLOSSARY_KINDS:
            fail(path, f'glossary entry "{entry.get("term")}" has kind '
                       f'{entry.get("kind")!r}, not one of {GLOSSARY_KINDS}.')
        if not entry.get("term") or not entry.get("definition"):
            fail(path, "a glossary entry is missing a term or a definition.")
    return entries


def series_chain(
    course: str, series: str, groups: dict[tuple[str, str], list[Tutorial]]
) -> list[Tutorial]:
    """Every tutorial one series' reference accumulates from: every earlier
    series of the course, in the course file's order, followed by this
    series' own members in theirs. A reference accumulates through the
    course the reader is following, and a series the course file leaves
    unlisted is simply not on that course — so "Reflections and review",
    listed last, inherits everything before it, and a reader reaches it
    whenever they like.
    """
    found = courses().get(course)
    if found is None:
        return groups.get((course, series), [])
    chain: list[Tutorial] = []
    for key in found.keys:
        chain.extend(groups.get((course, key), []))
        if key == series:
            break
    return chain


def cumulative_glossary(
    tutorial: Tutorial,
    registry: dict[str, Tutorial],
    groups: dict[tuple[str, str], list[Tutorial]],
    reader_at: Tutorial | None = None,
) -> list[dict]:
    """Everything a reader has met by this point: this tutorial's own
    glossary, everything earlier in its own series, and everything from
    each earlier series of its course (`series_chain()`). Whichever entry came first wins
    on a term repeated later, so a definition never contradicts an earlier
    one on the same page.

    A practice page has no series position that means anything —
    `practice_for`/`practice_across` name what it tests instead of where it
    sits — so its reference is the union of the tutorial(s) it names, each
    resolved the same way, rather than its own (nonexistent) coverage.
    """
    reader_at = reader_at or tutorial

    if tutorial.is_practice:
        targets = (
            [tutorial.practice_for] if tutorial.practice_for
            else list(tutorial.practice_across)
        )
        seen: set[tuple[str, str]] = set()
        found: list[dict] = []
        for slug in targets:
            target = registry.get(slug)
            if target is None:
                continue
            for entry in cumulative_glossary(target, registry, groups, reader_at):
                key = (entry["term"], entry["kind"])
                if key in seen:
                    continue
                seen.add(key)
                found.append(entry)
        return found

    chain = series_chain(tutorial.course, tutorial.series, groups)
    if tutorial not in chain:
        # Archived, same as nav_for()'s own "nowhere in the series it comes
        # before or after" — only its own entries, nothing inherited.
        return own_glossary(tutorial)

    seen = set()
    found = []
    for member in chain[: chain.index(tutorial) + 1]:
        for entry in own_glossary(member):
            key = (entry["term"], entry["kind"])
            if key in seen:
                continue
            seen.add(key)
            found.append(entry if member is reader_at
                         else {**entry, "origin": origin_of(reader_at, member, entry["term"])})
    return found


def origin_of(reader_at: Tutorial, introduced_by: Tutorial, term: str) -> dict:
    """The tutorial a term was introduced in, as something the reference panel
    can render: a title to name it and an href to reach it from the page the
    reader is on."""
    href = os.path.relpath(introduced_by.out_path, reader_at.out_path.parent)
    anchor = origin_anchor(introduced_by, term)
    return {
        "title": introduced_by.title,
        "href": f"{href}#{anchor}" if anchor else href,
    }


MATH_BASICS_DATA = ROOT / "planning" / "curriculum" / "math-basics.yaml"
PYTHON_BASICS_DATA = ROOT / "planning" / "curriculum" / "python-basics.yaml"


def _load_basics(path: Path, kind: str) -> list[dict]:
    """Shared loader for the Reference panel's own site-wide "Basics"
    tabs (Math Basics, Python Basics) — same shape, same validation,
    only the file and its own house rule differ; see load_math_basics()
    and load_python_basics() for what each promises its own content
    follows. Returns `[]`, not an error, when the file does not exist
    yet: the same "not written yet" tolerance `own_glossary()` gives a
    missing per-tutorial glossary.
    """
    if not path.is_file():
        return []
    data = read_yaml(path) or {}
    groups = data.get("groups") or []
    for group in groups:
        if not group.get("label"):
            fail(path, f"a {kind} group is missing a label.")
        entries = group.get("entries") or []
        if not entries:
            fail(path, f'the group {group.get("label")!r} has no entries.')
        for entry in entries:
            if not entry.get("term") or not entry.get("definition"):
                fail(path, f"a {kind} entry is missing a term or a definition.")
    return groups


def load_math_basics() -> list[dict]:
    """Math Basics: plain definitions for arithmetic notation and
    vocabulary, independent of any one tutorial or series — see
    planning/curriculum/math-basics.yaml for the house rule this file is
    written to (one sentence, no worked example, no leaning on another
    entry). Unlike a tutorial's own accumulated glossary, this is the
    same list on every page — re-read on every one of write()'s calls
    rather than cached, the same choice cumulative_glossary() already
    makes for the (much larger) per-tutorial glossary files it re-reads
    per page; a ~100-line YAML file is not worth memoizing against, and
    not caching it keeps this trivially safe to monkeypatch in tests.
    """
    return _load_basics(MATH_BASICS_DATA, "math-basics")


def load_python_basics() -> list[dict]:
    """Python Basics: plain definitions for Python's own vocabulary and
    punctuation — values, variables, functions and arguments, and the
    marks that give Python code its shape — independent of any one
    tutorial or series, the same way load_math_basics() is. See
    planning/curriculum/python-basics.yaml for the house rule this file
    is written to; unlike math-basics.yaml, an entry here may carry a
    short `example`, since Python's own syntax marks are often clearer
    shown than said.
    """
    return _load_basics(PYTHON_BASICS_DATA, "python-basics")


def download_link_html(href: str, label: str) -> str:
    """A `.dl-download` link/button, icon and all — the one shape every
    "take this away" offer uses, whether it's a single tutorial's own copy,
    a series' archive, or a whole module's. The icon is a plain empty span
    (a shape drawn in CSS, the same way .dl-settings-icon and its siblings
    already are — no font, no inline SVG to keep in step with a palette
    change) marked aria-hidden, so a screen reader reads only `label`, not
    an icon or the glyph CSS content: used to put there before it.
    """
    icon = '<span class="dl-download-icon" aria-hidden="true"></span>'
    return f'<a class="dl-download" href="{href}" download>{icon}{label}</a>'


def download_section(tutorial: Tutorial) -> str:
    """The settings panel's offer to take this tutorial away.

    Written here rather than in the shell because only build.py knows where a
    tutorial's downloadable copy ended up, and because the contents page — which
    shares the shell — has no single tutorial to offer.
    """
    up = "../" * tutorial.depth
    href = f"{up}download/{tutorial.slug}.html"
    return (
        "<h3>This tutorial</h3>"
        f"{download_link_html(href, 'Download to keep')}"
        '<p class="dl-panel-note">One file with the reading and the cells inside '
        "it. It needs an internet connection the first time you open it, and "
        "then it is yours.</p>"
    )


TOPIC_DATA = ROOT / "planning" / "curriculum" / "topics.yaml"
SCOPE_DATA = ROOT / "planning" / "curriculum" / "out-of-scope.yaml"
TOPIC_GROUPS_DATA = ROOT / "planning" / "curriculum" / "topic-groups.yaml"

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
    return (load_yaml_no_duplicate_keys(TOPIC_DATA.read_text()) or {}).get("topics") or {}


def load_topic_groups() -> list[dict]:
    """Broader, cross-module groupings for the "browse by topic" page
    (`write_topics_page()`) — see `planning/curriculum/topic-groups.yaml`'s
    own header comment for what these are and why they're a separate file
    from `topics.yaml` above. Optional, the same way the topic tree's own
    data is: without the file, there's simply no topics page."""
    if not TOPIC_GROUPS_DATA.is_file():
        return []
    data = load_yaml_no_duplicate_keys(TOPIC_GROUPS_DATA.read_text()) or {}
    return data.get("groups") or []


def load_out_of_scope() -> set[str]:
    """Outcomes we have decided not to teach. Shown, and shown as decided."""
    if not SCOPE_DATA.is_file():
        return set()
    data = load_yaml_no_duplicate_keys(SCOPE_DATA.read_text()) or {}
    return {entry["code"] for entry in data.get("outcomes") or []}


def taught_where(tutorials: list[Tutorial]) -> dict[str, dict]:
    """Outcome code to the tutorial section that teaches it.

    Read from each tutorial's own `covers:` frontmatter, so a topic's link
    cannot point somewhere the tutorial does not claim.
    """
    where: dict[str, dict] = {}
    for tutorial in tutorials:
        if tutorial.archived or tutorial.status != "live" or not tutorial.is_default:
            continue
        for anchor, claim in (tutorial.meta.get("covers") or {}).items():
            for code in claim.get("covers") or []:
                where.setdefault(code, {
                    "title": tutorial.title,
                    "href": f"tutorials/{tutorial.slug}.html#{anchor}",
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


def outcome_of(topics: dict, code: str) -> str:
    """Which learning outcome a topic serves, for looking it up in anything
    keyed by outcome — coverage, strands, the out-of-scope list.

    A topic code and an outcome code were once the same string. They are not
    any more: several topics may serve one outcome where the descriptor bundles
    ideas a student meets weeks apart, and one topic may serve several where it
    folds in what a thin neighbouring outcome asked for. Where a topic serves
    several, the first is the one the tree colours and links by. Falling back
    to the topic's own code keeps `PRE-` groundwork, which serves none, working
    as it did.
    """
    claimed = (topics.get(code) or {}).get("outcome")
    if not claimed:
        return code
    return claimed if isinstance(claimed, str) else claimed[0]


def topic_layout(topics: dict, strands: dict[str, str]) -> tuple[dict, float, float]:
    """Where every topic sits: one row per tier, reading downwards.

    `strands` is keyed by topic code, already resolved by the caller.

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
            rows[level],
            key=lambda c: (strands.get(c, "other"), topics[c]["name"]),
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
    by_outcome = load_strands()
    strands = {
        code: str(topic["strand"]) if topic.get("strand")
        else by_outcome.get(outcome_of(topics, code), "other")
        for code, topic in topics.items()
    }
    excluded = load_out_of_scope()
    taught = taught_where(tutorials)
    place, width, height = topic_layout(topics, strands)

    nodes = []
    for code, topic in sorted(topics.items()):
        at = place[code]
        where = taught.get(outcome_of(topics, code))
        if code.startswith("PRE-"):
            state = "groundwork"
        elif outcome_of(topics, code) in excluded:
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
    data = load_yaml_no_duplicate_keys(OUTCOME_DATA.read_text()) or {}
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


def progress_attrs(tutorial: Tutorial) -> str:
    """`data-id`/`data-cells` for a contents-page link, so
    tutorial-runtime.js's progress indicator can read a reader's
    saved-progress record for it with no fetch. A prose-only tutorial has
    nothing to show progress for, so it gets no attribute at all rather
    than a "0/0"."""
    if not tutorial.cells:
        return ""
    return (
        f' data-id="{html.escape(tutorial.slug, quote=True)}"'
        f' data-cells="{len(tutorial.cells)}"'
    )


def render_search_box(placeholder: str, big: bool = False, id_prefix: str = "dl-search",
                      hint: bool = True) -> str:
    """The search box markup shared by every page that carries one — the
    front page, "All tutorials", "Browse by topic", and (via
    `nav_search_html()`) the small search popover next to "All
    tutorials" in every page's own top nav. Identical shape everywhere,
    so `assets/search.js` (loaded on every page, a no-op wherever it
    finds no `.dl-search` at all) only ever has to know one shape to
    wire up — it finds every instance by class and reads each one's own
    children by class too, not by id, so `id_prefix` only has to keep
    two instances on the same page (a page's own body search plus the
    nav popover, on the handful of pages that carry both) from sharing
    one id — it plays no part in the wiring itself.
    `big` adds a modifier class for the front page's own copy, the one
    place this is the primary way in rather than a convenience partway
    down a long list. `hint=False` leaves out the line under the field
    saying what a search matches — the front page's own sentence above
    its box already says it (7.175).
    """
    classes = "dl-search dl-search-big" if big else "dl-search"
    input_id = f"{id_prefix}-input"
    hint_id = f"{id_prefix}-hint"
    results_id = f"{id_prefix}-results"
    described = f' aria-describedby="{hint_id}"' if hint else ""
    note = (
        f'<p class="dl-panel-note" id="{hint_id}">Matches titles and the '
        "terms each tutorial actually teaches — close counts too "
        '("loop" also finds "iteration").</p>'
    ) if hint else ""
    return (
        f'<div class="{classes}" id="{id_prefix}">'
        f'<label for="{input_id}" class="dl-search-label">Search tutorials</label>'
        f'<input type="search" id="{input_id}" class="dl-search-input" '
        f'placeholder="{html.escape(placeholder, quote=True)}" autocomplete="off"{described}>'
        f"{note}"
        f'<ul class="dl-search-results" id="{results_id}" hidden></ul>'
        "</div>"
    )


def nav_search_html() -> str:
    """The search line under the wordmark in every page's top-left dock
    (shell.html's `{{NAV_SEARCH}}`): a magnifier and the words "Search
    for a topic", set like the tree's lines beneath it. The line *is* the
    field — `render_search_box()`'s own input, the same widget the front
    page carries, so `assets/search.js` wires it the way it wires every
    other one, drawn with no border or background and those words as its
    placeholder. A click on the words or the magnifier puts the cursor in
    front of them; typing replaces them; the results drop beneath. There
    is no second bar to open, on any width (7.169 — Josh: "a tap or click
    on the icon or text puts a cursor in front of the text and then as
    the user types the text goes away and the results just appear
    below"). The magnifier sits over the input's left padding and lets
    clicks through to it.
    """
    return (
        '<div class="dl-nav-search">'
        '<svg class="dl-nav-search-icon" viewBox="0 0 20 20" aria-hidden="true" focusable="false">'
        '<circle cx="8.5" cy="8.5" r="6" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<line x1="13.3" y1="13.3" x2="18" y2="18" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round"/>'
        "</svg>"
        + render_search_box("Search for a topic", id_prefix="dl-nav-search")
        + "</div>"
    )


def render_tutorials_list(
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path] | None = None,
    retired: dict[str, list[Tutorial]] | None = None,
    practice: dict[str, Tutorial] | None = None,
    mixed: dict[str, list[Tutorial]] | None = None,
    course_archives: dict[str, Path] | None = None,
) -> str:
    """"All tutorials": every course, every series, in order — the whole
    site on one page, for a reader who wants to browse rather than
    search. Its own page (`write_all_tutorials_page()`) rather than part
    of the front page, so a first-time visitor meets the front page's own
    pitch first and this only when they choose "All tutorials" or come
    looking for something the search box on the front page didn't find.

    `archives` maps a series to its zip of downloadable copies, when the build
    wrote them. Without it the page simply carries no whole-series link, which
    is what a quick local build wants. `course_archives` is the same idea one
    level up: a course's every series and every practice page, combined.
    """
    archives = archives or {}
    retired = retired or {}
    practice = practice or {}
    mixed = mixed or {}
    course_archives = course_archives or {}
    if not groups:
        return "<p>No tutorials have been written yet.</p>"

    out = [
        "<h1>All tutorials</h1>",
        '<div class="dl-search-sticky">' + render_search_box(
            "Search by topic — e.g. loops, probability, sorting…") + "</div>",
        '<div class="dl-intro">',
        "<p>Everything runs in your browser, so there is nothing to "
        "install and no account to make. Open any tutorial and start.</p>",
        '<ul class="dl-intro-points">',
        "<li><strong>Tutorials are made of cells.</strong> A cell is a small "
        "box of Python set into the reading. We can change what is in it and "
        "run it. The result appears just underneath.</li>",
        "<li><strong>First we explore, then we name what we found.</strong> A "
        "tutorial usually opens with a problem or an idea to try out. Then we "
        "look at the general idea behind it. Then we learn the name "
        "people give it, so that we can talk to other people about the same "
        "idea.</li>",
        "<li><strong>We are not trying to hide the right answer.</strong> Most "
        "tutorials have a practice page beside them. The answer usually sits "
        "right below each problem. What we are learning is the steps that get "
        "us there. If you get stuck, you can open a hint, try a different "
        "approach, or read the answer and try the problem again.</li>",
        "<li><strong>Getting something wrong costs nothing.</strong> An error "
        "message is usually telling us something useful. Nothing here is "
        "scored. A wrong answer is information about a method, not a mark "
        "against you.</li>",
        "<li><strong>Your work is saved in this browser as you go.</strong> "
        "It stays on this device. You can also download any tutorial as a "
        "single file and keep it.</li>",
        "<li><strong>The list below is grouped into modules, and each module "
        "into series.</strong> A series is meant to be read in order, from the "
        'top. If you are not sure where to start, the <a href="tree.html">topic '
        "tree</a> shows what the course covers and what usually comes first. "
        '<a href="topics.html">Browse by topic</a> gathers one subject — '
        "trigonometry, say — in one place.</li>",
        "</ul>",
        '<p class="dl-intro-tree">This project is open and still growing. '
        '<a href="about.html">About this project</a> explains how to suggest a '
        "change or report a mistake.</p>",
        "</div>",
    ]

    catalog = courses()
    for course in courses_present(groups, retired, mixed):
        out.extend(render_course_body(
            catalog[course], groups, archives, retired, practice, mixed, course_archives,
        ))
    return "\n".join(out)


def render_course_body(
    course: Course,
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path],
    retired: dict[str, list[Tutorial]],
    practice: dict[str, Tutorial],
    mixed: dict[str, list[Tutorial]],
    course_archives: dict[str, Path],
    heading: bool = True,
) -> list[str]:
    """One course's own content: its heading, its whole-course download
    offer, every series in it (each with its own download offer and its
    tutorial/practice list), its mixed problems and its archive.

    Shared by `render_tutorials_list()`, where every course appears one after
    another on the all-tutorials page, and `write_course_page()`, where a
    course gets a page of its own — `heading=False` there, since the page's
    own `<h1>` already names it and repeating it as an `<h2>` right
    underneath would say the same thing twice.
    """
    out: list[str] = []
    if heading:
        out.append(f'<h2 class="dl-module-heading">{html.escape(course.title)}</h2>')
    course_archive = course_archives.get(course.id)
    if course_archive is not None:
        total = sum(
            len(zip_sequence(members, practice))
            for (owner, _), members in groups.items() if owner == course.id
        ) + len(mixed.get(course.id, []))
        out.append(
            '<p class="dl-series">' + download_link_html(
                f"download/{course_archive.name}",
                f"Download every tutorial and practice page in this module "
                f"({total} files, {readable_size(course_archive)})",
            ) + "</p>"
        )
    present = [key for key in course.keys if (course.id, key) in groups]
    for key in present:
        members = groups[(course.id, key)]
        if len(present) > 1:
            out.append(f'<h3>{html.escape(course.series_title(key))}</h3>')
        archive = archives.get((course.id, key))
        if archive is not None:
            sequence = zip_sequence(members, practice)
            count = len(sequence)
            what = ("this one as a single file" if count == 1
                    else f"all {count} as single files")
            out.append(
                '<p class="dl-series">' + download_link_html(
                    f"download/{archive.name}",
                    f"Download {what} ({readable_size(archive)})",
                ) + "</p>"
            )
        out.append('<ol class="dl-contents">')
        for member in members:
            href = member.out_path.relative_to(OUT).as_posix()
            also = practice.get(member.slug)
            extra = ""
            if also is not None:
                where = also.out_path.relative_to(OUT).as_posix()
                extra = (f' <a class="dl-contents-practice" href="{where}">'
                         "Practice</a>")
            out.append(
                f'<li><a class="dl-contents-btn" href="{href}"{progress_attrs(member)}>'
                f'<span class="dl-contents-kicker">Explore</span>'
                f"{html.escape(member.title)}</a>{extra}</li>"
            )
        out.append("</ol>")
    for member in mixed.get(course.id, []):
        if member is mixed[course.id][0]:
            out.append('<h3 class="dl-mixed-head">Mixed problems</h3>')
            out.append(
                '<p class="dl-mixed-note">Problems that draw on several '
                "tutorials at once. Try them once you have finished the "
                "tutorials they name.</p>"
            )
            out.append('<ul class="dl-contents dl-mixed">')
        href = member.out_path.relative_to(OUT).as_posix()
        out.append(
            f'<li><a href="{href}"{progress_attrs(member)}>'
            f"{html.escape(member.title)}</a></li>"
        )
        if member is mixed[course.id][-1]:
            out.append("</ul>")

    # Last, and marked, because it is not part of the course any more — but
    # present, because a student who worked in one has to be able to find it.
    for member in retired.get(course.id, []):
        if member is retired[course.id][0]:
            out.append('<h3 class="dl-archive-head">Archive</h3>')
            out.append(
                '<p class="dl-archive-note">No longer part of the course. '
                "Kept here so that saved work can still be found and old "
                "links still work.</p>"
            )
            out.append('<ul class="dl-contents dl-archive">')
        href = member.out_path.relative_to(OUT).as_posix()
        out.append(f'<li><a href="{href}">{html.escape(member.title)}</a></li>')
        if member is retired[course.id][-1]:
            out.append("</ul>")
    return out


def check_alt_text(tutorial: Tutorial) -> None:
    """Every image declares alt. An explicit alt="" marks a decorative one.

    Notes are checked too, even though they no longer live in body_html by
    this point (extract_notes() already pulled them out) — an image inside
    one is exactly as real as an inline one.
    """
    sources = [tutorial.body_html] + [note.html for note in tutorial.notes]
    for source in sources:
        for tag in IMG_RE.findall(source):
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


DATASET_ATTRIBUTION_FIELDS = ("source", "license", "description")
DATASET_EXTENSIONS = (".csv", ".txt")


def dataset_attribution(tutorial: Tutorial, name: str) -> dict:
    """A declared dataset's own attribution file —
    `data/<name>.yaml` beside `data/<name>.csv` (loaded with `load_csv()`)
    or `data/<name>.txt` (loaded with `load_text()`), the same
    beside-the-file pattern `<slug>.glossary.yaml` already established.
    Both files are required: an
    undocumented dataset defeats the point of declaring one at all, so a
    missing data file or a missing/incomplete attribution file fails the
    build the same way a `practice_for` naming no real tutorial does,
    rather than silently shipping a dataset nobody can trace.
    """
    has_data_file = any((DATA / f"{name}{ext}").is_file() for ext in DATASET_EXTENSIONS)
    if not has_data_file:
        extensions = " or ".join(f"data/{name}{ext}" for ext in DATASET_EXTENSIONS)
        fail(tutorial.path, f"declares datasets: {name}, and neither "
                            f"{extensions} exists.")
    yaml_path = DATA / f"{name}.yaml"
    if not yaml_path.is_file():
        fail(tutorial.path, f"declares datasets: {name}, and data/{name}.yaml "
                            "(its source, license, and description) does not exist.")
    data = load_yaml_no_duplicate_keys(yaml_path.read_text()) or {}
    missing = [f for f in DATASET_ATTRIBUTION_FIELDS if not data.get(f)]
    if missing:
        fail(yaml_path, f"is missing {', '.join(missing)}")
    return {"name": name, **{f: str(data[f]) for f in DATASET_ATTRIBUTION_FIELDS}}


def check_datasets(tutorial: Tutorial) -> list[dict]:
    """Every dataset this tutorial declares, with its attribution — checked
    and resolved together, since there is no use in resolving one without
    the other. Returns [] for a tutorial that declares none."""
    return [dataset_attribution(tutorial, name) for name in tutorial.datasets]


def resolve_links(tutorial: Tutorial, registry: dict[str, Tutorial]) -> str:
    """Rewrite tutorial:id#anchor into a real relative href, or fail.

    An id is site-wide (id_of()), so a link names one page and nothing has
    to be guessed: `tutorial:first-steps` is the same tutorial from any
    course. A link to an id this build has no page for stops the build
    rather than shipping a page that looks finished to everyone except the
    student who follows it.
    """

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


BIBLIOGRAPHY_RE = re.compile(r"read more", re.I)

TAG_RE = re.compile(r"<[^>]+>")


def origin_anchor(tutorial: Tutorial, term: str) -> str:
    """The section of `tutorial` a reader should land on for `term`, or "".

    Prefers the term's emphasised first use, since
    PEDAGOGICAL_STYLE_GUIDE.md §4 asks an author to italicise exactly that,
    and falls back to its first plain occurrence — a term introduced through
    a code cell rather than a sentence may never be italicised at all, and
    landing on the right section still beats landing on the page.

    Searched per `h2` section, against each section's *text* rather than its
    markup, which matters for both halves of that: a raw search over the HTML
    matches inside an `href` or a class name, and the nearest preceding
    heading of any level is usually "Your turn", which every tutorial has
    several of and none of which tells a reader where they are.
    """
    body = tutorial.body_html
    headings = list(re.finditer(r'<h2[^>]*\sid="([^"]+)"[^>]*>(.*?)</h2>', body, re.S))
    if not headings:
        return ""

    sections = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        title = TAG_RE.sub("", heading.group(2))
        if BIBLIOGRAPHY_RE.search(title):
            continue
        sections.append((heading.group(1), body[heading.end():end]))

    emphasised = re.compile(rf"<em>{re.escape(term)}</em>", re.I)
    plain = re.compile(rf"\b{re.escape(term)}\b", re.I)

    # Two passes rather than one, so an emphasised use anywhere in the
    # tutorial beats a passing mention in an earlier section.
    for pattern, over_markup in ((emphasised, True), (plain, False)):
        for anchor, section in sections:
            haystack = section if over_markup else TAG_RE.sub(" ", section)
            if pattern.search(haystack):
                return anchor
    return ""


# The files a tutorial's folder holds that are the build's own business, not
# assets: the pages themselves and the glossary that describes them.
NON_ASSET_SUFFIXES = {".md", ".yaml", ".yml"}

# src="..." on any element — img, audio, video, source. Assets are referenced
# the same way whatever the medium, so one pattern covers all of them.
SRC_RE = re.compile(r'src="(?P<url>[^"]*)"')

# href="..." pointing at a downloadable sibling file — a small standalone
# .html a reader can open or take as a starting point, not a picture and not
# a link to another page. Deliberately permissive where SRC_RE is strict: by
# the time this runs, resolve_links() has already turned every authored
# `tutorial:slug` reference into a real relative href, and some of those
# come out as a bare filename with no slash too (two tutorials in the same
# module, `os.path.relpath()` finding no directories between them) — this
# has to leave those alone rather than mistake them for a local asset.
HREF_ASSET_RE = re.compile(r'href="(?P<url>[^"]*)"')

# A reference that points somewhere other than this tutorial's own folder:
# an absolute URL, a root-relative path, a data: URI, or a page anchor.
EXTERNAL_URL_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//|/|#)", re.I)

# A tutorial teaching HTML shows `<img src="...">` and `<a href="...">` as
# text to read, not markup to run — markdown's own code-span handling
# escapes `<`/`>` there but leaves a literal quote alone, so
# `src="picture.png"` inside a `<code>` (inline, or a fenced block's
# `<pre><code>`) still reads, to SRC_RE/HREF_ASSET_RE, exactly like a real
# attribute. Masking a `<code>`'s contents before those run, then putting
# them back unchanged, is what keeps a quick-reference table honest.
CODE_SPAN_RE = re.compile(r"<code[^>]*>.*?</code>", re.S)


def tutorial_assets(tutorial: Tutorial) -> list[Path]:
    """Every asset file sitting in this tutorial's folder.

    Read from the folder rather than declared in frontmatter: a picture a
    tutorial uses is already named in the markdown that shows it, and asking
    an author to list it a second time only creates a way for the two lists
    to disagree.
    """
    return sorted(
        path for path in tutorial.path.parent.iterdir()
        if path.is_file() and path.suffix.lower() not in NON_ASSET_SUFFIXES
    )


# `<img src="diagram.svg" alt="…">` — a local SVG shown on the page, which
# gets inlined rather than linked. See inline_local_svg().
IMG_SVG_RE = re.compile(
    r'<img\b(?P<attrs>[^>]*?)\bsrc="(?P<url>[^"]*\.svg)"(?P<rest>[^>]*)>',
    re.IGNORECASE)
ALT_VALUE_RE = re.compile(r'\balt\s*=\s*"(?P<alt>[^"]*)"', re.IGNORECASE)
# Everything an SVG file may carry before its root element: the XML
# declaration, a DOCTYPE, and comments — draw.io writes all three, in that
# order, and a stripper that knew only the first two left the comment in
# front and quietly gave up on the file.
SVG_PROLOGUE_RE = re.compile(
    r"^\s*(?:<\?xml[^>]*\?>|<!DOCTYPE[^>]*>|<!--.*?-->)\s*", re.I | re.S)


def inline_local_svg(folder: Path, body: str, tutorial_path: Path) -> str:
    """Put a local SVG's own markup on the page, in place of linking to it.

    An `<img>`-loaded SVG is a separate document. The page's CSS custom
    properties do not reach inside it and `currentColor` has no inherited
    colour to resolve against, so a diagram drawn in `--dl-*` tokens renders
    black on black for any reader not in light mode — and the reader's own
    font choice, OpenDyslexic included, never reaches its labels either.
    Inlined, both work, and the same file is what a diagramming tool wrote.

    The contents page's map is already inline SVG for the same reason
    (`write_contents_page()`), so this extends a house pattern rather than
    inventing one.

    `alt` carries across rather than being dropped: alt text on an element
    that is no longer an image would mean nothing, so a described diagram
    becomes `role="img"` with an `aria-label`, and an explicit `alt=""` —
    the way this project marks a decorative image — becomes `aria-hidden`.
    `check_alt_text()` still runs against the `<img>` tags, before this.

    Raster images keep the `<img>` path: there is nothing inside a PNG for
    the page's stylesheet to reach.
    """

    def swap(match: re.Match) -> str:
        url = match.group("url")
        if EXTERNAL_URL_RE.match(url):
            return match.group(0)
        source = folder / url
        if not source.is_file():
            return match.group(0)          # src() reports it, with a better message
        attributes = match.group("attrs") + match.group("rest")
        described = ALT_VALUE_RE.search(attributes)
        label = html.escape(described.group("alt"), quote=True) if described else ""
        markup = source.read_text()
        while True:                       # xml declaration, doctype, comments
            trimmed = SVG_PROLOGUE_RE.sub("", markup, count=1)
            if trimmed == markup:
                break
            markup = trimmed
        markup = markup.strip()
        if not markup.startswith("<svg"):
            # Falling back to `<img>` here is what the whole change exists to
            # avoid, and it would do it in silence: the page builds, the
            # diagram renders black on black, and nothing says why. Better to
            # stop and name the file.
            fail(
                tutorial_path,
                f"{url!r} does not start with <svg> once its declaration, "
                "doctype and comments are stripped, so it cannot be inlined.",
            )
        opening = markup[: markup.index(">") + 1]
        # A fixed width would stop the figure fitting a narrow screen, and the
        # viewBox already carries the proportions.
        cleaned = re.sub(r'\s(?:width|height)="[^"]*"', "", opening)
        accessibility = (
            f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
        )
        cleaned = cleaned[:-1] + f' class="dl-diagram"{accessibility}>'
        return cleaned + markup[markup.index(">") + 1 :]

    return IMG_SVG_RE.sub(swap, body)


def resolve_assets(tutorial: Tutorial, body_html: str) -> str:
    """Point every `src="picture.png"` at the copy this build will write, and
    fail on one naming a file the tutorial's folder does not hold. Do the
    same for `href="worksheet.html"` — a downloadable sibling file linked
    rather than shown — except a name that matches nothing is left exactly
    as it is rather than failing the build: unlike an image, a page can link
    to plenty of things that are not a local asset at all, and by this point
    `resolve_links()` has already turned every `tutorial:slug` reference
    into a real relative href, some of them a bare filename too.

    An author writes the plain file name, the same one they see beside the
    markdown, and it resolves from whichever URL the page ends up at. That
    matters because the two are not the same shape: the current release is
    served at `tutorials/<id>.html`, one level *above* its own folder (a
    practice page, `tutorials/<id>-practice.html`, beside it), while a
    frozen release sits at `tutorials/<id>/v<version>.html`, inside it. So
    the reference a reader's browser needs differs by version, and neither
    is what the author typed.

    A missing file stops the build for the same reason a dead
    `tutorial:` link does: the alternative is a page that looks finished to
    everyone except the student who loads it.
    """
    folder = tutorial.path.parent
    # Where the page will sit, relative to the folder its assets are copied
    # into — the same relpath calculation resolve_links() uses for pages.
    prefix = "" if not tutorial.is_default else f"{tutorial.folder}/"

    def src(match: re.Match) -> str:
        url = match.group("url")
        if not url or EXTERNAL_URL_RE.match(url):
            return match.group(0)
        if not (folder / url).is_file():
            fail(
                tutorial.path,
                f"references {url!r}, which is not a file in this tutorial's "
                f"folder ({folder.relative_to(ROOT)}).",
            )
        return f'src="{prefix}{url}"'

    def href(match: re.Match) -> str:
        url = match.group("url")
        if not url or EXTERNAL_URL_RE.match(url) or "/" in url or not (folder / url).is_file():
            return match.group(0)
        return f'href="{prefix}{url}"'

    # Code spans are masked out before either substitution runs, and put
    # back untouched afterward — see CODE_SPAN_RE's own comment.
    code_spans: list[str] = []

    def stash(match: re.Match) -> str:
        code_spans.append(match.group(0))
        return f"\x00{len(code_spans) - 1}\x00"

    masked = CODE_SPAN_RE.sub(stash, body_html)
    # Before src() runs, so an inlined diagram has no src left to rewrite,
    # and after masking, so a tutorial *showing* `<img src="x.svg">` as an
    # example still shows it rather than drawing it.
    masked = inline_local_svg(folder, masked, tutorial.path)
    resolved = HREF_ASSET_RE.sub(href, SRC_RE.sub(src, masked))
    return re.sub(r"\x00(\d+)\x00", lambda m: code_spans[int(m.group(1))], resolved)


def copy_tutorial_assets(tutorial: Tutorial) -> None:
    """Copy a tutorial's assets to the site, into a folder named for the
    tutorial — which is where `resolve_assets()` has just pointed every
    reference, from the current release and every frozen one alike.

    Every version of a tutorial copies the same folder to the same place, so
    this runs more than once per tutorial and has to be safe to repeat. It is:
    the same bytes are written to the same path.
    """
    assets = tutorial_assets(tutorial)
    if not assets:
        return
    target = OUT / "tutorials" / tutorial.folder
    target.mkdir(parents=True, exist_ok=True)
    for asset in assets:
        shutil.copy2(asset, target / asset.name)


def load(path: Path) -> Tutorial:
    """Turns one tutorial's source file into a fully-parsed `Tutorial`
    object — this is the one function that runs the whole parsing
    pipeline described at the top of this file, in order: split off the
    frontmatter, pull out cells/code-blocks/maths so Markdown can't
    mangle them, convert the remaining prose to HTML, put the cells and
    blocks back in, then pull out pedagogical notes. Every tutorial page
    build.py builds starts here.
    """
    meta, body = split_frontmatter(path.read_text(), path)
    stripped, cells, blocks, hints, site_editors, questions, app_cells = extract_blocks(body, path)
    stripped, maths = extract_math(stripped)
    stripped = loosen_tight_lists(stripped)
    converted, toc = to_html(stripped)
    converted = place_hints(converted, hints, maths)
    body_html = place_blocks(converted, cells, blocks, maths, site_editors, questions, app_cells,
                              page=id_of(path), version=str(meta.get("version", "")))
    body_html, notes = extract_notes(body_html, path)
    anchors = (
        set(ID_RE.findall(body_html))
        | {c.id for c in cells}
        | {pane.id for editor in site_editors for pane in editor.panes.values()}
        | {pane.id for cell in app_cells for pane in cell.panes.values()}
    )
    return Tutorial(
        path=path,
        meta=meta,
        cells=cells,
        body_html=body_html,
        # Not just bool(maths): that list is only the top-level prose's
        # own maths, extracted before extract_notes()/
        # render_question() ever run, and each of those
        # can now add its own — a hand-written practice-page answer, a
        # pedagogical note, a question's prompt. Checking the finished
        # body_html (and, separately, a note's own html — extract_notes()
        # has already pulled that out of body_html by this point) for a
        # real .dl-math span is what write()'s own `if tutorial.has_math`
        # gate (the KaTeX bundle fetch) actually needs to know, wherever
        # the maths came from.
        has_math="dl-math" in body_html or any("dl-math" in note.html for note in notes),
        has_sql=any(c.type == "sql" for c in cells),
        site_editors=site_editors,
        app_cells=app_cells,
        anchors=anchors,
        toc=toc,
        notes=notes,
    )


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
    path = ASSETS / name
    key = str(path)
    if key not in _ASSET_VERSIONS:
        _ASSET_VERSIONS[key] = (
            hashlib.sha256(path.read_bytes()).hexdigest()[:8] if path.is_file()
            else "missing"
        )
    return _ASSET_VERSIONS[key]


def versioned(base: str, name: str) -> str:
    """Builds a full asset URL with its cache-busting `?v=...` hash
    appended — the thing every `<link>`/`<script>` tag for a CSS or JS
    file in the built pages actually uses, rather than a plain URL. """
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
                  registry: dict[str, Tutorial] | None = None,
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
            owner = (registry or {}).get(slug)
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
        owner = (registry or {}).get(tutorial.practice_for)
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
            registry[slug].title
            for slug in page.practice_across
            if slug != tutorial.slug and slug in (registry or {})
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


_LICENCE_URL = "https://github.com/deweydex/dewlab/blob/main/LICENSE.md"
_REPORT_REPO_URL = "https://github.com/deweydex/dewlab"
FEEDBACK_CONFIG_FILE = "feedback.yaml"


def feedback_enabled() -> bool:
    """Whether the "report something about this page" link appears anywhere
    on the site, read from `planning/feedback.yaml` rather than held in a
    constant computed at import time, which would not see a test's
    temporary ROOT — the same reasoning as `courses()`. `read_yaml()`
    parses it once per build and again whenever it changes, so the file
    still decides and the build does not re-parse it for all 1256 pages.

    Missing the file, or the file missing `enabled:`, both mean on. The
    switch exists to turn the link off in a hurry — one line, editable from
    GitHub's own web editor, no code to find — not to make on the fussy
    path.
    """
    path = ROOT / "planning" / FEEDBACK_CONFIG_FILE
    if not path.is_file():
        return True
    data = read_yaml(path, strict=False) or {}
    return bool(data.get("enabled", True))


_REPORT_KIND_ERROR = (
    "It gives an error, and I have tried resetting the cell, running the "
    "cells above it, and reloading the page"
)
_REPORT_KIND_WRONG = "The page is wrong, or I could not follow it"


def report_issue_url(page: str, version: str, kind: str = "", cell: str = "") -> str:
    """The prefilled GitHub issue link a report door opens.

    `page`, `version`, `kind` and `cell` only fill in fields on GitHub's own
    form — nothing is sent until the reader presses GitHub's own Submit, and
    every field is still theirs to edit or clear first. `kind`, when given,
    must match one of `.github/ISSUE_TEMPLATE/report.yml`'s dropdown options
    exactly, or GitHub leaves the dropdown unset rather than failing loudly.
    See docs/REPORTING_A_PROBLEM.md.
    """
    params = {"template": "report.yml", "page": page, "version": str(version)}
    if kind:
        params["kind"] = kind
    if cell:
        params["cell"] = cell
    return f"{_REPORT_REPO_URL}/issues/new?{urllib.parse.urlencode(params)}"


def report_doors_links(page: str, version: str, cell: str = "") -> str:
    """The three doors themselves: a question goes to Discussions rather
    than an issue, since a question filed as a bug report is the wrong
    container for it and for whoever answers it later; the other two open
    the issue form with `kind` already picked. Shared by the footer
    (`report_doors_html()`, no `cell`) and a cell's own report panel
    (`render_cell()`, `cell` set to that cell's id).

    Three links joined by " · " rather than a `<ul>`/`<li>` list — a
    bulleted list is the wrong shape for three short links, and it also
    silently broke every test that counted a page's `<li>` tags, since
    this markup reaches every page.

    The account note is here rather than repeated at each caller, so
    every surface a reader can reach these doors from — the footer, the
    Give Feedback panel, a cell's own report box — says it the same way,
    once, instead of drifting.
    """
    error_url = report_issue_url(page, version, _REPORT_KIND_ERROR, cell)
    wrong_url = report_issue_url(page, version, _REPORT_KIND_WRONG, cell)
    return (
        "<p>"
        f'<a href="{_REPORT_REPO_URL}/discussions/new">I have a question</a> · '
        f'<a class="dl-report-issue-link" href="{error_url}">It gives an error</a> · '
        f'<a class="dl-report-issue-link" href="{wrong_url}">The page is wrong, or I could not follow it</a>'
        "</p>"
        '<p class="dl-panel-note">GitHub will ask you to sign in with a free account first.</p>'
    )


def report_doors_html(page: str, version: str) -> str:
    """The footer's three-doors disclosure. A plain `<details>` element, so
    this needs no JavaScript and no runtime change.
    """
    return (
        '<details class="dl-report-doors">'
        "<summary>Something wrong on this page? Tell us.</summary>"
        + report_doors_links(page, version) +
        "</details>"
    )


def report_doors_panel_html(page: str, version: str) -> str:
    """The Give Feedback door's own content — the small circle fixed at the
    bottom-right of the screen, not a corner-dock tab (DECISIONS_LOG.md
    7.194) — the same three doors as the footer's disclosure (report_doors_html()),
    without the <details> wrapper, since the button that opens this panel
    is already the thing a reader clicked on purpose. This is a second way
    to the same doors, not a replacement: the footer's own version stays,
    since it needs no JavaScript and this panel does. Respects
    feedback_enabled() the same way site_footer() does, for the same
    reason.
    """
    if not page or not feedback_enabled():
        return ""
    return (
        '<p class="dl-panel-note">'
        "Is something wrong with this page, or is a cell not behaving? "
        "A report tells us the page and the version you're on, so it's "
        "easy to check."
        "</p>"
        + report_doors_links(page, version)
    )


def site_footer(page: str = "", version: str = "") -> str:
    """Copyright line and licence line, stamped with the current year, plus
    a "three doors" disclosure for reporting something about this page,
    unless `feedback_enabled()` says it is switched off, or the caller
    passed no `page` to report against.
    """
    year = datetime.date.today().year
    footer = (
        f'© {year} J. S. Aaron · '
        f'<a href="{_LICENCE_URL}">Licence</a>'
    )
    if page and feedback_enabled():
        footer += f" · {report_doors_html(page, version)}"
    return footer


def also_part_of(tutorial: Tutorial, body_html: str, up: str) -> str:
    """The page body, with one line under its heading when more than one
    course lists the page: which other courses it is part of, each a link
    to that course's page. Nothing at all on a page with one course or
    none, which is most pages — the line is there for the reader who came
    from the other course and wonders whether they are in the right place.
    """
    others = tutorial.courses[1:]
    if not others:
        return body_html
    links = [
        f'<a href="{up}{html.escape(c, quote=True)}.html">{html.escape(course_title(c))}</a>'
        for c in others
    ]
    named = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " and " + links[-1]
    line = f'<p class="dl-also-part-of">This page is also part of {named}.</p>'
    end = body_html.find("</h1>")
    if end == -1:
        return line + body_html
    end += len("</h1>")
    return body_html[:end] + line + body_html[end:]


def write(tutorial: Tutorial, shell: str, body_html: str, nav: str = "",
          default: Tutorial | None = None, family: list[Tutorial] | None = None,
          practice: Tutorial | None = None,
          registry: dict[str, Tutorial] | None = None,
          also: list[Tutorial] | None = None,
          glossary: list[dict] | None = None,
          notes: list[dict] | None = None,
          datasets: list[dict] | None = None,
          groups: dict[tuple[str, str], list[Tutorial]] | None = None,
          members: list[Tutorial] | None = None) -> Path:
    """Assembles and writes one finished tutorial page to disk: builds
    the JSON manifest that `assets/tutorial-runtime.js` reads on the
    page (`docs/tutorial-runtime-explained.md` covers what that file
    does with it), fills the page shell template with the tutorial's own
    content and navigation, and writes the result under `site/`. This is
    the one function that turns a parsed `Tutorial` object plus all its
    surrounding context (its series, its glossary, its notes) into an
    actual HTML file a browser can open.
    """
    up = "../" * tutorial.depth
    manifest: dict[str, object] = {
        # `id` is the page's key for everything the runtime saves; `slug`
        # is the same string under the name the runtime's older readers
        # used. `courses` is every course that lists the page, default
        # first, so the runtime can draw the chrome for whichever one the
        # reader is following; `legacy` (legacy_ids()) is the key the
        # page's saved work lived under before courses/ existed.
        "id": tutorial.slug,
        "slug": tutorial.slug,
        "courses": tutorial.courses,
        "version": tutorial.meta["version"],
        "assetBase": f"{up}assets/",
        # The runtime fetches these itself, so they need their own versions —
        # a page can only cache-bust what its own markup names.
        "assetVersions": {"tutorial_tools.py": asset_version("tutorial_tools.py")},
        "dataBase": f"{up}data/",
        "cells": [
            {"id": c.id, "hint": c.hint, "code": c.code}
            | ({"expect": c.expect} if c.expect else {})
            | ({"name": c.name} if c.name else {})
            | ({"type": c.type} if c.type != "python" else {})
            for c in tutorial.cells
        ],
    }
    legacy = legacy_ids().get(tutorial.slug)
    if legacy:
        manifest["legacy"] = legacy
    versions = version_manifest(tutorial, family or [tutorial])
    if versions:
        manifest["versions"] = versions
    if tutorial.has_math:
        # The runtime fetches the 266 KB KaTeX bundle only when this is set, so
        # a tutorial with no maths never pays for it.
        manifest["math"] = True
    if tutorial.has_sql or tutorial.app_cells:
        # An app cell's own JS needs the shared `db` connection to exist
        # at boot for it to read, the same reason a `sql exec` cell does.
        manifest["needsSqlite"] = True
    if tutorial.site_editors:
        manifest["siteEditors"] = [
            {
                "name": editor.name,
                "panes": {
                    lang: {"id": pane.id, "code": pane.code}
                    for lang, pane in editor.panes.items()
                },
            }
            for editor in tutorial.site_editors
        ]
    if tutorial.app_cells:
        manifest["appCells"] = [
            {
                "name": cell.name,
                "panes": {
                    lang: {"id": pane.id, "code": pane.code}
                    for lang, pane in cell.panes.items()
                },
            }
            for cell in tutorial.app_cells
        ]
    packages = tutorial.meta.get("packages")
    if packages:
        manifest["packages"] = list(packages)
    if glossary:
        manifest["glossary"] = glossary
    if notes:
        manifest["notes"] = notes
    if datasets:
        manifest["datasets"] = datasets
    # Same site-wide content on every page, so write() reads it directly
    # rather than every one of write()'s many call sites threading it
    # through as its own parameter.
    math_basics = load_math_basics()
    if math_basics:
        manifest["mathBasics"] = math_basics
    python_basics = load_python_basics()
    if python_basics:
        manifest["pythonBasics"] = python_basics

    tokens = {
        "{{TITLE}}": html.escape(str(tutorial.meta["title"])),
        "{{CANONICAL}}": canonical_link(tutorial, default),
        "{{VERSION}}": html.escape(str(tutorial.meta["version"]), quote=True),
        "{{SLUG}}": html.escape(tutorial.slug, quote=True),
        "{{MODULE}}": html.escape(tutorial.course, quote=True),
        "{{YEAR}}": html.escape(str(tutorial.meta["year"]), quote=True),
        "{{SERIES}}": html.escape(tutorial.series, quote=True),
        "{{ASSET_BASE}}": f"{up}assets/",
        "{{STYLE_URL}}": versioned(f"{up}assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned(f"{up}assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned(f"{up}assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned(f"{up}assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned(f"{up}assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned(f"{up}assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": up,
        "{{CRUMBS}}": (
            crumb_trail_html(tutorial, groups, members, up, practice, registry, also)
            if groups is not None
            else html.escape(f"{course_title(tutorial.course) or 'dewlab'} · {tutorial.meta['year']}")
        ),
        "{{NAV_PREV_NEXT}}": nav,
        "{{PAGE_SCRIPT}}": "",
        "{{DOWNLOAD}}": download_section(tutorial),
        "{{BODY}}": (
            page_notice(tutorial, default)
            + (practice_link(tutorial, practice, registry, also)
               if tutorial.is_practice else "")
            + also_part_of(tutorial, body_html, up)
            + (practice_link(tutorial, practice, registry, also)
               if not tutorial.is_practice else "")
        ),
        # `<` escaped so nothing in a cell can close the surrounding <script>.
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer(tutorial.slug, tutorial.meta["version"]),
        "{{REPORT_DOORS}}": report_doors_panel_html(tutorial.slug, tutorial.meta["version"]),
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


def inline_accessible_fonts_css() -> str:
    """The two accessible reading fonts' stylesheet, with its own fonts
    folded in as data — same shape as inline_katex_css() above, and able
    to reuse its FONT_URL_RE unchanged because vendor-src/build-vendor.mjs
    writes these woff2 files flat into vendor/fonts/ beside KaTeX's own
    rather than into a subfolder of their own.
    """
    css = (ASSETS / "vendor" / "accessible-fonts.css").read_text()

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
    # The same prefixes build.py wrote into the page's own references: `up`
    # for anything under assets/, `root` for the site root itself.
    root = "../" * tutorial.depth
    up = root + "assets/"
    style = (ASSETS / "tutorial-style.css").read_text()
    bundle = (ASSETS / "vendor" / "standalone.bundle.js").read_text()
    tools = (ASSETS / "tutorial_tools.py").read_text()

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
    # lines, which point at other files.
    def keep_contents(match: re.Match) -> str:
        contents = re.search(
            r'<details class="dl-crumb-level dl-crumb-level-4">.*?</details>',
            match.group(0), re.DOTALL,
        )
        if not contents:
            return ""
        own = re.sub(r'<div role="listitem" class="dl-crumb-practice">.*?</div>', "", contents.group(0), flags=re.DOTALL)
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
    figuring out where that string should be saved and doing a couple of
    build-time sanity checks (like the load_csv warning right below) that
    only make sense for this particular kind of output.
    """
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


def series_slug(course: str, series: str) -> str:
    """A filename for a whole series: the course id and the series key."""
    slug = SERIES_SLUG_RE.sub("-", f"{course}-{series}".lower()).strip("-")
    return slug or "tutorials"


def zip_sequence(
    members: list[Tutorial], practice: dict[str, Tutorial]
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
        page = practice.get(tutorial.slug)
        if page is not None:
            sequence.append(page)
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
        archive.write(OUT / "download" / f"{member.slug}.html", f"{folder}/{name}")
        entries.append((name, member))
    return entries


def write_series_zip(
    course: str,
    series: str,
    members: list[Tutorial],
    practice: dict[str, Tutorial],
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
    target = OUT / "download" / f"{folder}.zip"
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
    practice: dict[str, Tutorial],
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
    target = OUT / "download" / f"{course}-all.zip"
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


def write_dewmini_bundle() -> Path | None:
    """The downloadable dewmini: a folder a student or teacher can save and
    open with no internet at all, once assets/vendor/pyodide/ exists to
    include.

    It still needs a local server to open, though: dewmini.js imports
    dewmini-fs.js and pyodide-engine.js with real `import` statements,
    and a browser only allows that kind of cross-file import from
    http(s)://, never a file opened straight off disk. `index.html` below
    checks for this rather than assuming a downloader read a README first,
    and SERVE_SCRIPT is copied in as this bundle's own serve.py.

    The bundle mirrors the hosted site's actual folder shape — compose/,
    assets/, and data/ as siblings, exactly what compose/dewmini.html's own
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
    dewmini_html = COMPOSE / "dewmini.html"
    if not dewmini_html.exists():
        return None

    target = OUT / "download" / "dewmini"
    shutil.rmtree(target, ignore_errors=True)
    (target / "assets" / "vendor").mkdir(parents=True, exist_ok=True)

    pyodide_vendored = (ASSETS / "vendor" / "pyodide").is_dir()

    shutil.copytree(COMPOSE, target / "compose")
    html = (target / "compose" / "dewmini.html").read_text()
    if pyodide_vendored:
        html = html.replace(
            "<head>",
            '<head>\n<script>window.DEWLAB_PYODIDE_BASE = "../assets/vendor/pyodide/";</script>',
            1,
        )
        (target / "compose" / "dewmini.html").write_text(html)

    for rel in DEWMINI_ASSET_FILES:
        src = ASSETS / rel
        if not src.exists():
            print(f"note: dewmini bundle is missing {src.relative_to(ROOT)}", file=sys.stderr)
            continue
        dest = target / "assets" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    if DATA.is_dir():
        shutil.copytree(DATA, target / "data")

    fonts_dir = ASSETS / "vendor" / "fonts"
    if fonts_dir.is_dir():
        shutil.copytree(fonts_dir, target / "assets" / "vendor" / "fonts")

    if pyodide_vendored:
        shutil.copytree(ASSETS / "vendor" / "pyodide", target / "assets" / "vendor" / "pyodide")
    else:
        print(
            "note: assets/vendor/pyodide/ not found (see "
            "write_dewmini_bundle()'s docstring for the fetch command) — "
            "the dewmini bundle will still boot Python from the CDN on "
            "first run rather than fully offline",
            file=sys.stderr,
        )

    coi_src = ASSETS / "vendor" / "coi-serviceworker.js"
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
        "<title>dewmini</title>\n"
        "<style>body{font:15px/1.5 sans-serif;max-width:34rem;margin:3rem auto;padding:0 1rem;}"
        "code{background:#eee;padding:0.1rem 0.35rem;border-radius:3px;}</style>\n"
        "</head>\n"
        "<body>\n"
        '<div id="file-warning" hidden>\n'
        "<h1>One more step</h1>\n"
        "<p>Opening this file directly shows a blank page — dewmini's own "
        "JavaScript needs a real (if entirely local) web server to load, "
        "which a browser won't do for a file opened straight off disk.</p>\n"
        "<p>Open a terminal in this folder and run:</p>\n"
        "<p><code>python3 serve.py</code></p>\n"
        "<p>That opens a browser tab pointed at dewmini for you. Leave the "
        "terminal window open while you use it.</p>\n"
        "</div>\n"
        "<script>\n"
        "if (window.location.protocol === \"file:\") {\n"
        '  document.getElementById("file-warning").hidden = false;\n'
        "} else {\n"
        '  window.location.replace("compose/dewmini.html");\n'
        "}\n"
        "</script>\n"
        "<noscript><p>JavaScript is off, so this can't check what's needed automatically: "
        "run <code>python3 serve.py</code> in this folder from a terminal, then open the "
        "browser tab it starts, or (with JavaScript back on) open "
        '<a href="compose/dewmini.html">dewmini</a> directly once this is being served.</p></noscript>\n'
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


# The site's own hand-written pages: each is `pages/<name>.md`, written
# to `<file>.html` at the site root, with the crumb the corner shows and
# the one link the bottom nav offers. The home page is the one every other
# page's masthead links to, so its crumb is empty and its file is index.html.
SITE_PAGES: dict[str, tuple[str, str, str]] = {
    # name: (output file stem, crumb text, bottom-nav link)
    "home": ("index", "", '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>'),
    "about": ("about", "about", '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>'),
    "features": ("features", "features", '<a class="dl-nav-up" href="index.html">Home</a>'),
}


def write_page(shell: str, name: str) -> Path:
    """One of the site's own pages — the home page, About, or the features
    page — from `pages/<name>.md`, read through `read_page()`.

    A page is a hand-written markdown file with a `title` and nothing else
    in its frontmatter: no course, no version, no cells. `read_page()`
    converts its body the way a tutorial's prose converts, fills any
    `[[name]]` marker (`GENERATED_BLOCKS` — the live search box, the
    course cards) and any ```card fence, and this function only assembles
    the shell around what it returns. The three pages differ in their
    file name, the crumb in the corner and the one link the bottom nav
    offers, which is what `SITE_PAGES` holds; everything else is the same,
    and was written out three times before this function existed.

    Every word on these pages is student-facing: the plain-language rules
    in PEDAGOGICAL_STYLE_GUIDE.md section 4 apply.
    """
    stem, crumb, nav = SITE_PAGES[name]
    meta, body = read_page(name)
    manifest = {"slug": stem, "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    # renderMaths() (tutorial-runtime.js) checks manifest.math before it
    # ever looks for a .dl-math span, the same gate write()'s own
    # tutorial.has_math sets for a tutorial — a page's own prose, its
    # cards and its section wrappers can all carry maths now
    # (convert_prose_with_math), so this is what turns the KaTeX bundle
    # fetch on for whichever pages actually used it.
    if "dl-math" in body:
        manifest["math"] = True
    tokens = {
        "{{TITLE}}": meta["title"],
        "{{VERSION}}": "1",
        "{{SLUG}}": stem,
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": f'<span class="dl-crumbs">{html.escape(crumb)}</span>' if crumb else "",
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": nav,
        "{{PAGE_SCRIPT}}": "",
        # None of these is a tutorial: nothing to download, no canonical
        # release; the runtime hides the empty section rather than showing
        # a bare heading.
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": body,
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer(stem, "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html(stem, "1"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(f"shell template has tokens the {name} page does not fill: {leftover}")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{stem}.html"
    target.write_text(page)
    return target


def write_all_tutorials_page(
    shell: str,
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path] | None = None,
    retired: dict[str, list[Tutorial]] | None = None,
    practice: dict[str, Tutorial] | None = None,
    mixed: dict[str, list[Tutorial]] | None = None,
    course_archives: dict[str, Path] | None = None,
) -> Path:
    """Every course, every series, every tutorial — the page "All
    tutorials" on the front page and every other page's own "All
    tutorials" link point at.
    """
    manifest = {"slug": "all-tutorials", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "All tutorials",
        "{{VERSION}}": "1",
        "{{SLUG}}": "all-tutorials",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": '<span class="dl-crumbs">all tutorials</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="index.html">Home</a>',
        "{{PAGE_SCRIPT}}": "",
        # This page is not a tutorial and has nothing to download; the
        # runtime hides the empty section rather than showing a bare heading.
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        # This page is a contents list. It does not need one of its own.
        # Nor a series to navigate — it is the thing every series links back to.
        "{{BODY}}": render_tutorials_list(
            groups, archives, retired, practice, mixed, course_archives),
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("all-tutorials", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("all-tutorials", "1"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(
            f"shell template has tokens the all-tutorials page does not fill: {leftover}")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "all-tutorials.html"
    target.write_text(page)
    return target


def write_all_notes_page(shell: str, tutorials: list[Tutorial]) -> Path:
    """My Notes: every highlight and every page's own free-text notes,
    gathered from every tutorial this browser has ever saved progress
    for — into one page to review, search, or download as a plain-text
    study sheet (DECISIONS_LOG.md, the highlight-colours-and-list entry).

    Nothing here comes from the build: localStorage is shared per
    origin, not per page, so `assets/my-notes.js` reads every saved
    record itself, client-side, once this page loads. The one thing the
    build *can* give it that storage can't is a title for each slug —
    a saved record only carries `tutorial-slug`, not a human title — so
    this bakes in a small {slug: title} map the same way tree.js reads
    its own topic-graph data island (`write_tree_page()`).
    """
    titles = {t.slug: t.title for t in tutorials if t.is_default}
    body = (
        '<h1>My Notes</h1>'
        '<p class="dl-panel-note">Every highlight and note you\'ve made '
        "across every tutorial you've opened in this browser, on this "
        "device — gathered here to review. Nothing on this page is sent "
        "anywhere; it's read straight out of this browser's own storage, "
        "the same way each tutorial's own Notes panel already is.</p>"
        '<div class="dl-my-notes-controls">'
        '<input type="search" id="dl-my-notes-search" '
        'placeholder="Search your notes and highlights…" '
        'aria-label="Search your notes and highlights">'
        '<button type="button" class="dl-btn" id="dl-my-notes-download">'
        "Download as text</button>"
        "</div>"
        '<p class="dl-panel-note" id="dl-my-notes-empty" hidden></p>'
        '<div id="dl-my-notes-list"></div>'
    )
    manifest = {"slug": "all-notes", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "My Notes",
        "{{VERSION}}": "1",
        "{{SLUG}}": "all-notes",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": '<span class="dl-crumbs">my notes</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": (
            '<script type="application/json" id="dewlab-titles">'
            + json.dumps(titles).replace("<", "\\u003c")
            + "</script>\n"
            + f'<script type="module" src="{versioned("assets/", "my-notes.js")}"></script>'
        ),
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": body,
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("all-notes", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("all-notes", "1"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(
            f"shell template has tokens the my-notes page does not fill: {leftover}")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "all-notes.html"
    target.write_text(page)
    return target


def render_course_cards() -> str:
    """One front-page tile per course, in courses/index.yaml order, from
    the course files: the title, the status badge, the QQI code, and the
    `card:` text. What `pages/home.md` used to hand-write six times over,
    now the `[[course-cards]]` generated block — so adding a course is a
    course file and one line in the index, and the front page follows."""
    return "".join(
        render_card(PageCard(
            url=f"{course.id}.html",
            heading=course.title,
            body_html=f"<p>{html.escape(course.card)}</p>" if course.card else "",
            status=course.status,
            meta=course.code or None,
            wide=False,
        ))
        for course in courses().values()
    )


def write_course_page(
    shell: str,
    course: Course,
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path],
    retired: dict[str, list[Tutorial]],
    practice: dict[str, Tutorial],
    mixed: dict[str, list[Tutorial]],
    course_archives: dict[str, Path],
) -> Path:
    """One course's own page: its description, its QQI code, and only its
    own tutorials and practice pages — not the other courses' too.

    A reader following a course tile from the front page lands here
    rather than partway down the full contents list. Written at the site
    root, alongside `index.html`, so it can reuse every href
    `render_course_body()` builds unchanged — those are relative to the
    site root already, which is exactly where a course page also lives.
    """
    body = [
        f"<h1>{html.escape(course.title)} "
        f'<span class="dl-module-card-badge" data-status="{html.escape(course.status, quote=True)}">'
        f"{html.escape(course.status.capitalize())}</span></h1>"
    ]
    if course.code:
        body.append(f'<p class="dl-module-card-meta">{html.escape(course.code)}</p>')
    for para in course.description:
        body.append(f"<p>{html.escape(para)}</p>")
    body.extend(render_course_body(
        course, groups, archives, retired, practice, mixed, course_archives, heading=False,
    ))

    # `course` is what the runtime remembers: opening a tutorial from here
    # is following this course (tutorial-runtime.js, initCourse()).
    manifest = {"slug": course.id, "course": course.id, "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": html.escape(course.title),
        "{{VERSION}}": "1",
        "{{SLUG}}": html.escape(course.id, quote=True),
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": f'<span class="dl-crumbs">{html.escape(course.title)}</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": "",
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": "\n".join(body),
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer(course.id, "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html(course.id, "1"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(f"shell template has tokens the course page does not fill: {leftover}")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{course.id}.html"
    target.write_text(page)
    return target


REDIRECT_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={href}">
<link rel="canonical" href="{href}">
<title>This page has moved</title>
</head>
<body>
<p>This page has a new address. If it does not open on its own,
<a href="{href}">open it here</a>.</p>
</body>
</html>
"""


def write_redirects(pages: list[Path]) -> list[Path]:
    """A small page at every address the site used to have, sending the
    browser on to the new one — read from `courses/redirects.yaml`, one
    `old: new` line per page. Written after every real page, and refusing
    to overwrite one: an old address that is also a current address is a
    mistake in the file, not a page to replace. A new address the build
    wrote nothing at is refused too, so the file cannot quietly point a
    bookmark at nothing.

    `pages` is what this build wrote, and is the only thing consulted: a
    file left in `site/` by an earlier build (before an address moved,
    say) is not a page at that address, and a build without `--clean`
    would otherwise refuse the very line that retires it. The stub
    overwrites it.
    """
    path = COURSES / REDIRECTS_FILE
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        fail(path, "is a mapping of old address to new address, one per line")
    written: list[Path] = []
    current = {page.resolve() for page in pages}
    for old, new in data.items():
        old, new = str(old), str(new)
        source, target = OUT / old, OUT / new
        if target.resolve() not in current:
            fail(path, f"sends {old} to {new}, and this build wrote no page at {new}")
        if source.resolve() in current:
            fail(path, f"sends {old} somewhere, but the build writes a page at {old}. "
                       "Delete the line.")
        href = os.path.relpath(target, source.parent).replace(os.sep, "/")
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(REDIRECT_PAGE.format(href=html.escape(href, quote=True)))
        written.append(source)
    return written


def write_routes(
    groups: dict[tuple[str, str], list[Tutorial]],
    practice: dict[str, Tutorial],
    mixed: dict[str, list[Tutorial]],
) -> Path:
    """`assets/routes.json`: every course's contents, by id, with each
    page's title and address — what tutorial-runtime.js reads to draw a
    page's tree and previous/next for a course other than the one the
    build wrote in (a tutorial on two courses; see crumb_trail_html()).
    Written under `site/assets/` after the assets are copied, since that
    copy starts from an empty folder."""
    routes = []
    for course in courses().values():
        series = []
        for key in course.keys:
            members = groups.get((course.id, key), [])
            if not members:
                continue
            entries = []
            for member in members:
                entry = {
                    "id": member.slug,
                    "title": member.title,
                    "url": member.out_path.relative_to(OUT).as_posix(),
                }
                problems = practice.get(member.slug)
                if problems is not None:
                    entry["practice"] = {
                        "id": problems.slug,
                        "title": problems.title,
                        "url": problems.out_path.relative_to(OUT).as_posix(),
                    }
                entries.append(entry)
            series.append({"key": key, "title": course.series_title(key), "tutorials": entries})
        routes.append({
            "id": course.id,
            "title": course.title,
            "url": f"{course.id}.html",
            "series": series,
            "mixed": [
                {"id": page.slug, "title": page.title,
                 "url": page.out_path.relative_to(OUT).as_posix()}
                for page in mixed.get(course.id, [])
            ],
        })
    target = OUT / "assets" / "routes.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"courses": routes}, ensure_ascii=False))
    return target


def warn_about_titles_and_overlap(tutorials: list[Tutorial]) -> None:
    """Two things the build lets through and says so: two pages with one
    title, and two tutorials teaching mostly the same outcomes. Neither is
    wrong — two courses may each have a "Joins" — but each is worth a
    second look, and nothing else would ever mention it (refactor
    decisions: DECISIONS_LOG 7.172).
    """
    pages = [t for t in tutorials if t.is_default and not t.is_practice]
    by_title: dict[str, list[Tutorial]] = {}
    for page in pages:
        by_title.setdefault(page.title.strip().lower(), []).append(page)
    for members in by_title.values():
        if len(members) > 1:
            named = ", ".join(
                f"{m.path.relative_to(ROOT)} (on {', '.join(m.courses) or 'no course'})"
                for m in members
            )
            print(f'note: two pages share the title "{members[0].title}": {named}',
                  file=sys.stderr)

    def outcomes(page: Tutorial) -> set[str]:
        return {
            code
            for claim in (page.meta.get("covers") or {}).values()
            for code in (claim.get("covers") or [])
        }

    covered = [(page, outcomes(page)) for page in pages if page.status == "live"]
    for index, (page, codes) in enumerate(covered):
        for other, other_codes in covered[index + 1:]:
            shared = sorted(codes & other_codes)
            if len(shared) >= 3:
                print(f"note: {page.path.relative_to(ROOT)} and "
                      f"{other.path.relative_to(ROOT)} both cover "
                      f"{', '.join(shared)}", file=sys.stderr)


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
        '<p class="dl-tree-strands-note">The stripe down the left of each topic '
        "shows its subject. The columns do not group subjects; only depth does. "
        "So the colour is how you follow one subject down the tree.</p>"
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
        '<p class="dl-tree-intro">Every topic both modules cover, and the order '
        "they build in. <strong>The tree reads downwards.</strong> Topics in the "
        "top row need nothing before them, so you could start any of them today. "
        "The further down a topic sits, the more you need to know first. Drag to "
        "move around, scroll to zoom, and choose any topic to see what it is, "
        "where it comes up in computing, and where it is taught.</p>"
        '<div class="dl-tree-layout">'
        '<div class="dl-tree-main">'
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

    strands = load_strands()
    for (_, _), members in sorted(series_of(tutorials).items()):
        svg = render_knowledge_map(members, strands)
        if svg:
            body += (
                '<h2 class="dl-tree-second">How the tutorials relate</h2>'
                '<figure class="dl-map-figure">' + svg +
                "<figcaption>Solid arrows show the reading order. A dashed arrow "
                "means the later tutorial builds on the earlier one and says so "
                "in its own text. Choose any box to open that "
                "tutorial.</figcaption></figure>"
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
        "{{CRUMBS}}": '<span class="dl-crumbs">topic tree</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": (
            '<script type="application/json" id="dewlab-tree">'
            + json.dumps(data).replace("<", "\\u003c")
            + "</script>\n"
            + f'<script type="module" src="{versioned("assets/", "tree.js")}"></script>'
        ),
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": body,
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("tree", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("tree", "1"),
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


def write_topics_page(
    shell: str,
    registry: dict[str, Tutorial],
    practice: dict[str, Tutorial],
) -> Path | None:
    """"Browse by topic" — the topic tree's sibling, and a genuinely
    different question. The tree says what a topic needs before it, for
    a reader moving through the course in order; this page is for a
    reader who already has some of it behind them and wants to jump
    straight to, say, everything about trigonometry, in whatever order
    suits them (planning/curriculum/topic-groups.yaml's own header
    comment goes into more depth on the two files' different jobs).

    A group naming a tutorial `registry` doesn't have (a typo, a rename,
    or — same as `topics.yaml`'s own module-level path — simply a test
    building a small, sandboxed set of tutorials that was never going to
    contain dewlab's real ones) is skipped rather than fatal, with a note
    on stderr. `tests/test_build.py`'s own
    `TestTopicGroupsMatchRealTutorials` is what actually holds this file
    accountable against the genuine tutorials on disk, the same way nothing
    checks `topics.yaml` against a build's tutorials either.
    """
    groups = load_topic_groups()
    if not groups:
        return None

    body = [
        "<h1>Browse by topic</h1>",
        '<p class="dl-topics-intro">The tutorials list reads top to bottom '
        "in the order the course teaches them. This page cuts across that "
        "— everything about one topic, gathered in one place, for "
        "practicing in whatever order suits you rather than paging "
        "through the whole course to find it. A tutorial that genuinely "
        "spans two topics is listed under both.</p>",
        render_search_box("Search — e.g. loops, probability, sorting…"),
    ]
    any_group_rendered = False
    for group in groups:
        items = []
        for ident in group["tutorials"]:
            member = registry.get(str(ident))
            if member is None:
                print(
                    f'note: topic-groups.yaml group "{group["key"]}" names '
                    f"{ident}, which this build has no tutorial for",
                    file=sys.stderr,
                )
                continue
            href = member.out_path.relative_to(OUT).as_posix()
            also = practice.get(member.slug)
            extra = ""
            if also is not None:
                where = also.out_path.relative_to(OUT).as_posix()
                extra = f' <a class="dl-contents-practice" href="{where}">Practice</a>'
            items.append(
                f'<li><a class="dl-contents-btn" href="{href}"{progress_attrs(member)}>'
                f'<span class="dl-contents-kicker">Explore</span>'
                f"{html.escape(member.title)}</a>{extra}</li>"
            )
        if not items:
            continue
        any_group_rendered = True
        body.append(f'<h2 id="{html.escape(group["key"], quote=True)}">'
                     f'{html.escape(group["name"])}</h2>')
        body.append(f'<p class="dl-panel-note">{html.escape(group["intro"].strip())}</p>')
        body.append('<ol class="dl-contents">')
        body.extend(items)
        body.append("</ol>")

    if not any_group_rendered:
        return None

    manifest = {"slug": "topics", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "Browse by topic",
        "{{VERSION}}": "1",
        "{{SLUG}}": "topics",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": '<span class="dl-crumbs">browse by topic</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": "",
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": "".join(body),
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("topics", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("topics", "1"),
    }
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    if "{{" in page:
        leftover = sorted({p.split("}}")[0] + "}}" for p in page.split("{{")[1:]})
        raise BuildError(f"shell template has tokens the topics page does not fill: {leftover}")

    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "topics.html"
    target.write_text(page)
    return target


def write_search_index(
    tutorials: list[Tutorial],
    registry: dict[str, Tutorial],
    groups: dict[tuple[str, str], list[Tutorial]],
) -> Path:
    """One JSON file, `assets/search-index.json`, listing every live
    tutorial with what a reader might actually search for: its title,
    which course and series it belongs to, and — this is the part that
    makes it more than a title search — the terms its own glossary
    entry says it *introduces* (`own_glossary()`, not the cumulative
    one: a later tutorial in the same series has already inherited an
    earlier term, and searching for it should point at where it was
    actually taught, not at every page downstream of that).

    `assets/search.js` loads this once and does the actual matching
    client-side — nothing server-side to run, consistent with the rest
    of a site that is just static files. Archived and practice-only
    pages are left out: a search result should be something worth
    sending a reader to first, and both already sit off the main
    reading order for the same reason.
    """
    documents = []
    for tutorial in tutorials:
        if tutorial.archived or not tutorial.is_default or tutorial.is_practice:
            continue
        terms = sorted({entry["term"] for entry in own_glossary(tutorial) if entry.get("term")})
        course = courses().get(tutorial.course)
        documents.append({
            "id": tutorial.slug,
            "title": tutorial.title,
            # The default course, under the names search.js reads; every
            # course, by id, for whoever needs the whole picture.
            "module": tutorial.course,
            "moduleTitle": course.title if course else "",
            "series": course.series_title(tutorial.series) if course and tutorial.series else "",
            "courses": tutorial.courses,
            "url": tutorial.out_path.relative_to(OUT).as_posix(),
            "terms": terms,
        })
    target = OUT / "assets" / "search-index.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(documents, ensure_ascii=False))
    return target


OUTCOME_SUBJECTS = {
    "MIT": "maths",       # Maths for Information Technology, 5N18396
    "PDP": "computing",   # Programming and Design Principles, 5N2927
    "CMPS": "computing",  # Computational Methods and Problem Solving, 5N0554
}

LEVEL_BANDS = ((2, "beginner"), (3, "intermediate"), (99, "advanced"))


def level_for_tier(tier: int) -> str:
    for ceiling, name in LEVEL_BANDS:
        if tier <= ceiling:
            return name
    return "advanced"


def tutorial_facets(
    tutorials: list[Tutorial],
) -> dict[str, dict]:
    """What each tutorial can be filtered by, keyed by id.

    Three facets, none of them invented here — each is read from data that
    already exists for another purpose, so none can drift from the thing it
    describes:

      * `subjects` — from the outcome codes a tutorial claims in `covers:`.
        A tutorial covering both an MIT and a PDP outcome gets both, which is
        not a fudge: seven of them genuinely do, and a term introduced there
        belongs to both subjects.
      * `level` — from the *deepest* outcome it covers, since that is the
        one gating how far in you need to be to follow the whole thing.
        The shallowest was tried first and is worse in both directions: it
        rates a tutorial by its easiest moment, so 150 of 222 terms came
        out "beginner", and it would cheerfully tell someone at the start
        of the course that a tutorial needing four layers of groundwork is
        approachable. Erring deep is the kinder error.
      * `groups` — the curated topic groups from topic-groups.yaml, which
        already allow a tutorial in more than one group by design.

    A tutorial claiming no outcomes (two real ones, plus every practice page)
    simply has no subject and no level. That is left as absence rather than
    guessed at, and the panel offers it as "unfiled" instead of hiding it.
    """
    topics = load_topics()
    tiers = topic_tiers(topics) if topics else {}

    groups_by_tutorial: dict[str, list[str]] = {}
    for group in load_topic_groups():
        for member in group.get("tutorials") or []:
            groups_by_tutorial.setdefault(str(member), []).append(group["key"])

    facets: dict[str, dict] = {}
    for tutorial in tutorials:
        codes = [
            code
            for claim in (tutorial.meta.get("covers") or {}).values()
            for code in (claim.get("covers") or [])
        ]
        subjects = sorted({
            OUTCOME_SUBJECTS[code.split("-")[0]]
            for code in codes
            if code.split("-")[0] in OUTCOME_SUBJECTS
        })
        depths = [tiers[code] for code in codes if code in tiers]
        facet = {"subjects": subjects}
        if depths:
            facet["level"] = level_for_tier(max(depths))
        groups = groups_by_tutorial.get(tutorial.slug)
        if groups:
            facet["groups"] = sorted(set(groups))
        facets[tutorial.slug] = facet
    return facets


def write_reference_index(tutorials: list[Tutorial]) -> Path:
    """One JSON file, `assets/reference-index.json`: every term every
    tutorial introduces, in one list, for dewmini's Library rail.

    Deliberately drops the rule a tutorial page's own Reference panel is
    built around — never show a reader a term they haven't been taught yet
    (`cumulative_glossary()`, assembled per page and series position).
    dewmini has no position in a series; it's the workspace a reader opens
    outside the curriculum, so this index is the plain union instead.

    Built from `own_glossary()` so each entry names the tutorial that
    introduced it — a reader meeting an unfamiliar term can see where it's
    actually taught. Deduplicated on `(term, kind)`, first definition
    winning, the same key `cumulative_glossary()` dedupes on.

    Names the tutorial's *title*, not a link: this file ships inside
    dewmini's offline bundle, which carries no tutorials, so a link would
    404 for every offline reader.
    """
    facets = tutorial_facets(tutorials)
    seen: dict[tuple[str, str], dict] = {}
    for tutorial in sorted(tutorials, key=lambda t: t.slug):
        if tutorial.archived or not tutorial.is_default or tutorial.is_practice:
            continue
        facet = facets.get(tutorial.slug, {})
        for entry in own_glossary(tutorial):
            key = (entry["term"], entry["kind"])
            if key in seen:
                continue
            record = {
                "term": entry["term"],
                "kind": entry["kind"],
                "definition": entry["definition"],
                "origin": tutorial.title,
            }
            if facet.get("subjects"):
                record["subjects"] = facet["subjects"]
            if facet.get("level"):
                record["level"] = facet["level"]
            if facet.get("groups"):
                record["groups"] = facet["groups"]
            if entry.get("example"):
                record["example"] = entry["example"]
            seen[key] = record

    entries = sorted(seen.values(), key=lambda e: e["term"].lower())
    target = OUT / "assets" / "reference-index.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(entries, ensure_ascii=False))
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
        "{{CRUMBS}}": '<span class="dl-crumbs">editor</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": (
            f'<link rel="stylesheet" href="{versioned("assets/", "vendor/milkdown.bundle.css")}">'
            f'<script type="module" src="{versioned("assets/", "editor.js")}"></script>'
        ),
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": body,
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("editor", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("editor", "1"),
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


def load_all() -> list[Tutorial]:
    """Every page under `tutorials/`, drafts included: one folder per
    tutorial, holding `<id>.md`, its practice page and any frozen release.

    Two files claiming one id stop the build here, naming both — the
    filesystem already refuses a second folder with the same name, and
    this catches the other way it can happen, a practice file beside a
    folder of the same name. A markdown file loose under `tutorials/`,
    outside any folder, is refused too: it has no id.
    """
    loose = sorted(TUTORIALS.glob("*.md"))
    if loose:
        fail(loose[0], "is not inside a folder. A tutorial is tutorials/<id>/<id>.md.")
    everything = [load(p) for p in sorted(TUTORIALS.glob("*/*.md"))]
    claimed: dict[str, Tutorial] = {}
    for tutorial in everything:
        if VERSION_FILE_RE.match(tutorial.path.stem):
            continue
        other = claimed.get(tutorial.slug)
        if other is not None:
            fail(tutorial.path, f"has the id {tutorial.slug}, and so does "
                                f"{other.path.relative_to(ROOT)}. An id is site-wide; "
                                "rename one folder.")
        claimed[tutorial.slug] = tutorial
    return everything


def build(clean: bool = False, standalone: bool = False) -> list[Path]:
    """Build the site. `standalone` also writes the downloadable single files,
    which need the real assets on disk and are the slow part of a build."""
    if not SHELL.is_file():
        raise BuildError(f"no shell template at {SHELL.relative_to(ROOT)}")
    if clean and OUT.exists():
        shutil.rmtree(OUT)

    everything = load_all()
    tutorials = versions_of([t for t in everything if t.status != "draft"])

    registry: dict[str, Tutorial] = {t.slug: t for t in tutorials if t.is_default}

    families: dict[str, list[Tutorial]] = {}
    for tutorial in tutorials:
        families.setdefault(tutorial.slug, []).append(tutorial)

    catalog = courses()
    place_tutorials(tutorials, registry)
    practice = practice_pairs(tutorials, registry)
    mixed = mixed_practice(tutorials, registry)
    # A frozen release sits where its current one does.
    for tutorial in tutorials:
        if not tutorial.is_default and tutorial.slug in registry:
            tutorial.placements = list(registry[tutorial.slug].placements)

    shell = SHELL.read_text()
    groups = series_of(tutorials)
    retired = archived_of(tutorials)
    warn_about_titles_and_overlap(tutorials)
    for tutorial in tutorials:
        if (tutorial.is_default and not tutorial.is_practice and not tutorial.placements
                and catalog and tutorial.status == "live"):
            print(f"note: no course lists {tutorial.slug}. It builds at "
                  f"tutorials/{tutorial.slug}.html, and nothing links to it — add "
                  "its id to a course file under courses/ when it is ready.",
                  file=sys.stderr)
    written: list[Path] = []
    for tutorial in tutorials:
        check_alt_text(tutorial)
        check_folds(tutorial)
        # An archived tutorial belongs to no reading order, so there is no
        # previous and no next — only the way back.
        members = groups.get((tutorial.course, tutorial.series), [])
        body_html = resolve_assets(tutorial, resolve_links(tutorial, registry))
        copy_tutorial_assets(tutorial)
        page_path = write(
            tutorial, shell, body_html, nav_for(tutorial, members),
            default=registry.get(tutorial.slug),
            family=families.get(tutorial.slug),
            practice=practice.get(tutorial.slug),
            also=[page for pages in mixed.values() for page in pages
                  if tutorial.slug in page.practice_across],
            registry=registry,
            glossary=cumulative_glossary(tutorial, registry, groups),
            notes=[{"id": n.id, "html": n.html} for n in tutorial.notes],
            datasets=check_datasets(tutorial),
            groups=groups,
            members=members,
        )
        written.append(page_path)
        # 0.7MB against 19KB for the hosted page, so only the version students
        # are actually being given is worth building forty times over.
        if standalone and tutorial.is_default:
            written.append(write_standalone(tutorial, page_path.read_text()))

    archives: dict[tuple[str, str], Path] = {}
    course_archives: dict[str, Path] = {}
    if standalone:
        for course in catalog.values():
            series_in_order: list[tuple[str, str, list[Tutorial]]] = []
            for key in course.keys:
                members = groups.get((course.id, key))
                if not members:
                    continue
                title = course.series_title(key)
                archives[(course.id, key)] = write_series_zip(
                    course.id, key, members, practice, title
                )
                series_in_order.append((key, title, members))
            if series_in_order or mixed.get(course.id):
                course_archives[course.id] = write_course_zip(
                    course.id, course.title, series_in_order, practice,
                    mixed.get(course.id, []),
                )
        written.extend(archives.values())
        written.extend(course_archives.values())

    if tutorials:
        written.append(write_page(shell, "home"))
        written.append(write_page(shell, "features"))
        written.append(write_all_tutorials_page(
            shell, groups, archives, retired, practice, mixed, course_archives
        ))
        written.append(write_all_notes_page(shell, tutorials))
        for course in catalog.values():
            written.append(write_course_page(
                shell, course, groups, archives, retired, practice, mixed,
                course_archives,
            ))
        tree = write_tree_page(shell, tutorials)
        if tree is not None:
            written.append(tree)
        topics_page = write_topics_page(shell, registry, practice)
        if topics_page is not None:
            written.append(topics_page)
        written.append(write_page(shell, "about"))
        written.append(write_editor_page(shell))
        written.extend(write_redirects(written))

    OUT.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(OUT / "assets", ignore_errors=True)
    shutil.copytree(ASSETS, OUT / "assets", ignore=shutil.ignore_patterns("shell.html"))
    if DATA.is_dir():
        shutil.rmtree(OUT / "data", ignore_errors=True)
        shutil.copytree(DATA, OUT / "data")

    if tutorials:
        written.append(write_reference_index(tutorials))
        written.append(write_routes(groups, practice, mixed))

    # dewmini (compose/) is its own small folder rather than more root-level
    # files, so it copies wholesale like assets/ does.
    if COMPOSE.is_dir():
        shutil.rmtree(OUT / "compose", ignore_errors=True)
        shutil.copytree(COMPOSE, OUT / "compose")

    if DEWMARK_WORKBENCH.is_dir():
        shutil.rmtree(OUT / "dewmark", ignore_errors=True)
        shutil.copytree(DEWMARK_WORKBENCH, OUT / "dewmark")

    if TOPIC_GAME.is_dir():
        shutil.rmtree(OUT / "topic_tree_game", ignore_errors=True)
        shutil.copytree(TOPIC_GAME, OUT / "topic_tree_game",
                        ignore=shutil.ignore_patterns("README.md"))

    # And the topic editor, on the same terms: reached by typing
    # /topic_editor/, for whoever is drawing the graph, and never linked.
    if TOPIC_EDITOR.is_dir():
        shutil.rmtree(OUT / "topic_editor", ignore_errors=True)
        shutil.copytree(TOPIC_EDITOR, OUT / "topic_editor",
                        ignore=shutil.ignore_patterns("README.md"))

    if standalone:
        dewmini_bundle_dir = write_dewmini_bundle()
        if dewmini_bundle_dir is not None:
            written.append(dewmini_bundle_dir)
            written.append(zip_directory(dewmini_bundle_dir, OUT / "download" / "dewmini.zip"))

    coi_src = ASSETS / "vendor" / "coi-serviceworker.js"
    if coi_src.exists():
        shutil.copy2(coi_src, OUT / "coi-serviceworker.js")

    if tutorials:
        written.append(write_search_index(tutorials, registry, groups))
    return written


def _reference_index_for_bundle(target: Path) -> None:
    """Copies the generated reference index into an offline bundle.

    It needs its own step because it is *generated* rather than checked
    in: DEWMINI_ASSET_FILES names files copied out of the source
    `assets/`, and this one only exists under `OUT` once
    write_reference_index() has run. Silently skipped when it isn't
    there — a build with no tutorials in it writes no index, and that
    should still produce a working bundle (just one whose Library says
    the reference is unavailable rather than showing an empty list).
    """
    source = OUT / "assets" / "reference-index.json"
    if source.exists():
        shutil.copy2(source, target / "assets" / "reference-index.json")


def main() -> int:
    """The command-line entry point — what actually runs when someone
    types `python3 build.py`. Parses the command-line flags, calls
    `build()` to do the real work, and translates the result into a
    process exit code: 0 for success, 1 if a `BuildError` was raised
    somewhere along the way (returning 1 rather than letting the
    exception crash with a Python traceback is what keeps the error
    message clean and readable, per `fail()`'s own comment above, instead
    of also showing an unrelated stack trace).
    """
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
