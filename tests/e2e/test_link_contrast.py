"""Link colour against its background, measured rather than eyeballed.

The rule this file protects: **body-sized text meets WCAG AA, 4.5:1.**

Links are most of the text on the contents page, and the brand orange
was 3.5:1 on the light background — under the ordinary AA minimum, for
the reader planning/PEDAGOGICAL_STYLE_GUIDE.md section 1 describes. The
High contrast toggle already fixed it there; the default did not.

No single value serves both themes. The brand orange is 4.96:1 on the
dark background and fails on light; a value dark enough for light drops
to 3.66:1 on dark. So the stylesheet carries one per theme, and this
checks both.

    python3 -m pytest tests/e2e/test_link_contrast.py -q
"""

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

MODULE = "contrast-fixtures"

TUTORIAL = """---
title: "Contrast"
slug: contrast
module: contrast-fixtures
module_title: "Contrast Fixtures"
year: "2026-2027"
series: contrast-series
version: 2026.08.30.1
---

# Contrast

Prose with [a link](https://example.org) in it.
"""


def relative_luminance(rgb):
    def channel(value):
        v = value / 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, bl = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * bl


def contrast_ratio(fg, bg):
    """WCAG's own formula, so the number here is the number that is cited."""
    high, low = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def parse_rgb(value):
    inner = value[value.index("(") + 1:value.index(")")]
    return tuple(int(float(part)) for part in inner.split(",")[:3])


@pytest.fixture()
def site(tmp_path, monkeypatch):
    (tmp_path / "tutorials" / MODULE).mkdir(parents=True)
    monkeypatch.setattr(b, "ROOT", tmp_path)
    monkeypatch.setattr(b, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(b, "OUT", tmp_path / "site")
    monkeypatch.setattr(b, "SETUP", DEWLAB / "setup")
    monkeypatch.setattr(b, "DATA", DEWLAB / "data")
    monkeypatch.setattr(b, "ASSETS", DEWLAB / "assets")
    monkeypatch.setattr(b, "SHELL", DEWLAB / "assets" / "shell.html")
    folder = tmp_path / "tutorials" / MODULE / "contrast"
    folder.mkdir(parents=True)
    (folder / "contrast.md").write_text(TUTORIAL)
    # The reading order lives beside the series, not in frontmatter.
    (tmp_path / "tutorials" / MODULE / "contrast-series.order.yaml").write_text(
        "order:\n  - contrast\n"
    )
    b.build()
    return tmp_path


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture()
def base_url(site):
    handler = functools.partial(_QuietHandler, directory=str(site / "site"))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_a_link_meets_aa_against_its_own_background(browser, base_url, scheme):
    page = browser.new_page(color_scheme=scheme)
    try:
        # A link in the tutorial's own prose, not the first anchor on the
        # page: that one is the header wordmark, which takes its colour
        # from --dl-fg and passes whatever --dl-link is doing.
        page.goto(f"{base_url}/tutorials/{MODULE}/contrast.html")
        page.wait_for_selector('a[href="https://example.org"]')
        measured = page.evaluate(
            """() => {
              const link = document.querySelector('a[href="https://example.org"]');
              return {
                color: getComputedStyle(link).color,
                size: parseFloat(getComputedStyle(link).fontSize),
                background: getComputedStyle(document.body).backgroundColor,
              };
            }"""
        )
        ratio = contrast_ratio(parse_rgb(measured["color"]), parse_rgb(measured["background"]))
        # 4.5 is the AA minimum for text below 24px (or 18.66px bold).
        assert measured["size"] < 24
        assert ratio >= 4.5, (
            f"{scheme}: link {measured['color']} on {measured['background']} "
            f"is {ratio:.2f}:1, under the 4.5:1 AA minimum"
        )
    finally:
        page.close()
