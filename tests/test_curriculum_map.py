"""Tests for the curriculum map generator.

The map's whole value is that it cannot disagree with the tutorials. These tests
are mostly about the ways it refuses to be built rather than the prose it emits:
a map that quietly links to a section that does not exist is worse than no map.

    python3 -m pytest tests -q
"""

from __future__ import annotations

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
        'year: "2026-2027"\nseries: s\norder: 1\nversion: 1\n'
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
    def test_it_finds_an_earlier_tutorial_named_in_the_text(self, repo):
        for n in (1, 2):
            (repo / "tutorials" / "demo" / f"t{n}.md").write_text(
                f'---\ntitle: "T{n}"\nslug: t{n}\nmodule: demo\nyear: "2026-2027"\n'
                f"series: s\norder: {n}\nversion: 1\n---\n\n# T{n}\n\n"
                + ("Recall your work from Tutorial 1.\n" if n == 2 else "Prose.\n")
            )
        outcomes, _ = cm.load_outcomes()
        refs = cm.back_references(cm.load_tutorials(outcomes))
        assert refs["t2"] == {1}
        assert refs["t1"] == set()

    def test_it_ignores_a_reference_to_itself_or_later(self, repo):
        (repo / "tutorials" / "demo" / "t1.md").write_text(
            '---\ntitle: "T1"\nslug: t1\nmodule: demo\nyear: "2026-2027"\n'
            "series: s\norder: 1\nversion: 1\n---\n\n# T1\n\n"
            "Covered in Tutorial 1 and again in Tutorial 5.\n"
        )
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

    def test_the_outlines_index_lists_every_outline(self):
        folder = cm.ROOT / "planning" / "outlines"
        index = (folder / "README.md").read_text()
        for path in folder.glob("*.md"):
            if path.name != "README.md":
                assert path.name in index, f"{path.name} is not in the outlines index"
