"""My words (#340; assets/my-words.js): a word selected on one page and
saved with the reader's own meaning. The list is one localStorage key for
the whole site, so the word is marked on every other page where it
appears, and shows the reader's meaning there. It survives a reload, and
an exported file imports again into an empty browser.

Every fixture here is prose-only, so no page boots Pyodide: like
test_my_notes.py, this file runs without `python3 dev/fetch_pyodide.py`."""

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

ONE = """---
title: "Charging a Capacitor"
year: "2026-2027"
version: 2026.09.27.1
---

# Charging a Capacitor

A *capacitor* stores charge. The battery pushes current through the
resistor. Then the capacitor fills, more and more slowly.
"""

GLOSSARY_ONE = """entries:
  - term: capacitor
    kind: concept
    definition: >
      A part that stores electric charge.
"""

TWO = """---
title: "A Light That Blinks"
year: "2026-2027"
version: 2026.09.27.1
---

# A Light That Blinks

The capacitor empties through the light. Then the capacitor fills again.

Two capacitors in a row fill more slowly.

The `capacitor` in this code is not prose.
"""

SELECT = """(word) => {
  const walk = document.createTreeWalker(
    document.getElementById('dl-body'), NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walk.nextNode())) {
    const at = node.textContent.indexOf(word);
    if (at >= 0 && !node.parentElement.closest('.dl-editor, code, em')) {
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

# The same, for a phrase that crosses a mark: found by its paragraph's own
# text, and the range built from the text nodes inside it.
SELECT_ACROSS = """(phrase) => {
  const block = [...document.querySelectorAll('#dl-body p')].find((p) => p.textContent.includes(phrase));
  if (!block) return false;
  const start = block.textContent.indexOf(phrase);
  const end = start + phrase.length;
  const range = document.createRange();
  const walk = document.createTreeWalker(block, NodeFilter.SHOW_TEXT);
  let seen = 0;
  let node;
  while ((node = walk.nextNode())) {
    const next = seen + node.data.length;
    if (start >= seen && start <= next) range.setStart(node, start - seen);
    if (end >= seen && end <= next) { range.setEnd(node, end - seen); break; }
    seen = next;
  }
  getSelection().removeAllRanges();
  getSelection().addRange(range);
  return true;
}"""


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, "one", ONE)
    (tmp_path / "tutorials" / "one" / "one.glossary.yaml").write_text(GLOSSARY_ONE)
    write_tutorial(tmp_path, "two", TWO)
    write_course(tmp_path, "my-words-fixtures", "Sample Series", ["one", "two"])
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


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture()
def site_url(site):
    handler = functools.partial(_QuietHandler, directory=str(site / "site"))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def _open(context, url):
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.errors = errors
    page.goto(url)
    page.wait_for_function("() => !!globalThis.dewlab && !!dewlab.myWords")
    return page


def _save_word(page, word: str, meaning: str) -> None:
    assert page.evaluate(SELECT, word)
    page.wait_for_selector(".dl-myword-btn:not([hidden])")
    page.click(".dl-myword-btn")
    page.wait_for_selector("#dl-word-form:not([hidden])")
    page.fill("#dl-word-meaning", meaning)
    page.click("#dl-word-save")
    page.wait_for_selector("#dl-word-form", state="hidden")


class TestSaving:
    def test_the_entry_holds_the_word_sentence_page_meaning_and_definition(self, browser, site_url):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(page, "resistor", "a part that slows the current")
        [entry] = page.evaluate("dewlab.readWords()")
        assert entry["word"] == "resistor"
        assert entry["meaning"] == "a part that slows the current"
        assert entry["sentence"] == "The battery pushes current through the resistor."
        assert entry["page"] == "one"
        assert entry["title"] == "Charging a Capacitor"
        assert entry["path"] == "tutorials/one.html"
        assert entry["definition"] == ""
        assert page.errors == []
        context.close()

    def test_a_glossary_definition_is_kept_with_the_word(self, browser, site_url):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/one.html")
        # The first "capacitor" is the author's italic; select a later one.
        assert page.evaluate("""() => {
          const p = [...document.querySelectorAll('#dl-body p')].find((el) => el.textContent.includes('Then the capacitor'));
          const node = [...p.childNodes].find((n) => n.nodeType === 3 && n.data.includes('Then the capacitor'));
          const at = node.data.indexOf('capacitor');
          const range = document.createRange();
          range.setStart(node, at); range.setEnd(node, at + 9);
          getSelection().removeAllRanges(); getSelection().addRange(range);
          return true;
        }""")
        page.wait_for_selector(".dl-myword-btn:not([hidden])")
        page.click(".dl-myword-btn")
        page.wait_for_selector("#dl-word-form:not([hidden])")
        assert "A part that stores electric charge." in page.inner_text("#dl-word-definition")
        page.fill("#dl-word-meaning", "condensateur")
        page.click("#dl-word-save")
        [entry] = page.evaluate("dewlab.readWords()")
        assert entry["term"] == "capacitor"
        assert entry["definition"] == "A part that stores electric charge."
        context.close()

    def test_saving_a_word_twice_opens_the_first_one(self, browser, site_url):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(page, "resistor", "first meaning")
        assert page.evaluate(SELECT, "resistor")
        page.wait_for_selector(".dl-myword-btn:not([hidden])")
        page.click(".dl-myword-btn")
        page.wait_for_selector("#dl-word-form:not([hidden])")
        assert page.input_value("#dl-word-meaning") == "first meaning"
        assert "You saved this word before" in page.inner_text("#dl-word-form-note")
        page.click("#dl-word-cancel")
        assert len(page.evaluate("dewlab.readWords()")) == 1
        context.close()


class TestOnAnotherPage:
    def test_a_word_saved_on_one_page_shows_its_meaning_on_another(self, browser, site_url):
        context = browser.new_context()
        one = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(one, "capacitor", "condensateur")
        one.close()

        two = _open(context, f"{site_url}/tutorials/two.html")
        marks = two.locator("#dl-body .dl-myword")
        # Once in each paragraph where it appears, plural included, and never
        # in code.
        assert marks.count() == 2
        assert marks.nth(0).inner_text() == "capacitor"
        assert marks.nth(1).inner_text() == "capacitors"
        assert two.locator("code .dl-myword").count() == 0
        marks.nth(0).hover()
        two.wait_for_selector(".dl-myword-popover:not([hidden])")
        assert "condensateur" in two.inner_text(".dl-myword-popover")
        assert two.errors == []
        context.close()

    def test_marks_leave_the_text_as_it_was(self, browser, site_url):
        context = browser.new_context()
        one = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(one, "capacitor", "condensateur")
        one.close()
        two = _open(context, f"{site_url}/tutorials/two.html")
        text_with = two.evaluate("document.getElementById('dl-body').textContent")
        two.click("#dl-settings-toggle")
        two.click('[data-mywords] button[data-value="off"]')
        assert two.locator(".dl-myword").count() == 0
        assert two.evaluate("document.getElementById('dl-body').textContent") == text_with
        two.click('[data-mywords] button[data-value="on"]')
        assert two.locator("#dl-body .dl-myword").count() == 2
        context.close()

    def test_a_highlight_over_a_marked_word_still_works(self, browser, site_url):
        context = browser.new_context()
        one = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(one, "capacitor", "condensateur")
        one.close()
        two = _open(context, f"{site_url}/tutorials/two.html")
        assert two.locator("#dl-body .dl-myword").count() == 2
        assert two.evaluate(SELECT_ACROSS, "The capacitor empties")
        two.wait_for_selector(".dl-highlight-btn:not([hidden])")
        two.click(".dl-highlight-btn")
        two.wait_for_selector("mark.dl-highlight")
        assert two.evaluate("dewlab.highlights[0].quote") == "The capacitor empties"
        context.close()


class TestKeeping:
    def test_the_list_survives_a_reload(self, browser, site_url):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(page, "resistor", "a part that slows the current")
        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab && !!dewlab.myWords")
        # The page remembers an open panel across a reload.
        if page.is_hidden("#dl-yourwork"):
            page.click("#dl-yourwork-toggle")
        page.wait_for_selector(".dl-word-item")
        assert "a part that slows the current" in page.inner_text("#dl-words-list")
        context.close()

    def test_changing_and_deleting_a_word(self, browser, site_url):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(page, "resistor", "old meaning")
        page.click(".dl-word-edit")
        page.fill("#dl-word-meaning", "new meaning")
        page.click("#dl-word-save")
        assert page.evaluate("dewlab.readWords()[0].meaning") == "new meaning"
        page.click(".dl-word-delete")
        assert page.evaluate("dewlab.readWords()") == []
        assert page.inner_text("#dl-words-status") == "No words saved yet."
        context.close()

    def test_search_and_order(self, browser, site_url):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(page, "resistor", "slows the current")
        _save_word(page, "battery", "pushes the current")
        page.click('[data-words-sort] button[data-value="az"]')
        words = page.locator(".dl-word-head strong").all_inner_texts()
        assert words == ["battery", "resistor"]
        page.fill("#dl-words-search", "slows")
        assert page.locator(".dl-word-head strong").all_inner_texts() == ["resistor"]
        page.fill("#dl-words-search", "nothing like it")
        assert page.inner_text("#dl-words-status") == "No word matches your search."
        context.close()

    def test_an_export_imports_into_an_empty_browser(self, browser, site_url, tmp_path):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(page, "resistor", "a part that slows the current")
        _save_word(page, "battery", "pushes the current")
        before = page.evaluate("dewlab.readWords()")
        page.click("#dl-settings-toggle")
        page.click("#dl-settings-tab-importsexports")
        with page.expect_download() as download:
            page.click("#dl-words-export")
        assert download.value.suggested_filename == "my-dewlab-words.json"
        saved = tmp_path / "words.json"
        download.value.save_as(saved)
        data = json.loads(saved.read_text())
        assert data["dewlab"] == "my-words" and len(data["words"]) == 2
        context.close()

        fresh = browser.new_context()
        page = _open(fresh, f"{site_url}/tutorials/two.html")
        assert page.evaluate("dewlab.readWords()") == []
        page.click("#dl-settings-toggle")
        page.click("#dl-settings-tab-importsexports")
        page.set_input_files("#dl-words-file", str(saved))
        page.wait_for_function("() => dewlab.readWords().length === 2")
        assert page.evaluate("dewlab.readWords()") == before
        assert page.inner_text("#dl-words-io-status") == "Added 2 words."
        # Importing the same file again changes nothing.
        page.set_input_files("#dl-words-file", str(saved))
        page.wait_for_function("() => document.getElementById('dl-words-io-status').textContent === 'Added 0 words.'")
        assert len(page.evaluate("dewlab.readWords()")) == 2
        fresh.close()

    def test_a_file_that_is_not_my_words_changes_nothing(self, browser, site_url, tmp_path):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/one.html")
        _save_word(page, "resistor", "kept")
        other = tmp_path / "other.json"
        other.write_text(json.dumps({"cells": []}))
        page.click("#dl-settings-toggle")
        page.click("#dl-settings-tab-importsexports")
        page.set_input_files("#dl-words-file", str(other))
        page.wait_for_function("() => document.getElementById('dl-words-io-status').textContent.length > 0")
        assert "not a copy of My words" in page.inner_text("#dl-words-io-status")
        assert page.evaluate("dewlab.readWords()[0].meaning") == "kept"
        context.close()

    def test_imported_text_is_never_read_as_markup(self, browser, site_url, tmp_path):
        context = browser.new_context()
        page = _open(context, f"{site_url}/tutorials/two.html")
        evil = tmp_path / "evil.json"
        evil.write_text(json.dumps({"dewlab": "my-words", "version": 1, "words": [
            {"id": "w-1", "word": "capacitor", "meaning": "<img src=x onerror=window.pwned=1>",
             "title": "<b>bold</b>", "path": "javascript:alert(1)"}]}))
        page.click("#dl-settings-toggle")
        page.click("#dl-settings-tab-importsexports")
        page.set_input_files("#dl-words-file", str(evil))
        page.wait_for_function("() => dewlab.readWords().length === 1")
        page.click("#dl-yourwork-toggle")
        assert page.locator("#dl-words-list img").count() == 0
        assert page.evaluate("window.pwned === undefined")
        assert "<img src=x" in page.inner_text("#dl-words-list")
        context.close()


class TestOnAPhone:
    def test_the_button_fits_on_a_narrow_screen(self, browser, site_url):
        context = browser.new_context(viewport={"width": 360, "height": 740}, has_touch=True,
                                      is_mobile=True)
        page = _open(context, f"{site_url}/tutorials/one.html")
        assert page.evaluate(SELECT, "resistor")
        page.wait_for_selector(".dl-myword-btn:not([hidden])")
        for selector in (".dl-highlight-btn", ".dl-myword-btn"):
            box = page.locator(selector).bounding_box()
            assert box["x"] >= 0 and box["x"] + box["width"] <= 360, selector
        page.tap(".dl-myword-btn")
        page.wait_for_selector("#dl-word-form:not([hidden])")
        page.fill("#dl-word-meaning", "on a phone")
        page.tap("#dl-word-save")
        assert page.evaluate("dewlab.readWords()[0].meaning") == "on a phone"
        context.close()
