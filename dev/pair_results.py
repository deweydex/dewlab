"""Turn the pair-game judgements into a report on the topic graph.

    python3 dev/pair_results.py                 # write the report
    python3 dev/pair_results.py --from blind    # ... over the blind judgements
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

  * **New edges** — a pair judged "needs" that the graph does not have. An
    arrow the graph already gives you through a chain is listed apart from one
    that changes anything: both judges kept flagging that distinction by hand,
    and confirming a path is a different finding from adding one.
  * **Edges nobody kept** — an existing arrow that judges called unrelated.
  * **Disagreements** — one pair, two judges, two answers.
  * **Levels** — two topics that each need the other. They are not a defect.
    They are one level of the graph: two things taught together, or one topic
    wearing two names. A longer loop is different, and does have to be broken.

Two judges who pick opposite directions on the same pair have between them
said what the game's "both ways" button says. The report treats that as a
level rather than as a disagreement to settle.
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
REVIEW = ROOT / "planning" / "curriculum" / "review"
PAIRS = REVIEW / "pairs"
REPORT = REVIEW / "pair-results.md"

# Judgements made while the judge could see the graph, and judgements made
# blind, are two different piles and are reported separately. Mixing them
# would lose the comparison that is the point of having both. `blind/README.md`
# has what the comparison showed.
SOURCES = {"pairs": (PAIRS, REPORT),
           "blind": (REVIEW / "blind", REVIEW / "pair-results-blind.md"),
           "sighted": (REVIEW / "sighted", REVIEW / "pair-results-sighted.md")}

# Thirteen topics were split after these judgements were made, so a judgement
# names a code that is gone. Each stands for the child that took over its
# arrows, which is what `dev/draw_topic_graph.py` does; here it only decides
# which name the report prints, so a reader is not left looking up a code that
# no longer exists.
GONE = {
    "MIT-6.3": "MIT-6.3a", "MIT-1.1": "MIT-1.1a", "MIT-6.8": "MIT-6.8a",
    "PDP-LO6": "PDP-LO6a", "MIT-1.10": "MIT-1.10a", "MIT-4.10": "MIT-4.10a",
    "MIT-5.12": "MIT-5.12a", "CMPS-LO1": "CMPS-LO1a", "MIT-5.8": "MIT-5.8a",
    "MIT-4.6": "MIT-4.6a", "CMPS-LO4": "CMPS-LO4a", "CMPS-LO2": "CMPS-LO2a",
    "MIT-2.1": "MIT-2.1a", "MIT-6.5": "MIT-6.3a",
    "CMPS-LO2a": "MIT-5.6",
}


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


def names_in(value) -> list[str]:
    """A list of names out of whatever a batch put in the field.

    A batch is written by whoever was judging, through a page or by hand, so a
    field can arrive in a shape this script did not picture. One judge wrote
    each new group as an object carrying a name and the topics it covers,
    which is more thought than a bare string and no reason to lose the lot.
    Anything with no name in it is skipped rather than fatal.
    """
    out = []
    for item in value if isinstance(value, list) else []:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
        elif isinstance(item, dict):
            name = item.get("name") or item.get("group") or item.get("key")
            if isinstance(name, str) and name.strip():
                out.append(name.strip())
    return out


def text_map(value) -> dict[str, str]:
    """The string-to-string pairs of a field, ignoring anything else."""
    if not isinstance(value, dict):
        return {}
    return {k: v for k, v in value.items()
            if isinstance(k, str) and isinstance(v, str)}


def tally(batches: list[dict]) -> dict[tuple, list[dict]]:
    """Group every judgement by the unordered pair it is about."""
    votes: dict[tuple, list[dict]] = defaultdict(list)
    for batch in batches:
        who = batch.get("by") or "anon"
        for j in batch.get("judgements") or []:
            if not isinstance(j, dict):
                continue
            pair = j.get("pair") or []
            if not isinstance(pair, list) or len(pair) != 2 \
                    or not all(isinstance(c, str) for c in pair):
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


def reachable_from(edges: set[tuple]) -> dict[str, set[str]]:
    """For each topic, everything a chain of arrows already leads to.

    An arrow from A to B is news only when B is not already downstream of A.
    A judge saying "factorials before combinations" is right and tells us
    nothing new when the graph runs factorials to permutations to
    combinations already.
    """
    # Sorted, because a set of edges iterates in whatever order the hash
    # gives, and the walk below follows that order. The loops it reports would
    # otherwise differ between two runs over the same data, which makes a
    # generated file impossible to check into CI.
    ahead: dict[str, list[str]] = defaultdict(list)
    for early, late in sorted(edges):
        ahead[early].append(late)

    memo: dict[str, set[str]] = {}

    def walk(node: str, on_path: frozenset) -> set[str]:
        if node in memo:
            return memo[node]
        # A graph with a loop in it is one of the things this report exists to
        # find, so this walk has to survive one rather than recurse forever.
        out: set[str] = set()
        for nxt in ahead.get(node, []):
            out.add(nxt)
            if nxt not in on_path:
                out |= walk(nxt, on_path | {nxt})
        memo[node] = out
        return out

    return {node: walk(node, frozenset([node])) for node in ahead}


def cycles(edges: set[tuple]) -> list[list[str]]:
    """Every loop the edge set contains, found by walking depth-first and
    watching for a node that is still on the current path.

    A loop of two topics and a loop of five are different findings, so the
    caller separates them; this only finds them.
    """
    # Sorted, because a set of edges iterates in whatever order the hash
    # gives, and the walk below follows that order. The loops it reports would
    # otherwise differ between two runs over the same data, which makes a
    # generated file impossible to check into CI.
    ahead: dict[str, list[str]] = defaultdict(list)
    for early, late in sorted(edges):
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

    for node in sorted(ahead):
        if node not in seen:
            walk(node)
    return found


def live_code(code: str) -> str:
    """The live code a dead one stands for, following a chain of them.

    A split can be followed by a merge — CMPS-LO2 became CMPS-LO2a, which was
    then folded into MIT-5.6 — so one lookup is not enough. Ten steps is far
    past any chain this file will ever hold, and stopping there means a
    mistake in GONE cannot hang the build.
    """
    for _ in range(10):
        nxt = GONE.get(code)
        if nxt is None:
            return code
        code = nxt
    raise SystemExit(f"GONE loops around {code}")


def name_of(topics: dict, code: str, renames: dict) -> str:
    live = live_code(code)
    if code in renames:
        return f"{renames[code]} (was {topics.get(live, {}).get('name', code)})"
    return topics.get(live, {}).get("name", code)


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
        renames.update(text_map(batch.get("renamed")))
        for code, gs in (batch.get("groups") or {}).items() \
                if isinstance(batch.get("groups"), dict) else []:
            if isinstance(code, str):
                groups[code] = names_in(gs)
        new_groups.update(names_in(batch.get("new_groups")))
        needs_work.update(n for n in names_in(batch.get("needs_work")))

    downstream = reachable_from(existing)
    judged_edges: set[tuple] = set()
    added, implied, dropped, disputed, both_ways, unsure = [], [], [], [], [], []

    for key, cast in sorted(votes.items()):
        verdict, first, agreed = settled(cast)
        a, b = key
        second = b if first == a else a

        # Two judges who both saw a prerequisite and pointed it opposite ways
        # have between them said the pair is a level. That is the "both ways"
        # answer, arrived at by two people instead of one, so it belongs with
        # the levels rather than in a list of things to settle.
        directions = {v["first"] for v in cast if v["verdict"] == "needs"}
        if (not agreed and len(directions) > 1
                and all(v["verdict"] == "needs" for v in cast)):
            both_ways.append((key, len(cast), "opposite"))
            continue

        if not agreed:
            disputed.append((key, cast))
        if verdict == "needs" and first:
            judged_edges.add((first, second))
            if (first, second) not in existing:
                where = (implied if second in downstream.get(first, set())
                         else added)
                where.append((first, second, len(cast), agreed))
        elif verdict == "unrelated":
            for edge in ((a, b), (b, a)):
                if edge in existing:
                    dropped.append((edge, len(cast), agreed))
        elif verdict == "both":
            both_ways.append((key, len(cast), "said" if agreed else "one judge"))
        elif verdict == "unsure":
            unsure.append(key)

    both_ways.sort(key=lambda entry: entry[0])
    loops = cycles(existing | judged_edges)
    # A two-topic loop says those two are a level. A longer one is a real
    # problem: it cannot be taught in any order and no amount of teaching
    # them together fixes it.
    levels = sorted((lp for lp in loops if len(lp) == 3), key=lambda lp: lp[0])
    tangles = sorted((lp for lp in loops if len(lp) > 3), key=lambda lp: lp[0])

    nm = lambda code: name_of(topics, code, renames)
    L = []
    A = L.append
    A("# What the pair judgements say about the graph")
    A("")
    A(f"Written by `dev/pair_results.py` from the saved batches in "
      f"`{PAIRS.name}/`. Nothing here has been applied to `topics.yaml`.")
    A("")
    A(f"{len(batches)} saved batches · {len(votes)} pairs judged · "
      f"{sum(len(c) for c in votes.values())} judgements in total")
    A("")

    A("## Arrows to add")
    A("")
    A("Pairs judged to need each other in one direction, where no chain of")
    A("existing arrows already leads from the first to the second. These are")
    A("the ones that change the graph.")
    A("")
    if added:
        A("| Comes first | Comes after | Judgements | Agreed |")
        A("|---|---|---|---|")
        for first, second, n, agreed in sorted(added):
            A(f"| {nm(first)} | {nm(second)} | {n} | {'yes' if agreed else 'no'} |")
    else:
        A("Nothing new.")
    A("")

    A("## Arrows the graph already gives you")
    A("")
    A("Judged the same way, but a chain of existing arrows already runs from")
    A("the first to the second. Drawing these would change nothing. They are")
    A("here because they confirm the chain rather than because they add to it.")
    A("")
    if implied:
        A("| Comes first | Comes after | Judgements | Agreed |")
        A("|---|---|---|---|")
        for first, second, n, agreed in sorted(implied):
            A(f"| {nm(first)} | {nm(second)} | {n} | {'yes' if agreed else 'no'} |")
    else:
        A("None.")
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

    A("## Pairs that turn out to be one level")
    A("")
    if levels or both_ways:
        A("Two topics that each need the other sit at the same level of the")
        A("graph. Either they are taught together, or they are one topic under")
        A("two names. Neither is a fault to fix.")
        A("")
        for loop in levels:
            A(f"- {nm(loop[0])} and {nm(loop[1])} — the arrow between them runs "
              "both ways once these judgements go in")
        how = {"opposite": "judges pointed opposite ways, which between them says this",
               "said": "every judge said so",
               "one judge": "one judge said so, another saw an order"}
        for key, n, why in both_ways:
            A(f"- {nm(key[0])} and {nm(key[1])} — {how[why]} "
              f"({n} judgement{'' if n == 1 else 's'})")
    else:
        A("None.")
    A("")

    A("## Loops of three or more")
    A("")
    if tangles:
        A("A loop this long cannot be taught in any order, and teaching the")
        A("topics together does not fix it. Each has to be broken.")
        A("")
        for loop in tangles:
            A("- " + " → ".join(nm(c) for c in loop))
    else:
        A("None.")
    A("")

    A("## Pairs where one judge saw an arrow and the other did not")
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
    ap.add_argument("--from", dest="source", default="pairs", choices=sorted(SOURCES),
                    help="which pile of judgements to report on (default: pairs)")
    args = ap.parse_args()

    global PAIRS, REPORT
    PAIRS, REPORT = SOURCES[args.source]

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
