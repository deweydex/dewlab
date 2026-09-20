"""makeEdgeResizable() (assets/tutorial-runtime.js): dragging a panel's own
edge resize handle. The panel's own width, and the reading column beside
it, already tracked the drag live via a ResizeObserver -- what didn't was
the corner-dock tab stack sitting above the panel (and, on the right,
the other two panels sharing its width): that only caught up once on
release, so mid-drag the tabs sat frozen at their old width while
everything below them was already a different size. Josh: "I think there
is some odd drag behavior on the right panel where only the bottom part
moves and not the tabs themselves." These tests hold the drag open (mouse
down, moved, not yet released) and check the stack's width matches the
panel's right then, not only after mouse up.

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

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402
from layout import write_course, write_tutorial  # noqa: E402

COURSE = "panel-resize-fixtures"

FRONTMATTER = """---
title: "One"
year: "2026-2027"
version: 2026.08.23.1
---

# One

Some prose. Nothing here is a cell, on purpose.
"""


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, "one", FRONTMATTER)
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
    context = browser.new_context(viewport={"width": 1400, "height": 900})
    dl_page = context.new_page()
    dl_page.goto(f"{site_url}/tutorials/one.html")
    dl_page.wait_for_function("() => !!globalThis.dewlab")
    yield dl_page
    context.close()


def _widths(page, panel_selector: str, stack_selector: str):
    panel_w = page.eval_on_selector(panel_selector, "el => el.getBoundingClientRect().width")
    stack_w = page.eval_on_selector(stack_selector, "el => el.getBoundingClientRect().width")
    return panel_w, stack_w


def _drag_without_releasing(page, handle_selector: str, dx: int):
    handle = page.locator(handle_selector)
    box = handle.bounding_box()
    start_x = box["x"] + box["width"] / 2
    start_y = box["y"] + box["height"] / 2
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    # Several intermediate moves, the way a real drag arrives in several
    # pointermove events rather than one -- if the stack only followed the
    # last one, that would still look "live" in a single-step test.
    steps = 4
    for i in range(1, steps + 1):
        page.mouse.move(start_x + dx * i / steps, start_y)


# A resize handle is no longer a child of the panel it resizes (the panel
# clips its own overflow, which is exactly the bug this file also covers)
# -- every one lives under <body> as a sibling, told apart by which panel
# it belongs to (makeEdgeResizable()'s own data-for).
def _handle(panel_id: str) -> str:
    return f'.dl-panel-resize-handle[data-for="{panel_id}"]'


class TestTheRightDock:
    def test_the_tab_stack_widens_with_the_panel_mid_drag(self, page):
        page.click("#dl-settings-toggle")
        page.wait_for_selector("#dl-settings:not([hidden])")

        before_panel, before_stack = _widths(
            page, "#dl-settings", ".dl-corner-dock-tr .dl-corner-stack"
        )
        # Wider on the left in screen terms means narrower panel width for
        # a right-docked handle (dragging left grows a right-edge panel).
        _drag_without_releasing(page, _handle("dl-settings"), -120)
        during_panel, during_stack = _widths(
            page, "#dl-settings", ".dl-corner-dock-tr .dl-corner-stack"
        )
        page.mouse.up()

        assert during_panel > before_panel + 50
        # The bug: before this fix, during_stack stayed equal to
        # before_stack until mouse up.
        assert during_stack > before_stack + 50
        assert abs(during_stack - during_panel) < 2

    def test_the_other_two_panels_share_the_width_mid_drag(self, page):
        page.click("#dl-settings-toggle")
        page.wait_for_selector("#dl-settings:not([hidden])")
        _drag_without_releasing(page, _handle("dl-settings"), -120)
        settings_style = page.eval_on_selector("#dl-settings", "el => el.style.width")
        notes_style = page.eval_on_selector("#dl-yourwork", "el => el.style.width")
        python_style = page.eval_on_selector("#dl-python", "el => el.style.width")
        page.mouse.up()

        assert notes_style == settings_style
        assert python_style == settings_style

    def test_the_handle_reaches_all_the_way_up_past_the_tab_stack(self, page):
        """Josh: "the 'drag highlight' doesn't go all the way up" -- the
        handle used to be a child of the panel, whose own top sits below
        the corner dock (trackCornerDockHeights()), so its highlight and
        its actually-grabbable area both stopped right where the dock's
        tabs began. Detached and fixed to the viewport now, it should
        reach y=0, well above the dock, not merely up to the panel."""
        page.click("#dl-settings-toggle")
        page.wait_for_selector("#dl-settings:not([hidden])")
        handle_top = page.eval_on_selector(
            _handle("dl-settings"), "el => el.getBoundingClientRect().top"
        )
        dock_top = page.eval_on_selector(
            ".dl-corner-dock-tr", "el => el.getBoundingClientRect().top"
        )
        assert handle_top <= dock_top


class TestTheLeftDock:
    def test_the_tab_stack_widens_with_the_panel_mid_drag(self, page):
        page.click("#dl-reference-toggle")
        page.wait_for_selector("#dl-reference:not([hidden])")

        before_panel, before_stack = _widths(
            page, "#dl-reference", ".dl-corner-dock-tl .dl-corner-stack"
        )
        # A left-docked handle grows the panel by dragging right.
        _drag_without_releasing(page, _handle("dl-reference"), 120)
        during_panel, during_stack = _widths(
            page, "#dl-reference", ".dl-corner-dock-tl .dl-corner-stack"
        )
        page.mouse.up()

        assert during_panel > before_panel + 50
        assert during_stack > before_stack + 50
        assert abs(during_stack - during_panel) < 2

    def test_the_handle_reaches_all_the_way_up_past_the_tab_stack(self, page):
        page.click("#dl-reference-toggle")
        page.wait_for_selector("#dl-reference:not([hidden])")
        handle_top = page.eval_on_selector(
            _handle("dl-reference"), "el => el.getBoundingClientRect().top"
        )
        dock_top = page.eval_on_selector(
            ".dl-corner-dock-tl", "el => el.getBoundingClientRect().top"
        )
        assert handle_top <= dock_top

    def test_the_handle_tracks_the_panel_horizontally_as_it_resizes(self, page):
        """The handle is no longer a child of the panel -- nothing but
        positionHandle() keeps its left glued to the panel's own right
        edge (a left-docked panel's inner edge) once a drag moves it."""
        page.click("#dl-reference-toggle")
        page.wait_for_selector("#dl-reference:not([hidden])")
        _drag_without_releasing(page, _handle("dl-reference"), 120)
        handle_left = page.eval_on_selector(
            _handle("dl-reference"), "el => el.getBoundingClientRect().left"
        )
        panel_right = page.eval_on_selector(
            "#dl-reference", "el => el.getBoundingClientRect().right"
        )
        page.mouse.up()
        assert abs(handle_left - panel_right) < 2


class TestHandleHiddenWithItsPanel:
    def test_a_closed_panels_handle_is_not_in_the_hit_area(self, page):
        # Never opened -- the handle should start hidden, the same way a
        # child of a [hidden] panel used to be for free.
        assert page.is_hidden(_handle("dl-settings"))

    def test_reopening_shows_it_again(self, page):
        page.click("#dl-settings-toggle")
        page.wait_for_selector("#dl-settings:not([hidden])")
        assert page.is_visible(_handle("dl-settings"))
        page.click("#dl-settings-toggle")
        page.wait_for_selector("#dl-settings", state="hidden")
        assert page.is_hidden(_handle("dl-settings"))
