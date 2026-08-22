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
import html
import json
import os
import re
import shutil
import sys
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


def write(tutorial: Tutorial, shell: str, body_html: str) -> Path:
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
        "{{NAV_PREV_NEXT}}": "",  # Phase 3 fills this.
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


def build(clean: bool = False) -> list[Path]:
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
    written: list[Path] = []
    for tutorial in tutorials:
        check_alt_text(tutorial)
        written.append(write(tutorial, shell, resolve_links(tutorial, registry)))

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
    args = parser.parse_args()
    try:
        written = build(clean=args.clean)
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
