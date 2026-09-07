"""Staged hints, in a real browser — planning/CELL_HINTS.md.

The fixture's `staged-hints` cell fails with a NameError as written. Its
first hint waits for two identical errors, its second for three errors in
all, and neither appears once the cell's `expect:` (`total == 6`) holds.
The counters and the revealed folds travel in the saved-work record, so a
reload keeps a hint the reader had just been shown.

    python3 -m pytest tests/e2e/test_cell_hints_staged.py -q
"""

from __future__ import annotations

import pytest

CELL = "staged-hints"


def fold(page, index: int):
    return page.locator(f"#dl-staged-{CELL}-{index}")


def marker(page):
    return page.locator(f".dl-cell[data-cell-id='{CELL}'] .dl-hint-marker")


def run(page):
    button = page.locator(f".dl-cell[data-cell-id='{CELL}'] .dl-btn-run")
    button.click()
    # The run-line paints once the run is over, so waiting on it is waiting
    # on the whole run, boot included the first time.
    page.wait_for_function(
        f"""() => {{
          const el = document.querySelector(".dl-cell[data-cell-id='{CELL}'] .dl-cell-runline");
          return el && /^Ran /.test(el.textContent);
        }}""",
        timeout=240_000,
    )
    page.wait_for_function(
        f"document.querySelector(\".dl-cell[data-cell-id='{CELL}'] .dl-btn-run\").textContent === 'Run'",
        timeout=240_000,
    )


def attempts(page):
    return page.evaluate(
        f"globalThis.dewlab.cells.find((c) => c.id === '{CELL}').attempts"
    )


def set_code(page, code: str):
    page.evaluate(
        f"([code]) => globalThis.dewlab.cells.find((c) => c.id === '{CELL}').editor.setValue(code)",
        [code],
    )


@pytest.fixture()
def clean_storage(page):
    page.evaluate("localStorage.clear()")
    yield
    page.evaluate("localStorage.clear()")


class TestStagedHints:
    def test_both_folds_start_hidden(self, page, clean_storage):
        assert fold(page, 0).is_hidden()
        assert fold(page, 1).is_hidden()
        assert marker(page).is_hidden()

    def test_hints_arrive_one_per_run_as_the_errors_pile_up(self, page, clean_storage):
        run(page)
        assert attempts(page)["errors"] == 1
        assert fold(page, 0).is_hidden(), "one error is not yet two identical ones"

        run(page)
        a = attempts(page)
        assert a["errors"] == 2 and a["sameErrors"] == 2 and a["unchanged"] == 1
        assert fold(page, 0).is_visible()
        assert not fold(page, 0).evaluate("el => el.open"), "arrives closed"
        assert fold(page, 1).is_hidden(), "one hint per run, and this one needs three"
        assert marker(page).is_visible()
        assert "spelled the same way" in fold(page, 0).text_content()

        run(page)
        assert fold(page, 1).is_visible()
        # The body went through the markdown converter and KaTeX.
        assert fold(page, 1).locator("ol li").count() == 2
        assert fold(page, 1).locator(".katex").count() >= 1

    def test_opening_the_fold_clears_the_marker(self, page, clean_storage):
        run(page)
        run(page)
        assert marker(page).is_visible()
        fold(page, 0).locator("summary").click()
        assert marker(page).is_hidden()

    def test_a_reload_keeps_what_was_shown(self, page, clean_storage):
        run(page)
        run(page)
        assert fold(page, 0).is_visible()
        page.reload()
        page.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        page.wait_for_selector(f".dl-cell[data-cell-id='{CELL}'] .cm-content", timeout=30_000)
        assert fold(page, 0).is_visible()
        assert fold(page, 1).is_hidden()
        assert attempts(page)["errors"] == 2
        # Restored, not arriving: no marker for a hint already seen.
        assert marker(page).is_hidden()

    def test_reaching_the_result_stops_further_hints_but_hides_none(self, page, clean_storage):
        run(page)
        run(page)
        assert fold(page, 0).is_visible()
        set_code(page, "total = 0\nfor value in [1, 2, 3]:\n    total = total + value\n")
        run(page)
        a = attempts(page)
        assert a["errors"] == 2 and a["sameErrors"] == 0
        assert fold(page, 0).is_visible(), "a hint once shown stays"
        assert fold(page, 1).is_hidden(), "three errors never happened"
        # Two more clean runs would satisfy nothing, but even a fold whose
        # terms held would not appear once expect: is true.
        run(page)
        run(page)
        assert fold(page, 1).is_hidden()

    def test_the_setting_hides_and_shows_without_forgetting(self, page, clean_storage):
        run(page)
        run(page)
        assert fold(page, 0).is_visible()
        page.click("#dl-settings-toggle")
        page.click("[data-staged-hints] button[data-value='off']")
        assert fold(page, 0).is_hidden()
        page.click("[data-staged-hints] button[data-value='on']")
        assert fold(page, 0).is_visible()

    def test_restart_keeps_hints_unless_asked_to_hide_them(self, page, clean_storage):
        run(page)
        run(page)
        assert fold(page, 0).is_visible()
        page.evaluate("globalThis.dewlab.restartPython()")
        page.wait_for_function(
            "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
            timeout=240_000,
        )
        assert fold(page, 0).is_visible(), "the default keeps what was shown"
        page.evaluate("localStorage.setItem('dewlab:staged-hints-restart', 'hide')")
        page.evaluate("globalThis.dewlab.restartPython()")
        page.wait_for_function(
            "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
            timeout=240_000,
        )
        assert fold(page, 0).is_hidden()
        assert attempts(page)["errors"] == 0
