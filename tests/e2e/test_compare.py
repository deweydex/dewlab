"""The comparison view (#312), on the fixture's `comparing` page: a
`total_of` that leaves out the last value, a solution that does not, three
inputs with a guess column, a cell of the reader's own tests, and a task
with inputs and no solution.

Driven twice: on the hosted page, where Python runs in a Worker, and on the
same page with its manifest rewritten the way a downloaded copy's is, so
Python runs on the main thread. The table has to read the same either way.
"""

from __future__ import annotations

import json
import re

import pytest

from conftest import DEWLAB

PAGE = "tutorials/comparing.html"


def _open(browser, url, route=None):
    # No service worker: the page's cross-origin-isolation shim reloads it
    # through one, and a page a service worker serves never reaches the
    # route below. The comparison needs no isolation (that is for Stop).
    context = browser.new_context(service_workers="block")
    tab = context.new_page()
    problems: list[str] = []
    tab.on("pageerror", lambda err: problems.append(f"pageerror: {err}"))
    tab.problems = problems
    if route:
        tab.route(f"**/{PAGE}", route)
    tab.goto(url)
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    return context, tab


def _serve(site_dir, standalone: bool):
    """The built page, pointed at the Pyodide the fixture site serves (the
    conftest does this for rendering-tour only). With `standalone`, it is
    also changed the way write_standalone() changes a download: the
    manifest says `standalone` and carries the Python tools inline, and the
    classic Pyodide script is on the page, so Python runs on the main
    thread. Read from disk rather than fetched, so no proxy sits between
    the test and its own server."""
    page = (site_dir / PAGE).read_text()
    runtime = re.search(
        r'<script type="module" src="\.\./assets/tutorial-runtime\.js[^"]*"></script>', page
    ).group(0)
    before = '<script>globalThis.DEWLAB_PYODIDE_BASE = "../pyodide/";</script>\n'
    if standalone:
        before = '<script src="../pyodide/pyodide.js"></script>\n' + before
        marker = '<script type="application/json" id="dewlab-manifest">'
        start = page.index(marker) + len(marker)
        end = page.index("</script>", start)
        manifest = json.loads(page[start:end])
        manifest["standalone"] = True
        manifest["toolsSource"] = (DEWLAB / "assets" / "tutorial_tools.py").read_text()
        page = page[:start] + json.dumps(manifest).replace("<", "\\u003c") + page[end:]
    page = page.replace(runtime, before + runtime, 1)

    def handle(route):
        route.fulfill(status=200, content_type="text/html; charset=utf-8", body=page)
    return handle


@pytest.fixture(params=["worker", "main-thread"])
def tab(request, browser, base_url, site_dir):
    route = _serve(site_dir, standalone=request.param == "main-thread")
    context, tab = _open(browser, f"{base_url}/{PAGE}", route)
    tab.evaluate("localStorage.clear()")
    try:
        yield tab
    finally:
        context.close()


def compare(tab, cell):
    box = tab.locator(f".dl-compare[data-cell='{cell}']")
    box.locator(".dl-btn-compare").click()
    tab.wait_for_function(
        f"""() => {{
          const box = document.querySelector(".dl-compare[data-cell='{cell}']");
          return box.querySelector(".dl-compare-yours span")
            && !box.querySelector(".dl-btn-compare").disabled;
        }}""",
        timeout=240_000,
    )
    return box


def row(box, index):
    return box.locator(f"tr[data-case='{index}']")


class TestComparison:
    def test_nothing_is_compared_until_the_reader_asks(self, tab):
        box = tab.locator(".dl-compare[data-cell='compare-total']")
        assert box.locator(".dl-compare-yours span").count() == 0
        assert box.locator(".dl-btn-compare").inner_text() == "Compare with a solution"

    def test_each_case_shows_both_sides_and_marks_only_what_differs(self, tab):
        box = compare(tab, "compare-total")
        first = row(box, 0)
        assert first.locator(".dl-compare-yours").inner_text() == "3"
        assert first.locator(".dl-compare-theirs").inner_text().startswith("6")
        assert "different" in first.locator(".dl-compare-theirs").inner_text()
        assert "dl-compare-differ" in first.get_attribute("class")

        empty = row(box, 1)
        assert empty.locator(".dl-compare-yours").inner_text() == "0"
        assert empty.locator(".dl-compare-theirs").inner_text() == "0"
        assert "dl-compare-differ" not in (empty.get_attribute("class") or "")
        assert "an empty list" in empty.inner_text()

    def test_no_word_on_the_table_judges(self, tab):
        box = compare(tab, "compare-total")
        text = box.inner_text().lower()
        for word in ("correct", "wrong", "not yet", "right", "pass", "fail", "✓", "✗"):
            assert word not in text, word

    def test_the_readers_own_tests_run_on_both_sides_first(self, tab):
        box = compare(tab, "compare-total")
        tests = box.locator("tbody.dl-compare-tests tr:not(.dl-compare-section)")
        assert tests.count() == 2
        assert tests.nth(0).locator(".dl-compare-yours").inner_text() == "AssertionError"
        assert tests.nth(0).locator(".dl-compare-theirs").inner_text().startswith("no error")
        assert tests.nth(1).locator(".dl-compare-yours").inner_text() == "0"
        assert box.locator(".dl-compare-authors").inner_text() == "Cases you may not have tried"

    def test_asking_changes_nothing_the_reader_has(self, tab):
        compare(tab, "compare-total")
        # The solution's total_of replaced the reader's only in a copy.
        tab.evaluate(
            "globalThis.dewlab.cells.find((c) => c.id === 'compare-own')"
            ".editor.setValue('print(total_of([1, 2, 3]))')"
        )
        tab.locator(".dl-cell[data-cell-id='compare-own'] .dl-btn-run").click()
        tab.wait_for_function(
            "document.querySelector(\".dl-cell[data-cell-id='compare-own'] .dl-output\")"
            ".textContent.includes('3')",
            timeout=60_000,
        )
        output = tab.locator(".dl-cell[data-cell-id='compare-own'] .dl-output").inner_text()
        assert output.strip() == "3"

    def test_a_guess_is_saved_with_the_cell_and_comes_back(self, tab):
        guess = tab.locator(".dl-compare[data-cell='compare-total'] tr[data-case='0'] input")
        guess.fill("6")
        tab.evaluate("globalThis.dewlab.saveNow()")
        saved = tab.evaluate("globalThis.dewlab.readSaved()")
        cell = next(c for c in saved["cells"] if c["task_id"] == "compare-total")
        assert cell["guesses"] == ["6", "", ""]
        tab.reload()
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        assert guess.input_value() == "6"

    def test_without_a_solution_only_the_readers_side_is_shown(self, tab):
        box = tab.locator(".dl-compare[data-cell='compare-own']")
        assert box.locator(".dl-btn-compare").inner_text() == "Try these on your code"
        assert box.locator(".dl-compare-theirs").count() == 0
        box = compare(tab, "compare-own")
        assert row(box, 0).locator(".dl-compare-yours").inner_text() == "8"

    def test_no_errors_on_the_page(self, tab):
        compare(tab, "compare-total")
        assert tab.problems == []
