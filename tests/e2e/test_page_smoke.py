"""The cheapest real check there is: does this page load in a browser at
all, with no console errors, and does it fit on a phone screen without
scrolling sideways. Every page template build.py writes gets one visit here
-- before this file, four of roughly ten templates ever got a browser at
all (the rest -- about, features, a practice page, the topics/pair-game
page -- had zero live coverage of any kind, not just no scroll check).

Retires test_narrow_screen.py, whose two tests (a tutorial page and the
home page, at phone width) are two of the cases parametrized below."""

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

COURSE = "page-smoke-fixtures"

ONE = """---
title: "One"
year: "2026-2027"
version: 2026.08.23.1
---

# One

Some prose, so this page has something to read.
"""

TWO = """---
title: "Two"
year: "2026-2027"
version: 2026.08.23.1
---

# Two

More prose.
"""

PRACTICE = """---
title: "One, practice"
year: "2026-2027"
version: 2026.08.23.1
practice_for: one
---

# One, practice

**1.** A question.
"""


# write_topics_page() ("browse by topic") skips writing the page entirely
# if no group it's given resolves to a real tutorial -- the real
# topic-groups.yaml won't name this fixture's own tutorials, so it gets
# one group of its own rather than depending on real curriculum content.
TOPIC_GROUPS = """groups:
  - key: page-smoke-fixtures
    name: Fixtures
    intro: This group exists only so topics.html has something to render.
    tutorials:
      - one
"""


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("page-smoke")
    (tmp_path / "tutorials").mkdir(parents=True)
    write_tutorial(tmp_path, "one", ONE)
    write_tutorial(tmp_path, "two", TWO)
    (tmp_path / "tutorials" / "one" / "one-practice.md").write_text(PRACTICE)
    write_course(tmp_path, COURSE, "Sample Series", ["one", "two"])

    (tmp_path / "curriculum").mkdir()
    topic_groups_path = tmp_path / "curriculum" / "topic-groups.yaml"
    topic_groups_path.write_text(TOPIC_GROUPS)

    original = {name: getattr(b, name) for name in (
        "ROOT", "TUTORIALS", "COURSES", "OUT", "SETUP", "DATA", "ASSETS",
        "SHELL", "PAGES", "TOPIC_DATA", "TOPIC_GROUPS_DATA", "OUTCOME_DATA",
    )}
    b.ROOT = tmp_path
    b.TUTORIALS = tmp_path / "tutorials"
    b.COURSES = tmp_path / "courses"
    b.OUT = tmp_path / "site"
    b.SETUP = DEWLAB / "setup"
    b.DATA = DEWLAB / "data"
    b.ASSETS = DEWLAB / "assets"
    b.SHELL = DEWLAB / "assets" / "shell.html"
    # The real project's own pages and outcomes/tree data, read-only --
    # this fixture's own tutorials don't need to correspond to any of it
    # for the home/about/features/tree pages to load and lay out
    # correctly (only topics.html actually gates on a group resolving,
    # hence its own small file above).
    b.PAGES = DEWLAB / "pages"
    b.TOPIC_DATA = DEWLAB / "planning" / "curriculum" / "topics.yaml"
    b.TOPIC_GROUPS_DATA = topic_groups_path
    b.OUTCOME_DATA = DEWLAB / "planning" / "curriculum" / "outcomes.yaml"
    try:
        b.build()
    finally:
        for name, value in original.items():
            setattr(b, name, value)
    return tmp_path


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="module")
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


PAGES = [
    "index.html",
    "about.html",
    "features.html",
    "all-tutorials.html",
    "all-notes.html",
    f"{COURSE}.html",
    "tree.html",
    "topics.html",
    "tutorials/one.html",
    "tutorials/one-practice.html",
]


@pytest.mark.parametrize("path", PAGES)
def test_a_page_loads_with_no_console_errors(site_url, browser, path):
    context = browser.new_context()
    page = context.new_page()
    problems: list[str] = []
    page.on("pageerror", lambda err: problems.append(f"pageerror: {err}"))
    page.on(
        "console",
        lambda msg: problems.append(f"console.{msg.type}: {msg.text}")
        if msg.type == "error" else None,
    )
    page.goto(f"{site_url}/{path}")
    page.wait_for_load_state("networkidle")
    context.close()
    assert problems == [], f"{path}: {problems}"


@pytest.mark.parametrize("path", PAGES)
def test_a_page_never_scrolls_sideways_on_a_phone(site_url, browser, path):
    context = browser.new_context(viewport={"width": 375, "height": 700}, is_mobile=True, has_touch=True)
    page = context.new_page()
    page.goto(f"{site_url}/{path}")
    page.wait_for_load_state("networkidle")
    overflow = page.evaluate(
        "document.documentElement.scrollWidth - document.documentElement.clientWidth"
    )
    context.close()
    assert overflow <= 1, f"{path} scrolls sideways on a phone: {overflow}px over"


def test_a_failure_message_wraps_instead_of_widening_the_page(site_url, browser):
    """Guards against a compounding failure: a network error's text carries
    a URL, which must not also widen the page."""
    context = browser.new_context(viewport={"width": 375, "height": 700}, is_mobile=True, has_touch=True)
    page = context.new_page()
    page.goto(f"{site_url}/tutorials/one.html")
    page.wait_for_selector("#dl-body")
    overflow = page.evaluate("""() => {
      const status = document.getElementById('dl-status');
      status.classList.add('dl-status-error');
      status.hidden = false;
      status.textContent = 'Python failed to start: Failed to fetch '
        + 'dynamically imported module: '
        + 'https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.mjs. '
        + 'Reloading the page usually fixes it.';
      return {inBody: document.getElementById('dl-body').contains(status),
              sw: status.scrollWidth, cw: status.clientWidth,
              page: document.documentElement.scrollWidth,
              client: document.documentElement.clientWidth};
    }""")
    context.close()
    assert overflow["inBody"] is False, (
        "this test only means anything while #dl-status sits outside #dl-body")
    assert overflow["sw"] <= overflow["cw"] + 1, "the error message itself overflows"
    assert overflow["page"] <= overflow["client"] + 1, "the error widened the page"
