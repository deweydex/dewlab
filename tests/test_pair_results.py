"""Tests for the pair-judgement report.

The report's job is to say what a pile of judgements implies without touching
`topics.yaml`. These tests are about the findings that would cost real work if
they were missed: a loop, a disagreement, and an arrow nobody kept.

    python3 -m pytest tests -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import pair_results as pr  # noqa: E402


TOPICS = {
    "A": {"name": "Alpha", "needs": []},
    "B": {"name": "Beta", "needs": ["A"]},
    "C": {"name": "Gamma", "needs": []},
}


@pytest.fixture()
def pairs(tmp_path, monkeypatch):
    """An empty batch directory, wired into the module."""
    d = tmp_path / "pairs"
    d.mkdir()
    monkeypatch.setattr(pr, "PAIRS", d)
    return d


def batch(d: Path, name: str, by: str, judgements: list[dict], **rest) -> None:
    body = {"by": by, "judgements": judgements}
    body.update(rest)
    (d / name).write_text(json.dumps(body))


def test_a_new_pair_becomes_an_arrow_to_add(pairs):
    batch(pairs, "1.json", "josh",
          [{"pair": ["A", "C"], "verdict": "needs", "first": "C"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "| Gamma | Alpha | 1 | yes |" in out


def test_an_arrow_the_graph_already_has_is_not_listed_again(pairs):
    batch(pairs, "1.json", "josh",
          [{"pair": ["A", "B"], "verdict": "needs", "first": "A"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert out.split("## Arrows to add")[1].split("\n## ")[0].strip().endswith(
        "Nothing new.")


def test_unrelated_flags_an_arrow_the_graph_does_have(pairs):
    batch(pairs, "1.json", "josh", [{"pair": ["A", "B"], "verdict": "unrelated"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "| Alpha | Beta | 1 | yes |" in out.split("did not keep")[1]


def test_one_judge_seeing_an_arrow_the_other_does_not_is_reported(pairs):
    batch(pairs, "1.json", "josh",
          [{"pair": ["A", "C"], "verdict": "needs", "first": "A"}])
    batch(pairs, "2.json", "maria", [{"pair": ["A", "C"], "verdict": "unrelated"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    disputed = out.split("the other did not")[1].split("##")[0]
    assert "josh: Alpha first" in disputed
    assert "maria: unrelated" in disputed


def test_two_topics_that_need_each_other_are_a_level_not_a_fault(pairs):
    """`B` already needs `A`. Judging `B` to come first makes the arrow run
    both ways, which says the two sit at one level rather than that something
    is broken."""
    batch(pairs, "1.json", "josh",
          [{"pair": ["A", "B"], "verdict": "needs", "first": "B"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    level = out.split("one level")[1].split("##")[0]
    assert "Alpha" in level and "Beta" in level
    assert out.split("three or more")[1].split("##")[0].strip() == "None."


def test_two_judges_pointing_opposite_ways_are_a_level_not_a_disagreement(pairs):
    """Between them they have said what the "both ways" button says."""
    batch(pairs, "1.json", "ruth",
          [{"pair": ["A", "C"], "verdict": "needs", "first": "A"}])
    batch(pairs, "2.json", "tom",
          [{"pair": ["A", "C"], "verdict": "needs", "first": "C"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "Alpha" in out.split("one level")[1].split("##")[0]
    assert out.split("the other did not")[1].split("##")[0].strip() == "None."


def test_a_longer_loop_is_still_reported_as_one_to_break(pairs):
    """Three topics in a ring cannot be taught in any order, and teaching
    them together does not help."""
    topics = {"A": {"name": "Alpha", "needs": ["C"]},
              "B": {"name": "Beta", "needs": ["A"]},
              "C": {"name": "Gamma", "needs": ["B"]}}
    batch(pairs, "1.json", "josh", [])
    out = pr.build_report(topics, pr.load_batches())
    tangle = out.split("three or more")[1].split("##")[0]
    assert "Alpha" in tangle and "Beta" in tangle and "Gamma" in tangle


def test_an_unreadable_batch_is_skipped_rather_than_fatal(pairs, capsys):
    (pairs / "broken.json").write_text("not json")
    batch(pairs, "1.json", "josh", [{"pair": ["A", "C"], "verdict": "unrelated"}])
    assert len(pr.load_batches()) == 1
    assert "broken.json" in capsys.readouterr().err


def test_a_pair_with_the_wrong_shape_is_ignored(pairs):
    batch(pairs, "1.json", "josh", [{"pair": ["A"], "verdict": "unrelated"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "0 pairs judged" in out


def test_a_group_written_as_an_object_still_counts(pairs):
    """A judge wrote each new group as an object carrying a name and the
    topics it covers. That is more thought than a bare string, not less, so
    the name is taken rather than the batch lost."""
    batch(pairs, "1.json", "tom", [{"pair": ["A", "C"], "verdict": "unrelated"}],
          new_groups=[{"key": "approach", "name": "How to approach a problem",
                       "topics": ["A", "C"]}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "How to approach a problem" in out


def test_a_field_of_the_wrong_type_does_not_stop_the_report(pairs):
    batch(pairs, "1.json", "tom", [{"pair": ["A", "C"], "verdict": "unrelated"}],
          renamed=["not", "a", "map"], groups="nonsense", needs_work=42,
          new_groups={"also": "wrong"})
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "1 pairs judged" in out


def test_a_judgement_that_is_not_an_object_is_skipped(pairs):
    batch(pairs, "1.json", "tom",
          ["a string where an object belongs",
           {"pair": ["A", "C"], "verdict": "unrelated"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "1 pairs judged" in out


def test_a_pair_of_non_strings_is_skipped(pairs):
    batch(pairs, "1.json", "tom", [{"pair": [1, 2], "verdict": "unrelated"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "0 pairs judged" in out


def test_an_arrow_a_chain_already_gives_you_is_listed_apart(pairs):
    """`B` needs `A` and `C` needs `B`, so the graph already runs A to C.
    A judge saying so is right and changes nothing."""
    topics = {"A": {"name": "Alpha", "needs": []},
              "B": {"name": "Beta", "needs": ["A"]},
              "C": {"name": "Gamma", "needs": ["B"]}}
    batch(pairs, "1.json", "ruth",
          [{"pair": ["A", "C"], "verdict": "needs", "first": "A"}])
    out = pr.build_report(topics, pr.load_batches())
    assert out.split("## Arrows to add")[1].split("\n## ")[0].strip().endswith(
        "Nothing new.")
    assert "Alpha" in out.split("already gives you")[1].split("\n## ")[0]


def test_an_arrow_no_chain_gives_you_is_a_real_addition(pairs):
    topics = {"A": {"name": "Alpha", "needs": []},
              "B": {"name": "Beta", "needs": []},
              "C": {"name": "Gamma", "needs": ["B"]}}
    batch(pairs, "1.json", "ruth",
          [{"pair": ["A", "C"], "verdict": "needs", "first": "A"}])
    out = pr.build_report(topics, pr.load_batches())
    assert "| Alpha | Gamma |" in out.split("## Arrows to add")[1].split("\n## ")[0]


def test_reachability_survives_a_graph_that_already_loops(pairs):
    """The report exists partly to find loops, so working out what a chain
    reaches must not hang on one."""
    topics = {"A": {"name": "Alpha", "needs": ["B"]},
              "B": {"name": "Beta", "needs": ["A"]},
              "C": {"name": "Gamma", "needs": []}}
    batch(pairs, "1.json", "ruth",
          [{"pair": ["A", "C"], "verdict": "needs", "first": "C"}])
    out = pr.build_report(topics, pr.load_batches())
    assert "Gamma" in out
