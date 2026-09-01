"""Browser tests for a reader's own cells (planning/PRACTICE.md §3-5).

Most of what matters here is that this feature stays a separate system
from the tutorial's own saved-work record — its own storage key, its own
array, never counted anywhere the real cells are counted. The tests below
check that directly (reading `dewlab.customCellsKey()`'s own storage,
never `dewlab.readSaved()`) rather than assuming it from the code.

A second thing worth its own coverage: a custom cell is no longer only
addable from one button at the bottom of the page — a divider sits after
every real cell and every custom cell (`.dl-insert`), each offering "+
Code" and "+ Text", and where a cell was added (its `anchor`) is what a
reload uses to put it back in the same place. See
`docs/tutorial-runtime-explained.md`'s "Custom cells" section for the
full mechanics.

The one thing genuinely worth a self-contained fixture (like
test_student_notes_prose_only.py's) is confirming the feature is *absent*
on a page with zero cells — that case never boots Pyodide at all, so it
would be wasteful to route it through the shared `page` fixture, which
waits for a real Pyodide boot before it even yields.

    python3 -m pytest tests/e2e/test_custom_cells.py -q
"""

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

TRAILING_ANCHOR = "__trailing__"


def reload_and_wait(page):
    page.reload()
    page.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    page.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
        timeout=240_000,
    )


def custom_cells_storage(page) -> list:
    """Whatever is actually saved under this page's own custom-cells key
    — not `dewlab.readSaved()`, which is the tutorial's own, separate
    record and should never see a custom cell at all."""
    key = page.evaluate("globalThis.dewlab.customCellsKey()")
    raw = page.evaluate("(k) => localStorage.getItem(k)", key)
    return json.loads(raw) if raw else []


def wait_for_saved_count(page, count):
    page.wait_for_function(
        """([key, count]) => {
          const raw = localStorage.getItem(key);
          return raw !== null && JSON.parse(raw).length === count;
        }""",
        arg=[page.evaluate("globalThis.dewlab.customCellsKey()"), count],
        timeout=10_000,
    )


def add_via_trailing_divider(page, kind="Code"):
    """Clicks the trailing section's own divider — the general "add one
    somewhere, no particular cell in mind" entry point every custom-cells
    page always has, even with zero cells added yet."""
    divider = page.locator(f'.dl-insert[data-anchor="{TRAILING_ANCHOR}"]').first
    divider.locator(".dl-insert-btn", has_text=kind).click()


@pytest.fixture()
def clean_storage(page):
    page.evaluate("localStorage.clear()")
    yield page
    page.evaluate("localStorage.clear()")


class TestDividersAppearEverywhere:
    def test_a_divider_follows_every_real_cell_plus_one_trailing(self, clean_storage):
        page = clean_storage
        real = page.locator(".dl-cell:not(.dl-cell-custom)").count()
        dividers = page.locator(".dl-insert").count()
        assert dividers == real + 1

    def test_each_real_cells_divider_carries_that_cells_id_as_anchor(self, clean_storage):
        page = clean_storage
        first_id = page.locator(".dl-cell:not(.dl-cell-custom)").first.get_attribute("data-cell-id")
        assert page.locator(f'.dl-insert[data-anchor="{first_id}"]').count() == 1


class TestAddingACustomCell:
    def test_the_section_appears_on_a_page_with_cells(self, clean_storage):
        page = clean_storage
        assert page.is_visible("#dl-custom-cells")
        assert page.locator(".dl-cell-custom").count() == 0

    def test_adding_a_code_cell_creates_a_dl_cell_custom(self, clean_storage):
        page = clean_storage
        add_via_trailing_divider(page, "Code")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        assert page.locator(".dl-cell-custom").count() == 1
        assert page.locator(".dl-cell-custom.dl-cell-text").count() == 0

    def test_adding_a_text_cell_creates_a_dl_cell_text_with_no_run_button(self, clean_storage):
        page = clean_storage
        add_via_trailing_divider(page, "Text")
        page.wait_for_selector(".dl-cell-custom.dl-cell-text", timeout=5_000)
        cell = page.locator(".dl-cell-custom.dl-cell-text").first
        assert cell.locator(".dl-btn-run").count() == 0
        assert cell.locator(".dl-doc-editor").count() == 1

    def test_a_divider_right_after_a_real_cell_inserts_the_cell_there(self, clean_storage):
        page = clean_storage
        second_real = page.locator(".dl-cell:not(.dl-cell-custom)").nth(1)
        second_id = second_real.get_attribute("data-cell-id")
        page.locator(f'.dl-insert[data-anchor="{second_id}"]').first.locator(
            ".dl-insert-btn", has_text="Code"
        ).click()
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        new_cell = page.locator(".dl-cell-custom").first
        assert new_cell.get_attribute("data-anchor") == second_id
        preceding_real = page.evaluate(
            """() => {
              let n = document.querySelector('.dl-cell-custom').previousElementSibling;
              while (n && !n.classList.contains('dl-cell')) n = n.previousElementSibling;
              return n ? n.dataset.cellId : null;
            }"""
        )
        assert preceding_real == second_id

    def test_typing_autosaves_under_its_own_key_not_the_tutorials(self, clean_storage):
        page = clean_storage
        add_via_trailing_divider(page, "Code")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("6 * 7")
        wait_for_saved_count(page, 1)
        saved = custom_cells_storage(page)
        assert len(saved) == 1
        assert "6 * 7" in saved[0]["code"]
        assert saved[0]["type"] == "python"
        assert saved[0]["anchor"] == TRAILING_ANCHOR

        # The tutorial's own saved-work record never sees it.
        tutorial_record = page.evaluate("globalThis.dewlab.readSaved()")
        if tutorial_record:
            ids = [c["task_id"] for c in tutorial_record["cells"]]
            assert saved[0]["id"] not in ids

    def test_a_text_cells_notes_autosave_too(self, clean_storage):
        page = clean_storage
        add_via_trailing_divider(page, "Text")
        page.wait_for_selector(".dl-cell-text", timeout=5_000)
        page.fill(".dl-cell-text .dl-doc-editor", "# Heading\n\n**bold** notes")
        wait_for_saved_count(page, 1)
        saved = custom_cells_storage(page)
        assert saved[0]["type"] == "text"
        assert "**bold** notes" in saved[0]["code"]

        page.locator(".dl-cell-text .dl-doc-editor").blur()
        page.wait_for_selector(".dl-cell-text .dl-doc-render:not([hidden])", timeout=5_000)
        rendered = page.inner_html(".dl-cell-text .dl-doc-render")
        assert "<h4>Heading</h4>" in rendered
        assert "<strong>bold</strong>" in rendered

    def test_a_rendered_text_cells_chrome_is_invisible_until_touched(self, clean_storage):
        """DECISIONS_LOG.md 7.115, planning/CELL_IDENTITY.md §4 — a rendered
        text cell reads like part of the page, not a code widget, until a
        reader actually touches it. Ported from compose/dewmini-style.css's
        own .dm-cell-text rule."""
        page = clean_storage
        add_via_trailing_divider(page, "Text")
        page.wait_for_selector(".dl-cell-text", timeout=5_000)
        page.fill(".dl-cell-text .dl-doc-editor", "A note for the reader.")
        page.locator(".dl-cell-text .dl-doc-editor").blur()
        page.wait_for_selector(".dl-cell-text .dl-doc-render:not([hidden])", timeout=5_000)

        page.mouse.move(5, 5)
        page.wait_for_timeout(150)  # let the 0.1s opacity transition settle
        bar = page.locator(".dl-cell-text .dl-cell-bar")
        assert bar.evaluate("el => getComputedStyle(el).opacity") == "0"

        page.hover(".dl-cell-text")
        page.wait_for_timeout(150)
        assert bar.evaluate("el => getComputedStyle(el).opacity") == "1"

    def test_the_view_edit_button_toggles_while_the_textarea_is_still_focused(self, clean_storage):
        """A click on the button, not a blur-then-click, is the case worth
        covering: clicking straight out of the textarea (rather than
        tabbing or clicking elsewhere first) used to blur it — which
        auto-rendered — and then the button's own handler saw the
        already-flipped state and toggled straight back to editing."""
        page = clean_storage
        add_via_trailing_divider(page, "Text")
        page.wait_for_selector(".dl-cell-text", timeout=5_000)
        page.click(".dl-cell-text .dl-doc-editor")
        page.keyboard.type("Some notes")
        btn = page.locator(".dl-cell-text .dl-btn-preview")
        assert btn.text_content() == "view"
        btn.click()
        assert page.eval_on_selector(".dl-cell-text .dl-doc-editor", "el => el.hidden") is True
        assert btn.text_content() == "edit"
        btn.click()
        assert page.eval_on_selector(".dl-cell-text .dl-doc-editor", "el => el.hidden") is False

    def test_a_custom_cell_survives_a_reload_in_the_same_place(self, clean_storage):
        page = clean_storage
        second_real = page.locator(".dl-cell:not(.dl-cell-custom)").nth(1)
        second_id = second_real.get_attribute("data-cell-id")
        page.locator(f'.dl-insert[data-anchor="{second_id}"]').first.locator(
            ".dl-insert-btn", has_text="Code"
        ).click()
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("remember this one")
        wait_for_saved_count(page, 1)

        reload_and_wait(page)
        assert page.locator(".dl-cell-custom").count() == 1
        text = page.eval_on_selector(".dl-cell-custom .cm-content", "el => el.innerText")
        assert "remember this one" in text
        assert page.locator(".dl-cell-custom").first.get_attribute("data-anchor") == second_id

    def test_an_orphaned_anchor_falls_back_to_the_trailing_section(self, clean_storage):
        """A tutorial update can remove the real cell a custom cell was
        anchored to — PRACTICE.md §3's "survives a version change
        untouched" means the cell is never dropped, only repositioned."""
        page = clean_storage
        key = page.evaluate("globalThis.dewlab.customCellsKey()")
        page.evaluate(
            """([key]) => {
              localStorage.setItem(key, JSON.stringify([
                {id: "custom-orphan", type: "python", anchor: "not-a-real-cell-id", code: "1"},
              ]));
            }""",
            [key],
        )
        reload_and_wait(page)
        anchor = page.evaluate(
            '() => document.querySelector(\'[data-cell-id="custom-orphan"]\').dataset.anchor'
        )
        assert anchor == TRAILING_ANCHOR

    def test_output_is_saved_and_restored_too(self, clean_storage):
        page = clean_storage
        add_via_trailing_divider(page, "Code")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("print('from a custom cell')")
        page.click(".dl-cell-custom .dl-btn-run")
        page.wait_for_selector(".dl-cell-custom .dl-output .dl-stdout", timeout=120_000)

        reload_and_wait(page)
        assert "from a custom cell" in page.inner_text(".dl-cell-custom .dl-output")

    def test_deleting_one_needs_no_confirmation_and_removes_its_own_divider(self, clean_storage):
        page = clean_storage
        before = page.locator(".dl-insert").count()
        add_via_trailing_divider(page, "Code")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        assert page.locator(".dl-insert").count() == before + 1
        # If a confirm() dialog appeared, this test would hang waiting for
        # it — no dialog listener is registered, on purpose.
        page.click(".dl-cell-custom .dl-btn-delete")
        page.wait_for_timeout(300)
        assert page.locator(".dl-cell-custom").count() == 0
        assert custom_cells_storage(page) == []
        assert page.locator(".dl-insert").count() == before


class TestSharingAndLoadingACustomCell:
    def test_share_downloads_the_cells_code_and_type(self, clean_storage, tmp_path):
        page = clean_storage
        add_via_trailing_divider(page, "Code")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("shared_value = 42")

        with page.expect_download() as dl_info:
            page.click(".dl-cell-custom .dl-btn-share")
        download = dl_info.value
        saved_to = tmp_path / "shared.json"
        download.save_as(saved_to)
        payload = json.loads(saved_to.read_text())
        assert payload["dewlab-custom-cell"] == 1
        assert payload["type"] == "python"
        assert "shared_value = 42" in payload["code"]

    def test_loading_a_shared_cell_never_runs_it(self, clean_storage, tmp_path):
        page = clean_storage
        shared_file = tmp_path / "shared.json"
        shared_file.write_text(json.dumps({"dewlab-custom-cell": 1, "code": "1 + 1"}))

        page.click("#dl-settings-toggle")
        page.wait_for_selector("#dl-settings-custom-cells", timeout=5_000)
        with page.expect_file_chooser() as fc_info:
            page.click("#dl-custom-cells-import")
        fc_info.value.set_files(str(shared_file))
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)

        text = page.eval_on_selector(".dl-cell-custom .cm-content", "el => el.innerText")
        assert "1 + 1" in text
        output = page.eval_on_selector(".dl-cell-custom .dl-output", "el => el.innerHTML")
        assert output.strip() == ""

    def test_loading_a_shared_cell_never_reuses_its_id(self, clean_storage, tmp_path):
        """A file's own id is never trusted — always a fresh local one, so an
        imported cell can never collide with one of this reader's own."""
        page = clean_storage
        shared_file = tmp_path / "shared.json"
        shared_file.write_text(
            json.dumps({"dewlab-custom-cell": 1, "code": "0", "id": "custom-not-mine"})
        )
        page.click("#dl-settings-toggle")
        with page.expect_file_chooser() as fc_info:
            page.click("#dl-custom-cells-import")
        fc_info.value.set_files(str(shared_file))
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        saved = custom_cells_storage(page)
        assert saved[0]["id"] != "custom-not-mine"
        assert saved[0]["id"].startswith("custom-")

    def test_loading_a_shared_text_cell_keeps_its_type(self, clean_storage, tmp_path):
        page = clean_storage
        shared_file = tmp_path / "shared.json"
        shared_file.write_text(
            json.dumps({"dewlab-custom-cell": 1, "type": "text", "code": "# A note"})
        )
        page.click("#dl-settings-toggle")
        with page.expect_file_chooser() as fc_info:
            page.click("#dl-custom-cells-import")
        fc_info.value.set_files(str(shared_file))
        page.wait_for_selector(".dl-cell-text", timeout=5_000)
        assert custom_cells_storage(page)[0]["type"] == "text"

    def test_a_file_that_is_not_a_shared_cell_is_rejected(self, clean_storage, tmp_path):
        page = clean_storage
        bad_file = tmp_path / "not-a-cell.json"
        bad_file.write_text(json.dumps({"hello": "world"}))
        page.click("#dl-settings-toggle")
        with page.expect_file_chooser() as fc_info:
            page.click("#dl-custom-cells-import")
        fc_info.value.set_files(str(bad_file))
        page.wait_for_timeout(500)
        assert page.locator(".dl-cell-custom").count() == 0


class TestClearingAllCustomCells:
    def test_asks_for_confirmation_and_respects_cancel(self, clean_storage):
        page = clean_storage
        add_via_trailing_divider(page, "Code")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)

        page.click("#dl-settings-toggle")
        page.once("dialog", lambda d: d.dismiss())
        page.click("#dl-custom-cells-clear")
        page.wait_for_timeout(300)
        assert page.locator(".dl-cell-custom").count() == 1

    def test_accepting_removes_every_custom_cell_but_keeps_the_seed_dividers(self, clean_storage):
        page = clean_storage
        before = page.locator(".dl-insert").count()
        add_via_trailing_divider(page, "Code")
        add_via_trailing_divider(page, "Text")
        page.wait_for_function(
            "document.querySelectorAll('.dl-cell-custom').length === 2", timeout=5_000
        )

        page.click("#dl-settings-toggle")
        page.once("dialog", lambda d: d.accept())
        page.click("#dl-custom-cells-clear")
        page.wait_for_timeout(300)
        assert page.locator(".dl-cell-custom").count() == 0
        assert custom_cells_storage(page) == []
        assert page.locator(".dl-insert").count() == before


class TestExport:
    def test_print_button_calls_window_print(self, clean_storage):
        page = clean_storage
        page.evaluate("window.__printed = false; window.print = () => { window.__printed = true; }")
        page.click("#dl-settings-toggle")
        page.click("#dl-print-pdf")
        assert page.evaluate("window.__printed") is True

    def test_ipynb_export_includes_real_and_custom_cells_in_document_order(self, clean_storage, tmp_path):
        page = clean_storage
        add_via_trailing_divider(page, "Code")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("exported = True")

        page.click("#dl-settings-toggle")
        with page.expect_download() as dl_info:
            page.click("#dl-export-ipynb")
        nb_path = tmp_path / "exported.ipynb"
        dl_info.value.save_as(nb_path)
        notebook = json.loads(nb_path.read_text())
        assert notebook["nbformat"] == 4
        assert notebook["cells"][0]["cell_type"] == "markdown"
        assert any(
            c["cell_type"] == "code" and "exported = True" in "".join(c["source"])
            for c in notebook["cells"]
        )

    def test_ipynb_export_with_zero_cells_shows_a_status_message_not_a_download(self, clean_storage):
        # This tutorial always has at least its own authored cells, so
        # exercise the guard directly rather than needing a zero-cell
        # fixture — the same function a real zero-cell page would call.
        page = clean_storage
        page.evaluate(
            """() => {
              document.querySelectorAll('.dl-cell').forEach((el) => el.remove());
              globalThis.dewlab.cells.length = 0;
              globalThis.dewlab.customCells.length = 0;
            }"""
        )
        page.evaluate("globalThis.dewlab.downloadAsIpynb()")
        page.wait_for_selector("#dl-status:not([hidden])", timeout=5_000)
        assert "No cells to export" in page.inner_text("#dl-status")


# --------------------------------------------------------- a page with no cells
#
# Self-contained, no Pyodide needed — same reasoning
# test_student_notes_prose_only.py already established: a prose-only
# tutorial's own boot() never loads Pyodide at all, so there's no reason
# to route this through the shared `page` fixture, which waits for a real
# boot before it even yields.

MODULE = "custom-cells-fixtures"

FRONTMATTER = """---
title: "{title}"
slug: {slug}
module: custom-cells-fixtures
module_title: "Custom Cells Fixtures"
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
def prose_only_site(tmp_path, monkeypatch):
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


def _serve(out_dir: Path):
    handler = functools.partial(_QuietHandler, directory=str(out_dir))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{port}"


class TestNoCustomCellsOnAProseOnlyPage:
    def test_neither_the_section_nor_the_settings_entry_appear(self, prose_only_site, browser):
        site = prose_only_site
        _tutorial(site, "one", "One")
        _set_order(site, ["one"])
        b.build()
        server, thread, url = _serve(site / "site")
        try:
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{url}/tutorials/{MODULE}/one.html")
            assert page.locator("#dl-custom-cells").count() == 0
            assert page.locator(".dl-insert").count() == 0
            page.click("#dl-settings-toggle")
            assert page.is_hidden("#dl-settings-custom-cells")
            # Print/export still applies to a prose-only page — only the
            # custom-cells machinery is what's gated on cells.length.
            assert page.is_visible("#dl-settings-export")
            context.close()
        finally:
            server.shutdown()
            thread.join(timeout=5)
