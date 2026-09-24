"""The Workspace (dewmini web) runs no Python, so these serve the repo's source tree directly rather than a build.py output — compose/workspace.html's links already resolve against the real assets/ folder."""
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
        yield f"http://127.0.0.1:{port}/compose/workspace.html"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.fixture()
def page(browser, dewminiweb_url):
    """Exposes ``page.problems`` like conftest.py's fixture does: one test here deliberately breaks a pane's script, so "no problems" is a per-test assertion, not a teardown check."""
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
    f = frame(page)
    f.wait_for_selector("h1", timeout=10_000)
    assert f.inner_text("h1") == "Hello"
    f.wait_for_function(
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


def _html_pane_text(page):
    return page.eval_on_selector(
        '.dl-site-pane[data-lang="html"] .cm-content', "el => el.innerText"
    )


def test_undo_after_switching_sites_cannot_bring_back_the_other_sites_code(page):
    page.click('.dl-site-pane[data-lang="html"] .cm-content')
    page.keyboard.press("Control+a")
    page.keyboard.insert_text("<h1>Site one's own</h1>")
    # Past CodeMirror's 500ms undo grouping, as a reader's pause would be;
    # sooner, one Ctrl+Z would undo the typing along with the switch.
    page.wait_for_timeout(700)

    page.click(".dl-ws-new")
    page.wait_for_function("document.querySelectorAll('.dl-ws-list button').length === 2")
    page.click('.dl-site-pane[data-lang="html"] .cm-content')
    page.keyboard.press("Control+z")
    page.wait_for_timeout(400)  # past the 150ms debounced save

    assert "Site one's own" not in _html_pane_text(page)
    saved = page.evaluate(
        "JSON.parse(localStorage.getItem('dewminiweb:sites:v1')).sites.map(s => s.html)"
    )
    assert "Site one's own" not in saved[1]


def test_switching_sites_never_runs_the_previous_sites_script(page):
    page.click('.dl-site-pane[data-lang="js"] .cm-content')
    page.keyboard.press("Control+a")
    page.keyboard.insert_text('console.log("site one script");')
    page.click(".dl-btn-site-run")
    page.wait_for_function(
        "document.getElementById('dl-ws-console').textContent.includes('site one script')"
    )
    page.evaluate(
        """() => {
            window.__docs = [];
            const f = document.getElementById('dl-ws-frame');
            new MutationObserver(() => window.__docs.push(f.srcdoc))
                .observe(f, { attributes: true, attributeFilter: ['srcdoc'] });
        }"""
    )
    page.click(".dl-ws-new")
    page.wait_for_function(
        "document.getElementById('dl-ws-console').textContent.includes('The script ran')",
        timeout=5_000,
    )
    docs = page.evaluate("window.__docs")
    assert docs and not any("site one script" in d for d in docs)


def test_picking_a_site_from_the_keyboard_keeps_focus_on_it(page):
    page.click(".dl-ws-new")
    page.wait_for_function("document.querySelectorAll('.dl-ws-list button').length === 2")
    page.focus(".dl-ws-list li:first-child button")
    page.keyboard.press("Enter")
    page.wait_for_function("document.querySelector('.dl-ws-current').textContent === 'Site 1'")
    assert page.evaluate(
        "document.activeElement === document.querySelector('.dl-ws-current')"
    )


def test_an_emptied_name_box_shows_the_name_the_site_kept(page):
    page.fill("#dl-ws-name", "")
    page.focus(".dl-ws-new")  # leaving the box
    assert page.input_value("#dl-ws-name") == "Site 1"
    assert page.inner_text(".dl-ws-list button") == "Site 1"


def test_delete_removes_the_site_on_screen_even_if_the_saved_open_id_is_stale(
    page, dewminiweb_url
):
    page.wait_for_timeout(400)  # let the first visit's own save land first
    page.evaluate(
        """localStorage.setItem('dewminiweb:sites:v1', JSON.stringify({
            active: 'gone',
            sites: [
                {id: 'a', name: 'Shown', html: '', css: '', js: ''},
                {id: 'b', name: 'Kept', html: '', css: '', js: ''},
            ],
        }))"""
    )
    page.goto(dewminiweb_url)
    page.wait_for_selector(".dl-ws-current", timeout=5_000)
    assert page.input_value("#dl-ws-name") == "Shown"
    page.click(".dl-ws-delete")
    page.click(".dl-ws-delete")
    page.wait_for_function("document.querySelectorAll('.dl-ws-list button').length === 1")
    assert page.inner_text(".dl-ws-list button") == "Kept"
