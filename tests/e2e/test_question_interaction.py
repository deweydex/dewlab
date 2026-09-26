"""Live behaviour of a ```question fence in a real browser: choosing an
option or filling a gap, then asking for the page's answer. Since #314 a
question never grades: it marks the page's own answer beside the reader's
choice, shows the note for that choice, and says "You chose the same as
the page." when it is. The reader's answer, and whether they asked,
survive a reload."""

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
answer: 2

Which of these is a right angle?

- 45 degrees
  - Half of a right angle: the corner of a square cut in two.
- 90 degrees
- 180 degrees
  - A straight line: two right angles side by side.
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


def option(page, position: int) -> str:
    """An option by its place in the source, which travels with it however
    the page shuffles the buttons."""
    return f'{MC} .dl-question-option[data-option="{position}"]'


def ask(page, where: str) -> None:
    page.click(f"{where} .dl-question-check")


JUDGING = ("right answer", "correct", "wrong", "not quite", "not yet", "✓", "✗")


class TestMultipleChoice:
    def test_the_button_waits_for_a_choice_and_asks_for_the_pages_answer(self, page):
        button = f"{MC} .dl-question-check"
        assert page.is_disabled(button)
        assert page.inner_text(button) == "Show the page’s answer"
        page.click(option(page, 1))
        assert not page.is_disabled(button)

    def test_asking_marks_the_pages_answer_beside_a_different_choice(self, page):
        page.click(option(page, 1))
        ask(page, MC)
        assert "is-page-answer" in page.get_attribute(option(page, 2), "class")
        assert page.inner_text(f"{option(page, 2)} .dl-question-page-label") == "the page’s answer"
        assert "is-selected" in page.get_attribute(option(page, 1), "class")
        assert page.is_visible(f'{MC} .dl-question-note[data-option="1"]')
        assert page.is_hidden(f'{MC} .dl-question-note[data-option="3"]')
        assert page.is_hidden(f"{MC} .dl-question-same")
        text = page.inner_text(MC).lower()
        for word in JUDGING:
            assert word not in text, word

    def test_the_same_choice_as_the_page_is_confirmed(self, page):
        page.click(option(page, 2))
        ask(page, MC)
        assert page.is_visible(f"{MC} .dl-question-same")

    def test_changing_the_choice_afterwards_updates_the_note(self, page):
        page.click(option(page, 1))
        ask(page, MC)
        page.click(option(page, 3))
        assert page.is_visible(f'{MC} .dl-question-note[data-option="3"]')
        assert page.is_hidden(f'{MC} .dl-question-note[data-option="1"]')

    def test_a_choice_and_the_asking_survive_a_reload(self, page):
        page.click(option(page, 1))
        ask(page, MC)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")
        assert "is-selected" in (page.get_attribute(option(page, 1), "class") or "")
        assert "is-page-answer" in (page.get_attribute(option(page, 2), "class") or "")
        assert page.is_visible(f'{MC} .dl-question-note[data-option="1"]')


class TestFillInTheBlank:
    def test_asking_shows_the_pages_word_after_each_gap_and_marks_nothing(self, page):
        assert page.inner_text(f"{FIB} .dl-question-check") == "Show the page’s words"
        page.select_option(f"{FIB} .dl-question-gap-select", label="straight angle")
        page.fill(f"{FIB} .dl-question-gap-input", "nucleus")
        ask(page, FIB)
        words = page.eval_on_selector_all(f"{FIB} .dl-question-page-word", "els => els.map(e => e.textContent)")
        assert words == [" (the page: right angle)", " (the page: mitochondrion)"]
        for gap in (".dl-question-gap-select", ".dl-question-gap-input"):
            classes = page.get_attribute(f"{FIB} {gap}", "class") or ""
            assert "correct" not in classes
        text = page.inner_text(FIB).lower()
        for word in JUDGING:
            assert word not in text, word

    def test_the_gap_values_and_the_asking_survive_a_reload(self, page):
        page.select_option(f"{FIB} .dl-question-gap-select", label="right angle")
        page.fill(f"{FIB} .dl-question-gap-input", "mitochondrion")
        ask(page, FIB)
        page.wait_for_function("globalThis.dewlab.readSaved() !== null", timeout=10_000)

        page.reload()
        page.wait_for_function("() => !!globalThis.dewlab")
        assert page.eval_on_selector(f"{FIB} .dl-question-gap-input", "el => el.value") == "mitochondrion"
        assert page.locator(f"{FIB} .dl-question-page-word").count() == 2
