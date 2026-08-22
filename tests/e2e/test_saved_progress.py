"""Browser tests for saved work (Phase 2).

The happy path — nothing changed since last time — would very nearly work by
accident. The paths worth driving are the awkward ones: a tutorial edited under
a student's feet, and a saved cell that no longer exists in it. Both are
seeded directly into storage here rather than by rebuilding the page, because
what the restore logic actually reads is the record, not the file it came from.
"""

from __future__ import annotations

import json

import pytest


def output_of(cell_id: str) -> str:
    return f".dl-cell[data-cell-id='{cell_id}'] .dl-output"


def editor_text(page, cell_id: str) -> str:
    return page.eval_on_selector(
        f".dl-cell[data-cell-id='{cell_id}'] .cm-content", "el => el.innerText"
    )


def reload_and_wait(page):
    page.reload()
    page.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    page.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
        timeout=240_000,
    )


def seed(page, record: dict):
    page.evaluate(
        "([key, value]) => localStorage.setItem(key, value)",
        [page.evaluate("globalThis.dewlab.progressKey()"), json.dumps(record)],
    )


@pytest.fixture()
def clean_storage(page):
    """Each test starts with nothing saved, and leaves nothing behind."""
    page.evaluate("localStorage.clear()")
    yield page
    page.evaluate("localStorage.clear()")


class TestAutosave:
    def test_typing_is_saved_without_being_asked(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.type("# a note to self\n")
        page.wait_for_function(
            "globalThis.dewlab.readSaved() !== null", timeout=10_000
        )
        saved = page.evaluate("globalThis.dewlab.readSaved()")
        code = next(c for c in saved["cells"] if c["task_id"] == "plain-python")
        assert "a note to self" in code["student_code"]

    def test_the_record_carries_the_page_version_and_slug(self, clean_storage):
        page = clean_storage
        page.evaluate("globalThis.dewlab.saveNow()")
        saved = page.evaluate("globalThis.dewlab.readSaved()")
        assert saved["tutorial-slug"] == "rendering-tour"
        assert str(saved["tutorial-version"]) == "1"
        assert saved["saved_at"]

    def test_work_comes_back_after_a_reload(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.type("# remember me\n")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        reload_and_wait(page)
        assert "remember me" in editor_text(page, "plain-python")
        assert page.query_selector(".dl-restored") is not None

    def test_output_comes_back_too(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .dl-btn-run")
        page.wait_for_selector(f"{output_of('plain-python')} .dl-stdout", timeout=120_000)

        reload_and_wait(page)
        assert "counting:" in page.inner_text(output_of("plain-python"))


class TestTheAwkwardPaths:
    def test_an_edited_tutorial_restores_anyway_and_says_so(self, clean_storage):
        page = clean_storage
        seed(page, {
            "tutorial-slug": "rendering-tour",
            "tutorial-version": 99,
            "saved_at": "2026-01-01T00:00:00Z",
            "cells": [{"task_id": "plain-python", "student_code": "# from an older version",
                       "output_html": ""}],
        })
        reload_and_wait(page)

        assert "from an older version" in editor_text(page, "plain-python")
        notice = page.inner_text(".dl-restored")
        assert "updated" in notice.lower()

    def test_a_matching_version_restores_without_the_warning(self, clean_storage):
        page = clean_storage
        seed(page, {
            "tutorial-slug": "rendering-tour",
            "tutorial-version": 1,
            "saved_at": "2026-01-01T00:00:00Z",
            "cells": [{"task_id": "plain-python", "student_code": "# same version",
                       "output_html": ""}],
        })
        reload_and_wait(page)

        assert "same version" in editor_text(page, "plain-python")
        assert "updated" not in page.inner_text(".dl-restored").lower()

    def test_a_saved_cell_that_no_longer_exists_is_reported_not_discarded(self, clean_storage):
        page = clean_storage
        seed(page, {
            "tutorial-slug": "rendering-tour",
            "tutorial-version": 1,
            "saved_at": "2026-01-01T00:00:00Z",
            "cells": [
                {"task_id": "plain-python", "student_code": "# still here", "output_html": ""},
                {"task_id": "a-cell-that-was-deleted", "student_code": "# orphaned",
                 "output_html": ""},
            ],
        })
        reload_and_wait(page)

        notice = page.inner_text(".dl-restored")
        assert "not in this tutorial any more" in notice
        assert "still here" in editor_text(page, "plain-python")

    def test_a_cell_missing_from_the_save_keeps_its_starter_code(self, clean_storage):
        page = clean_storage
        seed(page, {
            "tutorial-slug": "rendering-tour",
            "tutorial-version": 1,
            "saved_at": "2026-01-01T00:00:00Z",
            "cells": [{"task_id": "plain-python", "student_code": "# only this one",
                       "output_html": ""}],
        })
        reload_and_wait(page)

        assert "readings" in editor_text(page, "numpy-basics")

    def test_a_restored_widget_says_it_needs_running_again(self, clean_storage):
        page = clean_storage
        seed(page, {
            "tutorial-slug": "rendering-tour",
            "tutorial-version": 1,
            "saved_at": "2026-01-01T00:00:00Z",
            "cells": [{"task_id": "tools-widgets", "student_code": "# widgets",
                       "output_html": '<div class="dl-widget">a box</div>'}],
        })
        reload_and_wait(page)

        assert "running again" in page.inner_text(".dl-restored")

    def test_nothing_saved_means_no_notice_at_all(self, clean_storage):
        page = clean_storage
        reload_and_wait(page)
        assert page.query_selector(".dl-restored") is None


class TestStartingAgain:
    def test_clearing_puts_the_starter_code_back_and_forgets_the_save(self, clean_storage):
        page = clean_storage
        page.click(".dl-cell[data-cell-id='plain-python'] .cm-content")
        page.keyboard.type("# to be cleared\n")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        page.on("dialog", lambda dialog: dialog.accept())
        page.click("#dl-settings-toggle")
        page.click("#dl-progress-clear")

        assert "to be cleared" not in editor_text(page, "plain-python")
        assert page.evaluate("globalThis.dewlab.readSaved()") is None


class TestAPageWithNothingToSave:
    """A prose-only tutorial, and the contents page, have no cells at all."""

    def test_it_does_not_offer_to_save_work_that_cannot_exist(self, browser, base_url):
        context = browser.new_context()
        tab = context.new_page()
        tab.goto(f"{base_url}/tutorials/fixtures/prose-only.html")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        assert tab.query_selector("#dl-settings-work") is None
        # The panel itself still belongs: a page with no cells is still a
        # reading surface, and the texture section is what makes it one.
        assert tab.query_selector("#dl-settings-toggle") is not None
        assert tab.query_selector("#dl-settings-texture") is not None
        context.close()

    def test_it_never_starts_python(self, browser, base_url):
        context = browser.new_context()
        tab = context.new_page()
        requested = []
        tab.on("request", lambda r: requested.append(r.url))
        tab.goto(f"{base_url}/tutorials/fixtures/prose-only.html")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        tab.wait_for_timeout(1500)
        assert not any("pyodide" in url for url in requested)
        context.close()

    def test_its_mathematics_still_renders(self, browser, base_url):
        context = browser.new_context()
        tab = context.new_page()
        tab.goto(f"{base_url}/tutorials/fixtures/prose-only.html")
        tab.wait_for_selector(".dl-math .katex", timeout=15_000)
        assert tab.eval_on_selector_all(".dl-math .katex", "e => e.length") >= 1
        context.close()
