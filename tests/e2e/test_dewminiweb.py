"""dewmini web (compose/dewminiweb.html), in a real browser.

No Pyodide involved anywhere in this page — it runs no Python at all — so
unlike test_phase0_golden_path.py and test_dewmini_workbench.py, these
tests need no self-hosted Pyodide and serve the repository's own source
tree directly rather than a build.py output: compose/dewminiweb.html's
own links (`../assets/...`, `dewminiweb.js`) already resolve against the
real assets/ folder, the same files site/ would otherwise just copy in
unchanged (build.py's `shutil.copytree(COMPOSE, OUT / "compose")`).
"""
from __future__ import annotations

import functools
import http.server
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def dewminiweb_url():
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}/compose/dewminiweb.html"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def page(browser, dewminiweb_url):
    """A page with dewmini web loaded and its starter site already run.

    Exposes the same ``page.problems`` list conftest.py's own ``page``
    fixture does, for the same reason: one test here deliberately breaks
    a pane's script to check the friendly-hint path, so a page-wide "no
    problems" assertion belongs to the tests that expect a clean run, not
    to teardown (test_phase0_golden_path.py's own
    test_python_started_with_no_console_errors is the same shape).
    """
    context = browser.new_context()
    tab = context.new_page()

    problems: list[str] = []
    tab.on("pageerror", lambda err: problems.append(f"pageerror: {err}"))
    tab.on(
        "console",
        lambda msg: problems.append(f"console.{msg.type}: {msg.text}")
        if msg.type == "error"
        else None,
    )
    tab.problems = problems

    tab.goto(dewminiweb_url)
    tab.wait_for_selector(".dl-site-editor", timeout=15_000)

    yield tab

    context.close()


def frame(page):
    return page.query_selector(".dl-site-frame").content_frame()


def test_a_fresh_visit_shows_one_site_with_all_three_panes(page):
    assert page.locator(".dl-ws-list button").count() == 1
    assert page.locator(".dl-site-pane").count() == 3
    assert page.input_value("#dl-ws-name") == "Site 1"
    assert page.problems == []


def test_the_starter_script_has_already_run(page):
    """A reader opening dewmini web for the first time should see the
    starter working, not three empty boxes and a blank preview."""
    f = frame(page)
    f.wait_for_selector("h1", timeout=10_000)
    assert f.inner_text("h1") == "Hello"
    page.wait_for_function(
        "document.querySelector('#dl-ws-console').textContent.includes('The script ran')",
        timeout=5_000,
    )


def test_css_is_live_without_pressing_run(page):
    page.click('.dl-site-pane[data-lang="css"] .cm-content')
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("h1 { color: rgb(9, 9, 9); }")
    frame(page).wait_for_function(
        "getComputedStyle(document.querySelector('h1')).color === 'rgb(9, 9, 9)'",
        timeout=5_000,
    )


def test_new_site_starts_from_the_same_starter(page):
    page.click(".dl-ws-new")
    page.wait_for_function("document.querySelectorAll('.dl-ws-list button').length === 2")
    f = frame(page)
    f.wait_for_selector("h1", timeout=10_000)
    assert f.inner_text("h1") == "Hello"


def test_renaming_updates_the_download_filename(page):
    page.fill("#dl-ws-name", "My First Site")
    page.dispatch_event("#dl-ws-name", "input")
    page.wait_for_function(
        "document.getElementById('dl-ws-editor').dataset.siteName === 'my-first-site'"
    )


def test_switching_sites_keeps_each_ones_own_edits(page):
    page.click('.dl-site-pane[data-lang="css"] .cm-content')
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("h1 { color: rgb(1, 2, 3); }")
    frame(page).wait_for_function(
        "getComputedStyle(document.querySelector('h1')).color === 'rgb(1, 2, 3)'",
        timeout=5_000,
    )

    page.click(".dl-ws-new")
    page.wait_for_function("document.querySelectorAll('.dl-ws-list button').length === 2")
    frame(page).wait_for_function(
        "getComputedStyle(document.querySelector('h1')).color !== 'rgb(1, 2, 3)'",
        timeout=5_000,
    )

    page.click(".dl-ws-list button:has-text('Site 1')")
    frame(page).wait_for_function(
        "getComputedStyle(document.querySelector('h1')).color === 'rgb(1, 2, 3)'",
        timeout=5_000,
    )


def test_delete_needs_two_clicks(page):
    page.click(".dl-ws-new")
    page.wait_for_function("document.querySelectorAll('.dl-ws-list button').length === 2")
    page.click(".dl-ws-delete")
    assert "again" in page.inner_text(".dl-ws-delete").lower()
    assert page.locator(".dl-ws-list button").count() == 2, "one click must not delete anything"
    page.click(".dl-ws-delete")
    page.wait_for_function("document.querySelectorAll('.dl-ws-list button').length === 1")


def test_the_width_slider_resizes_the_preview_frame(page):
    page.fill("#dl-ws-width", "60")
    page.dispatch_event("#dl-ws-width", "input")
    assert page.eval_on_selector(".dl-site-frame", "el => el.style.width") == "60%"


def test_loading_a_file_replaces_the_matching_pane(page, tmp_path):
    loaded = tmp_path / "loaded.html"
    loaded.write_text("<h2>Loaded from a file</h2>")
    with page.expect_file_chooser() as chooser_info:
        page.click(".dl-ws-load")
    chooser_info.value.set_files([str(loaded)])
    f = frame(page)
    f.wait_for_selector("h2", timeout=5_000)
    assert f.inner_text("h2") == "Loaded from a file"


def test_a_js_error_shows_a_friendly_hint(page):
    page.click('.dl-site-pane[data-lang="js"] .cm-content')
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("undefinedThing.explode();")
    page.click(".dl-btn-site-run")
    page.wait_for_function(
        "document.getElementById('dl-ws-console').querySelector('.dl-error') !== null",
        timeout=10_000,
    )
    html = page.inner_html("#dl-ws-console")
    assert "dl-error-hint" in html
    assert "dl-site-goto" in html
