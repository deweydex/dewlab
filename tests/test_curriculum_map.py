"""Tests for the curriculum map generator.

The map's whole value is that it cannot disagree with the tutorials. These tests
are mostly about the ways it refuses to be built rather than the prose it emits:
a map that quietly links to a section that does not exist is worse than no map.

    python3 -m pytest tests -q
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import curriculum_map as cm  # noqa: E402


@pytest.fixture()
def repo(tmp_path, monkeypatch):
    """A small curriculum: two outcomes, one tutorial covering one of them."""
    (tmp_path / "tutorials" / "demo").mkdir(parents=True)
    (tmp_path / "planning" / "curriculum").mkdir(parents=True)

    (tmp_path / "planning" / "curriculum" / "outcomes.yaml").write_text(
        "modules:\n"
        "  DEMO:\n"
        "    title: Demo Module\n"
        "    code: '0000'\n"
        "    sections:\n"
        "      '1': First things\n"
        "outcomes:\n"
        "  - code: DEMO-1.1\n    title: The first outcome\n    strand: one\n"
        "  - code: DEMO-1.2\n    title: The second outcome\n    strand: one\n"
    )
    monkeypatch.setattr(cm, "ROOT", tmp_path)
    monkeypatch.setattr(cm, "TUTORIALS", tmp_path / "tutorials")
    monkeypatch.setattr(cm, "OUTCOMES", tmp_path / "planning" / "curriculum" / "outcomes.yaml")
    monkeypatch.setattr(cm, "OUT_OF_SCOPE", tmp_path / "planning" / "curriculum" / "out-of-scope.yaml")
    monkeypatch.setattr(cm, "PROPOSED", tmp_path / "planning" / "curriculum" / "proposed.yaml")
    monkeypatch.setattr(cm, "MAP", tmp_path / "planning" / "CURRICULUM_MAP.md")
    return tmp_path


def write_tutorial(repo, covers: str = "", heading: str = "A Real Section"):
    (repo / "tutorials" / "demo" / "sample.md").write_text(
        '---\ntitle: "Sample"\nslug: sample\nmodule: demo\n'
        'year: "2026-2027"\nseries: s\norder: 1\nversion: 2026.08.23.1\n'
        + covers
        + f"---\n\n# Sample\n\n## {heading}\n\nProse.\n"
    )


class TestWhatItRefusesToBuild:
    def test_an_outcome_no_descriptor_lists_stops_it(self, repo):
        write_tutorial(repo, "covers:\n  a-real-section:\n    covers: [DEMO-9.9]\n")
        outcomes, _ = cm.load_outcomes()
        with pytest.raises(cm.MapError, match="no module descriptor lists"):
            cm.load_tutorials(outcomes)

    def test_a_section_the_tutorial_does_not_have_stops_it(self, repo):
        write_tutorial(repo, "covers:\n  no-such-section:\n    covers: [DEMO-1.1]\n")
        outcomes, _ = cm.load_outcomes()
        with pytest.raises(cm.MapError, match="not a section of it"):
            cm.load_tutorials(outcomes)

    def test_the_error_says_which_sections_there_are(self, repo):
        write_tutorial(repo, "covers:\n  wrong:\n    covers: [DEMO-1.1]\n")
        outcomes, _ = cm.load_outcomes()
        with pytest.raises(cm.MapError, match="a-real-section"):
            cm.load_tutorials(outcomes)

    def test_an_outcome_listed_twice_stops_it(self, repo):
        path = repo / "planning" / "curriculum" / "outcomes.yaml"
        path.write_text(path.read_text() + "  - code: DEMO-1.1\n    title: Again\n    strand: one\n")
        with pytest.raises(cm.MapError, match="listed twice"):
            cm.load_outcomes()


class TestTheAnchors:
    def test_a_heading_becomes_the_anchor_the_site_uses(self):
        assert cm.anchor_for("Variables: Giving Names to Things") == (
            "variables-giving-names-to-things"
        )
        assert cm.anchor_for("If-Else: Two Paths") == "if-else-two-paths"
        assert cm.anchor_for("What Are the Chances?") == "what-are-the-chances"

    def test_every_declared_section_in_the_real_tutorials_exists(self):
        """The map is only as good as this. Runs against the real repository."""
        outcomes, _ = cm.load_outcomes()
        cm.load_tutorials(outcomes)  # raises if any anchor is wrong


class TestStatus:
    def covered(self, **kw):
        return {"covers": kw.get("covers", []), "touches": kw.get("touches", [])}

    def test_a_section_that_teaches_it_counts_as_taught(self):
        assert cm.status_of(self.covered(covers=[object()])) == "taught"

    def test_a_section_that_only_uses_it_does_not(self):
        assert cm.status_of(self.covered(touches=[object()])) == "touched"

    def test_nothing_at_all_is_a_gap(self):
        assert cm.status_of(self.covered()) == "absent"

    def test_a_deliberate_exclusion_is_not_a_gap(self):
        scope = {"outcomes": {"X": {}}, "partial": {}}
        assert cm.status_of(self.covered(), "X", scope) == "excluded"

    def test_narrowing_something_unwritten_leaves_it_a_gap(self):
        """Deciding to teach half of something does not teach half of it."""
        scope = {"outcomes": {}, "partial": {"X": {}}}
        assert cm.status_of(self.covered(), "X", scope) == "absent"

    def test_narrowing_something_written_is_its_own_state(self):
        scope = {"outcomes": {}, "partial": {"X": {}}}
        assert cm.status_of(self.covered(covers=[object()]), "X", scope) == "partial"


class TestBackReferences:
    def order_file(self, repo, slugs):
        (repo / "tutorials" / "demo" / "s.order.yaml").write_text(
            "order:\n" + "".join(f"  - {s}\n" for s in slugs)
        )

    def test_it_finds_an_earlier_tutorial_named_in_the_text(self, repo):
        """By title now that the numbers are gone — which is also what a
        tutorial would naturally write."""
        titles = {1: "Counting Carefully", 2: "What Are the Chances"}
        for n in (1, 2):
            (repo / "tutorials" / "demo" / f"t{n}.md").write_text(
                f'---\ntitle: "{titles[n]}"\nslug: t{n}\nmodule: demo\n'
                f'year: "2026-2027"\nseries: s\nversion: 2026.08.23.1\n---\n\n# {titles[n]}\n\n'
                + ("Recall your work from Counting Carefully.\n" if n == 2 else "Prose.\n")
            )
        self.order_file(repo, ["t1", "t2"])
        outcomes, _ = cm.load_outcomes()
        refs = cm.back_references(cm.load_tutorials(outcomes))
        assert refs["t2"] == {1}
        assert refs["t1"] == set()

    def test_it_ignores_a_tutorial_naming_itself_or_a_later_one(self, repo):
        titles = {1: "Counting Carefully", 2: "What Are the Chances"}
        for n in (1, 2):
            (repo / "tutorials" / "demo" / f"t{n}.md").write_text(
                f'---\ntitle: "{titles[n]}"\nslug: t{n}\nmodule: demo\n'
                f'year: "2026-2027"\nseries: s\nversion: 2026.08.23.1\n---\n\n# {titles[n]}\n\n'
                "Covered in Counting Carefully and later in What Are the Chances.\n"
            )
        self.order_file(repo, ["t1", "t2"])
        outcomes, _ = cm.load_outcomes()
        refs = cm.back_references(cm.load_tutorials(outcomes))
        assert refs["t1"] == set()


class TestTheRealMap:
    def test_it_is_committed_current(self):
        """The same guard CI runs. A stale map is a misleading one."""
        assert cm.MAP.read_text() == cm.render()

    def test_every_out_of_scope_code_is_a_real_outcome(self):
        outcomes, _ = cm.load_outcomes()
        scope = cm.load_scope()
        for code in list(scope["outcomes"]) + list(scope["partial"]):
            assert code in outcomes, f"{code} is not an outcome in any descriptor"

    def test_every_proposal_names_real_outcomes(self):
        outcomes, _ = cm.load_outcomes()
        for proposal in cm.load_proposals():
            for code in (proposal.get("covers") or []) + (proposal.get("optional") or []):
                assert code in outcomes, f"{proposal['id']} names {code}"

    def test_every_proposal_has_an_outline(self):
        """A proposal without an outline is a title and a wish."""
        for proposal in cm.load_proposals():
            outline = cm.ROOT / "planning" / "outlines" / f"{proposal['outline']}.md"
            assert outline.is_file(), f"{proposal['id']} points at a missing {outline.name}"

    def test_a_proposal_never_claims_something_already_taught(self):
        """A proposal left in place after its tutorial shipped would make the
        plan look larger than it is, and make the next survey wrong."""
        outcomes, _ = cm.load_outcomes()
        tutorials = cm.load_tutorials(outcomes)
        found = cm.coverage(outcomes, tutorials)
        scope = cm.load_scope()
        for proposal in cm.load_proposals():
            for code in proposal.get("covers") or []:
                state = cm.status_of(found[code], code, scope)
                assert state in ("absent", "touched"), (
                    f"{proposal['id']} proposes to teach {code}, which is "
                    f"already {state}"
                )

    def test_the_map_says_how_many_gaps_nobody_has_planned(self):
        """The number worth acting on. "Not covered" is the work outstanding;
        this is the work nobody has thought about, which is smaller and more
        urgent — and it is what the first survey of this got wrong."""
        outcomes, _ = cm.load_outcomes()
        tutorials = cm.load_tutorials(outcomes)
        found = cm.coverage(outcomes, tutorials)
        scope = cm.load_scope()
        states = {c: cm.status_of(found[c], c, scope) for c in outcomes}
        wanted = {c for c, state in states.items() if state in ("absent", "touched")}

        line = cm.unplanned_line(states, cm.load_proposals())
        assert str(len(wanted)) in line
        assert "proposal" in line

    def test_it_names_the_outcomes_that_have_no_proposal(self):
        outcomes, _ = cm.load_outcomes()
        states = {c: "absent" for c in outcomes}
        line = cm.unplanned_line(states, [{"covers": []}])
        for code in outcomes:
            assert f"`{code}`" in line

    def test_the_outlines_index_lists_every_outline(self):
        folder = cm.ROOT / "planning" / "outlines"
        index = (folder / "README.md").read_text()
        for path in folder.glob("*.md"):
            if path.name != "README.md":
                assert path.name in index, f"{path.name} is not in the outlines index"


class TestTheTopicGlossary:
    """`topics.yaml` says, for every learning outcome, what the topic actually
    is and where it turns up in computing. It is what the knowledge map shows
    when a node is opened, and it stands on its own as a glossary.

    These tests are about it staying complete and consistent with the outcome
    list, because a map with a node missing its description is a dead end.
    """

    @staticmethod
    def topics() -> dict:
        path = cm.ROOT / "planning" / "curriculum" / "topics.yaml"
        return yaml.safe_load(path.read_text())["topics"]

    def test_every_outcome_has_a_topic(self):
        outcomes, _ = cm.load_outcomes()
        missing = sorted(set(outcomes) - set(self.topics()))
        assert not missing, f"no topic written for {missing}"

    def test_no_topic_invents_an_outcome(self):
        """A `MIT-` or `PDP-` code has to be a real one, or it is a typo that
        silently detaches a topic from the descriptor it claims to come from.

        `PRE-` codes are deliberately not outcomes — see the next test."""
        outcomes, _ = cm.load_outcomes()
        claimed = {c for c in self.topics() if not c.startswith("PRE-")}
        unknown = sorted(claimed - set(outcomes))
        assert not unknown, f"{unknown} are not in any module descriptor"

    def test_groundwork_is_marked_as_groundwork_and_says_as_much(self):
        """Not everything a student needs is a numbered outcome. Naming the
        kinds of triangle is nobody's learning outcome and every later rule
        about triangles assumes it. Those topics carry a `PRE-` code so the map
        can show the prerequisite without pretending a descriptor asked for
        it."""
        outcomes, _ = cm.load_outcomes()
        groundwork = {c for c in self.topics() if c.startswith("PRE-")}
        assert not (groundwork & set(outcomes)), (
            "a PRE- code collides with a real outcome"
        )
        for code in groundwork:
            topic = self.topics()[code]
            assert topic.get("name") and topic.get("plain") and topic.get("uses"), (
                f"{code} is groundwork but is not written up like a topic"
            )

    def test_every_prerequisite_is_a_real_topic(self):
        """A `needs` pointing nowhere is an arrow the map cannot draw."""
        topics = self.topics()
        for code, topic in topics.items():
            for need in topic.get("needs") or []:
                assert need in topics, f"{code} needs {need}, which does not exist"

    def test_nothing_requires_itself(self):
        for code, topic in self.topics().items():
            assert code not in (topic.get("needs") or [])

    def test_the_prerequisites_have_no_cycles(self):
        """A cycle would make the tiers of a tech tree impossible to compute."""
        topics = self.topics()
        state: dict[str, int] = {}

        def walk(code: str, trail: list[str]) -> None:
            if state.get(code) == 2:
                return
            assert state.get(code) != 1, f"cycle: {' -> '.join(trail + [code])}"
            state[code] = 1
            for need in topics[code].get("needs") or []:
                walk(need, trail + [code])
            state[code] = 2

        for code in topics:
            walk(code, [])

    def test_every_topic_says_what_it_is_and_where_it_is_used(self):
        for code, topic in self.topics().items():
            assert topic.get("name"), f"{code} has no name"
            assert len(topic.get("plain", "").split()) >= 12, (
                f"{code}'s description is too short to be worth reading"
            )
            assert topic.get("uses"), f"{code} lists no applications"

    def test_the_descriptions_avoid_the_jargon_they_are_there_to_replace(self):
        """A plain-English description that opens with the term itself has not
        explained anything."""
        for code, topic in self.topics().items():
            first = topic["plain"].strip().split(".")[0].lower()
            assert not first.startswith(topic["name"].lower()), (
                f"{code} defines itself with its own name"
            )


class TestWhatTheTutorialsSayAboutTheCourse:
    """Checks against the real tutorials, not a fixture. These are about the
    course rather than the converter, and there is nowhere else for them."""

    def tutorials(self):
        folder = cm.ROOT / "tutorials"
        return sorted(p for p in folder.rglob("*.md"))

    def test_the_sequence_graph_has_no_repeated_node(self):
        """`order` restarts at 1 in each series. When reflections moved into
        their own, the mermaid graph came out with two nodes called T1 and an
        arrow from one of them to itself."""
        # The map holds several mermaid blocks; the sequence one is whichever
        # declares T-nodes. Taking "the first block" silently tested the strand
        # diagram instead, and passed against a map that was visibly broken.
        blocks = [
            b for b in re.findall(r"```mermaid\n(.*?)```", cm.MAP.read_text(), re.S)
            if re.search(r"^  T\d+\[", b, re.MULTILINE)
        ]
        assert blocks, "no tutorial sequence graph in the map"
        for block in blocks:
            ids = re.findall(r"^  (T\d+)\[", block, re.MULTILINE)
            assert len(ids) == len(set(ids)), f"repeated node: {sorted(ids)}"
            assert not re.search(r"^  (T\d+) --> \1$", block, re.MULTILINE)

    def test_no_tutorial_mentions_a_skills_demo(self):
        """The assessments were named throughout the prose — "you are now ready
        for Skills Demo 1", "the last tutorial before Skills Demo 2B". That ties
        the tutorials to one institution's assessment schedule, and the schedule
        is the thing most likely to change. A tutorial can say what a student is
        ready to build without naming the paperwork."""
        guilty = [
            path.relative_to(cm.ROOT)
            for path in self.tutorials()
            if "skills demo" in path.read_text().lower()
        ]
        assert guilty == [], f"still names a skills demo: {guilty}"
