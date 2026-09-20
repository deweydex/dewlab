"""Browser tests for saved work (Phase 2): saving it, showing it back to a
reader (the live run summary, and the site-wide badges), and restoring it.

The happy path — nothing changed since last time — would very nearly work by
accident. The paths worth driving are the awkward ones: a tutorial edited under
a student's feet, and a saved cell that no longer exists in it. Both are
seeded directly into storage here rather than by rebuilding the page, because
what the restore logic actually reads is the record, not the file it came from.
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

from conftest import _open_panel, _open_settings_tab

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402
from layout import write_course, write_tutorial  # noqa: E402


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
    """A large embedded figure can blow the storage quota; saveNow() must not
    let that cost a reader their code and notes too. Storage.prototype.setItem
    is overridden to throw past a size deterministically, standing in for a
    real quota."""

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
    """A student's own free-text notes, distinct from a tutorial's
    author-written pedagogical notes, riding on the same record."""

    def test_typing_a_note_is_saved_without_being_asked(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", "the ISO date trick only works because...")
        page.wait_for_function(
            "globalThis.dewlab.readSaved() !== null", timeout=10_000
        )
        saved = page.evaluate("globalThis.dewlab.readSaved()")
        assert saved["notes"] == "the ISO date trick only works because..."

    def test_a_note_comes_back_after_a_reload(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", "remember this for later")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        reload_and_wait(page)
        _open_panel(page, "#dl-yourwork-toggle")
        assert page.input_value("#dl-progress-notes") == "remember this for later"

    def test_start_again_clears_the_note_too(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", "throwaway")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        page.once("dialog", lambda dialog: dialog.accept())
        page.click("#dl-progress-clear")
        assert page.input_value("#dl-progress-notes") == ""

    def test_declining_start_again_keeps_the_note(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", "keep me")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        page.once("dialog", lambda dialog: dialog.dismiss())
        page.click("#dl-progress-clear")
        assert page.input_value("#dl-progress-notes") == "keep me"
        assert page.evaluate("globalThis.dewlab.readSaved()") is not None

    def test_exporting_downloads_the_note_alongside_the_cells(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", "goes in the export too")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        with page.expect_download() as download_info:
            page.click("#dl-progress-export")
        download = download_info.value
        content = download.path().read_text()
        assert "goes in the export too" in content


class TestNotesNudge:
    """A marker on "Export a copy" once notes have grown since the last
    export. NOTES_NUDGE_THRESHOLD (tutorial-runtime.js) is 120 characters —
    SHORT/LONG below are sized against that, not an arbitrary guess."""

    SHORT = "a few words"
    LONG = "x" * 130

    def export_button_class(self, page) -> str:
        return page.get_attribute("#dl-progress-export", "class") or ""

    def test_a_short_note_gets_no_marker(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", self.SHORT)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" not in self.export_button_class(page)

    def test_a_long_note_gets_a_marker(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", self.LONG)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" in self.export_button_class(page)

    def test_exporting_clears_the_marker(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", self.LONG)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" in self.export_button_class(page)

        with page.expect_download():
            page.click("#dl-progress-export")
        assert "dl-nudge" not in self.export_button_class(page)

        # And it stays gone across a reload — the baseline is stored, not
        # just the in-memory class.
        reload_and_wait(page)
        _open_panel(page, "#dl-yourwork-toggle")
        assert "dl-nudge" not in self.export_button_class(page)

    def test_writing_more_after_export_marks_it_again(self, clean_storage):
        page = clean_storage
        _open_panel(page, "#dl-yourwork-toggle")
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
        _open_panel(page, "#dl-yourwork-toggle")
        page.fill("#dl-progress-notes", self.LONG)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)
        assert "dl-nudge" in self.export_button_class(page)

        page.click('[data-notes-nudge] button[data-value="off"]')
        assert "dl-nudge" not in self.export_button_class(page)

        reload_and_wait(page)
        assert "dl-nudge" not in self.export_button_class(page)

        page.click('[data-notes-nudge] button[data-value="on"]')
        assert "dl-nudge" in self.export_button_class(page)


def _summary_js_string(text: str) -> str:
    return json.dumps(text)


def run_cell(page, cell_id: str) -> None:
    selector = f".dl-cell[data-cell-id='{cell_id}'] .dl-output"
    page.evaluate(f"dewlab.runCell({_summary_js_string(cell_id)})")
    page.wait_for_function(
        f"document.querySelector({_summary_js_string(selector)}).children.length > 0",
        timeout=60_000,
    )


def summary_text(page) -> str:
    _open_panel(page, "#dl-yourwork-toggle")
    text = page.inner_text("#dl-progress-summary")
    _open_panel(page, "#dl-yourwork-toggle")
    return text


class TestProgressSummary:
    """The live "N of M cells run" line in the Your Work panel — read while
    still on the page, from the session's own runs rather than a saved
    record, since the `errored` count depends on the real traceback markup
    a run produces (tutorial_tools.py's class="dl-error")."""

    def test_stays_hidden_with_nothing_run(self, page):
        _open_panel(page, "#dl-yourwork-toggle")
        assert page.is_hidden("#dl-progress-summary")
        _open_panel(page, "#dl-yourwork-toggle")

    def test_updates_after_a_successful_run(self, page):
        run_cell(page, "plain-python")
        text = summary_text(page)
        assert "of" in text and "cells run" in text
        assert "error" not in text

    def test_counts_an_errored_cell_separately_from_a_successful_one(self, page):
        run_cell(page, "plain-python")
        run_cell(page, "error-traceback")
        text = summary_text(page)
        assert "2 of" in text
        assert "1 with an error" in text


class TestProgressBadges:
    """The fraction badge shown elsewhere on the site (all-tutorials.html)
    for a tutorial with saved work — read from a saved record rather than a
    live interpreter, so seeded directly into localStorage rather than by
    running a cell, against a small fixture site of this class's own
    (the shared `page` fixture's tutorial isn't listed on a contents page)."""

    COURSE = "progress-fixtures"

    FRONTMATTER = """---
title: "{title}"
year: "2026-2027"
version: 2026.08.23.1
---

# {title}

```python exec
id: {slug}-1
print("hello")
```

```python exec
id: {slug}-2
print("world")
```
"""

    @staticmethod
    def _tutorial(root: Path, slug: str, title: str = "A Title") -> None:
        path = root / "tutorials" / slug / f"{slug}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(TestProgressBadges.FRONTMATTER.format(title=title, slug=slug))

    @classmethod
    def _set_order(cls, root: Path, slugs: list[str]) -> None:
        write_course(root, cls.COURSE, "Sample Series", slugs)

    @staticmethod
    def _seed(page, slug: str, cells: list[dict]) -> None:
        """A saved-progress record written straight into localStorage, as saveNow() would, without a cell run."""
        record = {
            "tutorial-id": slug,
            "tutorial-version": "2026.08.23.1",
            "saved_at": "2026-08-28T00:00:00.000Z",
            "cells": cells,
        }
        page.evaluate(
            "([key, value]) => localStorage.setItem(key, value)",
            [f"dewlab:progress:{slug}", json.dumps(record)],
        )

    @pytest.fixture()
    def badges_site(self, tmp_path, monkeypatch):
        (tmp_path / "tutorials").mkdir(parents=True)
        monkeypatch.setattr(b, "ROOT", tmp_path)
        monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
        monkeypatch.setattr(b, "COURSES", tmp_path / "courses")
        monkeypatch.setattr(b, "OUT", tmp_path / "site")
        monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
        monkeypatch.setattr(b, "DATA", DEWLAB / "data")
        monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
        monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
        return tmp_path

    @pytest.fixture()
    def badges_site_url(self, badges_site):
        handler = functools.partial(_QuietBadgesHandler, directory=str(badges_site / "site"))
        server = socketserver.TCPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_address[1]}"
        finally:
            server.shutdown()
            thread.join(timeout=5)

    def test_a_tutorial_with_no_saved_record_shows_no_badge(self, badges_site, browser, badges_site_url):
        self._tutorial(badges_site, "one", "One")
        self._set_order(badges_site, ["one"])
        b.build()
        context = browser.new_context()
        badge_page = context.new_page()
        badge_page.goto(f"{badges_site_url}/all-tutorials.html")
        assert badge_page.is_hidden(".dl-progress-badge")
        context.close()

    def test_a_saved_record_with_nothing_run_shows_no_badge(self, badges_site, browser, badges_site_url):
        """A cell only edited, never run, has no output_html, so an empty one here must count as untouched."""
        self._tutorial(badges_site, "one", "One")
        self._set_order(badges_site, ["one"])
        b.build()
        context = browser.new_context()
        badge_page = context.new_page()
        badge_page.goto(f"{badges_site_url}/all-tutorials.html")
        self._seed(badge_page, "one", [
            {"task_id": "one-1", "student_code": "x = 1", "output_html": "", "errored": False},
        ])
        badge_page.reload()
        assert badge_page.is_hidden(".dl-progress-badge")
        context.close()

    def test_a_run_cell_shows_a_fraction_badge(self, badges_site, browser, badges_site_url):
        self._tutorial(badges_site, "one", "One")
        self._set_order(badges_site, ["one"])
        b.build()
        context = browser.new_context()
        badge_page = context.new_page()
        badge_page.goto(f"{badges_site_url}/all-tutorials.html")
        self._seed(badge_page, "one", [
            {"task_id": "one-1", "student_code": "", "output_html": "<pre>hello</pre>", "errored": False},
            {"task_id": "one-2", "student_code": "", "output_html": "", "errored": False},
        ])
        badge_page.reload()
        badge = badge_page.locator(".dl-progress-badge")
        assert badge.inner_text() == "1/2"
        assert "dl-progress-badge-errored" not in (badge.get_attribute("class") or "")
        context.close()

    def test_an_errored_cell_gives_the_badge_the_error_colour(self, badges_site, browser, badges_site_url):
        self._tutorial(badges_site, "one", "One")
        self._set_order(badges_site, ["one"])
        b.build()
        context = browser.new_context()
        badge_page = context.new_page()
        badge_page.goto(f"{badges_site_url}/all-tutorials.html")
        self._seed(badge_page, "one", [
            {"task_id": "one-1", "student_code": "", "output_html": "<pre>hello</pre>", "errored": False},
            {"task_id": "one-2", "student_code": "", "output_html": '<pre class="dl-error">boom</pre>', "errored": True},
        ])
        badge_page.reload()
        badge = badge_page.locator(".dl-progress-badge")
        assert badge.inner_text() == "2/2"
        assert "dl-progress-badge-errored" in badge.get_attribute("class")
        context.close()

    def test_the_settings_toggle_hides_and_restores_badges(self, badges_site, browser, badges_site_url):
        self._tutorial(badges_site, "one", "One")
        self._set_order(badges_site, ["one"])
        b.build()
        context = browser.new_context()
        badge_page = context.new_page()
        badge_page.goto(f"{badges_site_url}/all-tutorials.html")
        self._seed(badge_page, "one", [
            {"task_id": "one-1", "student_code": "", "output_html": "<pre>hello</pre>", "errored": False},
        ])
        badge_page.reload()
        assert badge_page.is_visible(".dl-progress-badge")

        _open_settings_tab(badge_page, "behavior")
        badge_page.click('[data-progress-badges] button[data-value="off"]')
        _open_panel(badge_page, "#dl-settings-toggle")
        assert badge_page.is_hidden(".dl-progress-badge")

        # And it holds across a reload — a real setting, not a one-off toggle.
        badge_page.reload()
        assert badge_page.is_hidden(".dl-progress-badge")

        _open_settings_tab(badge_page, "behavior")
        badge_page.click('[data-progress-badges] button[data-value="on"]')
        _open_panel(badge_page, "#dl-settings-toggle")
        assert badge_page.is_visible(".dl-progress-badge")
        context.close()


class _QuietBadgesHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


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
        _open_panel(page, "#dl-yourwork-toggle")
        page.click("#dl-progress-clear")

        assert "to be cleared" not in editor_text(page, "plain-python")
        assert page.evaluate("globalThis.dewlab.readSaved()") is None


class TestAPageWithNothingToSave:
    """A prose-only tutorial has no cells, but it is still a tutorial, so
    "Your work" stays for its notes field."""

    def test_a_prose_only_tutorial_still_offers_the_notes_field(self, browser, base_url):
        context = browser.new_context()
        tab = context.new_page()
        tab.goto(f"{base_url}/tutorials/prose-only.html")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        assert tab.query_selector("#dl-settings-work") is not None
        assert tab.query_selector("#dl-progress-notes") is not None
        # The panel itself still belongs: a page with no cells is still a
        # reading surface, and the texture section is what makes it one.
        assert tab.query_selector("#dl-yourwork-toggle") is not None
        assert tab.query_selector("#dl-settings-toggle") is not None
        assert tab.query_selector("#dl-settings-reading") is not None
        context.close()

    def test_it_never_starts_python(self, browser, base_url):
        context = browser.new_context()
        tab = context.new_page()
        requested = []
        tab.on("request", lambda r: requested.append(r.url))
        tab.goto(f"{base_url}/tutorials/prose-only.html")
        tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
        tab.wait_for_timeout(1500)
        assert not any("pyodide" in url for url in requested)
        context.close()

    def test_its_mathematics_still_renders(self, browser, base_url):
        context = browser.new_context()
        tab = context.new_page()
        tab.goto(f"{base_url}/tutorials/prose-only.html")
        tab.wait_for_selector(".dl-math .katex", timeout=15_000)
        assert tab.eval_on_selector_all(".dl-math .katex", "e => e.length") >= 1
        context.close()


def test_saved_work_is_keyed_on_the_tutorials_id(page):
    """An id is site-wide — the folder name — so it is the whole key."""
    key = page.evaluate("globalThis.dewlab.progressKey()")
    slug = page.get_attribute('meta[name="tutorial-slug"]', "content")
    assert key == f"dewlab:progress:{slug}"


class TestLoadingSomebodyElsesFile:
    """Import used to write the file into this page's key and only then find
    out it didn't match — destroying a student's real work in the process."""

    def test_a_record_from_this_tutorial_fits(self, page):
        slug = page.get_attribute('meta[name="tutorial-slug"]', "content")
        assert page.evaluate(
            "(r) => globalThis.dewlab.describeMismatch(r)",
            {"tutorial-id": slug, "cells": []},
        ) == ""

    def test_a_record_from_another_tutorial_does_not(self, page):
        message = page.evaluate(
            "(r) => globalThis.dewlab.describeMismatch(r)",
            {"tutorial-id": "something-else", "cells": []},
        )
        assert "not this tutorial" in message
        assert "Nothing has been changed" in message

    def test_a_record_from_before_courses_fits_where_the_page_had_that_address(self, page, base_url):
        """A file saved when pages were addressed by module and slug names
        them both. On a page whose manifest records that old address, it
        fits when both halves match and not otherwise; on a page that never
        had one, the slug alone decides, as it always did."""
        slug = page.get_attribute('meta[name="tutorial-slug"]', "content")
        assert page.evaluate(
            "(r) => globalThis.dewlab.describeMismatch(r)",
            {"tutorial-slug": slug, "tutorial-module": "fixtures", "cells": []},
        ) == ""
        tab = page.context.new_page()
        try:
            tab.goto(f"{base_url}/tutorials/prose-only.html")
            tab.wait_for_selector("#dl-body")
            assert tab.evaluate(
                "(r) => globalThis.dewlab.describeMismatch(r)",
                {"tutorial-slug": "prose-only", "tutorial-module": "fixtures", "cells": []},
            ) == ""
            message = tab.evaluate(
                "(r) => globalThis.dewlab.describeMismatch(r)",
                {"tutorial-slug": "prose-only", "tutorial-module": "somewhere-else", "cells": []},
            )
            assert "not this tutorial" in message
            assert "somewhere-else" in message
        finally:
            tab.close()

    def test_a_record_naming_only_a_slug_fits_on_its_own_id(self, page):
        """Leniency with a reason: a file saved before the id was recorded
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
        mine = {"tutorial-id": page.get_attribute('meta[name="tutorial-slug"]', "content"),
                "saved_at": "2026-01-01T00:00:00Z",
                "cells": []}
        seed(page, mine)
        page.evaluate(
            """(other) => {
                 if (!globalThis.dewlab.describeMismatch(other)) {
                   localStorage.setItem(globalThis.dewlab.progressKey(),
                                        JSON.stringify(other));
                 }
               }""",
            {"tutorial-id": "elsewhere", "cells": []},
        )
        assert page.evaluate("globalThis.dewlab.readSaved()")["saved_at"] == mine["saved_at"]
