"""The reference panel: glossaries, maths and Python basics, the cross-tutorial reference and its filters."""

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

class TestTheReference:
    """planning/REFERENCE_PANEL.md's cumulative glossary: a tutorial's
    manifest carries its own entries plus every earlier series member's, so
    the panel never shows a term this reader has not been taught yet.

    The scenarios: a lone tutorial with nothing at all (no glossary, and no
    maths or Python basics files either); a series of two, each with a
    term, with a practice page for the first and a mixed practice page
    across both (where a tutorial's own glossary, inheritance, its
    direction, and the origin of an inherited term are all checked at
    once); a term repeated later; one tutorial whose three sections settle
    which section an origin points at; and the two malformed glossary
    files that stop the build."""

    def practice(self, repo, slug: str, **frontmatter) -> Path:
        path = tutorial_path(repo, f"{slug}")
        extra = "".join(
            f"{key}: {value}\n" if not isinstance(value, list)
            else f"{key}:\n" + "".join(f"  - {v}\n" for v in value)
            for key, value in frontmatter.items()
        )
        path.write_text(
            FRONTMATTER.format(version="2026.08.23.1").replace(
                "version: 2026.08.23.1\n", f"version: 2026.08.23.1\n{extra}")
            + "**1.** A question.\n"
        )
        listed = sorted(
            p.stem for p in path.parent.parent.glob("*/*.md")
            if "practice_for" not in p.read_text()
            and "practice_across" not in p.read_text()
        )
        set_order(repo, "computational-methods", "python-fundamentals", listed)
        return path

    def test_a_lone_tutorial_with_no_glossary_and_no_basics_files_builds_with_none_of_them(
            self, repo, monkeypatch):
        # Absence all round: no glossary file, and neither basics file. A
        # missing basics file is fine, not an error (the two basics classes
        # below test the files themselves).
        monkeypatch.setattr(
            b, "MATH_BASICS_DATA", repo / "planning" / "curriculum" / "math-basics.yaml")
        monkeypatch.setattr(
            b, "PYTHON_BASICS_DATA", repo / "planning" / "curriculum" / "python-basics.yaml")
        assert b.load_math_basics() == []
        assert b.load_python_basics() == []
        write(repo, "One.\n", slug="one")
        b.build()
        # A tutorial with no glossary file has no glossary key.
        assert "glossary" not in manifest(built(repo, "one"))

    def test_a_series_of_two_with_practice_pages_accumulates_forwards_only(self, repo):
        """One scenario, one build: `one` teaches x, `two` teaches y, `one`
        has a practice page and a mixed practice page covers both.
        Everything the cumulative glossary promises about a tutorial's own
        entries, direction and origin is checked here."""
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        set_order(repo, "computational-methods", "python-fundamentals", ["one", "two"])
        glossary(repo, "one", [
            {"term": "x", "kind": "concept", "definition": "The first thing."},
        ])
        glossary(repo, "two", [{"term": "y", "kind": "concept", "definition": "Second."}])
        self.practice(repo, "one-practice", practice_for="one")
        self.practice(repo, "mixed", practice_across=["one", "two"])
        b.build()

        # A tutorial's own glossary appears in its manifest.
        assert manifest(built(repo, "one"))["glossary"] == [
            {"term": "x", "kind": "concept", "definition": "The first thing."},
        ]

        # A later tutorial inherits earlier ones' terms.
        assert [e["term"] for e in manifest(built(repo, "two"))["glossary"]] == ["x", "y"]

        # An earlier tutorial never shows a later one's terms: the guarantee
        # that matters most in this feature (planning/REFERENCE_PANEL.md §1),
        # nothing forward-looking.
        assert [e["term"] for e in manifest(built(repo, "one"))["glossary"]] == ["x"]

        # An inherited term says where it was introduced: the panel answers
        # "what does this mean"; the origin answers "where did I meet this".
        entry = manifest(built(repo, "two"))["glossary"][0]
        assert entry["origin"]["href"] == "one.html"
        assert entry["origin"]["title"]

        # A tutorial's own terms carry no origin: saying "you met this here"
        # on the page teaching it is noise.
        assert "origin" not in manifest(built(repo, "one"))["glossary"][0]

        # A practice page gets its tutorial's cumulative glossary.
        page = (repo / "site" / "tutorials" / "one-practice.html").read_text()
        assert [e["term"] for e in manifest(page)["glossary"]] == ["x"]

        # A practice page's origins resolve from the practice page: it
        # borrows its tutorial's glossary, but the link has to resolve from
        # where the *reader* is — the two sit at different depths the
        # moment either has a frozen release.
        entry = manifest(page)["glossary"][0]
        assert entry["origin"]["href"].startswith("one.html")

        # A mixed practice page unions its tutorials' glossaries.
        page = (repo / "site" / "tutorials" / "mixed.html").read_text()
        assert [e["term"] for e in manifest(page)["glossary"]] == ["x", "y"]

    def test_a_term_repeated_later_keeps_its_first_definition(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        set_order(repo, "computational-methods", "python-fundamentals", ["one", "two"])
        glossary(repo, "one", [{"term": "x", "kind": "concept", "definition": "First."}])
        glossary(repo, "two", [{"term": "x", "kind": "concept", "definition": "Second, wrongly."}])
        b.build()
        entries = manifest(built(repo, "two"))["glossary"]
        assert len(entries) == 1
        assert entries[0]["term"] == "x"
        assert entries[0]["definition"] == "First."

    def test_the_origin_points_at_the_section_the_term_is_taught_in(self, repo):
        """One tutorial, three terms, each settling one rule about which
        section an inherited term's origin lands on. A whole-page link makes
        a reader hunt; the emphasised first use is where
        docs/WRITING_TUTORIALS.md#marking-a-term puts the introduction."""
        write(repo,
              "Intro.\n\n"
              # `gamma` is in this link's href, and the origin must ignore a
              # match inside markup: searching the raw HTML matches inside an
              # href or a class name, and anchors the reader to whichever
              # section happened to contain it.
              "## Early\n\n[a link](https://example.org/gamma/page)\n\n"
              "## Later On\n\nHere we meet *alpha* properly.\n\n"
              "## Doing It\n\nWe use *beta* here.\n\n"
              "## Where It Is Taught\n\nHere is *gamma* itself.\n\n"
              # A term's name often appears in a citation title — "The Monte
              # Carlo Method" is a paper as well as a concept — and the
              # bibliography is the one section that does not teach it.
              "## Where to Read More\n\nSomebody (1949). *All About beta.*\n",
              slug="one")
        write(repo, "Two.\n", slug="two")
        set_order(repo, "computational-methods", "python-fundamentals", ["one", "two"])
        glossary(repo, "one", [
            {"term": "alpha", "kind": "concept", "definition": "First."},
            {"term": "beta", "kind": "concept", "definition": "Second."},
            {"term": "gamma", "kind": "concept", "definition": "Third."},
        ])
        b.build()
        by_term = {e["term"]: e for e in manifest(built(repo, "two"))["glossary"]}

        # The origin points at the section the term is taught in.
        entry = by_term["alpha"]
        assert entry["origin"]["href"] == "one.html#later-on"
        # The origin never points at the bibliography.
        entry = by_term["beta"]
        assert entry["origin"]["href"] == "one.html#doing-it"
        # The origin ignores a match inside markup.
        entry = by_term["gamma"]
        assert entry["origin"]["href"] == "one.html#where-it-is-taught"

    @pytest.mark.parametrize("entry,match", [
        ({"term": "x", "kind": "vibe", "definition": "Nope."}, "not one of"),
        ({"term": "x", "kind": "concept"}, "missing a term or a definition"),
    ])
    def test_a_malformed_own_glossary_entry_fails_the_build(self, repo, entry, match):
        write(repo, "One.\n", slug="one")
        glossary(repo, "one", [entry])
        with pytest.raises(b.BuildError, match=match):
            b.build()


class TestMathBasics:
    """Independent of any tutorial or series, unlike the cumulative reference
    glossary, so tests monkeypatch MATH_BASICS_DATA directly rather than
    using the `repo` fixture's tutorial layout. The scenarios: a well-formed
    maths file and a well-formed Python file, loaded and both reaching a
    built page's manifest; and the files this repo ships, maths and Python
    both. The three malformed shapes that stop the build are shared with
    Python Basics and live in TestBasicsValidation below. A missing file is
    covered by TestTheReference's lone tutorial with nothing."""

    def _write(self, repo: Path, monkeypatch, text: str) -> Path:
        path = repo / "planning" / "curriculum" / "math-basics.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        monkeypatch.setattr(b, "MATH_BASICS_DATA", path)
        return path

    def test_well_formed_files_load_their_groups_and_reach_every_pages_own_manifest(
            self, repo, monkeypatch):
        self._write(repo, monkeypatch, """
groups:
  - label: Operations
    entries:
      - term: Sum
        definition: The result of adding numbers together.
""")
        assert b.load_math_basics() == [
            {"label": "Operations", "entries": [
                {"term": "Sum", "definition": "The result of adding numbers together."},
            ]},
        ]
        # The Python file rides on the same build (TestPythonBasics loads
        # the other shapes of that file).
        python_path = repo / "planning" / "curriculum" / "python-basics.yaml"
        python_path.write_text("""
groups:
  - label: Values
    entries:
      - term: String
        definition: Text, written between quotation marks.
""")
        monkeypatch.setattr(b, "PYTHON_BASICS_DATA", python_path)
        write(repo, "One.\n", slug="one")
        b.build()
        assert manifest(built(repo, "one"))["mathBasics"] == [
            {"label": "Operations", "entries": [
                {"term": "Sum", "definition": "The result of adding numbers together."},
            ]},
        ]
        assert manifest(built(repo, "one"))["pythonBasics"] == [
            {"label": "Values", "entries": [
                {"term": "String", "definition": "Text, written between quotation marks."},
            ]},
        ]

    def test_the_shipped_files_are_themselves_well_formed(self):
        # Not monkeypatched: loads the real files this repo ships, guarding
        # against a malformed hand-edit reaching main.
        assert b.load_math_basics()
        assert b.load_python_basics()


class TestPythonBasics:
    """Same shape and shared validation (_load_basics()) as Math Basics;
    tests mirror TestMathBasics, monkeypatching PYTHON_BASICS_DATA directly.
    The one difference is an entry's optional `example`: the well-formed
    file with one example is already exercised by TestMathBasics (which
    loads a Python file alongside its own and checks both reach the
    manifest), so this class covers only the file with no example at all.
    The malformed shapes it shares with Math Basics live in
    TestBasicsValidation below."""

    def _write(self, repo: Path, monkeypatch, text: str) -> Path:
        path = repo / "planning" / "curriculum" / "python-basics.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        monkeypatch.setattr(b, "PYTHON_BASICS_DATA", path)
        return path

    def test_an_entry_with_no_example_is_fine(self, repo, monkeypatch):
        self._write(repo, monkeypatch, """
groups:
  - label: Values
    entries:
      - term: Boolean
        definition: A value that is either True or False.
""")
        assert b.load_python_basics() == [
            {"label": "Values", "entries": [
                {"term": "Boolean", "definition": "A value that is either True or False."},
            ]},
        ]


@pytest.mark.parametrize("attr,filename,loader", [
    ("MATH_BASICS_DATA", "math-basics.yaml", "load_math_basics"),
    ("PYTHON_BASICS_DATA", "python-basics.yaml", "load_python_basics"),
])
class TestBasicsValidation:
    """The three malformed shapes _load_basics() rejects, shared by Math
    Basics and Python Basics alike, so each is checked once here against
    both files rather than twice in TestMathBasics and TestPythonBasics."""

    def _write(self, repo: Path, monkeypatch, attr: str, filename: str, text: str) -> Path:
        path = repo / "planning" / "curriculum" / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        monkeypatch.setattr(b, attr, path)
        return path

    def test_a_group_with_no_label_fails_the_build(
            self, repo, monkeypatch, attr, filename, loader):
        self._write(repo, monkeypatch, attr, filename, """
groups:
  - entries:
      - term: Sum
        definition: Adding.
""")
        with pytest.raises(b.BuildError, match="label"):
            getattr(b, loader)()

    def test_a_group_with_no_entries_fails_the_build(
            self, repo, monkeypatch, attr, filename, loader):
        self._write(repo, monkeypatch, attr, filename,
                     "groups:\n  - label: Operations\n    entries: []\n")
        with pytest.raises(b.BuildError, match="no entries"):
            getattr(b, loader)()

    def test_an_entry_missing_a_definition_fails_the_build(
            self, repo, monkeypatch, attr, filename, loader):
        self._write(repo, monkeypatch, attr, filename, """
groups:
  - label: Operations
    entries:
      - term: Sum
""")
        with pytest.raises(b.BuildError, match="term or a definition"):
            getattr(b, loader)()


class TestTheCrossTutorialReference:
    """`write_reference_index()` deliberately breaks the rule TestTheReference
    protects — a reader is never shown a term not yet reached — because
    dewmini has no position in a series to protect.

    The scenarios: two tutorials sharing a term, one of which also has a
    term of two kinds and an entry with an example (what each entry
    carries, keyed by term, and that the index carries terms from every
    tutorial at once, not just the first); one tutorial whose two terms
    show the sort order; and the offline bundle."""

    def index(self, repo: Path):
        return json.loads((repo / "site" / "assets" / "reference-index.json").read_text())

    def test_each_entry_carries_its_origin_kind_and_example_but_no_link(self, repo):
        write(repo, "One.\n", slug="one")
        write(repo, "Two.\n", slug="two")
        set_order(repo, "computational-methods", "python-fundamentals", ["one", "two"])
        glossary(repo, "one", [
            {"term": "x", "kind": "concept", "definition": "A thing.", "example": "x = 1"},
            {"term": "y", "kind": "concept", "definition": "Another."},
            {"term": "print", "kind": "concept", "definition": "The idea."},
            {"term": "print", "kind": "function", "definition": "The call."},
            {"term": "shared", "kind": "concept", "definition": "The first definition."},
        ])
        glossary(repo, "two", [
            {"term": "shared", "kind": "concept", "definition": "A later one."},
        ])
        b.build()

        # It carries terms from every tutorial at once, not just the first
        # — including one taught only in a *later* tutorial, which is
        # exactly what a tutorial page's own panel would hide.
        assert {e["term"] for e in self.index(repo)} == {"x", "y", "print", "shared"}

        # Each entry names the tutorial that introduced it.
        entry = self.index(repo)[0]
        assert entry["origin"] == "A Title"

        # It carries no link to that tutorial: this file ships inside
        # dewmini's offline bundle, which has no tutorials in it, so a link
        # would 404 for every offline reader.
        assert "href" not in json.dumps(self.index(repo))

        # A term defined twice appears once: deduplicated on (term, kind),
        # first definition winning — the same key cumulative_glossary() uses.
        entries = [e for e in self.index(repo) if e["term"] == "shared"]
        assert len(entries) == 1
        assert entries[0]["definition"] == "The first definition."

        # The same term of a different kind is kept: `kind` is part of the
        # key, a word can be both a concept and a function, and collapsing
        # those would lose one.
        assert len([e for e in self.index(repo) if e["term"] == "print"]) == 2

        # An example is carried through when there is one.
        by_term = {e["term"]: e for e in self.index(repo)}
        assert by_term["x"]["example"] == "x = 1"
        assert "example" not in by_term["y"]

    def test_entries_are_sorted_by_term(self, repo):
        write(repo, "One.\n", slug="one")
        glossary(repo, "one", [
            {"term": "zebra", "kind": "concept", "definition": "Last."},
            {"term": "apple", "kind": "concept", "definition": "First."},
        ])
        b.build()

        assert [e["term"] for e in self.index(repo)] == ["apple", "zebra"]

    def test_the_offline_bundle_carries_the_index(self, repo_with_assets):
        # Generated rather than checked in, so it needs its own copy step
        # (_reference_index_for_bundle), or dewmini's Library is empty offline.
        write(repo_with_assets, "One.\n", slug="one")
        glossary(repo_with_assets, "one", [
            {"term": "x", "kind": "concept", "definition": "A thing."},
        ])
        b.build(standalone=True)

        bundled = (repo_with_assets / "site" / "download" / "notebook"
                   / "assets" / "reference-index.json")
        assert bundled.is_file()
        assert json.loads(bundled.read_text())[0]["term"] == "x"


class TestWhatTheReferenceCanBeFilteredBy:
    """`tutorial_facets()`: neither facet is a field anyone maintains.
    Subject is read off the learning-outcome codes a tutorial claims in
    `covers:`; level is read off the prerequisite depth of the topic tree —
    so these tests are mostly about the *derivation* holding under change.

    The scenarios: four tutorials against the real tree, claiming a maths
    outcome, a computing one, both and none; two tutorials against a
    stubbed tree, rated and then rearranged; and the bands themselves."""

    def covers(self, path: Path, codes: list[str]) -> None:
        claim = "covers:\n  a-section:\n    covers: [" + ", ".join(codes) + "]\n"
        path.write_text(path.read_text().replace(
            "version: 2026.08.23.1\n", "version: 2026.08.23.1\n" + claim))

    def tree(self, monkeypatch, tmp_path: Path, topics: str) -> None:
        # `repo` does not stub TOPIC_DATA, so without this the real
        # planning/curriculum/topics.yaml would be read instead.
        path = tmp_path / "topics.yaml"
        path.write_text(topics)
        monkeypatch.setattr(b, "TOPIC_DATA", path)

    def index(self, repo: Path):
        return json.loads((repo / "site" / "assets" / "reference-index.json").read_text())

    def test_the_outcomes_claimed_decide_the_subjects_a_term_is_filed_under(self, repo):
        # The outcome prefix is the key, not `strand` — PDP-LO2 shares a
        # strand with several MIT outcomes, so strands cut across the
        # maths/computing line rather than along it.
        maths = write(repo, "## A section\n\nProse.\n", slug="one")
        self.covers(maths, ["MIT-1.4"])
        computing = write(repo, "## A section\n\nProse.\n", slug="two")
        self.covers(computing, ["PDP-LO9"])
        both = write(repo, "## A section\n\nProse.\n", slug="three")
        self.covers(both, ["MIT-1.4", "PDP-LO9"])
        write(repo, "Prose.\n", slug="four")
        glossary(repo, "one", [{"term": "sine", "kind": "concept", "definition": "A wave."}])
        glossary(repo, "two", [{"term": "loop", "kind": "concept", "definition": "Again."}])
        glossary(repo, "three", [{"term": "plot", "kind": "function", "definition": "Draws."}])
        glossary(repo, "four", [{"term": "x", "kind": "concept", "definition": "A thing."}])
        b.build()

        by_term = {e["term"]: e for e in self.index(repo)}
        # The outcome prefix decides the subject.
        assert by_term["sine"]["subjects"] == ["maths"]
        assert by_term["loop"]["subjects"] == ["computing"]

        # A tutorial covering both files its terms under both. Not a fudge
        # to avoid choosing: seven real tutorials genuinely claim an outcome
        # from each side.
        assert by_term["plot"]["subjects"] == ["computing", "maths"]

        # A tutorial claiming nothing is left unfiled. Absence, not a guess:
        # two real tutorials claim no outcomes at all, so the panel offers
        # "unfiled" rather than inventing a subject.
        entry = by_term["x"]
        assert "subjects" not in entry
        assert "level" not in entry

    def test_the_level_comes_from_the_deepest_outcome_and_follows_the_tree(
            self, repo, monkeypatch, tmp_path):
        # Two tutorials against a stubbed chain of four outcomes: `deep`
        # claims the shallowest and the deepest, `one` claims the second.
        self.tree(monkeypatch, tmp_path,
                  "topics:\n"
                  "  MIT-1.4:\n    name: Root\n    plain: A stub.\n"
                  "  MIT-2.1:\n    name: One down\n    plain: A stub.\n    needs: [MIT-1.4]\n"
                  "  MIT-3.1:\n    name: Two down\n    plain: A stub.\n    needs: [MIT-2.1]\n"
                  "  MIT-4.1:\n    name: Three down\n    plain: A stub.\n    needs: [MIT-3.1]\n")
        path = write(repo, "## A section\n\nProse.\n", slug="deep")
        self.covers(path, ["MIT-1.4", "MIT-4.1"])
        glossary(repo, "deep", [{"term": "y", "kind": "concept", "definition": "A thing."}])
        path = write(repo, "## A section\n\nProse.\n", slug="one")
        self.covers(path, ["MIT-2.1"])
        glossary(repo, "one", [{"term": "x", "kind": "concept", "definition": "A thing."}])
        b.build()

        # The level comes from the deepest outcome, not the shallowest.
        # Rating by the easiest moment once put 150 of 222 terms in
        # "beginner"; erring deep is the kinder error, so `max()`, not `min()`.
        # Shallowest is tier 0 (beginner); deepest is tier 3 (intermediate).
        by_term = {e["term"]: e for e in self.index(repo)}
        assert by_term["y"]["level"] == "intermediate"
        assert by_term["x"]["level"] == "beginner"

        # Rearranging the tree refiles the terms. Nothing is hand-tagged, so
        # adding a prerequisite to the tree moves every term that depends on
        # it on the next build, untouched by anyone.
        self.tree(monkeypatch, tmp_path,
                  "topics:\n"
                  "  MIT-0.1:\n    name: New root\n    plain: A stub.\n"
                  "  MIT-0.2:\n    name: New second\n    plain: A stub.\n    needs: [MIT-0.1]\n"
                  "  MIT-0.3:\n    name: New third\n    plain: A stub.\n    needs: [MIT-0.2]\n"
                  "  MIT-1.4:\n    name: Root\n    plain: A stub.\n    needs: [MIT-0.3]\n"
                  "  MIT-2.1:\n    name: One down\n    plain: A stub.\n    needs: [MIT-1.4]\n"
                  "  MIT-3.1:\n    name: Two down\n    plain: A stub.\n    needs: [MIT-2.1]\n"
                  "  MIT-4.1:\n    name: Three down\n    plain: A stub.\n    needs: [MIT-3.1]\n")
        b.build()
        by_term = {e["term"]: e for e in self.index(repo)}
        assert by_term["x"]["level"] == "advanced"

    def test_the_bands_are_the_ones_chosen_against_the_real_spread(self):
        # Not an even three-way split of 0-6: the obvious alternative
        # (<=1 / <=3) collapses the real corpus to 10/28/5, making
        # "intermediate" mean almost everything.
        assert [b.level_for_tier(n) for n in range(7)] == [
            "beginner", "beginner", "beginner",
            "intermediate",
            "advanced", "advanced", "advanced",
        ]
