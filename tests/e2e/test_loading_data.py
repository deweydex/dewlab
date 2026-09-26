"""Datasets fetched live, with the saved copy as the backup (#324), on the
fixture's `loading-data` page: `life-expectancy.csv`, whose recipe
fetches Our World in Data, and `the-time-machine.txt`, which has no live
source.

The live source is never the real website: the test answers for it, or
refuses, so what is checked is the page's behaviour and not the network.
The downloaded copy runs with no network at all beyond Pyodide itself.
"""

from __future__ import annotations

import base64
import gzip
import json
import re

import pytest

from test_compare import _open, _serve

PAGE = "tutorials/loading-data.html"
LIVE = "https://ourworldindata.org/grapher/life-expectancy.csv*"
LIVE_CSV = (
    "entity,code,year,life_expectancy_0\n"
    "Ireland,IRL,1949,64.0\n"          # before 1950: the recipe drops it
    "Ireland,IRL,1950,65.581\n"
    "Ireland,IRL,2024,82.7\n"
    "World,OWID_WRL,2024,73.3\n"
)


def run(tab, cell):
    tab.locator(f".dl-cell[data-cell-id='{cell}'] .dl-btn-run").click()
    tab.wait_for_function(
        f"""() => {{
          const el = document.querySelector(".dl-cell[data-cell-id='{cell}'] .dl-cell-runline");
          const label = document.querySelector(".dl-cell[data-cell-id='{cell}'] .dl-btn-run .dl-btn-label");
          return el && /^Ran /.test(el.textContent) && label && label.textContent === "Run";
        }}""",
        timeout=240_000,
    )
    output = tab.locator(f".dl-cell[data-cell-id='{cell}'] .dl-output")
    note = output.locator(".dl-data-note")
    printed = output.locator(".dl-stdout").inner_text().strip()
    return printed, (note.inner_text() if note.count() else None)


def _answer(route):
    route.fulfill(status=200, content_type="text/csv", body=LIVE_CSV,
                  headers={"Access-Control-Allow-Origin": "*"})


@pytest.fixture()
def hosted(browser, base_url, site_dir):
    route = _serve(site_dir, standalone=False, path=PAGE)
    context, tab = _open(browser, f"{base_url}/{PAGE}", route, page=PAGE)
    try:
        yield context, tab
    finally:
        context.close()


class TestOnTheSite:
    def test_a_live_source_that_answers_is_used_and_shaped(self, hosted):
        context, tab = hosted
        context.route(LIVE, _answer)
        printed, note = run(tab, "load-live")
        assert printed == "3 rows"
        assert note.startswith("Loaded life-expectancy.csv from Our World in Data just now.")
        assert "copy saved on 26 September 2026" in note

    def test_a_live_source_that_fails_gives_the_saved_copy(self, hosted, site_dir):
        context, tab = hosted
        context.route(LIVE, lambda route: route.abort())
        printed, note = run(tab, "load-live")
        saved = (site_dir / "data" / "life-expectancy.csv").read_text().count("\n") - 1
        assert printed == f"{saved} rows"
        assert note.startswith("Loaded the copy of life-expectancy.csv saved on 26 September 2026")
        assert "could not be used just now" in note

    def test_a_dataset_with_no_live_source_says_which_copy(self, hosted):
        _, tab = hosted
        printed, note = run(tab, "load-saved")
        assert printed == "True"
        assert note == "Loaded the copy of the-time-machine.txt saved on 20 September 2026."


def _offline_copy(site_dir):
    """The page as a download carries it: _serve()'s main-thread page, plus
    the datasets standalone_html() packs into the manifest."""
    serve = _serve(site_dir, standalone=True, path=PAGE)
    index = json.loads((site_dir / "data" / "index.json").read_text())
    files = ["life-expectancy.csv", "the-time-machine.txt"]

    def handle(route):
        captured = {}

        class Grab:
            def fulfill(self, **kwargs):
                captured.update(kwargs)
        serve(Grab())
        page = captured["body"]
        marker = '<script type="application/json" id="dewlab-manifest">'
        start = page.index(marker) + len(marker)
        end = page.index("</script>", start)
        manifest = json.loads(page[start:end].replace("\\u003c", "<"))
        manifest["dataIndex"] = {name: index[name] for name in files}
        manifest["dataFiles"] = {
            name: base64.b64encode(gzip.compress((site_dir / "data" / name).read_bytes())).decode()
            for name in files
        }
        page = page[:start] + json.dumps(manifest).replace("<", "\\u003c") + page[end:]
        route.fulfill(status=200, content_type="text/html; charset=utf-8", body=page)
    return handle


class TestOffline:
    def test_a_downloaded_copy_with_no_network_uses_what_it_carries(
            self, browser, base_url, site_dir):
        context, tab = _open(browser, f"{base_url}/{PAGE}", _offline_copy(site_dir), page=PAGE)
        try:
            fetched = []
            # Nothing from data/ and no live source: as a copy opened from
            # disk on a train would find things.
            def refuse(route):
                fetched.append(route.request.url)
                route.abort()
            context.route(re.compile(r".*/data/.*"), refuse)
            context.route(LIVE, refuse)
            printed, note = run(tab, "load-live")
            assert printed.endswith(" rows") and printed != "3 rows"
            assert "could not be used just now" in note
            printed, note = run(tab, "load-saved")
            assert printed == "True"
            assert note == "Loaded the copy of the-time-machine.txt saved on 20 September 2026."
            assert not any("/data/" in url for url in fetched)
        finally:
            context.close()
