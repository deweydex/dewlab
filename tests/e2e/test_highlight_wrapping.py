"""planning/HIGHLIGHTS_AND_NOTES.md §6, rollout step 4: wrapping/unwrapping a
Range in `<mark class="dl-highlight">`, and rangeForOffsets() -- the bridge
that turns locateHighlightAnchor()'s plain number back into something
wrapRange() can actually show. Together these are what makes a *restored*
highlight visible on reload, with nothing selected by a reader yet."""

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

MODULE = "highlight-wrap-fixtures"
SLUG = "one"

FRONTMATTER = """---
title: "Highlight Wrap Fixture"
slug: one
module: highlight-wrap-fixtures
module_title: "Highlight Wrap Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# Highlight Wrap Fixture

TARGET-PARAGRAPH begins here, with *word* emphasised right after it.

PLAIN-PARAGRAPH holds a passage worth marking on reload, nothing fancy in it.
"""


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials" / MODULE).mkdir(parents=True)
    (tmp_path / "tutorials" / MODULE / f"{SLUG}.md").write_text(FRONTMATTER)
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
    dl_page.goto(f"{site_url}/tutorials/{MODULE}/{SLUG}.html")
    dl_page.wait_for_function("() => !!globalThis.dewlab")
    yield dl_page
    context.close()


def _seed(page, highlight: dict):
    page.evaluate(
        "([key, value]) => localStorage.setItem(key, value)",
        [
            page.evaluate("dewlab.progressKey()"),
            json.dumps({
                "tutorial-slug": SLUG,
                "tutorial-module": MODULE,
                "tutorial-version": "2026.08.23.1",
                "saved_at": "2026-01-01T00:00:00.000Z",
                "notes": "",
                "cells": [],
                "highlights": [highlight],
            }),
        ],
    )


class TestWrapRange:
    def test_wraps_a_selection_spanning_a_child_element(self, page):
        # A range from inside the plain text before <em>word</em> to inside
        # the plain text after it -- the exact shape a real reader's
        # selection would have, and the one Range.surroundContents() can't
        # handle in one call.
        result = page.evaluate(
            """() => {
                const block = [...document.querySelectorAll('p')].find(
                    (p) => p.textContent.includes('TARGET-PARAGRAPH')
                );
                const before = block.firstChild;
                const em = block.querySelector('em');
                const after = em.nextSibling;
                const range = document.createRange();
                range.setStart(before, before.length - 5);
                range.setEnd(after, 11);
                const marks = dewlab.wrapRange(range, 'h-multi');
                return {
                    count: marks.length,
                    ids: [...new Set(marks.map((m) => m.dataset.highlightId))],
                    text: marks.map((m) => m.textContent).join(''),
                    blockText: block.textContent,
                };
            }"""
        )
        assert result["count"] == 3  # "with ", "word", " emphasised"
        assert result["ids"] == ["h-multi"]
        assert result["text"] == "with word emphasised"
        assert "TARGET-PARAGRAPH begins here, with word emphasised right after it." \
            == result["blockText"]

    def test_unwrap_restores_plain_text_without_touching_the_prose(self, page):
        page.evaluate(
            """() => {
                const block = [...document.querySelectorAll('p')].find(
                    (p) => p.textContent.includes('TARGET-PARAGRAPH')
                );
                const before = block.firstChild;
                const em = block.querySelector('em');
                const after = em.nextSibling;
                const range = document.createRange();
                range.setStart(before, before.length - 5);
                range.setEnd(after, 11);
                dewlab.wrapRange(range, 'h-multi');
            }"""
        )
        result = page.evaluate(
            """() => {
                const removed = dewlab.unwrapHighlight('h-multi');
                const block = [...document.querySelectorAll('p')].find(
                    (p) => p.textContent.includes('TARGET-PARAGRAPH')
                );
                return {
                    removed,
                    marksLeft: document.querySelectorAll('.dl-highlight').length,
                    blockText: block.textContent,
                    emText: block.querySelector('em').textContent,
                };
            }"""
        )
        assert result["removed"] == 3
        assert result["marksLeft"] == 0
        assert result["blockText"] == (
            "TARGET-PARAGRAPH begins here, with word emphasised right after it."
        )
        assert result["emText"] == "word"


class TestRangeForOffsets:
    def test_builds_a_range_that_wraps_the_same_text_describe_quote_saw(self, page):
        result = page.evaluate(
            """() => {
                const block = [...document.querySelectorAll('p')].find(
                    (p) => p.textContent.includes('TARGET-PARAGRAPH')
                );
                const quote = 'with word emphasised';
                const start = block.textContent.indexOf(quote);
                const range = dewlab.rangeForOffsets(block, start, start + quote.length);
                const marks = dewlab.wrapRange(range, 'h-roundtrip');
                return marks.map((m) => m.textContent).join('');
            }"""
        )
        assert result == "with word emphasised"


class TestRestoredHighlightsRenderVisibly:
    def test_a_restored_highlight_appears_as_a_visible_mark(self, page):
        anchor = page.evaluate(
            """() => {
                const blocks = dewlab.proseBlocks();
                const block = blocks.find((el) => el.textContent.includes('PLAIN-PARAGRAPH'));
                const quote = 'a passage worth marking on reload';
                const start = block.textContent.indexOf(quote);
                return {
                    block_index: blocks.indexOf(block),
                    ...dewlab.describeQuote(block, start, start + quote.length),
                };
            }"""
        )
        _seed(page, {
            "id": "h-visible",
            "note": "",
            "created_at": "2026-01-01T00:00:00.000Z",
            **anchor,
        })
        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")

        mark = page.locator('mark.dl-highlight[data-highlight-id="h-visible"]')
        assert mark.count() > 0
        assert "".join(mark.all_inner_texts()) == "a passage worth marking on reload"


@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_a_highlight_meets_aa_against_its_own_background(browser, site_url, scheme):
    page = browser.new_page(color_scheme=scheme)
    try:
        page.goto(f"{site_url}/tutorials/{MODULE}/{SLUG}.html")
        page.wait_for_function("() => !!globalThis.dewlab")
        anchor = page.evaluate(
            """() => {
                const blocks = dewlab.proseBlocks();
                const block = blocks.find((el) => el.textContent.includes('PLAIN-PARAGRAPH'));
                const quote = 'a passage worth marking';
                const start = block.textContent.indexOf(quote);
                return {
                    block_index: blocks.indexOf(block),
                    ...dewlab.describeQuote(block, start, start + quote.length),
                };
            }"""
        )
        _seed(page, {
            "id": "h-contrast", "note": "", "created_at": "2026-01-01T00:00:00.000Z", **anchor,
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
        color = _parse_rgb(measured["color"])
        background = _parse_rgb(measured["background"])
        ratio = _contrast_ratio(color, background)
        assert measured["size"] < 24
        assert ratio >= 4.5, (
            f"{scheme}: highlight text {measured['color']} on {measured['background']} "
            f"is {ratio:.2f}:1, under the 4.5:1 AA minimum"
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
