"""`slider()` (#329): moving it runs its own cell again, the thumb stays
put while the output is redrawn, and where the reader left it survives a
reload.

Driven twice, like the comparison view: on the hosted page, where Python
runs in a Worker, and on the same page rewritten the way a downloaded copy
is, where Python runs on the main thread.
"""

from __future__ import annotations

import json

import pytest

from conftest import PAGE
from test_compare import _open, _serve

CELL = "tools-slider"
OUTPUT = f".dl-cell[data-cell-id='{CELL}'] .dl-output"
STRIP = f".dl-cell[data-cell-id='{CELL}'] .dl-slider-strip"
THUMB = json.dumps(f"{STRIP} input[type=range]")


@pytest.fixture(params=["worker", "main-thread"])
def tab(request, browser, base_url, site_dir):
    route = _serve(site_dir, standalone=request.param == "main-thread", path=PAGE)
    context, tab = _open(browser, f"{base_url}/{PAGE}", route, page=PAGE)
    tab.evaluate("localStorage.clear()")
    tab.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
        timeout=240_000,
    )
    try:
        yield tab
    finally:
        context.close()


def wait_for_output(tab, text: str) -> None:
    tab.wait_for_function(
        f"document.querySelector({OUTPUT!r}).textContent.includes({text!r})",
        timeout=120_000,
    )


def test_moving_the_slider_runs_the_cell_again(tab):
    tab.evaluate(f"dewlab.runCell({CELL!r})")
    wait_for_output(tab, "amplitude is 2")

    # The slider sits in the strip above the output, not in the output.
    assert tab.locator(f"{STRIP} input[type=range]").count() == 1
    assert tab.locator(f"{OUTPUT} .dl-slider").count() == 0

    thumb = tab.locator(f"{STRIP} input[type=range]")
    thumb.focus()
    tab.keyboard.press("ArrowRight")
    wait_for_output(tab, "amplitude is 3")
    assert tab.locator(f"{STRIP} output").inner_text() == "3"

    # The same element, not a fresh one: a drag would survive the redraw.
    tab.evaluate(f"window.__thumb = document.querySelector({THUMB})")
    tab.keyboard.press("ArrowRight")
    wait_for_output(tab, "amplitude is 4")
    assert tab.evaluate(
        f"window.__thumb === document.querySelector({THUMB})"
    )
    assert tab.locator(f"{STRIP} input[type=range]").count() == 1
    # The fixture page's sandboxed frames complain that service workers are
    # blocked in this context (_open() blocks them); nothing else may.
    assert [p for p in tab.problems if "serviceWorker" not in p] == []


def test_where_the_reader_left_it_survives_a_reload(tab):
    tab.evaluate(f"dewlab.runCell({CELL!r})")
    wait_for_output(tab, "amplitude is 2")
    tab.locator(f"{STRIP} input[type=range]").focus()
    tab.keyboard.press("End")
    wait_for_output(tab, "amplitude is 5")

    tab.reload()
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    tab.wait_for_selector(f"{STRIP} input[type=range]", timeout=30_000)
    assert tab.locator(f"{STRIP} input[type=range]").input_value() == "5"

    # And Python hears it: the first run after the reload reads 5, not 2.
    tab.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
        timeout=240_000,
    )
    tab.evaluate(f"dewlab.runCell({CELL!r})")
    wait_for_output(tab, "amplitude is 5")


def test_reset_empties_the_strip_with_the_output(tab):
    tab.evaluate(f"dewlab.runCell({CELL!r})")
    wait_for_output(tab, "amplitude is 2")
    reset = tab.locator(f".dl-cell[data-cell-id='{CELL}'] .dl-btn-reset")
    if reset.count() == 0:
        pytest.skip("this cell has no reset button")
    reset.first.click()
    assert tab.locator(f"{STRIP} .dl-slider").count() == 0
