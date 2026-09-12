"""Mostly about the ways the curriculum map refuses to be built rather than
the prose it emits: a map that quietly links to a missing section is worse
than no map."""

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
        # Runs against the real repository, not a fixture.
        outcomes, _ = cm.load_outcomes()
        cm.load_tutorials(outcomes)  # raises if any anchor is wrong


class TestProseExcludesTheBibliography:
    """A bibliography title like `*Getting Sorted & Big O Notation.*` uses the
    same emphasis markup as a term being introduced; found when it showed up
    that way in the map's "introduced more than once" table."""

    def test_a_bibliography_title_is_not_read_as_a_term(self, tmp_path, monkeypatch):
        (tmp_path / "mod").mkdir(parents=True)
        path = tmp_path / "mod" / "sample.md"
        path.write_text(
            "# Sample\n\nSome *actual term* here.\n\n"
            "## Where to Read More\n\n"
            "Computerphile (2013). *Getting Sorted & Big O Notation.*\n"
            "<https://www.youtube.com/watch?v=kgBjXUE_Nwc>. Why this matters.\n"
        )
        monkeypatch.setattr(cm, "TUTORIALS", tmp_path)
        tutorial = cm.Tutorial(
            slug="sample", title="Sample", module="mod", series="s", order=1,
            sections=[],
        )
        prose = cm.prose_of(tutorial)
        assert "actual term" in prose
        assert "getting sorted" not in prose.lower()


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
        # The same guard CI runs, against the real committed file.
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
        for proposal in cm.load_proposals():
            outline = cm.ROOT / "planning" / "outlines" / f"{proposal['outline']}.md"
            assert outline.is_file(), f"{proposal['id']} points at a missing {outline.name}"

    def test_a_proposal_never_claims_something_already_taught(self):
        # A proposal left in place after its tutorial ships makes the plan
        # look bigger than it is, and throws off the next unplanned-gaps survey.
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
        # "Not covered" is work outstanding; this is work nobody has even
        # planned — smaller and more urgent, and what an earlier hand-count missed.
        outcomes, _ = cm.load_outcomes()
        tutorials = cm.load_tutorials(outcomes)
        found = cm.coverage(outcomes, tutorials)
        scope = cm.load_scope()
        states = {c: cm.status_of(found[c], c, scope) for c in outcomes}
        wanted = {c for c, state in states.items() if state in ("absent", "touched")}

        line = cm.unplanned_line(states, cm.load_proposals())
        if not wanted:
            assert "Everything in both descriptors is written" in line
            return
        assert str(len(wanted)) in line or len(wanted) == 1
        assert "proposal" in line

    def test_and_says_so_plainly_when_there_is_nothing_left(self):
        # Guards the zero case: "every one of the 0 outcomes still to write
        # has a proposal" is a sentence nobody wrote on purpose.
        outcomes, _ = cm.load_outcomes()
        line = cm.unplanned_line({c: "taught" for c in outcomes}, [])
        assert "Everything in both descriptors is written" in line
        assert "0" not in line

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
    """topics.yaml (not part of curriculum_map.py itself) backs the knowledge
    map's per-node glossary text; these tests keep it complete and consistent
    with the outcome list."""

    @staticmethod
    def topics() -> dict:
        path = cm.ROOT / "planning" / "curriculum" / "topics.yaml"
        return yaml.safe_load(path.read_text())["topics"]

    def test_every_outcome_is_claimed_by_a_topic(self):
        # Several topics may legitimately claim one outcome (a descriptor can
        # bundle ideas met weeks apart); only an unclaimed outcome is an error.
        outcomes, _ = cm.load_outcomes()
        served = {o for t in self.topics().values() for o in cm.outcomes_of(t)}
        missing = sorted(set(outcomes) - served)
        assert not missing, f"no topic claims {missing}"

    def test_no_topic_invents_an_outcome(self):
        outcomes, _ = cm.load_outcomes()
        for code, topic in self.topics().items():
            claimed = cm.outcomes_of(topic)
            if code.startswith("PRE-"):
                assert not claimed, f"{code} is groundwork and claims {claimed}"
                continue
            assert claimed, f"{code} names no outcome"
            for one in claimed:
                assert one in outcomes, (
                    f"{code} claims {one}, which is in no module descriptor"
                )

    def test_groundwork_is_marked_as_groundwork_and_says_as_much(self):
        # Not everything a student needs is a numbered outcome (e.g. naming
        # kinds of triangle); such topics carry a PRE- code instead of one.
        outcomes, _ = cm.load_outcomes()
        groundwork = {c for c in self.topics() if c.startswith("PRE-")}
        assert not (groundwork & set(outcomes)), (
            "a PRE- code collides with a real outcome"
        )
        assert groundwork, "no groundwork topic left; the PRE- convention is dead"
        for code in groundwork:
            topic = self.topics()[code]
            assert topic.get("name") and topic.get("plain") and topic.get("uses"), (
                f"{code} is groundwork but is not written up like a topic"
            )

    def test_every_prerequisite_is_a_real_topic(self):
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
        for code, topic in self.topics().items():
            first = topic["plain"].strip().split(".")[0].lower()
            assert not first.startswith(topic["name"].lower()), (
                f"{code} defines itself with its own name"
            )


class TestWhatTheTutorialsSayAboutTheCourse:
    """Checks against the real tutorials, not a fixture — these are about the
    course itself, so there is nowhere else for them to live."""

    def tutorials(self):
        folder = cm.ROOT / "tutorials"
        return sorted(p for p in folder.rglob("*.md"))

    def test_the_sequence_graph_has_no_repeated_node(self):
        # `order` restarts at 1 per series; when reflections moved into their
        # own series, the graph came out with two T1 nodes and a self-loop.
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
        # Prose used to name assessments directly ("ready for Skills Demo 1"),
        # tying tutorials to one institution's schedule — the part most likely to change.
        guilty = [
            path.relative_to(cm.ROOT)
            for path in self.tutorials()
            if "skills demo" in path.read_text().lower()
        ]
        assert guilty == [], f"still names a skills demo: {guilty}"


class TestSeveralReleasesOfOneTutorial:
    """A tutorial with several releases is a folder of files, all with real
    frontmatter; reading the folder naively counts it several times — found
    when re-releasing four tutorials turned thirty-one into thirty-five."""

    def release(self, repo, name: str, version: str, status: str = "live",
                slug: str = "sample", heading: str = "A Real Section") -> Path:
        folder = repo / "tutorials" / "demo" / slug
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / name
        path.write_text(
            f'---\ntitle: "Sample"\nslug: {slug}\nmodule: demo\n'
            f'year: "2026-2027"\nseries: s\nversion: {version}\n'
            f"status: {status}\n---\n\n# Sample\n\n## {heading}\n\nProse.\n"
        )
        (repo / "tutorials" / "demo" / "s.order.yaml").write_text(
            f"order:\n  - {slug}\n")
        return path

    def test_one_tutorial_however_many_releases(self, repo):
        self.release(repo, "v2026.08.23.1.md", "2026.08.23.1")
        self.release(repo, "v2026.08.23.2.md", "2026.08.23.2")
        self.release(repo, "sample.md", "2026.08.24.1")
        assert len(cm.load_tutorials(cm.load_outcomes()[0])) == 1

    def test_the_newest_live_release_is_the_one_reported(self, repo):
        old = self.release(repo, "v2026.08.23.1.md", "2026.08.23.1")
        old.write_text(old.read_text().replace('title: "Sample"', 'title: "The Old Name"'))
        new = self.release(repo, "sample.md", "2026.08.24.1")
        new.write_text(new.read_text().replace('title: "Sample"', 'title: "The New Name"'))
        found = cm.load_tutorials(cm.load_outcomes()[0])
        assert [t.title for t in found] == ["The New Name"]

    def test_a_beta_release_does_not_displace_the_live_one(self, repo):
        # Must match build.py's own rule: newest live, not newest overall.
        live = self.release(repo, "v2026.08.23.1.md", "2026.08.23.1", status="live")
        self.release(repo, "sample.md", "2026.08.24.1", status="beta")
        assert cm.newest_live(sorted(
            (repo / "tutorials").rglob("*.md"))) == {live}

    def test_with_nothing_live_the_newest_still_answers(self, repo):
        self.release(repo, "v2026.08.23.1.md", "2026.08.23.1", status="beta")
        newest = self.release(repo, "sample.md", "2026.08.24.1", status="beta")
        assert cm.newest_live(sorted(
            (repo / "tutorials").rglob("*.md"))) == {newest}

    def test_two_different_tutorials_are_still_two(self, repo):
        self.release(repo, "sample.md", "2026.08.24.1", slug="sample")
        self.release(repo, "other.md", "2026.08.24.1", slug="other")
        (repo / "tutorials" / "demo" / "s.order.yaml").write_text(
            "order:\n  - sample\n  - other\n")
        assert len(cm.load_tutorials(cm.load_outcomes()[0])) == 2
