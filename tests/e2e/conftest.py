"""Fixtures for the e2e tests: a built harness page and a server to hold it.

These tests drive a real Chromium against a real Pyodide, because that is the
only way to know the execution path actually works. They need two things the
unit tests don't:

  * Playwright with a Chromium (`pip install playwright && playwright install
    chromium`);
  * a self-hosted Pyodide in `dev/pyodide/` (`python3 dev/fetch_pyodide.py`).

Missing either, the tests skip with a message saying which. Self-hosting rather
than using the CDN keeps the suite runnable on a machine with no route to
jsdelivr, and exercises the same DEWLAB_PYODIDE_BASE override that a
CDN-blocked school network would need.
"""

from __future__ import annotations

import functools
import http.server
import shutil
import socketserver
import subprocess
import sys
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]
HARNESS = DEWLAB / "dev" / "harness"
PYODIDE = DEWLAB / "dev" / "pyodide"

RUNTIME_OVERRIDE = (
    '<script>globalThis.DEWLAB_PYODIDE_BASE = "pyodide/";</script>\n'
    '<script type="module" src="assets/tutorial-runtime.js"></script>'
)


@pytest.fixture(scope="session")
def harness_dir() -> Path:
    """Build the harness page and stage a local Pyodide beside it."""
    if not (PYODIDE / "pyodide.mjs").exists():
        pytest.skip(
            "no self-hosted Pyodide — run `python3 dev/fetch_pyodide.py` first"
        )

    subprocess.run(
        [sys.executable, str(DEWLAB / "dev" / "make_harness.py")],
        check=True,
        capture_output=True,
    )

    page = HARNESS / "index.html"
    html = page.read_text()
    original = '<script type="module" src="assets/tutorial-runtime.js"></script>'
    assert original in html, "harness no longer loads the runtime the way this expects"
    page.write_text(html.replace(original, RUNTIME_OVERRIDE))

    served = HARNESS / "pyodide"
    if served.exists():
        shutil.rmtree(served)
    shutil.copytree(PYODIDE, served)

    return HARNESS


@pytest.fixture(scope="session")
def base_url(harness_dir: Path):
    """Serve the harness on a free port for the duration of the session."""
    handler = functools.partial(_QuietHandler, directory=str(harness_dir))
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
        """Closing the browser resets connections mid-response. That is normal
        teardown, not a test failure, and its traceback is pure noise in an
        otherwise passing run."""


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
    """Use a preinstalled Chromium if one is on this machine."""
    root = Path("/opt/pw-browsers")
    if not root.exists():
        return None
    for chrome in sorted(root.glob("chromium-*/chrome-linux/chrome")):
        return str(chrome)
    return None


@pytest.fixture()
def page(browser, base_url):
    """A page with the harness loaded and Python already started."""
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

    tab.goto(f"{base_url}/index.html")
    # Pyodide plus three packages is a slow first load, and deliberately so:
    # it happens once per page, not once per cell.
    tab.wait_for_function("globalThis.dewlab !== undefined", timeout=30_000)
    tab.wait_for_function(
        "document.querySelectorAll('.dl-btn-run:not([disabled])').length > 0",
        timeout=240_000,
    )
    try:
        yield tab
    finally:
        context.close()
