"""Every `dl-` class an author writes by hand has a rule behind it.

A tutorial can write raw HTML in its body — a hint fold, a section
wrapper, a diagram built out of the thing it describes (`.dl-boxmodel`
and the rest of the `.dl-drawn` family). Python-Markdown passes that
through untouched and the build never looks at the class names, so a
renamed or mistyped one produces a page that is valid, silent, and
unstyled: nested divs with no colours and no layout, which reads as a
stack of empty boxes rather than as a broken reference.

This is the only thing standing between that and a reader, so it scans
the real content rather than a fixture.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# A fenced block is what a cell's own code lives in — a site editor's
# `<div class="box">`, or a runtime class a page happens to quote — and
# none of it is markup the build puts on the page.
FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)
CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')
CSS_SELECTOR_RE = re.compile(r"\.(dl-[A-Za-z0-9_-]+)")


def _defined() -> set[str]:
    return set(CSS_SELECTOR_RE.findall((REPO / "assets/tutorial-style.css").read_text()))


def _used() -> dict[str, list[Path]]:
    sources: dict[str, list[Path]] = {}
    files = sorted((REPO / "tutorials").rglob("*.md")) + sorted((REPO / "pages").glob("*.md"))
    for path in files:
        body = FENCE_RE.sub("", path.read_text())
        for attr in CLASS_ATTR_RE.findall(body):
            for name in attr.split():
                if name.startswith("dl-"):
                    sources.setdefault(name, []).append(path.relative_to(REPO))
    return sources


def test_every_hand_written_dl_class_is_styled():
    defined = _defined()
    missing = {
        name: paths for name, paths in _used().items() if name not in defined
    }
    assert not missing, "\n".join(
        f"{name} is written in {', '.join(str(p) for p in paths)} "
        "but assets/tutorial-style.css has no rule for it"
        for name, paths in sorted(missing.items())
    )


def test_the_scan_finds_the_markup_built_diagrams():
    # Guards the scanner itself: a regex that quietly stopped matching would
    # make the test above pass on everything, including a real break.
    used = _used()
    assert "dl-boxmodel" in used
    assert used["dl-boxmodel"] == [Path("tutorials/the-box/the-box.md")]


# --------------------------------------------------------------------------
# The annotated traceback in when-it-goes-wrong.
#
# It quotes real output, so it can go stale two ways: the cell it describes
# gets edited, or CPython changes how it formats a traceback. The second is
# not checkable here — CI runs 3.12 and the reader's Pyodide runs 3.13, and
# the two already disagree about where a call's carets start, so comparing
# against a locally generated traceback would assert the wrong thing. What
# is version-independent is everything the cell itself determines: which
# line each frame names, what that line says, and which error it raises.
# --------------------------------------------------------------------------

WHEN_IT_GOES_WRONG = REPO / "tutorials/when-it-goes-wrong/when-it-goes-wrong.md"
CELL_ID = "reading-a-traceback-1"

FRAME_RE = re.compile(rf'File "<cell {CELL_ID}>", line (\d+), in (\S+)$')
CODE_ROW_RE = re.compile(r"<code>(.*?)</code>")
HEADER_RE = re.compile(r"^(id|hint|label|site|app|title):\s")


def _cell_source(path: Path, cell_id: str) -> list[str]:
    text = path.read_text()
    for block in re.findall(r"^```python exec\n(.*?)^```", text, re.S | re.M):
        lines = block.splitlines()
        if f"id: {cell_id}" not in lines[:3]:
            continue
        while lines and HEADER_RE.match(lines[0]):
            lines.pop(0)
        return lines
    raise AssertionError(f"no `python exec` cell with id {cell_id} in {path}")


def _diagram_rows(path: Path) -> list[str]:
    import html

    block = re.search(
        r'<div class="dl-drawn dl-traceback">(.*?)\n</div>\n',
        path.read_text(),
        re.S,
    )
    assert block, "the annotated traceback is gone from when-it-goes-wrong"
    return [html.unescape(m) for m in CODE_ROW_RE.findall(block.group(1))]


def test_the_annotated_traceback_quotes_the_cell_it_describes():
    source = _cell_source(WHEN_IT_GOES_WRONG, CELL_ID)
    rows = _diagram_rows(WHEN_IT_GOES_WRONG)

    frames = [(i, m) for i, row in enumerate(rows) if (m := FRAME_RE.search(row))]
    assert len(frames) == 3, "expected three frames in the diagram"

    for i, match in frames:
        lineno, where = int(match.group(1)), match.group(2)
        quoted = rows[i + 1].strip()
        assert quoted == source[lineno - 1].strip(), (
            f"the diagram's frame at line {lineno} quotes {quoted!r}, but line "
            f"{lineno} of cell {CELL_ID} is {source[lineno - 1].strip()!r}"
        )
        if where != "<module>":
            assert f"def {where}(" in "\n".join(source[: lineno - 1]), (
                f"the diagram names a frame in {where}(), which the cell does "
                "not define above that line"
            )


def test_the_annotated_traceback_names_the_error_the_cell_raises():
    source = "\n".join(_cell_source(WHEN_IT_GOES_WRONG, CELL_ID))
    try:
        exec(compile(source, f"<cell {CELL_ID}>", "exec"), {"__name__": "__main__"})
    except Exception as exc:  # noqa: BLE001 — the point is to catch whatever it is
        raised = f"{type(exc).__name__}: {exc}"
    else:
        raise AssertionError(f"cell {CELL_ID} no longer raises anything")

    assert _diagram_rows(WHEN_IT_GOES_WRONG)[-1] == raised
