"""Toolkit cells in a real browser against a real Pyodide: a course of two
pages, the first with a toolkit cell (a stub, plus a reference fence), the
second with a cell that calls the function. What the second page loads
depends on what the reader saved on the first and on the toolkit mode
(build.py's toolkit_for(), tutorial-runtime.js's loadToolkit(),
tutorial_tools._load_toolkit()).

A site of its own, built per test, so nothing here changes a page another
test uses."""

from __future__ import annotations

import functools
import http.server
import json
import re
import socketserver
import sys
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]
PYODIDE = DEWLAB / "dev" / "pyodide"
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402
from layout import write_course, write_tutorial  # noqa: E402

COURSE = "toolkit-fixtures"

FIRST = """---
title: "Numbers in binary"
year: "2026-2027"
version: 2026.09.24.1
---

# Numbers in binary

```python exec
id: toolkit-binary
toolkit: yes
def to_binary(n):
    '''Turn n into a string of 0s and 1s.'''
    ...

def to_hex(n):
    '''Turn n into hexadecimal.'''
    ...
```

```python toolkit-reference
for: toolkit-binary
print("this line is never shown")
def to_binary(n):
    return "ref:" + bin(n)[2:]

def to_hex(n):
    return "ref:" + format(n, "x")

to_hex(4096)
```
"""

SECOND = """---
title: "Using binary"
year: "2026-2027"
version: 2026.09.24.1
---

# Using binary

```python exec
id: use-binary
print(to_binary(5))
```

```python exec
id: use-hex
print(to_hex(255))
```

```python exec
id: second-cell
print("second")
```
"""

MINE = ('def to_binary(n):\n    return "mine:" + format(n, "b")\n\n'
        'def to_hex(n):\n    """Turn n into hexadecimal."""\n    ...\n')
RAISES = 'def to_binary(n):\n    return "broken"\nraise ValueError("not finished")'


@pytest.fixture()
def site(tmp_path, monkeypatch):
    if not (PYODIDE / "pyodide.mjs").exists():
        pytest.skip("no self-hosted Pyodide — run `python3 dev/fetch_pyodide.py` first")
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, "tk-first", FIRST)
    write_tutorial(tmp_path, "tk-second", SECOND)
    write_course(tmp_path, COURSE, "Toolkit", ["tk-first", "tk-second"])
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "COURSES", tmp_path / "courses")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
    b.build()

    (tmp_path / "site" / "pyodide").symlink_to(PYODIDE)
    for slug in ("tk-first", "tk-second"):
        page_path = tmp_path / "site" / "tutorials" / f"{slug}.html"
        html = page_path.read_text()
        found = re.search(
            r'<script type="module" src="\.\./assets/tutorial-runtime\.js[^"]*"></script>', html)
        assert found, "the built page no longer loads the runtime as this expects"
        page_path.write_text(html.replace(
            found.group(0),
            '<script>globalThis.DEWLAB_PYODIDE_BASE = "../pyodide/";</script>\n' + found.group(0),
        ))
    return tmp_path


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class _QuietServer(socketserver.TCPServer):
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        """A reload mid-boot resets connections; that is not a failure."""


@pytest.fixture()
def site_url(site):
    handler = functools.partial(_QuietHandler, directory=str(site / "site"))
    server = _QuietServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def tab(browser):
    context = browser.new_context()
    page = context.new_page()
    page.on("dialog", lambda dialog: dialog.accept())
    yield page
    context.close()


def _saved_on_first(code: str) -> str:
    """The first page's saved work, as saveNow() writes it."""
    return json.dumps({
        "tutorial-id": "tk-first",
        "tutorial-slug": "tk-first",
        "tutorial-version": "2026.09.24.1",
        "cells": [{"task_id": "toolkit-binary", "student_code": code, "output_html": ""}],
    })


def _open_second(tab, site_url, saved: str | None = None, mode: str | None = None):
    tab.goto(f"{site_url}/tutorials/tk-second.html")
    tab.evaluate("localStorage.clear()")
    if saved is not None:
        tab.evaluate("(v) => localStorage.setItem('dewlab:progress:tk-first', v)", saved)
    if mode is not None:
        tab.evaluate("(v) => localStorage.setItem('dewlab:toolkit-mode', v)", mode)
    tab.reload()
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    tab.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
        timeout=240_000,
    )


def _run_and_read(tab, cell_id: str = "use-binary") -> str:
    tab.evaluate("(id) => globalThis.dewlab.runCell(id)", cell_id)
    return tab.text_content(f'.dl-cell[data-cell-id="{cell_id}"] .dl-output').strip()


def _line(tab) -> str:
    return " ".join(tab.text_content(".dl-toolkit-text").split())


def test_with_nothing_saved_the_reference_is_loaded(tab, site_url):
    _open_second(tab, site_url)
    assert _run_and_read(tab) == "ref:101"
    assert _run_and_read(tab, "use-hex") == "ref:ff"
    assert _line(tab) == ("Your toolkit has to_binary and to_hex. It comes from 1 earlier page. "
                          "You have not written any of these yet, so the reference ones "
                          "are loaded.")
    # The reference's own print went nowhere.
    assert "never shown" not in tab.text_content("#dl-body")
    assert "ref:1000" not in tab.text_content("#dl-body")
    # The line sits just above the first cell, and My code is the default.
    assert tab.evaluate(
        "document.querySelector('.dl-toolkit').nextElementSibling.dataset.cellId") == "use-binary"
    assert tab.is_checked("input[name='dl-toolkit-mode'][value='mine']")


def test_the_readers_saved_version_is_loaded_function_by_function(tab, site_url):
    # The reader wrote to_binary and left to_hex as the page gave it.
    _open_second(tab, site_url, saved=_saved_on_first(MINE))
    assert _run_and_read(tab) == "mine:101"
    assert _run_and_read(tab, "use-hex") == "ref:ff"
    assert _line(tab) == ("Your toolkit has to_binary and to_hex. It comes from 1 earlier page. "
                          "You have not written to_hex yet, so the reference one is loaded.")


def test_an_untouched_stub_counts_as_not_written(tab, site_url):
    # What saveNow() stores for a reader who opened the page and wrote nothing.
    stub = FIRST.split("toolkit: yes\n", 1)[1].split("```", 1)[0]
    _open_second(tab, site_url, saved=_saved_on_first(stub))
    assert _run_and_read(tab) == "ref:101"
    assert _run_and_read(tab, "use-hex") == "ref:ff"
    assert ("You have not written any of these yet, so the reference ones are loaded."
            in _line(tab))


def test_a_saved_version_that_raises_falls_back_and_the_line_says_so(tab, site_url):
    _open_second(tab, site_url, saved=_saved_on_first(RAISES))
    assert _run_and_read(tab) == "ref:101"
    assert ("to_binary and to_hex: your version raised an error, so the reference ones "
            "are loaded." in _line(tab))


def test_switching_to_reference_loads_the_reference_at_once(tab, site_url):
    _open_second(tab, site_url, saved=_saved_on_first(MINE))
    assert _run_and_read(tab) == "mine:101"
    tab.check("input[name='dl-toolkit-mode'][value='reference']")
    assert tab.evaluate("localStorage.getItem('dewlab:toolkit-mode')") == "reference"
    assert _run_and_read(tab) == "ref:101"
    tab.check("input[name='dl-toolkit-mode'][value='mine']")
    assert _run_and_read(tab) == "mine:101"


def test_the_reference_mode_is_remembered_across_pages(tab, site_url):
    _open_second(tab, site_url, saved=_saved_on_first(MINE), mode="reference")
    assert tab.is_checked("input[name='dl-toolkit-mode'][value='reference']")
    assert _run_and_read(tab) == "ref:101"


def test_the_toolkit_survives_run_all_and_a_restart(tab, site_url):
    _open_second(tab, site_url, saved=_saved_on_first(MINE))
    # "Run this cell and all above" clears the namespace before it runs.
    tab.evaluate("(id) => document.querySelector("
                 "`.dl-cell[data-cell-id='${id}'] [data-run-menu='above']`).click()",
                 "second-cell")
    tab.wait_for_function(
        "document.querySelector('.dl-cell[data-cell-id=\"second-cell\"] .dl-output')"
        ".textContent.includes('second')", timeout=60_000)
    assert tab.text_content('.dl-cell[data-cell-id="use-binary"] .dl-output').strip() == "mine:101"

    # Restart & run all: a fresh interpreter, then every cell from the top.
    tab.evaluate("document.querySelectorAll('.dl-output').forEach((el) => el.replaceChildren())")
    tab.evaluate("document.getElementById('dl-restart-run-all').click()")
    tab.wait_for_function(
        "document.querySelector('.dl-cell[data-cell-id=\"second-cell\"] .dl-output')"
        ".textContent.includes('second')", timeout=240_000)
    assert tab.text_content('.dl-cell[data-cell-id="use-binary"] .dl-output').strip() == "mine:101"
    assert _line(tab).startswith("Your toolkit has to_binary and to_hex.")
