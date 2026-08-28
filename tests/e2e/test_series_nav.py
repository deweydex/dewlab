"""The series navigation panel, in a real browser — planning/SIDEBAR_CONTENT.md §4b.

A dedicated, tiny site build rather than the shared rendering-tour fixture:
this needs its own series order, and no self-hosted Pyodide — every fixture
tutorial here is prose-only, and tutorial-runtime.js's own boot() skips
loading Pyodide entirely when a page has no cells
(CONTENT_AND_FILE_ARCHITECTURE.md) — so unlike most of this directory, this
file runs without `python3 dev/fetch_pyodide.py` first.

    python3 -m pytest tests/e2e/test_series_nav.py -q
"""

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

MODULE = "seriesnav-fixtures"

FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: seriesnav-fixtures
module_title: "Series Nav Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# {title}

Some prose. Nothing here is a cell, on purpose — this file's own fixtures
never boot Pyodide.
"""

def _tutorial(root: Path, slug: str, title: str = "A Title") -> None:
    path = root / "tutorials" / MODULE / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FRONTMATTER.format(title=title, slug=slug))


def _archive(root: Path, slug: str) -> None:
    """Take a tutorial out of the reading order without deleting it — the
    one way a tutorial ends up with nowhere in a series to sit."""
    path = root / "tutorials" / MODULE / f"{slug}.md"
    path.write_text(path.read_text().replace(
        "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: archived\n"))


def _set_order(root: Path, slugs: list[str]) -> None:
    path = root / "tutorials" / MODULE / "sample-series.order.yaml"
    path.write_text("series: Sample Series\norder:\n" + "".join(f"  - {s}\n" for s in slugs))


@pytest.fixture()
def site(tmp_path, monkeypatch):
    """A real build, real assets, isolated content — ROOT/TUTORIALS/OUT move
    to tmp_path; ASSETS/SHELL/SETUP/DATA stay pointed at the real repository,
    read-only, so the page that loads is running the actual runtime and CSS
    rather than a stand-in for them."""
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
def base_url(site):
    server, thread, url = _serve(site / "site")
    try:
        yield url
    finally:
        server.shutdown()
        thread.join(timeout=5)


class TestVisibility:
    def test_a_tutorial_outside_any_series_hides_the_toggle(self, site, browser, base_url):
        _tutorial(site, "solo", "Solo")
        _tutorial(site, "other", "Other")
        _set_order(site, ["other"])
        _archive(site, "solo")
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/solo.html")
        assert page.is_hidden("#dl-seriesnav-toggle")
        context.close()

    def test_a_tutorial_in_a_series_shows_the_toggle(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_visible("#dl-seriesnav-toggle")
        context.close()


class TestOpeningAndClosing:
    def open_page(self, site, browser, base_url, slug="two"):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _tutorial(site, "three", "Three")
        _set_order(site, ["one", "two", "three"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/{slug}.html")
        return context, page

    def test_the_panel_is_closed_by_default(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        assert page.is_hidden("#dl-seriesnav")
        context.close()

    def test_clicking_the_toggle_opens_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        context.close()

    def test_escape_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-seriesnav-toggle")
        page.keyboard.press("Escape")
        assert page.is_hidden("#dl-seriesnav")
        context.close()

    def test_the_close_button_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-seriesnav-toggle")
        page.click("#dl-seriesnav-close")
        assert page.is_hidden("#dl-seriesnav")
        context.close()

    def test_clicking_outside_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-seriesnav-toggle")
        page.click("main#dl-body")
        assert page.is_hidden("#dl-seriesnav")
        context.close()

    def test_opening_the_series_nav_closes_settings(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        page.click("#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        assert page.is_hidden("#dl-settings")
        context.close()

    def test_opening_settings_closes_the_series_nav(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        page.click("#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        page.click("#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        assert page.is_hidden("#dl-seriesnav")
        context.close()


class TestMutualExclusionWithCheatSheet:
    """The cheat sheet, settings, and series nav are a three-way mutual
    exclusion group sharing the same left-anchored corner (PR #65 moved
    the cheat sheet there; the series nav panel joined it)."""

    def test_opening_the_series_nav_closes_the_cheat_sheet(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        (site / "tutorials" / MODULE / "one.glossary.yaml").write_text(
            "entries:\n  - term: x\n    kind: concept\n    definition: The first thing.\n"
        )
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-cheatsheet-toggle")
        assert page.is_visible("#dl-cheatsheet")
        page.click("#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        assert page.is_hidden("#dl-cheatsheet")
        context.close()

    def test_opening_the_cheat_sheet_closes_the_series_nav(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        (site / "tutorials" / MODULE / "one.glossary.yaml").write_text(
            "entries:\n  - term: x\n    kind: concept\n    definition: The first thing.\n"
        )
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        page.click("#dl-cheatsheet-toggle")
        assert page.is_visible("#dl-cheatsheet")
        assert page.is_hidden("#dl-seriesnav")
        context.close()


class TestContent:
    def test_it_lists_every_tutorial_in_the_series_in_order(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _tutorial(site, "three", "Three")
        _set_order(site, ["one", "two", "three"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/two.html")
        page.click("#dl-seriesnav-toggle")
        items = page.eval_on_selector_all(
            "#dl-seriesnav .dl-seriesnav-series li", "els => els.map(e => e.textContent)")
        assert items == ["1. One", "2. Two", "3. Three"]
        context.close()

    def test_the_current_tutorial_is_marked_and_not_a_link(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/two.html")
        page.click("#dl-seriesnav-toggle")
        current = page.query_selector("#dl-seriesnav .dl-seriesnav-current")
        assert current is not None
        assert "Two" in current.inner_text()
        assert current.query_selector("a") is None
        context.close()

    def test_other_tutorials_are_links_that_navigate(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/two.html")
        page.click("#dl-seriesnav-toggle")
        page.click("#dl-seriesnav .dl-seriesnav-series li a")
        page.wait_for_url(f"{base_url}/tutorials/{MODULE}/one.html")
        context.close()


class TestMobile:
    def test_the_toggle_is_visible_on_a_phone_sized_viewport(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_visible("#dl-seriesnav-toggle")
        context.close()

    def test_opening_it_shows_a_sheet_anchored_to_the_bottom_edge(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        page.click("#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        style = page.eval_on_selector(
            "#dl-seriesnav",
            "el => { const s = getComputedStyle(el); "
            "return { position: s.position, bottom: s.bottom, left: s.left, right: s.right }; }",
        )
        assert style["position"] == "fixed"
        assert style["bottom"] == "0px"
        assert style["left"] == "0px"
        assert style["right"] == "0px"
        context.close()
