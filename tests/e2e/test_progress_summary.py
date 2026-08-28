"""The in-tutorial "Progress" summary in Settings, in a real browser —
planning/PROGRESS_INDICATORS.md.

Real cell runs, not seeded state, since the whole point of the `errored`
capture is that it reads what a real traceback actually rendered
(tutorial_tools.py's class="dl-error") — a seeded fake risks testing the
test's own assumption about that shape rather than the real one.

    python3 -m pytest tests/e2e/test_progress_summary.py -q
"""

from __future__ import annotations

import json


def js_string(text: str) -> str:
    return json.dumps(text)


def run(page, cell_id: str) -> None:
    selector = f".dl-cell[data-cell-id='{cell_id}'] .dl-output"
    page.evaluate(f"dewlab.runCell({js_string(cell_id)})")
    page.wait_for_function(
        f"document.querySelector({js_string(selector)}).children.length > 0",
        timeout=60_000,
    )


def summary_text(page) -> str:
    page.click("#dl-settings-toggle")
    text = page.inner_text("#dl-progress-summary")
    page.click("#dl-settings-close")
    return text


class TestProgressSummary:
    def test_stays_hidden_with_nothing_run(self, page):
        page.click("#dl-settings-toggle")
        assert page.is_hidden("#dl-progress-summary")
        page.click("#dl-settings-close")

    def test_updates_after_a_successful_run(self, page):
        run(page, "plain-python")
        text = summary_text(page)
        assert "of" in text and "cells run" in text
        assert "error" not in text

    def test_counts_an_errored_cell_separately_from_a_successful_one(self, page):
        run(page, "plain-python")
        run(page, "error-traceback")
        text = summary_text(page)
        assert "2 of" in text
        assert "1 with an error" in text
