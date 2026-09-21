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
    (tmp_path / "tutorials").mkdir(parents=True)
    (tmp_path / "courses").mkdir(parents=True)
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
    monkeypatch.setattr(cm, "COURSES", tmp_path / "courses")
    monkeypatch.setattr(cm, "OUTCOMES", tmp_path / "planning" / "curriculum" / "outcomes.yaml")
    monkeypatch.setattr(cm, "OUT_OF_SCOPE", tmp_path / "planning" / "curriculum" / "out-of-scope.yaml")
    monkeypatch.setattr(cm, "PROPOSED", tmp_path / "planning" / "curriculum" / "proposed.yaml")
    monkeypatch.setattr(cm, "MAP", tmp_path / "planning" / "CURRICULUM_MAP.md")
    return tmp_path


def course_file(repo, ids: list[str], course: str = "demo", series: str = "S") -> None:
    """`courses/<course>.yaml` with one series listing `ids` in order."""
    (repo / "courses" / f"{course}.yaml").write_text(
        f"title: Demo\ncontents:\n  - title: {series}\n    tutorials:\n"
        + "".join(f"      - {i}\n" for i in ids)
    )


def write_tutorial(repo, covers: str = "", heading: str = "A Real Section"):
    folder = repo / "tutorials" / "sample"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "sample.md").write_text(
        '---\ntitle: "Sample"\n'
        'year: "2026-2027"\nversion: 2026.08.23.1\n'
        + covers
        + f"---\n\n# Sample\n\n## {heading}\n\nProse.\n"
    )
    course_file(repo, ["sample"])


class TestWhatItRefusesToBuild:
    @pytest.mark.parametrize(
        "covers, match",
        [
            pytest.param(
                "covers:\n  a-real-section:\n    covers: [DEMO-9.9]\n",
                "no module descriptor lists",
                id="outcome-no-descriptor-lists",
            ),
            pytest.param(
                "covers:\n  no-such-section:\n    covers: [DEMO-1.1]\n",
                "not a section of it",
                id="section-tutorial-lacks",
            ),
            pytest.param(
                "covers:\n  wrong:\n    covers: [DEMO-1.1]\n",
                "a-real-section",
                id="error-names-real-sections",
            ),
        ],
    )
    def test_a_bad_covers_entry_stops_it(self, repo, covers, match):
        write_tutorial(repo, covers)
        outcomes, _ = cm.load_outcomes()
        with pytest.raises(cm.MapError, match=match):
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
            slug="sample", title="Sample", course="mod", series="s", order=1,
            sections=[],
        )
        prose = cm.prose_of(tutorial)
        assert "actual term" in prose
        assert "getting sorted" not in prose.lower()


class TestStatus:
    def covered(self, **kw):
        return {"covers": kw.get("covers", []), "touches": kw.get("touches", [])}

    @pytest.mark.parametrize(
        "kwargs, code, scope, expected",
        [
            pytest.param({"covers": [object()]}, "", None, "taught", id="taught"),
            pytest.param({"touches": [object()]}, "", None, "touched", id="touched"),
            pytest.param({}, "", None, "absent", id="nothing-is-a-gap"),
            pytest.param(
                {}, "X", {"outcomes": {"X": {}}, "partial": {}}, "excluded",
                id="deliberate-exclusion",
            ),
            pytest.param(
                {}, "X", {"outcomes": {}, "partial": {"X": {}}}, "absent",
                id="narrowing-something-unwritten",
            ),
            pytest.param(
                {"covers": [object()]}, "X", {"outcomes": {}, "partial": {"X": {}}},
                "partial", id="narrowing-something-written",
            ),
        ],
    )
    def test_status_of(self, kwargs, code, scope, expected):
        assert cm.status_of(self.covered(**kwargs), code, scope) == expected


class TestBackReferences:
    def order_file(self, repo, slugs):
        course_file(repo, slugs)

    @pytest.mark.parametrize(
        "t2_text, expected",
        [
            pytest.param(
                "Recall your work from Counting Carefully.\n",
                {"t2": {1}, "t1": set()},
                id="finds-an-earlier-tutorial",
            ),
            pytest.param(
                "Covered in Counting Carefully and later in What Are the Chances.\n",
                {"t1": set()},
                id="ignores-self-and-later",
            ),
        ],
    )
    def test_back_references(self, repo, t2_text, expected):
        titles = {1: "Counting Carefully", 2: "What Are the Chances"}
        texts = {1: "Prose.\n", 2: t2_text}
        for n in (1, 2):
            (repo / "tutorials" / f"t{n}").mkdir()
            (repo / "tutorials" / f"t{n}" / f"t{n}.md").write_text(
                f'---\ntitle: "{titles[n]}"\n'
                f'year: "2026-2027"\nversion: 2026.08.23.1\n---\n\n# {titles[n]}\n\n'
                + texts[n]
            )
        self.order_file(repo, ["t1", "t2"])
        outcomes, _ = cm.load_outcomes()
        refs = cm.back_references(cm.load_tutorials(outcomes))
        for key, val in expected.items():
            assert refs[key] == val


class TestTheRealMap:
    def test_it_is_committed_current(self):
        # The same guard CI runs, against the real committed file.
        assert cm.MAP.read_text() == cm.render()

    def test_every_out_of_scope_code_is_a_real_outcome(self):
        outcomes, _ = cm.load_outcomes()
        scope = cm.load_scope()
        for code in list(scope["outcomes"]) + list(scope["partial"]):
            assert code in outcomes, f"{code} is not an outcome in any descriptor"

    def test_every_proposal_is_well_formed(self):
        outcomes, _ = cm.load_outcomes()
        for proposal in cm.load_proposals():
            for code in (proposal.get("covers") or []) + (proposal.get("optional") or []):
                assert code in outcomes, f"{proposal['id']} names {code}"
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

    def test_unplanned_line_edge_cases(self):
        outcomes, _ = cm.load_outcomes()

        # Guards the zero case: "every one of the 0 outcomes still to write
        # has a proposal" is a sentence nobody wrote on purpose.
        nothing_left = cm.unplanned_line({c: "taught" for c in outcomes}, [])
        assert "Everything in both descriptors is written" in nothing_left
        assert "0" not in nothing_left

        # Every outcome with no proposal gets named.
        states = {c: "absent" for c in outcomes}
        all_unplanned = cm.unplanned_line(states, [{"covers": []}])
        for code in outcomes:
            assert f"`{code}`" in all_unplanned

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

    def test_topics_and_outcomes_correspond(self):
        # Several topics may legitimately claim one outcome (a descriptor can
        # bundle ideas met weeks apart); only an unclaimed outcome is an error.
        # The reverse must also hold: no topic invents one that isn't real.
        outcomes, _ = cm.load_outcomes()
        topics = self.topics()
        served = {o for t in topics.values() for o in cm.outcomes_of(t)}
        missing = sorted(set(outcomes) - served)
        assert not missing, f"no topic claims {missing}"

        for code, topic in topics.items():
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

    def test_prerequisites_are_real_and_not_self_referential(self):
        topics = self.topics()
        for code, topic in topics.items():
            needs = topic.get("needs") or []
            assert code not in needs, f"{code} requires itself"
            for need in needs:
                assert need in topics, f"{code} needs {need}, which does not exist"

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
            # The description should avoid the jargon it exists to replace.
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
        folder = repo / "tutorials" / slug
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / name
        path.write_text(
            f'---\ntitle: "Sample"\n'
            f'year: "2026-2027"\nversion: {version}\n'
            f"status: {status}\n---\n\n# Sample\n\n## {heading}\n\nProse.\n"
        )
        course_file(repo, [slug])
        return path

    @pytest.mark.parametrize(
        "releases, expected_count",
        [
            pytest.param(
                [
                    ("v2026.08.23.1.md", "2026.08.23.1", "live", "sample"),
                    ("v2026.08.23.2.md", "2026.08.23.2", "live", "sample"),
                    ("sample.md", "2026.08.24.1", "live", "sample"),
                ],
                1,
                id="one-tutorial-however-many-releases",
            ),
            pytest.param(
                [
                    ("sample.md", "2026.08.24.1", "live", "sample"),
                    ("other.md", "2026.08.24.1", "live", "other"),
                ],
                2,
                id="two-different-tutorials-are-still-two",
            ),
        ],
    )
    def test_tutorial_count_by_releases(self, repo, releases, expected_count):
        slugs = []
        for name, version, status, slug in releases:
            self.release(repo, name, version, status, slug)
            slugs.append(slug)
        course_file(repo, sorted(set(slugs)))
        assert len(cm.load_tutorials(cm.load_outcomes()[0])) == expected_count

    def test_the_newest_live_release_is_the_one_reported(self, repo):
        old = self.release(repo, "v2026.08.23.1.md", "2026.08.23.1")
        old.write_text(old.read_text().replace('title: "Sample"', 'title: "The Old Name"'))
        new = self.release(repo, "sample.md", "2026.08.24.1")
        new.write_text(new.read_text().replace('title: "Sample"', 'title: "The New Name"'))
        found = cm.load_tutorials(cm.load_outcomes()[0])
        assert [t.title for t in found] == ["The New Name"]

    @pytest.mark.parametrize(
        "old_status, new_status, which_wins",
        [
            pytest.param("live", "beta", "old", id="beta-does-not-displace-live"),
            pytest.param("beta", "beta", "new", id="nothing-live-newest-still-answers"),
        ],
    )
    def test_newest_live(self, repo, old_status, new_status, which_wins):
        # Must match build.py's own rule: newest live, not newest overall.
        old = self.release(repo, "v2026.08.23.1.md", "2026.08.23.1", status=old_status)
        new = self.release(repo, "sample.md", "2026.08.24.1", status=new_status)
        expected = {old} if which_wins == "old" else {new}
        assert cm.newest_live(sorted((repo / "tutorials").rglob("*.md"))) == expected


class TestEmphasisReadsBoldItalics:
    def test_a_term_in_bold_italics_is_found_like_a_plain_italic_one(self):
        prose = "One *frame* and a ***frame rate***, but not **bold** alone."
        found = [plain or bold for plain, bold in cm.EMPHASIS_RE.findall(prose)]
        assert found == ["frame", "frame rate"]
