"""The curriculum data: the knowledge map, the topic tree, browse by topic."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import zipfile
from pathlib import Path

import pytest
import yaml

from helpers import *  # noqa: F401,F403
from helpers import DEWLAB, FRONTMATTER, CELL, COURSE, SERIES, b

class TestTheKnowledgeMap:
    def series(self, repo, monkeypatch, count=4, covers=True):
        strands = ["programming", "programming", "algorithms", "algebra"]
        codes = ["PDP-LO4", "PDP-LO6", "MIT-6.3", "MIT-1.6"]
        (repo / "planning" / "curriculum").mkdir(parents=True, exist_ok=True)
        outcomes_path = repo / "planning" / "curriculum" / "outcomes.yaml"
        outcomes_path.write_text(
            "outcomes:\n" + "".join(
                f"  - code: {c}\n    title: t\n    strand: {s}\n"
                for c, s in zip(codes, strands)
            )
        )
        # OUTCOME_DATA is bound to the real project root at import time, so
        # the `repo` fixture's own ROOT monkeypatch never touches it —
        # without this, every test here would silently read this repo's
        # own real outcomes.yaml instead of the fake one just written above.
        monkeypatch.setattr(b, "OUTCOME_DATA", outcomes_path)
        for n in range(1, count + 1):
            block = ""
            if covers:
                block = f"covers:\n  a-section:\n    covers: [{codes[(n - 1) % 4]}]\n"
            (tutorial_path(repo, f"t{n}")).write_text(
                f'---\ntitle: "Tutorial {n}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n{block}'
                f"---\n\n# Tutorial {n}\n\n## A section\n\nProse.\n"
            )
        set_order(repo, "computational-methods", "s",
                  [f"t{n}" for n in range(1, count + 1)])

    def svg(self, repo) -> str:
        # The tutorial map lives on the tree page, under the topic tree.
        page = repo / "site" / "tree.html"
        match = re.search(r'<svg class="dl-map".*?</svg>',
                          page.read_text() if page.is_file() else "", re.DOTALL)
        return match.group(0) if match else ""

    def test_a_series_too_short_to_have_a_shape_gets_none(self, repo, monkeypatch):
        self.series(repo, monkeypatch, count=2)
        b.build()
        assert self.svg(repo) == ""

    def test_it_still_builds_without_the_curriculum_data(self, repo, monkeypatch):
        # Without outcome data there is no topic tree — but the tutorial map
        # does not need it.
        self.series(repo, monkeypatch, covers=False)
        (repo / "planning" / "curriculum" / "outcomes.yaml").unlink()
        b.build()
        assert (repo / "site" / "index.html").is_file()

    def test_a_series_of_four_gets_a_map_and_naming_an_earlier_tutorial_draws_an_arrow_back(self, repo, monkeypatch):
        """Four tutorials in one series, the last naming the first: a map of
        linked nodes in lanes from the curriculum data, plus one arrow back."""
        self.series(repo, monkeypatch)
        path = tutorial_path(repo, "t4")
        path.write_text(path.read_text() + "\nWe used this in Tutorial 1.\n")
        b.build()
        svg = self.svg(repo)
        # A series gets a map: one node per tutorial, one reading-order arrow
        # between each pair of neighbours.
        assert svg.count('class="dl-map-node"') == 4
        assert svg.count('class="dl-map-next"') == 3
        # Every node links to a page that exists.
        for href in re.findall(r'<a class="dl-map-node" href="([^"]+)"', svg):
            assert (repo / "site" / href).is_file(), href
        # The lanes come from the curriculum data (outcomes.yaml's strands).
        assert ">programming</text>" in svg
        assert ">algorithms</text>" in svg
        # Naming an earlier tutorial draws an arrow back to it.
        assert 'class="dl-map-back"' in svg

    def test_the_tutorial_just_before_does_not_get_a_second_arrow(self, repo, monkeypatch):
        """The reading-order arrow already says that one."""
        self.series(repo, monkeypatch)
        path = tutorial_path(repo, "t4")
        path.write_text(path.read_text() + "\nAs in Tutorial 3.\n")
        b.build()
        assert 'class="dl-map-back"' not in self.svg(repo)

    def test_a_long_title_is_shortened_and_a_tutorial_is_placed_by_what_it_mostly_covers(self):
        # A long title is shortened rather than overflowing.
        assert b.shorten("Short") == "Short"
        assert b.shorten("A very considerably longer tutorial title") == (
            "A very considerably…"
        )
        assert len(b.shorten("A" * 60)) <= 23
        # A tutorial is placed by what it mostly covers.
        strands = {"A": "algebra", "B": "algebra", "C": "sets"}
        assert b.strand_of(["A", "B", "C"], strands) == "algebra"
        assert b.strand_of([], strands) == "other"


class TestTheTopicTree:
    def tree(self, repo) -> str:
        page = repo / "site" / "tree.html"
        return page.read_text() if page.is_file() else ""

    def data(self, repo) -> dict:
        match = re.search(
            r'<script type="application/json" id="dewlab-tree">(.*?)</script>',
            self.tree(repo), re.DOTALL,
        )
        return json.loads(match.group(1)) if match else {}

    def test_a_tutorial_claiming_nothing_gives_a_vertical_tree_of_every_topic_with_none_taught(self, repo):
        """One plain tutorial, no `covers:`: the tree page is built with every
        topic on it, laid out top to bottom by dependency, with the tiers
        labelled and the colours explained, nothing marked taught, and the
        contents page pointing here."""
        write(repo, "Some prose.\n")
        b.build()
        page = self.tree(repo)
        data = self.data(repo)
        nodes = data["nodes"]

        # The page is built.
        assert "The topic tree" in page

        # Every topic in the glossary becomes a node.
        topics = yaml.safe_load(
            (DEWLAB / "planning" / "curriculum" / "topics.yaml").read_text()
        )["topics"]
        assert len(nodes) == len(topics)

        # A topic carries what it is and where it is used.
        node = next(n for n in nodes if n["code"] == "MIT-1.4")
        assert "two digits" in node["plain"]
        assert node["uses"]
        assert node["strand"] == "number"

        # Nothing needs something below it: top to bottom is dependency, so
        # an arrow pointing upwards would be a lie about the tree.
        tier = {n["code"]: n["tier"] for n in nodes}
        for node in nodes:
            for need in node["needs"]:
                assert tier[need] < node["tier"], f"{node['code']} needs {need}"

        # The tree is drawn vertically. Tier is an abstraction; y is what a
        # student actually sees. The two agreeing is what makes this a
        # vertical tree, not a horizontal one with vertical labels.
        place = {n["code"]: n for n in nodes}
        for node in nodes:
            for need in node["needs"]:
                assert place[need]["y"] < node["y"], f"{node['code']} needs {need}"

        # Each tier is a row of its own: two tiers sharing vertical space
        # would say two different depths are the same depth.
        bands = data["bands"]
        assert [band["tier"] for band in bands] == sorted(band["tier"] for band in bands)
        for earlier, later in zip(bands, bands[1:]):
            assert earlier["y"] + earlier["height"] <= later["y"]

        # The tree is taller than it is wide. Giving each subject its own
        # column once produced 5854px wide against 756px tall — a horizontal
        # tree in disguise, unusable on a phone.
        assert data["height"] > data["width"]

        # The top row says you can start there: the stripe labels are the
        # only place the map explains itself.
        labels = {band["tier"]: band["label"] for band in bands}
        assert labels[0] == "start anywhere here"
        assert labels[1] == "one layer down"
        assert labels[2] == "two layers down"

        # A topic no tutorial claims is not marked taught.
        assert all(n["state"] != "taught" for n in nodes)

        # A topic nobody teaches is marked planned.
        states = {n["code"]: n["state"] for n in nodes}
        assert states["MIT-3.6"] == "planned"

        # Groundwork is not reported as a missing tutorial: a `PRE-` topic is
        # nobody's learning outcome, so no tutorial can claim it in
        # `covers:` — left as "planned" it would read as a gap.
        node = next(n for n in nodes if n["code"] == "PRE-1")
        assert node["state"] == "groundwork"

        # A topic may name its own strand. Strands come from outcomes.yaml,
        # so a topic deliberately not an outcome has none — and would
        # otherwise land in "other".
        assert node["strand"] == "geometry"

        # The colour key lists every strand on the tree and no others. The
        # colours are on every node and were explained nowhere except the
        # panel you only see after choosing something.
        listed = set(re.findall(r'<span class="dl-tree-hue" data-strand="([^"]+)"', page))
        assert listed == {n["strand"] for n in nodes}
        assert "What the colours mean" in page

        # A topic we ruled out says so. Read from the file rather than named
        # here: this once named MIT-2.3 outright and broke the day
        # Venn diagrams came back into scope — a decision changing, not the
        # tree breaking. When nothing is ruled out at the moment there is
        # nothing for the tree to say so about, and the loop checks nothing.
        scope = yaml.safe_load(
            (DEWLAB / "planning" / "curriculum" / "out-of-scope.yaml").read_text()
        )
        ruled_out = [entry["code"] for entry in scope["outcomes"] or []]
        for code in ruled_out:
            assert states[code] == "excluded", f"{code} is out of scope and the tree does not say so"

        # The contents page introduces the place instead of carrying the map.
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "Open any tutorial and start" in index
        assert 'href="tree.html"' in index

        # No topics page when nothing in topic-groups.yaml matches this build
        # (TestBrowseByTopicPage has the page that does appear).
        topics_page = repo / "site" / "topics.html"
        assert (topics_page.read_text() if topics_page.is_file() else "") == ""

    def test_a_topic_takes_its_strand_and_coverage_from_the_outcome_it_serves(
        self, repo, monkeypatch
    ):
        # Topic codes and outcome codes used to be identical; now several
        # topics can share one outcome, so strand/coverage must follow the
        # `outcome:` field or a split topic silently looks untaught.
        real = b.load_topics()
        split = {
            "SPLIT-A": {
                "name": "The first half",
                "outcome": "MIT-1.4",
                "plain": "One half of what the descriptor asks for.",
                "uses": ["Somewhere it comes up."],
                "needs": [],
            }
        }
        monkeypatch.setattr(b, "load_topics", lambda: {**real, **split})
        write(repo, "Some prose.\n")
        b.build()

        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "SPLIT-A")
        original = next(n for n in self.data(repo)["nodes"] if n["code"] == "MIT-1.4")
        assert node["strand"] == original["strand"], (
            "a split topic lost the strand of the outcome it serves"
        )
        assert node["state"] == original["state"], (
            "a split topic lost the coverage of the outcome it serves"
        )

    def test_three_tutorials_one_claiming_a_topic_put_the_map_on_the_tree_page_and_link_the_topic_to_its_section(self, repo):
        """The link comes from the tutorial's own `covers:`, so it cannot point
        somewhere the tutorial does not claim; and the tutorial map is drawn
        on the tree page, not on the contents page."""
        path = write(repo, "## A section\n\nProse.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\ncovers:\n  a-section:\n    covers: [MIT-1.4]\n"
        ))
        for n in (2, 3):
            write(repo, f"# T{n}\n\nProse.\n", slug=f"t{n}")
        b.build()
        # A taught topic links to the section that teaches it.
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "MIT-1.4")
        assert node["state"] == "taught"
        assert node["where"]["href"] == (
            "tutorials/sample.html#a-section"
        )
        # The tutorial map is on the tree page and not on the contents page.
        assert "dl-map-node" not in (repo / "site" / "all-tutorials.html").read_text()
        assert "How the tutorials relate" in self.tree(repo)
        assert self.tree(repo).count('class="dl-map-node"') == 3


class TestBrowseByTopicPage:
    """Built against the sandboxed fixture set like every other test here, so
    a mismatch against the real topic-groups.yaml is expected — see
    TestTopicGroupsMatchRealTutorials for what actually checks that file.
    The plain build with no matching tutorial, and so no page, is checked
    with the rest of the plain page in TestTheTopicTree."""

    def page(self, repo) -> str:
        path = repo / "site" / "topics.html"
        return path.read_text() if path.is_file() else ""

    def test_a_group_appears_once_its_own_tutorial_is_in_this_build(self, repo):
        # Any real group entry will do: an id is site-wide.
        groups = yaml.safe_load(
            (DEWLAB / "planning" / "curriculum" / "topic-groups.yaml").read_text()
        )["groups"]
        group = groups[0]
        write(repo, "Some prose.\n", slug=group["tutorials"][0])
        b.build()
        page = self.page(repo)
        assert group["name"] in page
        assert group["intro"].strip()[:20] in page


class TestNoDuplicateKeysInCurriculumData:
    """Found in the wild: a bundle's insertion spliced CMPS outcomes into the
    middle of an existing entry in topics.yaml, giving it a second `needs:`
    key. Plain `yaml.safe_load` kept the last one and silently dropped the
    real prerequisite, with no test noticing since both values were valid
    topic codes."""

    def test_a_repeated_top_level_key_is_rejected(self):
        with pytest.raises(yaml.YAMLError, match="duplicate key"):
            b.load_yaml_no_duplicate_keys("one: 1\ntwo: 2\none: 3\n")

    def test_a_repeated_key_inside_a_nested_mapping_is_rejected(self):
        # The actual shape of the bug: the duplicate was not at the top
        # level, it was a second `needs:` inside one topic's own entry.
        text = (
            "topics:\n"
            "  T1:\n"
            "    name: One\n"
            "    needs: [A]\n"
            "    needs: [B]\n"
        )
        with pytest.raises(yaml.YAMLError, match="duplicate key"):
            b.load_yaml_no_duplicate_keys(text)

    def test_ordinary_yaml_and_the_real_curriculum_files_load(self):
        # Ordinary YAML with no repeats still loads.
        text = "topics:\n  T1:\n    name: One\n    needs: [A]\n"
        assert b.load_yaml_no_duplicate_keys(text) == {
            "topics": {"T1": {"name": "One", "needs": ["A"]}}
        }
        # The real topics.yaml, outcomes.yaml and, if it exists,
        # out-of-scope.yaml have no duplicate keys.
        curriculum = DEWLAB / "planning" / "curriculum"
        for name in ("topics.yaml", "outcomes.yaml", "out-of-scope.yaml"):
            path = curriculum / name
            if path.is_file() or name != "out-of-scope.yaml":
                b.load_yaml_no_duplicate_keys(path.read_text())
