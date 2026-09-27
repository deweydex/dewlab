"""`input()` on the fixture's `asking` page (assets/input-wait.js).

On the hosted page, once cross-origin isolation has landed, Python waits in
its Worker and a box appears after the prompt; Enter sends the line, and
Stop ends the wait. A downloaded copy runs Python on the page's thread and
asks with the browser's own dialog. A hosted page that never became
isolated says so in words. The comparison never waits: it reads the cell's
```typed lines."""

from __future__ import annotations

import json

import pytest

from test_compare import _open, _serve
from test_dewmini_workbench import add_python_cell, dewmini, dewmini_url  # noqa: F401

PAGE = "tutorials/asking.html"


def _output(cell_id: str) -> str:
    return f".dl-cell[data-cell-id='{cell_id}'] .dl-output"


def _run(tab, cell_id: str) -> None:
    tab.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-btn-run").click()


def _wait_for_text(tab, cell_id: str, text: str) -> None:
    tab.wait_for_function(
        f"document.querySelector({json.dumps(_output(cell_id))}).innerText"
        f".includes({json.dumps(text)})",
        timeout=60_000,
    )


@pytest.fixture()
def isolated(browser, base_url, site_dir):
    """The page as the site serves it, service worker and all, so the
    isolation shim can do its first-visit reload. Pointed at the fixture's
    own Pyodide on disk, as conftest.py does for rendering-tour, since a
    page a service worker serves never reaches a Playwright route."""
    built = site_dir / PAGE
    html = built.read_text()
    marker = '<script>globalThis.DEWLAB_PYODIDE_BASE = "../pyodide/";</script>\n'
    if marker not in html:
        runtime = html.index('<script type="module" src="../assets/tutorial-runtime.js')
        built.write_text(html[:runtime] + marker + html[runtime:])
    context = browser.new_context()
    tab = context.new_page()
    problems: list[str] = []
    tab.on("pageerror", lambda err: problems.append(f"pageerror: {err}"))
    tab.problems = problems
    tab.goto(f"{base_url}/{PAGE}")
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    tab.wait_for_function("dewlab.canStop()", timeout=240_000)
    try:
        yield tab
    finally:
        context.close()


def test_the_box_appears_after_the_prompt_and_enter_sends_the_line(isolated):
    tab = isolated
    _run(tab, "ask-name")
    box = tab.locator(f"{_output('ask-name')} input.dl-stdin")
    box.wait_for(timeout=60_000)
    assert box.get_attribute("aria-label") == "What is your name?"
    assert box.evaluate("el => el === document.activeElement")
    assert tab.locator(f"{_output('ask-name')} pre.dl-stdout").inner_text().startswith(
        "What is your name?")

    box.fill("Ada")
    box.press("Enter")
    _wait_for_text(tab, "ask-name", "Hello, Ada")
    assert tab.locator(f"{_output('ask-name')} input.dl-stdin").count() == 0
    assert tab.locator(_output("ask-name")).inner_text().strip() == "What is your name? Ada\nHello, Ada"
    assert tab.problems == []


def test_a_function_asks_again_until_the_answer_makes_sense(isolated):
    tab = isolated
    cell = tab.locator(".dl-cell[data-cell-id='ask-shift'] .dl-editor .cm-content")
    cell.click()
    tab.keyboard.press("Control+End")
    tab.keyboard.insert_text("\n\nprint('Shift:', ask_shift())")
    _run(tab, "ask-shift")
    for answer in ("seven", "12"):
        box = tab.locator(f"{_output('ask-shift')} input.dl-stdin")
        box.wait_for(timeout=60_000)
        box.fill(answer)
        box.press("Enter")
    _wait_for_text(tab, "ask-shift", "Shift: 12")
    assert "Please type a whole number from 1 to 25." in tab.locator(
        _output("ask-shift")).inner_text()


def test_stop_ends_the_wait(isolated):
    tab = isolated
    _run(tab, "ask-name")
    box = tab.locator(f"{_output('ask-name')} input.dl-stdin")
    box.wait_for(timeout=60_000)
    _run(tab, "ask-name")  # the same button, now meaning Stop
    _wait_for_text(tab, "ask-name", "Stopped.")
    assert box.count() == 0
    label = tab.locator(".dl-cell[data-cell-id='ask-name'] .dl-btn-run .dl-btn-label")
    tab.wait_for_function(
        "document.querySelector(\".dl-cell[data-cell-id='ask-name'] .dl-btn-run .dl-btn-label\")"
        ".textContent === 'Run'",
        timeout=10_000,
    )
    assert label.inner_text() == "Run"

    # Python is still there, and asks again.
    _run(tab, "ask-name")
    box = tab.locator(f"{_output('ask-name')} input.dl-stdin")
    box.wait_for(timeout=60_000)
    box.fill("Grace")
    box.press("Enter")
    _wait_for_text(tab, "ask-name", "Hello, Grace")


def test_the_comparison_reads_the_typed_lines_and_says_so(isolated):
    tab = isolated
    note = tab.locator(".dl-compare[data-cell='ask-shift'] .dl-compare-typed")
    assert "seven" in note.inner_text()
    tab.locator(".dl-compare[data-cell='ask-shift'] .dl-btn-compare").click()
    tab.wait_for_function(
        "document.querySelector('.dl-compare[data-cell=\"ask-shift\"] .dl-compare-yours')"
        ".textContent === '7'",
        timeout=60_000,
    )
    theirs = tab.locator(".dl-compare[data-cell='ask-shift'] .dl-compare-theirs").inner_text()
    assert theirs.startswith("7")
    assert tab.locator(f"{_output('ask-shift')} input.dl-stdin").count() == 0


def test_a_downloaded_copy_asks_with_the_browsers_dialog(browser, base_url, site_dir):
    context, tab = _open(browser, f"{base_url}/{PAGE}",
                         _serve(site_dir, standalone=True, path=PAGE), page=PAGE)
    try:
        asked = []

        def answer(dialog):
            asked.append((dialog.type, dialog.message))
            dialog.accept("Ada")

        tab.on("dialog", answer)
        tab.wait_for_function(
            "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
            timeout=240_000,
        )
        _run(tab, "ask-name")
        _wait_for_text(tab, "ask-name", "Hello, Ada")
        assert asked == [("prompt", "What is your name?")]
        assert tab.locator(_output("ask-name")).inner_text().strip() == "What is your name? Ada\nHello, Ada"
    finally:
        context.close()


def test_a_page_that_cannot_wait_says_so(browser, base_url, site_dir):
    context, tab = _open(browser, f"{base_url}/{PAGE}",
                         _serve(site_dir, standalone=False, path=PAGE), page=PAGE)
    try:
        tab.wait_for_function(
            "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
            timeout=240_000,
        )
        assert tab.evaluate("window.crossOriginIsolated") is False
        _run(tab, "ask-name")
        _wait_for_text(tab, "ask-name", "has not let the page wait")
        assert "EOFError" in tab.locator(_output("ask-name")).inner_text()
    finally:
        context.close()


def test_the_notebook_asks_the_same_way(dewmini):  # noqa: F811 - the imported fixture
    dewmini.wait_for_function("window.crossOriginIsolated", timeout=30_000)
    add_python_cell(dewmini, 'city = input("Which city? ")\nprint(city.upper())')
    dewmini.locator(".dm-cell .dm-icon-run").first.click()
    box = dewmini.locator(".dm-cell-output input.dl-stdin")
    box.wait_for(timeout=240_000)
    box.fill("Cork")
    box.press("Enter")
    dewmini.wait_for_function(
        "[...document.querySelectorAll('.dm-cell-output')]"
        ".some(o => o.textContent.includes('Which city? Cork') && o.textContent.includes('CORK'))",
        timeout=60_000,
    )
