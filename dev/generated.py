#!/usr/bin/env python3
"""Is every generated file current? One command, where there were seven.

    python3 dev/generated.py            say which are stale; fail if one that blocks is
    python3 dev/generated.py --all      fail if any is stale (what the house-style job runs)
    python3 dev/generated.py --fix      regenerate the stale ones

Some files in the repository are written by a script from other files: the
curriculum map, the pair game's topics, the topic editor's graph, the pair
reports, the Dewey Track's pictures. Each script can say whether its file is
current (`--check`), and until now CI knew each command and a contributor had
to find them there. This lists them once.

Whether a stale one stops a pull request is a separate question, answered per
file below. The pair game, the topic editor's graph and the pair reports
block: a reader's page or a tool draws from them, or every regeneration would
show up as noise in a diff. The curriculum map and the pictures are reported:
a stale planning document breaks no page, and a picture that is a sentence
behind its page still works. A file that cannot be made at all (the map names
an outcome that does not exist) always blocks.
(DECISIONS_LOG 7.291, 7.301.)
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# name, the commands that check it, the commands that rewrite it, and what a
# stale one does: "blocks" or "reports". A command is a script and its flags.
CHECKS = [
    ("curriculum map", [["dev/curriculum_map.py", "--check"]], [["dev/curriculum_map.py"]], "reports"),
    ("pair game topics", [["dev/build_topic_game.py", "--check"]], [["dev/build_topic_game.py"]], "blocks"),
    ("topic editor graph", [["dev/build_topic_editor.py", "--check"]], [["dev/build_topic_editor.py"]], "blocks"),
    ("pair reports",
     [["dev/pair_results.py", "--check"], ["dev/pair_results.py", "--from", "blind", "--check"],
      ["dev/pair_results.py", "--from", "sighted", "--check"]],
     [["dev/pair_results.py"], ["dev/pair_results.py", "--from", "blind"],
      ["dev/pair_results.py", "--from", "sighted"]], "blocks"),
    ("Dewey pictures, units 1 to 5", [["dev/graphics/dewey_units_1_5.py", "--check"]],
     [["dev/graphics/dewey_units_1_5.py", "--write"]], "reports"),
    ("Dewey pictures, units 6 to 10", [["dev/graphics/dewey_units_6_10.py", "--check"]],
     [["dev/graphics/dewey_units_6_10.py", "--write"]], "reports"),
]


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *command], cwd=ROOT, capture_output=True, text=True)


def state_of(checks: list[list[str]]) -> tuple[str, str]:
    """("current" | "stale" | "broken", what the scripts said). The curriculum
    map's script exits 1 for out of date and 2 for cannot be made; the others
    only say 1."""
    said = []
    result = "current"
    for command in checks:
        done = run(command)
        said.append((done.stdout + done.stderr).strip())
        if done.returncode == 2:
            result = "broken"
        elif done.returncode != 0 and result != "broken":
            result = "stale"
    return result, "\n".join(line for line in said if line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--all", action="store_true",
                        help="fail on any stale file, not only one that blocks")
    parser.add_argument("--fix", action="store_true", help="regenerate the stale ones")
    args = parser.parse_args(argv)

    with ThreadPoolExecutor(max_workers=len(CHECKS)) as pool:
        states = list(pool.map(lambda row: state_of(row[1]), CHECKS))

    failing = 0
    for (name, _, fixes, effect), (state, said) in zip(CHECKS, states):
        if state == "current":
            print(f"current   {name}")
            continue
        if args.fix and state == "stale":
            for command in fixes:
                run(command)
            print(f"fixed     {name}")
            continue
        counts = state == "broken" or effect == "blocks" or args.all
        failing += counts
        label = "CANNOT BE MADE" if state == "broken" else "STALE"
        how = "" if state == "broken" else f"  (fix: python3 {' '.join(fixes[0])})"
        print(f"{label:9} {name}{how}" + ("" if counts else "  [reported, does not fail]"))
        if said:
            print("          " + said.replace("\n", "\n          "))
    return 1 if failing else 0


if __name__ == "__main__":
    raise SystemExit(main())
