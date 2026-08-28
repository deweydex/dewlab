"""A cell's own hint, in a real browser.

Click-to-open, not hover — DECISIONS_LOG.md has the account of why the
previous hover popover was replaced. Wired in buildCells(), which runs
before Pyodide's boot is even attempted, so none of this needs a cell to
have run or Pyodide to have finished loading — the same reasoning
test_autocomplete.py's first class already relies on for static
completion.

    python3 -m pytest tests/e2e/test_cell_hint.py -q
"""

from __future__ import annotations


def icon(page):
    return page.locator(".dl-cell[data-cell-id='numpy-basics'] .dl-hint-icon")


def text(page):
    return page.locator("#dl-hint-numpy-basics")


class TestCellHint:
    def test_starts_closed(self, page):
        assert text(page).is_hidden()
        assert icon(page).get_attribute("aria-expanded") == "false"

    def test_a_click_opens_it_in_place_not_as_a_floating_popover(self, page):
        icon(page).click()
        assert text(page).is_visible()
        assert icon(page).get_attribute("aria-expanded") == "true"
        assert "not one number at a time" in text(page).inner_text()
        # In normal flow, not position: absolute — its box actually has
        # height, which is what pushes the rest of the page down rather
        # than floating over the editor or output above it.
        box = text(page).bounding_box()
        assert box["height"] > 0
        position = text(page).evaluate("el => getComputedStyle(el).position")
        assert position == "static"

    def test_a_second_click_closes_it_again(self, page):
        icon(page).click()
        assert text(page).is_visible()
        icon(page).click()
        assert text(page).is_hidden()
        assert icon(page).get_attribute("aria-expanded") == "false"
