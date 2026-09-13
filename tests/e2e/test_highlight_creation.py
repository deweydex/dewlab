"""planning/HIGHLIGHTS_AND_NOTES.md §5, rollout step 5: the selection
toolbar's Highlight button -- the first reader-facing way to actually make
a highlight, wired to the anchoring (step 2), schema (step 3), and DOM
wrapping (step 4) rollout steps built before it.

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
import yaml

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402

MODULE = "highlight-creation-fixtures"

FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: highlight-creation-fixtures
module_title: "Highlight Creation Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# {title}

The gradient of a line is one thing, and this whole sentence is fine to mark too.

A second paragraph exists only so a selection can be made to cross into it.
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

# Selects from partway into the first paragraph's last word to partway into
# the second paragraph's first word -- a selection that genuinely crosses a
# block boundary, the case the one-block anchoring constraint (§3) has to
# refuse rather than silently mis-anchor.
SELECT_ACROSS_PARAGRAPHS = """() => {
  const paras = [...document.querySelectorAll('#dl-body p')];
  const first = paras.find((p) => p.textContent.includes('mark too'));
  const second = paras.find((p) => p.textContent.includes('cross into it'));
  const range = document.createRange();
  range.setStart(first.firstChild, first.firstChild.length - 4);
  range.setEnd(second.firstChild, 4);
  const selection = getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
  return true;
}"""


def _tutorial(root: Path, slug: str, title: str = "A Title") -> None:
    path = root / "tutorials" / MODULE / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FRONTMATTER.format(title=title, slug=slug))


def _glossary(root: Path, slug: str, entries: list[dict]) -> None:
    path = root / "tutorials" / MODULE / f"{slug}.glossary.yaml"
    path.write_text(yaml.dump({"entries": entries}))


def _set_order(root: Path, slugs: list[str]) -> None:
    path = root / "tutorials" / MODULE / "sample-series.order.yaml"
    path.write_text("series: Sample Series\norder:\n" + "".join(f"  - {s}\n" for s in slugs))


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials" / MODULE).mkdir(parents=True)
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
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


def _open(browser, site_url, slug="one"):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{site_url}/tutorials/{MODULE}/{slug}.html")
    page.wait_for_function("() => !!globalThis.dewlab")
    return context, page


class TestHighlightButtonWithNoGlossary:
    """A tutorial with no glossary at all gets no Look Up button -- but the
    Highlight button is a different feature (§5) and needs no glossary."""

    def test_still_offers_to_highlight(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context, page = _open(browser, site_url)
        assert page.evaluate(SELECT, "fine to mark")
        page.wait_for_selector(".dl-highlight-btn:not([hidden])")
        assert page.is_hidden(".dl-lookup")
        context.close()


class TestHighlightButtonAlongsideLookUp:
    def test_nothing_is_offered_until_something_is_selected(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [
            {"term": "gradient", "kind": "concept", "definition": "How steeply something changes."},
        ])
        _set_order(site, ["one"])
        b.build()
        context, page = _open(browser, site_url)
        assert page.is_hidden(".dl-lookup")
        assert page.is_hidden(".dl-highlight-btn")
        context.close()

    def test_a_known_term_offers_both_buttons_together(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _glossary(site, "one", [
            {"term": "gradient", "kind": "concept", "definition": "How steeply something changes."},
        ])
        _set_order(site, ["one"])
        b.build()
        context, page = _open(browser, site_url)
        assert page.evaluate(SELECT, "gradient")
        page.wait_for_selector(".dl-lookup:not([hidden])")
        page.wait_for_selector(".dl-highlight-btn:not([hidden])")
        context.close()

    def test_a_selection_crossing_two_paragraphs_offers_no_highlight(
        self, site, browser, site_url
    ):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context, page = _open(browser, site_url)
        assert page.evaluate(SELECT_ACROSS_PARAGRAPHS)
        page.wait_for_timeout(200)
        assert page.is_hidden(".dl-highlight-btn")
        context.close()


class TestClickingHighlight:
    def test_creates_a_visible_mark_and_saves_it(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context, page = _open(browser, site_url)

        assert page.evaluate(SELECT, "this whole sentence is fine to mark too")
        page.wait_for_selector(".dl-highlight-btn:not([hidden])")
        page.click(".dl-highlight-btn")

        mark = page.locator("mark.dl-highlight")
        assert mark.count() > 0
        assert "".join(mark.all_inner_texts()) == "this whole sentence is fine to mark too"

        page.evaluate("dewlab.saveNow()")
        saved = page.evaluate("dewlab.readSaved()")
        assert len(saved["highlights"]) == 1
        assert saved["highlights"][0]["quote"] == "this whole sentence is fine to mark too"
        context.close()

    def test_the_buttons_go_away_after_use(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context, page = _open(browser, site_url)

        assert page.evaluate(SELECT, "fine to mark")
        page.wait_for_selector(".dl-highlight-btn:not([hidden])")
        page.click(".dl-highlight-btn")

        assert page.is_hidden(".dl-highlight-btn")
        assert page.is_hidden(".dl-lookup")
        context.close()

    def test_a_created_highlight_survives_a_reload(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context, page = _open(browser, site_url)

        assert page.evaluate(SELECT, "fine to mark")
        page.wait_for_selector(".dl-highlight-btn:not([hidden])")
        page.click(".dl-highlight-btn")
        highlight_id = page.eval_on_selector("mark.dl-highlight", "el => el.dataset.highlightId")
        # createHighlight() only schedules the debounced autosave -- waiting
        # for it to have actually landed, the same way test_saved_progress.py
        # does before its own reload, rather than racing it.
        page.wait_for_function("() => dewlab.readSaved() !== null")

        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")

        mark = page.locator(f'mark.dl-highlight[data-highlight-id="{highlight_id}"]')
        assert mark.count() > 0
        assert "".join(mark.all_inner_texts()) == "fine to mark"
        context.close()
