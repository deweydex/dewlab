"""Tests for the pair-judgement report: a loop, a disagreement, and an arrow
nobody kept are the findings that would cost real work if missed."""

from __future__ import annotations

import json
import os
import random
import subprocess
import sys
from pathlib import Path

import yaml

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


def test_the_same_judgements_give_the_same_report_across_runs(tmp_path):
    # A generated file that varies with PYTHONHASHSEED can't be checked into
    # CI; this runs the build under several seeds and requires one output.
    rng = random.Random(7)
    codes = list("abcdefghij")
    edges = [(a, b) for a in codes
             for b in rng.sample([c for c in codes if c != a], 3)]
    (tmp_path / "topics.yaml").write_text(yaml.safe_dump(
        {"topics": {c: {"name": c.upper(), "needs": []} for c in codes}}))
    (tmp_path / "pairs").mkdir()
    (tmp_path / "pairs" / "1.json").write_text(json.dumps({"by": "josh", "judgements": [
        {"pair": [a, b], "verdict": "needs", "first": a} for a, b in edges]}))

    script = (
        "import sys, pathlib; sys.path.insert(0, %r);"
        "import pair_results as pr;"
        "pr.TOPICS = pathlib.Path(%r); pr.PAIRS = pathlib.Path(%r);"
        "print(pr.build_report(pr.load_topics(), pr.load_batches()))"
    ) % (str(Path(__file__).resolve().parent.parent / "dev"),
         str(tmp_path / "topics.yaml"), str(tmp_path / "pairs"))

    seen = set()
    for seed in ("1", "7", "42", "1234", "99999"):
        out = subprocess.run([sys.executable, "-c", script], capture_output=True,
                             text=True, env={**os.environ, "PYTHONHASHSEED": seed})
        assert out.returncode == 0, out.stderr
        seen.add(out.stdout)
    assert len(seen) == 1, "the report differs between runs over one pile"


def test_a_pair_with_the_wrong_shape_is_ignored(pairs):
    batch(pairs, "1.json", "josh", [{"pair": ["A"], "verdict": "unrelated"}])
    out = pr.build_report(TOPICS, pr.load_batches())
    assert "0 pairs judged" in out


def test_a_group_written_as_an_object_still_counts(pairs):
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
    # reachable_from's memoized walk must terminate on a self-referencing
    # graph rather than hang.
    topics = {"A": {"name": "Alpha", "needs": ["B"]},
              "B": {"name": "Beta", "needs": ["A"]},
              "C": {"name": "Gamma", "needs": []}}
    batch(pairs, "1.json", "ruth",
          [{"pair": ["A", "C"], "verdict": "needs", "first": "C"}])
    out = pr.build_report(topics, pr.load_batches())
    assert "Gamma" in out
