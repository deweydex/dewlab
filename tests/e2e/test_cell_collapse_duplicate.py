"""Browser tests for the collapse triangle and Duplicate — the rest of
dewmini's cell anatomy (DECISIONS_LOG.md 7.110), ported onto tutorial
pages' `.dl-cell` in 7.114.

    python3 -m pytest tests/e2e/test_cell_collapse_duplicate.py -q
"""

from __future__ import annotations

import pytest


def is_collapsed(page, cell_id: str) -> bool:
    return page.eval_on_selector(
        f".dl-cell[data-cell-id='{cell_id}'] .dl-cell-content", "el => el.hidden"
    )


def summary_text(page, cell_id: str) -> str:
    return page.eval_on_selector(
        f".dl-cell[data-cell-id='{cell_id}'] .dl-cell-collapsed-summary",
        "el => el.textContent",
    )


@pytest.fixture()
def clean_storage(page):
    page.evaluate("localStorage.clear()")
    yield page
    page.evaluate("localStorage.clear()")


class TestCollapse:
    def test_starts_expanded(self, clean_storage):
        page = clean_storage
        assert not is_collapsed(page, "plain-python")
        assert page.locator(
            ".dl-cell[data-cell-id='plain-python'] .dl-cell-collapsed-summary"
        ).is_hidden()

    def test_the_triangle_collapses_and_expands_the_code(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-collapse-toggle")
        assert is_collapsed(page, "plain-python")
        # The summary is the cell's own first line (fixture/rendering-tour.md).
        assert "Printed text" in summary_text(page, "plain-python")

        page.click(".dl-cell[data-cell-id='plain-python'] .dl-collapse-toggle")
        assert not is_collapsed(page, "plain-python")

    def test_clicking_the_summary_also_expands_it(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-collapse-toggle")
        assert is_collapsed(page, "plain-python")

        page.click(".dl-cell[data-cell-id='plain-python'] .dl-cell-collapsed-summary")
        assert not is_collapsed(page, "plain-python")

    def test_output_stays_visible_while_collapsed(self, clean_storage):
        """Collapsing hides the code, not the result it produced
        (planning/CELL_IDENTITY.md §4)."""
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-run")
        page.wait_for_function(
            "sel => document.querySelector(sel).textContent === 'Run'",
            arg=".dl-cell[data-cell-id='plain-python'] .dl-btn-run",
            timeout=20_000,
        )
        output_before = page.inner_text(".dl-cell[data-cell-id='plain-python'] .dl-output")
        assert output_before.strip() != ""

        page.click(".dl-cell[data-cell-id='plain-python'] .dl-collapse-toggle")
        output_after = page.inner_text(".dl-cell[data-cell-id='plain-python'] .dl-output")
        assert output_after == output_before

    def test_collapse_survives_a_reload(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-collapse-toggle")
        assert is_collapsed(page, "plain-python")

        page.reload()
        page.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        page.wait_for_function(
            "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
            timeout=240_000,
        )
        assert is_collapsed(page, "plain-python")


class TestDuplicate:
    def test_duplicate_adds_a_custom_cell_with_the_same_code(self, clean_storage):
        page = clean_storage
        before = page.locator(".dl-cell-custom").count()
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-duplicate")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        assert page.locator(".dl-cell-custom").count() == before + 1

        original_code = page.eval_on_selector(
            ".dl-cell[data-cell-id='plain-python'] .cm-content", "el => el.innerText"
        )
        copy_code = page.eval_on_selector(
            ".dl-cell-custom .cm-content", "el => el.innerText"
        )
        assert copy_code == original_code

    def test_the_original_cell_is_unaffected_by_editing_the_copy(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-duplicate")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)

        page.click(".dl-cell-custom .cm-content")
        page.keyboard.press("Control+End")
        page.keyboard.insert_text("\n# a change only in the copy")

        original_code = page.eval_on_selector(
            ".dl-cell[data-cell-id='plain-python'] .cm-content", "el => el.innerText"
        )
        assert "a change only in the copy" not in original_code

    def test_duplicating_twice_keeps_both_copies(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-duplicate")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-duplicate")
        page.wait_for_function(
            "document.querySelectorAll('.dl-cell-custom').length === 2", timeout=5_000
        )

    def test_a_custom_cell_can_duplicate_itself_too(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-duplicate")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)

        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("\nmarker = 'only in the first copy'")

        page.click(".dl-cell-custom .dl-btn-duplicate")
        page.wait_for_function(
            "document.querySelectorAll('.dl-cell-custom').length === 2", timeout=5_000
        )
        second_copy_code = page.eval_on_selector_all(
            ".dl-cell-custom .cm-content", "els => els[1].innerText"
        )
        assert "only in the first copy" in second_copy_code

    def test_duplicate_inserts_right_after_the_cell_not_at_the_end(self, clean_storage):
        """A reader's own later cell, added under the same authored cell,
        must not end up between the original and its own fresh copy."""
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-duplicate")
        page.wait_for_selector(".dl-cell-custom", timeout=5_000)
        page.click(".dl-cell-custom .cm-content")
        page.keyboard.type("first_custom = True")

        # A second Duplicate of the *authored* cell must land right after
        # the authored cell — before the reader's own first custom cell —
        # not appended after everything already in that group.
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-duplicate")
        page.wait_for_function(
            "document.querySelectorAll('.dl-cell-custom').length === 2", timeout=5_000
        )
        second_dup_code = page.eval_on_selector_all(
            ".dl-cell-custom .cm-content", "els => els[0].innerText"
        )
        assert "first_custom" not in second_dup_code
