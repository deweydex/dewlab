"""My Notes (all-notes.html, write_all_notes_page()/my-notes.js): every
highlight and every page's own free-text notes, gathered client-side from
every tutorial's saved-progress record this browser holds -- localStorage
is shared per origin, not per page, so this page needs no server data
beyond the {slug: title} map baked into it at build time.

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
from layout import write_course, write_tutorial  # noqa: E402

COURSE = "my-notes-fixtures"

FRONTMATTER_ONE = """---
title: "First Tutorial"
year: "2026-2027"
version: 2026.08.23.1
---

# First Tutorial

A passage worth marking sits right here, plain and simple.
"""

FRONTMATTER_TWO = """---
title: "Second Tutorial"
year: "2026-2027"
version: 2026.08.23.1
---

# Second Tutorial

Another passage worth marking lives in this one instead.
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
    write_tutorial(tmp_path, "one", FRONTMATTER_ONE)
    write_tutorial(tmp_path, "two", FRONTMATTER_TWO)
    write_course(tmp_path, COURSE, "Sample Series", ["one", "two"])
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


def _make_highlight(page, phrase: str, note: str = "") -> None:
    assert page.evaluate(SELECT, phrase)
    page.wait_for_selector(".dl-highlight-btn:not([hidden])")
    page.click(".dl-highlight-btn")
    page.wait_for_selector("mark.dl-highlight")
    if note:
        page.click("mark.dl-highlight")
        page.wait_for_selector(".dl-highlight-popover:not([hidden])")
        page.fill(".dl-highlight-popover-note", note)
        page.click(".dl-highlight-popover-save")


class TestEmptyState:
    def test_nothing_saved_shows_the_empty_message(self, browser, site_url):
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/all-notes.html")
        page.wait_for_selector("#dl-my-notes-empty:not([hidden])")
        assert page.locator(".dl-my-notes-card").count() == 0
        context.close()


class TestGatheringAcrossTutorials:
    def test_highlights_from_two_tutorials_both_appear(self, browser, site_url):
        context = browser.new_context()
        one = context.new_page()
        one.goto(f"{site_url}/tutorials/one.html")
        one.wait_for_function("() => !!globalThis.dewlab")
        _make_highlight(one, "worth marking", "first note")
        one.wait_for_function("() => dewlab.readSaved() !== null")
        one.close()

        two = context.new_page()
        two.goto(f"{site_url}/tutorials/two.html")
        two.wait_for_function("() => !!globalThis.dewlab")
        _make_highlight(two, "worth marking")
        two.wait_for_function("() => dewlab.readSaved() !== null")
        two.close()

        notes = context.new_page()
        notes.goto(f"{site_url}/all-notes.html")
        notes.wait_for_selector(".dl-my-notes-card")
        assert notes.locator(".dl-my-notes-card").count() == 2
        assert notes.locator(".dl-my-notes-card h2:has-text('First Tutorial')").count() == 1
        assert notes.locator(".dl-my-notes-card h2:has-text('Second Tutorial')").count() == 1
        assert "first note" in notes.inner_text(".dl-my-notes-card")
        assert notes.is_hidden("#dl-my-notes-empty")
        context.close()

    def test_a_card_links_back_to_its_own_highlight(self, browser, site_url):
        context = browser.new_context()
        one = context.new_page()
        one.goto(f"{site_url}/tutorials/one.html")
        one.wait_for_function("() => !!globalThis.dewlab")
        _make_highlight(one, "worth marking")
        one.wait_for_function("() => dewlab.readSaved() !== null")
        highlight_id = one.evaluate("dewlab.highlights[0].id")
        one.close()

        notes = context.new_page()
        notes.goto(f"{site_url}/all-notes.html")
        notes.wait_for_selector(".dl-highlight-row")
        href = notes.get_attribute(".dl-highlight-row", "href")
        assert href == f"tutorials/one.html#dl-highlight-{highlight_id}"
        context.close()

    def test_free_text_notes_appear_too(self, browser, site_url):
        context = browser.new_context()
        one = context.new_page()
        one.goto(f"{site_url}/tutorials/one.html")
        one.wait_for_function("() => !!globalThis.dewlab")
        one.click("#dl-yourwork-toggle")
        one.fill("#dl-progress-notes", "a page note, not a highlight")
        one.wait_for_function("() => dewlab.readSaved() !== null")
        one.close()

        notes = context.new_page()
        notes.goto(f"{site_url}/all-notes.html")
        notes.wait_for_selector(".dl-my-notes-card")
        assert "a page note, not a highlight" in notes.inner_text(".dl-my-notes-freeform")
        context.close()


class TestSearch:
    def test_filtering_hides_the_card_that_does_not_match(self, browser, site_url):
        context = browser.new_context()
        one = context.new_page()
        one.goto(f"{site_url}/tutorials/one.html")
        one.wait_for_function("() => !!globalThis.dewlab")
        _make_highlight(one, "worth marking", "apples")
        one.wait_for_function("() => dewlab.readSaved() !== null")
        one.close()

        two = context.new_page()
        two.goto(f"{site_url}/tutorials/two.html")
        two.wait_for_function("() => !!globalThis.dewlab")
        _make_highlight(two, "worth marking", "oranges")
        two.wait_for_function("() => dewlab.readSaved() !== null")
        two.close()

        notes = context.new_page()
        notes.goto(f"{site_url}/all-notes.html")
        notes.wait_for_selector(".dl-my-notes-card")
        notes.fill("#dl-my-notes-search", "apples")

        visible = notes.locator(".dl-my-notes-card:not([hidden])")
        assert visible.count() == 1
        assert "First Tutorial" in visible.inner_text()
        context.close()


class TestDownload:
    def test_the_download_button_offers_a_text_file(self, browser, site_url):
        context = browser.new_context()
        one = context.new_page()
        one.goto(f"{site_url}/tutorials/one.html")
        one.wait_for_function("() => !!globalThis.dewlab")
        _make_highlight(one, "worth marking", "remember this")
        one.wait_for_function("() => dewlab.readSaved() !== null")
        one.close()

        notes = context.new_page()
        notes.goto(f"{site_url}/all-notes.html")
        notes.wait_for_selector(".dl-my-notes-card")
        with notes.expect_download() as download_info:
            notes.click("#dl-my-notes-download")
        download = download_info.value
        assert download.suggested_filename == "my-dewlab-notes.txt"
        path = download.path()
        text = Path(path).read_text()
        assert "First Tutorial" in text
        assert "worth marking" in text
        assert "remember this" in text
        context.close()
