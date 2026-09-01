"""Browser tests for the merged run line (order, duration, staleness), the
"⋯" Run above/below menu, and Restart & run all — planning/CELL_IDENTITY.md,
ported from dewmini.js's own already-shipped versions (DECISIONS_LOG.md
7.105, 7.106, 7.108, 7.113) onto tutorial pages' `.dl-cell`.

    python3 -m pytest tests/e2e/test_cell_run_menu.py -q
"""

from __future__ import annotations

import pytest


def cell(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}']")


def output_text(page, cell_id: str) -> str:
    return page.eval_on_selector(
        f".dl-cell[data-cell-id='{cell_id}'] .dl-output", "el => el.innerText"
    )


def run_line(page, cell_id: str):
    return page.locator(f".dl-cell[data-cell-id='{cell_id}'] .dl-cell-runline")


def run_line_text(page, cell_id: str) -> str:
    return page.eval_on_selector(
        f".dl-cell[data-cell-id='{cell_id}'] .dl-cell-runline", "el => el.textContent"
    )


def run_cell(page, cell_id: str):
    page.click(f".dl-cell[data-cell-id='{cell_id}'] .dl-btn-run")
    page.wait_for_function(
        "sel => document.querySelector(sel).textContent === 'Run'",
        arg=f".dl-cell[data-cell-id='{cell_id}'] .dl-btn-run",
        timeout=20_000,
    )


def wait_for_run_stats(page, cell_id: str, timeout: int = 20_000):
    """Waits for a specific cell's own run line to say it ran — a signal
    tied to that one cell, unlike the shared #dl-status line, which a
    later step of the same batch could already have overwritten by the
    time this gets to check it."""
    page.wait_for_function(
        "sel => (document.querySelector(sel)?.textContent || '').startsWith('Ran ')",
        arg=f".dl-cell[data-cell-id='{cell_id}'] .dl-cell-runline",
        timeout=timeout,
    )


def open_run_menu(page, cell_id: str):
    page.click(f".dl-cell[data-cell-id='{cell_id}'] .dl-btn-more")


@pytest.fixture()
def clean_storage(page):
    """Each test starts with nothing saved, and leaves nothing behind."""
    page.evaluate("localStorage.clear()")
    yield page
    page.evaluate("localStorage.clear()")


class TestRunLine:
    def test_says_not_yet_run_before_a_cell_has_ever_run(self, clean_storage):
        page = clean_storage
        assert run_line_text(page, "plain-python") == "Not yet run this session"

    def test_appears_after_editing_a_cell_that_already_ran(self, clean_storage):
        page = clean_storage
        run_cell(page, "plain-python")
        text = run_line_text(page, "plain-python")
        assert text.startswith("Ran ")
        assert "edited since" not in text

        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\n# a harmless edit")
        assert "edited since" in run_line_text(page, "plain-python")

    def test_clears_once_the_cell_is_run_again(self, clean_storage):
        page = clean_storage
        run_cell(page, "plain-python")
        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\n# a harmless edit")
        assert "edited since" in run_line_text(page, "plain-python")

        run_cell(page, "plain-python")
        assert "edited since" not in run_line_text(page, "plain-python")

    def test_reset_clears_it_along_with_the_output(self, clean_storage):
        page = clean_storage
        run_cell(page, "plain-python")
        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\n# a harmless edit")
        assert "edited since" in run_line_text(page, "plain-python")

        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-reset")
        assert run_line_text(page, "plain-python") == "Not yet run this session"


class TestRunMenu:
    def test_run_above_runs_this_cell_and_everything_before_it_only(self, clean_storage):
        page = clean_storage
        open_run_menu(page, "pandas-table")
        page.click(".dl-cell[data-cell-id='pandas-table'] [data-run-menu='above']")

        wait_for_run_stats(page, "pandas-table")
        assert "counting: 2" in output_text(page, "plain-python")
        assert "mean:" in output_text(page, "numpy-basics")
        assert output_text(page, "pandas-table").strip() != ""
        # Nothing below the target ran — the whole point of "above".
        assert run_line_text(page, "matplotlib-figure") == "Not yet run this session"

    def test_run_below_keeps_earlier_state_and_does_not_reset_the_namespace(self, clean_storage):
        page = clean_storage
        # Define something only "above" would normally re-seed, then run
        # "below" from the next cell down — it must still be there
        # afterwards, since "below" is documented to never reset first.
        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\nmarker_from_above = 'still here'")
        run_cell(page, "plain-python")

        open_run_menu(page, "numpy-basics")
        page.click(".dl-cell[data-cell-id='numpy-basics'] [data-run-menu='below']")
        # "below" runs every cell from numpy-basics to the end of the page —
        # wait for the very last one, tools-widgets, to know the whole
        # batch actually finished rather than just its first cell.
        wait_for_run_stats(page, "tools-widgets", timeout=60_000)
        assert "mean:" in output_text(page, "numpy-basics")

        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\nmarker_from_above")
        run_cell(page, "plain-python")
        assert "still here" in output_text(page, "plain-python")

    def test_the_menu_closes_on_an_outside_click(self, clean_storage):
        page = clean_storage
        open_run_menu(page, "plain-python")
        assert page.locator(".dl-cell[data-cell-id='plain-python'] .dl-cell-run-menu").is_visible()
        # initCellRunMenu() registers its outside-click listener via
        # setTimeout(fn, 0), deliberately after the click that opened the
        # menu has finished bubbling — a real click straight afterwards
        # lands comfortably after that, but this one is scripted right on
        # its heels, so it needs the same beat to actually be caught.
        page.wait_for_timeout(50)
        page.mouse.click(5, 5)
        assert page.locator(".dl-cell[data-cell-id='plain-python'] .dl-cell-run-menu").is_hidden()


class TestRestartAndRunAll:
    def test_restart_and_run_all_from_settings(self, clean_storage):
        page = clean_storage
        # Give the namespace something a fresh interpreter would not have,
        # so a stale, merely-reset namespace couldn't pass this by accident.
        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\nonly_the_old_interpreter_has_this = True")
        run_cell(page, "plain-python")

        page.click("#dl-settings-toggle")
        page.once("dialog", lambda dialog: dialog.accept())
        page.click("#dl-restart-run-all")

        # A real restart reboots the whole interpreter — as slow as the
        # very first boot the `page` fixture itself already waited out.
        page.wait_for_function(
            "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
            timeout=240_000,
        )
        # Then "run all" runs every cell on the page — wait for the last one.
        wait_for_run_stats(page, "tools-widgets", timeout=60_000)
        assert "counting: 2" in output_text(page, "plain-python")
        assert "mean:" in output_text(page, "numpy-basics")
        assert run_line_text(page, "plain-python").startswith("Ran ")
