"""Write an export from the topic editor back into the curriculum files.

    python3 dev/apply_topic_edits.py topic-graph-edits.json

The editor never writes a file itself; it hands you a JSON export and this
turns it into `topics.yaml`, `strands.yaml` and `topic-positions.json`, so the
YAML's shape stays in one place and the editor's state stays in the other.

After this has run, `topics.yaml` carries `authored: true` at the top and the
graph is what the YAML says. The judgements and decisions under `review/`
stop being applied on top: they are how the graph got here, and they stay as
that record.

Five kinds of link come across:

    needs          — requires, stored on the topic that needs the other
    helps          — the lighter one-way link, stored on the topic that helps
    applied_in     — a tool and the topic it is applied in, stored on the tool
    interdependent — the strong two-way link, stored on both
    involves       — the weak two-way link, stored on both

A topic merged away in the editor is removed here, and the code it folded
into is printed at the end for `GONE` in `draw_topic_graph.py` and
`pair_results.py`, which still map dead codes by hand.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TOPICS = ROOT / "planning" / "curriculum" / "topics.yaml"
STRANDS = ROOT / "planning" / "curriculum" / "strands.yaml"
OUTCOMES = ROOT / "planning" / "curriculum" / "outcomes.yaml"
POSITIONS = ROOT / "planning" / "curriculum" / "topic-positions.json"

FIELDS = {"requires": "needs", "helps": "helps", "applied": "applied_in",
          "inter": "interdependent", "involves": "involves"}
TWO_WAY = {"inter", "involves"}


def scalar(value: str) -> str:
    """One YAML scalar, quoted only when it has to be."""
    return yaml.safe_dump(value, default_flow_style=True, width=10_000,
                          allow_unicode=True).strip().removesuffix("\n...")


def block(text: str, indent: int) -> str:
    pad = " " * indent
    body = textwrap.fill(" ".join(text.split()), width=76 - indent,
                         initial_indent=pad, subsequent_indent=pad)
    return ">\n" + body + "\n"


def headers_of(source: str) -> tuple[str, dict[str, str]]:
    """The file's opening comment, and the comment sitting above each topic.

    Both are worth keeping: the header says what the file is, and the
    dividers say which part of a descriptor a run of topics belongs to.
    """
    lines = source.split("\n")
    top = []
    for line in lines:
        if line.startswith("topics:"):
            break
        top.append(line)
    above: dict[str, str] = {}
    pending: list[str] = []
    for line in lines:
        stripped = line.strip()
        if line.startswith("  ") and not line.startswith("   ") and stripped.endswith(":") \
                and not stripped.startswith("#") and not stripped.startswith("-"):
            code = stripped[:-1]
            if pending:
                above[code] = "\n".join(pending) + "\n"
            pending = []
        elif line.startswith("  #"):
            pending.append(line)
        elif stripped == "":
            continue
        else:
            pending = []
    header = "\n".join(l for l in top if not l.startswith("authored:")).rstrip("\n")
    return header, above


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip().split("\n")[2].strip(), file=sys.stderr)
        return 2
    export = json.loads(Path(sys.argv[1]).read_text())
    topics: dict = export["topics"]
    links: list = export["links"]

    source = TOPICS.read_text()
    header, above = headers_of(source)
    old_order = list((yaml.safe_load(source) or {}).get("topics") or {})
    order = [c for c in old_order if c in topics] + sorted(c for c in topics if c not in old_order)

    lists: dict[str, dict[str, list[str]]] = {c: {f: [] for f in FIELDS.values()} for c in topics}
    for link in links:
        a, b, kind = link["a"], link["b"], link["k"]
        if a not in topics or b not in topics:
            continue
        field = FIELDS[kind]
        if kind == "requires":
            lists[b]["needs"].append(a)
        elif kind in TWO_WAY:
            lists[a][field].append(b)
            lists[b][field].append(a)
        else:
            lists[a][field].append(b)

    out = [header, "",
           "# The graph is what this file says. It was drawn in the topic editor, and",
           "# the judgements and decisions under review/ are how it got here.",
           "authored: true", "", "topics:"]
    for code in order:
        t = topics[code]
        if above.get(code):
            out.append(above[code].rstrip("\n"))
        out.append(f"  {code}:")
        out.append(f"    name: {scalar(t['n'])}")
        claimed = t.get("o") or []
        if len(claimed) == 1:
            out.append(f"    outcome: {claimed[0]}")
        elif claimed:
            out.append(f"    outcome: [{', '.join(claimed)}]")
        if t.get("p"):
            out.append("    plain: " + block(t["p"], 6).rstrip("\n"))
        if t.get("w"):
            out.append("    uses:")
            for use in t["w"]:
                body = textwrap.fill(" ".join(use.split()), width=68,
                                     initial_indent="      - ", subsequent_indent="        ")
                out.append(body)
        if t.get("t"):
            out.append(f"    tags: [{', '.join(t['t'])}]")
        for key, value in (t.get("x") or {}).items():
            dumped = yaml.safe_dump({key: value}, default_flow_style=False,
                                    allow_unicode=True, width=76).rstrip("\n")
            out.append(textwrap.indent(dumped, "    "))
        for field in FIELDS.values():
            members = sorted(set(lists[code][field]))
            if field == "needs" or members:
                out.append(f"    {field}: [{', '.join(members)}]")
        out.append("")
    TOPICS.write_text("\n".join(out).rstrip("\n") + "\n")

    # strands.yaml: the columns as the editor has them, and every topic whose
    # column is not what its fine strand would give it.
    spec = yaml.safe_load(STRANDS.read_text())
    outcomes = {o["code"]: o for o in yaml.safe_load(OUTCOMES.read_text())["outcomes"]}
    spec["columns"] = [{"id": c["id"], "name": c["name"]} for c in export["columns"]]
    overrides = {}
    for code in order:
        claimed = topics[code].get("o") or []
        fine = (outcomes.get(claimed[0]) or {}).get("strand") if claimed else None
        default = spec["from_strand"].get(fine)
        if topics[code]["c"] != default:
            old = (spec.get("topics") or {}).get(code) or {}
            overrides[code] = {"column": topics[code]["c"],
                               "why": old.get("why", "Placed in the topic editor.")}
    spec["topics"] = overrides
    strand_text = STRANDS.read_text()
    head = strand_text[:strand_text.index("columns:")]
    STRANDS.write_text(head + yaml.safe_dump(spec, sort_keys=False, allow_unicode=True, width=80))

    POSITIONS.write_text(json.dumps(
        {"pos": export.get("pos") or {}, "pinned": export.get("pinned") or {}},
        sort_keys=True, indent=0))

    gone = export.get("gone") or {}
    print(f"wrote {len(order)} topics and {len(links)} links into {TOPICS.relative_to(ROOT)}")
    print(f"wrote {len(spec['columns'])} columns and {len(overrides)} placements into "
          f"{STRANDS.relative_to(ROOT)}")
    if gone:
        print("\nAdd to GONE in dev/draw_topic_graph.py and dev/pair_results.py:")
        for dead, live in sorted(gone.items()):
            print(f'    "{dead}": "{live}",')
    print("\nThen: python3 dev/build_topic_editor.py && python3 dev/build_topic_game.py "
          "&& python3 dev/curriculum_map.py && python3 -m pytest -q")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
