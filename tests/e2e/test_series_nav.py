"""planning/SIDEBAR_CONTENT.md §4b. Every fixture here is prose-only, so
tutorial-runtime.js never boots Pyodide for these pages — unlike most of
tests/e2e/, this file runs without `python3 dev/fetch_pyodide.py` first."""

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
    """The one way a tutorial ends up with nowhere in a series to sit."""
    path = root / "tutorials" / MODULE / f"{slug}.md"
    path.write_text(path.read_text().replace(
        "version: 2026.08.23.1\n", "version: 2026.08.23.1\nstatus: archived\n"))


def _set_order(root: Path, slugs: list[str]) -> None:
    path = root / "tutorials" / MODULE / "sample-series.order.yaml"
    path.write_text("series: Sample Series\norder:\n" + "".join(f"  - {s}\n" for s in slugs))


@pytest.fixture()
def site(tmp_path, monkeypatch):
    """Only ROOT/TUTORIALS/OUT move to tmp_path; ASSETS/SHELL/SETUP/DATA stay
    pointed at the real repo, so the page runs the actual runtime and CSS."""
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


def _open_panel(actor, selector: str) -> None:
    """Reference/Series/Settings' toggles now collapse behind one
    "Panels" control in the masthead (shell.html's
    <details class="dl-panels">) rather than always showing — expand it
    first if it isn't already, then click the actual target. Checked via
    #dl-panels' own `open` property rather than the target's own
    visibility, so this never mistakes "already open" for "not open" and
    toggles it shut again right before the click that was supposed to
    land. Left expanded once opened (no auto-collapse), so this is only
    needed once per page load, not before every toggle click."""
    if not actor.eval_on_selector("#dl-panels", "el => el.open"):
        actor.click("#dl-panels summary")
    actor.click(selector)


def _toggle_shows(actor, selector: str) -> bool:
    """Whether a masthead toggle has content to show, via its own
    `hidden` attribute (tutorial-runtime.js's own content-presence
    signal) rather than Playwright's is_visible()/is_hidden() — those now
    also depend on whether "Panels" happens to be expanded, which is a
    question about the masthead's own UI state, not this page's
    content."""
    return actor.get_attribute(selector, "hidden") is None


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
        assert not _toggle_shows(page, "#dl-seriesnav-toggle")
        context.close()

    def test_a_tutorial_in_a_series_shows_the_toggle(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert _toggle_shows(page, "#dl-seriesnav-toggle")
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
        _open_panel(page, "#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        context.close()

    def test_escape_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-seriesnav-toggle")
        page.keyboard.press("Escape")
        assert page.is_hidden("#dl-seriesnav")
        context.close()

    def test_the_close_button_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-seriesnav-toggle")
        page.click("#dl-seriesnav-close")
        assert page.is_hidden("#dl-seriesnav")
        context.close()

    def test_clicking_outside_closes_it(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-seriesnav-toggle")
        page.click("main#dl-body")
        assert page.is_hidden("#dl-seriesnav")
        context.close()

    def test_opening_the_series_nav_does_not_close_settings(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        _open_panel(page, "#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        assert page.is_visible("#dl-settings")
        context.close()

    def test_opening_settings_does_not_close_the_series_nav(self, site, browser, base_url):
        context, page = self.open_page(site, browser, base_url)
        _open_panel(page, "#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        _open_panel(page, "#dl-settings-toggle")
        assert page.is_visible("#dl-settings")
        assert page.is_visible("#dl-seriesnav")
        context.close()


class TestMutualExclusionWithReference:
    """The reference and series nav are the one pair that still conflicts —
    they share the same left-anchored corner. Settings anchors to the right
    and no longer force-closes (or gets force-closed by) either one."""

    def test_opening_the_series_nav_closes_the_reference(self, site, browser, base_url):
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
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
        _open_panel(page, "#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        assert page.is_hidden("#dl-reference")
        context.close()

    def test_opening_the_reference_closes_the_series_nav(self, site, browser, base_url):
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
        _open_panel(page, "#dl-seriesnav-toggle")
        assert page.is_visible("#dl-seriesnav")
        _open_panel(page, "#dl-reference-toggle")
        assert page.is_visible("#dl-reference")
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
        _open_panel(page, "#dl-seriesnav-toggle")
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
        _open_panel(page, "#dl-seriesnav-toggle")
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
        _open_panel(page, "#dl-seriesnav-toggle")
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
        assert _toggle_shows(page, "#dl-seriesnav-toggle")
        context.close()

    def test_opening_it_shows_a_sheet_anchored_to_the_bottom_edge(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _tutorial(site, "two", "Two")
        _set_order(site, ["one", "two"])
        b.build()
        context = browser.new_context(viewport={"width": 375, "height": 700})
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-seriesnav-toggle")
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
