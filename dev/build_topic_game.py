"""Put the current topics into the pair game.

    python3 dev/build_topic_game.py            # rewrite the game's DATA block
    python3 dev/build_topic_game.py --check    # fail if it is out of date

`topic_tree_game/index.html` carries the topics as a JSON blob, because the
game is one file a phone opens with no build step and no fetch. That blob is
a copy, and a copy drifts: after thirteen topics were split it still offered
fourteen that no longer exist and none of the forty-two that replaced them.

So it is generated from `topics.yaml`, and CI runs `--check`. The same bargain
the standalone bundle makes.

The blob is deliberately not the whole file. A name, a section, the first part
of the plain description and the prerequisite list are what a card shows; the
`uses` list is several times the size of everything else and never appears.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "planning" / "curriculum" / "topics.yaml"
GROUPS = ROOT / "planning" / "curriculum" / "topic-groups.yaml"
GAME = ROOT / "topic_tree_game" / "index.html"

# What a card shows before it would need scrolling on a phone.
PLAIN_CHARS = 200


def section(code: str) -> str:
    """Which part of a descriptor a topic belongs to, for grouping the queue.

    `MIT-4.6c` is in MIT-4; `CMPS-LO2a` is in CMPS. The suffix a split adds is
    part of the topic, never part of the section.
    """
    if code.startswith("MIT-") and "." in code:
        return code.rsplit(".", 1)[0]
    return code.split("-")[0]


def blob() -> str:
    topics = yaml.safe_load(TOPICS.read_text())["topics"]
    groups = yaml.safe_load(GROUPS.read_text())["groups"]
    data = {
        "topics": {
            code: {
                "n": t["name"],
                "s": section(code),
                "p": " ".join(str(t.get("plain", "")).split())[:PLAIN_CHARS],
                "d": [n for n in (t.get("needs") or []) if n in topics],
            }
            for code, t in topics.items()
        },
        "groups": [g["name"] for g in groups],
    }
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


def rewritten() -> str:
    text = GAME.read_text()
    return re.sub(r"const DATA = \{.*?\};", "const DATA = " + blob() + ";",
                  text, count=1, flags=re.S)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="fail if the game's topics are out of date")
    args = ap.parse_args()

    want = rewritten()
    if args.check:
        if GAME.read_text() != want:
            print("topic_tree_game/index.html is out of date; run "
                  "python3 dev/build_topic_game.py", file=sys.stderr)
            return 1
        print("the pair game's topics are current")
        return 0
    GAME.write_text(want)
    n = len(json.loads(blob())["topics"])
    print(f"wrote {n} topics into {GAME.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
