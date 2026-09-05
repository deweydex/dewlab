"""A cell's own report panel, in a real browser — DECISIONS_LOG.md Phase 8.

The icon and the panel's shell are static, built by build.py's
render_cell() and covered by tests/test_build.py already. What can only
be checked in a real browser is the live half: that
updateCellReportLinks() in tutorial-runtime.js actually reads the cell's
current code and output at the moment the panel opens, not whatever was
there at page load.

    python3 -m pytest tests/e2e/test_cell_report.py -q
"""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse


def icon(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-report-icon")


def panel(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-report-doors")


def issue_link_params(page, cell_id: str, which: str) -> dict:
    """`which` is a fragment of the link's visible text — "error" or
    "wrong" — since that is the only thing telling the two issue links
    apart from the reader's side."""
    links = page.locator(
        f".dl-cell[data-cell-id='{cell_id}'] .dl-report-issue-link"
    )
    for i in range(links.count()):
        link = links.nth(i)
        if which in link.inner_text().lower():
            return parse_qs(urlparse(link.get_attribute("href")).query)
    raise AssertionError(f"no report link contains {which!r}")


def js_string(value: str) -> str:
    return json.dumps(value)


def run(page, cell_id: str) -> None:
    """Run a cell and wait for it to actually finish — the same pattern
    test_phase0_golden_path.py and test_autocomplete.py already use."""
    selector = f".dl-cell[data-cell-id='{cell_id}'] .dl-output"
    page.evaluate(f"dewlab.runCell({js_string(cell_id)})")
    page.wait_for_function(
        f"document.querySelector({js_string(selector)}).children.length > 0",
        timeout=60_000,
    )


class TestCellReportPanel:
    def test_starts_closed(self, page):
        assert panel(page, "plain-python").is_hidden()
        assert icon(page, "plain-python").get_attribute("aria-expanded") == "false"

    def test_a_click_opens_it_in_place_not_as_a_floating_popover(self, page):
        icon(page, "plain-python").click()
        assert panel(page, "plain-python").is_visible()
        assert icon(page, "plain-python").get_attribute("aria-expanded") == "true"
        box = panel(page, "plain-python").bounding_box()
        assert box["height"] > 0
        position = panel(page, "plain-python").evaluate(
            "el => getComputedStyle(el).position"
        )
        assert position == "static"

    def test_a_second_click_closes_it_again(self, page):
        icon(page, "plain-python").click()
        assert panel(page, "plain-python").is_visible()
        icon(page, "plain-python").click()
        assert panel(page, "plain-python").is_hidden()
        assert icon(page, "plain-python").get_attribute("aria-expanded") == "false"

    def test_links_carry_page_version_and_this_cell(self, page):
        icon(page, "numpy-basics").click()
        params = issue_link_params(page, "numpy-basics", "error")
        assert params["page"] == ["fixtures/rendering-tour"]
        assert params["cell"] == ["numpy-basics"]
        assert params["template"] == ["report.yml"]
        assert "version" in params
        assert "kind" in params
        wrong = issue_link_params(page, "numpy-basics", "wrong")
        assert wrong["kind"] != params["kind"]

    def test_code_reflects_a_live_edit_not_the_starter(self, page):
        cell_content = page.locator(
            ".dl-cell[data-cell-id='plain-python'] .cm-content"
        )
        cell_content.click()
        page.keyboard.press("Control+End")
        page.keyboard.type("\n# a note only this reader added")

        icon(page, "plain-python").click()
        params = issue_link_params(page, "plain-python", "error")
        assert "a note only this reader added" in params["code"][0]

    def test_output_is_absent_before_the_cell_has_run(self, page):
        icon(page, "tools-widgets").click()
        params = issue_link_params(page, "tools-widgets", "error")
        assert "output" not in params

    def test_output_carries_the_traceback_after_running(self, page):
        run(page, "error-traceback")
        icon(page, "error-traceback").click()
        params = issue_link_params(page, "error-traceback", "error")
        assert "TypeError" in params["output"][0]
        assert "total += value" in params["output"][0]
        # The runtime's own plumbing has no business in a student's report.
        assert "tutorial_tools" not in params["output"][0]
        assert "total = 0" in params["code"][0]

    def test_reopening_after_a_run_refreshes_the_output(self, page):
        """Opened once before running (still cached in the DOM from the
        earlier click), then run, then opened again — the second open has
        to re-read the output, not show what the first open saw."""
        icon(page, "matplotlib-show").click()
        icon(page, "matplotlib-show").click()  # closed again
        run(page, "matplotlib-show")
        icon(page, "matplotlib-show").click()
        params = issue_link_params(page, "matplotlib-show", "error")
        assert "after the plot" in params["output"][0]
