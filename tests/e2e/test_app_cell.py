"""A full-stack (`html app`/`css app`/`js app`) cell, in a real browser
against a real Pyodide.

Exercises fixture/rendering-tour.md's "Full-stack cell" section: a `sql
exec` cell seeds a `readers` table, then the app cell's JS pane reads it
through `dlQuery` — the Worker-crossing bridge to `_query_rows()`
(planning/DEWSTACK_MERGE.md §3, §7 phase 4) — and writes into its own
`root` element. Unlike a site editor's sandboxed iframe (test_dewminiweb.py,
test_phase0_golden_path.py's site-editor tests), there is no frame here at
all: the point of this cell kind is reaching the page's own shared `db`,
which a site editor's sandbox exists specifically to block.
"""

from __future__ import annotations

import json

APP_SELECTOR = '.dl-app-cell[data-app-name="readers"]'


def js_string(text: str) -> str:
    """A JavaScript string literal, safely quoted for wait_for_function."""
    return json.dumps(text)


def seed_readers(page) -> None:
    """Run the sql exec cell the app cell's fixture section depends on."""
    output_selector = ".dl-cell[data-cell-id='app-seed-readers'] .dl-output"
    page.evaluate(f"dewlab.runCell({js_string('app-seed-readers')})")
    page.wait_for_function(
        f"document.querySelector({js_string(output_selector)}).children.length > 0",
        timeout=60_000,
    )


def run_app_cell(page) -> None:
    page.click(f"{APP_SELECTOR} .dl-btn-app-run")


def test_the_html_and_css_panes_are_live_before_run_is_pressed(page):
    """Only the js pane needs Run — the same rule a site editor's html/css
    panes follow (test_dewminiweb.py's "css is live without pressing
    run"). No reader-list items yet, since that only exists once the js
    pane's own query has written them in."""
    assert page.eval_on_selector(f"{APP_SELECTOR} #reader-list", "el => el.children.length") == 0
    weight = page.eval_on_selector(f"{APP_SELECTOR} #reader-list", "el => getComputedStyle(el).fontWeight")
    assert weight in ("700", "bold")


def test_running_the_cell_reads_the_shared_db_and_renders_the_page(page):
    seed_readers(page)
    run_app_cell(page)
    page.wait_for_function(
        f"document.querySelectorAll({js_string(APP_SELECTOR + ' #reader-list li')}).length === 2",
        timeout=15_000,
    )
    names = page.eval_on_selector_all(
        f"{APP_SELECTOR} #reader-list li", "els => els.map(e => e.textContent)"
    )
    assert names == ["Ada", "Grace"]
    assert page.problems == []


def test_the_css_pane_is_scoped_with_scope_not_a_global_rule(page):
    seed_readers(page)
    run_app_cell(page)
    page.wait_for_selector(f"{APP_SELECTOR} #reader-list li")
    text = page.eval_on_selector(f"{APP_SELECTOR} .dl-app-style", "el => el.textContent")
    assert text.strip().startswith("@scope (#")
    weight = page.eval_on_selector(f"{APP_SELECTOR} #reader-list", "el => getComputedStyle(el).fontWeight")
    assert weight in ("700", "bold")


def test_reset_reverts_the_editors_and_clears_the_preview(page):
    seed_readers(page)
    run_app_cell(page)
    page.wait_for_selector(f"{APP_SELECTOR} #reader-list li")

    page.click(f'{APP_SELECTOR} .dl-app-pane[data-lang="html"] .cm-content')
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("<p>edited</p>")

    page.click(f"{APP_SELECTOR} .dl-btn-app-reset")
    page.wait_for_function(
        f"document.querySelector({js_string(APP_SELECTOR + ' .dl-app-preview')}).children.length === 0"
    )
    assert "edited" not in page.eval_on_selector(
        f'{APP_SELECTOR} .dl-app-pane[data-lang="html"] .cm-content', "el => el.textContent"
    )


def test_a_bad_query_shows_in_the_error_box_not_silently(page):
    page.click(f'{APP_SELECTOR} .dl-app-pane[data-lang="js"] .cm-content')
    page.keyboard.press("Control+a")
    page.keyboard.insert_text('await dlQuery("select * from no_such_table");')

    run_app_cell(page)
    page.wait_for_function(
        f"document.querySelector({js_string(APP_SELECTOR + ' .dl-app-error')}).textContent.length > 0",
        timeout=15_000,
    )
    assert "no_such_table" in page.inner_text(f"{APP_SELECTOR} .dl-app-error")
    # The error is caught inside the injected script, not left to bubble as
    # an unhandled rejection — this is the friendly path, not a crash.
    assert page.problems == []


def test_saved_progress_restores_the_edited_panes_and_reruns_if_it_had_run(page):
    seed_readers(page)
    page.click(f'{APP_SELECTOR} .dl-app-pane[data-lang="html"] .cm-content')
    page.keyboard.press("Control+a")
    page.keyboard.insert_text('<ul id="reader-list"></ul><p id="marker">saved</p>')
    run_app_cell(page)
    page.wait_for_function(
        f"document.querySelector({js_string(APP_SELECTOR + ' #marker')}) !== null", timeout=15_000
    )
    page.evaluate("globalThis.dewlab.saveNow()")

    page.reload()
    page.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    page.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0", timeout=240_000
    )
    page.wait_for_function(
        f"document.querySelector({js_string(APP_SELECTOR + ' #marker')}) !== null", timeout=15_000
    )
