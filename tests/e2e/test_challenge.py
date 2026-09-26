"""A closer's challenge (#316), on the fixture's `a-challenge` page: a
Python starter for the Notebook, and an HTML, CSS and JS starter for the
Workspace.

The link carries the starter in its address. The Notebook and the
Workspace each open it as a new tab named after the page, beside what the
reader already has and never over it. A downloaded page, with neither
beside it, offers the starter as a file to save instead."""

from __future__ import annotations

import json
import urllib.parse

import pytest

from test_compare import _open, _serve
from test_dewmini_workbench import dewmini_url  # noqa: F401  (points the Notebook at local Pyodide)

PAGE = "tutorials/a-challenge.html"
CODE = "# A running total that never goes below zero.\nchanges = [5, -3, -4, 6]\ntotal = 0"


@pytest.fixture(params=["hosted", "downloaded"])
def tab(request, browser, base_url, site_dir):
    route = _serve(site_dir, standalone=request.param == "downloaded", path=PAGE)
    context, tab = _open(browser, f"{base_url}/{PAGE}", route, page=PAGE)
    tab.kind = request.param
    try:
        yield tab
    finally:
        context.close()


def box(tab, target):
    return tab.locator(f".dl-challenge[data-target='{target}']")


def starter(href: str) -> dict:
    return json.loads(urllib.parse.unquote(href.split("#challenge=", 1)[1]))


def test_the_starter_travels_in_the_link_or_saves_as_a_file(tab):
    notebook, workspace = box(tab, "notebook"), box(tab, "workspace")
    if tab.kind == "hosted":
        link = notebook.locator(".dl-challenge-open")
        assert link.inner_text() == "Open it in the Notebook"
        assert notebook.locator(".dl-challenge-save").is_hidden()
        href = link.get_attribute("href")
        assert href.startswith("../compose/notebook.html#challenge=")
        assert starter(href) == {"name": "a-challenge", "page": "A challenge to take away",
                                 "code": CODE}
        href = workspace.locator(".dl-challenge-open").get_attribute("href")
        assert href.startswith("../compose/workspace.html#challenge=")
        assert starter(href)["css"] == "#total { font-size: 2rem; }"
        return
    # A downloaded page has no Notebook beside it.
    assert notebook.locator(".dl-challenge-open").is_hidden()
    with tab.expect_download() as download:
        notebook.locator(".dl-challenge-save").click()
    assert download.value.suggested_filename == "a-challenge.py"
    assert open(download.value.path()).read() == CODE + "\n"
    with tab.expect_download() as download:
        workspace.locator(".dl-challenge-save").click()
    assert download.value.suggested_filename == "a-challenge.html"
    page = open(download.value.path()).read()
    assert "<style>\n#total { font-size: 2rem; }\n</style>" in page
    assert '<p id="total">0</p>' in page and "textContent = 5" in page


def link_to(browser, base_url, site_dir, target):
    route = _serve(site_dir, standalone=False, path=PAGE)
    context, tab = _open(browser, f"{base_url}/{PAGE}", route, page=PAGE)
    href = box(tab, target).locator(".dl-challenge-open").get_attribute("href")
    context.close()
    return urllib.parse.urljoin(f"{base_url}/{PAGE}", href)


def test_the_notebook_opens_it_beside_what_is_there(browser, base_url, site_dir, dewmini_url):  # noqa: F811
    url = link_to(browser, base_url, site_dir, "notebook")
    context = browser.new_context()
    tab = context.new_page()
    try:
        tab.goto(dewmini_url)
        # A tab of the reader's own, already named after the page.
        tab.evaluate("""() => localStorage.setItem('dewmini:notebooks:v1', JSON.stringify({
            active: 'nb-mine', notebooks: [{id: 'nb-mine', name: 'a-challenge', view: 'cells',
              cells: [{id: 'c1', type: 'python', content: 'my own work'}]}]}))""")
        # A fresh load, so the Notebook reads what was just stored.
        tab.goto("about:blank")
        tab.goto(url)
        tab.wait_for_selector(".dm-toolbar")
        tab.wait_for_function("!location.hash")
        saved = tab.evaluate("JSON.parse(localStorage.getItem('dewmini:notebooks:v1'))")
        names = [nb["name"] for nb in saved["notebooks"]]
        assert names == ["a-challenge", "a-challenge 2"]
        assert saved["notebooks"][0]["cells"][0]["content"] == "my own work"
        assert saved["notebooks"][1]["cells"][0]["content"] == CODE
        assert saved["active"] == saved["notebooks"][1]["id"]
        # The same link again, followed in the open Notebook, goes back to
        # that tab rather than making a third.
        tab.goto(url)
        tab.wait_for_selector(".dm-toolbar")
        tab.wait_for_function("!location.hash")
        saved = tab.evaluate("JSON.parse(localStorage.getItem('dewmini:notebooks:v1'))")
        assert [nb["name"] for nb in saved["notebooks"]] == ["a-challenge", "a-challenge 2"]
    finally:
        context.close()


def test_the_workspace_opens_it_as_a_site_of_its_own(browser, base_url, site_dir):
    url = link_to(browser, base_url, site_dir, "workspace")
    context = browser.new_context()
    tab = context.new_page()
    try:
        tab.goto(url)
        tab.wait_for_function("!location.hash")
        saved = tab.evaluate("JSON.parse(localStorage.getItem('dewminiweb:sites:v1'))")
        site = next(s for s in saved["sites"] if s["name"] == "a-challenge")
        assert site["html"] == '<p id="total">0</p>'
        assert site["js"] == 'document.getElementById("total").textContent = 5;'
        assert saved["active"] == site["id"]
        assert len(saved["sites"]) == 2  # the Workspace's own first site, and this
        tab.goto(url)
        tab.wait_for_function("!location.hash")
        saved = tab.evaluate("JSON.parse(localStorage.getItem('dewminiweb:sites:v1'))")
        assert [s["name"] for s in saved["sites"]].count("a-challenge") == 1
    finally:
        context.close()
