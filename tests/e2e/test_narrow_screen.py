"""A tutorial on a phone — planning/ROADMAP.md Phase 6's edges audit.

The rule this file protects: **the page body must never scroll
horizontally.** A reader on a 375px screen who has to drag the page sideways
to finish a sentence is reading a broken page, and the two things that
caused it were both invisible on a desktop — a URL in a bibliography and a
URL inside an error message, neither of which has a space to wrap at.

Like tests/e2e/test_reference.py, this builds its own tiny prose-only site
and needs no self-hosted Pyodide: a page with no cells never boots one.

    python3 -m pytest tests/e2e/test_narrow_screen.py -q
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

MODULE = "narrow-fixtures"

# The smallest screen a student is realistically carrying.
PHONE = {"width": 375, "height": 667}

# A bibliography entry with a real DOI in it — the shape every tutorial's
# "Where to Read More" section ends with, and the one that pushed the page
# sideways before `#dl-body { overflow-wrap: break-word }`.
TUTORIAL = """---
title: "Narrow"
slug: narrow
module: narrow-fixtures
module_title: "Narrow Fixtures"
year: "2026-2027"
series: narrow-series
version: 2026.08.30.1
---

# Narrow

Some prose, with a reference after it.

## Where to Read More

Metropolis, N. and Ulam, S. (1949). *The Monte Carlo Method.* Journal of the
American Statistical Association, 44(247), 335-341.
<https://doi.org/10.1080/01621459.1949.10483310>. A long identifier with no
space anywhere in it, which is the whole point of this fixture.
"""


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


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture()
def base_url(site):
    handler = functools.partial(_QuietHandler, directory=str(site / "site"))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def _build(site: Path) -> None:
    (site / "tutorials" / MODULE / "narrow.md").write_text(TUTORIAL)
    (site / "tutorials" / MODULE / "narrow-series.order.yaml").write_text(
        "series: Narrow Series\norder:\n  - narrow\n")
    b.build()


def _phone(browser):
    return browser.new_context(viewport=PHONE, is_mobile=True, has_touch=True)


class TestNothingScrollsSideways:
    def test_a_tutorial_fits_the_screen(self, site, browser, base_url):
        """A bibliography URL is the usual culprit: no spaces, so nothing to
        wrap at unless the prose is told it may break inside a word."""
        _build(site)
        context = _phone(browser)
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/narrow.html")
        page.wait_for_selector("#dl-body")
        widths = page.evaluate("""() => ({
          scroll: document.documentElement.scrollWidth,
          client: document.documentElement.clientWidth,
        })""")
        assert widths["scroll"] <= widths["client"] + 1, (
            f"page scrolls sideways: {widths['scroll']} > {widths['client']}")
        context.close()

    def test_the_contents_page_fits_the_screen(self, site, browser, base_url):
        _build(site)
        context = _phone(browser)
        page = context.new_page()
        page.goto(f"{base_url}/index.html")
        widths = page.evaluate("""() => ({
          scroll: document.documentElement.scrollWidth,
          client: document.documentElement.clientWidth,
        })""")
        assert widths["scroll"] <= widths["client"] + 1
        context.close()

    def test_a_failure_message_wraps_instead_of_widening_the_page(
            self, site, browser, base_url):
        """The compounding failure this exists to prevent: a reader on a poor
        connection gets an error whose text carries the URL that failed, and
        the message itself then makes the page unreadable. One problem should
        not become two.
        """
        _build(site)
        context = _phone(browser)
        page = context.new_page()
        page.goto(f"{base_url}/tutorials/{MODULE}/narrow.html")
        page.wait_for_selector("#dl-body")
        # The real #dl-status from shell.html, not a stand-in appended into
        # the reading. It is a *sibling* of #dl-body, so it does not inherit
        # that element's own wrapping — filling a copy inside #dl-body would
        # test the wrong rule and pass whatever .dl-status does.
        overflow = page.evaluate("""() => {
          const status = document.getElementById('dl-status');
          status.classList.add('dl-status-error');
          status.hidden = false;
          status.textContent = 'Python failed to start: Failed to fetch '
            + 'dynamically imported module: '
            + 'https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.mjs. '
            + 'Reloading the page usually fixes it.';
          return {inBody: document.getElementById('dl-body').contains(status),
                  sw: status.scrollWidth, cw: status.clientWidth,
                  page: document.documentElement.scrollWidth,
                  client: document.documentElement.clientWidth};
        }""")
        assert overflow["inBody"] is False, (
            "this test only means anything while #dl-status sits outside #dl-body")
        assert overflow["sw"] <= overflow["cw"] + 1, "the error message itself overflows"
        assert overflow["page"] <= overflow["client"] + 1, "the error widened the page"
        context.close()
