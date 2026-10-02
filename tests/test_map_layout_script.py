"""dev/map_layout.py writes map/layout.json, which the build reads and never
recomputes. These hold the script to the committed file: run again on the same
graph it must give the same map, so that a change to the graph that was not
followed by a run of the script, or a change to the script that moves every
town, is found here and not by a learner who cannot find a town."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

DEWLAB = Path(__file__).resolve().parent.parent
SCRIPT = DEWLAB / "dev" / "map_layout.py"
FIXTURE = DEWLAB / "tests" / "e2e" / "fixture" / "map"


def run(graph: Path, out: Path, hash_seed: str = "0") -> dict:
    subprocess.run([sys.executable, str(SCRIPT), str(graph), str(out)], check=True, capture_output=True,
                   env={**os.environ, "PYTHONHASHSEED": hash_seed})
    return json.loads(out.read_text())


def same_map(fresh: dict, committed: dict, wiggle: int = 30) -> list[str]:
    """What differs, allowing a town to be a few units off: the settling is
    arithmetic on floats, and another machine's maths library may round the
    last digit differently."""
    problems = []
    for key in ("towns", "regions", "districts", "continents", "landmarks"):
        if set(fresh[key]) != set(committed[key]):
            problems.append(f"{key} differ: {sorted(set(fresh[key]) ^ set(committed[key]))[:5]}")
    for code, town in committed["towns"].items():
        if code in fresh["towns"]:
            now = fresh["towns"][code]
            if abs(now["x"] - town["x"]) > wiggle or abs(now["y"] - town["y"]) > wiggle or now["tier"] != town["tier"]:
                problems.append(f"town {code} moved from {town['x'], town['y']} to {now['x'], now['y']}")
    def pairs(m):
        return sorted((b["a"], b["b"], b["count"]) for b in m["bridges"])
    if pairs(fresh) != pairs(committed):
        problems.append(f"bridges differ: {pairs(fresh)} against {pairs(committed)}")
    return problems


def test_the_same_graph_gives_the_same_layout_whatever_the_hash_seed(tmp_path):
    first = run(FIXTURE / "graph.json", tmp_path / "a.json", "1")
    second = run(FIXTURE / "graph.json", tmp_path / "b.json", "2")
    assert first == second


def test_the_script_reproduces_the_committed_layout_of_the_fixture_map(tmp_path):
    fresh = run(FIXTURE / "graph.json", tmp_path / "layout.json")
    committed = json.loads((FIXTURE / "layout.json").read_text())
    assert same_map(fresh, committed) == []


def test_the_script_reproduces_the_committed_layout_of_the_real_map(tmp_path):
    fresh = run(DEWLAB / "map" / "graph.json", tmp_path / "layout.json")
    committed = json.loads((DEWLAB / "map" / "layout.json").read_text())
    assert same_map(fresh, committed) == [], (
        "map/layout.json is not the layout of map/graph.json. If the map changed on purpose, "
        "run python3 dev/map_layout.py and commit the result.")
