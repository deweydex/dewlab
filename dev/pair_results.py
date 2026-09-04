"""Turn the pair-game judgements into a report on the topic graph.

    python3 dev/pair_results.py                 # write the report
    python3 dev/pair_results.py --check         # fail if the report is stale

The pair game (`topic_tree_game/index.html`) writes one JSON file per save
into `planning/curriculum/review/pairs/`. Each file holds a batch of
judgements about pairs of topics: which one has to come first, or that
neither does, or that they need each other, or that the judge was not sure.

This script reads every one of those files, sets them against the `needs:`
lists already in `topics.yaml`, and writes what it finds to
`planning/curriculum/review/pair-results.md`.

It does not edit `topics.yaml`. Two people can judge the same pair and
disagree, and a majority is not a reason to rewrite the curriculum without
somebody looking. The report says what the judgements imply; changing the
graph stays a decision a person makes.

Four things it looks for:

  * **New edges** — a pair judged "needs" that the graph does not have.
  * **Edges nobody kept** — an existing arrow that judges called unrelated.
  * **Disagreements** — one pair, two judges, two answers.
  * **Cycles** — a set of new edges that would make the graph loop back on
    itself. A prerequisite graph that loops cannot be taught in any order, so
    these have to be broken before the edges go in.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "planning" / "curriculum" / "topics.yaml"
PAIRS = ROOT / "planning" / "curriculum" / "review" / "pairs"
REPORT = ROOT / "planning" / "curriculum" / "review" / "pair-results.md"


def load_topics() -> dict:
    data = yaml.safe_load(TOPICS.read_text()) or {}
    return data.get("topics") or {}


def load_batches() -> list[dict]:
    """Every saved batch, oldest first, skipping anything unreadable.

    A batch arrives as a commit made by whoever was judging, so a malformed
    one is a thing that can happen. It is named and skipped rather than
    stopping the report.
    """
    out = []
    for path in sorted(PAIRS.glob("*.json")):
        try:
            batch = json.loads(path.read_text())
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"skipped {path.name}: {exc}", file=sys.stderr)
            continue
        batch["_file"] = path.name
        out.append(batch)
    return out


def tally(batches: list[dict]) -> dict[tuple, list[dict]]:
    """Group every judgement by the unordered pair it is about."""
    votes: dict[tuple, list[dict]] = defaultdict(list)
    for batch in batches:
        who = batch.get("by") or "anon"
        for j in batch.get("judgements") or []:
            pair = j.get("pair") or []
            if len(pair) != 2:
                continue
            key = tuple(sorted(pair))
            votes[key].append({"by": who, "verdict": j.get("verdict"),
                               "first": j.get("first"), "file": batch["_file"]})
    return votes


def settled(cast: list[dict]) -> tuple[str, str | None, bool]:
    """One pair's answer: the verdict, which topic comes first, and whether
    the judges agreed. A verdict of "needs" only counts as agreement when the
    judges also picked the same topic to come first."""
    shapes = {(v["verdict"], v["first"] if v["verdict"] == "needs" else None)
              for v in cast}
    if len(shapes) == 1:
        verdict, first = shapes.pop()
        return verdict, first, True
    counts: dict[tuple, int] = defaultdict(int)
    for v in cast:
        counts[(v["verdict"], v["first"] if v["verdict"] == "needs" else None)] += 1
    best = max(counts.items(), key=lambda kv: kv[1])[0]
    return best[0], best[1], False


def cycles(edges: set[tuple]) -> list[list[str]]:
    """Every loop the edge set contains, found by walking depth-first and
    watching for a node that is still on the current path."""
    ahead: dict[str, list[str]] = defaultdict(list)
    for early, late in edges:
        ahead[early].append(late)
    found, path, on_path, seen = [], [], set(), set()

    def walk(node: str) -> None:
        path.append(node)
        on_path.add(node)
        seen.add(node)
        for nxt in ahead.get(node, []):
            if nxt in on_path:
                found.append(path[path.index(nxt):] + [nxt])
            elif nxt not in seen:
                walk(nxt)
        on_path.discard(node)
        path.pop()

    for node in list(ahead):
        if node not in seen:
            walk(node)
    return found


def name_of(topics: dict, code: str, renames: dict) -> str:
    if code in renames:
        return f"{renames[code]} (was {topics.get(code, {}).get('name', code)})"
    return topics.get(code, {}).get("name", code)


def build_report(topics: dict, batches: list[dict]) -> str:
    votes = tally(batches)
    existing = {(need, code)
                for code, entry in topics.items()
                for need in (entry.get("needs") or [])}

    renames: dict[str, str] = {}
    groups: dict[str, list[str]] = {}
    new_groups: set[str] = set()
    needs_work: set[str] = set()
    for batch in batches:
        renames.update(batch.get("renamed") or {})
        groups.update(batch.get("groups") or {})
        new_groups.update(batch.get("new_groups") or [])
        needs_work.update(batch.get("needs_work") or [])

    judged_edges: set[tuple] = set()
    added, dropped, disputed, both_ways, unsure = [], [], [], [], []

    for key, cast in sorted(votes.items()):
        verdict, first, agreed = settled(cast)
        a, b = key
        second = b if first == a else a
        if not agreed:
            disputed.append((key, cast))
        if verdict == "needs" and first:
            judged_edges.add((first, second))
            if (first, second) not in existing:
                added.append((first, second, len(cast), agreed))
        elif verdict == "unrelated":
            for edge in ((a, b), (b, a)):
                if edge in existing:
                    dropped.append((edge, len(cast), agreed))
        elif verdict == "both":
            both_ways.append((key, len(cast)))
        elif verdict == "unsure":
            unsure.append(key)

    loops = cycles(existing | judged_edges)

    nm = lambda code: name_of(topics, code, renames)
    L = []
    A = L.append
    A("# What the pair judgements say about the graph")
    A("")
    A("Written by `dev/pair_results.py` from the saved batches in `pairs/`.")
    A("Nothing here has been applied to `topics.yaml`.")
    A("")
    A(f"{len(batches)} saved batches · {len(votes)} pairs judged · "
      f"{sum(len(c) for c in votes.values())} judgements in total")
    A("")

    A("## Arrows to add")
    A("")
    if added:
        A("| Comes first | Comes after | Judgements | Agreed |")
        A("|---|---|---|---|")
        for first, second, n, agreed in sorted(added):
            A(f"| {nm(first)} | {nm(second)} | {n} | {'yes' if agreed else 'no'} |")
    else:
        A("Nothing new.")
    A("")

    A("## Arrows the judges did not keep")
    A("")
    if dropped:
        A("| Comes first | Comes after | Judgements | Agreed |")
        A("|---|---|---|---|")
        for (first, second), n, agreed in sorted(dropped):
            A(f"| {nm(first)} | {nm(second)} | {n} | {'yes' if agreed else 'no'} |")
    else:
        A("None. Every existing arrow survived the pairs that were judged.")
    A("")

    A("## Loops")
    A("")
    if loops:
        A("A prerequisite graph that loops cannot be taught in any order.")
        A("Each of these has to be broken before its arrows go in.")
        A("")
        for loop in loops:
            A("- " + " → ".join(nm(c) for c in loop))
    else:
        A("None. The graph these judgements imply can still be taught in order.")
    A("")

    A("## Pairs the judges disagreed about")
    A("")
    if disputed:
        for key, cast in disputed:
            A(f"- **{nm(key[0])}** and **{nm(key[1])}**")
            for v in cast:
                said = (f"{nm(v['first'])} first" if v["verdict"] == "needs"
                        else v["verdict"])
                A(f"  - {v['by']}: {said}")
    else:
        A("None.")
    A("")

    A("## Pairs judged as needing each other")
    A("")
    if both_ways:
        A("Two topics that each need the other cannot both come first.")
        A("Either one of them splits in two, or they are taught together.")
        A("")
        for key, n in both_ways:
            A(f"- {nm(key[0])} and {nm(key[1])} "
              f"({n} judgement{'' if n == 1 else 's'})")
    else:
        A("None.")
    A("")

    A("## Topics with a suggested new name")
    A("")
    if renames:
        A("| Topic | Suggested name |")
        A("|---|---|")
        for code, new in sorted(renames.items()):
            A(f"| {topics.get(code, {}).get('name', code)} | {new} |")
    else:
        A("None.")
    A("")

    A("## Groups")
    A("")
    if new_groups:
        A("Groups the judges invented:")
        A("")
        for g in sorted(new_groups):
            A(f"- {g}")
        A("")
    placed = {c: gs for c, gs in groups.items() if gs}
    if placed:
        A("| Topic | Groups |")
        A("|---|---|")
        for code, gs in sorted(placed.items()):
            A(f"| {nm(code)} | {', '.join(gs)} |")
    else:
        A("No topic has been put in a group yet.")
    A("")

    A("## Topics flagged as needing work")
    A("")
    if needs_work:
        for code in sorted(needs_work):
            A(f"- {nm(code)}")
    else:
        A("None.")
    A("")

    if unsure:
        A("## Pairs nobody could call")
        A("")
        for key in unsure:
            A(f"- {nm(key[0])} and {nm(key[1])}")
        A("")

    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="fail if the report is out of date")
    args = ap.parse_args()

    report = build_report(load_topics(), load_batches())
    if args.check:
        if not REPORT.exists() or REPORT.read_text() != report:
            print(f"{REPORT.relative_to(ROOT)} is out of date; "
                  "run python3 dev/pair_results.py", file=sys.stderr)
            return 1
        return 0
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report)
    print(f"wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
