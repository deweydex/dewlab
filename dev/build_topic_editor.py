"""Put the graph as it stands into the topic editor.

    python3 dev/build_topic_editor.py            # rewrite the editor's DATA block
    python3 dev/build_topic_editor.py --check    # fail if it is out of date

`topic_editor/index.html` is one file a browser opens with no build step, so
it carries the graph as a JSON blob. The blob is generated from the same
sources the map is drawn from — `topics.yaml`, the judgements, the decisions,
the wall in `strands.yaml` — so what the editor opens on is exactly what the
map shows, and CI runs `--check` so the copy cannot drift.

The editor's export goes back the other way through `dev/apply_topic_edits.py`,
which rewrites the YAML; the editor never writes a file itself.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "dev"))
import draw_topic_graph as graph  # noqa: E402

EDITOR = ROOT / "topic_editor" / "index.html"
KNOWN = {"name", "outcome", "plain", "uses", "tags", "needs", "helps", "applied_in",
         "interdependent", "involves"}
POSITIONS = ROOT / "planning" / "curriculum" / "topic-positions.json"


def blob() -> str:
    topics = yaml.safe_load(graph.TOPICS.read_text())["topics"]
    g = graph.current(topics)
    band = graph.bands(topics)
    spec = yaml.safe_load(graph.STRANDS.read_text())
    first = lambda o: [o] if isinstance(o, str) else list(o)
    data = {
        "topics": {
            code: {
                "n": t["name"],
                "p": " ".join(str(t.get("plain") or "").split()),
                "w": [" ".join(u.split()) for u in (t.get("uses") or [])],
                "o": first(t.get("outcome") or []),
                "c": band[code],
                "m": code.split("-")[0],
                "t": list(t.get("tags") or []),
                # Anything else on the topic goes through untouched, so a
                # field the editor does not know about survives the round trip.
                "x": {k: v for k, v in t.items() if k not in KNOWN},
            }
            for code, t in topics.items()
        },
        "requires": sorted([a, b] for a, b in g["edges"]),
        "level": sorted([a, b] for a, b in g["levels"]),
        "helps": sorted([a, b] for a, b in g.get("helps", set())),
        "applied": sorted([a, b] for a, b in g.get("applied", set())),
        "columns": [{"id": c["id"], "name": c["name"]} for c in spec["columns"]],
        "modules": graph.MODULES,
        "pos": json.loads(POSITIONS.read_text()) if POSITIONS.exists() else None,
    }
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def rewritten() -> str:
    page = EDITOR.read_text()
    # A function rather than a string, because a replacement string is parsed
    # for backslash escapes and the JSON carries "\u2014" and the like.
    return re.sub(r"const DATA = \{.*?\};", lambda _: "const DATA = " + blob() + ";",
                  page, count=1, flags=re.S)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    new = rewritten()
    if args.check:
        if new != EDITOR.read_text():
            print(f"{EDITOR.relative_to(ROOT)} is out of date; run "
                  f"python3 dev/build_topic_editor.py", file=sys.stderr)
            return 1
        print("the topic editor's graph is current")
        return 0
    EDITOR.write_text(new)
    n = len(json.loads(blob())["topics"])
    print(f"wrote {n} topics into {EDITOR.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
