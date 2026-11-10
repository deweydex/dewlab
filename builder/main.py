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
import ast
import base64
import concurrent.futures
import contextlib
import datetime
import functools
import gzip
import hashlib
import html
import io
import json
import os
import re
import shutil
import sys
import threading
import tokenize
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import markdown
import yaml

import source_map
from builder.config import REPO, Config, cfg  # noqa: F401


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


REQUIRED_FRONTMATTER = ("title", "version")

STATUSES = ("draft", "beta", "live", "archived")

VERSION_RE = re.compile(r"^(?P<y>\d{4})\.(?P<m>\d{2})\.(?P<d>\d{2})\.(?P<n>\d+)$")

# Fields a tutorial used to carry and no longer may. Where a tutorial sits is
# not the tutorial's own business any more: a course file under courses/
# lists it, and the folder name is its id.
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
HEADER_RE = re.compile(r"^\s*(id|hint|expect|name|toolkit|tests)\s*:\s*(.*)$")
# `toolkit:` on a Python exec cell: its code is loaded into every later page
# of the course (toolkit_for()). Either spelling of each answer is accepted.
TOOLKIT_VALUES = {"yes": True, "true": True, "no": False, "false": False}
# The one header line a ```python toolkit-reference fence carries.
TOOLKIT_REFERENCE_HEADER_RE = re.compile(r"^\s*for\s*:\s*(.*)$")
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
QUESTION_HEADER_RE = re.compile(r"^\s*(id|type|answer|correct)\s*:\s*(.*)$")
QUESTION_TYPES = {"multiple-choice", "fill-in-the-blank"}
# One flat level of {...} — a gap with no "|" is a typing box, one with
# "|" a dropdown, the first item either way the expected answer. Braces
# inside $...$ maths are the maths' own, not gaps: find_gaps() below.
GAP_RE = re.compile(r"\{([^{}]*)\}")
# `html app`/`css app`/`js app` — a full-stack module's own fence kind.
# Same three languages as a site pane, on
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
    "empty results": "empty-results", "empty result": "empty-results",
    "empty-results": "empty-results", "empty-result": "empty-results",
    "minutes": "minutes", "minute": "minutes",
    # The predict block's two moments (#313): the reader says they are not
    # sure yet, and a guess and the output differ. Either may be written
    # bare, meaning once.
    "unsure": "unsure", "not sure": "unsure",
    "guess differed": "guess-differed", "guesses differed": "guess-differed",
    "guess-differed": "guess-differed",
}
# Signals that read naturally with no number: `after: unsure`.
BARE_TRIGGERS = {"unsure", "not sure", "guess differed", "guess-differed"}
TRIGGER_TERM_RE = re.compile(
    r"^(?:(?P<n1>\d+)\s+(?P<k1>[a-z][a-z -]*[a-z])|(?P<k2>[a-z][a-z-]*)\s*:\s*(?P<n2>\d+))$"
)
DEFAULT_HINT_AFTER = "errors:5"
DEFAULT_HINT_TITLE = "Let\u2019s slow down a moment\u2026"
# The ```solution and ```inputs blocks (#312). Like a hint, each belongs to
# the exec cell above it, or to the one its `for:` line names.
SOLUTION_HEADER_RE = re.compile(r"^\s*(for|title|needs)\s*:\s*(.*)$")
INPUTS_HEADER_RE = re.compile(r"^\s*(for|guess)\s*:\s*(.*)$")
# The ```typed block: the lines input() reads when nobody can type, in the
# comparison and in the build. Only `for:` is a header; every other line is
# one line typed, exactly as written.
TYPED_HEADER_RE = re.compile(r"^\s*(for)\s*:\s*(.*)$")
DEFAULT_SOLUTION_TITLE = "One way to do it"
# A line holding only `---` ends a solution's code and starts its notes.
SOLUTION_NOTES_RE = re.compile(r"^---[ \t]*$", re.MULTILINE)
# The ```predict block (#313): a guess written before the cell runs.
PREDICT_HEADER_RE = re.compile(r"^\s*(for|type|tolerance)\s*:\s*(.*)$")
PREDICT_TYPES = ("choice", "number", "text")
# An option starts at the left margin; an indented bullet under it is its
# note; an indented plain line carries on whichever came last (#314).
PREDICT_OPTION_RE = re.compile(r"^[-*+]\s+(.*\S)\s*$")
NOTE_LINE_RE = re.compile(r"^[ \t]+[-*+]\s+(.*\S)\s*$")
INCLUDE_RE = re.compile(r"\{\{\s*include\s*:\s*(?P<path>[^}]+?)\s*\}\}")
# A line holding only {{include: setup/x.md}}, in a page's prose. Markdown
# includes are expanded before anything else reads the page, so an included
# heading, cell or block is the page's own; a .py include stays for a cell.
PROSE_INCLUDE_RE = re.compile(
    r"^\{\{\s*include\s*:\s*(?P<path>[^}]+?\.md)\s*\}\}[ \t]*$", re.MULTILINE)
# {{snapshot: life-expectancy}}: the date that dataset's copy was saved (#324).
SNAPSHOT_RE = re.compile(r"\{\{\s*snapshot\s*:\s*(?P<name>[^}]+?)\s*\}\}")
TIGHT_LIST_RE = re.compile(
    r"(?m)^(?P<prose>(?![ \t]*(?:[-*+]|\d+[.)])\s)(?![ \t]*#)(?![ \t]*>)[^\n]*\S[^\n]*)\n"
    r"(?P<item>[ \t]*(?:[-*+]|\d+[.)])\s+\S)"
)
TUTORIAL_HREF_RE = re.compile(r'href="tutorial:(?P<slug>[^"#]+)(?:#(?P<anchor>[^"]*))?"')
ID_RE = re.compile(r'\bid="([^"]+)"')
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ALT_RE = re.compile(r"\balt\s*=", re.IGNORECASE)
DETAILS_RE = re.compile(r"<details\b[^>]*>", re.IGNORECASE)
FOLD_CLASSES = ("dl-hint", "dl-answer", "dl-why", "dl-solution")
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
    r'^ {0,3}<details\b(?![^>\n]*\bmarkdown=)[^>\n]*>'
    r'|<(?:div|ul) class="(?:dl-hero|dl-audience|dl-attribution|dl-feature-list)">'
    r'|<aside class="dl-note" id="[^"]+">'
    r'|<div class="dl-world" data-world="[a-z0-9-]+">'
    r'|<div class="dl-project" data-project="[a-z0-9-]+">',
    re.MULTILINE,
)
# A closer's challenge (#316): the language of each starter fence, and where
# each kind opens, relative to the site root, with its button's words.
CHALLENGE_LANGS = ("python", "html", "css", "js")
CHALLENGE_TARGETS = {
    "notebook": ("compose/notebook.html", "Open it in the Notebook"),
    "workspace": ("compose/workspace.html", "Open it in the Workspace"),
}
# A link the build writes before it knows how deep the page sits; write()
# turns it into the page's own way back to the site root.
ROOT_HREF = 'href="dlroot:'
# A task's variant for one world (#315): the opening tag on a line of its
# own, a world key from the page's `worlds:` frontmatter, and a matching
# `</div>` further down. See world_spans().
WORLD_OPEN_RE = re.compile(r'^[ \t]*<div class="dl-world" data-world="(?P<world>[^"]*)">[ \t]*$')
WORLD_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
WORLD_DIV_RE = re.compile(r'<div class="dl-world" data-world="(?P<world>[a-z0-9-]+)">')
# One project of a "choose your project" page: the
# opening tag on a line of its own, an id from the page's `projects:`
# frontmatter, and a matching `</div>`. See project_spans().
PROJECT_OPEN_RE = re.compile(r'^[ \t]*<div class="dl-project" data-project="(?P<project>[^"]*)">[ \t]*$')
PROJECT_DIV_RE = re.compile(r'<div class="dl-project" data-project="(?P<project>[a-z0-9-]+)">')
# A run of one or more adjacent card placeholders — see place_page_cards().
# Whitespace only between them: inside an md_in_html wrapper (the home
# page's dl-hero) adjacent cards come out one newline apart, not two.
CARD_RUN_RE = re.compile(r"<!--dewlab-page-card-\d+-->(?:\s*<!--dewlab-page-card-\d+-->)*")


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
    # A toolkit cell's code is loaded into every later page of its course;
    # `reference` is the complete version from its ```python
    # toolkit-reference fence, when the cell itself is a stub.
    toolkit: bool = False
    reference: str | None = None
    # The blocks attached to this cell (#312): its solutions, in source
    # order, and the one inputs block the comparison evaluates.
    solutions: list["Solution"] = field(default_factory=list)
    inputs: "Inputs | None" = None
    # The lines a ```typed block gives input() when nobody can type: the
    # comparison, and the build's run of the page and its solutions.
    typed: list[str] | None = None
    # `tests: <cell id>` on a cell of the reader's own tests names the cell
    # they test; `tested_by` is the other end, set on that cell.
    tests_for: str | None = None
    tested_by: str | None = None
    predict: "Predict | None" = None
    # The world variant this cell sits in (#315), and which run of adjacent
    # variants that is: None for a cell every reader sees.
    world: str | None = None
    world_group: int | None = None

    @property
    def toolkit_reference(self) -> str:
        """What a later page loads when the reader's own version is not
        used: the reference fence, or the cell's own code without one."""
        return self.reference if self.reference is not None else self.code


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
class Solution:
    """A ```solution fence: one way to do a cell's task, with notes."""

    cell: str
    title: str
    code: str
    notes: str = ""
    # What the fold shows when `code` is more than the reader should read:
    # a `needs:` file is run first, so it is in `code`, but it is not here.
    shown: str = ""


@dataclass
class PredictOption:
    """One option of a choice prediction, and the note naming the thinking
    that leads to it. Neither is ever marked right or wrong."""

    text: str
    note: str = ""


@dataclass
class Predict:
    """A ```predict fence: the reader's guess, written before the cell runs."""

    cell: str
    type: str
    prompt: str
    options: list[PredictOption] = field(default_factory=list)
    tolerance: float | None = None


@dataclass
class Case:
    """One line of an ```inputs fence: an expression, and what it is for."""

    expr: str
    label: str | None = None


@dataclass
class Inputs:
    """An ```inputs fence: the cases a comparison evaluates on both sides."""

    cell: str
    cases: list[Case]
    guess: bool = False


@dataclass
class Typed:
    """A ```typed fence: the lines `input()` reads, in order, wherever
    nobody can type them."""

    cell: str
    lines: list[str]


@dataclass
class Challenge:
    """A page closer's challenge (#316): a ```python challenge fence, which
    opens in the Notebook, or adjacent ```html/css/js challenge fences, one
    starter the Workspace opens as a site. `parts` maps each language to
    its starter code."""

    target: str
    parts: dict[str, str]


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
    text, not converted HTML. `answer` is the 1-based position in
    `options` of the page's own answer (the `answer:` line), shown to a
    reader only when they ask for it, and never called right (#314); unused
    (0) for fill-in-the-blank, where the page's word for each {...} gap is
    read straight out of `prompt` at render time instead. `notes` holds,
    per option, the line naming the thinking that leads to it, or "" for
    an option without one."""

    id: str
    type: str
    prompt: str
    options: list[str] = field(default_factory=list)
    answer: int = 0
    notes: list[str] = field(default_factory=list)


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
    # A "choose your project" page's projects, each with the ids of the
    # cells inside it, in source order. Empty on most pages.
    project_cells: dict[str, list[str]] = field(default_factory=dict)
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
        here = cfg.OUT / "tutorials"
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
        return tuple(dict.fromkeys(listed_ids(self.meta.get("practice_across"))))

    @property
    def is_practice(self) -> bool:
        """Whether this page sets problems rather than teaching."""
        return bool(self.practice_for or self.practice_across)

    @property
    def context_for(self) -> tuple[str, ...]:
        """The slugs a context page is background reading for, or ().

        A context page holds what a tutorial does not need a reader to
        finish it: where the idea is used, why things behave as they do,
        history, the deeper detail. Mechanically it is a practice page's
        shape — off the reading order, no coverage, hanging off the
        tutorial(s) it names, which link to it in turn.
        """
        return tuple(dict.fromkeys(listed_ids(self.meta.get("context_for"))))

    @property
    def is_context(self) -> bool:
        """Whether this page is optional background reading."""
        return bool(self.context_for)

    @property
    def is_companion(self) -> bool:
        """Whether this page sits beside a tutorial rather than on the
        route: a page of problems or a context page. The gate for "not a
        teaching page" — the search index, the series, coverage."""
        return self.is_practice or self.is_context

    @property
    def owners(self) -> tuple[str, ...]:
        """The tutorial(s) a companion page belongs to, first one first;
        () for a tutorial."""
        if self.practice_for:
            return (self.practice_for,)
        return self.practice_across or self.context_for

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
        return len(self.out_path.relative_to(cfg.OUT).parts) - 1


def fail(path: Path, message: str) -> None:
    """Raises a `BuildError` naming which file the problem is in, using a
    path relative to the repository root rather than a full absolute path
    — shorter, and the same no matter whose computer the build runs on.
    Every validation check throughout this file calls this instead of
    raising directly, so every build failure reads in the same
    "file: what's wrong" shape.
    """
    raise BuildError(f"{path.relative_to(cfg.ROOT)}: {message}")


def listed_ids(value) -> list[str]:
    """The ids a frontmatter field names, from one id or a list, as written:
    a repeat is still in it, so the caller can say so."""
    if not value:
        return []
    if isinstance(value, str):
        value = [value]
    return [str(item) for item in value]


_NOTED: set[tuple[str, str]] = set()


# What the build says it carried on despite. A command-line build gathers it
# and prints it once, after the summary and where it will be seen, instead of
# among a thousand lines of progress; anything else (a test, a script that
# imports build) gets each line as it happens.
_NOTE_LINES: list[str] = []


def say(line: str) -> None:
    """One note line: printed now, or kept for main() to print at the end."""
    if cfg.NOTES_AT_END:
        _NOTE_LINES.append(line)
    else:
        print(line, file=sys.stderr)


@contextlib.contextmanager
def collecting_notes():
    """Keep every note for the caller to read while inside the block, instead
    of printing it: what check.py turns into its Note lines. The way notes
    were handled before is put back afterwards."""
    before = cfg.NOTES_AT_END
    cfg.NOTES_AT_END = True
    _NOTED.clear()
    _NOTE_LINES.clear()
    try:
        yield
    finally:
        cfg.NOTES_AT_END = before


def note(path: Path, message: str) -> None:
    """Tells the author something the build is carrying on in spite of.

    For a rule about how a page is shaped, as opposed to one whose breaking
    would leave a reader with a page that does not work. The page builds
    and the note goes to stderr in the same "file: what" shape `fail()`
    uses.
    """
    key = (str(path), message)
    if key in _NOTED:
        return
    _NOTED.add(key)
    say(f"note: {path.relative_to(cfg.ROOT)}: {message}")


SHELL_TOKEN_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")


def fill_shell(shell: str, tokens: dict[str, str], subject: str) -> str:
    """The shell template with each token's value put in, in `tokens` order
    (a value may carry a token that a later entry fills).

    Refuses when the shell holds a token this page has no value for, which
    is a mistake in the build and would show up as raw `{{NAME}}` on the
    page. It looks at the shell and not at the finished page: a title, a
    sentence or a cell the author wrote may well contain `{{`, in a Python
    f-string or an example of a template, and that is theirs to write.
    """
    unfilled = sorted(set(SHELL_TOKEN_RE.findall(shell)) - set(tokens))
    if unfilled:
        raise BuildError(f"shell template has tokens {subject} does not fill: {unfilled}")
    page = shell
    for token, value in tokens.items():
        page = page.replace(token, value)
    return page


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
    missing = [f for f in REQUIRED_FRONTMATTER if f != "title" and not meta.get(f)]
    if missing:
        today = datetime.date.today()
        fail(path, f"frontmatter is missing {', '.join(missing)}"
                   + (f" — for a new page, write `version: {today.year}.{today.month:02d}.{today.day:02d}.1`"
                      if "version" in missing else ""))
    if not meta.get("title"):
        # A title is the page's name, and one left off (or left empty, which
        # YAML reads as None and a page would print as "None") is a page
        # still being written, not one to stop the build over.
        meta["title"] = id_of(path).replace("-", " ").capitalize()
        note(path, f"has no `title:`, so the page is called {meta['title']!r}. Add one to the "
                   "frontmatter")
    for field_name, where_now in MOVED_FRONTMATTER.items():
        if field_name in meta:
            note(path, f"{field_name} no longer belongs in frontmatter — "
                       f"{where_now}. The build ignores it; delete the line.")
    status = meta.get("status", "live")
    if status not in STATUSES:
        fail(path, f"status {status!r} is not one of {', '.join(STATUSES)}")
    version = str(meta.get("version", ""))
    if not VERSION_RE.match(version):
        today = datetime.date.today()
        fail(path, f"version {version!r} is not a release date — it should look "
                   f"like {today.year}.{today.month:02d}.{today.day:02d}.1 (year, month, day, "
                   "which release of that day; that one is today's first)")
    return meta, body.lstrip("\n")


def loosen_tight_lists(body: str) -> str:
    """Give a list that starts straight after a paragraph the blank line it needs."""
    previous = None
    while previous != body:
        previous = body
        body = TIGHT_LIST_RE.sub(lambda m: f"{m.group('prose')}\n\n{m.group('item')}", body)
    return body


def _included_text(rel: str, path: Path) -> str:
    """The contents of an included file, named relative to the repository."""
    rel = rel.strip()
    target = (cfg.ROOT / rel).resolve()
    if not str(target).startswith(str(cfg.ROOT)):
        fail(path, f"include escapes the repository: {rel}")
    if not target.is_file():
        fail(path, f"include names a file that does not exist: {rel}")
    return target.read_text().strip("\n")


def expand_includes(code: str, path: Path) -> str:
    """Replace {{include: setup/x.py}} with the contents of that file.

    De-duplicates the source, not the runtime: the expanded cell still
    executes on every page load.
    """
    return INCLUDE_RE.sub(lambda match: _included_text(match.group("path"), path), code)


def expand_prose_includes(body: str, path: Path) -> str:
    """Replace a line holding only {{include: setup/x.md}} with that file.

    For prose two pages share word for word, such as what to do when a cell
    fails. The included markdown becomes part of the page before it is
    parsed, so its headings, cells and blocks are the page's own. It is
    not expanded again: an include inside an include is left as written.
    """
    body = PROSE_INCLUDE_RE.sub(lambda match: _included_text(match.group("path"), path), body)
    for match in INCLUDE_RE.finditer(body):
        if match.group("path").strip().endswith(".md"):
            fail(path, f"{match.group(0)} shares its line with other text; a markdown "
                       "include has to be a line of its own")
    return body


def expand_snapshot_dates(body: str, meta: dict, path: Path) -> str:
    """Replace {{snapshot: name}} with the date that dataset's copy was
    saved, as "26 September 2026".

    A page that quotes numbers from a dataset says which copy they came
    from (#324), and the date is read from `data/<name>.yaml`, so a
    refreshed snapshot cannot leave a page naming the old one. The dataset
    has to be one the page declares.
    """
    declared = meta.get("datasets") or []
    if isinstance(declared, str):
        declared = [declared]

    def one(match: re.Match) -> str:
        name = match.group("name")
        if name not in declared:
            note(path, f"{match.group(0)} names a dataset that datasets: does not list, so a "
                       "downloaded copy of the page will not carry it")
        if not (cfg.DATA / f"{name}.yaml").is_file():
            fail(path, f"{match.group(0)} names a dataset with no data/{name}.yaml, so "
                       "there is no saved date to put here")
        data = read_dataset(name)
        if data is None:
            fail(path, f"{match.group(0)} names a dataset with no snapshot date in "
                       f"data/{name}.yaml, so there is no saved date to put here")
        return long_date(datetime.date.fromisoformat(data["snapshot"]))

    return SNAPSHOT_RE.sub(one, body)


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
    toolkit = False
    if "toolkit" in header:
        value = header["toolkit"].lower()
        if value not in TOOLKIT_VALUES:
            fail(path, f"cell {header['id']!r} says `toolkit: {header['toolkit']}` — "
                       "write `toolkit: yes` or leave the line out")
        toolkit = TOOLKIT_VALUES[value]
        if toolkit and cell_type != "python":
            fail(path, f"cell {header['id']!r} is a {cell_type} cell; only a Python "
                       "cell can be a toolkit cell")
    code = expand_includes("\n".join(lines).strip("\n"), path)
    return Cell(
        id=header["id"],
        hint=header.get("hint") or None,
        code=code,
        expect=header.get("expect") or None,
        name=header.get("name") or None,
        type=cell_type,
        toolkit=toolkit,
        tests_for=header.get("tests") or None,
    )


def _block_header(lines: list[str], pattern: re.Pattern) -> dict[str, str]:
    """Read `key: value` lines off the top of a block fence, as hints do:
    the first line that is not one, or repeats a key, ends the header."""
    header: dict[str, str] = {}
    while lines:
        match = pattern.match(lines[0])
        if not match or match.group(1) in header:
            break
        header[match.group(1)] = match.group(2).strip()
        lines.pop(0)
    return header


def parse_solution(body: str, path: Path, previous_cell: str | None) -> Solution | None:
    """A ```solution fence: `for:` and `title:`, then Python, then
    optionally a `---` line and markdown notes. The code has to compile,
    so a typo in a solution fails the build, not a reader's comparison."""
    lines = body.split("\n")
    header = _block_header(lines, SOLUTION_HEADER_RE)
    cell = header.get("for") or previous_cell
    if not cell:
        fail(path, "a solution fence has no exec cell above it and no `for:` "
                   "line naming one")
    code, notes = _split_solution("\n".join(lines))
    code = expand_includes(code.strip("\n"), path)
    shown = ""
    if header.get("needs"):
        # Setup the solution runs on, kept out of the fold: the reader has
        # these functions already, from this page and the pages before it.
        setup = "\n".join(_included_text(rel, path) for rel in header["needs"].split(","))
        shown = code
        code = f"{setup}\n\n{code}" if code.strip() else code
    if not code.strip():
        note(path, f"the solution for cell {cell!r} has no code in it, so it is left out")
        return None
    try:
        compile(code, f"<the solution for {cell}>", "exec",
                flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    except SyntaxError as exc:
        fail(path, f"the solution for cell {cell!r} is not valid Python: "
                   f"{exc.msg} (line {exc.lineno} of the solution)")
    notes = notes.strip("\n")
    if notes:
        no_footnotes_in(notes, path, f"the solution for cell {cell!r}")
    return Solution(cell=cell, title=header.get("title") or DEFAULT_SOLUTION_TITLE,
                    code=code, notes=notes, shown=shown)


def _split_solution(text: str) -> tuple[str, str]:
    """The code before a solution's `---` line, and the notes after it."""
    match = SOLUTION_NOTES_RE.search(text)
    if not match:
        return text, ""
    return text[:match.start()], text[match.end():]


def parse_predict(body: str, path: Path, previous_cell: str | None) -> Predict:
    """A ```predict fence: `for:`, `type:` and `tolerance:`, then the
    question, then for a choice the options as a list at the left margin.
    An indented bullet under an option is its note (options_and_notes()).
    `type:` defaults to `choice` when there is a list and `text` when
    there is not."""
    lines = body.split("\n")
    header = _block_header(lines, PREDICT_HEADER_RE)
    cell = header.get("for") or previous_cell
    if not cell:
        fail(path, "a predict fence has no exec cell above it and no `for:` "
                   "line naming one")
    first_option = next((i for i, line in enumerate(lines) if PREDICT_OPTION_RE.match(line)),
                        None)
    inferred = "choice" if first_option is not None else "text"
    kind = (header.get("type") or inferred).lower()
    if kind not in PREDICT_TYPES:
        note(path, f"the prediction for cell {cell!r} says `type: {kind}`, which is not one of "
                   f"{', '.join(PREDICT_TYPES)}, so it is read as `{inferred}`")
        kind = inferred
    options: list[PredictOption] = []
    prompt_lines = lines
    if kind == "choice" and first_option is None:
        note(path, f"the prediction for cell {cell!r} is a choice with no options, so it "
                   "asks for a typed guess instead. List options with `- ` at the left margin")
        kind = "text"
    if kind == "choice":
        prompt_lines = lines[:first_option]
        texts, notes, stray = options_and_notes(lines[first_option:])
        if stray:
            fail(path, f"the prediction for cell {cell!r} has a line after its "
                       f"options that is neither an option nor indented under one: "
                       f"{stray[0].strip()!r}")
        options = [PredictOption(text=text, note=note) for text, note in zip(texts, notes)]
        if len(options) < 2:
            note(path, f"the prediction for cell {cell!r} offers one option, so a "
                       "reader cannot guess wrong; it builds as written")
    tolerance = None
    if "tolerance" in header and kind != "number":
        note(path, f"the prediction for cell {cell!r} has a tolerance, which only a "
                   "`type: number` prediction uses; it is ignored")
    elif "tolerance" in header:
        try:
            tolerance = float(header["tolerance"])
        except ValueError:
            note(path, f"the prediction for cell {cell!r} says `tolerance: "
                       f"{header['tolerance']}`, which is not a number, so a guess "
                       "has to match exactly")
        if tolerance is not None and tolerance < 0:
            note(path, f"the prediction for cell {cell!r} has a negative tolerance, "
                       "so a guess has to match exactly")
            tolerance = None
    prompt = "\n".join(prompt_lines).strip("\n")
    if not prompt.strip():
        note(path, f"the prediction for cell {cell!r} asks no question; the reader "
                   "gets the box with nothing above it")
    for text in [prompt] + [o.text for o in options] + [o.note for o in options]:
        no_footnotes_in(text, path, f"the prediction for cell {cell!r}")
    return Predict(cell=cell, type=kind, prompt=prompt, options=options, tolerance=tolerance)


def parse_inputs(body: str, path: Path, previous_cell: str | None) -> Inputs | None:
    """An ```inputs fence: `for:` and `guess:`, then one expression per
    line. A `#` comment after an expression is its label, found with the
    tokenizer so a `#` inside a string is not mistaken for one. Every
    expression has to compile; one that names something the page never
    defines is caught when the build runs the solution (check_solutions)."""
    lines = body.split("\n")
    header = _block_header(lines, INPUTS_HEADER_RE)
    cell = header.get("for") or previous_cell
    if not cell:
        fail(path, "an inputs fence has no exec cell above it and no `for:` "
                   "line naming one")
    guess = header.get("guess", "no").lower()
    if guess not in TOOLKIT_VALUES:
        note(path, f"the inputs for cell {cell!r} say `guess: {header['guess']}`, which "
                   "is not yes or no, so the reader is not asked to guess")
        guess = "no"
    cases: list[Case] = []
    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        expr, label = line, None
        try:
            for token in tokenize.generate_tokens(io.StringIO(line).readline):
                if token.type == tokenize.COMMENT:
                    expr = line[:token.start[1]]
                    label = token.string[1:].strip() or None
                    break
        except (tokenize.TokenError, SyntaxError):
            pass
        expr = expr.strip()
        try:
            compile(expr, "<input>", "eval", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        except SyntaxError:
            fail(path, f"an input for cell {cell!r} is not a Python expression: {expr}")
        cases.append(Case(expr=expr, label=label))
    if not cases:
        note(path, f"the inputs for cell {cell!r} list no cases, so the block is left out")
        return None
    return Inputs(cell=cell, cases=cases, guess=TOOLKIT_VALUES[guess])


def parse_typed(body: str, path: Path, previous_cell: str | None) -> Typed | None:
    """A ```typed fence: `for:`, then one line for each time `input()`
    reads, kept exactly as written, spaces included, since a program that
    strips what it is given is one worth testing. A blank line between two
    others is an empty line typed; blank lines at either end are not."""
    lines = body.split("\n")
    header = _block_header(lines, TYPED_HEADER_RE)
    cell = header.get("for") or previous_cell
    if not cell:
        fail(path, "a typed fence has no exec cell above it and no `for:` "
                   "line naming one")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        note(path, f"the typed block for cell {cell!r} has no lines in it, so it is left out")
        return None
    return Typed(cell=cell, lines=lines)


def parse_toolkit_reference(body: str, path: Path) -> tuple[str, str]:
    """A ```python toolkit-reference fence: its `for:` line, naming the
    toolkit cell it completes, and the code under it. Never shown to a
    reader — extract_blocks() leaves nothing of it on the page."""
    lines = body.split("\n")
    match = TOOLKIT_REFERENCE_HEADER_RE.match(lines[0]) if lines else None
    if not match or not match.group(1).strip():
        fail(path, "a toolkit-reference fence needs a `for:` line first, naming "
                   "the toolkit cell it completes")
    return match.group(1).strip(), expand_includes("\n".join(lines[1:]).strip("\n"), path)


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
    runtime knows (`TRIGGER_KEYS`). A line with a term that is not, or that
    says nothing, is the educator's typo in an optional setting, not a reason
    to stop the build: the hint takes the default trigger instead, the whole
    line replaced and not only the bad term, since "3 errors and a typo" is
    not "3 errors", and the build says so.
    """
    terms = []
    for raw in re.split(r"\s*(?:,|\band\b|&)\s*", text.strip().lower()):
        if not raw:
            continue
        if raw in BARE_TRIGGERS:
            terms.append(f"{TRIGGER_KEYS[raw]}:1")
            continue
        match = TRIGGER_TERM_RE.match(raw)
        if not match:
            return _default_trigger(path, f"has a term I cannot read: {raw!r}")
        key = match.group("k1") or match.group("k2")
        count = int(match.group("n1") or match.group("n2"))
        canonical = TRIGGER_KEYS.get(key.strip())
        if canonical is None:
            return _default_trigger(
                path, f"names a signal the runtime does not track: {key!r}. It tracks "
                      "errors, identical errors, unchanged runs, runs, empty results, "
                      "minutes, unsure and guess differed")
        if count < 1:
            note(path, f"a hint's after: count is {count}, so the hint opens after the "
                       "first counted run that does not reach the goal")
            count = 0
        terms.append(f"{canonical}:{count}")
    if not terms:
        return _default_trigger(path, "says nothing")
    return " ".join(terms)


def _default_trigger(path: Path, why: str) -> str:
    note(path, f"a hint's after: line {why}, so the hint opens at the default "
               f"({DEFAULT_HINT_AFTER.replace(':', ' ')}) instead")
    return parse_trigger(DEFAULT_HINT_AFTER, path)


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
    a `dl-hint`/`dl-answer`/`dl-why` fold and a `dl-note` aside are all part of the
    page's own single conversion pass (mark_markdown_wrappers()), so a
    footnote works in any of those.
    """
    if FOOTNOTE_TOKEN_RE.search(INLINE_CODE_RE.sub("``", text)):
        fail(path, f"{what} has a footnote in it. A fence is converted on its own, "
                   "so a footnote written here cannot reach the foot of the page — "
                   "put it in the page's own prose instead, or write `\\[^` to mean "
                   "a literal bracket")


def parse_hint(body: str, path: Path, previous_cell: str | None) -> StagedHint | None:
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
        note(path, f"the hint for cell {cell!r} has no text in it, so it is left out")
        return None
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


def render_solution(solution: Solution, maths: list[Math]) -> str:
    """The fold a ```solution fence becomes: closed until the reader opens
    it, holding the code (read-only, highlighted like any illustrative
    block) and the notes under it. Its notes' maths joins the page's list,
    the way a staged hint's does (render_staged_hint())."""
    safe_cell = html.escape(solution.cell, quote=True)
    notes_html = ""
    if solution.notes:
        stripped, _ = extract_math(solution.notes, maths)
        notes_html, _ = to_html(loosen_tight_lists(stripped))
    return (
        f'<details class="dl-solution" data-cell="{safe_cell}">'
        f"<summary>{html.escape(solution.title)}</summary>\n"
        f"{render_code_block(CodeBlock(language='python', code=solution.shown or solution.code))}\n"
        f"{notes_html}\n"
        "</details>"
    )


def _inline(text: str) -> str:
    """Markdown for one line of a block, as inline HTML: a single
    paragraph's own <p> unwrapped, as a question's option is."""
    converted = convert_prose_with_math(text)
    if converted.startswith("<p>") and converted.endswith("</p>") and converted.count("<p>") == 1:
        return converted[len("<p>"):-len("</p>")]
    return converted


def render_predict(prediction: Predict) -> str:
    """The guess a ```predict fence becomes, drawn above its cell (#313).

    The question, then a way to answer it (radio buttons for a choice, a
    box for a number or a sentence), then how sure the reader is: sure, a
    hunch, or not sure yet. Nothing here, and nothing the runtime adds
    after a run, calls an answer right or wrong. Each option's note waits
    in a hidden list until the cell has run, when the page shows the note
    for the option the reader chose."""
    safe_cell = html.escape(prediction.cell, quote=True)
    tolerance = (f' data-tolerance="{prediction.tolerance:g}"'
                 if prediction.tolerance is not None else "")
    if prediction.type == "choice":
        choices = "".join(
            f'<label class="dl-predict-option"><input type="radio" '
            f'name="dl-predict-{safe_cell}" value="{index}"> '
            f'<span class="dl-predict-option-text">{_inline(option.text)}</span></label>'
            for index, option in enumerate(prediction.options)
        )
        answer = (f'<div class="dl-predict-options" role="radiogroup" '
                  f'aria-label="Your guess">{choices}</div>')
    else:
        mode = ' inputmode="decimal"' if prediction.type == "number" else ""
        answer = (f'<input type="text" class="dl-predict-value"{mode} '
                  'aria-label="Your guess" placeholder="Your guess">')
    notes = "".join(
        f'<div class="dl-predict-note" data-option="{index}" hidden>{_inline(option.note)}</div>'
        for index, option in enumerate(prediction.options) if option.note
    )
    sure = "".join(
        f'<button type="button" class="dl-predict-sure-btn" data-sure="{key}" '
        f'aria-pressed="false">{label}</button>'
        for key, label in (("sure", "Sure"), ("hunch", "A hunch"),
                           ("unsure", "I\u2019m not sure yet"))
    )
    return (
        f'<div class="dl-predict" id="dl-predict-{safe_cell}" data-cell="{safe_cell}" '
        f'data-type="{prediction.type}"{tolerance}>'
        f'<div class="dl-predict-prompt">{convert_prose_with_math(prediction.prompt)}</div>'
        f"{answer}"
        '<div class="dl-predict-sure" role="group" aria-label="How sure are you?">'
        '<span class="dl-predict-sure-label">How sure are you?</span>'
        f"{sure}</div>"
        '<div class="dl-predict-unsure" hidden>'
        "<p>That is a good place to start. "
        '<span class="dl-predict-hint-open" hidden>The first hint under the cell '
        "is open now. </span>Two ways on:</p>"
        '<button type="button" class="dl-btn dl-predict-guess-now">Make a guess now</button> '
        '<button type="button" class="dl-btn dl-predict-run">Run it and see</button>'
        "</div>"
        '<p class="dl-predict-footer">Guess first, or just run it.</p>'
        '<div class="dl-predict-after" hidden aria-live="polite">'
        '<div class="dl-predict-sides">'
        '<div><span class="dl-predict-side-label">Your guess</span>'
        '<span class="dl-predict-your"></span></div>'
        '<div><span class="dl-predict-side-label">What the cell printed</span>'
        '<span class="dl-predict-output"></span></div>'
        "</div>"
        '<p class="dl-predict-match" hidden>Your guess and the output match.</p>'
        f"{notes}"
        '<p class="dl-predict-which" hidden>Which line explains what you saw?</p>'
        "</div>"
        "</div>"
    )


# The end of a page with predict blocks (#313): the cells where the
# reader's guess and the output differed, and the ones they were not sure
# about. The runtime fills the list, and shows the section once it has
# something in it.
SURPRISES_HTML = (
    '<section class="dl-surprises" hidden aria-labelledby="dl-surprises-heading">'
    '<h2 id="dl-surprises-heading">Your surprises</h2>'
    "<p>The cells where your guess and the output differed, and the ones you "
    "were not sure about yet. They are worth a second look.</p>"
    '<ul class="dl-surprises-list"></ul>'
    "</section>"
)


def render_typed(lines: list[str]) -> str:
    """The line under a comparison that says what it types for `input()`,
    so a reader can see where their code's answers came from."""
    shown = " ".join(
        f"<code>{html.escape(line)}</code>" if line else "(an empty line)"
        for line in lines
    )
    return (
        '<p class="dl-compare-typed">Nobody can type during the comparison. '
        "When the code calls <code>input()</code>, the comparison types these "
        f"lines, in order, and each case starts again at the first: {shown}</p>"
    )


def render_inputs(block: Inputs, has_solution: bool, typed: list[str] | None = None) -> str:
    """The comparison table an ```inputs fence becomes (#312).

    Each case is a row. The reader's column, and the solution's when the
    cell has one, are empty until the reader asks for the comparison; the
    runtime fills them. With `guess: yes`, a column of text boxes comes
    first, for what the reader expects each case to give. Nothing in the
    table says right or wrong: a row where the two sides differ is marked
    "different", in words as well as colour. A cell with a ```typed block
    says under the table what the comparison types."""
    safe_cell = html.escape(block.cell, quote=True)
    heads = ['<th scope="col">Input</th>']
    if block.guess:
        heads.append('<th scope="col">Your guess</th>')
    heads.append('<th scope="col">Your code</th>')
    if has_solution:
        heads.append('<th scope="col">A solution</th>')
    rows = []
    for index, case in enumerate(block.cases):
        label = (f' <span class="dl-compare-label">{html.escape(case.label)}</span>'
                 if case.label else "")
        cells_html = [f'<td class="dl-compare-input"><code>{html.escape(case.expr)}</code>{label}</td>']
        if block.guess:
            cells_html.append(
                f'<td class="dl-compare-guess"><input type="text" '
                f'aria-label="Your guess for {html.escape(case.expr, quote=True)}"></td>'
            )
        cells_html.append('<td class="dl-compare-yours"></td>')
        if has_solution:
            cells_html.append('<td class="dl-compare-theirs"></td>')
        rows.append(f'<tr data-case="{index}">{"".join(cells_html)}</tr>')
    label = "Compare with a solution" if has_solution else "Try these on your code"
    return (
        f'<div class="dl-compare" data-cell="{safe_cell}">'
        '<table class="dl-compare-table">'
        "<caption>Cases to try</caption>"
        f'<thead><tr>{"".join(heads)}</tr></thead>'
        f'<tbody>{"".join(rows)}</tbody>'
        "</table>"
        f'{render_typed(typed) if typed else ""}'
        '<div class="dl-compare-actions">'
        f'<button type="button" class="dl-btn dl-btn-compare">{label}</button>'
        '<span class="dl-compare-status" role="status"></span>'
        "</div>"
        "</div>"
    )


def place_cell_blocks(page_html: str, solutions: list[Solution], inputs_blocks: list[Inputs],
                      cells: list[Cell], maths: list[Math]) -> str:
    """Swap each solution's and inputs block's placeholder for its markup.
    Run before place_blocks(), like place_hints(), so the maths a
    solution's notes add is still there to render."""
    has_solution = {cell.id for cell in cells if cell.solutions}
    typed = {cell.id: cell.typed for cell in cells if cell.typed}
    for index, solution in enumerate(solutions):
        placeholder = f"<!--dewlab-solution-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"the solution for cell {solution.cell!r} was lost during "
                             "markdown conversion")
        page_html = page_html.replace(placeholder, render_solution(solution, maths))
    for index, block in enumerate(inputs_blocks):
        placeholder = f"<!--dewlab-inputs-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"the inputs for cell {block.cell!r} were lost during "
                             "markdown conversion")
        page_html = page_html.replace(placeholder,
                                      render_inputs(block, block.cell in has_solution,
                                                    typed.get(block.cell)))
    return page_html


def options_and_notes(lines: list[str]) -> tuple[list[str], list[str], list[str]]:
    """A list of options, as a question or a prediction writes them, read
    into (options, notes, stray lines). An option is a bullet at the left
    margin. An indented bullet under it is its note: the thinking that
    leads to it. An indented plain line carries on whichever came last,
    option or note, so a long option can wrap. Anything else is returned
    as stray, for the caller to refuse or ignore."""
    options: list[str] = []
    notes: list[str] = []
    stray: list[str] = []
    last = None
    for line in lines:
        option = PREDICT_OPTION_RE.match(line)
        note = NOTE_LINE_RE.match(line)
        if option:
            options.append(option.group(1))
            notes.append("")
            last = "option"
        elif note and options:
            notes[-1] = f"{notes[-1]} {note.group(1)}".strip()
            last = "note"
        elif options and line.strip() and line[:1].isspace():
            if last == "note":
                notes[-1] = f"{notes[-1]} {line.strip()}"
            else:
                options[-1] = f"{options[-1]} {line.strip()}"
        elif line.strip():
            stray.append(line)
    return options, notes, stray


def _split_multiple_choice(text: str) -> tuple[str, list[str], list[str]]:
    """The prompt, the options under it, and each option's note: the prose
    before the first list is the question, the list is the options. The
    first bullet at the left margin starts the options, read by
    options_and_notes(): a margin bullet is an option, an indented bullet
    its note (#314), an indented plain line a wrapped continuation."""
    lines = text.split("\n")
    start = len(lines)
    for index, line in enumerate(lines):
        if PREDICT_OPTION_RE.match(line):
            start = index
            break
    prompt = "\n".join(lines[:start]).strip()
    options, notes, _ = options_and_notes(lines[start:])
    return prompt, options, notes


def find_gaps(text: str) -> list[re.Match]:
    """The {...} gaps in a fill-in-the-blank question's text, left to right.

    Braces inside $...$ or $$...$$ maths belong to the maths, so
    `$10^{-12}$` stays a power and does not become a typing box. The text
    is read in one pass: a `{` outside maths starts a gap, and a gap is
    taken whole, so a dollar sign inside one (a price offered as a choice,
    `{$5|$10}`) never opens a maths span. A `$` that opens a real maths
    span (DISPLAY_MATH_RE, INLINE_MATH_RE, the same test extract_math
    makes) skips past the span; any other `$` is a plain character.
    """
    gaps: list[re.Match] = []
    position = 0
    while position < len(text):
        char = text[position]
        if char == "$":
            maths = DISPLAY_MATH_RE.match(text, position) or INLINE_MATH_RE.match(text, position)
            position = maths.end() if maths else position + 1
        elif char == "{" and (gap := GAP_RE.match(text, position)):
            gaps.append(gap)
            position = gap.end()
        else:
            position += 1
    return gaps


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
            if depth:
                depth -= 1
            else:
                note(path, f"question {question_id!r} has a }} with no matching {{; "
                           "it shows as written")
    if depth > 0:
        note(path, f"question {question_id!r} has a {{ with no matching }}; "
                   "it shows as written")


def parse_question(body: str, path: Path) -> Question | None:
    """Read `id:`, `type:` and `answer:` off the top of a ```question
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
        note(path, f"question {question_id!r} has no text in it, so it is left out")
        return None
    no_footnotes_in(text, path, f"question {question_id!r}")

    if question_type == "multiple-choice":
        prompt, options, notes = _split_multiple_choice(text)
        if not prompt:
            note(path, f"question {question_id!r} has options but no question above them "
                       "in its fence; the reader sees only the options")
        if len(options) == 1:
            note(path, f"question {question_id!r} has one option, so a reader cannot "
                       "choose wrong; it builds as written")
        # `answer:` names the page's own answer; `correct:`, its older
        # spelling, still reads the same.
        key = "answer" if "answer" in header else "correct"
        raw_answer = header.get(key)
        if not raw_answer:
            fail(path, f"question {question_id!r} is multiple-choice and has no `answer:` line")
        if not raw_answer.isdigit() or not (1 <= int(raw_answer) <= len(options)):
            fail(path, f"question {question_id!r}'s `{key}: {raw_answer}` does not "
                       f"name one of its {len(options)} options")
        return Question(id=question_id, type=question_type, prompt=prompt,
                         options=options, answer=int(raw_answer), notes=notes)

    _check_balanced_gaps(text, path, question_id)
    if not find_gaps(text):
        fail(path, f"question {question_id!r} is fill-in-the-blank and has no {{...}} gap "
                   f"in it outside its maths")
    return Question(id=question_id, type=question_type, prompt=text)


def render_question(question: Question) -> str:
    """The markup `buildQuestions()` (tutorial-runtime.js) binds a
    "Show the page's answer" button and its feedback to.

    Nothing here is a verdict (#314). The page's own answer lives in the
    markup, on the option or gap it belongs to (`data-answer="true"`, or a
    typing gap's own `data-expected`), and the reader sees it only when
    they ask, beside their own choice: never "right", never "not yet". A
    reader who opens the page's source can read it, which is the right
    trade for a question to think with and the wrong one for an exam.
    Marking the answer instead of its position is also what lets the
    runtime shuffle the options it draws without a second, parallel record
    of which one moved where. Each option's note waits hidden in the
    feedback slot, and the runtime shows the one for the reader's choice.

    Both types share the same outer shell (a prompt, the button, a closed
    feedback slot) and differ only in what sits between: a column of
    option buttons for multiple-choice, or the prompt's own sentence with
    each {...} gap already turned into a real control for
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
            answer_attr = ' data-answer="true"' if position == question.answer else ""
            option_items.append(
                f'<button type="button" class="dl-question-option" '
                f'data-option="{position}"{answer_attr}>{option_html}</button>'
            )
        notes_html = "".join(
            f'<div class="dl-question-note" data-option="{position}" hidden>{_inline(note)}</div>'
            for position, note in enumerate(question.notes, start=1) if note
        )
        options_html = (
            '<div class="dl-question-options" role="group" '
            f'aria-label="Choose one">{"".join(option_items)}</div>'
        )
    else:
        def gap_widget(raw: str) -> str:
            choices = [c.strip() for c in raw.split("|")] if "|" in raw else None
            if choices is not None:
                # The gap starts on a blank "choose", which cannot be chosen
                # back. Without it the browser shows the first option, the
                # page's own word, and the runtime's shuffle leaves it
                # selected wherever it lands.
                option_tags = '<option value="" selected disabled>choose</option>' + "".join(
                    (f'<option data-answer="true">{html.escape(choice)}</option>' if i == 0
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
        # find_gaps() skips braces inside maths, so they stay in the text
        # and reach KaTeX as the maths' own grouping.
        found = find_gaps(question.prompt)
        gaps = [gap.group(1) for gap in found]
        tokenised = question.prompt
        for index, gap in reversed(list(enumerate(found))):
            tokenised = tokenised[:gap.start()] + f"dlgap{index}z" + tokenised[gap.end():]
        prompt_html = convert_prose_with_math(tokenised)
        for index, raw in enumerate(gaps):
            prompt_html = prompt_html.replace(f"dlgap{index}z", gap_widget(raw))
        options_html = ""
        notes_html = ""
    reveal = ("Show the page\u2019s answer" if question.type == "multiple-choice"
              else "Show the page\u2019s words")
    return (
        f'<div class="dl-question" id="dl-question-{safe_id}" '
        f'data-question-id="{safe_id}" data-question-type="{question.type}">'
        f'<div class="dl-question-prompt">{prompt_html}</div>'
        f"{options_html}"
        f'<button type="button" class="dl-btn dl-question-check" disabled>{reveal}</button>'
        '<div class="dl-question-feedback" hidden>'
        f'<p class="dl-question-same" hidden>You chose the same as the page.</p>{notes_html}</div>'
        "</div>"
    )


@dataclass
class WorldSpan:
    """One world's variant of a task (#315): where it starts and ends in the
    source, its world, and the run of adjacent variants it belongs to."""

    start: int
    end: int
    world: str
    group: int


def page_worlds(meta: dict, path: Path) -> dict[str, str]:
    """The worlds a page offers, from its `worlds:` frontmatter: each key, in
    order, with its one line. The first is the world the page teaches in."""
    worlds = meta.get("worlds")
    if worlds is None:
        return {}
    if isinstance(worlds, list) and worlds and all(isinstance(key, str) for key in worlds):
        note(path, "`worlds:` is a list of keys, so each world goes without the line that "
                   "would say what it is. Write `key: one line saying what it is` to add one")
        worlds = {key: "" for key in worlds}
    if not isinstance(worlds, dict) or not worlds:
        fail(path, "`worlds:` lists each world as `key: one line saying what it is`")
    for key, line in worlds.items():
        if not isinstance(key, str) or not WORLD_KEY_RE.match(key):
            fail(path, f"world {key!r} in `worlds:` is not a key like `sea-floor`: "
                       "lower-case letters and digits, joined by hyphens")
    # A world with no line keeps its name in the chooser and goes without
    # the sentence under it.
    return {key: str(line or "").strip() for key, line in worlds.items()}


def world_name(key: str) -> str:
    """A world's key as a reader sees it: `sea-floor` is "Sea floor"."""
    words = key.replace("-", " ")
    return words[:1].upper() + words[1:]


def world_spans(body: str, path: Path, worlds: dict[str, str]) -> list[WorldSpan]:
    """Find each `<div class="dl-world" data-world="…">` variant in a page's
    source, and the `</div>` that closes it (#315).

    Fences are blanked out first, so a `</div>` inside a code example is
    not taken for the end of a variant. A `<div>` the variant holds is
    counted, so its own `</div>` is not either. Variants separated by
    nothing but blank lines are one group: the same task, once per world."""
    masked = FENCE_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), body)
    spans: list[WorldSpan] = []
    open_span: tuple[int, str] | None = None
    depth = 0
    offset = 0
    for line in masked.splitlines(keepends=True):
        opening = WORLD_OPEN_RE.match(line.rstrip("\n"))
        if opening:
            world = opening.group("world")
            if open_span is not None:
                fail(path, f"the {world!r} variant starts inside the "
                           f"{open_span[1]!r} one — close each with </div> first")
            if not worlds:
                fail(path, "this page has world variants and no `worlds:` in its "
                           "frontmatter to say which worlds it offers")
            if world not in worlds:
                fail(path, f"a variant is for world {world!r}, which is not in "
                           f"this page's `worlds:` ({', '.join(worlds)})")
            open_span, depth = (offset, world), 1
        elif open_span is not None:
            depth += len(re.findall(r"<div\b", line)) - line.count("</div>")
            if depth <= 0:
                start, world = open_span
                end = offset + len(line)
                previous = spans[-1] if spans else None
                # The source, not the masked copy: a cell between two variants
                # is blank in the mask, and it ends the group.
                joined = previous is not None and not body[previous.end:start].strip()
                group = previous.group if joined else (previous.group + 1 if previous else 0)
                if joined and any(s.world == world and s.group == group for s in spans):
                    fail(path, f"two {world!r} variants of the same task sit side by "
                               "side — a task has one variant per world")
                spans.append(WorldSpan(start=start, end=end, world=world, group=group))
                open_span = None
        offset += len(line)
    if open_span is not None:
        fail(path, f"the {open_span[1]!r} variant has no </div> to close it")
    return spans


# A card cannot be drawn without these. `maths` and `data` only fill two
# cells of the comparison table, and a project that has none of either (a
# project that is all writing, say) leaves them blank.
PROJECT_REQUIRED = ("title", "question", "make")
PROJECT_FIELDS = PROJECT_REQUIRED + ("maths", "data")


def page_projects(meta: dict, path: Path) -> dict[str, dict]:
    """A "choose your project" page's projects, from its `projects:`
    frontmatter: each id, in order, with its title, the curious
    question its card leads with, what the reader makes, the maths and the
    data it uses, and an optional picture. `own: true` marks the project of
    the reader's own, which gets the wide card under the grid; any number of
    projects may say so and they may come in any position. `maths` and `data`
    may be left out, and so, with a note, may a project's title (it is called
    after its id), its question and what it makes (its card goes without
    them): a project still being drafted should not stop the page."""
    projects = meta.get("projects")
    if projects is None:
        return {}
    if isinstance(projects, list) and projects and all(isinstance(key, str) for key in projects):
        note(path, "`projects:` is a list of ids, so each project has no title, question "
                   "or make yet. Write `id:` with those under it to fill them in")
        projects = {key: {} for key in projects}
    if not isinstance(projects, dict) or not projects:
        fail(path, "`projects:` lists each project as `id:` with its title, "
                   "question, make, maths and data")
    found: dict[str, dict] = {}
    for key, fields in projects.items():
        if not isinstance(key, str) or not WORLD_KEY_RE.match(key):
            fail(path, f"project {key!r} in `projects:` is not an id like `best-line`: "
                       "lower-case letters and digits, joined by hyphens")
        if not isinstance(fields, dict):
            fields = {}
        fields = dict(fields)
        for name in PROJECT_REQUIRED:
            if not isinstance(fields.get(name), str) or not fields[name].strip():
                fields[name] = key.replace("-", " ").capitalize() if name == "title" else ""
                note(path, f"project {key!r} in `projects:` has no `{name}:`, so "
                           + ("it is called after its id" if name == "title"
                              else f"its card goes without the {name} line"))
        picture = fields.get("picture")
        if picture is not None and not (path.parent / str(picture)).is_file():
            fail(path, f"project {key!r}'s picture {picture!r} is not in the tutorial's folder")
        found[key] = {**{name: str(fields.get(name) or "").strip() for name in PROJECT_FIELDS},
                      "picture": picture, "own": bool(fields.get("own"))}
    return found


def project_spans(body: str, path: Path, projects: dict[str, dict]) -> dict[str, tuple[int, int]]:
    """Where each `<div class="dl-project" data-project="…">` starts and
    ends in a page's source, the way world_spans() finds a variant: fences
    blanked first, nested `<div>`s counted. Every project in `projects:`
    has exactly one. Each should open with its `##` heading, which the page
    turns into the project's open-and-close control, and appear in the order
    `projects:` lists them; a page that does neither still builds, with a
    note saying what the reader loses."""
    masked = FENCE_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), body)
    spans: dict[str, tuple[int, int]] = {}
    open_span: tuple[int, str] | None = None
    depth = 0
    offset = 0
    for line in masked.splitlines(keepends=True):
        opening = PROJECT_OPEN_RE.match(line.rstrip("\n"))
        if opening:
            project = opening.group("project")
            if open_span is not None:
                fail(path, f"project {project!r} starts inside {open_span[1]!r} — "
                           "close each with </div> first")
            if project not in projects:
                fail(path, f"a project div is for {project!r}, which is not in this "
                           f"page's `projects:` ({', '.join(projects) or 'none'})")
            if project in spans:
                fail(path, f"project {project!r} has two divs; a project has one")
            open_span, depth = (offset, project), 1
        elif open_span is not None:
            depth += len(re.findall(r"<div\b", line)) - line.count("</div>")
            if depth <= 0:
                start, project = open_span
                spans[project] = (start, offset + len(line))
                open_span = None
        offset += len(line)
    if open_span is not None:
        fail(path, f"project {open_span[1]!r} has no </div> to close it")
    missing = [key for key in projects if key not in spans]
    if missing:
        fail(path, f"`projects:` lists {', '.join(missing)} with no project div in the page")
    if list(spans) != list(projects):
        note(path, "the project divs are not in the order `projects:` lists them; "
                   "the cards and the table follow `projects:`, the sections follow the page")
    for project, (start, end) in spans.items():
        inside = body[start:end].split("\n", 1)[1].lstrip("\n")
        if not inside.startswith("## "):
            note(path, f"project {project!r} does not open with a `## ` heading, so it has "
                       "no control to open and close it. It shows nothing until a reader "
                       "opens it from its card, and cannot be closed again")
    return spans


def project_cell_ids(body: str, spans: dict[str, tuple[int, int]], cells: list[Cell]) -> dict[str, list[str]]:
    """Each project's cells, by id, for the progress counts."""
    known = {cell.id for cell in cells}
    return {
        project: [found for found in re.findall(r"^id:\s*(\S+)\s*$", body[start:end], re.M)
                  if found in known]
        for project, (start, end) in spans.items()
    }


def render_project_chooser(projects: dict[str, dict]) -> str:
    """A "choose your project" page's cards and comparison table:
    a 2×2 grid, each card led by its curious question, the reader's own
    project as a wide card under it, then the projects side by side. Each
    card is a link to its project, so without JavaScript it still takes
    the reader there."""
    def card(key: str, fields: dict) -> str:
        # A plain local name, like an author's own <img>: inline_local_svg()
        # puts an SVG's markup in its place later, decorative (alt="") since
        # the card's question says what the picture shows.
        picture = (f'<img class="dl-project-picture" src="{html.escape(str(fields["picture"]))}" alt="">'
                   if fields["picture"] else "")
        own = " dl-project-card-own" if fields["own"] else ""
        return (
            f'<a class="dl-project-card{own}" href="#project-{key}" data-project="{key}">'
            f"{picture}"
            + (f'<span class="dl-project-question">{_inline(fields["question"])}</span>'
               if fields["question"] else "")
            + f'<span class="dl-project-title">{_inline(fields["title"])}</span>'
            + (f'<span class="dl-project-make">You make: {_inline(fields["make"])}</span>'
               if fields["make"] else "")
            + "</a>"
        )

    grid = "".join(card(key, fields) for key, fields in projects.items() if not fields["own"])
    own = "".join(card(key, fields) for key, fields in projects.items() if fields["own"])
    rows = "".join(
        "<tr>"
        f'<th scope="row"><a href="#project-{key}" data-project="{key}">{_inline(fields["title"])}</a></th>'
        f'<td>{_inline(fields["question"])}</td>'
        f'<td>{_inline(fields["make"])}</td>'
        f'<td>{_inline(fields["maths"])}</td>'
        f'<td>{_inline(fields["data"])}</td>'
        "</tr>"
        for key, fields in projects.items()
    )
    return (
        '<section class="dl-project-chooser" id="dl-project-chooser" aria-labelledby="dl-project-chooser-title">'
        '<h3 id="dl-project-chooser-title">Choose a project</h3>'
        '<p class="dl-project-note">Pick the one you are most curious about. '
        "One is enough, and you can come back for another.</p>"
        f'<div class="dl-project-grid">{grid}</div>'
        f"{own}"
        '<div class="dl-table-wrap"><table class="dl-project-table">'
        "<caption>The projects side by side</caption>"
        "<thead><tr><th scope=\"col\">Project</th><th scope=\"col\">The question</th>"
        "<th scope=\"col\">You make</th><th scope=\"col\">The maths</th>"
        "<th scope=\"col\">It uses</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></div>"
        "</section>"
    )


def place_projects(body_html: str, projects: dict[str, dict], path: Path) -> str:
    """Give each project its anchor, and put the cards and table just before
    the first one."""
    if not projects:
        return body_html
    if body_html.count('<div class="dl-project"') != len(projects):
        fail(path, "a `<div class=\"dl-project\">` tag shares its line with other text — "
                   "put each opening tag on a line of its own")
    first = True

    def anchor(match: re.Match) -> str:
        nonlocal first
        key = match.group("project")
        chooser = render_project_chooser(projects) + "\n" if first else ""
        first = False
        own = ' data-project-own="true"' if projects[key]["own"] else ""
        return f'{chooser}<div class="dl-project" data-project="{key}" id="project-{key}"{own}>'

    return PROJECT_DIV_RE.sub(anchor, body_html)


def check_fences_closed(body: str, path: Path) -> None:
    """Stops the build when a ``` fence is opened and never closed.

    `FENCE_RE` only matches a fence that closes, so an unclosed one is left
    in the text and markdown reads everything after it as code: the rest of
    the page becomes one grey block, with no error to say why. A line that
    starts with ``` and sits outside every matched fence is that opener.
    This needs no judgement about what the author meant, which is why it
    refuses while the style rules around it do not.
    """
    matched = [m.span() for m in FENCE_RE.finditer(body)]
    for opener in re.finditer(r"^ *```", body, re.MULTILINE):
        if not any(start <= opener.start() < end for start, end in matched):
            line = body.count("\n", 0, opener.start()) + 1
            fail(path, f"the code fence on line {line} of the page text is opened and "
                       f"never closed, so everything after it would show as code — "
                       f"close it with a line holding only ```")


def extract_blocks(
    body: str, path: Path, spans: list[WorldSpan] | None = None,
) -> tuple[str, list[Cell], list[CodeBlock], list[StagedHint], list[SiteEditor], list[Question],
           list[AppCell], list[Solution], list[Inputs], list[Challenge]]:
    """Pull every fence out, leaving a comment placeholder markdown will keep.

    An `exec` fence becomes a cell; a `python toolkit-reference` fence
    becomes the reference code of the toolkit cell its `for:` names, and
    leaves nothing on the page; a `hint` fence becomes a staged hint;
    an `html site`/`css site`/`js site` fence
    becomes one pane of a `SiteEditor`, grouped with any of the same
    `site:` name immediately before or after it; a `question` fence
    becomes a `Question`; an `html app`/
    `css app`/`js app` fence becomes one pane of an `AppCell`, grouped
    the same way by its `app:` name; a `solution` or `inputs` fence
    becomes a block attached to its cell (#312), and a `predict` fence
    one that leaves no placeholder, since render_cell() draws it above
    its cell (#313); a `typed` fence gives its cell the lines `input()`
    reads when nobody can type, and leaves no placeholder either, since
    render_inputs() says what it types; any other fence becomes an
    illustrative, read-only block.
    All six leave the source before the markdown converter runs, so
    nothing inside any of them can be reinterpreted as markup.
    """
    check_fences_closed(body, path)
    cells: list[Cell] = []
    blocks: list[CodeBlock] = []
    hints: list[StagedHint] = []
    site_editors: list[SiteEditor] = []
    questions: list[Question] = []
    app_cells: list[AppCell] = []
    solutions: list[Solution] = []
    inputs_blocks: list[Inputs] = []
    typed_blocks: list[Typed] = []
    predictions: list[Predict] = []
    hints_per_cell: dict[str, int] = {}
    used_site_names: set[str] = set()
    current_site: SiteEditor | None = None
    last_site_pane_end = -1
    used_app_names: set[str] = set()
    current_app: AppCell | None = None
    last_app_pane_end = -1
    references: list[tuple[str, str]] = []
    challenges: list[Challenge] = []
    last_challenge_end = -1
    # Each attached block, the cell it names, and the world variant it sits
    # in, checked against its cell's once every cell is known (#315).
    placed: list[tuple[str, str, str | None]] = []

    def world_at(position: int) -> WorldSpan | None:
        return next((span for span in spans or [] if span.start <= position < span.end), None)

    def one(match: re.Match) -> str:
        nonlocal current_site, last_site_pane_end, current_app, last_app_pane_end
        nonlocal last_challenge_end
        info = match.group("info").strip().split()
        indent = match.group("indent")
        span = world_at(match.start())
        world = span.world if span else None
        if "exec" in info:
            cell_type = info[0] if info[0] != "exec" else "python"
            if cell_type not in CELL_TYPES:
                fail(path, f"an exec cell's fence starts with {cell_type!r}, "
                           f"not one of {sorted(CELL_TYPES)}")
            cell = parse_cell(match.group("body"), path, cell_type)
            if span:
                cell.world, cell.world_group = span.world, span.group
                if not cell.id.endswith(f"--{span.world}"):
                    fail(path, f"cell {cell.id!r} sits in the {span.world!r} variant, so "
                               f"its id ends in `--{span.world}`, the way switching "
                               "worlds keeps each world's saved work apart")
            cells.append(cell)
            return f"{indent}<!--dewlab-cell-{len(cells) - 1}-->"
        if "toolkit-reference" in info:
            if info[0] != "python":
                fail(path, f"a toolkit-reference fence starts with {info[0]!r}, not 'python'")
            references.append(parse_toolkit_reference(match.group("body"), path))
            return ""
        if info and info[0] == "hint":
            hint = parse_hint(match.group("body"), path, cells[-1].id if cells else None)
            if hint is None:
                return ""
            hint.index = hints_per_cell.get(hint.cell, 0)
            hints_per_cell[hint.cell] = hint.index + 1
            hints.append(hint)
            placed.append(("hint", hint.cell, world))
            return f"{indent}<!--dewlab-hint-{len(hints) - 1}-->"
        if info and info[0] == "solution":
            solution = parse_solution(match.group("body"), path,
                                      cells[-1].id if cells else None)
            if solution is None:
                return ""
            solutions.append(solution)
            placed.append(("solution", solutions[-1].cell, world))
            return f"{indent}<!--dewlab-solution-{len(solutions) - 1}-->"
        if info and info[0] == "predict":
            predictions.append(parse_predict(match.group("body"), path,
                                             cells[-1].id if cells else None))
            placed.append(("predict block", predictions[-1].cell, world))
            return ""
        if info and info[0] == "inputs":
            block = parse_inputs(match.group("body"), path, cells[-1].id if cells else None)
            if block is None:
                return ""
            inputs_blocks.append(block)
            placed.append(("inputs block", inputs_blocks[-1].cell, world))
            return f"{indent}<!--dewlab-inputs-{len(inputs_blocks) - 1}-->"
        if info and info[0] == "typed":
            typed = parse_typed(match.group("body"), path, cells[-1].id if cells else None)
            if typed is None:
                return ""
            typed_blocks.append(typed)
            placed.append(("typed block", typed_blocks[-1].cell, world))
            return ""
        if len(info) >= 2 and info[1] == "challenge":
            language = info[0]
            if language not in CHALLENGE_LANGS:
                fail(path, f"a challenge fence starts with {language!r}, not one of "
                           f"{', '.join(CHALLENGE_LANGS)}")
            code = match.group("body").strip("\n")
            target = "notebook" if language == "python" else "workspace"
            # html, css and js starters side by side are one site.
            adjacent = (
                target == "workspace" and challenges
                and challenges[-1].target == "workspace"
                and not body[last_challenge_end:match.start()].strip()
            )
            last_challenge_end = match.end()
            if adjacent:
                if language in challenges[-1].parts:
                    fail(path, f"a challenge has two {language} starters side by side")
                challenges[-1].parts[language] = code
                return ""
            challenges.append(Challenge(target=target, parts={language: code}))
            return f"{indent}<!--dewlab-challenge-{len(challenges) - 1}-->"
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
            question = parse_question(match.group("body"), path)
            if question is None:
                return ""
            questions.append(question)
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
    by_id = {cell.id: cell for cell in cells}
    for target, code in references:
        cell = by_id.get(target)
        if cell is None:
            fail(path, f"a toolkit-reference fence is for {target!r}, and this "
                       "tutorial has no cell with that id")
        if not cell.toolkit:
            fail(path, f"a toolkit-reference fence is for {target!r}, which is not "
                       "a toolkit cell — add `toolkit: yes` to it")
        if cell.reference is not None:
            fail(path, f"cell {target!r} has two toolkit-reference fences")
        cell.reference = code
    for editor in site_editors:
        for pane in editor.panes.values():
            if pane.id in seen:
                fail(path, f"two cells share the id {pane.id!r}")
            seen.add(pane.id)
    for hint in hints:
        if hint.cell not in seen:
            fail(path, f"a hint names a cell this tutorial does not have: {hint.cell!r}")
    for solution in solutions:
        cell = by_id.get(solution.cell)
        if cell is None:
            fail(path, f"a solution names a cell this tutorial does not have: {solution.cell!r}")
        if cell.type != "python":
            fail(path, f"cell {cell.id!r} is a {cell.type} cell; only a Python cell "
                       "can have a solution")
        cell.solutions.append(solution)
    for block in inputs_blocks:
        cell = by_id.get(block.cell)
        if cell is None:
            fail(path, f"an inputs block names a cell this tutorial does not have: {block.cell!r}")
        if cell.type != "python":
            fail(path, f"cell {cell.id!r} is a {cell.type} cell; only a Python cell "
                       "can have inputs")
        if cell.inputs is not None:
            fail(path, f"cell {cell.id!r} has two inputs blocks — put every case in one")
        cell.inputs = block
    for block in typed_blocks:
        cell = by_id.get(block.cell)
        if cell is None:
            fail(path, f"a typed block names a cell this tutorial does not have: {block.cell!r}")
        if cell.type != "python":
            fail(path, f"cell {cell.id!r} is a {cell.type} cell; only a Python cell "
                       "can have typed lines")
        if cell.typed is not None:
            note(path, f"cell {cell.id!r} has two typed blocks, so their lines are read "
                       "one after the other")
            cell.typed = [*cell.typed, *block.lines]
        else:
            cell.typed = block.lines
    for prediction in predictions:
        cell = by_id.get(prediction.cell)
        if cell is None:
            fail(path, f"a prediction names a cell this tutorial does not have: "
                       f"{prediction.cell!r}")
        if cell.predict is not None:
            note(path, f"cell {cell.id!r} has two predict blocks, and a cell takes one "
                       "guess, so the second is left out")
            continue
        cell.predict = prediction
    def where(world: str | None) -> str:
        return f"in the {world!r} variant" if world else "outside every world variant"

    for kind, cell_id, world in placed:
        cell = by_id.get(cell_id)
        if cell is not None and cell.world != world:
            fail(path, f"a {kind} {where(world)} belongs to cell {cell_id!r}, which is "
                       f"{where(cell.world)} — a block shows and hides with its cell's world")
    for cell in cells:
        if not cell.tests_for:
            continue
        target = by_id.get(cell.tests_for)
        if target is None or target is cell:
            fail(path, f"cell {cell.id!r} says `tests: {cell.tests_for}`, and this "
                       "tutorial has no other cell with that id")
        if target.world != cell.world:
            fail(path, f"cell {cell.id!r} tests {target.id!r}, and the two are in "
                       f"different worlds ({where(cell.world)}, {where(target.world)})")
        if target.tested_by:
            fail(path, f"cells {target.tested_by!r} and {cell.id!r} both say they test "
                       f"{target.id!r} — one cell of tests per cell")
        target.tested_by = cell.id
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
    return (rewritten, cells, blocks, hints, site_editors, questions, app_cells,
            solutions, inputs_blocks, challenges)


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
        (render_predict(cell.predict) if cell.predict else "")
        + f'<div class="dl-cell" data-cell-id="{safe_id}">'
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


def render_challenge(challenge: Challenge, page: str, title: str) -> str:
    """A closer's challenge (#316): its starter, read-only, and a link that
    opens it in the Notebook or the Workspace as a new file named after the
    page. The starter travels in the link's own address (`#challenge=`, a
    JSON object), so opening it needs nothing from this page but the click,
    and the Notebook or Workspace decides where it goes: a new tab, never
    over one. On a downloaded page, with neither beside it, the runtime
    swaps the link for the hidden Save button (initChallenges())."""
    where, label = CHALLENGE_TARGETS[challenge.target]
    payload: dict[str, str] = {"name": page, "page": title}
    if challenge.target == "notebook":
        payload["code"] = challenge.parts["python"]
    else:
        payload.update({lang: challenge.parts.get(lang, "") for lang in ("html", "css", "js")})
    href = f"dlroot:{where}#challenge=" + urllib.parse.quote(
        json.dumps(payload, ensure_ascii=False), safe="")
    starters = "".join(
        render_code_block(CodeBlock(language=lang, code=challenge.parts[lang]))
        for lang in CHALLENGE_LANGS if lang in challenge.parts
    )
    return (
        f'<div class="dl-challenge" data-target="{challenge.target}">{starters}'
        '<p class="dl-challenge-actions">'
        f'<a class="dl-btn dl-challenge-open" href="{html.escape(href, quote=True)}" '
        f'target="_blank" rel="noopener">{label}</a>'
        '<button type="button" class="dl-btn dl-challenge-save" hidden>Save it as a file</button>'
        "</p></div>"
    )


def place_challenges(body_html: str, challenges: list[Challenge], page: str,
                     title: str) -> str:
    """Swap each challenge's placeholder for render_challenge()'s block."""
    for index, challenge in enumerate(challenges):
        placeholder = f"<!--dewlab-challenge-{index}-->"
        if placeholder not in body_html:
            raise BuildError(f"a challenge on {page!r} was lost during markdown conversion")
        body_html = body_html.replace(placeholder, render_challenge(challenge, page, title))
    return body_html


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

    It steps by 1 rather than by 5, and its `<output>` is filled by the
    runtime with the preview's width in pixels beside the percentage,
    because a layout tutorial's question is nearly always *at what width*.
    A reader who can only land on multiples of 5% cannot find the width
    where a row wraps, and a percentage alone does not tell them what they
    found. Left empty here: the pixel figure depends on the rendered width
    of a frame that does not exist until the page is laid out.
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
        'min="30" max="100" step="1" value="100" '
        'aria-label="Preview width, as a percentage">'
        f'<output for="{width_id}"></output>'
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


_CONVERTERS = threading.local()


def _converter() -> markdown.Markdown:
    """This thread's Markdown converter, built once. Making one registers
    every extension's patterns afresh, which was most of the time a page
    took to read (a whole-tree `check.py` built 30,000 of them); `reset()`
    before each use clears what a document leaves behind, footnotes and the
    contents tree included. One per thread, since a converter is not safe to
    share between threads."""
    converter = getattr(_CONVERTERS, "converter", None)
    if converter is None:
        converter = _CONVERTERS.converter = markdown.Markdown(
            extensions=["extra", "sane_lists", "toc",
                        "pymdownx.tilde", "pymdownx.tasklist"],
            # `tilde` gives `~~struck out~~` as `<del>`, and would also give a
            # single `~2~` as a subscript. Subscript is off: a lone tilde is
            # already prose here — "~1,000", "after ~5 minutes", a CSS
            # `:checked ~ .toggle` selector — and two of those on nearby lines
            # would pair up into a subscript spanning them.
            extension_configs={"pymdownx.tilde": {"subscript": False}},
        )
    return converter


def to_html(body: str) -> tuple[str, list]:
    """The page's HTML, and the heading tree the `toc` extension collected.

    The tree comes free — the extension is already here to give headings their
    ids, which is what makes `tutorial:slug#anchor` links and the curriculum
    map's section links possible. Taking its tokens as well means the contents
    list on the page is built from the same headings the anchors came from,
    rather than from a second pass that could disagree with them.
    """
    converter = _converter()
    converter.reset()
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

    Any `<details>` that starts a line is marked, whatever its class or
    attributes, so a fold written without one of the three project classes
    still has its markdown converted rather than shown as literal asterisks
    and backticks. Only a tag at the start of a line counts, so a sentence
    that mentions `<details>` in backticks is left alone.

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
            note(path, f"[[{name}]] is not a generated block dewlab knows, so it is left "
                       f"out of the page. The ones it knows are {', '.join(sorted(GENERATED_BLOCKS))}")
            return ""
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
    path = cfg.PAGES / f"{name}.md"
    if path.is_file():
        text = path.read_text()
    elif name == "home":
        text = DEFAULT_HOME
    else:
        fail(path, "does not exist")
    if not text.startswith("---"):
        # A page with nothing above it is only a page with no title yet.
        meta, body = {}, text
    else:
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
    if not meta.get("title"):
        meta["title"] = name.replace("-", " ").capitalize()
        note(path, f"has no title:, so the page is called {meta['title']!r}. Add "
                   "`title:` between two --- lines at the top")
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
    for index, (cell, number) in enumerate(zip(cells, cell_numbers(cells))):
        placeholder = f"<!--dewlab-cell-{index}-->"
        if placeholder not in page_html:
            raise BuildError(f"cell {cell.id!r} was lost during markdown conversion")
        page_html = page_html.replace(
            placeholder, render_cell(cell, number, page, version)
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


def cell_numbers(cells: list[Cell]) -> list[int]:
    """The number on each cell's pill, "Cell 3". A reader sees one world's
    variant of a task at a time (#315), so each variant in a run of them
    counts from the same number, and the cell after the run follows the
    longest variant."""
    numbers: list[int] = []
    upcoming = 1
    group: int | None = None
    base = 0
    counts: dict[str, int] = {}
    for cell in cells:
        if cell.world_group != group:
            if group is not None:
                upcoming = base + max(counts.values())
            group, base, counts = cell.world_group, upcoming, {}
        if group is None:
            numbers.append(upcoming)
            upcoming += 1
        else:
            numbers.append(base + counts.get(cell.world, 0))
            counts[cell.world] = counts.get(cell.world, 0) + 1
    return numbers


def render_world_chooser(worlds: dict[str, str]) -> str:
    """The worlds a page offers, as a choice near its top (#315). Hidden
    until the runtime wires it, so a page without JavaScript shows every
    variant, each under its world's name, and no control that does
    nothing."""
    choices = "".join(
        '<label class="dl-world-choice">'
        f'<input type="radio" name="dl-world" value="{html.escape(key, quote=True)}">'
        f'<span class="dl-world-name">{html.escape(world_name(key))}</span>'
        f'<span class="dl-world-line">{_inline(line)}</span></label>'
        for key, line in worlds.items()
    )
    return (
        '<fieldset class="dl-world-chooser" hidden>'
        "<legend>Choose a world for this page</legend>"
        f'<div class="dl-world-choices">{choices}</div>'
        '<p class="dl-world-note">A world is the setting for the examples and the '
        "tasks. The lesson is the same in each one. You can change your choice "
        "at any time, and your work in each world is saved separately.</p>"
        "</fieldset>"
    )


def place_worlds(body_html: str, spans: list[WorldSpan], worlds: dict[str, str],
                 path: Path) -> str:
    """Give each variant its group and its world's name, and put the chooser
    under the page's title (#315). Variants reach here in source order, the
    order world_spans() found them, since code examples were placeholders
    when the markdown was converted and cannot hold a real variant."""
    if not spans:
        return body_html
    if body_html.count('<div class="dl-world"') != len(spans):
        fail(path, "a `<div class=\"dl-world\">` tag shares its line with other text — "
                   "put each opening tag on a line of its own")
    found = iter(spans)

    def label(match: re.Match) -> str:
        span = next(found)
        return (f'<div class="dl-world" data-world="{span.world}" '
                f'data-world-group="{span.group}">'
                f'<p class="dl-world-label">{html.escape(world_name(span.world))}</p>')

    body_html = WORLD_DIV_RE.sub(label, body_html)
    chooser = render_world_chooser(worlds)
    if "</h1>" in body_html:
        return body_html.replace("</h1>", "</h1>\n" + chooser, 1)
    return chooser + "\n" + body_html


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
            # An id only lets a link reach the note in the reference panel.
            number = 2
            while f"{note_id}-{number}" in seen:
                number += 1
            note(path, f"two notes share the id {note_id!r}, so the second is "
                       f"{note_id}-{number}")
            note_id = f"{note_id}-{number}"
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
    if not cfg.COURSES.is_dir():
        return (str(cfg.COURSES),)
    return tuple(
        (str(path), path.stat().st_mtime_ns, path.stat().st_size)
        for path in sorted(cfg.COURSES.glob("*.yaml"))
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
    if cfg.COURSES.is_dir():
        for path in sorted(cfg.COURSES.glob("*.yaml")):
            if path.name in (COURSE_INDEX_FILE, REDIRECTS_FILE):
                continue
            found[path.stem] = read_course(path)

    order: list[str] = []
    index = cfg.COURSES / COURSE_INDEX_FILE
    if index.is_file():
        data = yaml.safe_load(index.read_text()) or {}
        order = data.get("order") or []
        if not isinstance(order, list) or not all(isinstance(c, str) for c in order):
            note(index, "needs `order:` as a list of course ids, one per line, so the "
                        "courses are in alphabetical order")
            order = []
        for name in order:
            if name not in found:
                note(index, f"lists {name}, and there is no courses/{name}.yaml, "
                            "so it is left out")
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
        title = path.stem
        note(path, f"has no `title:` line, so the course is called {title!r} on the site")
    status = str(data.get("status", "live"))
    if status not in COURSE_STATUSES:
        # Status only picks the badge on the course's tile, so a value this
        # build does not know is no badge, not a stopped build.
        note(path, f"status {status!r} is not one of {', '.join(COURSE_STATUSES)}, "
                   "so the course has no badge")
        status = "live"
    contents = data.get("contents")
    if contents is None:
        contents = []
    if not isinstance(contents, list):
        fail(path, "`contents:` is a list of series, each with a title and its tutorials")
    series: list[Series] = []
    listed: dict[str, str] = {}
    for position, entry in enumerate(contents, start=1):
        if not isinstance(entry, dict):
            fail(path, "each series under `contents:` is a `title:` and its `tutorials:`")
        title_line = entry.get("title")
        if not isinstance(title_line, str) or not series_key(title_line):
            # A series still being named keeps its tutorials where they are,
            # under a heading that says where it comes in.
            title_line = f"Part {position}"
            note(path, f"series {position} under `contents:` has no usable `title:` (it needs "
                       f"a letter or a digit), so it is headed {title_line!r}")
        ids = entry.get("tutorials")
        if ids is None:
            ids = []
        if not isinstance(ids, list) or not all(isinstance(i, str) for i in ids):
            fail(path, f'the series "{title_line}" needs `tutorials:` as a list of ids')
        key = series_key(title_line)
        if key in {s.key for s in series}:
            fail(path, f'two series are both called "{title_line}" (or differ only in '
                       "punctuation). Give one of them another title.")
        kept: list[str] = []
        for ident in ids:
            if ident in listed:
                # A tutorial sits in one place on a course, and the first
                # place it is listed is the one it keeps.
                note(path, f'lists {ident} twice — under "{listed[ident]}" and under '
                           f'"{title_line}". It stays under "{listed[ident]}"')
                continue
            listed[ident] = title_line
            kept.append(ident)
        series.append(Series(key=key, title=title_line.strip(), ids=kept))
    mixed = data.get("mixed")
    if mixed is None:
        mixed = []
    if not isinstance(mixed, list) or not all(isinstance(i, str) for i in mixed):
        fail(path, "`mixed:` is a list of ids of mixed problem sets")
    for ident in list(mixed):
        if ident in listed:
            note(path, f'lists {ident} under `mixed:` and under "{listed[ident]}". '
                       f'It stays under "{listed[ident]}"')
            mixed = [other for other in mixed if other != ident]
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
    path = cfg.COURSES / REDIRECTS_FILE
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
    listed at all — it is reached from its tutorial — and neither can a
    context page; an archived one may be, but sits in the course's Archive
    rather than on the route.

    Practice and context pages are placed afterwards, by practice_pairs(),
    mixed_practice() and context_pages(), from the tutorial they belong to.
    """
    for course in courses().values():
        for series in course.contents:
            for position, ident in enumerate(series.ids, start=1):
                member = registry.get(ident)
                if member is None:
                    if (cfg.TUTORIALS / ident / f"{ident}.md").is_file():
                        say(f"note: {course.path.relative_to(cfg.ROOT)} lists {ident}, "
                              "which is a draft, so it is not on the course yet")
                        continue
                    fail(course.path, f'the series "{series.title}" lists {ident}, but '
                                      f"there is no folder tutorials/{ident}/")
                # A context page or a tutorial's own page of problems sits
                # wherever its tutorial does, so listing it here adds
                # nothing: the line is left out. A mixed set is another
                # matter: it is placed by its course's `mixed:` list, and a
                # series line would put it on the reading order.
                if member.is_context or member.practice_for:
                    kind = "a context page" if member.is_context else "a page of problems"
                    note(course.path, f'the series "{series.title}" lists {ident}, which is '
                                      f"{kind} and follows its tutorial, so the line is left out")
                    continue
                if member.practice_across:
                    fail(course.path, f'the series "{series.title}" lists {ident}, which is '
                                      "a mixed problem set; list it under `mixed:` instead.")
                member.placements.append(Placement(course.id, series.key, position))
        for ident in course.mixed:
            member = registry.get(ident)
            if member is None:
                fail(course.path, f"lists {ident} under `mixed:`, but there is no folder "
                                  f"tutorials/{ident}/")
            if not member.practice_across:
                note(course.path, f"lists {ident} under `mixed:`, and it is not a mixed "
                                  "problem set (it has no practice_across line), so the "
                                  "line is left out")
                continue
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
                                   f"is {seen[version.version].path.relative_to(cfg.ROOT)}. "
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
) -> dict[str, list[Tutorial]]:
    """Each tutorial's pages of problems, by the id of the tutorial they belong to.

    A practice page names its tutorial with `practice_for:`. Both directions are
    checked here rather than being discovered by a reader following a link that
    goes nowhere: the tutorial has to exist. A tutorial may have several
    practice pages (a set per topic, or an easier and a harder set); they are
    listed in the order of their ids, numbers read as numbers, so
    `first-steps-practice-2` comes before `first-steps-practice-10`. Each page
    then sits wherever its tutorial sits — it takes the tutorial's placements,
    so its tree and its course are the tutorial's own.

    A practice page should declare no coverage. It sets problems on what its
    tutorial taught, and counting it would report the same outcome as taught
    twice — see `docs/WRITING_TUTORIALS.md`, "Practice pages". One that does
    builds, with a note, since only the curriculum map's counts are affected.
    """
    pairs: dict[str, list[Tutorial]] = {}
    for page in tutorials:
        target = page.practice_for
        if target and page.practice_across:
            fail(page.path, "sets both practice_for and practice_across. A page "
                            "of problems either belongs to one tutorial or "
                            "draws on several; it cannot do both.")
        if not target:
            continue
        if page.meta.get("covers"):
            note(page.path, "is a practice page and declares `covers:`, so the curriculum "
                            "map and the topic tree count its outcomes a second time, and may "
                            "link a topic to this page instead of its tutorial. Delete "
                            "`covers:` unless you mean that.")
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
        if owner.is_context:
            fail(page.path, f"has practice_for: {target}, which is a context "
                            "page. Practice sets problems on what a tutorial "
                            "teaches, and a context page teaches nothing a "
                            "reader needs.")
        page.placements = list(owner.placements)
        if not page.is_default:
            continue
        pairs.setdefault(target, []).append(page)
    for pages in pairs.values():
        pages.sort(key=lambda p: [int(t) if t.isdigit() else t
                                  for t in re.split(r"(\d+)", p.slug)])
    return pairs


def mixed_practice(
    tutorials: list[Tutorial], registry: dict[str, Tutorial]
) -> dict[str, list[Tutorial]]:
    """Problem sets that draw on several tutorials, per course, in title order.

    Checked the same way as `practice_for`: every id it names has to exist and
    not be the page itself or a context page. A set naming one tutorial, or
    naming a page of problems, is unusual and builds with a note. A repeated
    id is listed once.

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
            note(page.path, "is a practice page and declares `covers:`, so the curriculum "
                            "map and the topic tree count its outcomes a second time, and may "
                            "link a topic to this page. Delete `covers:` unless you mean that.")
        listed = listed_ids(page.meta.get("practice_across"))
        if len(set(listed)) != len(listed):
            repeated = sorted({s for s in listed if listed.count(s) > 1})
            note(page.path, f"names {', '.join(repeated)} in practice_across more than "
                            "once. Each is listed once.")
        if len(across) < 2:
            note(page.path, "has practice_across naming one tutorial. `practice_for` says "
                            "that more plainly; a tutorial with a page of its own problems "
                            "will link both.")
        for slug in across:
            if slug == page.slug:
                fail(page.path, f"has practice_across naming {slug}, which is "
                                "itself.")
            owner = registry.get(slug)
            if owner is None:
                fail(page.path, f"has practice_across naming {slug}, and there "
                                f"is no folder tutorials/{slug}/.")
            if owner.is_practice:
                note(page.path, f"has practice_across naming {slug}, which is itself a "
                                "page of problems. It builds, and the set sits with the "
                                "first tutorial it names.")
            if owner.is_context:
                fail(page.path, f"has practice_across naming {slug}, which is "
                                "a context page, not a tutorial.")
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


def context_pages(
    tutorials: list[Tutorial], registry: dict[str, Tutorial]
) -> dict[str, list[Tutorial]]:
    """Each tutorial's context pages, by the id of the tutorial, in title order.

    A context page names the tutorial(s) it gives background for with
    `context_for:`, one id or a list. Checked the way `practice_for` and
    `practice_across` are: every id exists, is a tutorial rather than
    another companion page, and is not the page itself; one named twice is
    listed once, with a note. It should declare no coverage — nothing on it
    is needed to finish a tutorial, so it cannot be where an outcome is
    taught; one that does builds, with a note — and it is not also a page of
    problems, since a reader has to be able to tell optional reading from
    work. It sits wherever its first tutorial sits, the same as a practice
    page.

    Unlike practice, a tutorial may have several: background splits
    naturally by subject, and each page is only read by whoever wants it.
    """
    out: dict[str, list[Tutorial]] = {}
    for page in tutorials:
        named = page.context_for
        if not named:
            continue
        if page.is_practice:
            fail(page.path, "sets context_for and a practice line. A context "
                            "page is background reading and a practice page is "
                            "problems; one page cannot be both.")
        if page.meta.get("covers"):
            note(page.path, "is a context page and declares `covers:`, so the curriculum "
                            "map and the topic tree count it as teaching an outcome, and may "
                            "link a topic to it. Delete `covers:` unless you mean that.")
        listed = listed_ids(page.meta.get("context_for"))
        if len(set(listed)) != len(listed):
            repeated = sorted({s for s in listed if listed.count(s) > 1})
            note(page.path, f"names {', '.join(repeated)} in context_for more than once. "
                            "Each is listed once.")
        for slug in named:
            if slug == page.slug:
                fail(page.path, f"has context_for naming {slug}, which is itself.")
            owner = registry.get(slug)
            if owner is None:
                fail(page.path, f"has context_for naming {slug}, and there is "
                                f"no folder tutorials/{slug}/.")
            if owner.is_practice:
                fail(page.path, f"has context_for naming {slug}, which is a "
                                "page of problems. Name the tutorial it "
                                "practises instead.")
            if owner.is_context:
                fail(page.path, f"has context_for naming {slug}, which is "
                                "itself a context page.")
        page.placements = list(registry[named[0]].placements)
        if not page.is_default:
            continue
        for slug in named:
            out.setdefault(slug, []).append(page)
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
    built; a practice or context page hangs off its tutorial. None of them
    is here.
    """
    groups: dict[tuple[str, str], list[Tutorial]] = {}
    for tutorial in tutorials:
        if tutorial.status != "live" or not tutorial.is_default or tutorial.is_companion:
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


def series_fragment(
    course: Course,
    groups: dict[tuple[str, str], list[Tutorial]],
    key: str,
) -> str:
    """The `#series-<key>` a link to one series should carry. The course
    page (render_course_body()) only prints a series heading, and so only
    has something to land on, when the course has more than one series."""
    present = [k for k in course.keys if (course.id, k) in groups]
    return f"#series-{html.escape(key, quote=True)}" if len(present) > 1 else ""


def crumb_trail_html(
    tutorial: Tutorial,
    groups: dict[tuple[str, str], list[Tutorial]],
    members: list[Tutorial],
    up: str,
    practice: list[Tutorial] | None = None,
    registry: dict[str, Tutorial] | None = None,
    also: list[Tutorial] | None = None,
    context: list[Tutorial] | None = None,
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
    `context` is the tutorial's context pages, listed after its problems
    with a "context" tag; a context page sits under its first tutorial the
    way a practice page does.

    The course and series rungs are the default course's — the first that
    lists this page. A page on more than one course says so on the nav
    (`data-courses`), and the runtime redraws these two rungs for the
    course the reader is following (tutorial-runtime.js, drawCourseChrome).
    A page no course lists has only the first rung and its own.

    The heading of each level above the page — all tutorials, the course,
    the series — is a link to the page it names (the all-tutorials page, the
    course's page, and the series' heading on the course's page), so every
    step back is one click from anywhere. The caret beside it still opens
    and closes the level's list.
    """
    if (tutorial.practice_for or tutorial.is_context) and registry:
        owner = registry.get(tutorial.owners[0])
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
    # sections, its practice and its context pages — the title itself
    # carries the caret, so the name is not printed twice (once bold in the
    # list, once as a rung of its own beneath). It starts closed: a reader
    # arriving at a tutorial should meet the tutorial, not a list of its
    # parts. A page with nothing behind its own name — too few sections for
    # a contents list (contents_items_html()), no companion page — gets a
    # plain bold line rather than a caret with nothing behind it.
    contents, count = contents_items_html(tutorial)
    # A practice page's own title already says what it is ("First Steps —
    # Practice", "Mixed Problems — Programming"), so the line is the title
    # and nothing more; the colour marks it as a different kind of page. A
    # context page's title names its subject, not its kind, so it carries a
    # small tag saying so.
    extra = [
        f'<div role="listitem" class="dl-crumb-practice">'
        f'<a href="{link_between(tutorial, problems)}">{html.escape(problems.title)}</a></div>'
        for problems in list(practice or []) + list(also or [])
    ] + [
        f'<div role="listitem" class="dl-crumb-context">'
        f'<a href="{link_between(tutorial, page)}">{html.escape(page.title)}</a>'
        ' <span class="dl-crumb-tag">context</span></div>'
        for page in context or []
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

    # An archived tutorial or a companion page has no reading-order position
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
            # A page of problems or a context page belongs to its
            # tutorial, so it sits one level under it — the tutorial stays a plain link back to
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
        f'<summary><a href="{up}all-tutorials.html">All tutorials</a></summary>'
        f'<div role="list">{courses_items}</div>'
        "</details>"
    ]
    if course is not None:
        levels.append(
            '<details class="dl-crumb-level dl-crumb-level-2">'
            f'<summary><a href="{up}{html.escape(course.id, quote=True)}.html">'
            f"{html.escape(course.title)}</a></summary>"
            f'<div role="list">{series_items}</div>'
            "</details>"
        )
    if course is not None and tutorial.series:
        series_href = f"{up}{html.escape(course.id, quote=True)}.html" + series_fragment(course, groups, tutorial.series)
        levels.append(
            '<details class="dl-crumb-level dl-crumb-level-3" open>'
            f'<summary><a href="{series_href}">'
            f"{html.escape(course.series_title(tutorial.series))}</a></summary>"
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


def python_signatures() -> dict[str, str]:
    """`assets/python-signatures.json`: each signature Python itself gives
    for a built-in, standard-library or `tutorial_tools` name a glossary
    entry declares with `python:`, written by `dev/glossary_python.py`
    (which also checks every such name exists and every example calls it
    the way its signature allows). Read at call time, like the glossary
    files themselves, and `{}` when the file is not there."""
    path = cfg.ASSETS / "python-signatures.json"
    if not path.is_file():
        return {}
    return json.loads(path.read_text()).get("signatures") or {}


def with_python(entries: list[dict], path: Path) -> list[dict]:
    """Each entry's declared `python:` names checked for shape, and the
    signatures Python gives for them attached as `signatures`, for the
    reference to show under the definition. An entry whose names have no
    signature (a keyword, an exception, a pandas method) carries none."""
    signatures = python_signatures()
    for entry in entries:
        names = entry.get("python")
        if names is None:
            continue
        if isinstance(names, str):
            names = [names]
        if not isinstance(names, list) or not all(isinstance(n, str) for n in names):
            note(path, f'glossary entry "{entry.get("term")}" has a `python:` that is not '
                       "a dotted name or a list of them, so it shows no signature")
            continue
        shown = [signatures[name] for name in names if name in signatures]
        if shown:
            entry["signatures"] = shown
    return entries


# Each page's reference walks every earlier page of its series, so a page's
# own glossary is asked for hundreds of times in a build (seventeen thousand
# on this site) and was read, parsed and checked against Python's signatures
# every time. The file does not change during a build, so what it said is
# kept; build() clears it. Callers get copies, since the entries are handed
# on to pages that add to them.
_GLOSSARIES: dict[Path, list[dict]] = {}


def own_glossary(tutorial: Tutorial) -> list[dict]:
    """This tutorial's own contribution — what it introduces, not what it
    inherits from earlier in its series. A missing file means none written
    yet, not an error: that is what lets this feature ship before every
    tutorial has one."""
    path = glossary_path(tutorial)
    if path not in _GLOSSARIES:
        _GLOSSARIES[path] = _read_glossary(path)
    return [dict(entry) for entry in _GLOSSARIES[path]]


def _read_glossary(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    data = read_yaml(path) or {}
    entries = data.get("entries") or []
    # What kind an entry is decides which group of the reference it sits in.
    # One this build does not know has nowhere to go, so it is left out, and
    # said: a guess at "concept" could put a function where a reader looks
    # for an idea.
    for entry in entries:
        if entry.get("kind") not in GLOSSARY_KINDS:
            note(path, f'glossary entry "{entry.get("term")}" has kind '
                       f'{entry.get("kind")!r}, not one of {", ".join(GLOSSARY_KINDS)}, '
                       "so it is left out of the reference")
    entries = [entry for entry in entries if entry.get("kind") in GLOSSARY_KINDS]
    kept = [entry for entry in entries if entry.get("term") and entry.get("definition")]
    if len(kept) < len(entries):
        note(path, f"{len(entries) - len(kept)} glossary entr"
                   f"{'y is' if len(entries) - len(kept) == 1 else 'ies are'} missing a term "
                   "or a definition and left out of the reference")
    return with_python(kept, path)


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
    _through: frozenset[str] = frozenset(),
) -> list[dict]:
    """Everything a reader has met by this point: this tutorial's own
    glossary, everything earlier in its own series, and everything from
    each earlier series of its course (`series_chain()`). Whichever entry came first wins
    on a term repeated later, so a definition never contradicts an earlier
    one on the same page.

    A practice or context page has no series position that means anything —
    `practice_for`/`practice_across`/`context_for` name what it belongs to
    instead of where it sits — so its reference is the union of the
    tutorial(s) it names, each resolved the same way. A context page may
    also define terms of its own (background reading goes further than
    its tutorials did), so its own glossary follows the union; a practice
    page teaches nothing new and has none. `_through` stops the walk when
    two mixed sets name each other, as in toolkit_for().
    """
    reader_at = reader_at or tutorial

    if tutorial.is_companion:
        if tutorial.slug in _through:
            return []
        targets = list(tutorial.owners)
        seen: set[tuple[str, str]] = set()
        found: list[dict] = []
        for slug in targets:
            target = registry.get(slug)
            if target is None:
                continue
            for entry in cumulative_glossary(target, registry, groups, reader_at,
                                             _through | {tutorial.slug}):
                key = (entry["term"], entry["kind"])
                if key in seen:
                    continue
                seen.add(key)
                found.append(entry)
        if tutorial.is_context:
            for entry in own_glossary(tutorial):
                key = (entry["term"], entry["kind"])
                if key not in seen:
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
        # The path from this page to the one that introduced the term is the
        # same for every term, so it is worked out once per page.
        href = None if member is reader_at else _relative_href(
            member.out_path, reader_at.out_path.parent)
        for entry in own_glossary(member):
            key = (entry["term"], entry["kind"])
            if key in seen:
                continue
            seen.add(key)
            found.append(entry if href is None
                         else {**entry, "origin": _origin(member, href, entry["term"])})
    return found


# Every term of every earlier page asks for the same path between the same
# two pages, and a relative path is slower to work out than it looks: a
# hundred thousand of them were most of the glossary's time. Cleared by
# build(), like _origin_anchor().
@functools.lru_cache(maxsize=None)
def _relative_href(target: Path, start: Path) -> str:
    return os.path.relpath(target, start)


def origin_of(reader_at: Tutorial, introduced_by: Tutorial, term: str) -> dict:
    """The tutorial a term was introduced in, as something the reference panel
    can render: a title to name it and an href to reach it from the page the
    reader is on."""
    return _origin(introduced_by, _relative_href(introduced_by.out_path, reader_at.out_path.parent), term)


def _origin(introduced_by: Tutorial, href: str, term: str) -> dict:
    anchor = origin_anchor(introduced_by, term)
    return {
        "title": introduced_by.title,
        "href": f"{href}#{anchor}" if anchor else href,
    }


def toolkit_entries(members: list[Tutorial]) -> list[dict]:
    """Every toolkit cell on `members`, in order, as a manifest entry.
    Whether a reader's saved version is really theirs, or the stub left
    as it was, is decided per function when it loads
    (`tutorial_tools._load_toolkit()`), so the stub itself need not travel."""
    return [
        {"tutorial": member.slug, "title": member.title, "cell": cell.id,
         "reference": cell.toolkit_reference}
        for member in members
        for cell in member.cells
        if cell.toolkit
    ]


def toolkit_for(
    tutorial: Tutorial,
    registry: dict[str, Tutorial],
    groups: dict[tuple[str, str], list[Tutorial]],
    _through: frozenset[str] = frozenset(),
) -> list[dict]:
    """The toolkit a page loads before its first cell runs: every toolkit
    cell on an earlier tutorial of its course, in the order
    cumulative_glossary() walks (`series_chain()`), and none of its own —
    the reader runs those. On a page listed by several courses, the first
    course in courses/index.yaml order whose earlier pages have any.

    A frozen release sits where its current one does, so it is matched by
    id rather than by identity. A practice or context page is on no route
    of its own, so it loads the toolkit of the tutorial(s) it belongs to,
    those tutorials' own toolkit cells included: the reader has been
    through them by then. A mixed set naming several gets everything up to
    and including the latest of them, in course order, whatever order its
    `practice_across` lists them in: each owner's chain is a prefix of
    the latest one's, so the union walks the course once. Two mixed sets
    may name each other; `_through` is the companions already on the way
    here, so the walk stops instead of going round.
    """
    if tutorial.is_companion:
        if tutorial.slug in _through:
            return []
        found: list[dict] = []
        seen: set[tuple[str, str]] = set()
        for slug in tutorial.owners:
            owner = registry.get(slug)
            if owner is None:
                continue
            onward = toolkit_for(owner, registry, groups, _through | {tutorial.slug})
            for entry in onward + toolkit_entries([owner]):
                key = (entry["tutorial"], entry["cell"])
                if key not in seen:
                    seen.add(key)
                    found.append(entry)
        return found

    for course in courses():
        for placement in tutorial.placements:
            if placement.course != course or not placement.series:
                continue
            chain = series_chain(course, placement.series, groups)
            slugs = [member.slug for member in chain]
            if tutorial.slug not in slugs:
                continue
            entries = toolkit_entries(chain[: slugs.index(tutorial.slug)])
            if entries:
                return entries
    return []


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
    groups = []
    for group in data.get("groups") or []:
        if not group.get("label"):
            note(path, f"a {kind} group is missing a label, so it is headed Other")
            group["label"] = "Other"
        entries = group.get("entries") or []
        kept = [entry for entry in entries if entry.get("term") and entry.get("definition")]
        if len(kept) < len(entries):
            note(path, f"a {kind} entry is missing a term or a definition, so it is left "
                       f"out of the group {group['label']!r}")
        if not kept:
            note(path, f'the group {group.get("label")!r} has no entries, so it is left out')
            continue
        group["entries"] = kept
        groups.append(group)
        with_python(kept, path)
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
    return _load_basics(cfg.MATH_BASICS_DATA, "math-basics")


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
    return _load_basics(cfg.PYTHON_BASICS_DATA, "python-basics")


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


def progress_attrs(tutorial: Tutorial) -> str:
    """`data-id`/`data-cells` for a contents-page link, so
    tutorial-runtime.js's progress indicator can read a reader's
    saved-progress record for it with no fetch. A prose-only tutorial has
    nothing to show progress for, so it gets no attribute at all rather
    than a "0/0"."""
    if not tutorial.cells:
        return ""
    # A choose-your-project page's projects count only once started,
    # so the badge needs to know which cells are whose.
    projects = (f' data-projects="{html.escape(json.dumps(tutorial.project_cells), quote=True)}"'
                if tutorial.project_cells else "")
    return (
        f' data-id="{html.escape(tutorial.slug, quote=True)}"'
        f' data-cells="{len(tutorial.cells)}"{projects}'
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
    its box already says it.
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
    is no second bar to open, on any width (Josh: "a tap or click
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


def companion_buttons_html(
    member: Tutorial,
    practice: dict[str, list[Tutorial]],
    context: dict[str, list[Tutorial]] | None = None,
) -> str:
    """The buttons after a tutorial's line on a contents list: its practice
    page, then each context page, which is marked with a small "context"
    tag since its title names its subject rather than its kind. Paths are
    relative to the site root, where every contents page lives."""
    extra = ""
    pages = practice.get(member.slug, [])
    for number, also in enumerate(pages, 1):
        where = also.out_path.relative_to(cfg.OUT).as_posix()
        label = "Practice" if len(pages) == 1 else f"Practice {number}"
        extra += f' <a class="dl-contents-practice" href="{where}">{label}</a>'
    for page in (context or {}).get(member.slug, []):
        where = page.out_path.relative_to(cfg.OUT).as_posix()
        extra += (f' <a class="dl-contents-context" href="{where}">'
                  f'{html.escape(page.title)} <span class="dl-contents-tag">context</span></a>')
    return extra


def render_tutorials_list(
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path] | None = None,
    retired: dict[str, list[Tutorial]] | None = None,
    practice: dict[str, list[Tutorial]] | None = None,
    mixed: dict[str, list[Tutorial]] | None = None,
    course_archives: dict[str, Path] | None = None,
    context: dict[str, list[Tutorial]] | None = None,
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
        'top. If you are not sure where to start, '
        + ('the <a href="map.html">topic map</a> shows what the courses cover and what '
           'usually comes first, as towns on a map. The <a href="tree.html">topic tree</a> '
           "shows the same topics as a list that reads downwards. "
           if (cfg.ROOT / "map" / "graph.json").is_file() else
           'the <a href="tree.html">topic tree</a> shows what the course covers and what '
           "usually comes first. ")
        + '<a href="topics.html">Browse by topic</a> gathers one subject — '
        "trigonometry, say — in one place.</li>",
        "</ul>",
        ('<p class="dl-intro-tree">This project is open and still growing. '
         '<a href="about.html">About this project</a> explains how to suggest a '
         "change or report a mistake.</p>") if (cfg.PAGES / "about.md").is_file() else "",
        "</div>",
    ]

    catalog = courses()
    for course in courses_present(groups, retired, mixed):
        out.extend(render_course_body(
            catalog[course], groups, archives, retired, practice, mixed, course_archives,
            context=context,
        ))
    return "\n".join(out)


def render_course_body(
    course: Course,
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path],
    retired: dict[str, list[Tutorial]],
    practice: dict[str, list[Tutorial]],
    mixed: dict[str, list[Tutorial]],
    course_archives: dict[str, Path],
    heading: bool = True,
    context: dict[str, list[Tutorial]] | None = None,
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
            len(downloads.zip_sequence(members, practice))
            for (owner, _), members in groups.items() if owner == course.id
        ) + len(mixed.get(course.id, []))
        out.append(
            '<p class="dl-series">' + download_link_html(
                f"download/{course_archive.name}",
                f"Download every tutorial and practice page in this module "
                f"({total} files, {downloads.readable_size(course_archive)})",
            ) + "</p>"
        )
    present = [key for key in course.keys if (course.id, key) in groups]
    for key in present:
        members = groups[(course.id, key)]
        if len(present) > 1:
            out.append(
                f'<h3 id="series-{html.escape(key, quote=True)}">'
                f"{html.escape(course.series_title(key))}</h3>"
            )
        archive = archives.get((course.id, key))
        if archive is not None:
            sequence = downloads.zip_sequence(members, practice)
            count = len(sequence)
            what = ("this one as a single file" if count == 1
                    else f"all {count} as single files")
            out.append(
                '<p class="dl-series">' + download_link_html(
                    f"download/{archive.name}",
                    f"Download {what} ({downloads.readable_size(archive)})",
                ) + "</p>"
            )
        out.append('<ol class="dl-contents">')
        for member in members:
            href = member.out_path.relative_to(cfg.OUT).as_posix()
            extra = companion_buttons_html(member, practice, context)
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
        href = member.out_path.relative_to(cfg.OUT).as_posix()
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
        href = member.out_path.relative_to(cfg.OUT).as_posix()
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
    """Say so when a `<details>` names none of the project's fold styles.

    A note, not a refusal. A fold with no class still
    works: its markdown is converted (`mark_markdown_wrappers()`) and a reader
    can open it. What it lacks is the project's look and marker, so it shows
    as the browser's default triangle. That is worth telling the author, and
    nothing a reader's page depends on, so it does not stop the build.
    """
    for tag in DETAILS_RE.findall(tutorial.body_html):
        if not any(name in tag for name in FOLD_CLASSES):
            say(f"note: {tutorial.path.relative_to(cfg.ROOT)}: a fold names no style: "
                  f'{tag} — class="dl-hint" (steps), class="dl-answer" (an answer) or '
                  f'class="dl-why" (why a page chose as it did) gives it the '
                  f"project's look")


DATASET_FIELDS = ("source", "url", "license", "snapshot", "trimmed", "description")
DATASET_EXTENSIONS = (".csv", ".txt")
# The steps a `recipe:` may give, which tutorial_tools.shape_live() runs in
# its own fixed order: how the snapshot is made from its source
# (dev/datasets.py), and, for a dataset with `live: true`, how a page
# shapes the live copy the same way. `source` names the website in the note
# under the cell; `url` is where its CSV is; `columns` is the snapshot's own.
RECIPE_FIELDS = ("source", "url", "columns", "skip_through", "rename", "missing",
                 "drop_empty", "at_least", "at_most", "round")
RECIPE_REQUIRED = ("source", "url", "columns")
# A literal file name in a load: `load_csv("life-expectancy.csv")`.
LOAD_CALL = re.compile(r"""load_(?:csv|text)\(\s*(["'])(?P<name>[^"']+)\1""")


def long_date(day: datetime.date) -> str:
    """26 September 2026: the way a page says a date."""
    return f"{day.day} {day.strftime('%B')} {day.year}"


def dataset_file(name: str) -> Path | None:
    """`data/<name>.csv` or `data/<name>.txt`, whichever exists."""
    for ext in DATASET_EXTENSIONS:
        if (cfg.DATA / f"{name}{ext}").is_file():
            return cfg.DATA / f"{name}{ext}"
    return None


@functools.lru_cache(maxsize=None)
def read_dataset(name: str) -> dict | None:
    """`data/<name>.yaml`, checked: a real date for its snapshot, a `recipe:`
    shape_live() can run, and `live: true` only where there is a recipe to
    shape the live copy with.

    Where a dataset came from is for the educator to say, and a file that
    does not is a note, not a stopped build: a field
    left blank is listed, and the Reference tab says it was not recorded.
    The one thing the page cannot do without is the `snapshot` date, which
    its numbers and the note under a cell come from. A file without a
    readable one is treated as a data file with no yaml at all, and None
    comes back. A `recipe:` that cannot run is still refused: it is
    machinery, and a wrong one would fetch the wrong numbers.
    """
    path = cfg.DATA / f"{name}.yaml"
    data = load_yaml_no_duplicate_keys(path.read_text()) or {}
    blank = [f for f in DATASET_FIELDS if f != "snapshot" and not data.get(f)]
    if blank:
        note(path, f"does not give its {', '.join(blank)}, so a page that uses it "
                   "cannot say all of where it came from")
    snapshot = data.get("snapshot")
    if isinstance(snapshot, str):
        try:
            snapshot = datetime.date.fromisoformat(snapshot)
        except ValueError:
            pass
    if not isinstance(snapshot, datetime.date):
        note(path, "has no snapshot: date like 2026-09-26, so a page that uses it "
                   "cannot say when its numbers were saved")
        return None
    data["snapshot"] = snapshot.isoformat()
    recipe = data.get("recipe")
    if recipe is not None:
        if not isinstance(recipe, dict):
            fail(path, "recipe: must be a mapping of the steps in RECIPE_FIELDS")
        unknown = sorted(set(recipe) - set(RECIPE_FIELDS))
        if unknown:
            fail(path, f"recipe: has {', '.join(unknown)}, which shape_live() does "
                       f"not know; it knows {', '.join(RECIPE_FIELDS)}")
        absent = [f for f in RECIPE_REQUIRED if not recipe.get(f)]
        if absent:
            fail(path, f"recipe: is missing {', '.join(absent)}")
        data_file = dataset_file(name)
        if data_file is not None and data_file.suffix != ".csv":
            fail(path, "has a recipe:, and only a CSV can be shaped by one")
    live = data.get("live", False)
    if not isinstance(live, bool):
        fail(path, f"live: {live!r} is not true or false")
    if live and recipe is None:
        fail(path, "says live: true, and has no recipe: for a page to shape the "
                   "live copy with")
    # A page that loads the recipe's address itself expects the file as that
    # address serves it, so the copy standing in for it is the same file.
    address = data.get("address", False)
    if not isinstance(address, bool):
        fail(path, f"address: {address!r} is not true or false")
    if address:
        steps = sorted(set(recipe or {}) - set(RECIPE_REQUIRED))
        if not live or steps:
            fail(path, "says address: true, which needs live: true and a recipe: "
                       "that keeps the file as it is (only source, url and columns)"
                       + (f"; it also has {', '.join(steps)}" if steps else ""))
    return data


@functools.lru_cache(maxsize=None)
def data_index() -> dict[str, dict]:
    """Every dataset in `data/`, keyed by file name, as tutorial_tools reads
    it from `data/index.json`: the snapshot date, and the recipe of a
    dataset a page fetches live.

    Checked in both directions, for every file and not only the declared
    ones, since dewmini and the Notebook load them by name too. A yaml
    without its data file fails: it describes nothing. A data file without
    its yaml builds with a note and an empty entry, so a cell that loads it
    says only "Loaded <name>." and the page's Reference tab does not list it:
    the page works, and cannot say where its numbers came from.
    """
    index: dict[str, dict] = {}
    if not cfg.DATA.is_dir():
        return index
    names = sorted({p.stem for p in cfg.DATA.iterdir()
                    if p.suffix in DATASET_EXTENSIONS + (".yaml",)})
    for name in names:
        data_file = dataset_file(name)
        if data_file is None:
            fail(cfg.DATA / f"{name}.yaml", f"describes data/{name}.csv or "
                                        f"data/{name}.txt, and neither exists")
        if not (cfg.DATA / f"{name}.yaml").is_file():
            note(data_file, f"has no data/{name}.yaml giving its "
                            f"{', '.join(DATASET_FIELDS)}, so a page that uses it "
                            "cannot say where it came from")
            index[data_file.name] = {}
            continue
        data = read_dataset(name)
        if data is None:  # read_dataset() has said why
            index[data_file.name] = {}
            continue
        entry = {"snapshot": data["snapshot"]}
        if data.get("live"):
            entry["live"] = data["recipe"]
        if data.get("address"):
            entry["address"] = True
        index[data_file.name] = entry
    return index


def write_data_index(folder: Path) -> Path:
    """`index.json` beside the data files it describes."""
    target = folder / "index.json"
    target.write_text(json.dumps(data_index(), indent=1, sort_keys=True))
    return target


def dataset_attribution(tutorial: Tutorial, name: str) -> dict | None:
    """A declared dataset's own attribution, for the page's Reference tab —
    `data/<name>.yaml` beside `data/<name>.csv` (loaded with `load_csv()`)
    or `data/<name>.txt` (loaded with `load_text()`), the same
    beside-the-file pattern `<slug>.glossary.yaml` already established.
    """
    if dataset_file(name) is None:
        extensions = " or ".join(f"data/{name}{ext}" for ext in DATASET_EXTENSIONS)
        fail(tutorial.path, f"declares datasets: {name}, and neither "
                            f"{extensions} exists.")
    if not (cfg.DATA / f"{name}.yaml").is_file():
        return None  # data_index() has said so; the Reference tab leaves it out
    data = read_dataset(name)
    if data is None:
        return None
    saved = long_date(datetime.date.fromisoformat(data["snapshot"]))
    # The Reference tab prints these as one sentence, so a field left blank
    # says so in words instead of leaving a gap in it.
    unsaid = {"source": "source not recorded", "license": "licence not recorded",
              "description": "No description recorded"}
    return {
        "name": name,
        **{f: str(data.get(f) or "").strip() or unsaid.get(f, "")
           for f in ("source", "url", "license", "description")},
        "saved": saved,
        "live": data["recipe"]["source"] if data.get("live") else None,
    }


def check_datasets(tutorial: Tutorial) -> list[dict]:
    """Every dataset this tutorial declares, with its attribution — checked
    and resolved together, since there is no use in resolving one without
    the other. Returns [] for a tutorial that declares none.

    A cell that loads a file from `data/` by name has to declare it, since
    the declaration is what puts the dataset inside the downloaded copy
    (standalone_html()): an undeclared load works on the site, and fails
    for a reader offline.
    """
    addresses = {entry["live"]["url"]: file_name
                 for file_name, entry in data_index().items() if entry.get("address")}
    for cell in tutorial.cells:
        if cell.type != "python":
            continue
        for code in [cell.code, *(s.code for s in cell.solutions)]:
            for match in LOAD_CALL.finditer(code):
                file_name = addresses.get(match.group("name"), match.group("name"))
                if file_name in data_index() and Path(file_name).stem not in tutorial.datasets:
                    fail(tutorial.path, f"cell {cell.id} loads {match.group('name')}, and "
                                        f"datasets: does not list {Path(file_name).stem}, "
                                        "so a downloaded copy would not carry it.")
    found = (dataset_attribution(tutorial, name) for name in tutorial.datasets)
    return [attribution for attribution in found if attribution is not None]


def standalone_data(tutorial: Tutorial) -> tuple[dict, dict]:
    """A downloaded page's datasets, carried inside it: the index entries
    of the ones it declares, and each snapshot gzipped and in base64. A
    page opened from disk cannot fetch its neighbours, and a page opened
    offline cannot fetch a live source, so this is the copy it falls back
    to in both cases."""
    index, files = {}, {}
    for name in tutorial.datasets:
        data_file = dataset_file(name)
        index[data_file.name] = data_index()[data_file.name]
        files[data_file.name] = base64.b64encode(
            gzip.compress(data_file.read_bytes(), mtime=0)).decode("ascii")
    return index, files


def resolve_links(tutorial: Tutorial, registry: dict[str, Tutorial]) -> str:
    """Rewrite tutorial:id#anchor into a real relative href, or fail.

    An id is site-wide (id_of()), so a link names one page and nothing has
    to be guessed: `tutorial:first-steps` is the same tutorial from any
    course. A link to an id this build has no page for stops the build
    rather than shipping a page that looks finished to everyone except the
    student who follows it. A link to a section the page no longer has is a
    note, and goes to the top of the page: the reader still arrives, and a
    teacher who cuts a section should not have to edit every page that
    pointed at it before theirs can go live.
    """

    def one(match: re.Match) -> str:
        slug, anchor = match.group("slug"), match.group("anchor")
        target = registry.get(slug)
        if target is None:
            known = ", ".join(sorted(registry)) or "none"
            fail(tutorial.path, f"link to unknown tutorial {slug!r} (built: {known})")
        if anchor and anchor not in target.anchors:
            note(tutorial.path, f"links to {slug}#{anchor}, and that tutorial has no section "
                                f"{anchor!r} now, so the link goes to the top of the page")
            anchor = ""
        href = os.path.relpath(target.out_path, tutorial.out_path.parent)
        return f'href="{href}#{anchor}"' if anchor else f'href="{href}"'

    return TUTORIAL_HREF_RE.sub(one, tutorial.body_html)


BIBLIOGRAPHY_RE = re.compile(r"read more", re.I)

TAG_RE = re.compile(r"<[^>]+>")


def origin_anchor(tutorial: Tutorial, term: str) -> str:
    """The section of `tutorial` a reader should land on for `term`, or "".

    Prefers the term's emphasised first use, since
    docs/WRITING_TUTORIALS.md#marking-a-term asks an author to italicise
    exactly that, and falls back to its first plain occurrence — a term
    introduced through a code cell rather than a sentence may never be
    italicised at all, and landing on the right section still beats landing
    on the page.

    Searched per `h2` section, against each section's *text* rather than its
    markup, which matters for both halves of that: a raw search over the HTML
    matches inside an `href` or a class name, and the nearest preceding
    heading of any level is usually "Your turn", which every tutorial has
    several of and none of which tells a reader where they are.
    """
    return _origin_anchor(tutorial.body_html, term)


# Every later page's glossary asks again where an earlier page introduced
# each of its terms, the same question with the same answer, and on the
# whole site that was a hundred thousand searches and most of a minute and
# a half. The answer depends only on the page's HTML and the term, so it is
# kept for each pair; build() clears it, like data_index().
@functools.lru_cache(maxsize=None)
def _origin_anchor(body: str, term: str) -> str:
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
                f"folder ({folder.relative_to(cfg.ROOT)}).",
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
    target = cfg.OUT / "tutorials" / tutorial.folder
    target.mkdir(parents=True, exist_ok=True)
    for asset in assets:
        shutil.copy2(asset, target / asset.name)


def load(path: Path) -> Tutorial:
    """`load_page()`, with the source map when it is on and safe.

    Safe means the page reads exactly as it would without the map: the mapped
    page, stripped of its `data-md` attributes, is the unmapped page. The
    tokenizer in source_map.py reads markdown from outside Python-Markdown, so
    a page whose markup it misreads would otherwise render differently. Such a
    page gets no map and a note, and is otherwise untouched.
    """
    if not cfg.SOURCE_MAP:
        return load_page(path, mapped=False)
    mapped = load_page(path, mapped=True)
    plain = load_page(path, mapped=False)
    if (source_map.strip(mapped.body_html) == plain.body_html
            and mapped.notes == plain.notes and mapped.toc == plain.toc):
        return mapped
    say(f"note: {path.relative_to(cfg.ROOT)}: the source map would change how the page "
          f"reads, so it has none")
    return plain


def load_page(path: Path, mapped: bool) -> Tutorial:
    """Turns one tutorial's source file into a fully-parsed `Tutorial`
    object — this is the one function that runs the whole parsing
    pipeline described at the top of this file, in order: split off the
    frontmatter, pull out cells/code-blocks/maths so Markdown can't
    mangle them, convert the remaining prose to HTML, put the cells and
    blocks back in, then pull out pedagogical notes. Every tutorial page
    build.py builds starts here.
    """
    text = path.read_text()
    meta, body = split_frontmatter(text, path)
    if mapped:
        body = source_map.mark(body, len(text) - len(body))
    body = expand_prose_includes(body, path)
    body = expand_snapshot_dates(body, meta, path)
    worlds = page_worlds(meta, path)
    spans = world_spans(body, path, worlds)
    projects = page_projects(meta, path)
    projects_at = project_spans(body, path, projects) if projects else {}
    (stripped, cells, blocks, hints, site_editors, questions, app_cells,
     solutions, inputs_blocks, challenges) = extract_blocks(body, path, spans)
    stripped, maths = extract_math(stripped)
    stripped = loosen_tight_lists(stripped)
    converted, toc = to_html(stripped)
    converted = place_hints(converted, hints, maths)
    converted = place_cell_blocks(converted, solutions, inputs_blocks, cells, maths)
    body_html = place_blocks(converted, cells, blocks, maths, site_editors, questions, app_cells,
                              page=id_of(path), version=str(meta.get("version", "")))
    body_html = place_challenges(body_html, challenges, id_of(path), str(meta.get("title", "")))
    body_html = place_worlds(body_html, spans, worlds, path)
    body_html = place_projects(body_html, projects, path)
    body_html, notes = extract_notes(body_html, path)
    if mapped:
        body_html = source_map.attach(body_html)
    if any(cell.predict for cell in cells):
        body_html += SURPRISES_HTML
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
        project_cells=project_cell_ids(body, projects_at, cells),
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
    path = cfg.ASSETS / name
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


def practice_link(tutorial: Tutorial, practice: list[Tutorial] | None,
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
    practice = practice or []
    if not practice and not also:
        return ""
    parts = ['<div class="dl-practice-link">']
    for page in practice:
        where = os.path.relpath(page.out_path, tutorial.out_path.parent)
        link = ("Practice problems for this tutorial" if len(practice) == 1
                else html.escape(page.title))
        parts.append(
            f'<p><a href="{where}">{link}</a> — '
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


def context_link(tutorial: Tutorial, context: list[Tutorial] | None = None,
                 registry: dict[str, Tutorial] | None = None) -> str:
    """The link between a tutorial and its context pages, in both directions.

    Placed as practice_link() places its own: on the tutorial at the end,
    after the practice link, one block per context page; on the context page
    at the top, naming every tutorial it is background for. Both say plainly
    that nothing on the context page is needed, so that a reader short of
    time can pass it by without worrying.
    """
    if tutorial.is_context:
        links = []
        for slug in tutorial.context_for:
            owner = (registry or {}).get(slug)
            if owner is None:
                continue
            where = os.path.relpath(owner.out_path, tutorial.out_path.parent)
            links.append(f'<a href="{where}">{html.escape(owner.title)}</a>')
        if not links:
            return ""
        named = links[0] if len(links) == 1 else ", ".join(links[:-1]) + " and " + links[-1]
        those = "that tutorial" if len(links) == 1 else "those tutorials"
        return (
            f'<p class="dl-context-back">Background for {named}. Nothing here '
            f"is needed to finish {those}.</p>"
        )
    parts = []
    for page in context or []:
        where = os.path.relpath(page.out_path, tutorial.out_path.parent)
        parts.append(
            f'<div class="dl-context-link"><p><a href="{where}">'
            f"{html.escape(page.title)}</a> — background reading, for when you "
            "want to know more. Nothing in it is needed to finish this "
            "tutorial.</p></div>"
        )
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
    path = cfg.ROOT / "planning" / FEEDBACK_CONFIG_FILE
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
    bottom-right of the screen, not a corner-dock tab — the same three doors as the footer's disclosure (report_doors_html()),
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
          practice: list[Tutorial] | None = None,
          registry: dict[str, Tutorial] | None = None,
          also: list[Tutorial] | None = None,
          context: list[Tutorial] | None = None,
          glossary: list[dict] | None = None,
          notes: list[dict] | None = None,
          datasets: list[dict] | None = None,
          groups: dict[tuple[str, str], list[Tutorial]] | None = None,
          members: list[Tutorial] | None = None,
          toolkit: list[dict] | None = None) -> Path:
    """Assembles and writes one finished tutorial page to disk: builds
    the JSON manifest that `assets/tutorial-runtime.js` reads on the
    page, fills the page shell template with the tutorial's own
    content and navigation, and writes the result under `site/`. This is
    the one function that turns a parsed `Tutorial` object plus all its
    surrounding context (its series, its glossary, its notes) into an
    actual HTML file a browser can open.
    """
    up = "../" * tutorial.depth
    body_html = body_html.replace(ROOT_HREF, f'href="{up}')
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
            # The comparison (#312) runs the first solution against the
            # inputs, and the reader's own tests from the cell that names
            # this one with `tests:`.
            | ({"solution": c.solutions[0].code} if c.solutions else {})
            | ({"inputs": [{"expr": case.expr, "label": case.label}
                           for case in c.inputs.cases]} if c.inputs else {})
            | ({"guess": True} if c.inputs and c.inputs.guess else {})
            | ({"typed": c.typed} if c.typed else {})
            | ({"tests": c.tested_by} if c.tested_by else {})
            | ({"predict": c.predict.type} if c.predict else {})
            for c in tutorial.cells
        ],
    }
    legacy = legacy_ids().get(tutorial.slug)
    if legacy:
        manifest["legacy"] = legacy
    if "data-md=" in body_html and tutorial.is_default:
        # What "Edit this page" needs (assets/inpage-edit.js): which file this
        # page came from, and the git blob it was built from, so the editor
        # reads exactly the bytes the page's block ranges point into.
        data = tutorial.path.read_bytes()
        manifest["edit"] = {
            "path": tutorial.path.relative_to(cfg.ROOT).as_posix(),
            "sha": hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(),
            "title": tutorial.title,
            "editor": versioned(f"{up}assets/", "vendor/milkdown.bundle.js"),
            "code": versioned(f"{up}assets/", "vendor/codemirror.bundle.js"),
            "module": versioned(f"{up}assets/", "inpage-edit.js"),
        }
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
    if toolkit:
        # Earlier pages' toolkit cells (toolkit_for()), loaded into this
        # page's namespace before its first cell runs.
        manifest["toolkit"] = toolkit
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
        "{{YEAR}}": html.escape(str(tutorial.meta.get("year") or ""), quote=True),
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
            crumb_trail_html(tutorial, groups, members, up, practice, registry, also,
                             context)
            if groups is not None
            else html.escape(" · ".join(filter(None, [course_title(tutorial.course) or "dewlab",
                                                     str(tutorial.meta.get("year") or "")])))
        ),
        "{{NAV_PREV_NEXT}}": nav,
        "{{PAGE_SCRIPT}}": "",
        "{{DOWNLOAD}}": download_section(tutorial),
        "{{BODY}}": (
            page_notice(tutorial, default)
            + (practice_link(tutorial, practice, registry, also)
               if tutorial.is_practice else "")
            + (context_link(tutorial, context, registry)
               if tutorial.is_context else "")
            + also_part_of(tutorial, body_html, up)
            + (practice_link(tutorial, practice, registry, also)
               + context_link(tutorial, context, registry)
               if not tutorial.is_companion else "")
        ),
        # `<` escaped so nothing in a cell can close the surrounding <script>.
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer(tutorial.slug, tutorial.meta["version"]),
        "{{REPORT_DOORS}}": report_doors_panel_html(tutorial.slug, tutorial.meta["version"]),
    }
    page = fill_shell(shell, tokens, "build.py")

    tutorial.out_path.parent.mkdir(parents=True, exist_ok=True)
    tutorial.out_path.write_text(page)
    return tutorial.out_path


# dewmark, the exam track, lived in dewmark/ and its marking workbench was
# published at /dewmark/ until it moved to its own repository and site.
# The old address is kept, as a redirect to
# dewmark's home page, for anyone who bookmarked it; the stub follows the
# compose/ redirects' pattern, keeping a query string and a #hash.
DEWMARK_HOME = "https://deweydex.github.io/dewmark/"
DEWMARK_REDIRECT = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>location.replace("{DEWMARK_HOME}" + location.search + location.hash);</script>
<meta http-equiv="refresh" content="0; url={DEWMARK_HOME}">
<link rel="canonical" href="{DEWMARK_HOME}">
<meta name="robots" content="noindex">
<title>This page has moved</title>
</head>
<body>
<p>dewmark, the exam tools, has moved to its own site. If it does not open
on its own, <a href="{DEWMARK_HOME}">open it here</a>.</p>
</body>
</html>
"""


# The site's own hand-written pages: each is `pages/<name>.md`, written
# to `<file>.html` at the site root, with the crumb the corner shows and
# the one link the bottom nav offers. The home page is the one every other
# page's masthead links to, so its crumb is empty and its file is index.html.
# Every file under `pages/` is optional, so a fork can keep the pages it wants
# and none of the others. The front page is the one a site cannot be without,
# since it is the page at the root, so a site with no `pages/home.md` gets
# this: the live search box and one card per course.
DEFAULT_HOME = '---\ntitle: "Home"\n---\n\n[[search-box]]\n\n[[course-cards]]\n'

SITE_PAGES: dict[str, tuple[str, str, str]] = {
    # name: (output file stem, crumb text, bottom-nav link)
    "home": ("index", "", '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>'),
    "about": ("about", "about", '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>'),
    "features": ("features", "features", '<a class="dl-nav-up" href="index.html">Home</a>'),
    "studying": ("studying", "studying here", '<a class="dl-nav-up" href="index.html">Home</a>'),
    "reading-helpers": ("reading-helpers", "reading helpers",
                        '<a class="dl-nav-up" href="index.html">Home</a>'),
}


def write_page(shell: str, name: str) -> Path | None:
    """One of the site's own pages — the home page, About, the features
    page, Studying here or Reading helpers — from `pages/<name>.md`, read
    through `read_page()`.

    Every one is optional. A page with no file is not written, and the one
    link the build adds to one itself, from the all-tutorials page to About,
    is left out too; returns None. A page's own links are its author's, so a
    link or card to a page this site does not have gets a note, not a
    refusal. The home page is the exception in the other direction: with no
    file it is built from `DEFAULT_HOME`, because the site needs a front page.

    A page is a hand-written markdown file with a `title` and nothing else
    in its frontmatter: no course, no version, no cells. `read_page()`
    converts its body the way a tutorial's prose converts, fills any
    `[[name]]` marker (`GENERATED_BLOCKS` — the live search box, the
    course cards) and any ```card fence, and this function only assembles
    the shell around what it returns. The pages differ in their file
    name, the crumb in the corner and the one link the bottom nav offers,
    which is what `SITE_PAGES` holds; everything else is the same, and was
    written out once per page before this function existed.

    Every word on these pages is student-facing: the plain-language rules
    in PEDAGOGICAL_STYLE_GUIDE.md#plain-language apply.
    """
    stem, crumb, nav = SITE_PAGES[name]
    if name != "home" and not (cfg.PAGES / f"{name}.md").is_file():
        return None
    meta, body = read_page(name)
    missing = {other_stem: other for other, (other_stem, _, _) in SITE_PAGES.items()
               if other != "home" and not (cfg.PAGES / f"{other}.md").is_file()}
    for target in sorted(set(re.findall(r'href="([\w-]+)\.html', body)) & set(missing)):
        note(cfg.PAGES / f"{name}.md", f"links to {target}.html, and this site has no "
                                   f"pages/{missing[target]}.md, so the link goes nowhere")
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
    page = fill_shell(shell, tokens, f"the {name} page")
    cfg.OUT.mkdir(parents=True, exist_ok=True)
    target = cfg.OUT / f"{stem}.html"
    target.write_text(page)
    return target


def write_site_pages(shell: str, names: tuple[str, ...]) -> list[Path]:
    """The pages among `names` that this site has, written."""
    pages = (write_page(shell, name) for name in names)
    return [page for page in pages if page is not None]


def write_all_tutorials_page(
    shell: str,
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path] | None = None,
    retired: dict[str, list[Tutorial]] | None = None,
    practice: dict[str, list[Tutorial]] | None = None,
    mixed: dict[str, list[Tutorial]] | None = None,
    course_archives: dict[str, Path] | None = None,
    context: dict[str, list[Tutorial]] | None = None,
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
            groups, archives, retired, practice, mixed, course_archives, context),
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("all-tutorials", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("all-tutorials", "1"),
    }
    page = fill_shell(shell, tokens, "the all-tutorials page")
    cfg.OUT.mkdir(parents=True, exist_ok=True)
    target = cfg.OUT / "all-tutorials.html"
    target.write_text(page)
    return target


def write_all_notes_page(shell: str, tutorials: list[Tutorial]) -> Path:
    """My Notes: every highlight and every page's own free-text notes,
    gathered from every tutorial this browser has ever saved progress
    for — into one page to review, search, or download as a plain-text
    study sheet (the highlight-colours-and-list entry).

    Nothing here comes from the build: localStorage is shared per
    origin, not per page, so `assets/my-notes.js` reads every saved
    record itself, client-side, once this page loads. The one thing the
    build *can* give it that storage can't is a title for each slug —
    a saved record only carries `tutorial-slug`, not a human title — so
    this bakes in a small {slug: title} map the same way tree.js reads
    its own topic-graph data island (`finding.write_tree_page()`).
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
    page = fill_shell(shell, tokens, "the my-notes page")
    cfg.OUT.mkdir(parents=True, exist_ok=True)
    target = cfg.OUT / "all-notes.html"
    target.write_text(page)
    return target


def course_card_order() -> list[Course]:
    """The courses in the order their front-page tiles appear: those
    `courses/index.yaml` names under `cards:` first, in that order, then
    the rest in `order:` order. Only the tiles — `order:` also decides
    each shared page's default course, so a card can move to the top
    without every page it shares changing its tree and previous/next."""
    found = courses()
    index = cfg.COURSES / COURSE_INDEX_FILE
    first: list[str] = []
    if index.is_file():
        first = (yaml.safe_load(index.read_text()) or {}).get("cards") or []
        if not isinstance(first, list) or not all(isinstance(c, str) for c in first):
            note(index, "needs `cards:` as a list of course ids, one per line, so the "
                        "tiles follow `order:`")
            first = []
        for name in first:
            if name not in found:
                note(index, f"lists {name} under `cards:`, and there is no "
                            f"courses/{name}.yaml, so it is left out")
        first = [name for name in dict.fromkeys(first) if name in found]
    return [found[c] for c in first] + [c for name, c in found.items() if name not in first]


def render_course_cards() -> str:
    """One front-page tile per course, in course_card_order(), from the
    course files: the title, the status badge, the QQI code, and the
    `card:` text. What `pages/home.md` used to hand-write six times over,
    now the `[[course-cards]]` generated block — so adding a course is a
    course file and one line in the index, and the front page follows.
    One `.dl-course-list` column rather than a `.dl-module-grid`: a
    course's card text is too long for two columns at the page's width."""
    return '<div class="dl-course-list">' + "".join(
        render_card(PageCard(
            url=f"{course.id}.html",
            heading=course.title,
            body_html=f"<p>{html.escape(course.card)}</p>" if course.card else "",
            status=course.status,
            meta=course.code or None,
            wide=False,
        ))
        for course in course_card_order()
    ) + "</div>"


def write_course_page(
    shell: str,
    course: Course,
    groups: dict[tuple[str, str], list[Tutorial]],
    archives: dict[tuple[str, str], Path],
    retired: dict[str, list[Tutorial]],
    practice: dict[str, list[Tutorial]],
    mixed: dict[str, list[Tutorial]],
    course_archives: dict[str, Path],
    context: dict[str, list[Tutorial]] | None = None,
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
        context=context,
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
    page = fill_shell(shell, tokens, "the course page")
    cfg.OUT.mkdir(parents=True, exist_ok=True)
    target = cfg.OUT / f"{course.id}.html"
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
    path = cfg.COURSES / REDIRECTS_FILE
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        fail(path, "is a mapping of old address to new address, one per line")
    written: list[Path] = []
    current = {page.resolve() for page in pages}
    for old, new in data.items():
        old, new = str(old), str(new)
        source, target = cfg.OUT / old, cfg.OUT / new
        if target.resolve() not in current:
            fail(path, f"sends {old} to {new}, and this build wrote no page at {new}")
        if source.resolve() in current:
            # The page that lives there now is the better answer, and nothing
            # a bookmark reaches is lost.
            note(path, f"sends {old} somewhere, but the build writes a page at {old}, so "
                       "the line is skipped. Delete it")
            continue
        href = os.path.relpath(target, source.parent).replace(os.sep, "/")
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(REDIRECT_PAGE.format(href=html.escape(href, quote=True)))
        written.append(source)
    return written


def write_routes(
    groups: dict[tuple[str, str], list[Tutorial]],
    practice: dict[str, list[Tutorial]],
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
                    "url": member.out_path.relative_to(cfg.OUT).as_posix(),
                }
                problems = practice.get(member.slug, [])
                if problems:
                    entry["practices"] = [{
                        "id": page.slug,
                        "title": page.title,
                        "url": page.out_path.relative_to(cfg.OUT).as_posix(),
                    } for page in problems]
                entries.append(entry)
            series.append({
                "key": key,
                "title": course.series_title(key),
                "url": f"{course.id}.html" + series_fragment(course, groups, key),
                "tutorials": entries,
            })
        routes.append({
            "id": course.id,
            "title": course.title,
            "url": f"{course.id}.html",
            "series": series,
            "mixed": [
                {"id": page.slug, "title": page.title,
                 "url": page.out_path.relative_to(cfg.OUT).as_posix()}
                for page in mixed.get(course.id, [])
            ],
        })
    target = cfg.OUT / "assets" / "routes.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"courses": routes}, ensure_ascii=False))
    return target


def warn_about_titles(tutorials: list[Tutorial]) -> None:
    """Two pages with one title: the build lets it through and says so. It
    is not wrong — two courses may each have a "Joins" — but it is worth a
    second look, and nothing else would ever mention it.
    """
    pages = [t for t in tutorials if t.is_default and not t.is_companion]
    by_title: dict[str, list[Tutorial]] = {}
    for page in pages:
        by_title.setdefault(page.title.strip().lower(), []).append(page)
    for members in by_title.values():
        if len(members) > 1:
            named = ", ".join(
                f"{m.path.relative_to(cfg.ROOT)} (on {', '.join(m.courses) or 'no course'})"
                for m in members
            )
            say(f'note: two pages share the title "{members[0].title}": {named}')


def shared_outcomes(claims: list[tuple[str, dict]]) -> list[str]:
    """Pairs of pages that say they teach three or more of the same outcomes,
    one line a pair. `claims` is each page's name and its `covers:`
    frontmatter. Coverage, not titles, is the signal that two pages may be
    one page written twice.

    A whole-site `python3 check.py` reports these. A build does not: nobody
    building a page can act on what two other pages have in common.
    """
    def outcomes(covers: dict) -> set[str]:
        return {code for claim in (covers or {}).values()
                for code in ((claim or {}).get("covers") or [])}

    covered = [(name, outcomes(covers)) for name, covers in claims]
    lines = []
    for index, (name, codes) in enumerate(covered):
        for other, other_codes in covered[index + 1:]:
            shared = sorted(codes & other_codes)
            if len(shared) >= 3:
                lines.append(f"{name} and {other} both cover {', '.join(shared)}")
    return lines


def load_all() -> list[Tutorial]:
    """Every page under `tutorials/`, drafts included: one folder per
    tutorial, holding `<id>.md`, its practice page and any frozen release.

    Two files claiming one id stop the build here, naming both — the
    filesystem already refuses a second folder with the same name, and
    this catches the other way it can happen, a practice file beside a
    folder of the same name. So does a main file that is not named for its
    folder: `tutorials/first-steps/steps.md` would be the tutorial `steps`,
    and every reader's saved work lives under `first-steps`. A page beside
    it is named for the folder and goes on (`first-steps-practice.md`).
    A markdown file loose under `tutorials/`, outside any folder, has no
    id: it is noted and not built, since it is a scratch file as often as a
    tutorial that forgot its folder.
    """
    for loose in sorted(cfg.TUTORIALS.glob("*.md")):
        note(loose, "is not inside a folder, so it is not built. A tutorial is "
                    "tutorials/<id>/<id>.md")
    everything = [load(p) for p in sorted(cfg.TUTORIALS.glob("*/*.md"))]
    claimed: dict[str, Tutorial] = {}
    for tutorial in everything:
        if VERSION_FILE_RE.match(tutorial.path.stem):
            continue
        folder, stem = tutorial.path.parent.name, tutorial.path.stem
        if stem != folder and not stem.startswith(f"{folder}-"):
            fail(tutorial.path, f"is called {stem}.md, so its id would be {stem}. A tutorial's id is "
                                f"its folder's name, and its main file is {folder}.md (a page "
                                f"beside it starts {folder}-). Rename the file back, or the "
                                "folder to match, before anyone has saved work under the id")
        other = claimed.get(tutorial.slug)
        if other is not None:
            fail(tutorial.path, f"has the id {tutorial.slug}, and so does "
                                f"{other.path.relative_to(cfg.ROOT)}. An id is site-wide; "
                                "rename one folder.")
        claimed[tutorial.slug] = tutorial
    return everything


@dataclass
class Site:
    """Every page, read and put in its place: what a build writes from, and
    what builder/solutions.py runs."""
    tutorials: list[Tutorial]          # every page that is not a draft, frozen releases included
    registry: dict[str, Tutorial]      # the current release of each, by id
    catalog: dict[str, "Course"]
    context: dict[str, list[Tutorial]]
    practice: dict[str, list[Tutorial]]
    mixed: object
    groups: dict[tuple[str, str], list[Tutorial]]


def read_site() -> Site:
    """Read every page and the courses, and work out where each page sits.
    Refuses what load() and the placing rules refuse; writes nothing."""
    everything = load_all()
    tutorials = versions_of([t for t in everything if t.status != "draft"])
    # Every file in data/ traced to its source, before any page uses one.
    # Read afresh on every build, since a test builds many repositories in
    # one process.
    read_dataset.cache_clear()
    data_index.cache_clear()
    _origin_anchor.cache_clear()
    solutions._tree_fingerprint.cache_clear()
    _relative_href.cache_clear()
    _GLOSSARIES.clear()
    data_index()

    registry: dict[str, Tutorial] = {t.slug: t for t in tutorials if t.is_default}

    catalog = courses()
    place_tutorials(tutorials, registry)
    context = context_pages(tutorials, registry)
    practice = practice_pairs(tutorials, registry)
    mixed = mixed_practice(tutorials, registry)
    # A frozen release sits where its current one does.
    for tutorial in tutorials:
        if not tutorial.is_default and tutorial.slug in registry:
            tutorial.placements = list(registry[tutorial.slug].placements)
    return Site(tutorials, registry, catalog, context, practice, mixed, series_of(tutorials))


def build(clean: bool = False, standalone: bool = False) -> list[Path]:
    """Build the site. `standalone` also writes the downloadable single files,
    which need the real assets on disk and are the slow part of a build."""
    if not cfg.SHELL.is_file():
        raise BuildError(f"no shell template at {cfg.SHELL.relative_to(cfg.ROOT)}")
    if clean and cfg.OUT.exists():
        shutil.rmtree(cfg.OUT)

    _NOTED.clear()  # once per build; a test builds many sites in one process
    _NOTE_LINES.clear()
    site = read_site()
    tutorials, registry, catalog = site.tutorials, site.registry, site.catalog
    context, practice, mixed, groups = site.context, site.practice, site.mixed, site.groups

    families: dict[str, list[Tutorial]] = {}
    for tutorial in tutorials:
        families.setdefault(tutorial.slug, []).append(tutorial)

    shell = cfg.SHELL.read_text()
    retired = archived_of(tutorials)
    warn_about_titles(tutorials)
    for tutorial in tutorials:
        if (tutorial.is_default and not tutorial.is_companion and not tutorial.placements
                and catalog and tutorial.status == "live"):
            say(f"note: no course lists {tutorial.slug}. It builds at "
                  f"tutorials/{tutorial.slug}.html, and nothing links to it — add "
                  "its id to a course file under courses/ when it is ready.")
    for tutorial in tutorials:
        check_alt_text(tutorial)
        check_folds(tutorial)
    toolkits = [toolkit_for(tutorial, registry, groups) for tutorial in tutorials]
    written: list[Path] = []
    for tutorial, toolkit in zip(tutorials, toolkits):
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
            # A mixed set that several courses list is one page, so it is
            # one link, however many courses name it.
            also=list({page.slug: page for pages in mixed.values() for page in pages
                       if tutorial.slug in page.practice_across}.values()),
            context=context.get(tutorial.slug),
            registry=registry,
            glossary=cumulative_glossary(tutorial, registry, groups),
            toolkit=toolkit,
            notes=[{"id": n.id, "html": n.html} for n in tutorial.notes],
            datasets=check_datasets(tutorial),
            groups=groups,
            members=members,
        )
        written.append(page_path)
        # 0.7MB against 19KB for the hosted page, so only the version students
        # are actually being given is worth building forty times over.
        if standalone and tutorial.is_default:
            written.append(downloads.write_standalone(tutorial, page_path.read_text()))

    archives: dict[tuple[str, str], Path] = {}
    course_archives: dict[str, Path] = {}
    if standalone:
        # Compressing is nearly all of what an archive costs, and zlib lets go
        # of the interpreter while it compresses, so the archives are written
        # side by side, one per core. Each is a file of its own, written by one
        # thread from start to finish, so the bytes are the same either way.
        series_jobs: dict[tuple[str, str], concurrent.futures.Future] = {}
        course_jobs: dict[str, concurrent.futures.Future] = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as pool:
            for course in catalog.values():
                series_in_order: list[tuple[str, str, list[Tutorial]]] = []
                for key in course.keys:
                    members = groups.get((course.id, key))
                    if not members:
                        continue
                    title = course.series_title(key)
                    series_jobs[(course.id, key)] = pool.submit(
                        downloads.write_series_zip, course.id, key, members, practice, title
                    )
                    series_in_order.append((key, title, members))
                if series_in_order or mixed.get(course.id):
                    course_jobs[course.id] = pool.submit(
                        downloads.write_course_zip, course.id, course.title, series_in_order,
                        practice, mixed.get(course.id, []),
                    )
        archives = {key: job.result() for key, job in series_jobs.items()}
        course_archives = {key: job.result() for key, job in course_jobs.items()}
        written.extend(archives.values())
        written.extend(course_archives.values())

    if tutorials:
        written.extend(write_site_pages(shell, ("home", "features")))
        written.append(write_all_tutorials_page(
            shell, groups, archives, retired, practice, mixed, course_archives,
            context,
        ))
        written.append(write_all_notes_page(shell, tutorials))
        for course in catalog.values():
            written.append(write_course_page(
                shell, course, groups, archives, retired, practice, mixed,
                course_archives, context,
            ))
        tree = finding.write_tree_page(shell, tutorials)
        if tree is not None:
            written.append(tree)
        if (cfg.ROOT / "map" / "graph.json").is_file():
            written.append(finding.write_map_page(shell, registry, catalog))
        topics_page = finding.write_topics_page(shell, registry, practice, context)
        if topics_page is not None:
            written.append(topics_page)
        written.extend(write_site_pages(shell, ("about", "studying", "reading-helpers")))
        written.extend(write_redirects(written))

    cfg.OUT.mkdir(parents=True, exist_ok=True)
    shutil.rmtree(cfg.OUT / "assets", ignore_errors=True)
    shutil.copytree(cfg.ASSETS, cfg.OUT / "assets", ignore=shutil.ignore_patterns("shell.html"))
    if cfg.DATA.is_dir():
        shutil.rmtree(cfg.OUT / "data", ignore_errors=True)
        shutil.copytree(cfg.DATA, cfg.OUT / "data")
        write_data_index(cfg.OUT / "data")

    if tutorials:
        written.append(finding.write_reference_index(tutorials))
        written.append(write_routes(groups, practice, mixed))

    # The Notebook and the Workspace (compose/) are their own small folder
    # rather than more root-level files, so it copies wholesale like assets/
    # does, COMPOSE_REDIRECTS included.
    if cfg.COMPOSE.is_dir():
        shutil.rmtree(cfg.OUT / "compose", ignore_errors=True)
        shutil.copytree(cfg.COMPOSE, cfg.OUT / "compose")

    # The old address of dewmark's marking workbench, now a redirect.
    shutil.rmtree(cfg.OUT / "dewmark", ignore_errors=True)
    (cfg.OUT / "dewmark").mkdir(parents=True)
    (cfg.OUT / "dewmark" / "index.html").write_text(DEWMARK_REDIRECT)

    if cfg.TOPIC_GAME.is_dir():
        shutil.rmtree(cfg.OUT / "topic_tree_game", ignore_errors=True)
        shutil.copytree(cfg.TOPIC_GAME, cfg.OUT / "topic_tree_game",
                        ignore=shutil.ignore_patterns("README.md"))

    # And the topic editor, on the same terms: reached by typing
    # /topic_editor/, for whoever is drawing the graph, and never linked.
    if cfg.TOPIC_EDITOR.is_dir():
        shutil.rmtree(cfg.OUT / "topic_editor", ignore_errors=True)
        shutil.copytree(cfg.TOPIC_EDITOR, cfg.OUT / "topic_editor",
                        ignore=shutil.ignore_patterns("README.md"))

    if standalone:
        dewmini_bundle_dir = downloads.write_dewmini_bundle()
        if dewmini_bundle_dir is not None:
            written.append(dewmini_bundle_dir)
            written.append(downloads.zip_directory(dewmini_bundle_dir, cfg.OUT / "download" / "notebook.zip"))

    coi_src = cfg.ASSETS / "vendor" / "coi-serviceworker.js"
    if coi_src.exists():
        shutil.copy2(coi_src, cfg.OUT / "coi-serviceworker.js")

    if tutorials:
        written.append(finding.write_search_index(tutorials, registry, groups))
    return written


def _reference_index_for_bundle(target: Path) -> None:
    """Copies the generated reference index into an offline bundle.

    It needs its own step because it is *generated* rather than checked
    in: DEWMINI_ASSET_FILES names files copied out of the source
    `assets/`, and this one only exists under `OUT` once
    finding.write_reference_index() has run. Silently skipped when it isn't
    there — a build with no tutorials in it writes no index, and that
    should still produce a working bundle (just one whose Library says
    the reference is unavailable rather than showing an empty list).
    """
    source = cfg.OUT / "assets" / "reference-index.json"
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
    parser = argparse.ArgumentParser(
        description="Turn the markdown in tutorials/ into the site in site/.",
        epilog="python3 build.py --serve     build, then look at the site in a browser\n"
               "python3 build.py --clean     start again from nothing\n"
               "python3 check.py tutorials/<id>   check one tutorial, and run its solutions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--clean", action="store_true", help="remove site/ before building")
    parser.add_argument(
        "--no-standalone",
        action="store_true",
        help="skip the downloadable single-file copies, which are the slow part",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="after building, show the site at http://localhost:8000/ until Ctrl-C. "
             "The downloadable copies are skipped, so a Download link on a page "
             "does not work in the preview",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="the port --serve uses (default 8000)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="print a line for every page written, and each note as it happens "
             "(by default there is one summary line, then the notes together)",
    )
    parser.add_argument(
        "--no-source-map",
        action="store_true",
        help="leave out the markdown range each block of a page carries (what "
             "\"Edit this page\" reads); a page is about 0.1%% smaller and a build about 14 seconds quicker",
    )
    args = parser.parse_args()
    cfg.SOURCE_MAP = not args.no_source_map
    cfg.NOTES_AT_END = not args.verbose
    try:
        written = build(clean=args.clean, standalone=not (args.no_standalone or args.serve))
    except BuildError as exc:
        print_notes()
        print(f"build failed — {exc}", file=sys.stderr)
        return 1
    if not written:
        print("nothing to build: tutorials/ holds no .md files")
        return 0
    if args.verbose:
        for path in written:
            print(f"wrote {path.relative_to(cfg.ROOT)}")
    print(f"{len(written)} page{'s' if len(written) != 1 else ''} into {cfg.OUT.relative_to(cfg.ROOT)}/")
    print_notes()
    if args.serve:
        return serve.run(cfg.OUT, args.port)
    return 0


def print_notes() -> None:
    """The notes a command-line build gathered, together and after the
    summary, so a teacher reading the end of the output sees every place the
    build carried on and what it did."""
    if not _NOTE_LINES:
        return
    many = len(_NOTE_LINES)
    print(f"\n{many} note{'s' if many != 1 else ''}: the build carried on, and says what it did.",
          file=sys.stderr)
    for line in _NOTE_LINES:
        print("  " + line.removeprefix("note: "), file=sys.stderr)


# The tree, the map, Browse by topic and the indexes (finding.py), what a
# reader can download (downloads.py), and running a page's solutions
# (solutions.py, which a build does not call). Imported last because those modules
# take their helpers from this one. A name this
# module no longer has is looked for there, so `build.load_topics()` and the
# like still work for the scripts and tests that call them.
from builder import downloads, finding, serve, solutions  # noqa: E402


def __getattr__(name: str):
    for module in (finding, downloads, solutions, serve):
        if hasattr(module, name):
            return getattr(module, name)
    raise AttributeError(f"module 'build' has no attribute {name!r}")
