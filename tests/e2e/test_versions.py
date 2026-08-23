"""The version picker, in a browser.

A tutorial with one release is the common case and has no picker at all, so
everything here runs against `two-takes`, which exists in two releases: a June
one and a September one, sharing two cells and differing in a third. That
third cell is the whole point — it makes "how much of your work carries over"
a number a test can check rather than a phrase it can match.

None of these wait for Pyodide. The picker is built from the manifest at load,
so it is there long before Python is, and a test that booted a runtime to look
at a dropdown would cost four minutes to learn nothing.

    python3 -m pytest tests/e2e/test_versions.py -q
"""

from __future__ import annotations

import json

import pytest

MODULE = "fixtures"
SLUG = "two-takes"
DEFAULT_PAGE = f"tutorials/{MODULE}/{SLUG}.html"
JUNE_PAGE = f"tutorials/{MODULE}/{SLUG}/v2026.06.02.1.html"
ONE_VERSION_PAGE = f"tutorials/{MODULE}/rendering-tour.html"


def opened(tab, base_url, path):
    tab.goto(f"{base_url}/{path}")
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    return tab


@pytest.fixture()
def tab(browser, base_url):
    """A bare tab. Each test navigates it itself, because half of them are
    about what happens on the way to a page."""
    context = browser.new_context()
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()


def seed(tab, answers: dict[str, str], version: str = "2026.09.15.1"):
    """Saved work, written straight into storage.

    Directly rather than by typing, because what the counting reads is the
    record, not the keystrokes that made it."""
    record = {
        "tutorial-slug": SLUG,
        "tutorial-module": MODULE,
        "tutorial-version": version,
        "saved_at": "2026-09-20T10:00:00.000Z",
        "cells": [
            {"task_id": task, "student_code": code, "output_html": ""}
            for task, code in answers.items()
        ],
    }
    tab.evaluate(
        "([key, value]) => localStorage.setItem(key, value)",
        [f"dewlab:progress:{MODULE}:{SLUG}", json.dumps(record)],
    )


class TestWhenThereIsNothingToChoose:
    def test_a_tutorial_with_one_release_shows_no_picker(self, tab, base_url):
        """Most tutorials, most of the time. A control with one option is
        furniture, and furniture beside a title is the thing worth avoiding."""
        opened(tab, base_url, ONE_VERSION_PAGE)
        assert tab.locator("#dl-versions").count() == 0

    def test_and_settings_does_not_carry_a_versions_section(self, tab, base_url):
        opened(tab, base_url, ONE_VERSION_PAGE)
        assert tab.locator("#dl-settings-versions").count() == 0


class TestTheMarkerBesideTheTitle:
    def test_it_is_there_without_being_hovered(self, tab, base_url):
        """Hover does not exist on a phone. An affordance that only appears on
        hover is not subtle to a reader on one, it is missing."""
        opened(tab, base_url, DEFAULT_PAGE)
        assert tab.locator("#dl-versions-toggle").is_visible()

    def test_it_reads_as_a_date_rather_than_a_number(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        assert "15 September 2026" in tab.inner_text("#dl-versions-toggle")

    def test_it_sits_after_the_title(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        assert tab.eval_on_selector(
            "#dl-versions",
            "el => el.previousElementSibling.tagName",
        ) == "H1"

    def test_the_list_is_closed_until_it_is_asked_for(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        assert tab.locator("#dl-versions-list").is_hidden()
        assert tab.get_attribute("#dl-versions-toggle", "aria-expanded") == "false"

    def test_opening_it_lists_every_release_newest_first(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-versions-toggle")
        names = tab.eval_on_selector_all(
            "#dl-versions-list .dl-version-name", "els => els.map(e => e.textContent)"
        )
        assert names == ["15 September 2026", "2 June 2026"]

    def test_the_one_being_read_is_marked_and_is_not_a_link(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-versions-toggle")
        here = tab.locator("#dl-versions-list .dl-version[data-current]")
        assert here.count() == 1
        assert "15 September 2026" in here.inner_text()
        assert here.locator("a").count() == 0

    def test_escape_closes_it(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-versions-toggle")
        tab.keyboard.press("Escape")
        assert tab.locator("#dl-versions-list").is_hidden()


class TestATutorialWithoutATitleHeading:
    """`prose-only` opens straight into a section and has no cells. Both are
    legal, and both are awkward for a marker that wants to sit under a title
    and count answers."""

    PAGE = f"tutorials/{MODULE}/prose-only.html"

    def test_the_marker_is_still_there(self, tab, base_url):
        opened(tab, base_url, self.PAGE)
        assert tab.locator("#dl-versions-toggle").is_visible()

    def test_it_goes_to_the_top_of_the_page(self, tab, base_url):
        opened(tab, base_url, self.PAGE)
        assert tab.eval_on_selector(
            "#dl-versions", "el => el.previousElementSibling === null"
        )

    def test_a_page_with_no_cells_counts_nothing(self, tab, base_url):
        opened(tab, base_url, self.PAGE)
        tab.click("#dl-versions-toggle")
        assert tab.locator("#dl-versions-list .dl-version").count() == 2
        assert tab.locator("#dl-versions-list .dl-version-carry").count() == 0


class TestSayingWhatWillHappen:
    """Rather than warning that something might.

    Restore matches on cell id, so which answers survive a move is knowable
    before the reader makes it. "Best to export just in case" teaches a reader
    to distrust something that is in fact deterministic."""

    def test_it_counts_the_answers_that_carry_over(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {
            "shared-one": "print('mine')",
            "shared-two": "print('mine too')",
            "only-in-september": "print('and this')",
        })
        tab.reload()
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        tab.click("#dl-versions-toggle")
        june = tab.locator("#dl-versions-list .dl-version[data-version='2026.06.02.1']")
        assert "2 of your 3 answers carry over" in june.inner_text()

    def test_it_says_where_the_third_one_went(self, tab, base_url):
        """"Lost" would be a lie. The answer stays in storage and comes back
        the moment the reader returns to a release that has the cell."""
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {
            "shared-one": "print('mine')",
            "shared-two": "print('mine too')",
            "only-in-september": "print('and this')",
        })
        tab.reload()
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        tab.click("#dl-versions-toggle")
        june = tab.locator("#dl-versions-list .dl-version[data-version='2026.06.02.1']")
        assert "saved but is not shown there" in june.inner_text()

    def test_an_untouched_starter_is_not_an_answer(self, tab, base_url):
        """Counting the cells a reader happened to have open rather than the
        ones they wrote in would inflate every number here, and the point of
        the numbers is that they are true."""
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {
            "shared-one": 'print("one")',        # the starter, untouched
            "shared-two": "print('mine')",
            "only-in-september": "print('and this')",
        })
        tab.reload()
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        tab.click("#dl-versions-toggle")
        june = tab.locator("#dl-versions-list .dl-version[data-version='2026.06.02.1']")
        assert "1 of your 2 answers carry over" in june.inner_text()

    def test_nothing_is_counted_at_a_reader_who_has_written_nothing(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-versions-toggle")
        assert tab.locator("#dl-versions-list .dl-version-carry").count() == 0


class TestContinuity:
    """A reader halfway through should not have the ground move."""

    def test_choosing_a_release_takes_them_to_it(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-versions-toggle")
        tab.click("#dl-versions-list .dl-version[data-version='2026.06.02.1'] a")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        assert tab.url.endswith("v2026.06.02.1.html")
        assert "This is the June release." in tab.inner_text("#dl-body")

    def test_and_that_is_where_the_plain_url_takes_them_next_time(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-versions-toggle")
        tab.click("#dl-versions-list .dl-version[data-version='2026.06.02.1'] a")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)

        opened(tab, base_url, DEFAULT_PAGE)
        assert tab.url.endswith("v2026.06.02.1.html")

    def test_work_saved_against_a_release_is_enough_on_its_own(self, tab, base_url):
        """Somebody who was here before a second release existed never picked
        anything. Their saved record says which one they were reading, and that
        is the whole of what a pin needs to be."""
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"shared-one": "print('mine')"}, version="2026.06.02.1")
        opened(tab, base_url, DEFAULT_PAGE)
        assert tab.url.endswith("v2026.06.02.1.html")

    def test_it_never_sends_them_away_from_a_release_they_asked_for(self, tab, base_url):
        """Only ever off the plain URL. Anything else could bounce between two
        pages, and would override a link somebody was deliberately sent."""
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"shared-one": "print('mine')"}, version="2026.06.02.1")
        opened(tab, base_url, JUNE_PAGE)
        assert tab.url.endswith("v2026.06.02.1.html")

    def test_a_release_that_is_gone_leaves_them_where_they_are(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"shared-one": "print('mine')"}, version="2019.01.01.1")
        opened(tab, base_url, DEFAULT_PAGE)
        assert tab.url.endswith(f"{SLUG}.html")

    def test_the_older_page_says_why_they_are_on_it(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"shared-one": "print('mine')"}, version="2026.06.02.1")
        opened(tab, base_url, DEFAULT_PAGE)
        notice = tab.inner_text("#dl-body .dl-archived")
        assert "where you left off" in notice
        assert "2 June 2026 version" in notice

    def test_and_what_moving_to_the_current_one_would_do(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {
            "shared-one": "print('mine')",
            "only-in-june": "print('and this')",
        }, version="2026.06.02.1")
        opened(tab, base_url, DEFAULT_PAGE)
        assert "1 of your 2 answers carry over" in tab.inner_text("#dl-body .dl-archived")


class TestWhatTheRestoreNoticeSays:
    """It used to apologise: your work is back, but "some of it may not line up
    with the new version". Where a tutorial has releases, that guess can be
    replaced by the two dates and a true statement about the answers with no
    cell to go in."""

    def test_it_names_both_releases(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"shared-one": "print('mine')"}, version="2026.06.02.1")
        # Follow the newest, so the reader lands on September with June's work.
        tab.evaluate("() => localStorage.setItem('dewlab:versions-follow', 'newest')")
        opened(tab, base_url, DEFAULT_PAGE)
        notice = tab.inner_text("#dl-body .dl-restored")
        assert "2 June 2026 version" in notice
        assert "15 September 2026 one" in notice

    def test_an_answer_with_nowhere_to_go_is_not_called_lost(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"only-in-june": "print('mine')"}, version="2026.06.02.1")
        tab.evaluate("() => localStorage.setItem('dewlab:versions-follow', 'newest')")
        opened(tab, base_url, DEFAULT_PAGE)
        notice = tab.inner_text("#dl-body .dl-restored")
        assert "this version does not have" in notice
        assert "still saved" in notice


class TestWhichNoticeComesFirst:
    def test_the_page_says_which_release_it_is_before_it_talks_about_your_work(
            self, tab, base_url):
        """Both boxes appear on an older release. Which one you are reading is
        the thing to know first — what happened to your answers only means
        anything once you know which version you are looking at."""
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"shared-one": "print('mine')"}, version="2026.06.02.1")
        opened(tab, base_url, DEFAULT_PAGE)
        order = tab.eval_on_selector_all(
            "#dl-body > .dl-archived, #dl-body > .dl-restored",
            "els => els.map(e => e.className)",
        )
        assert order == ["dl-archived", "dl-restored"]


class TestTheSwitchInSettings:
    def test_it_starts_on_where_i_left_off(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-settings-toggle")
        pressed = tab.eval_on_selector_all(
            "#dl-settings-versions [data-versions-follow] button",
            "els => els.filter(e => e.getAttribute('aria-pressed') === 'true')"
            ".map(e => e.dataset.value)",
        )
        assert pressed == ["started"]

    def test_it_lists_the_releases_too(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-settings-toggle")
        names = tab.eval_on_selector_all(
            "#dl-versions-settings .dl-version-name",
            "els => els.map(e => e.textContent)",
        )
        assert names == ["15 September 2026", "2 June 2026"]

    def test_asking_for_the_newest_takes_them_there_now(self, tab, base_url):
        """Not a preference that applies the next time they visit. Somebody who
        asks for the newest while reading an older one is asking to be on it."""
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"shared-one": "print('mine')"}, version="2026.06.02.1")
        opened(tab, base_url, DEFAULT_PAGE)
        assert tab.url.endswith("v2026.06.02.1.html")

        tab.click("#dl-settings-toggle")
        tab.click("#dl-settings-versions [data-versions-follow] button[data-value=newest]")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        assert tab.url.endswith(f"{SLUG}.html")

    def test_and_stops_them_being_sent_back(self, tab, base_url):
        opened(tab, base_url, DEFAULT_PAGE)
        seed(tab, {"shared-one": "print('mine')"}, version="2026.06.02.1")
        opened(tab, base_url, DEFAULT_PAGE)
        tab.click("#dl-settings-toggle")
        tab.click("#dl-settings-versions [data-versions-follow] button[data-value=newest]")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)

        opened(tab, base_url, DEFAULT_PAGE)
        assert tab.url.endswith(f"{SLUG}.html")
