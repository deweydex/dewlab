"""A highlight's colour (the popover's swatch row, mark[data-highlight-color],
HIGHLIGHT_COLORS) and the Notes panel's "Your highlights" list
(refreshHighlightsList(), renderHighlightRow(), jumpToHighlight()) -- built
on top of the base highlight feature (rollout steps 4-6) rather than
changing its schema's meaning: a highlight with no colour is still a
plain, valid, amber highlight, the same one that shipped before this.

Every fixture here is prose-only, so tutorial-runtime.js never boots
Pyodide for these pages -- unlike most of tests/e2e/, this file runs
without `python3 dev/fetch_pyodide.py` first."""

from __future__ import annotations

import functools
import http.server
import json
import socketserver
import sys
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402
from layout import write_course, write_tutorial  # noqa: E402

COURSE = "highlight-colors-fixtures"
SLUG = "one"

FRONTMATTER = """---
title: "Highlight Colors Fixture"
year: "2026-2027"
version: 2026.08.23.1
---

# Highlight Colors Fixture

This whole sentence is fine to mark, and a reader might want to say why.

A second passage worth marking sits here, once the first one already exists.
"""

SELECT = """(word) => {
  const walk = document.createTreeWalker(
    document.getElementById('dl-body'), NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walk.nextNode())) {
    const at = node.textContent.indexOf(word);
    if (at >= 0 && !node.parentElement.closest('.dl-editor')) {
      const range = document.createRange();
      range.setStart(node, at);
      range.setEnd(node, at + word.length);
      const selection = getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      return true;
    }
  }
  return false;
}"""


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, SLUG, FRONTMATTER)
    write_course(tmp_path, COURSE, "Sample Series", ["one"])
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "COURSES", tmp_path / "courses")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
    b.build()
    return tmp_path


def _serve(out_dir: Path):
    handler = functools.partial(_QuietHandler, directory=str(out_dir))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{port}"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture()
def site_url(site):
    server, thread, url = _serve(site / "site")
    try:
        yield url
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def page(browser, site_url):
    context = browser.new_context()
    dl_page = context.new_page()
    dl_page.goto(f"{site_url}/tutorials/{SLUG}.html")
    dl_page.wait_for_function("() => !!globalThis.dewlab")
    yield dl_page
    context.close()


def _make_highlight(page, phrase: str) -> None:
    assert page.evaluate(SELECT, phrase)
    page.wait_for_selector(".dl-highlight-btn:not([hidden])")
    page.click(".dl-highlight-btn")
    page.wait_for_selector("mark.dl-highlight")


def _open_notes(page) -> None:
    page.click("#dl-yourwork-toggle")
    page.wait_for_selector("#dl-yourwork:not([hidden])")


class TestDefaultColor:
    def test_a_fresh_highlight_is_amber_with_no_data_attribute(self, page):
        _make_highlight(page, "fine to mark")
        assert page.evaluate("dewlab.highlights[0].color") == "amber"
        # Amber is the CSS default (mark.dl-highlight's own background),
        # so a plain highlight carries no override attribute at all.
        assert page.get_attribute("mark.dl-highlight", "data-highlight-color") is None


class TestChoosingAColor:
    def test_clicking_a_swatch_recolors_the_mark(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.click('.dl-highlight-popover-color[data-color="green"]')

        assert page.get_attribute("mark.dl-highlight", "data-highlight-color") == "green"
        assert page.evaluate("dewlab.highlights[0].color") == "green"

    def test_the_choice_is_saved_and_survives_a_reload(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.click('.dl-highlight-popover-color[data-color="blue"]')

        page.wait_for_function(
            "() => dewlab.readSaved()?.highlights?.[0]?.color === 'blue'"
        )
        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")
        page.wait_for_selector("mark.dl-highlight")
        assert page.get_attribute("mark.dl-highlight", "data-highlight-color") == "blue"

    def test_reopening_the_popover_shows_the_chosen_swatch_checked(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.click('.dl-highlight-popover-color[data-color="pink"]')
        page.keyboard.press("Escape")

        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        checked = page.eval_on_selector(
            '.dl-highlight-popover-color[data-color="pink"]',
            "el => el.getAttribute('aria-checked')",
        )
        assert checked == "true"

    def test_a_new_highlight_defaults_to_the_last_colour_used(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.click('.dl-highlight-popover-color[data-color="green"]')
        page.keyboard.press("Escape")

        _make_highlight(page, "second passage")
        assert page.evaluate("dewlab.highlights[1].color") == "green"


class TestHighlightsListInNotesPanel:
    def test_empty_state_before_anything_is_highlighted(self, page):
        _open_notes(page)
        assert page.is_visible("#dl-highlights-status")
        assert page.locator(".dl-highlight-row").count() == 0

    def test_a_highlight_appears_in_the_list_with_its_quote(self, page):
        _make_highlight(page, "fine to mark")
        _open_notes(page)
        assert page.locator(".dl-highlight-row").count() == 1
        assert "fine to mark" in page.inner_text(".dl-highlight-quote")
        assert page.is_hidden("#dl-highlights-status")

    def test_a_note_shows_as_a_preview_in_its_row(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.fill(".dl-highlight-popover-note", "remember why")
        page.click(".dl-highlight-popover-save")

        _open_notes(page)
        assert "remember why" in page.inner_text(".dl-highlight-note")

    def test_removing_a_highlight_drops_its_row(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.on("dialog", lambda dialog: pytest.fail(f"unexpected dialog: {dialog.message}"))
        page.click(".dl-highlight-popover-remove")

        _open_notes(page)
        assert page.locator(".dl-highlight-row").count() == 0
        assert page.is_visible("#dl-highlights-status")

    def test_clicking_a_row_scrolls_to_and_opens_its_highlight(self, page):
        _make_highlight(page, "second passage")
        _open_notes(page)
        page.click(".dl-highlight-row")

        # The Notes panel itself closes -- jumpToHighlight() calls
        # closeRightPanels() before scrolling, so the highlight underneath
        # is actually visible once this returns.
        assert page.is_hidden("#dl-yourwork")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        assert page.evaluate(
            "() => document.querySelector('mark.dl-highlight')"
            ".getBoundingClientRect().top >= 0"
        )


def _seed(page, highlight: dict):
    page.evaluate(
        "([key, value]) => localStorage.setItem(key, value)",
        [
            page.evaluate("dewlab.progressKey()"),
            json.dumps({
                "tutorial-id": SLUG,
                "tutorial-version": "2026.08.23.1",
                "notes": "",
                "highlights": [highlight],
                "cells": [],
            }),
        ],
    )


class TestJumpFromAnotherPageViaTheUrlHash:
    # A hash-only change to a URL Playwright's own page is already on is a
    # same-document fragment navigation, the ordinary web-platform
    # behaviour for clicking a same-page "#anchor" link -- it does not
    # reload the document or re-run its scripts. Arriving from My Notes
    # (or anywhere else) is a genuine cross-page navigation instead, so
    # each of these tests opens the hash URL as a fresh page in a new tab
    # rather than re-using `page`, the same context (so localStorage
    # still carries the highlight seeded through the first tab) but an
    # honestly fresh load.
    def test_a_hash_naming_a_highlight_scrolls_to_it_without_opening_the_popover(
        self, page, browser, site_url
    ):
        anchor = page.evaluate(
            """() => {
                const blocks = dewlab.proseBlocks();
                const block = blocks.find((el) => el.textContent.includes('second passage'));
                const quote = 'second passage worth marking';
                const start = block.textContent.indexOf(quote);
                return {
                    block_index: blocks.indexOf(block),
                    ...dewlab.describeQuote(block, start, start + quote.length),
                };
            }"""
        )
        _seed(page, {
            "id": "h-hash-target", "note": "", "color": "green",
            "created_at": "2026-01-01T00:00:00.000Z", **anchor,
        })

        fresh = page.context.new_page()
        fresh.goto(f"{site_url}/tutorials/{SLUG}.html#dl-highlight-h-hash-target")
        fresh.wait_for_function("() => !!globalThis.dewlab")
        fresh.wait_for_selector('mark.dl-highlight[data-highlight-id="h-hash-target"]')

        assert fresh.is_hidden(".dl-highlight-popover")
        assert fresh.evaluate(
            "() => document.querySelector('mark.dl-highlight[data-highlight-id=\"h-hash-target\"]')"
            ".classList.contains('dl-highlight-flash')"
        )
        fresh.close()

    def test_a_hash_naming_no_real_highlight_is_ignored(self, page, site_url):
        fresh = page.context.new_page()
        fresh.goto(f"{site_url}/tutorials/{SLUG}.html#dl-highlight-nonexistent")
        fresh.wait_for_function("() => !!globalThis.dewlab")
        assert fresh.is_hidden(".dl-highlight-popover")
        fresh.close()


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("color", ["green", "blue", "pink"])
def test_every_new_colour_meets_aa_against_its_own_background(browser, site_url, scheme, color):
    page = browser.new_page(color_scheme=scheme)
    try:
        page.goto(f"{site_url}/tutorials/{SLUG}.html")
        page.wait_for_function("() => !!globalThis.dewlab")
        anchor = page.evaluate(
            """() => {
                const blocks = dewlab.proseBlocks();
                const block = blocks.find((el) => el.textContent.includes('second passage'));
                const quote = 'second passage worth marking';
                const start = block.textContent.indexOf(quote);
                return {
                    block_index: blocks.indexOf(block),
                    ...dewlab.describeQuote(block, start, start + quote.length),
                };
            }"""
        )
        _seed(page, {
            "id": "h-contrast", "note": "", "color": color,
            "created_at": "2026-01-01T00:00:00.000Z", **anchor,
        })
        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")

        measured = page.evaluate(
            """() => {
                const mark = document.querySelector('mark.dl-highlight[data-highlight-id="h-contrast"]');
                const style = getComputedStyle(mark);
                return {
                    color: style.color,
                    background: style.backgroundColor,
                    size: parseFloat(style.fontSize),
                };
            }"""
        )
        fg = _parse_rgb(measured["color"])
        background = _parse_rgb(measured["background"])
        ratio = _contrast_ratio(fg, background)
        assert measured["size"] < 24
        assert ratio >= 4.5, (
            f"{scheme}/{color}: highlight text {measured['color']} on "
            f"{measured['background']} is {ratio:.2f}:1, under the 4.5:1 AA minimum"
        )
    finally:
        page.close()


def _channel(value):
    v = value / 255
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def _relative_luminance(rgb):
    r, g, bl = (_channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * bl


def _contrast_ratio(fg, bg):
    """WCAG's own formula, so the number here is the number that is cited."""
    high, low = sorted((_relative_luminance(fg), _relative_luminance(bg)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def _parse_rgb(value):
    inner = value[value.index("(") + 1:value.index(")")]
    return tuple(int(float(part)) for part in inner.split(",")[:3])
