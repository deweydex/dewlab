"""dewmini and dewmini web became the Notebook and the Workspace, and their
pages moved to compose/notebook.html and compose/workspace.html. Teachers
have bookmarks and links to the old addresses, so those still open the
right page. Served from the repo's source tree, like test_dewminiweb.py:
the redirect is a plain file in compose/, and nothing here runs Python."""
from __future__ import annotations

import functools
import http.server
import re
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

MOVED = [
    ("dewmini.html", "notebook.html", "dewlab Notebook"),
    ("dewminiweb.html", "workspace.html", "dewlab Workspace"),
]


@pytest.fixture(scope="module")
def compose_url():
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}/compose"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.mark.parametrize("old, new, title", MOVED)
def test_an_old_address_opens_the_new_page_keeping_its_query_and_hash(
    browser, compose_url, old, new, title
):
    context = browser.new_context()
    tab = context.new_page()
    try:
        tab.goto(f"{compose_url}/{old}?from=bookmark#somewhere", wait_until="commit")
        tab.wait_for_url(re.compile(re.escape(new)), timeout=10_000)
        assert tab.url == f"{compose_url}/{new}?from=bookmark#somewhere"
        tab.wait_for_selector("h1", timeout=10_000)
        assert tab.inner_text("h1") == title
        assert title in tab.title()
        # location.replace(): the redirect leaves no entry of its own, so
        # Back goes to where the reader came from (the tab's about:blank
        # here) rather than to a page that only sends them forward again.
        assert tab.evaluate("history.length") == 2
    finally:
        context.close()


@pytest.mark.parametrize("old, new, title", MOVED)
def test_an_old_address_still_opens_the_new_page_without_javascript(
    browser, compose_url, old, new, title
):
    context = browser.new_context(java_script_enabled=False)
    tab = context.new_page()
    try:
        tab.goto(f"{compose_url}/{old}", wait_until="commit")
        tab.wait_for_url(f"{compose_url}/{new}", timeout=10_000)
        tab.wait_for_selector("h1", timeout=10_000)
        assert tab.inner_text("h1") == title
    finally:
        context.close()
