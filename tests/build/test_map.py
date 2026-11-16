"""The topic map page. build.write_map_page() reads map/graph.json and
map/layout.json and the tutorials, and refuses to write a map that names a
page the site does not have. What the page does in a browser is in
tests/e2e/test_map.py; this is the build side.

The sandboxed builds use the small map in tests/e2e/fixture/map/. The real
map is held to the real tutorials in TestTheRealMap, the same way
topic-groups.yaml is (tests/build/test_courses.py)."""

from __future__ import annotations

import json
import re
import shutil

import pytest
from helpers import DEWLAB, write

import build as b

FIXTURE_MAP = DEWLAB / "tests" / "e2e" / "fixture" / "map"
SLUGS = ["third-page", "asking", "predicting", "comparing", "a-challenge", "loading-data",
         "choosing-a-world", "rendering-tour", "choosing-a-project"]


def mapped(repo, skip=(), graph=None, layout=None):
    """A sandbox with every page the fixture map names, except `skip`, and
    the map's two files, changed by `graph` and `layout` if given."""
    for slug in SLUGS:
        if slug not in skip:
            write(repo, f"# {slug}\n\n## First part\n\nSome text.\n", slug=slug)
    shutil.copytree(FIXTURE_MAP, repo / "map")
    for name, change in (("graph", graph), ("layout", layout)):
        if change:
            path = repo / "map" / f"{name}.json"
            data = json.loads(path.read_text())
            change(data)
            path.write_text(json.dumps(data))
    return repo


def data_of(repo) -> dict:
    page = (repo / "site" / "map.html").read_text()
    block = re.search(r'<script type="application/json" id="dewlab-map">(.*?)</script>', page, re.S).group(1)
    return json.loads(block.replace("\\u003c", "<"))


class TestThePage:
    def test_it_is_written_with_its_data_and_a_list_that_needs_no_script(self, repo):
        mapped(repo)
        b.build()
        page = (repo / "site" / "map.html").read_text()
        assert "{{" not in page
        data = data_of(repo)
        assert len(data["towns"]) == 8
        # the list names every topic and links the pages that teach it
        assert "Asking with input" in page
        assert '<a href="tutorials/asking.html">' in page
        # a topic with no page yet says so, and links nothing
        assert "Choosing a project" in page and "page still to be written" in page
        # the picture waits for its script; without one it stays hidden
        assert '<div class="dl-tmap" id="dl-tmap" hidden></div>' in page
        assert 'src="assets/map.js' in page and 'href="assets/map.css' in page

    def test_the_list_links_a_page_once_and_shows_where_a_topic_sits_on_the_paths(self, repo):
        def pin(g):
            asking = next(t for t in g["topics"] if t["id"] == "t-asking")
            asking["steps"] = [
                {"tutorial": "asking", "section": None, "role": "teaches"},
                {"tutorial": "asking", "section": "first-part", "role": "teaches"},
                {"tutorial": "a-challenge", "section": None, "role": "closer-look"},
            ]
        mapped(repo, graph=pin)
        b.build()
        page = (repo / "site" / "map.html").read_text()
        topic = re.search(r'<li id="topic-t-asking">.*?(?=<li id="topic-|</ul>)', page, re.S).group(0)
        # a page that teaches in two places is linked once, with its parts after it
        assert topic.count('<a href="tutorials/asking.html">') == 1
        assert 'Part: <a href="tutorials/asking.html#first-part">First part</a>' in topic
        # the other kinds of step are in the list too, under their own label
        assert "A closer look: " in topic and 'href="tutorials/a-challenge.html"' in topic
        # and the topic says what comes before it and what comes after
        assert "Needs first: nothing, so you can start here." in topic
        assert 'Leads to: <a href="#topic-t-predict">' in topic
        compare = re.search(r'<li id="topic-t-compare">.*?(?=<li id="topic-|</ul>)', page, re.S).group(0)
        assert 'Needs first: <a href="#topic-t-predict">' in compare

    def test_the_list_opens_with_course_routes_and_places_to_begin(self, repo):
        mapped(repo)
        b.build()
        page = (repo / "site" / "map.html").read_text()
        # a course route names its topics in teaching order, each linked to its place in the list
        route = re.search(r'<details class="dl-tmap-list-course"><summary>Computational Methods.*?</details>', page, re.S).group(0)
        assert route.index('href="#topic-t-asking"') < route.index('href="#topic-t-predict"')
        assert 'id="topic-t-asking"' in page
        # a place to begin is a taught topic that needs nothing first
        begin = re.search(r"<h3>Places to begin</h3>.*?<h3>Browse by country</h3>", page, re.S).group(0)
        assert 'href="#topic-t-asking"' in begin
        assert 'href="#topic-t-predict"' not in begin
        # a country wears its colour from the map, and a topic that needs nothing says so
        assert 'class="dl-tmap-swatch"' in page and "var(--map-land-s)" in page
        assert '<span class="dl-tmap-list-begin">Begin here</span>' in page
        # a country says how big it is, and a long list of onward topics folds
        assert re.search(r'id="country-[a-z-]+"><summary>.*?\d+ topics?', page)

    def test_a_topic_that_leads_to_many_folds_its_list(self, repo):
        def widen(g):
            for extra in range(5):
                g["topics"].append({**next(t for t in g["topics"] if t["id"] == "t-predict"),
                                    "id": f"t-extra-{extra}", "name": f"Extra {extra}", "needs": ["t-asking"]})
        def place(lay):
            for extra in range(5):
                lay["towns"][f"t-extra-{extra}"] = dict(lay["towns"]["t-predict"])
        mapped(repo, graph=widen, layout=place)
        b.build()
        page = (repo / "site" / "map.html").read_text()
        assert "<summary>Leads to 6 topics</summary>" in page

    def test_titles_and_courses_come_from_the_tutorials_not_the_map(self, repo):
        mapped(repo)
        b.build()
        town = next(t for t in data_of(repo)["towns"] if t["code"] == "t-asking")
        assert town["steps"][0]["title"] == "A Title"
        assert town["steps"][0]["courses"] == ["Computational Methods"]
        assert town["steps"][0]["href"] == "tutorials/asking.html"
        assert town["state"] == "taught"
        assert next(t for t in data_of(repo)["towns"] if t["code"] == "t-project")["state"] == "planned"

    def test_a_section_is_named_by_its_heading_and_linked_by_its_anchor(self, repo):
        def pin(g):
            next(t for t in g["topics"] if t["id"] == "t-asking")["steps"][0]["section"] = "first-part"
        mapped(repo, graph=pin)
        b.build()
        step = next(t for t in data_of(repo)["towns"] if t["code"] == "t-asking")["steps"][0]
        assert step["section"] == "First part"
        assert step["href"] == "tutorials/asking.html#first-part"

    def test_a_section_the_page_no_longer_has_links_to_the_page_and_says_so(self, repo, capsys):
        # A teacher cut the section; the map should not stop their page going
        # live.
        def pin(g):
            next(t for t in g["topics"] if t["id"] == "t-asking")["steps"][0]["section"] = "no-such-part"
        mapped(repo, graph=pin)
        b.build()
        step = next(t for t in data_of(repo)["towns"] if t["code"] == "t-asking")["steps"][0]
        assert step["href"] == "tutorials/asking.html"
        assert step["section"] is None
        assert "asking#no-such-part" in capsys.readouterr().err

    def test_towns_come_in_reading_order_so_tab_follows_the_land(self, repo):
        mapped(repo)
        b.build()
        data = data_of(repo)
        lands = [c["id"] for c in data["continents"]]
        order = [lands.index(t["land"]) for t in data["towns"]]
        assert order == sorted(order)

    def test_a_tutorial_on_no_topic_is_noted_and_the_build_goes_on(self, repo, capsys):
        mapped(repo)
        write(repo, "# Extra\n\nText.\n", slug="not-on-the-map")
        b.build()
        assert "on no topic of the map yet" in capsys.readouterr().err
        assert (repo / "site" / "map.html").is_file()

    def test_no_map_folder_means_no_map_page_and_no_error(self, repo):
        write(repo, "# Sample\n\nText.\n")
        b.build()
        assert not (repo / "site" / "map.html").exists()


class TestTheBuildRefusesAMapThatDoesNotMatch:
    def test_a_topic_naming_a_missing_tutorial(self, repo):
        mapped(repo, skip=("loading-data",))
        with pytest.raises(b.BuildError) as why:
            b.build()
        assert "t-data" in str(why.value) and "loading-data" in str(why.value)

    def test_a_landmark_naming_a_missing_tutorial(self, repo):
        mapped(repo, skip=("choosing-a-project",))
        with pytest.raises(b.BuildError) as why:
            b.build()
        assert "choosing-a-project" in str(why.value)

    def test_a_need_that_is_not_a_topic(self, repo):
        mapped(repo, graph=lambda g: g["topics"][2]["needs"].append("t-nowhere"))
        with pytest.raises(b.BuildError) as why:
            b.build()
        assert "t-nowhere" in str(why.value)

    def test_a_topic_the_layout_has_not_placed_says_how_to_place_it(self, repo):
        mapped(repo, layout=lambda lay: lay["towns"].pop("t-tour"))
        with pytest.raises(b.BuildError) as why:
            b.build()
        assert "t-tour" in str(why.value) and "dev/map_layout.py" in str(why.value)

    def test_a_layout_that_places_a_topic_the_map_no_longer_has_is_noted_and_ignored(self, repo, capsys):
        mapped(repo, layout=lambda lay: lay["towns"].update({"t-gone": dict(lay["towns"]["t-tour"])}))
        b.build()
        assert "places 't-gone', which is not a topic; it is ignored" in capsys.readouterr().err
        assert "t-gone" not in (repo / "site" / "map.html").read_text()


@pytest.mark.advisory
class TestTheRealMap:
    """Held against the real tutorials, since a sandbox cannot be: a tutorial
    renamed, or a heading changed, on a page the map points at stops here."""

    def test_every_region_is_on_exactly_one_continent_and_every_district_in_a_region(self):
        graph = json.loads((DEWLAB / "map" / "graph.json").read_text())
        regions = {r["id"] for r in graph["regions"]}
        on = [r for c in graph["continents"] for r in c["regions"]]
        assert sorted(on) == sorted(regions)
        assert {d["region"] for d in graph["districts"]} <= regions
        assert sum(1 for c in graph["continents"] if c.get("kind") == "start") == 1

