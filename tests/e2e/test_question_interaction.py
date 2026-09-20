"""Live behaviour of a ```question fence -- selecting an option, filling a
gap, and Check grading it -- in a real browser. Everything that existed
before this file (tests/build/test_questions.py) checked the markup a
question builds; nothing had ever clicked an option or typed a gap and
watched `evaluateQuestion()`/`gapIsCorrect()` (tutorial-runtime.js) grade
it, and nothing had proven a reader's answer survives a reload."""

from __future__ import annotations

import functools
import http.server
import socketserver
import sys
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402
from layout import write_course, write_tutorial  # noqa: E402

COURSE = "question-fixtures"
SLUG = "one"

TUTORIAL = """---
title: "One"
year: "2026-2027"
version: 2026.08.23.1
---

# One

```question
id: right-angle
type: multiple-choice
correct: 2

Which of these is a right angle?

- 45 degrees
- 90 degrees
- 180 degrees
```

```question
id: angle-names
type: fill-in-the-blank

An angle of 90 degrees is a {right angle|straight angle|acute angle}.
The {mitochondrion} is the site of aerobic respiration.
```
"""

MC = '#dl-question-right-angle'
FIB = '#dl-question-angle-names'


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, SLUG, TUTORIAL)
    write_course(tmp_path, COURSE, "Sample Series", [SLUG])
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "COURSES", tmp_path / "courses")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
    b.build()
    return tmp_path


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture()
def site_url(site):
    handler = functools.partial(_QuietHandler, directory=str(site / "site"))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def page(browser, site_url):
    context = browser.new_context()
    dl_page = context.new_page()
    dl_page.goto(f"{site_url}/tutorials/{SLUG}.html")
    dl_page.wait_for_function("() => !!globalThis.dewlab")
    yield dl_page
    context.close()


def select_option(page, text: str) -> None:
    page.click(f'{MC} .dl-question-option:text-is("{text}")')


class TestMultipleChoice:
    def test_the_check_button_starts_disabled_until_something_is_selected(self, page):
        assert page.is_disabled(f"{MC} .dl-question-check")
        select_option(page, "90 degrees")
        assert not page.is_disabled(f"{MC} .dl-question-check")

    def test_selecting_the_correct_option_and_checking_shows_pass(self, page):
        select_option(page, "90 degrees")
        page.click(f"{MC} .dl-question-check")
        assert page.is_visible(f"{MC} .dl-check-pass")

    def test_selecting_the_wrong_option_and_checking_shows_fail(self, page):
        select_option(page, "45 degrees")
        page.click(f"{MC} .dl-question-check")
        assert page.is_visible(f"{MC} .dl-check-fail")

    def test_a_selection_and_its_grading_survive_a_reload(self, page):
        select_option(page, "90 degrees")
        page.click(f"{MC} .dl-question-check")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")
        assert "is-selected" in (page.get_attribute(
            f'{MC} .dl-question-option:text-is("90 degrees")', "class") or "")
        assert page.is_visible(f"{MC} .dl-check-pass")


class TestFillInTheBlank:
    def test_filling_both_gaps_correctly_and_checking_shows_pass(self, page):
        page.select_option(f"{FIB} .dl-question-gap-select", label="right angle")
        page.fill(f"{FIB} .dl-question-gap-input", "mitochondrion")
        page.click(f"{FIB} .dl-question-check")
        assert page.is_visible(f"{FIB} .dl-check-pass")
        assert "is-correct" in page.get_attribute(f"{FIB} .dl-question-gap-select", "class")
        assert "is-correct" in page.get_attribute(f"{FIB} .dl-question-gap-input", "class")

    def test_a_wrong_gap_is_marked_incorrect_and_the_question_fails(self, page):
        page.select_option(f"{FIB} .dl-question-gap-select", label="straight angle")
        page.fill(f"{FIB} .dl-question-gap-input", "mitochondrion")
        page.click(f"{FIB} .dl-question-check")
        assert page.is_visible(f"{FIB} .dl-check-fail")
        assert "is-incorrect" in page.get_attribute(f"{FIB} .dl-question-gap-select", "class")
        assert "is-correct" in page.get_attribute(f"{FIB} .dl-question-gap-input", "class")

    def test_the_gap_values_and_their_grading_survive_a_reload(self, page):
        page.select_option(f"{FIB} .dl-question-gap-select", label="right angle")
        page.fill(f"{FIB} .dl-question-gap-input", "mitochondrion")
        page.click(f"{FIB} .dl-question-check")
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")
        assert page.eval_on_selector(f"{FIB} .dl-question-gap-input", "el => el.value") == "mitochondrion"
        assert page.is_visible(f"{FIB} .dl-check-pass")
