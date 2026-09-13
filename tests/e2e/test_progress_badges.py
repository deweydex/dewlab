"""Progress is seeded directly into localStorage rather than by running a cell, since what the badge reads is the saved record, not a live interpreter."""

from __future__ import annotations

import functools
import http.server
import json
import socketserver
import sys
import threading
from pathlib import Path

import pytest

from conftest import _open_panel

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402

MODULE = "progress-fixtures"

FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: progress-fixtures
module_title: "Progress Fixtures"
year: "2026-2027"
series: sample-series
version: 2026.08.23.1
---

# {title}

```python exec
id: {slug}-1
print("hello")
```

```python exec
id: {slug}-2
print("world")
```
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
def site_url(site):
    server, thread, url = _serve(site / "site")
    try:
        yield url
    finally:
        server.shutdown()
        thread.join(timeout=5)


def _seed(page, module: str, slug: str, cells: list[dict]) -> None:
    """A saved-progress record written straight into localStorage, as saveNow() would, without a cell run."""
    record = {
        "tutorial-slug": slug,
        "tutorial-module": module,
        "tutorial-version": "2026.08.23.1",
        "saved_at": "2026-08-28T00:00:00.000Z",
        "cells": cells,
    }
    page.evaluate(
        "([key, value]) => localStorage.setItem(key, value)",
        [f"dewlab:progress:{module}:{slug}", json.dumps(record)],
    )


class TestProgressBadges:
    def test_a_tutorial_with_no_saved_record_shows_no_badge(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/all-tutorials.html")
        assert page.is_hidden(".dl-progress-badge")
        context.close()

    def test_a_saved_record_with_nothing_run_shows_no_badge(self, site, browser, site_url):
        """A cell only edited, never run, has no output_html, so an empty one here must count as untouched."""
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/all-tutorials.html")
        _seed(page, MODULE, "one", [
            {"task_id": "one-1", "student_code": "x = 1", "output_html": "", "errored": False},
        ])
        page.reload()
        assert page.is_hidden(".dl-progress-badge")
        context.close()

    def test_a_run_cell_shows_a_fraction_badge(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/all-tutorials.html")
        _seed(page, MODULE, "one", [
            {"task_id": "one-1", "student_code": "", "output_html": "<pre>hello</pre>", "errored": False},
            {"task_id": "one-2", "student_code": "", "output_html": "", "errored": False},
        ])
        page.reload()
        badge = page.locator(".dl-progress-badge")
        assert badge.inner_text() == "1/2"
        assert "dl-progress-badge-errored" not in (badge.get_attribute("class") or "")
        context.close()

    def test_an_errored_cell_gives_the_badge_the_error_colour(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/all-tutorials.html")
        _seed(page, MODULE, "one", [
            {"task_id": "one-1", "student_code": "", "output_html": "<pre>hello</pre>", "errored": False},
            {"task_id": "one-2", "student_code": "", "output_html": '<pre class="dl-error">boom</pre>', "errored": True},
        ])
        page.reload()
        badge = page.locator(".dl-progress-badge")
        assert badge.inner_text() == "2/2"
        assert "dl-progress-badge-errored" in badge.get_attribute("class")
        context.close()

    def test_the_settings_toggle_hides_and_restores_badges(self, site, browser, site_url):
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"{site_url}/all-tutorials.html")
        _seed(page, MODULE, "one", [
            {"task_id": "one-1", "student_code": "", "output_html": "<pre>hello</pre>", "errored": False},
        ])
        page.reload()
        assert page.is_visible(".dl-progress-badge")

        _open_panel(page, "#dl-settings-toggle")
        page.click('[data-progress-badges] button[data-value="off"]')
        page.click("#dl-settings-close")
        assert page.is_hidden(".dl-progress-badge")

        # And it holds across a reload — a real setting, not a one-off toggle.
        page.reload()
        assert page.is_hidden(".dl-progress-badge")

        _open_panel(page, "#dl-settings-toggle")
        page.click('[data-progress-badges] button[data-value="on"]')
        page.click("#dl-settings-close")
        assert page.is_visible(".dl-progress-badge")
        context.close()
