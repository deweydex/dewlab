"""Rollout step 3: `highlights` in the saved-progress record. A highlight
round-trips through saveNow()/readSaved() the same way `notes` already
does; one whose anchor no longer resolves on reload is dropped and
reported in the restore summary, the "notice, never a block" treatment
a cell whose id disappeared already gets."""

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

COURSE = "highlight-schema-fixtures"
SLUG = "one"

FRONTMATTER = """---
title: "Highlight Schema Fixture"
year: "2026-2027"
version: 2026.08.23.1
---

# Highlight Schema Fixture

TARGET-PARAGRAPH holds the one passage this test marks and unmarks.

FILLER-PARAGRAPH pads the page out a little.
"""


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


def _reload_and_wait(page):
    page.reload()
    page.wait_for_function("() => !!globalThis.dewlab")


def _seed(page, record: dict):
    page.evaluate(
        "([key, value]) => localStorage.setItem(key, value)",
        [page.evaluate("dewlab.progressKey()"), json.dumps(record)],
    )


def _anchor_for_target_paragraph(page) -> dict:
    """The {block_index, quote, prefix, suffix} anchor for the fixed phrase
    inside TARGET-PARAGRAPH, computed the same way rollout step 5's
    selection toolbar eventually will -- via proseBlocks()/describeQuote(),
    not a hand-picked offset."""
    return page.evaluate(
        """() => {
            const blocks = dewlab.proseBlocks();
            const block = blocks.find((el) => el.textContent.includes("TARGET-PARAGRAPH"));
            const quote = "the one passage this test marks and unmarks";
            const start = block.textContent.indexOf(quote);
            return {
                block_index: blocks.indexOf(block),
                ...dewlab.describeQuote(block, start, start + quote.length),
            };
        }"""
    )


class TestHighlightSchema:
    def test_a_highlight_round_trips_and_a_successful_restore_stays_silent(self, page):
        anchor = _anchor_for_target_paragraph(page)
        page.evaluate(
            """(anchor) => dewlab.highlights.push({
                id: "h-test",
                note: "worth remembering",
                created_at: new Date().toISOString(),
                ...anchor,
            })""",
            anchor,
        )
        page.evaluate("dewlab.saveNow()")

        saved = page.evaluate("dewlab.readSaved()")
        assert len(saved["highlights"]) == 1
        assert saved["highlights"][0]["id"] == "h-test"
        assert saved["highlights"][0]["note"] == "worth remembering"

        _reload_and_wait(page)
        restored = page.evaluate("dewlab.highlights")
        assert len(restored) == 1
        assert restored[0]["id"] == "h-test"
        assert restored[0]["note"] == "worth remembering"
        # A successful restore is silent -- announceRestore()'s guard only
        # fires on a dropped highlight (or cell), never on an ordinary one.
        assert page.locator(".dl-restored").count() == 0

    def test_a_dropped_highlight_keeps_its_note_and_is_reported_in_the_restore_summary(
        self, page
    ):
        # The anchor is what can go stale, not the note -- the record still
        # carries the note in localStorage even once the highlight itself
        # is dropped from the live page, in case a future version's prose
        # brings the same passage back (or a student exports the file). The
        # restore box, meanwhile, is the reader-visible half of that same
        # drop.
        _seed(page, {
            "tutorial-id": SLUG,
            "tutorial-version": "2026.08.23.1",
            "saved_at": "2026-01-01T00:00:00.000Z",
            "notes": "",
            "cells": [],
            "highlights": [{
                "id": "h-gone",
                "block_index": 0,
                "quote": "text this fixture never actually contains anywhere",
                "prefix": "",
                "suffix": "",
                "note": "a note worth keeping even if the highlight itself is gone",
                "created_at": "2026-01-01T00:00:00.000Z",
            }],
        })
        _reload_and_wait(page)

        assert page.evaluate("dewlab.highlights") == []
        saved = page.evaluate("dewlab.readSaved()")
        assert saved["highlights"][0]["note"] == (
            "a note worth keeping even if the highlight itself is gone"
        )
        box = page.locator(".dl-restored")
        assert box.count() == 1
        assert "could not be put back" in box.inner_text()

    def test_two_dropped_highlights_use_the_plural_wording(self, page):
        _seed(page, {
            "tutorial-id": SLUG,
            "tutorial-version": "2026.08.23.1",
            "saved_at": "2026-01-01T00:00:00.000Z",
            "notes": "",
            "cells": [],
            "highlights": [
                {
                    "id": "h-gone-1", "block_index": 0, "quote": "nope, gone one",
                    "prefix": "", "suffix": "", "note": "", "created_at": "2026-01-01T00:00:00.000Z",
                },
                {
                    "id": "h-gone-2", "block_index": 1, "quote": "nope, gone two",
                    "prefix": "", "suffix": "", "note": "", "created_at": "2026-01-01T00:00:00.000Z",
                },
            ],
        })
        _reload_and_wait(page)

        box_text = page.locator(".dl-restored").inner_text()
        assert "2 of your highlights were" in box_text
