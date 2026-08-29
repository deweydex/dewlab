#!/usr/bin/env python3
"""Convert Jupyter notebooks into dewlab tutorials.

A notebook and a dewlab tutorial are close cousins: prose interleaved with code
that a student runs. The differences are what this script handles.

  * Markdown cells become prose, unchanged.
  * Code cells become `exec` fences with a stable id.
  * Saved outputs are dropped. dewlab re-runs everything in the reader's own
    browser, so a stored output is at best redundant and at worst a stale
    answer to a question the code no longer asks.
  * IPython magics and shell escapes are dropped, with a note in the report.
    `%matplotlib inline` and `!pip install …` are notebook-server instructions;
    in dewlab the first is unnecessary and the second cannot work.

What it will not do is invent frontmatter it cannot know. `module`, `series`
and `year` are yours to supply; `title` comes from the notebook's first
heading, and `order` from the number in its filename where there is one.

    python3 dev/from_notebook.py notebooks/*.ipynb \\
        --module mit-pdp-maths-prog-integration \\
        --series maths-and-programming \\
        --year 2026-2027

Writes into tutorials/<module>/ unless --out says otherwise. Existing files are
left alone unless --force.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MAGIC_RE = re.compile(r"^\s*[%!]")
HEADING_RE = re.compile(r"^#{1,6}\s+(?P<text>.+?)\s*#*\s*$", re.MULTILINE)
LEADING_NUMBER_RE = re.compile(r"(?<!\d)(\d{1,3})(?!\d)")
FENCE_RE = re.compile(r"^\s*```", re.MULTILINE)


def today_release() -> str:
    """A converted notebook's first release, dated today.

    A version is a release date now, not a counter (planning/VERSIONS.md), and
    a notebook arriving from everlearning is being released for the first time
    on the day it is converted."""
    return datetime.date.today().strftime("%Y.%m.%d") + ".1"


class ConversionError(Exception):
    """The notebook cannot be converted without a decision from a person."""


@dataclass
class Result:
    path: Path
    slug: str
    title: str
    order: int
    cells: int
    prose_blocks: int
    notes: list[str] = field(default_factory=list)


def slugify(text: str) -> str:
    """Turns arbitrary text into a URL/filename-safe slug: lowercase,
    punctuation removed, and runs of spaces or underscores collapsed into
    a single hyphen. `"My Cool Title!"` becomes `"my-cool-title"`. Falls
    back to `"untitled"` if that leaves nothing at all (an empty or
    entirely-punctuation title).
    """
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_]+", "-", text).strip("-") or "untitled"


def source_of(cell: dict) -> str:
    """Reads one notebook cell's source, handling nbformat's own choice
    of representation: a cell's `source` can be stored as either one
    plain string or a list of individual line-strings (see
    `docs/dewmini-js-explained.md`'s note on `handleImportFile` for the
    same ambiguity, handled the same way, on the JavaScript side). This
    accepts either and always returns one plain string either way.
    """
    source = cell.get("source", "")
    return source if isinstance(source, str) else "".join(source)


def strip_magics(code: str, notes: list[str]) -> str:
    """Drop IPython magics and shell escapes, saying which were dropped."""
    kept = []
    for line in code.split("\n"):
        if MAGIC_RE.match(line) and line.strip() not in ("%", "!"):
            notes.append(f"dropped notebook-only line: {line.strip()}")
            continue
        kept.append(line)
    return "\n".join(kept).strip("\n")


def title_of(cells: list[dict], fallback: str) -> str:
    """Finds the notebook's title by looking for its first Markdown
    heading (`#`, `##`, and so on) among the cells, in order — a notebook
    conventionally opens with a `# Title` cell, the same way a dewlab
    tutorial does. If nothing looks like a heading anywhere, `fallback`
    (the notebook's own filename, cleaned up) is used instead, so every
    converted tutorial gets *some* title rather than a build failure.
    """
    for cell in cells:
        if cell.get("cell_type") != "markdown":
            continue
        match = HEADING_RE.search(source_of(cell))
        if match:
            return re.sub(r"\s+", " ", match.group("text")).strip()
    return fallback


def order_of(stem: str, default: int) -> int:
    """Reads a leading number out of a notebook's filename (e.g.
    `"03_loops.ipynb"` -> 3) to use as its reading-order position, since
    many notebook collections are already numbered that way by
    convention. Falls back to `default` (the notebook's position in the
    command-line arguments, 1-indexed) when the filename doesn't have one.
    """
    match = LEADING_NUMBER_RE.search(stem)
    return int(match.group(1)) if match else default


def cell_id(heading: str | None, used: dict[str, int]) -> str:
    """A readable id, derived from the section the cell sits under.

    Ids are what saved progress matches on, so they matter beyond tidiness: a
    positional id silently rebinds a student's work to a different cell the
    first time one is inserted above it. Deriving from the heading keeps them
    meaningful, and the counter keeps them unique.
    """
    base = slugify(heading) if heading else "cell"
    used[base] = used.get(base, 0) + 1
    return f"{base}-{used[base]}"


def convert(
    notebook: Path,
    *,
    module: str,
    series: str,
    year: str,
    default_order: int = 1,
) -> tuple[str, Result]:
    """Converts one notebook file into a dewlab tutorial's Markdown text,
    and a `Result` summarizing what happened (for the report `main()`
    prints). This is the heart of the whole script: it walks the
    notebook's cells in order, turning a Markdown cell into prose and a
    code cell into an `exec` fence (dropping IPython magics/shell
    escapes along the way, via `strip_magics`), and builds up the
    tutorial's frontmatter and body as it goes. Raises `ConversionError`
    for anything this script genuinely can't handle on its own — not a
    bug to fix here, but a case that needs a person's judgment (see the
    module's own top docstring for what those cases are).
    """
    try:
        data = json.loads(notebook.read_text())
    except json.JSONDecodeError as exc:
        raise ConversionError(f"{notebook.name}: not valid notebook JSON — {exc}") from exc

    cells = data.get("cells")
    if not isinstance(cells, list):
        raise ConversionError(f"{notebook.name}: no cells — is this a notebook?")

    notes: list[str] = []
    slug = slugify(re.sub(r"^(SOLUTION_)?", "", notebook.stem))
    title = title_of(cells, notebook.stem.replace("_", " "))
    order = order_of(notebook.stem, default_order)

    body: list[str] = []
    used: dict[str, int] = {}
    heading: str | None = None
    exec_cells = 0
    prose_blocks = 0

    for cell in cells:
        kind = cell.get("cell_type")
        source = source_of(cell).strip("\n")
        if not source.strip():
            continue

        if kind == "markdown":
            match = None
            for match in HEADING_RE.finditer(source):
                pass
            if match:
                heading = match.group("text")
            body.append(source)
            prose_blocks += 1
            if "attachment:" in source:
                notes.append(
                    "markdown cell references an embedded attachment; "
                    "the image needs extracting into data/ by hand"
                )
        elif kind == "code":
            code = strip_magics(source, notes)
            if not code.strip():
                notes.append("dropped a code cell that was only magics")
                continue
            if FENCE_RE.search(code):
                raise ConversionError(
                    f"{notebook.name}: a code cell contains a ``` fence, which "
                    "cannot be nested inside the fence this would write"
                )
            body.append(
                f"```python exec\nid: {cell_id(heading, used)}\n{code}\n```"
            )
            exec_cells += 1
        # Raw cells carry notebook-specific formatting; nothing to translate.
        elif kind == "raw":
            notes.append("skipped a raw cell")

    frontmatter = "\n".join(
        [
            "---",
            f'title: "{title.replace(chr(34), chr(39))}"',
            f"slug: {slug}",
            f"module: {module}",
            f'year: "{year}"',
            f"series: {series}",
            f"version: {today_release()}",
            "---",
        ]
    )
    text = frontmatter + "\n\n" + "\n\n".join(body) + "\n"
    return text, Result(
        path=notebook,
        slug=slug,
        title=title,
        order=order,
        cells=exec_cells,
        prose_blocks=prose_blocks,
        notes=notes,
    )


def shown(path: Path) -> str:
    """A path to print. Relative to the repository where it is inside it, and
    absolute where it is not.

    `--out` is a documented option and may point anywhere. Reporting through
    `relative_to` alone wrote every file and then crashed on the line saying so,
    which is the worst order to fail in: the work is done and the run looks like
    it failed.
    """
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    """The command-line entry point: parses arguments, converts every
    notebook given on the command line (via `convert()` above), and
    writes each result to a `.md` file under `tutorials/<module>/` — one
    tutorial per notebook — printing a short report of what was written,
    what was skipped, and why. A notebook that fails to convert doesn't
    stop the whole run; it's reported and the rest continue, so one bad
    file in a batch of many doesn't block all the others.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="+", type=Path)
    parser.add_argument("--module", required=True, help="module slug, and the folder name")
    parser.add_argument("--series", required=True)
    parser.add_argument("--year", default="2026-2027")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args()

    out_dir = args.out or (ROOT / "tutorials" / args.module)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    for index, notebook in enumerate(sorted(args.notebooks), start=1):
        try:
            text, result = convert(
                notebook,
                module=args.module,
                series=args.series,
                year=args.year,
                default_order=index,
            )
        except ConversionError as exc:
            print(f"skipped — {exc}", file=sys.stderr)
            continue

        target = out_dir / f"{result.slug}.md"
        if target.exists() and not args.force:
            print(f"exists, left alone: {shown(target)}")
            continue
        target.write_text(text)
        written += 1
        print(
            f"{shown(target)}  "
            f"order {result.order}, {result.cells} cells, {result.prose_blocks} prose blocks"
        )
        for note in dict.fromkeys(result.notes):
            print(f"    note: {note}")

    print(f"\n{written} tutorial{'s' if written != 1 else ''} written to {out_dir}")
    print("Run `python3 build.py` next — it will refuse anything that does not resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
