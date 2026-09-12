"""Hint icons are wired in buildCells(), before Pyodide's boot even starts, so these need no cell run and no Pyodide load."""

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
