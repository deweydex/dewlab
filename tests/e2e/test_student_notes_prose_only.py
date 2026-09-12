"""Regression check: the "Your work" section used to be removed entirely whenever cells.length === 0, which also hid notes on a prose-only tutorial."""

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

MODULE = "notes-fixtures"

FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: notes-fixtures
module_title: "Notes Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# {title}

Some prose. Nothing here is a cell, on purpose.
"""


def _tutorial(root: Path, slug: str, title: str = "A Title") -> None:
    path = root / "tutorials" / MODULE / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(FRONTMATTER.format(title=title, slug=slug))


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


class TestNotesOnAProseOnlyTutorial:
    def test_the_work_section_and_notes_field_are_not_removed(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        assert page.is_hidden("#dl-settings")
        _open_panel(page, "#dl-settings-toggle")
        assert page.is_visible("#dl-settings-work")
        assert page.is_visible("#dl-progress-notes")
        context.close()

    def test_a_note_still_autosaves_with_zero_cells(self, site, browser, base_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/one.html")
        _open_panel(page, "#dl-settings-toggle")
        page.fill("#dl-progress-notes", "worth writing down")
        page.wait_for_function(
            "globalThis.dewlab.readSaved() !== null", timeout=10_000
        )
        saved = page.evaluate("globalThis.dewlab.readSaved()")
        assert saved["notes"] == "worth writing down"
        assert saved["cells"] == []
        context.close()

    def test_the_contents_page_itself_gets_no_notes_field(self, site, browser, base_url):
        """index/tree/about are not tutorials — NON_TUTORIAL_PAGES."""
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{base_url}/index.html")
        _open_panel(page, "#dl-settings-toggle")
        assert page.is_hidden("#dl-settings-work")
        context.close()
