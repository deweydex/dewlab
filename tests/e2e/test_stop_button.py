"""The genuine Stop button, in a real browser — planning/CELL_CONTROLS.md §2,
DECISIONS_LOG.md 7.77.

Pyodide runs inside assets/pyodide-worker.js on the hosted site now, so a
tight, synchronous, no-yields-at-all Python loop can be interrupted from
outside it — the worst case a runaway cell could produce, and the one
CELL_CONTROLS.md's own prototype proved works before any of this was built.
`dewlab.canStop()` (assets/tutorial-runtime.js) is true exactly when cross-
origin isolation actually landed for this page; every test here waits for it
first rather than assuming coi-serviceworker.js's own first-visit reload has
already happened.

    python3 -m pytest tests/e2e/test_stop_button.py -q
"""

from __future__ import annotations

import json


def cell_content(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-editor .cm-content")


def output_selector(cell_id: str) -> str:
    return f".dl-cell[data-cell-id='{cell_id}'] .dl-output"


def run_button(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-btn-run")


def js_string(text: str) -> str:
    return json.dumps(text)


def test_the_page_is_cross_origin_isolated(page):
    """The precondition every other test here assumes. If this is ever
    false, coi-serviceworker.js (assets/shell.html) stopped registering —
    everything below would still "pass" by falling back to a plain,
    un-stoppable Run, which is the one way this whole feature could go
    quietly missing without a single test failing to say so."""
    page.wait_for_function("dewlab.canStop()", timeout=30_000)
    assert page.evaluate("window.crossOriginIsolated") is True
    assert page.evaluate("typeof SharedArrayBuffer") == "function"


def test_stopping_a_genuine_infinite_loop(page):
    page.wait_for_function("dewlab.canStop()", timeout=30_000)
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.insert_text("\ncounter = 0\nwhile True:\n    counter += 1")

    btn = run_button(page, "plain-python")
    btn_selector = js_string(".dl-cell[data-cell-id='plain-python'] .dl-btn-run")
    btn.click()
    page.wait_for_function(
        f"document.querySelector({btn_selector}).textContent === 'Stop'",
        timeout=10_000,
    )

    # Let it actually spin for a moment — stopping instantly would not tell
    # the difference between a real interrupt and a cell that just hadn't
    # started yet.
    page.wait_for_timeout(1_000)
    btn.click()  # the same button, now meaning Stop

    page.wait_for_function(
        f"document.querySelector({js_string(output_selector('plain-python'))}).innerText.includes('Stopped.')",
        timeout=20_000,
    )
    assert btn.inner_text() == "Run"
    assert not btn.is_disabled()


def test_a_stopped_cell_can_be_run_again(page):
    """The worker itself survives an interrupt — this is not a crash
    recovered from by rebooting Pyodide, just tutorial_tools.run_cell()
    catching KeyboardInterrupt the way it catches any other exception."""
    page.wait_for_function("dewlab.canStop()", timeout=30_000)
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.insert_text("\nwhile True:\n    pass")

    btn = run_button(page, "plain-python")
    btn_selector = js_string(".dl-cell[data-cell-id='plain-python'] .dl-btn-run")
    btn.click()
    page.wait_for_function(
        f"document.querySelector({btn_selector}).textContent === 'Stop'",
        timeout=10_000,
    )
    page.wait_for_timeout(1_000)
    btn.click()
    page.wait_for_function(
        f"document.querySelector({js_string(output_selector('plain-python'))}).innerText.includes('Stopped.')",
        timeout=20_000,
    )

    # Reset back to the cell's starter code first — appending after the
    # still-present `while True: pass` would just spin forever again
    # before ever reaching a new statement.
    page.locator(".dl-cell[data-cell-id='plain-python'] .dl-btn-reset").click()
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.insert_text("\n2 + 2")
    btn.click()
    page.wait_for_function(
        f"document.querySelector({js_string(output_selector('plain-python'))}).innerText.trim().endsWith('4')",
        timeout=15_000,
    )
