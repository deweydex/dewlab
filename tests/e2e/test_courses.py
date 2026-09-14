"""What a reader meets once a tutorial can sit on more than one course:
the course chooser on the tree, the tree drawn for the course they came
from, the "also part of" line, saved work carried across a renamed key,
and an old address that still opens the page. Prose-only pages, so
nothing here boots Pyodide."""

from __future__ import annotations

import json

import pytest

from conftest import UP


@pytest.fixture()
def tab(browser, base_url):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def _course_rung(page) -> str:
    return page.text_content(".dl-crumb-level-2 > summary").strip()


class TestTheCourseChooser:
    def test_a_page_on_one_course_has_no_chooser_and_no_also_part_of_line(self, tab, base_url):
        tab.goto(f"{base_url}/tutorials/rendering-tour.html")
        tab.wait_for_selector("#dl-body")
        assert tab.locator(".dl-course-switch").count() == 0
        assert tab.locator(".dl-also-part-of").count() == 0

    def test_a_page_on_two_courses_offers_both_and_says_which_other(self, tab, base_url):
        tab.goto(f"{base_url}/tutorials/third-page.html")
        tab.wait_for_selector(".dl-course-switch select", state="attached")
        options = tab.eval_on_selector_all(".dl-course-switch option", "els => els.map(e => e.textContent)")
        assert options == ["End to end", "Second Course"]
        assert _course_rung(tab) == "End to end"
        line = tab.text_content(".dl-also-part-of")
        assert line.strip() == "This page is also part of Second Course."

    def test_arriving_from_a_course_page_draws_that_courses_tree(self, tab, base_url):
        tab.goto(f"{base_url}/fixtures-second.html")
        tab.wait_for_selector("#dl-body")
        tab.click('a[href="tutorials/third-page.html"]')
        tab.wait_for_function(
            "document.querySelector('.dl-crumb-level-2 > summary').textContent.trim() === 'Second Course'")
        assert tab.text_content(".dl-crumb-level-3 > summary").strip() == "Also"
        assert "End to end" in tab.text_content(".dl-also-part-of")
        # Only this page is on that series, so there is no previous or next.
        assert tab.locator(".dl-nav-bottom .dl-nav-prev").count() == 0
        assert tab.locator(".dl-nav-bottom .dl-nav-next").count() == 0

    def test_choosing_a_course_on_the_tree_redraws_it_and_is_remembered(self, tab, base_url):
        tab.goto(f"{base_url}/tutorials/third-page.html")
        tab.wait_for_selector(".dl-course-switch select", state="attached")
        # The chooser sits inside the tree's course rung, which starts closed.
        tab.evaluate("document.querySelector('.dl-crumb-level-2').open = true")
        tab.select_option(".dl-course-switch select", "fixtures-second")
        tab.wait_for_function(
            "document.querySelector('.dl-crumb-level-2 > summary').textContent.trim() === 'Second Course'")
        assert tab.evaluate("localStorage.getItem('dewlab:course')") == "fixtures-second"
        tab.reload()
        tab.wait_for_function(
            "document.querySelector('.dl-crumb-level-2 > summary').textContent.trim() === 'Second Course'")
        tab.evaluate("document.querySelector('.dl-crumb-level-2').open = true")
        tab.select_option(".dl-course-switch select", "fixtures")
        tab.wait_for_function(
            "document.querySelector('.dl-crumb-level-2 > summary').textContent.trim() === 'End to end'")
        assert tab.get_attribute(".dl-nav-bottom .dl-nav-next", "href").endswith("two-takes.html")
        assert tab.get_attribute(".dl-nav-bottom .dl-nav-prev", "href").endswith("prose-only.html")


class TestSavedWorkAndOldAddresses:
    def test_work_saved_under_the_old_key_is_there_under_the_new_id(self, tab, base_url):
        """The runtime alone, not the migration script: a record keyed the
        old way is renamed on the first visit, and never overwrites work
        saved under the new key since."""
        tab.goto(f"{base_url}/tutorials/rendering-tour.html")
        tab.wait_for_selector("#dl-body")
        record = {"tutorial-slug": "prose-only", "tutorial-module": "fixtures",
                  "tutorial-version": "2026.09.15.1", "saved_at": "2026-01-01T00:00:00.000Z",
                  "notes": "kept across the rename", "cells": []}
        tab.evaluate("(r) => localStorage.setItem('dewlab:progress:fixtures:prose-only', r)",
                     json.dumps(record))
        tab.goto(f"{base_url}/tutorials/prose-only.html")
        tab.wait_for_selector("#dl-body")
        assert tab.evaluate("localStorage.getItem('dewlab:progress:fixtures:prose-only')") is None
        saved = json.loads(tab.evaluate("localStorage.getItem('dewlab:progress:prose-only')"))
        assert saved["notes"] == "kept across the rename"
        assert tab.evaluate("globalThis.dewlab.readSaved().notes") == "kept across the rename"

    def test_an_old_address_lands_on_the_new_page(self, tab, base_url):
        tab.goto(f"{base_url}/tutorials/fixtures/prose-only.html")
        tab.wait_for_url("**/tutorials/prose-only.html")
        tab.wait_for_selector("#dl-body")
        assert tab.get_attribute("meta[name=tutorial-slug]", "content") == "prose-only"
        assert UP == "../"
