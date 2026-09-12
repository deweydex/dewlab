"""E2E fixtures: build the fixture tutorial with build.py and serve it with a self-hosted Pyodide, so tests run the real build and execution path."""

from __future__ import annotations

import functools
import re
import http.server
import shutil
import socketserver
import sys
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]
PYODIDE = DEWLAB / "dev" / "pyodide"
FIXTURE_DIR = Path(__file__).resolve().parent / "fixture"
FIXTURE = FIXTURE_DIR / "rendering-tour.md"

sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402

MODULE = "fixtures"
SLUG = "rendering-tour"
PAGE = f"tutorials/{MODULE}/{SLUG}.html"
UP = "../../"  # from the built page back to the site root


@pytest.fixture(scope="session")
def site_dir(tmp_path_factory) -> Path:
    if not (PYODIDE / "pyodide.mjs").exists():
        pytest.skip(
            "no self-hosted Pyodide — run `python3 dev/fetch_pyodide.py` first"
        )

    root = tmp_path_factory.mktemp("dewlab-e2e")
    (root / "tutorials" / MODULE).mkdir(parents=True)
    # rglob rather than glob: a tutorial with more than one release lives in a
    # folder of its own, and the picker only exists on one of those.
    for source in sorted(FIXTURE_DIR.rglob("*.md")):
        into = root / "tutorials" / MODULE / source.relative_to(FIXTURE_DIR)
        into.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source, into)
    for source in sorted(FIXTURE_DIR.glob("*.order.yaml")):
        shutil.copy(source, root / "tutorials" / MODULE / source.name)
    for source in sorted(FIXTURE_DIR.glob("*.glossary.yaml")):
        shutil.copy(source, root / "tutorials" / MODULE / source.name)
    shutil.copytree(DEWLAB / "assets", root / "assets")
    shutil.copytree(DEWLAB / "data", root / "data")
    # The topic tree is built from the curriculum data, and its behaviour —
    # panning, zooming, choosing a topic — only exists in a browser.
    shutil.copytree(DEWLAB / "planning" / "curriculum", root / "planning" / "curriculum")
    groups = root / "planning" / "curriculum" / "topic-groups.yaml"
    groups.write_text(
        groups.read_text()
        + "  - key: e2e-fixtures\n"
          "    name: Fixtures\n"
          "    intro: The e2e fixture's own pages, so the topic filter has a group.\n"
          "    tutorials:\n"
          f"      - {{ module: {MODULE}, slug: third-page }}\n"
    )

    out = root / "site"
    for name, value in {
        "ROOT": root,
        "TUTORIALS": root / "tutorials",
        "SETUP": root / "setup",
        "DATA": root / "data",
        "ASSETS": root / "assets",
        "SHELL": root / "assets" / "shell.html",
        "OUT": out,
        "TOPIC_DATA": root / "planning" / "curriculum" / "topics.yaml",
        "TOPIC_GROUPS_DATA": root / "planning" / "curriculum" / "topic-groups.yaml",
        "OUTCOME_DATA": root / "planning" / "curriculum" / "outcomes.yaml",
    }.items():
        setattr(b, name, value)
    b.build(clean=True)

    # Point the runtime at the Pyodide staged in this tree rather than the CDN,
    # which is what a network with no route to jsdelivr would also have to do.
    page = out / PAGE
    html = page.read_text()
    # The URL carries a content hash, so match the shape rather than the string.
    found = re.search(
        rf'<script type="module" src="{re.escape(UP)}assets/tutorial-runtime\.js[^"]*">'
        r"</script>",
        html,
    )
    assert found, "the built page no longer loads the runtime as this expects"
    original = found.group(0)
    page.write_text(
        html.replace(
            original,
            f'<script>globalThis.DEWLAB_PYODIDE_BASE = "{UP}pyodide/";</script>\n'
            + original,
        )
    )

    shutil.copytree(PYODIDE, out / "pyodide")
    return out


@pytest.fixture(scope="session")
def base_url(site_dir: Path):
    # Served over HTTP, not file://, because the runtime's ES module imports
    # need an origin for the browser's CORS check to approve.
    handler = functools.partial(_QuietHandler, directory=str(site_dir))
    with _QuietServer(("127.0.0.1", 0), handler) as server:
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{port}"
        finally:
            server.shutdown()
            thread.join(timeout=5)


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        """No per-request logging; a Pyodide boot is a few hundred requests."""


class _QuietServer(socketserver.TCPServer):
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        """Closing the browser resets connections mid-response — normal teardown, not a failure, so its traceback is suppressed."""


@pytest.fixture(scope="session")
def browser():
    playwright = pytest.importorskip(
        "playwright.sync_api", reason="playwright is not installed"
    )
    with playwright.sync_playwright() as driver:
        candidate = _chromium_path()
        launch = {"args": ["--no-sandbox"]}
        if candidate:
            launch["executable_path"] = candidate
        instance = driver.chromium.launch(**launch)
        try:
            yield instance
        finally:
            instance.close()


def _chromium_path() -> str | None:
    # Reuses this project's CI/dev Chromium instead of triggering Playwright's
    # own network-dependent browser download.
    root = Path("/opt/pw-browsers")
    if not root.exists():
        return None
    for chrome in sorted(root.glob("chromium-*/chrome-linux/chrome")):
        return str(chrome)
    return None


@pytest.fixture()
def page(browser, base_url):
    """A page with the built tutorial loaded and Python already started."""
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

    tab.goto(f"{base_url}/{PAGE}")
    # Pyodide plus three packages is a slow first load, and deliberately so:
    # it happens once per page, not once per cell.
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    tab.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
        timeout=240_000,
    )
    problems.clear()
    try:
        yield tab
    finally:
        context.close()
