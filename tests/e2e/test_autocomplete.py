"""Code completion and hover docs inside a cell, in a real browser.

Static completion — keywords, builtins, and whatever a student has already
typed in the cell — comes from `@codemirror/lang-python`'s own
`globalCompletion`/`localCompletionSource`, wired in
vendor-src/codemirror-entry.js. It works before Pyodide has finished
booting, which the first class below checks by never running a cell at all.

The rest needs a live interpreter: live-namespace completion
(`pageNamesCompletion`, assets/tutorial-runtime.js) reads whatever names are
actually defined in tutorial_tools._page_globals right now, and the hover
tooltip (`docFor`) reads a real `inspect.getdoc()` off a real object — both
only meaningfully testable once a cell has actually run.

    python3 -m pytest tests/e2e/test_autocomplete.py -q
"""

from __future__ import annotations

import json


def cell_content(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-editor .cm-content")


def completion_labels(page):
    return page.eval_on_selector_all(
        ".cm-tooltip-autocomplete .cm-completionLabel", "els => els.map(e => e.textContent)"
    )


def js_string(text: str) -> str:
    return json.dumps(text)


def run(page, cell_id: str) -> None:
    """Run a cell and wait for it to actually finish, the same way
    test_phase0_golden_path.py does."""
    selector = f".dl-cell[data-cell-id='{cell_id}'] .dl-output"
    page.evaluate(f"dewlab.runCell({js_string(cell_id)})")
    page.wait_for_function(
        f"document.querySelector({js_string(selector)}).children.length > 0",
        timeout=60_000,
    )


def test_typing_a_partial_keyword_offers_it(page):
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.type("\ndef")
    page.wait_for_selector(".cm-tooltip-autocomplete")
    assert "def" in completion_labels(page)


def test_accepting_a_completion_inserts_it(page):
    """closeBrackets already auto-pairs the "(" typed below, so the buffer
    reads len(list) once the completion replaces "lis" with "list" —
    checked as one string rather than "list(" for that reason."""
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.type("\nlen(")
    page.keyboard.type("lis")
    page.wait_for_selector(".cm-tooltip-autocomplete")
    page.keyboard.press("Enter")
    assert "len(list)" in cell.inner_text()


def test_a_name_the_student_already_typed_is_offered(page):
    """localCompletionSource: names defined earlier in the same cell, not
    only Python's own builtins."""
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.type("\nsome_reading_value = 1\nsome_read")
    page.wait_for_selector(".cm-tooltip-autocomplete")
    assert "some_reading_value" in completion_labels(page)


def test_escape_closes_the_completion_without_inserting_it(page):
    cell = cell_content(page, "plain-python")
    cell.click()
    page.keyboard.press("Control+End")
    page.keyboard.type("\npri")
    page.wait_for_selector(".cm-tooltip-autocomplete")
    page.keyboard.press("Escape")
    page.wait_for_selector(".cm-tooltip-autocomplete", state="hidden")
    assert "pri" in cell.inner_text()
    assert "print" not in cell.inner_text().split("\n")[-1]


class TestLiveNamespaceCompletion:
    """pageNamesCompletion reads tutorial_tools._page_globals — the actual
    dict every cell runs against — so a name only really exists here once a
    cell defining it has run, not just been typed."""

    def test_a_name_defined_by_running_a_cell_is_offered(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.type("\nsome_named_thing = 42")
        run(page, "plain-python")
        page.keyboard.press("Control+End")
        page.keyboard.type("\nsome_named_")
        page.wait_for_selector(".cm-tooltip-autocomplete")
        assert "some_named_thing" in completion_labels(page)


class TestHoverDocs:
    """docFor (assets/tutorial-runtime.js) reads a real inspect.getdoc() off
    a real object living in the interpreter actually running the page's
    cells — there is nothing bundled here to fall out of date."""

    def test_hovering_a_name_shows_its_own_real_docstring(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.type('\ndef helper_fn():\n    """my own real docstring"""\n')
        run(page, "plain-python")
        cell.get_by_text("helper_fn", exact=True).first.hover()
        page.wait_for_selector(".cm-dewlab-doc-tooltip")
        assert "my own real docstring" in page.inner_text(".cm-dewlab-doc-tooltip")

    def test_hovering_a_name_that_was_never_run_shows_nothing(self, page):
        cell = cell_content(page, "plain-python")
        cell.click()
        page.keyboard.press("Control+End")
        page.keyboard.type("\ntotally_undefined_name_xyz = 1")
        page.keyboard.press("Escape")
        cell.get_by_text("totally_undefined_name_xyz", exact=False).first.hover()
        page.wait_for_timeout(600)
        assert page.locator(".cm-dewlab-doc-tooltip").count() == 0
