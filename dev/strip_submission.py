#!/usr/bin/env python3
"""Strip a student's submission down to what the student wrote, and make a
marking copy of it as a PDF.

An assessment notebook is a blank template (the brief, the instructions, the
data, the empty answer cells) that students fill in. The template is therefore
already the specification of what counts as teacher material: any cell of a
submission that is still identical to a template cell is the teacher's, and
anything else is the student's. No per-assignment configuration is needed
beyond the template itself, and an optional rubric.

    python3 dev/strip_submission.py init-rubric template.ipynb > rubric.yaml
    python3 dev/strip_submission.py strip template.ipynb subs/*.ipynb subs/*.py \\
        --rubric rubric.yaml --out marking/

For each submission this writes, into --out,

  <name>.stripped.ipynb (or .py)   the student's cells, plus the headings
                                   named in the rubric, annotated with marks
  <name>.marking.pdf               the same, led by a points table and with a
                                   wide right margin for writing on

and prints what it dropped, kept and flagged. The rule is fail-safe: a cell is
dropped only on an exact match with a template cell (ignoring whitespace), so
a surprise leaves too much in, never too little. Cells that are close to a
template cell but not the same are kept and flagged, as is any edit to a cell
the template marked "do not change".

The PDF goes through LaTeX (XeLaTeX, via nbconvert and pandoc), so a student's
own `$x^2$` typesets as maths and non-ASCII text survives. Needs:
    pip install nbconvert nbformat pyyaml ipython
    apt-get install pandoc texlive-xetex texlive-fonts-recommended \\
        texlive-plain-generic texlive-latex-extra
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import nbformat
import yaml

HERE = Path(__file__).resolve().parent
TEMPLATE_DIRS = [str(HERE / "strip_submission_templates")]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
PERCENT_MARKER_RE = re.compile(r"^\s*#\s*%%(.*)$")
NEAR_MATCH = 0.6


class StripError(Exception):
    """Something needs a person: an unreadable file, a malformed rubric."""


# ---------------------------------------------------------------- reading

def read_percent_py(text: str) -> nbformat.NotebookNode:
    """A `# %%` file as a notebook. Text before the first marker is code, a
    `[markdown]` or `[md]` marker makes a note whose lines lose their `# `."""
    cells = []
    kind, buffer = None, []

    def flush():
        nonlocal buffer
        if kind is None and not "".join(buffer).strip():
            buffer = []
            return
        if kind == "markdown":
            lines = [ln[2:] if ln.startswith("# ") else ln[1:] if ln.startswith("#") else ln
                     for ln in buffer]
            cells.append(nbformat.v4.new_markdown_cell("\n".join(lines).strip("\n")))
        else:
            cells.append(nbformat.v4.new_code_cell("\n".join(buffer).strip("\n")))
        buffer = []

    for line in text.splitlines():
        marker = PERCENT_MARKER_RE.match(line)
        if marker:
            flush()
            kind = "markdown" if re.search(r"\[(markdown|md)\]", marker.group(1), re.I) else "code"
            continue
        buffer.append(line)
    flush()
    return nbformat.v4.new_notebook(cells=cells)


def load(path: Path) -> nbformat.NotebookNode:
    try:
        if path.suffix.lower() == ".py":
            return read_percent_py(path.read_text(encoding="utf-8"))
        return nbformat.read(str(path), as_version=4)
    except Exception as exc:  # unreadable JSON, bad encoding, missing file
        raise StripError(f"{path.name}: cannot be read — {exc}") from exc


def write_percent_py(nb: nbformat.NotebookNode, path: Path) -> None:
    out = []
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            out.append("# %% [markdown]")
            out.extend(f"# {ln}" if ln else "#" for ln in cell.source.split("\n"))
        elif cell.cell_type == "code":
            out.append("# %%")
            out.append(cell.source)
        out.append("")
    path.write_text("\n".join(out), encoding="utf-8")


# --------------------------------------------------------------- matching

def normal(cell) -> str:
    """A cell's identity for matching: its type and its text, with trailing
    spaces, line endings and non-breaking spaces ignored."""
    text = cell.source.replace(" ", " ").replace("\r\n", "\n")
    lines = [ln.rstrip() for ln in text.strip().split("\n")]
    return f"{cell.cell_type}\n" + "\n".join(lines)


def headings_of(source: str):
    """(level, text) for each heading line of a Markdown source, skipping
    anything inside a fenced block, where `#` is a comment, not a heading."""
    in_fence = False
    for line in source.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        match = None if in_fence else HEADING_RE.match(line)
        if match:
            yield len(match.group(1)), match.group(2)


def heading_key(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[`*_]", "", text)).strip().lower()


# ----------------------------------------------------------------- rubric

@dataclass
class Rubric:
    title: str = ""
    parts: list[dict] = field(default_factory=list)

    @property
    def marks_by_heading(self) -> dict[str, object]:
        return {heading_key(p["heading"]): p.get("marks") for p in self.parts}


def load_rubric(path: Path | None) -> Rubric | None:
    if path is None:
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        raise StripError(f"{path.name}: cannot be read — {exc}") from exc
    parts = data.get("parts")
    if not isinstance(parts, list) or not all(isinstance(p, dict) and p.get("heading") for p in parts):
        raise StripError(f"{path.name}: `parts` must be a list, each with a `heading`")
    for part in parts:
        criteria = part.get("criteria") or []
        given = [c.get("marks") for c in criteria]
        if criteria and part.get("marks") is not None and None not in given \
                and sum(given) != part["marks"]:
            raise StripError(
                f"{path.name}: criteria under '{part['heading']}' add to {sum(given)}, "
                f"not {part['marks']}")
    return Rubric(title=str(data.get("title") or ""), parts=parts)


def init_rubric(template: Path) -> str:
    """A rubric skeleton from the template's own headings, marks left empty
    for a person to fill in. Nothing is guessed."""
    nb = load(template)
    lines = ["# Marks for each part. `marks: null` means not yet decided.",
             "# A part's heading is kept in the marking copy and shown with its marks;",
             "# delete a part to leave its heading out.", ""]
    title = next((t for c in nb.cells if c.cell_type == "markdown"
                  for lvl, t in headings_of(c.source) if lvl == 1), "")
    lines.append(f"title: {json.dumps(title, ensure_ascii=False)}")
    lines.append("parts:")
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        for level, text in headings_of(cell.source):
            if level == 2:
                lines.append(f"  - heading: {json.dumps(text, ensure_ascii=False)}")
                lines.append("    marks: null")
                lines.append("    criteria: []   # e.g. - {for: Pseudocode, marks: 2}")
            elif level == 3:
                lines.append(f"    # sub-heading in the template: {text}")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ strip

@dataclass
class Report:
    name: str
    kept: int = 0
    dropped: int = 0
    headings: int = 0
    flags: list[str] = field(default_factory=list)


def annotate_headings(source: str, marks: dict[str, object]) -> str:
    """Appends `(n marks)` to any heading line the rubric knows about."""
    def one(line: str) -> str:
        match = HEADING_RE.match(line)
        if not match:
            return line
        value = marks.get(heading_key(match.group(2)))
        if value is None or "mark" in line.lower().rsplit("(", 1)[-1]:
            return line
        return f"{line.rstrip()} *({value} mark{'s' if value != 1 else ''})*"
    out, in_fence = [], False
    for line in source.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
        out.append(line if in_fence else one(line))
    return "\n".join(out)


def strip(template: nbformat.NotebookNode, submission: nbformat.NotebookNode,
          rubric: Rubric | None, name: str) -> tuple[nbformat.NotebookNode, Report]:
    report = Report(name)
    marks = rubric.marks_by_heading if rubric else {}
    seen_headings: set[str] = set()

    template_cells = [c for c in template.cells if c.source.strip()]
    exact = {normal(c) for c in template_cells}
    do_not_change = [c for c in template_cells if c.cell_type == "code"
                     and re.search(r"do not change", c.source, re.I)]

    def wanted(level: int, text: str) -> bool:
        return heading_key(text) in marks if rubric else level <= 2

    out = []
    for cell in submission.cells:
        if not cell.source.strip():
            continue  # a blank cell is nobody's work

        if normal(cell) in exact:
            report.dropped += 1
            if cell.cell_type == "markdown":
                # The teacher's cell goes; its question headings stay.
                keep = [f"{'#' * lvl} {txt}" for lvl, txt in headings_of(cell.source)
                        if wanted(lvl, txt)]
                if keep:
                    text = annotate_headings("\n\n".join(keep), marks)
                    out.append(nbformat.v4.new_markdown_cell(text))
                    seen_headings.update(heading_key(h.lstrip("# ")) for h in keep)
                    report.headings += len(keep)
            continue

        # The student's: kept whole. Flag it if it is close to a teacher cell.
        best, best_ratio = None, 0.0
        for t in template_cells:
            if t.cell_type != cell.cell_type:
                continue
            ratio = difflib.SequenceMatcher(None, normal(t), normal(cell)).ratio()
            if ratio > best_ratio:
                best, best_ratio = t, ratio
        if best is not None and best_ratio >= NEAR_MATCH:
            first = next((ln for ln in best.source.strip().split("\n") if ln.strip()), "")[:50]
            reason = "edited a cell marked do-not-change" if best in do_not_change \
                else "edited from a template cell"
            report.flags.append(f"{reason} ({int(best_ratio * 100)}% like '{first}')")

        copy = nbformat.v4.new_markdown_cell(cell.source) if cell.cell_type == "markdown" \
            else nbformat.from_dict(cell)
        if cell.cell_type == "markdown":
            for _lvl, txt in headings_of(cell.source):
                seen_headings.add(heading_key(txt))
            copy.source = annotate_headings(cell.source, marks)
        out.append(copy)
        report.kept += 1

    unshowable = sorted({ch for c in out for ch in c.source
                         if ord(ch) >= 0x2E80 or 0x1F000 <= ord(ch) <= 0x1FAFF})
    if unshowable:
        report.flags.append(
            "characters the PDF font may not show (they print as blanks): "
            + "".join(unshowable[:12]))

    if rubric:
        for part in rubric.parts:
            if heading_key(part["heading"]) not in seen_headings:
                report.flags.append(f"rubric heading not found in the result: {part['heading']}")

    result = nbformat.v4.new_notebook(cells=out, metadata=submission.metadata)
    return result, report


# ----------------------------------------------------------------- output

def marks_table(rubric: Rubric) -> str:
    """The points table for the cover page: what each part is for and how
    many marks it carries, with a column left empty to write the mark in."""
    rows = []
    total, known = 0, True
    for part in rubric.parts:
        value = part.get("marks")
        total += value or 0
        known = known and value is not None
        criteria = part.get("criteria") or []
        if criteria:
            rows.append((f"**{part['heading']}**", "", "" if value is None else f"**{value}**", ""))
            rows.extend(("", c.get("for", ""), "" if c.get("marks") is None else str(c["marks"]), "")
                        for c in criteria)
        else:
            rows.append((f"**{part['heading']}**", "", "" if value is None else str(value), ""))
    rows.append(("**Total**", "", str(total) if known else "", ""))
    lines = ["| Part | Awarded for | Marks | Mark given |",
             "|:------------------------------------------|:------------------------------|----:|-------:|"]
    lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
    return "\n".join(lines)


def cover_cell(name: str, rubric: Rubric | None):
    title = (rubric.title if rubric and rubric.title else "Marking copy")
    text = f"# {title}\n\n**Submission:** `{name}`"
    if rubric:
        text += "\n\n" + marks_table(rubric)
    return nbformat.v4.new_markdown_cell(text)


def write_pdf(nb: nbformat.NotebookNode, name: str, path: Path) -> None:
    from nbconvert import PDFExporter
    exporter = PDFExporter(template_name="marking", extra_template_basedirs=TEMPLATE_DIRS)
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    try:
        body, _ = exporter.from_notebook_node(nb, resources={"metadata": {"name": name}})
    except Exception as exc:
        raise StripError(f"{name}: the PDF could not be built — {str(exc)[-600:]}") from exc
    path.write_bytes(body)


def run_strip(args) -> int:
    template = load(args.template)
    rubric = load_rubric(args.rubric)
    args.out.mkdir(parents=True, exist_ok=True)
    reports, failed = [], 0
    for path in args.submissions:
        try:
            nb, report = strip(template, load(path), rubric, path.name)
            stem = path.stem
            if path.suffix.lower() == ".py":
                write_percent_py(nb, args.out / f"{stem}.stripped.py")
            else:
                nbformat.write(nb, str(args.out / f"{stem}.stripped.ipynb"))
            if not args.no_pdf:
                marking = nbformat.v4.new_notebook(
                    cells=[cover_cell(path.name, rubric), *nb.cells], metadata=nb.metadata)
                write_pdf(marking, path.name, args.out / f"{stem}.marking.pdf")
        except StripError as exc:
            print(f"skipped — {exc}", file=sys.stderr)
            failed += 1
            continue
        reports.append(report)
        print(f"{path.name}: kept {report.kept}, dropped {report.dropped}, "
              f"headings {report.headings}")
        for flag in report.flags:
            print(f"    check: {flag}")

    with (args.out / "strip_report.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "cells_kept", "cells_dropped", "headings_kept", "flags"])
        for r in reports:
            writer.writerow([r.name, r.kept, r.dropped, r.headings, " | ".join(r.flags)])
    print(f"\n{len(reports)} written to {args.out}" + (f", {failed} skipped" if failed else ""))
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init-rubric", help="print a rubric skeleton from a template's headings")
    init.add_argument("template", type=Path)

    run = sub.add_parser("strip", help="strip submissions and build marking PDFs")
    run.add_argument("template", type=Path, help="the blank student notebook (.ipynb or .py)")
    run.add_argument("submissions", nargs="+", type=Path)
    run.add_argument("--rubric", type=Path, default=None)
    run.add_argument("--out", type=Path, default=Path("marking"))
    run.add_argument("--no-pdf", action="store_true", help="write only the stripped files")

    args = parser.parse_args()
    try:
        if args.command == "init-rubric":
            sys.stdout.write(init_rubric(args.template))
            return 0
        return run_strip(args)
    except StripError as exc:
        print(f"error — {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
