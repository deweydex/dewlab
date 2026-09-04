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
        assert str(saved["tutorial-version"]) == "2026.08.23.1"
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


class TestOversizedOutputFallback:
    """DECISIONS_LOG.md 7.131: a large embedded figure (tutorial_tools.py's
    _figure_html(), a base64 PNG) can be big enough on its own to blow this
    browser's storage quota — saveNow() must not let that cost a reader
    their code and notes too. Storage.prototype.setItem is overridden here
    to throw past a size deterministically, standing in for a browser's own
    quota rather than trying to actually fill one up."""

    def fail_past(self, page, limit: int):
        page.evaluate(
            """(limit) => {
                 const real = Storage.prototype.setItem;
                 Storage.prototype.setItem = function (key, value) {
                   if (value.length > limit) {
                     throw new DOMException("full", "QuotaExceededError");
                   }
                   return real.call(this, key, value);
                 };
               }""",
            limit,
        )

    def inflate_output(self, page, cell_id: str, size: int):
        page.evaluate(
            """([cellId, size]) => {
                 document.querySelector(
                   `.dl-cell[data-cell-id='${cellId}'] .dl-output`
                 ).innerHTML = "x".repeat(size);
               }""",
            [cell_id, size],
        )

    def test_a_too_large_cell_output_is_dropped_so_the_rest_still_saves(self, clean_storage):
        page = clean_storage
        self.fail_past(page, 150_000)
        page.click(".dl-cell[data-cell-id='numpy-basics'] .cm-content")
        page.keyboard.type("# keep me\n")
        self.inflate_output(page, "plain-python", 200_000)

        page.evaluate("globalThis.dewlab.saveNow()")

        saved = page.evaluate("globalThis.dewlab.readSaved()")
        big = next(c for c in saved["cells"] if c["task_id"] == "plain-python")
        kept = next(c for c in saved["cells"] if c["task_id"] == "numpy-basics")
        assert big["output_html"] == ""
        assert "keep me" in kept["student_code"]

    def test_it_says_so_rather_than_claiming_a_normal_save(self, clean_storage):
        page = clean_storage
        self.fail_past(page, 150_000)
        self.inflate_output(page, "plain-python", 200_000)

        page.evaluate("globalThis.dewlab.saveNow()")

        state = page.inner_text("#dl-progress-state")
        assert "ran out of room" in state
        assert "large figure" in state

    def test_a_reload_shows_no_output_for_the_dropped_cell(self, clean_storage):
        page = clean_storage
        self.fail_past(page, 150_000)
        self.inflate_output(page, "plain-python", 200_000)
        page.evaluate("globalThis.dewlab.saveNow()")

        reload_and_wait(page)
        assert page.inner_text(output_of("plain-python")).strip() == ""


class TestStudentNotes:
    """planning/STUDENT_NOTES.md — a student's own free-text notes, distinct
    from SIDEBAR_CONTENT.md's author-written pedagogical notes, riding along
    on the same saved-progress record as cell work."""

    def test_typing_a_note_is_saved_without_being_asked(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", "the ISO date trick only works because...")
        page.wait_for_function(
            "globalThis.dewlab.readSaved() !== null", timeout=10_000
        )
        saved = page.evaluate("globalThis.dewlab.readSaved()")
        assert saved["notes"] == "the ISO date trick only works because..."

    def test_a_note_comes_back_after_a_reload(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", "remember this for later")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        reload_and_wait(page)
        page.click("#dl-settings-toggle")
        assert page.input_value("#dl-progress-notes") == "remember this for later"

    def test_start_again_clears_the_note_too(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", "throwaway")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        page.once("dialog", lambda dialog: dialog.accept())
        page.click("#dl-progress-clear")
        assert page.input_value("#dl-progress-notes") == ""

    def test_exporting_downloads_the_note_alongside_the_cells(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", "goes in the export too")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        with page.expect_download() as download_info:
            page.click("#dl-progress-export")
        download = download_info.value
        content = download.path().read_text()
        assert "goes in the export too" in content


class TestNotesNudge:
    """planning/STUDENT_NOTES.md §4's larger proposal: a small marker on
    "Export a copy" once notes have grown a fair bit since the last export.
    NOTES_NUDGE_THRESHOLD (tutorial-runtime.js) is 120 characters — every
    string below uses that directly rather than a magic number of its own."""

    SHORT = "a few words"
    LONG = "x" * 130

    def export_button_class(self, page) -> str:
        return page.get_attribute("#dl-progress-export", "class") or ""

    def test_a_short_note_gets_no_marker(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", self.SHORT)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" not in self.export_button_class(page)

    def test_a_long_note_gets_a_marker(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", self.LONG)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" in self.export_button_class(page)

    def test_exporting_clears_the_marker(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", self.LONG)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" in self.export_button_class(page)

        with page.expect_download():
            page.click("#dl-progress-export")
        assert "dl-nudge" not in self.export_button_class(page)

        # And it stays gone across a reload — the baseline is stored, not
        # just the in-memory class.
        reload_and_wait(page)
        page.click("#dl-settings-toggle")
        assert "dl-nudge" not in self.export_button_class(page)

    def test_writing_more_after_export_marks_it_again(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", self.SHORT)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        with page.expect_download():
            page.click("#dl-progress-export")
        assert "dl-nudge" not in self.export_button_class(page)

        page.fill("#dl-progress-notes", self.SHORT + self.LONG)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" in self.export_button_class(page)

    def test_the_settings_toggle_turns_the_marker_off(self, clean_storage):
        page = clean_storage
        page.click("#dl-settings-toggle")
        page.fill("#dl-progress-notes", self.LONG)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" in self.export_button_class(page)

        page.click('[data-notes-nudge] button[data-value="off"]')
        assert "dl-nudge" not in self.export_button_class(page)

        # Holds across a reload — a real setting, not a one-off toggle.
        reload_and_wait(page)
        page.click("#dl-settings-toggle")
        assert "dl-nudge" not in self.export_button_class(page)

        page.click('[data-notes-nudge] button[data-value="on"]')
        assert "dl-nudge" in self.export_button_class(page)


class TestTheAwkwardPaths:
    def test_an_edited_tutorial_restores_anyway_and_says_so(self, clean_storage):
        page = clean_storage
        seed(page, {
            "tutorial-slug": "rendering-tour",
            "tutorial-version": "2020.01.01.1",
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
            "tutorial-version": "2026.08.23.1",
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
            "tutorial-version": "2026.08.23.1",
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
            "tutorial-version": "2026.08.23.1",
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
            "tutorial-version": "2026.08.23.1",
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
    """A prose-only tutorial has no cells at all — but it is still a
    tutorial, so "Your work" stays for its notes field
    (planning/STUDENT_NOTES.md, DECISIONS_LOG.md 7.71). The contents page
    is the one that truly has nothing here at all, since it is not a
    tutorial in the first place."""

    def test_a_prose_only_tutorial_still_offers_the_notes_field(self, browser, base_url):
        context = browser.new_context()
        tab = context.new_page()
        tab.goto(f"{base_url}/tutorials/fixtures/prose-only.html")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        assert tab.query_selector("#dl-settings-work") is not None
        assert tab.query_selector("#dl-progress-notes") is not None
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


def test_saved_work_is_keyed_on_the_module_as_well_as_the_slug(page):
    """A slug is only unique within its module, and both modules have a
    `first-steps`. Keyed on the slug alone the two shared one record, so a
    student's answers in one appeared in the other and each overwrote it.

    Checked through the key rather than by building two modules: if the module
    is in the key, the collision cannot happen, and the e2e fixture is one
    module by design."""
    key = page.evaluate("globalThis.dewlab.progressKey()")
    assert key.startswith("dewlab:progress:")
    assert "fixtures" in key, key
    slug = page.get_attribute('meta[name="tutorial-slug"]', "content")
    assert key.endswith(slug), key
    # And the two parts are distinguishable, so a module named like a slug
    # cannot be confused for one.
    assert key == f"dewlab:progress:fixtures:{slug}"


class TestLoadingSomebodyElsesFile:
    """Import used to write the file into this page's key and only then find
    out the cells did not match — destroying a student's real work to make room
    for a record that did not belong here."""

    def test_a_record_from_this_tutorial_fits(self, page):
        slug = page.get_attribute('meta[name="tutorial-slug"]', "content")
        assert page.evaluate(
            "(r) => globalThis.dewlab.describeMismatch(r)",
            {"tutorial-slug": slug, "tutorial-module": "fixtures", "cells": []},
        ) == ""

    def test_a_record_from_the_same_slug_in_another_module_does_not(self, page):
        """The case that made this necessary: both modules have a
        `first-steps`, so the slug alone says nothing."""
        slug = page.get_attribute('meta[name="tutorial-slug"]', "content")
        message = page.evaluate(
            "(r) => globalThis.dewlab.describeMismatch(r)",
            {"tutorial-slug": slug, "tutorial-module": "somewhere-else", "cells": []},
        )
        assert "not this tutorial" in message
        assert "somewhere-else" in message
        assert "Nothing has been changed" in message

    def test_a_record_from_another_tutorial_does_not(self, page):
        message = page.evaluate(
            "(r) => globalThis.dewlab.describeMismatch(r)",
            {"tutorial-slug": "something-else", "tutorial-module": "fixtures", "cells": []},
        )
        assert "not this tutorial" in message

    def test_a_record_with_no_module_still_fits_on_its_own_slug(self, page):
        """Leniency with a reason: a file saved before the module was recorded
        should still load where it belongs rather than hitting a cliff."""
        slug = page.get_attribute('meta[name="tutorial-slug"]', "content")
        assert page.evaluate(
            "(r) => globalThis.dewlab.describeMismatch(r)",
            {"tutorial-slug": slug, "cells": []},
        ) == ""

    def test_something_that_is_not_saved_work_is_refused(self, page):
        for junk in ({"hello": "world"}, [], "text"):
            assert "could not be read" in page.evaluate(
                "(r) => globalThis.dewlab.describeMismatch(r)", junk)

    def test_a_mismatched_file_leaves_the_existing_record_alone(self, page):
        """The point of the whole check."""
        mine = {"tutorial-slug": page.get_attribute('meta[name="tutorial-slug"]', "content"),
                "tutorial-module": "fixtures", "saved_at": "2026-01-01T00:00:00Z",
                "cells": []}
        seed(page, mine)
        page.evaluate(
            """(other) => {
                 if (!globalThis.dewlab.describeMismatch(other)) {
                   localStorage.setItem(globalThis.dewlab.progressKey(),
                                        JSON.stringify(other));
                 }
               }""",
            {"tutorial-slug": "elsewhere", "tutorial-module": "other", "cells": []},
        )
        assert page.evaluate("globalThis.dewlab.readSaved()")["saved_at"] == mine["saved_at"]
