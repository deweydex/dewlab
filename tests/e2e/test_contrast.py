"""Every text/background colour pairing the design system defines as
deliberately distinct from body prose, checked against the real WCAG AA
4.5:1 minimum in both themes -- not just the one pairing (link colour) that
happened to get checked because someone hit a real bug in it once.

Regression context: the brand orange link colour was once 3.5:1 on light
backgrounds, under the AA minimum. That's the only pairing this file used to
cover; the rest (muted text, headings, pass/fail text, per-language pills,
every highlight colour) had never been measured at all.
"""

from __future__ import annotations

import functools
import http.server
import json
import re
import socketserver
import sys
import threading
from pathlib import Path

import pytest

from conftest import PAGE
from contrast import AA_MINIMUM, contrast_ratio, parse_rgb

DEWLAB = Path(__file__).resolve().parents[2]
PYODIDE = DEWLAB / "dev" / "pyodide"
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402
from layout import write_course, write_tutorial  # noqa: E402

COURSE = "contrast-fixtures"
SLUG = "contrast"

TUTORIAL = """---
title: "Contrast"
year: "2026-2027"
version: 2026.08.30.1
---

# Contrast

Prose with [a link](https://example.org) in it.

## A Heading

An AMBER passage sits here for the default highlight colour.

A GREEN passage sits here for the green highlight colour.

A BLUE passage sits here for the blue highlight colour.

A PINK passage sits here for the pink highlight colour.

```python exec
id: contrast-python
print("hi")
```

```sql exec
id: contrast-sql
select 1;
```
"""


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, SLUG, TUTORIAL)
    write_course(tmp_path, COURSE, "Contrast Series", [SLUG])
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "COURSES", tmp_path / "courses")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
    b.build()

    # This fixture's tutorial has a python and a sql exec cell, so the page
    # always attempts a Pyodide boot even on tests that never run a cell --
    # with no local route that boot fails against the CDN and eventually
    # shows a #dl-status error overlay that can intercept clicks meant for
    # unrelated elements. Point it at the self-hosted copy instead, the same
    # way conftest.py's session-scoped fixture does.
    if PYODIDE.exists():
        (tmp_path / "site" / "pyodide").symlink_to(PYODIDE)
        page_path = tmp_path / "site" / "tutorials" / f"{SLUG}.html"
        html = page_path.read_text()
        found = re.search(
            r'<script type="module" src="\.\./assets/tutorial-runtime\.js[^"]*">'
            r"</script>",
            html,
        )
        if found:
            page_path.write_text(html.replace(
                found.group(0),
                '<script>globalThis.DEWLAB_PYODIDE_BASE = "../pyodide/";</script>\n'
                + found.group(0),
            ))
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


def _seed_highlights(page, highlights: list[dict]) -> None:
    page.evaluate(
        "([key, value]) => localStorage.setItem(key, value)",
        [
            page.evaluate("dewlab.progressKey()"),
            json.dumps({
                "tutorial-id": SLUG,
                "tutorial-version": "2026.08.30.1",
                "saved_at": "2026-01-01T00:00:00.000Z",
                "notes": "",
                "cells": [],
                "highlights": highlights,
            }),
        ],
    )


def _anchor_for(page, marker: str, quote: str) -> dict:
    return page.evaluate(
        """([marker, quote]) => {
             const blocks = dewlab.proseBlocks();
             const block = blocks.find((el) => el.textContent.includes(marker));
             const start = block.textContent.indexOf(quote);
             return {
                 block_index: blocks.indexOf(block),
                 ...dewlab.describeQuote(block, start, start + quote.length),
             };
           }""",
        [marker, quote],
    )


def _measured_color(page, selector: str) -> dict:
    return page.evaluate(
        """(sel) => {
             const el = document.querySelector(sel);
             const style = getComputedStyle(el);
             return {color: style.color, background: style.backgroundColor, size: parseFloat(style.fontSize)};
           }""",
        selector,
    )


def _page_background(page) -> str:
    return page.evaluate("getComputedStyle(document.body).backgroundColor")


def _assert_aa(scheme: str, label: str, fg: str, bg: str) -> None:
    ratio = contrast_ratio(parse_rgb(fg), parse_rgb(bg))
    assert ratio >= AA_MINIMUM, (
        f"{scheme}: {label} {fg} on {bg} is {ratio:.2f}:1, under the {AA_MINIMUM}:1 AA minimum"
    )


@pytest.mark.parametrize("scheme", ["light", "dark"])
class TestProseAndCellColours:
    """Pairings present on every build with no cell run required, plus the
    two that need one run each (check()'s pass/fail text)."""

    def test_the_link_colour(self, site_url, browser, scheme):
        page = browser.new_page(color_scheme=scheme)
        try:
            page.goto(f"{site_url}/tutorials/{SLUG}.html")
            page.wait_for_selector('a[href="https://example.org"]')
            measured = _measured_color(page, 'a[href="https://example.org"]')
            assert measured["size"] < 24
            # A link sets no background-color of its own (which doesn't
            # inherit), so its computed value is transparent -- the real
            # background it reads against is the page's.
            _assert_aa(scheme, "link", measured["color"], _page_background(page))
        finally:
            page.close()

    def test_a_heading(self, site_url, browser, scheme):
        page = browser.new_page(color_scheme=scheme)
        try:
            page.goto(f"{site_url}/tutorials/{SLUG}.html")
            page.wait_for_selector("h2")
            measured = _measured_color(page, "h2")
            _assert_aa(scheme, "heading", measured["color"], _page_background(page))
        finally:
            page.close()

    def test_the_crumbs_label(self, site_url, browser, scheme):
        """`.dl-crumbs` labels the site's own utility pages (all-tutorials,
        course, tree...), not a tutorial page -- which has no equivalent
        static label, only the dynamic where-you-are tree."""
        page = browser.new_page(color_scheme=scheme)
        try:
            page.goto(f"{site_url}/all-tutorials.html")
            page.wait_for_selector(".dl-crumbs")
            measured = _measured_color(page, ".dl-crumbs")
            _assert_aa(scheme, "crumbs label (muted text)", measured["color"], _page_background(page))
        finally:
            page.close()

    @pytest.mark.parametrize("cell_type", ["python", "sql"])
    def test_a_cell_type_pill(self, site_url, browser, scheme, cell_type):
        page = browser.new_page(color_scheme=scheme)
        try:
            page.goto(f"{site_url}/tutorials/{SLUG}.html")
            selector = f'.dl-cell-pill-type[data-type="{cell_type}"]'
            page.wait_for_selector(selector)
            measured = _measured_color(page, selector)
            background = _page_background(page)
            _assert_aa(scheme, f"{cell_type} pill", measured["color"], background)
        finally:
            page.close()

    def test_a_passing_check(self, base_url, browser, scheme):
        # Against the shared fixture tutorial, not this file's own tiny
        # one: it's the one place already set up to point Pyodide at the
        # self-hosted copy rather than a CDN this environment can't reach,
        # and it already has a cell (tools-show-check) whose check() calls
        # produce both a pass and a fail in one run.
        page = browser.new_page(color_scheme=scheme)
        try:
            page.goto(f"{base_url}/{PAGE}")
            page.wait_for_function("() => !!globalThis.dewlab")
            page.wait_for_function(
                "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
                timeout=240_000,
            )
            # tools-show-check reads `df`, defined by pandas-table -- cells
            # share one namespace built up by what has actually run, not by
            # what merely sits earlier on the page.
            page.evaluate('dewlab.runCell("pandas-table")')
            page.wait_for_function(
                "document.querySelector(\"[data-cell-id='pandas-table'] .dl-output\").children.length > 0"
            )
            page.evaluate('dewlab.runCell("tools-show-check")')
            page.wait_for_selector(".dl-check-pass")
            measured = _measured_color(page, ".dl-check-pass")
            _assert_aa(scheme, "passing check", measured["color"], measured["background"])
        finally:
            page.close()

    def test_a_failing_check(self, base_url, browser, scheme):
        page = browser.new_page(color_scheme=scheme)
        try:
            page.goto(f"{base_url}/{PAGE}")
            page.wait_for_function("() => !!globalThis.dewlab")
            page.wait_for_function(
                "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
                timeout=240_000,
            )
            page.evaluate('dewlab.runCell("pandas-table")')
            page.wait_for_function(
                "document.querySelector(\"[data-cell-id='pandas-table'] .dl-output\").children.length > 0"
            )
            page.evaluate('dewlab.runCell("tools-show-check")')
            page.wait_for_selector(".dl-check-fail")
            measured = _measured_color(page, ".dl-check-fail")
            _assert_aa(scheme, "failing check", measured["color"], measured["background"])
        finally:
            page.close()


@pytest.mark.parametrize("scheme", ["light", "dark"])
@pytest.mark.parametrize("color,marker,quote", [
    (None, "An AMBER passage", "AMBER"),
    ("green", "A GREEN passage", "GREEN"),
    ("blue", "A BLUE passage", "BLUE"),
    ("pink", "A PINK passage", "PINK"),
])
def test_a_highlight_colour(site_url, browser, scheme, color, marker, quote):
    """One highlight per colour (amber is the unset default), each on its
    own passage so their anchors never collide."""
    page = browser.new_page(color_scheme=scheme)
    try:
        page.goto(f"{site_url}/tutorials/{SLUG}.html")
        page.wait_for_function("() => !!globalThis.dewlab")
        anchor = _anchor_for(page, marker, quote)
        highlight = {"id": f"h-{color or 'amber'}", "note": "",
                     "created_at": "2026-01-01T00:00:00.000Z", **anchor}
        if color:
            highlight["color"] = color
        _seed_highlights(page, [highlight])
        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")

        mark_selector = f'mark.dl-highlight[data-highlight-id="h-{color or "amber"}"]'
        page.wait_for_selector(mark_selector)
        measured = _measured_color(page, mark_selector)
        assert measured["size"] < 24
        _assert_aa(scheme, f"{color or 'amber'} highlight", measured["color"], measured["background"])
    finally:
        page.close()
