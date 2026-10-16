"""Mostly about the ways the curriculum map refuses to be built rather than
the prose it emits: a map that quietly links to a missing section is worse
than no map."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

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
        ],
    )
    def test_a_bad_covers_entry_stops_it(self, repo, covers, match):
        write_tutorial(repo, covers)
        outcomes, _ = cm.load_outcomes()
        with pytest.raises(cm.MapError, match=match):
            cm.load_tutorials(outcomes)

    def test_a_claim_for_a_section_the_page_no_longer_has_is_left_out_and_noted(self, repo, capsys):
        # A teacher cut the section (DECISIONS_LOG 7.299). The note names the
        # sections the page has, so the claim can be moved to one of them.
        write_tutorial(repo, "covers:\n  no-such-section:\n    covers: [DEMO-1.1]\n")
        outcomes, _ = cm.load_outcomes()
        tutorials = cm.load_tutorials(outcomes)
        assert all(not t.sections for t in tutorials)
        err = capsys.readouterr().err
        assert "no-such-section" in err and "a-real-section" in err

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

    def test_the_heading_is_found_whatever_its_capitals(self, tmp_path, monkeypatch):
        # Most pages write "Where to read more"; matching only the capitalised
        # form counted every title in their bibliographies as a term.
        (tmp_path / "mod").mkdir(parents=True)
        (tmp_path / "mod" / "sample.md").write_text(
            "# Sample\n\nSome *actual term* here.\n\n"
            "## Where to read more\n\n"
            "Stand-up Maths (2020). *The Datasaurus Dozen.*\n"
        )
        monkeypatch.setattr(cm, "TUTORIALS", tmp_path)
        tutorial = cm.Tutorial(
            slug="sample", title="Sample", course="mod", series="s", order=1,
            sections=[],
        )
        prose = cm.prose_of(tutorial)
        assert "actual term" in prose
        assert "datasaurus" not in prose.lower()


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


class TestTheUnplannedLine:
    """The sentence that says how much of the plan nobody has proposed a
    tutorial for. Against the fixture's two outcomes, not the real plan."""

    def test_the_map_says_how_many_gaps_nobody_has_planned(self, repo):
        # "Not covered" is work outstanding; this is work nobody has even
        # planned — smaller and more urgent, and what an earlier hand-count missed.
        write_tutorial(repo)
        outcomes, _ = cm.load_outcomes()
        found = cm.coverage(outcomes, cm.load_tutorials(outcomes))
        states = {c: cm.status_of(found[c], c, cm.load_scope()) for c in outcomes}
        line = cm.unplanned_line(states, [])
        assert "2" in line and "proposal" in line

    def test_unplanned_line_edge_cases(self, repo):
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


class TestPlanningProblems:
    """What `--check` reports about the planning files disagreeing with each
    other. A report, never a build failure: no page reads these files."""

    def plan(self, repo, monkeypatch, proposed: str, topics: str) -> list[str]:
        monkeypatch.setattr(cm, "TOPICS", repo / "planning" / "curriculum" / "topics.yaml")
        monkeypatch.setattr(cm, "OUTLINES", repo / "planning" / "outlines")
        (repo / "planning" / "outlines").mkdir(parents=True)
        (repo / "planning" / "outlines" / "README.md").write_text("- first.md\n")
        (repo / "planning" / "outlines" / "first.md").write_text("# First\n")
        (repo / "planning" / "curriculum" / "out-of-scope.yaml").write_text("outcomes: []\npartial: []\n")
        (repo / "planning" / "curriculum" / "proposed.yaml").write_text(proposed)
        (repo / "planning" / "curriculum" / "topics.yaml").write_text(topics)
        write_tutorial(repo)
        return cm.planning_problems("")

    def test_files_that_agree_have_nothing_to_report(self, repo, monkeypatch):
        topics = ("topics:\n  T1:\n    name: One\n    plain: p\n    outcome: DEMO-1.1\n"
                  "  T2:\n    name: Two\n    plain: p\n    outcome: DEMO-1.2\n")
        assert self.plan(repo, monkeypatch, "proposed: []\n", topics) == []

    def test_each_disagreement_is_named(self, repo, monkeypatch):
        proposed = ("proposed:\n  - id: p1\n    outline: missing\n    covers: [DEMO-9.9]\n")
        topics = "topics:\n  T1:\n    name: One\n    plain: p\n    outcome: DEMO-1.1\n"
        problems = self.plan(repo, monkeypatch, proposed, topics)
        assert any("p1 names DEMO-9.9" in p for p in problems)
        assert any("missing outline" in p for p in problems)
        assert any("no topic in topics.yaml claims DEMO-1.2" in p for p in problems)

    def test_a_topic_graph_that_cannot_be_drawn_is_named(self, repo, monkeypatch):
        topics = ("topics:\n"
                  "  T1:\n    name: One\n    plain: p\n    outcome: DEMO-1.1\n    needs: [T2]\n"
                  "  T2:\n    name: Two\n    plain: p\n    outcome: DEMO-1.2\n    needs: [T1, T9]\n"
                  "  T3:\n    plain: p\n    outcome: DEMO-1.2\n")
        problems = self.plan(repo, monkeypatch, "proposed: []\n", topics)
        assert any("T2 needs T9" in p for p in problems)
        assert any("cycle" in p for p in problems)
        assert any("T3 has no name" in p for p in problems)


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


def test_a_node_label_keeps_the_words_before_a_colon():
    """A title's topic often comes before its colon. Only the old
    "Tutorial N: " numbering is dropped, since the node is numbered."""
    assert cm.node_label("Lists: keeping many values in order") == \
        "Lists: keeping many values in order"
    assert cm.node_label("Tutorial 14: Expressions Come Alive") == \
        "Expressions Come Alive"


class TestALaterUseIsNotAnIntroduction:
    def test_a_marked_later_use_reads_as_the_plain_word(self, tmp_path, monkeypatch):
        # `*matrix*{.term}` marks a later use for the hover definition. It is
        # not an introduction, and its `{.term}` is not the word "term".
        (tmp_path / "mod").mkdir(parents=True)
        (tmp_path / "mod" / "sample.md").write_text(
            "# Sample\n\nA new *vector* here, and a *matrix*{.term} from before.\n"
        )
        monkeypatch.setattr(cm, "TUTORIALS", tmp_path)
        tutorial = cm.Tutorial(
            slug="sample", title="Sample", course="mod", series="s", order=1,
            sections=[],
        )
        prose = cm.prose_of(tutorial)
        found = [plain or bold for plain, bold in cm.EMPHASIS_RE.findall(prose)]
        assert found == ["vector"]
        assert "matrix from before" in prose
        assert "term" not in prose
