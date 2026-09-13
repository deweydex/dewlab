"""planning/HIGHLIGHTS_AND_NOTES.md §7, rollout step 6: the edit/remove
popover on an existing highlight -- clicking a `<mark>` (or reaching it with
Tab, per wrapRange()'s first-fragment tab stop, then Enter) opens it.

Every fixture here is prose-only, so tutorial-runtime.js never boots
Pyodide for these pages -- unlike most of tests/e2e/, this file runs
without `python3 dev/fetch_pyodide.py` first."""

from __future__ import annotations

import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402

MODULE = "highlight-popover-fixtures"

FRONTMATTER = """---
title: "One"
slug: one
module: highlight-popover-fixtures
module_title: "Highlight Popover Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# One

This whole sentence is fine to mark, and a reader might want to say why.
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
    (tmp_path / "tutorials" / MODULE).mkdir(parents=True)
    (tmp_path / "tutorials" / MODULE / "one.md").write_text(FRONTMATTER)
    (tmp_path / "tutorials" / MODULE / "sample-series.order.yaml").write_text(
        "series: Sample Series\norder:\n  - one\n"
    )
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
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
    dl_page.goto(f"{site_url}/tutorials/{MODULE}/one.html")
    dl_page.wait_for_function("() => !!globalThis.dewlab")
    yield dl_page
    context.close()


def _make_highlight(page, phrase: str) -> None:
    assert page.evaluate(SELECT, phrase)
    page.wait_for_selector(".dl-highlight-btn:not([hidden])")
    page.click(".dl-highlight-btn")
    page.wait_for_selector("mark.dl-highlight")


class TestOpeningThePopover:
    def test_clicking_a_highlight_opens_it_with_an_empty_note(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        assert page.input_value(".dl-highlight-popover-note") == ""

    def test_keyboard_activation_opens_it_too(self, page):
        _make_highlight(page, "fine to mark")
        page.eval_on_selector("mark.dl-highlight", "el => el.focus()")
        page.keyboard.press("Enter")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")

    def test_escape_closes_it(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.keyboard.press("Escape")
        assert page.is_hidden(".dl-highlight-popover")

    def test_clicking_outside_closes_it(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.click("h1")
        assert page.is_hidden(".dl-highlight-popover")


class TestSavingANote:
    def test_typing_a_note_and_saving_persists_it(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.fill(".dl-highlight-popover-note", "worth remembering")
        page.click(".dl-highlight-popover-save")

        assert page.is_hidden(".dl-highlight-popover")
        assert page.evaluate("dewlab.highlights[0].note") == "worth remembering"

        page.wait_for_function("() => dewlab.readSaved() !== null")
        saved = page.evaluate("dewlab.readSaved()")
        assert saved["highlights"][0]["note"] == "worth remembering"

    def test_reopening_shows_the_saved_note(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.fill(".dl-highlight-popover-note", "worth remembering")
        page.click(".dl-highlight-popover-save")

        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        assert page.input_value(".dl-highlight-popover-note") == "worth remembering"


class TestRemovingAHighlight:
    def test_a_highlight_with_no_note_is_removed_without_asking(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")

        # No confirm() dialog should appear at all -- fail loudly if one does,
        # rather than silently auto-handling it and masking the bug.
        page.on("dialog", lambda dialog: pytest.fail(f"unexpected dialog: {dialog.message}"))
        page.click(".dl-highlight-popover-remove")

        assert page.locator("mark.dl-highlight").count() == 0
        assert page.evaluate("dewlab.highlights") == []

    def test_a_highlight_with_a_note_asks_for_confirmation(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.fill(".dl-highlight-popover-note", "worth remembering")
        page.click(".dl-highlight-popover-save")

        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.once("dialog", lambda dialog: dialog.accept())
        page.click(".dl-highlight-popover-remove")

        assert page.locator("mark.dl-highlight").count() == 0
        assert page.evaluate("dewlab.highlights") == []

    def test_declining_the_confirmation_keeps_the_highlight_and_its_note(self, page):
        _make_highlight(page, "fine to mark")
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.fill(".dl-highlight-popover-note", "worth remembering")
        page.click(".dl-highlight-popover-save")

        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.click(".dl-highlight-popover-remove")

        assert page.locator("mark.dl-highlight").count() == 1
        assert page.evaluate("dewlab.highlights[0].note") == "worth remembering"
