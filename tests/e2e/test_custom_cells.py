"""Browser tests for a reader's own cells (planning/PRACTICE.md §3-5).

Most of what matters here is that this feature stays a separate system
from the tutorial's own saved-work record — its own storage key, its own
array, never counted anywhere the real cells are counted. The tests below
check that directly (reading `dewlab.customCellsKey()`'s own storage,
never `dewlab.readSaved()`) rather than assuming it from the code.

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


@pytest.fixture()
def clean_storage(page):
    page.evaluate("localStorage.clear()")
    yield page
    page.evaluate("localStorage.clear()")


class TestAddingACustomCell:
    def test_the_section_appears_on_a_page_with_cells(self, clean_storage):
        page = clean_storage
        assert page.is_visible("#dl-custom-cells")
        assert page.locator(".dl-cell-custom").count() == 0

    def test_adding_one_creates_a_dl_cell_custom(self, clean_storage):
        page = clean_storage
        page.click(".dl-custom-cells-add")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        assert page.locator(".dl-cell-custom").count() == 1

    def test_typing_autosaves_under_its_own_key_not_the_tutorials(self, clean_storage):
        page = clean_storage
        page.click(".dl-custom-cells-add")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("6 * 7")
        page.wait_for_function(
            "globalThis.dewlab.customCellsKey && "
            "localStorage.getItem(globalThis.dewlab.customCellsKey()) !== null",
            timeout=10_000,
        )
        saved = custom_cells_storage(page)
        assert len(saved) == 1
        assert "6 * 7" in saved[0]["code"]

        # The tutorial's own saved-work record never sees it.
        tutorial_record = page.evaluate("globalThis.dewlab.readSaved()")
        if tutorial_record:
            ids = [c["task_id"] for c in tutorial_record["cells"]]
            assert saved[0]["id"] not in ids

    def test_a_custom_cell_survives_a_reload(self, clean_storage):
        page = clean_storage
        page.click(".dl-custom-cells-add")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("remember this one")
        page.wait_for_function(
            "localStorage.getItem(globalThis.dewlab.customCellsKey()) !== null",
            timeout=10_000,
        )

        reload_and_wait(page)
        assert page.locator(".dl-cell-custom").count() == 1
        text = page.eval_on_selector(".dl-cell-custom .cm-content", "el => el.innerText")
        assert "remember this one" in text

    def test_output_is_saved_and_restored_too(self, clean_storage):
        page = clean_storage
        page.click(".dl-custom-cells-add")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("print('from a custom cell')")
        page.click(".dl-cell-custom .dl-btn-run")
        page.wait_for_selector(".dl-cell-custom .dl-output .dl-stdout", timeout=120_000)

        reload_and_wait(page)
        assert "from a custom cell" in page.inner_text(".dl-cell-custom .dl-output")

    def test_deleting_one_needs_no_confirmation(self, clean_storage):
        page = clean_storage
        page.click(".dl-custom-cells-add")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        # If a confirm() dialog appeared, this test would hang waiting for
        # it — no dialog listener is registered, on purpose.
        page.click(".dl-cell-custom .dl-btn-delete")
        page.wait_for_timeout(300)
        assert page.locator(".dl-cell-custom").count() == 0
        assert custom_cells_storage(page) == []


class TestSharingAndLoadingACustomCell:
    def test_share_downloads_the_cells_code(self, clean_storage, tmp_path):
        page = clean_storage
        page.click(".dl-custom-cells-add")
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
        page.click(".dl-custom-cells-add")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)

        page.click("#dl-settings-toggle")
        page.once("dialog", lambda d: d.dismiss())
        page.click("#dl-custom-cells-clear")
        page.wait_for_timeout(300)
        assert page.locator(".dl-cell-custom").count() == 1

    def test_accepting_removes_every_custom_cell(self, clean_storage):
        page = clean_storage
        for _ in range(2):
            page.click(".dl-custom-cells-add")
        page.wait_for_function(
            "document.querySelectorAll('.dl-cell-custom').length === 2", timeout=5_000
        )

        page.click("#dl-settings-toggle")
        page.once("dialog", lambda d: d.accept())
        page.click("#dl-custom-cells-clear")
        page.wait_for_timeout(300)
        assert page.locator(".dl-cell-custom").count() == 0
        assert custom_cells_storage(page) == []


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
            page.click("#dl-settings-toggle")
            assert page.is_hidden("#dl-settings-custom-cells")
            context.close()
        finally:
            server.shutdown()
            thread.join(timeout=5)
