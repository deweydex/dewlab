"""Uses real cell runs rather than seeded state, since the `errored` count depends on the real traceback markup a run produces (tutorial_tools.py's class="dl-error")."""

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
    _open_panel(page, "#dl-settings-toggle")
    text = page.inner_text("#dl-progress-summary")
    page.click("#dl-settings-close")
    return text


def _open_panel(actor, selector: str) -> None:
    """Reference/Series/Settings' toggles now collapse behind one
    "Panels" control in the masthead (shell.html's
    <details class="dl-panels">) rather than always showing — expand it
    first if it isn't already, then click the actual target. Checked via
    #dl-panels' own `open` property rather than the target's own
    visibility, so this never mistakes "already open" for "not open" and
    toggles it shut again right before the click that was supposed to
    land. Left expanded once opened (no auto-collapse), so this is only
    needed once per page load, not before every toggle click."""
    if not actor.eval_on_selector("#dl-panels", "el => el.open"):
        actor.click("#dl-panels summary")
    actor.click(selector)


class TestProgressSummary:
    def test_stays_hidden_with_nothing_run(self, page):
        _open_panel(page, "#dl-settings-toggle")
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
