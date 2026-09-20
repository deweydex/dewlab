"""One contract, wired by hand at seven separate places in
tutorial-runtime.js: a panel opens from a toggle, and Escape closes it
again everywhere. Four of the seven sites share one implementation
(initRightPanels()'s loop over Your Work / Python / Settings / Give
Feedback) and are parametrized here as one case each rather than one test
each.

Not every site implements every facet -- this file asserts what each one
actually does, not what a tidier design would have it do. Outside-click no
longer closes Your Work/Python/Settings/Give Feedback or Reference
(DECISIONS_LOG 7.99/7.199: "a docked rail must not close on an outside
click, unlike a popover" -- the tutorial pages' panels used to be the
exception, on purpose, until Josh found it closing a panel he'd left open
on the other dock); it still does for the mobile launcher menu, the
highlight popover, the cell run menu, and the versions toggle, none of
which are part of that dock system. Those same five docked panels close
instead by clicking their own toggle again, now that Reference's close
button is gone too (7.190/7.201's "no repeated title, no close button"
cleanup, applied to all five in the end). Returning focus to the opener on
Escape is only wired for Reference, the mobile launcher menu, the cell run
menu, and the versions toggle; Your Work/Python/Settings/Give Feedback,
the mobile "where you are" sheet, and the highlight popover close without
moving focus anywhere."""

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

DEWLAB = Path(__file__).resolve().parents[2]
PYODIDE = DEWLAB / "dev" / "pyodide"
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402
from layout import write_course, write_tutorial  # noqa: E402

COURSE = "dismiss-fixtures"
SLUG = "one"
PHONE = {"width": 375, "height": 700}

TUTORIAL = """---
title: "One"
year: "2026-2027"
version: 2026.08.23.1
---

# One

A passage worth marking sits right here for the highlight popover.

```python exec
id: one-1
print("hello")
```
"""


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, SLUG, TUTORIAL)
    write_course(tmp_path, COURSE, "Sample Series", [SLUG])
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "COURSES", tmp_path / "courses")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
    b.build()

    # This fixture's page has a python exec cell (for the cell-run-menu
    # case), so tutorial-runtime.js always tries to boot Pyodide -- even
    # though no test here waits on it. Left pointed at the real CDN, that
    # attempt fails in an environment with no route there, and the
    # resulting "Python failed to start" status message can visually
    # overlap and intercept clicks meant for something else entirely.
    # Symlinking in the same self-hosted copy conftest.py's own session
    # fixture uses, and rewriting the page the same way, makes the boot
    # attempt succeed quickly and quietly instead.
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


def _goto(page, site_url):
    page.goto(f"{site_url}/tutorials/{SLUG}.html")
    page.wait_for_function("() => !!globalThis.dewlab")
    # Deliberately not waiting for Pyodide here (unlike most e2e fixtures):
    # this file is chrome mechanics, not execution, and every one of its
    # ten cases -- including the run menu's own "..." button, wired at
    # DOMContentLoaded independent of Pyodide's async boot -- works before
    # Python is ready. This fixture also has no route to the self-hosted
    # Pyodide the shared `page` fixture sets up, so waiting on it here
    # would just hang.


def _open_generic_panel(page, name: str) -> None:
    page.click(f"#dl-{name}-toggle")
    page.wait_for_selector(f"#dl-{name}:not([hidden])")


def _open_reference(page) -> None:
    page.click("#dl-reference-toggle")
    page.wait_for_selector("#dl-reference:not([hidden])")


def _open_versions(page) -> None:
    page.click("#dl-versions-toggle")
    page.wait_for_selector("#dl-versions-list:not([hidden])")


def _open_run_menu(page) -> None:
    page.click(".dl-cell[data-cell-id='one-1'] .dl-btn-more")
    page.wait_for_selector(".dl-cell[data-cell-id='one-1'] .dl-cell-run-menu:not([hidden])")


def _open_mobile_menu(page) -> None:
    page.click("#dl-mobile-fab")
    page.wait_for_selector("#dl-mobile-menu:not([hidden])")


def _open_whereyouare(page) -> None:
    page.click("#dl-mobile-fab")
    page.wait_for_selector("#dl-mobile-item-whereyouare")
    page.click("#dl-mobile-item-whereyouare")
    page.wait_for_selector("#dl-whereyouare:not([hidden])")


def _seed_highlight(page) -> None:
    anchor = page.evaluate(
        """() => {
             const blocks = dewlab.proseBlocks();
             const block = blocks.find((el) => el.textContent.includes('passage worth marking'));
             const quote = 'passage worth marking';
             const start = block.textContent.indexOf(quote);
             return {
                 block_index: blocks.indexOf(block),
                 ...dewlab.describeQuote(block, start, start + quote.length),
             };
           }"""
    )
    page.evaluate(
        "([key, value]) => localStorage.setItem(key, value)",
        [
            page.evaluate("dewlab.progressKey()"),
            json.dumps({
                "tutorial-id": SLUG, "tutorial-version": "2026.08.23.1",
                "saved_at": "2026-01-01T00:00:00.000Z", "notes": "", "cells": [],
                "highlights": [{"id": "h-1", "note": "", "created_at": "2026-01-01T00:00:00.000Z", **anchor}],
            }),
        ],
    )
    page.reload()
    page.wait_for_function("() => !!globalThis.dewlab")


def _open_highlight_popover(page) -> None:
    _seed_highlight(page)
    page.click('mark.dl-highlight[data-highlight-id="h-1"]')
    page.wait_for_selector(".dl-highlight-popover:not([hidden])")


# Each case: (viewport, open(page), target selector, opener selector to
# check focus-return against (None if the source never returns focus),
# close-button selector (None if there isn't one), URL to open (None =
# this file's own single-release fixture), whether an outside click
# closes it, the toggle selector to re-click if doing so closes it again
# (None if it doesn't).
CASES = [
    pytest.param(PHONE, _open_whereyouare, "#dl-whereyouare",
                 None, "#dl-whereyouare-close", None, True, None, id="whereyouare"),
    pytest.param(None, functools.partial(_open_generic_panel, name="yourwork"), "#dl-yourwork",
                 None, None, None, False, "#dl-yourwork-toggle", id="yourwork"),
    pytest.param(None, functools.partial(_open_generic_panel, name="python"), "#dl-python",
                 None, None, None, False, "#dl-python-toggle", id="python"),
    pytest.param(None, functools.partial(_open_generic_panel, name="settings"), "#dl-settings",
                 None, None, None, False, "#dl-settings-toggle", id="settings"),
    pytest.param(None, functools.partial(_open_generic_panel, name="report"), "#dl-report",
                 None, None, None, False, "#dl-report-toggle", id="report"),
    pytest.param(PHONE, _open_mobile_menu, "#dl-mobile-menu",
                 "#dl-mobile-fab", None, None, True, None, id="mobile-menu"),
    pytest.param(None, _open_reference, "#dl-reference",
                 "#dl-reference-toggle", None, None, False, "#dl-reference-toggle", id="reference"),
    pytest.param(None, _open_highlight_popover, ".dl-highlight-popover",
                 None, None, None, True, None, id="highlight-popover"),
    pytest.param(None, _open_run_menu, ".dl-cell[data-cell-id='one-1'] .dl-cell-run-menu",
                 ".dl-cell[data-cell-id='one-1'] .dl-btn-more", None, None, True, None, id="cell-run-menu"),
    # The versions toggle only exists on a tutorial with more than one
    # release, which this file's own fixture isn't -- reuses the shared
    # e2e fixture's own multi-release tutorial instead.
    pytest.param(None, _open_versions, "#dl-versions-list",
                 "#dl-versions-toggle", None, "two-takes", True, None, id="versions-toggle"),
]


def _open_context(browser, site_url, base_url, viewport, opener, target, remote_slug):
    kwargs = {"viewport": viewport, "is_mobile": True, "has_touch": True} if viewport else {}
    context = browser.new_context(**kwargs)
    page = context.new_page()
    if remote_slug:
        page.goto(f"{base_url}/tutorials/{remote_slug}.html")
        page.wait_for_function("() => !!globalThis.dewlab")
    else:
        _goto(page, site_url)
    opener(page)
    assert page.is_visible(target), f"{target} did not open"
    return context, page


@pytest.mark.parametrize(
    "viewport,opener,target,focus_target,close_button,remote_slug,outside_closes,reopen_toggle",
    CASES,
)
class TestDismissiblePanels:
    def test_escape_closes_it(self, browser, site_url, base_url, viewport, opener, target, focus_target, close_button, remote_slug, outside_closes, reopen_toggle):
        context, page = _open_context(browser, site_url, base_url, viewport, opener, target, remote_slug)
        page.keyboard.press("Escape")
        assert page.is_hidden(target), f"{target}: Escape did not close it"
        if focus_target:
            assert page.evaluate(
                "(sel) => document.activeElement === document.querySelector(sel)", focus_target
            ), f"{target}: Escape did not return focus to {focus_target}"
        context.close()

    def test_an_outside_click(self, browser, site_url, base_url, viewport, opener, target, focus_target, close_button, remote_slug, outside_closes, reopen_toggle):
        context, page = _open_context(browser, site_url, base_url, viewport, opener, target, remote_slug)
        page.click("h1")
        if outside_closes:
            assert page.is_hidden(target), f"{target}: an outside click did not close it"
        else:
            assert page.is_visible(target), (
                f"{target}: an outside click closed it, but this is a docked panel -- "
                "DECISIONS_LOG 7.99/7.199 says a docked rail must not close on an outside click"
            )
        context.close()

    def test_its_own_close_button_closes_it(self, browser, site_url, base_url, viewport, opener, target, focus_target, close_button, remote_slug, outside_closes, reopen_toggle):
        if not close_button:
            pytest.skip(f"{target} has no close button of its own")
        context, page = _open_context(browser, site_url, base_url, viewport, opener, target, remote_slug)
        page.click(close_button)
        assert page.is_hidden(target), f"{target}: its close button did not close it"
        if focus_target:
            assert page.evaluate(
                "(sel) => document.activeElement === document.querySelector(sel)", focus_target
            ), f"{target}: its close button did not return focus to {focus_target}"
        context.close()

    def test_clicking_the_opener_again_closes_it(self, browser, site_url, base_url, viewport, opener, target, focus_target, close_button, remote_slug, outside_closes, reopen_toggle):
        if not reopen_toggle:
            pytest.skip(f"{target} does not close by re-clicking its opener")
        context, page = _open_context(browser, site_url, base_url, viewport, opener, target, remote_slug)
        page.click(reopen_toggle)
        assert page.is_hidden(target), f"{target}: clicking the opener again did not close it"
        context.close()
