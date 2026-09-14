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
    def series(self, repo, count=4, covers=True):
        strands = ["programming", "programming", "algorithms", "algebra"]
        codes = ["PDP-LO4", "PDP-LO6", "MIT-6.3", "MIT-1.6"]
        (repo / "planning" / "curriculum").mkdir(parents=True, exist_ok=True)
        (repo / "planning" / "curriculum" / "outcomes.yaml").write_text(
            "outcomes:\n" + "".join(
                f"  - code: {c}\n    title: t\n    strand: {s}\n"
                for c, s in zip(codes, strands)
            )
        )
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

    def test_a_series_gets_a_map(self, repo):
        self.series(repo)
        b.build()
        svg = self.svg(repo)
        assert svg.count('class="dl-map-node"') == 4
        assert svg.count('class="dl-map-next"') == 3

    def test_a_series_too_short_to_have_a_shape_gets_none(self, repo):
        self.series(repo, count=2)
        b.build()
        assert self.svg(repo) == ""

    def test_every_node_links_to_a_page_that_exists(self, repo):
        self.series(repo)
        b.build()
        for href in re.findall(r'<a class="dl-map-node" href="([^"]+)"', self.svg(repo)):
            assert (repo / "site" / href).is_file(), href

    def test_lanes_come_from_the_curriculum_data(self, repo):
        self.series(repo)
        b.build()
        svg = self.svg(repo)
        assert ">programming</text>" in svg
        assert ">algorithms</text>" in svg

    def test_it_still_builds_without_the_curriculum_data(self, repo):
        # Without outcome data there is no topic tree — but the tutorial map
        # does not need it.
        self.series(repo, covers=False)
        (repo / "planning" / "curriculum" / "outcomes.yaml").unlink()
        b.build()
        assert (repo / "site" / "index.html").is_file()

    def test_naming_an_earlier_tutorial_draws_an_arrow_back_to_it(self, repo):
        self.series(repo)
        path = tutorial_path(repo, "t4")
        path.write_text(path.read_text() + "\nWe used this in Tutorial 1.\n")
        b.build()
        assert 'class="dl-map-back"' in self.svg(repo)

    def test_the_tutorial_just_before_does_not_get_a_second_arrow(self, repo):
        """The reading-order arrow already says that one."""
        self.series(repo)
        path = tutorial_path(repo, "t4")
        path.write_text(path.read_text() + "\nAs in Tutorial 3.\n")
        b.build()
        assert 'class="dl-map-back"' not in self.svg(repo)

    def test_a_long_title_is_shortened_rather_than_overflowing(self):
        assert b.shorten("Short") == "Short"
        assert b.shorten("A very considerably longer tutorial title") == (
            "A very considerably…"
        )
        assert len(b.shorten("A" * 60)) <= 23

    def test_a_tutorial_is_placed_by_what_it_mostly_covers(self):
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

    def test_the_page_is_built(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert "The topic tree" in self.tree(repo)

    def test_every_topic_in_the_glossary_becomes_a_node(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        topics = yaml.safe_load(
            (DEWLAB / "planning" / "curriculum" / "topics.yaml").read_text()
        )["topics"]
        assert len(self.data(repo)["nodes"]) == len(topics)

    def test_a_topic_carries_what_it_is_and_where_it_is_used(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "MIT-1.4")
        assert "two digits" in node["plain"]
        assert node["uses"]
        assert node["strand"] == "number"

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

    def test_nothing_needs_something_below_it(self, repo):
        # Top to bottom is dependency, so an arrow pointing upwards would be
        # a lie about the tree.
        write(repo, "Some prose.\n")
        b.build()
        data = self.data(repo)
        tier = {n["code"]: n["tier"] for n in data["nodes"]}
        for node in data["nodes"]:
            for need in node["needs"]:
                assert tier[need] < node["tier"], f"{node['code']} needs {need}"

    def test_the_tree_is_drawn_vertically(self, repo):
        # Tier is an abstraction; y is what a student actually sees. The two
        # agreeing is what makes this a vertical tree, not a horizontal one
        # with vertical labels.
        write(repo, "Some prose.\n")
        b.build()
        data = self.data(repo)
        place = {n["code"]: n for n in data["nodes"]}
        for node in data["nodes"]:
            for need in node["needs"]:
                assert place[need]["y"] < node["y"], f"{node['code']} needs {need}"

    def test_each_tier_is_a_row_of_its_own(self, repo):
        # Two tiers sharing vertical space would say two different depths
        # are the same depth.
        write(repo, "Some prose.\n")
        b.build()
        bands = self.data(repo)["bands"]
        assert [band["tier"] for band in bands] == sorted(band["tier"] for band in bands)
        for earlier, later in zip(bands, bands[1:]):
            assert earlier["y"] + earlier["height"] <= later["y"]

    def test_the_tree_is_taller_than_it_is_wide(self, repo):
        # Giving each subject its own column once produced 5854px wide
        # against 756px tall — a horizontal tree in disguise, unusable on a phone.
        write(repo, "Some prose.\n")
        b.build()
        data = self.data(repo)
        assert data["height"] > data["width"]

    def test_the_top_row_says_you_can_start_there(self, repo):
        """The stripe labels are the only place the map explains itself."""
        write(repo, "Some prose.\n")
        b.build()
        bands = {band["tier"]: band["label"] for band in self.data(repo)["bands"]}
        assert bands[0] == "start anywhere here"
        assert bands[1] == "one layer down"
        assert bands[2] == "two layers down"

    def test_a_taught_topic_links_to_the_section_that_teaches_it(self, repo):
        """The link comes from the tutorial's own `covers:`, so it cannot point
        somewhere the tutorial does not claim."""
        path = write(repo, "## A section\n\nProse.\n")
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\ncovers:\n  a-section:\n    covers: [MIT-1.4]\n"
        ))
        b.build()
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "MIT-1.4")
        assert node["state"] == "taught"
        assert node["where"]["href"] == (
            "tutorials/sample.html#a-section"
        )

    def test_a_topic_no_tutorial_claims_is_not_marked_taught(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert all(n["state"] != "taught" for n in self.data(repo)["nodes"])

    def test_a_topic_nobody_teaches_is_marked_planned(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        states = {n["code"]: n["state"] for n in self.data(repo)["nodes"]}
        assert states["MIT-3.6"] == "planned"

    def test_groundwork_is_not_reported_as_a_missing_tutorial(self, repo):
        # A `PRE-` topic is nobody's learning outcome, so no tutorial can
        # claim it in `covers:` — left as "planned" it would read as a gap.
        write(repo, "Some prose.\n")
        b.build()
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "PRE-1")
        assert node["state"] == "groundwork"

    def test_a_topic_may_name_its_own_strand(self, repo):
        # Strands come from outcomes.yaml, so a topic deliberately not an
        # outcome has none — and would otherwise land in "other".
        write(repo, "Some prose.\n")
        b.build()
        node = next(n for n in self.data(repo)["nodes"] if n["code"] == "PRE-1")
        assert node["strand"] == "geometry"

    def test_the_colour_key_lists_every_strand_on_the_tree_and_no_others(self, repo):
        """The colours are on every node and were explained nowhere except the
        panel you only see after choosing something."""
        write(repo, "Some prose.\n")
        b.build()
        page = self.tree(repo)
        listed = set(re.findall(r'<span class="dl-tree-hue" data-strand="([^"]+)"', page))
        assert listed == {n["strand"] for n in self.data(repo)["nodes"]}
        assert "What the colours mean" in page

    def test_a_topic_we_ruled_out_says_so(self, repo):
        # Read from the file rather than named here: this test used to assert
        # on MIT-2.3 by name and broke the day Venn diagrams came back into
        # scope — a decision changing, not the tree breaking.
        write(repo, "Some prose.\n")
        b.build()
        scope = yaml.safe_load(
            (DEWLAB / "planning" / "curriculum" / "out-of-scope.yaml").read_text()
        )
        ruled_out = [entry["code"] for entry in scope["outcomes"] or []]
        if not ruled_out:
            pytest.skip("nothing is ruled out at the moment, so there is nothing "
                        "for the tree to say so about")
        states = {n["code"]: n["state"] for n in self.data(repo)["nodes"]}
        for code in ruled_out:
            assert states[code] == "excluded", f"{code} is out of scope and the tree does not say so"

    def test_the_tutorial_map_moved_here_from_the_contents_page(self, repo):
        for n in (1, 2, 3):
            (tutorial_path(repo, f"t{n}")).write_text(
                f'---\ntitle: "T{n}"\n'
                f'year: "2026-2027"\n'
                f"version: 2026.08.23.1\n---\n\n# T{n}\n\nProse.\n"
            )
        set_order(repo, "computational-methods", "python-fundamentals",
                  ["t1", "t2", "t3"])
        b.build()
        assert "dl-map-node" not in (repo / "site" / "all-tutorials.html").read_text()
        assert "How the tutorials relate" in self.tree(repo)
        assert self.tree(repo).count('class="dl-map-node"') == 3

    def test_the_contents_page_introduces_the_place_instead(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        index = (repo / "site" / "all-tutorials.html").read_text()
        assert "Open any tutorial and start" in index
        assert 'href="tree.html"' in index


class TestBrowseByTopicPage:
    """Built against the sandboxed fixture set like every other test here, so
    a mismatch against the real topic-groups.yaml is expected — see
    TestTopicGroupsMatchRealTutorials for what actually checks that file."""

    def page(self, repo) -> str:
        path = repo / "site" / "topics.html"
        return path.read_text() if path.is_file() else ""

    def test_no_topics_page_when_nothing_in_it_matches_this_build(self, repo):
        write(repo, "Some prose.\n")
        b.build()
        assert self.page(repo) == ""

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

    def test_ordinary_yaml_with_no_repeats_still_loads(self):
        text = "topics:\n  T1:\n    name: One\n    needs: [A]\n"
        assert b.load_yaml_no_duplicate_keys(text) == {
            "topics": {"T1": {"name": "One", "needs": ["A"]}}
        }

    def test_the_real_topics_yaml_has_no_duplicate_keys(self):
        path = DEWLAB / "planning" / "curriculum" / "topics.yaml"
        b.load_yaml_no_duplicate_keys(path.read_text())

    def test_the_real_outcomes_yaml_has_no_duplicate_keys(self):
        path = DEWLAB / "planning" / "curriculum" / "outcomes.yaml"
        b.load_yaml_no_duplicate_keys(path.read_text())

    def test_the_real_out_of_scope_yaml_has_no_duplicate_keys(self):
        path = DEWLAB / "planning" / "curriculum" / "out-of-scope.yaml"
        if path.is_file():
            b.load_yaml_no_duplicate_keys(path.read_text())
