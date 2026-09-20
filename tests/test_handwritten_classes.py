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


# --------------------------------------------------------------------------
# The wrap threshold in flexbox-first-steps.
#
# The diagram measures the tutorial's own cards, and the numbers on it are
# only true while the CSS cell above it says what it says now. Edit the
# padding and the picture keeps claiming 366px for a row that no longer
# needs it — a failure nothing else would notice, since both the cell and
# the diagram would still render perfectly.
# --------------------------------------------------------------------------

FLEXBOX = REPO / "tutorials/flexbox-first-steps/flexbox-first-steps.md"
SUM_ROW_RE = re.compile(r'<p class="dl-fx-sum">([^<]*)')


def _flexbox_measurements() -> dict[str, int]:
    css = re.search(r"^```css site\n(.*?)^```", FLEXBOX.read_text(), re.S | re.M)
    assert css, "the site editor's CSS cell is gone from flexbox-first-steps"
    body = css.group(1)

    def one(pattern: str, what: str) -> int:
        match = re.search(pattern, body)
        assert match, f"no {what} in the tutorial's CSS cell"
        return int(match.group(1))

    return {
        "basis": one(r"flex:\s*\d+\s+\d+\s+(\d+)px", "flex-basis"),
        "padding": one(r"padding:\s*(\d+)px", "card padding"),
        "border": one(r"border:\s*(\d+)px", "card border"),
        "gap": one(r"gap:\s*(\d+)px", "row gap"),
    }


def test_the_wrap_threshold_matches_the_tutorials_own_css():
    m = _flexbox_measurements()
    card = m["border"] * 2 + m["padding"] * 2 + m["basis"]
    row = card * 3 + m["gap"] * 2

    sums = [line.strip() for line in SUM_ROW_RE.findall(FLEXBOX.read_text())]
    assert len(sums) == 2, "expected two arithmetic lines under the diagram"

    assert sums[0] == (
        f"{m['border']} + {m['padding']} + {m['basis']} + {m['padding']} + "
        f"{m['border']} = {card}px"
    ), f"the card's arithmetic no longer follows from the CSS cell: {sums[0]!r}"
    assert sums[1] == (
        f"{card} + {m['gap']} + {card} + {m['gap']} + {card} = {row}px"
    ), f"the row's arithmetic no longer follows from the CSS cell: {sums[1]!r}"


# --------------------------------------------------------------------------
# Three things about the live layout demos that can drift silently.
# --------------------------------------------------------------------------


def test_the_preview_width_readout_can_land_on_a_threshold():
    """A layout tutorial's question is at what width, so the slider has to
    step finely enough to find one and say what it found. At the old
    step of 5 the reader could not land near 366px, and a percentage of a
    column whose width depends on their font told them nothing anyway."""
    build = (REPO / "build.py").read_text()
    assert 'min="30" max="100" step="1"' in build, (
        "the preview-width slider no longer steps by 1"
    )
    assert '<output for="{width_id}"></output>' in build, (
        "the readout is no longer left for the runtime to fill with pixels"
    )
    runtime = (REPO / "assets/tutorial-runtime.js").read_text()
    assert "iframe.getBoundingClientRect().width" in runtime, (
        "the readout no longer measures the frame"
    )


def test_the_flexbox_preview_measures_the_row_and_not_the_frame():
    """The page tells the reader to watch the pixel figure and find where
    the row wraps, and names 366. Both are only true while the previewed
    page has no body margin: the readout measures the frame, and a default
    8px margin each side would put the wrap at 382."""
    css = re.search(r"^```css site\n(.*?)^```", FLEXBOX.read_text(), re.S | re.M).group(1)
    assert re.search(r"body\s*\{[^}]*margin:\s*0", css), (
        "flexbox-first-steps' CSS cell no longer zeroes the body margin, so "
        "the preview's pixel readout no longer agrees with the 366 in the prose"
    )


GRID_AREAS = REPO / "tutorials/named-grid-areas/named-grid-areas.md"


def test_the_grid_map_flips_at_the_tutorials_own_breakpoint():
    """The diagram is a container query standing in for the tutorial's
    media query, and a slider that reads out the width it is setting. Move
    either one and the picture changes shape at a width the page says
    nothing happens at, with a number beside it insisting otherwise."""
    grid = GRID_AREAS.read_text()
    media = re.search(r"@media \(min-width:\s*(\d+)px\)", grid)
    assert media, "no media query in named-grid-areas' CSS cell"
    threshold = int(media.group(1))

    css = (REPO / "assets/tutorial-style.css").read_text()
    block = re.search(
        r"@container \(min-width:\s*(\d+)px\)\s*\{[^@]*?\.dl-gm-grid", css, re.S
    )
    assert block, "the grid map's container query is gone"
    assert int(block.group(1)) == threshold, (
        f"the grid map flips at {block.group(1)}px but the tutorial's media "
        f"query turns on at {threshold}px"
    )

    slider = re.search(
        r'<input type="range" id="dl-gm-width" min="(\d+)" max="(\d+)"', grid
    )
    assert slider, "the grid map's width slider is gone"
    low, high = int(slider.group(1)), int(slider.group(2))
    assert low < threshold < high, (
        f"the slider runs {low}-{high}px, which cannot cross {threshold}px"
    )


def test_the_grid_maps_queried_width_is_the_width_it_draws():
    """A container query measures the content box, and the site sets
    `box-sizing: border-box` for everything — so padding or a border on the
    queried element eats into its declared width and the map flips late.
    It did: with the frame on the same element the map changed shape at an
    outer 376px while its own caption said 350. The frame belongs on a
    child, and the slider's number has to be the width of what is drawn."""
    css = (REPO / "assets/tutorial-style.css").read_text()
    rule = re.search(r"\n\.dl-gridmap \{(.*?)\n\}", css, re.S)
    assert rule, "no .dl-gridmap rule"
    for forbidden in ("padding", "border"):
        assert forbidden not in rule.group(1), (
            f".dl-gridmap declares {forbidden}, which shrinks the content box "
            "the container query measures — put it on .dl-gm-frame instead"
        )
    assert "container-type: inline-size" in rule.group(1)
