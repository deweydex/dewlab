"""The topic map, in a browser: the picture is drawn by assets/map.js from a
data block, so what it does (names that stay off the towns, a town that opens,
a road that is drawn, a panel that opens on a phone) only exists here. It is
built from the small map in fixture/map/, over tutorials this file writes."""

from __future__ import annotations

import functools
import http.server
import shutil
import socketserver
import sys
import threading
from pathlib import Path

import pytest

DEWLAB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(DEWLAB))

import build as b  # noqa: E402
from layout import write_course, write_tutorial  # noqa: E402

FIXTURE_MAP = Path(__file__).resolve().parent / "fixture" / "map"

PAGE = """---
title: "{title}"
year: "2026-2027"
version: 2026.08.23.1
---

# {title}

Some prose, so this page has something to read.
"""

TITLES = {
    "third-page": "A third page", "asking": "Asking with input", "predicting": "Guessing before running",
    "comparing": "Comparing with a solution", "a-challenge": "A challenge", "loading-data": "Loading data",
    "choosing-a-world": "Choosing a world", "rendering-tour": "Rendering tour", "choosing-a-project": "Choosing a project",
}


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    root = tmp_path_factory.mktemp("topic-map")
    for slug, title in TITLES.items():
        write_tutorial(root, slug, PAGE.format(title=title))
    write_course(root, "map-fixtures", "Everything", list(TITLES))
    shutil.copytree(FIXTURE_MAP, root / "map")
    (root / "curriculum").mkdir()
    groups = root / "curriculum" / "topic-groups.yaml"
    groups.write_text("groups:\n  - key: map\n    name: Map\n    intro: Only so topics.html has a group.\n    tutorials:\n      - asking\n")

    names = ("ROOT", "TUTORIALS", "COURSES", "OUT", "SETUP", "DATA", "ASSETS", "SHELL", "PAGES",
             "TOPIC_DATA", "TOPIC_GROUPS_DATA", "OUTCOME_DATA")
    original = {name: getattr(b, name) for name in names}
    b.ROOT, b.TUTORIALS, b.COURSES, b.OUT = root, root / "tutorials", root / "courses", root / "site"
    b.SETUP, b.DATA, b.ASSETS, b.SHELL = DEWLAB / "setup", DEWLAB / "data", DEWLAB / "assets", DEWLAB / "assets" / "shell.html"
    b.PAGES = DEWLAB / "pages"
    b.TOPIC_DATA = DEWLAB / "planning" / "curriculum" / "topics.yaml"
    b.TOPIC_GROUPS_DATA = groups
    b.OUTCOME_DATA = DEWLAB / "planning" / "curriculum" / "outcomes.yaml"
    try:
        b.build()
    finally:
        for name, value in original.items():
            setattr(b, name, value)
    return root


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


@pytest.fixture(scope="module")
def map_url(site):
    handler = functools.partial(_Quiet, directory=str(site / "site"))
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}/map.html"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def open_map(browser, url, width=1440, height=900, **kw):
    context = browser.new_context(viewport={"width": width, "height": height}, **kw)
    page = context.new_page()
    problems: list[str] = []
    page.on("pageerror", lambda err: problems.append(f"pageerror: {err}"))
    page.on("console", lambda msg: problems.append(f"console.{msg.type}: {msg.text}") if msg.type == "error" else None)
    page.goto(url)
    page.wait_for_selector(".dl-tmap-stage")
    page.wait_for_timeout(400)
    page.problems = problems
    page.context_to_close = context
    return page


def test_the_map_loads_without_errors_and_does_not_scroll_a_phone_sideways(browser, map_url):
    desktop = open_map(browser, map_url)
    assert desktop.problems == []
    assert desktop.evaluate("document.getElementById('dl-tmap').hidden") is False
    desktop.context_to_close.close()
    phone = open_map(browser, map_url, 375, 700, is_mobile=True, has_touch=True)
    overflow = phone.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
    phone.context_to_close.close()
    assert overflow <= 1, f"the map page scrolls sideways on a phone: {overflow}px over"


NAMES_OVER = """() => {
  const rect = (n) => n.getBoundingClientRect();
  const hit = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
  const labels = [...document.querySelectorAll('.dl-tmap-continent')].map((n) => ({ name: n.textContent.trim(), r: rect(n) }));
  const frame = rect(document.getElementById('dl-tmap'));
  const dots = [...document.querySelectorAll('.dl-tmap-town .dl-tmap-dot')].map(rect);
  // a bridge is a line, so it is as long as its points, not as big as its box
  const bridgePoints = [...document.querySelectorAll('.dl-tmap-bridge-deck')].map((path) => {
    const m = path.getScreenCTM(), len = path.getTotalLength(), pts = [];
    for (let i = 0; i <= 16; i++) { const q = path.getPointAtLength(len * i / 16); pts.push([m.a * q.x + m.c * q.y + m.e, m.b * q.x + m.d * q.y + m.f]); }
    return pts;
  });
  const onBridge = (r) => bridgePoints.filter((pts) => pts.some(([x, y]) => x >= r.left && x <= r.right && y >= r.top && y <= r.bottom)).length;
  const chrome = ['.dl-tmap-top', '.dl-tmap-controls', '.dl-tmap-panel'].map((s) => rect(document.querySelector(s)));
  return labels.map((l, i) => ({
    name: l.name,
    towns: dots.filter((d) => hit(l.r, d)).length,
    bridges: onBridge(l.r),
    names: labels.filter((o, j) => j !== i && hit(l.r, o.r)).length,
    chrome: chrome.filter((c) => hit(l.r, c)).length,
    cut: l.r.left < frame.left || l.r.right > frame.right || l.r.top < frame.top || l.r.bottom > frame.bottom,
  }));
}"""


@pytest.mark.parametrize("width,height", [(1440, 900), (1280, 720), (1024, 768), (390, 844), (360, 640)])
def test_a_continents_name_covers_no_town_bridge_name_or_control(browser, map_url, width, height):
    page = open_map(browser, map_url, width, height)
    page.evaluate("document.getElementById('dl-tmap').scrollIntoView({block: 'start'})")
    page.wait_for_timeout(300)
    found = page.evaluate(NAMES_OVER)
    page.context_to_close.close()
    assert len(found) == 3
    bad = [f for f in found if f["towns"] or f["bridges"] or f["names"] or f["chrome"] or f["cut"]]
    assert bad == [], f"at {width}x{height}: {bad}"


def town_at(page, code):
    box = page.locator(f'.dl-tmap-town[data-code="{code}"] .dl-tmap-dot').bounding_box()
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


def test_a_town_opens_from_a_click_and_from_search_and_shows_its_pages(browser, map_url):
    page = open_map(browser, map_url)
    page.fill("#dl-tmap-q", "comparing")
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)
    heading = page.locator(".dl-tmap-body h2").inner_text()
    assert heading == "Comparing with a solution"
    links = page.locator(".dl-tmap-street-list a").evaluate_all("els => els.map((e) => e.getAttribute('href'))")
    assert links[0] == "tutorials/comparing.html"
    assert "tutorials/a-challenge.html" in links
    # a press that does not move is a click on the town under it, not on the map behind it
    page.keyboard.press("Escape")
    page.click("[data-zoom=fit]")
    page.fill("#dl-tmap-q", "loading")
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)
    x, y = town_at(page, "t-data")
    page.mouse.click(x, y)
    page.wait_for_timeout(200)
    assert page.locator(".dl-tmap-body h2").inner_text() == "Loading data"
    assert page.problems == []
    page.context_to_close.close()


def test_a_road_is_drawn_through_a_bridge_and_the_other_roads_fade(browser, map_url):
    page = open_map(browser, map_url)
    page.fill("#dl-tmap-q", "rendering")
    page.keyboard.press("Enter")
    page.wait_for_timeout(900)
    assert page.evaluate("document.getElementById('dl-tmap').classList.contains('has-focus')")
    page.click("[data-directions]")
    page.wait_for_timeout(900)
    stops = page.locator(".dl-tmap-steps li").count()
    assert stops == 6  # every town this needs, however far back
    # the route joins towns on different continents, so it passes through bridge ends
    route = page.locator(".dl-tmap-route").first.get_attribute("d")
    assert route.count("L") > stops
    # a road that is not the open town's own is faded
    faded = page.evaluate("""() => {
      const road = [...document.querySelectorAll('.dl-tmap-road')].find((r) => !r.classList.contains('is-lit-in') && !r.classList.contains('is-lit-out'));
      return getComputedStyle(road).opacity;
    }""")
    assert float(faded) < 0.2
    page.keyboard.press("Escape")
    page.wait_for_timeout(200)
    assert not page.evaluate("document.getElementById('dl-tmap').classList.contains('has-focus')")
    page.context_to_close.close()


def test_a_bridge_is_as_wide_as_the_roads_it_carries(browser, map_url):
    page = open_map(browser, map_url)
    widths = page.evaluate("""() => [...document.querySelectorAll('.dl-tmap-bridge-deck')].map((d) => ({
      width: parseFloat(d.style.strokeWidth), title: d.parentNode.querySelector('title').textContent }))""")
    page.context_to_close.close()
    by_count = {}
    for w in widths:
        count = int(w["title"].split(". ")[1].split(" ")[0])
        by_count.setdefault(count, []).append(w["width"])
    assert len(by_count) >= 2, widths
    assert max(by_count[max(by_count)]) > max(by_count[min(by_count)])


def test_on_a_phone_the_panel_starts_as_a_bar_that_opens_with_a_tap(browser, map_url):
    page = open_map(browser, map_url, 390, 844, is_mobile=True, has_touch=True)
    assert page.evaluate("document.querySelector('.dl-tmap-panel').classList.contains('is-collapsed')")
    grab = page.locator(".dl-tmap-grab").bounding_box()
    assert grab["height"] >= 24, "the bar must be tall enough to tap"
    page.locator(".dl-tmap-grab").tap()
    page.wait_for_timeout(300)
    assert not page.evaluate("document.querySelector('.dl-tmap-panel').classList.contains('is-collapsed')")
    page.context_to_close.close()


def test_the_list_under_the_map_has_every_topic_and_works_without_a_script(browser, map_url):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(map_url)
    assert page.locator("#dl-tmap").evaluate("e => e.hidden") is True
    expanded = page.evaluate("document.querySelector('.dl-tmap-list').textContent")
    context.close()
    for name in ("Asking with input", "Loading data", "A tour of rendering", "A third page"):
        assert name in expanded
    assert "page still to be written" in expanded


def test_at_the_country_zoom_a_town_is_left_out_where_a_name_stands(browser, map_url):
    page = open_map(browser, map_url)
    page.click("[data-zoom=in]")
    page.wait_for_timeout(300)
    assert page.evaluate("document.getElementById('dl-tmap').dataset.lod") == "1"
    shown = page.evaluate("""() => {
      const hit = (a, b) => a.left < b.right && a.right > b.left && a.top < b.bottom && a.bottom > b.top;
      const names = [...document.querySelectorAll('.dl-tmap-region')].filter((n) => getComputedStyle(n).opacity > 0.1).map((n) => n.getBoundingClientRect());
      const dots = [...document.querySelectorAll('.dl-tmap-town .dl-tmap-dot')].filter((d) => getComputedStyle(d).opacity > 0.1).map((d) => d.getBoundingClientRect());
      return { names: names.length, covered: dots.filter((d) => names.some((n) => hit(n, d))).length };
    }""")
    page.context_to_close.close()
    assert shown["names"] >= 1
    assert shown["covered"] == 0
