"""Build the curriculum map from the tutorials and the module descriptors.

    python3 dev/curriculum_map.py            # rewrite planning/CURRICULUM_MAP.md
    python3 dev/curriculum_map.py --check    # fail if it is out of date

Two files decide what the map says, and neither is the map:

  * `planning/curriculum/outcomes.yaml` — every learning outcome in the two QQI
    module descriptors.
  * each tutorial's `covers:` frontmatter — which of those outcomes each section
    of that tutorial teaches (`covers`) or merely uses (`touches`).

So the map is derived, never written by hand, and it cannot quietly disagree
with the tutorials. An outcome code that no descriptor lists, or an anchor no
tutorial has, stops this script rather than producing a map with a dead link in
it — the same bargain the site build makes about `tutorial:` links.

The distinction between `covers` and `touches` is the whole point of the
exercise. A section that uses Boolean operators inside an `if` statement is not
teaching truth tables, and a map that counted it as coverage would tell us the
curriculum is complete when it is not.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TUTORIALS = ROOT / "tutorials"
OUTCOMES = ROOT / "planning" / "curriculum" / "outcomes.yaml"
OUT_OF_SCOPE = ROOT / "planning" / "curriculum" / "out-of-scope.yaml"
MAP = ROOT / "planning" / "CURRICULUM_MAP.md"
SITE = "https://deweydex.github.io/dewlab"

HEADING_RE = re.compile(r"^##\s+(?P<text>.+?)\s*$", re.MULTILINE)
# Python-Markdown's toc slugify, which is what build.py's anchors come from.
PUNCTUATION_RE = re.compile(r"[^\w\s-]")


class MapError(Exception):
    """Something in the data would produce a map that lies."""


def anchor_for(heading: str) -> str:
    slug = PUNCTUATION_RE.sub("", heading).strip().lower()
    return re.sub(r"[-\s]+", "-", slug)


@dataclass
class Section:
    anchor: str
    heading: str
    covers: list[str] = field(default_factory=list)
    touches: list[str] = field(default_factory=list)


@dataclass
class Tutorial:
    slug: str
    title: str
    module: str
    series: str
    order: int
    sections: list[Section]

    @property
    def url(self) -> str:
        return f"{SITE}/tutorials/{self.module}/{self.slug}.html"


@dataclass
class Outcome:
    code: str
    title: str
    strand: str


def load_outcomes() -> tuple[dict[str, Outcome], dict]:
    data = yaml.safe_load(OUTCOMES.read_text())
    outcomes = {}
    for entry in data["outcomes"]:
        if entry["code"] in outcomes:
            raise MapError(f"{entry['code']} is listed twice in outcomes.yaml")
        outcomes[entry["code"]] = Outcome(**entry)
    return outcomes, data["modules"]


def load_tutorials(known: dict[str, Outcome]) -> list[Tutorial]:
    tutorials = []
    for path in sorted(TUTORIALS.rglob("*.md")):
        text = path.read_text()
        if not text.startswith("---\n"):
            continue
        end = text.index("\n---\n", 4)
        meta = yaml.safe_load(text[4:end])
        body = text[end:]

        headings = {anchor_for(h): h for h in HEADING_RE.findall(body)}
        declared = meta.get("covers") or {}
        sections = []
        for anchor, claim in declared.items():
            if anchor not in headings:
                raise MapError(
                    f"{path.relative_to(ROOT)} declares coverage for "
                    f"{anchor!r}, which is not a section of it. "
                    f"It has: {', '.join(sorted(headings)) or 'no sections'}"
                )
            covers = list(claim.get("covers") or [])
            touches = list(claim.get("touches") or [])
            for code in covers + touches:
                if code not in known:
                    raise MapError(
                        f"{path.relative_to(ROOT)} names outcome {code!r}, "
                        "which no module descriptor lists in outcomes.yaml"
                    )
            sections.append(Section(anchor, headings[anchor], covers, touches))

        tutorials.append(
            Tutorial(
                slug=str(meta["slug"]),
                title=str(meta["title"]),
                module=str(meta["module"]),
                series=str(meta["series"]),
                order=int(meta.get("order", 0)),
                sections=sections,
            )
        )
    return tutorials


def coverage(
    outcomes: dict[str, Outcome], tutorials: list[Tutorial]
) -> dict[str, dict[str, list[tuple[Tutorial, Section]]]]:
    """For each outcome, which sections teach it and which only use it."""
    found = {code: {"covers": [], "touches": []} for code in outcomes}
    for tutorial in tutorials:
        for section in tutorial.sections:
            for code in section.covers:
                found[code]["covers"].append((tutorial, section))
            for code in section.touches:
                found[code]["touches"].append((tutorial, section))
    return found


# ------------------------------------------------------------- back-references

BACKREF_RE = re.compile(r"\bTutorial\s+(\d{1,2})\b")


def back_references(tutorials: list[Tutorial]) -> dict[str, set[int]]:
    """Which earlier tutorials each tutorial actually names in its own text.

    Evidence rather than intention: a tutorial that says "your functions from
    Tutorial 11" depends on Tutorial 11 whether or not anyone recorded that.
    Drawing these makes the load-bearing tutorials visible — and a tutorial
    nothing refers back to is a candidate for moving.
    """
    refs: dict[str, set[int]] = {}
    for tutorial in tutorials:
        path = next(TUTORIALS.rglob(f"{tutorial.slug}.md"))
        body = path.read_text()
        seen = {int(n) for n in BACKREF_RE.findall(body)}
        refs[tutorial.slug] = {n for n in seen if 0 < n < tutorial.order}
    return refs


# --------------------------------------------------------------------- render

STATUS = {
    "taught": ("Taught", "🟩"),
    "partial": ("Taught in part, by choice", "🟦"),
    "touched": ("Used, not taught", "🟨"),
    "absent": ("Not covered", "🟥"),
    "excluded": ("Out of scope, by choice", "⬜"),
}


def load_scope() -> dict:
    """What we have decided not to teach. A decision is not a gap."""
    if not OUT_OF_SCOPE.is_file():
        return {"outcomes": {}, "partial": {}, "topics": [], "undecided": []}
    data = yaml.safe_load(OUT_OF_SCOPE.read_text()) or {}
    return {
        "outcomes": {e["code"]: e for e in data.get("outcomes") or []},
        "partial": {e["code"]: e for e in data.get("partial") or []},
        "topics": data.get("topics") or [],
        "undecided": data.get("undecided") or [],
    }


def status_of(entry: dict, code: str = "", scope: dict | None = None) -> str:
    """Where an outcome actually stands, scope decision and coverage together.

    Deciding to teach only half of something does not mean half of it is
    taught. An outcome we have narrowed but not yet written is still a gap —
    a smaller one — so it counts as one until a tutorial covers it.
    """
    scope = scope or {"outcomes": {}, "partial": {}}
    if code in scope["outcomes"]:
        return "excluded"
    if entry["covers"]:
        return "partial" if code in scope["partial"] else "taught"
    if entry["touches"]:
        return "touched"
    return "absent"


def section_link(tutorial: Tutorial, section: Section) -> str:
    return f"[{tutorial.title} — {section.heading}]({tutorial.url}#{section.anchor})"


def strand_table(outcomes, found, scope) -> str:
    strands: dict[str, list[str]] = {}
    for code, outcome in outcomes.items():
        strands.setdefault(outcome.strand, []).append(code)

    rows = [
        "| Strand | 🟩 Taught | 🟦 Part, by choice | 🟨 Used only "
        "| 🟥 Not covered | ⬜ Out of scope |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for strand in sorted(strands):
        codes = strands[strand]
        counts = dict.fromkeys(STATUS, 0)
        for code in codes:
            counts[status_of(found[code], code, scope)] += 1
        rows.append(
            f"| **{strand}** | {counts['taught']} | {counts['partial']} "
            f"| {counts['touched']} | {counts['absent']} | {counts['excluded']} |"
        )
    return "\n".join(rows)


def strand_graph(outcomes, found, scope) -> str:
    """One node per strand, coloured by how much of it is actually taught."""
    strands: dict[str, list[str]] = {}
    for code, outcome in outcomes.items():
        strands.setdefault(outcome.strand, []).append(code)

    lines = ["```mermaid", "graph LR"]
    classes = {"full": [], "part": [], "none": []}
    for strand in sorted(strands):
        codes = strands[strand]
        states = [status_of(found[c], c, scope) for c in codes]
        taught = sum(1 for s in states if s in ("taught", "partial"))
        wanted = sum(1 for s in states if s != "excluded")
        node = strand.replace("-", "_")
        lines.append(f'  {node}["{strand}<br/>{taught} of {wanted} in place"]')
        if taught == wanted:
            classes["full"].append(node)
        elif taught == 0:
            classes["none"].append(node)
        else:
            classes["part"].append(node)

    lines += [
        "",
        "  classDef full fill:#edf7f0,stroke:#1f6b3f,color:#1f6b3f;",
        "  classDef part fill:#fdf6ec,stroke:#b5651d,color:#7a4310;",
        "  classDef none fill:#fdf0ef,stroke:#9b2226,color:#9b2226;",
    ]
    for name, nodes in classes.items():
        if nodes:
            lines.append(f"  class {','.join(nodes)} {name};")
    lines.append("```")
    return "\n".join(lines)


def sequence_graph(tutorials: list[Tutorial], refs: dict[str, set[int]]) -> str:
    """The teaching order, with a dashed arrow wherever one tutorial names
    an earlier one in its own text."""
    ordered = sorted(
        [t for t in tutorials if t.order and t.module == "mit-pdp-maths-prog-integration"],
        key=lambda t: t.order,
    )
    by_order = {t.order: t for t in ordered}

    lines = ["```mermaid", "graph TD"]
    for tutorial in ordered:
        label = tutorial.title.split(":", 1)[-1].strip()
        lines.append(f'  T{tutorial.order}["{tutorial.order}. {label}"]')
    lines.append("")
    for a, b in zip(ordered, ordered[1:]):
        lines.append(f"  T{a.order} --> T{b.order}")
    lines.append("")
    for tutorial in ordered:
        for target in sorted(refs.get(tutorial.slug, set())):
            if target in by_order and target != tutorial.order - 1:
                lines.append(f"  T{tutorial.order} -.->|builds on| T{target}")
    lines.append("```")
    return "\n".join(lines)


def outcome_tables(outcomes, modules, found, scope) -> str:
    """Every outcome, its state, and a link straight to where it is taught."""
    out = []
    for module, meta in modules.items():
        out.append(f"### {meta['title']} {meta['code']}\n")
        codes = [c for c in outcomes if c.startswith(module + "-")]
        by_section: dict[str, list[str]] = {}
        for code in codes:
            tail = code.split("-", 1)[1]
            section = tail.split(".")[0] if "." in tail else "LO"
            by_section.setdefault(section, []).append(code)

        for section in sorted(by_section, key=lambda s: (s == "LO", s)):
            name = meta["sections"].get(section, section)
            if len(by_section) > 1:
                out.append(f"#### {section}. {name}\n" if section != "LO" else f"#### {name}\n")
            out.append("| Outcome | | Where |")
            out.append("|---|---|---|")
            for code in by_section[section]:
                outcome = outcomes[code]
                state = status_of(found[code], code, scope)
                mark = STATUS[state][1]
                where = []
                for tutorial, sec in found[code]["covers"]:
                    where.append(section_link(tutorial, sec))
                for tutorial, sec in found[code]["touches"]:
                    where.append("_used in:_ " + section_link(tutorial, sec))
                if state == "excluded":
                    where = ["**Out of scope** — " +
                             scope["outcomes"][code]["reason"].strip().replace("\n", " ")]
                elif state == "partial":
                    entry = scope["partial"][code]
                    where.append(
                        f"**Narrowed:** not {entry['excluded'].strip()}"
                    )
                elif state == "absent" and code in scope["partial"]:
                    entry = scope["partial"][code]
                    where = [f"**Not written. When it is:** {entry['kept'].strip()} "
                             f"only, not {entry['excluded'].strip()}"]
                out.append(
                    f"| `{code}` {outcome.title} | {mark} | "
                    f"{'<br/>'.join(where) or '—'} |"
                )
            out.append("")
    return "\n".join(out)


def conflicts(found, scope) -> list[str]:
    """Sections still teaching something we decided not to assess."""
    notes = []
    for code, entry in scope["outcomes"].items():
        for tutorial, section in found[code]["covers"]:
            notes.append(
                f"- `{code}` is out of scope, but {section_link(tutorial, section)} "
                "still teaches it."
            )
    return notes



# ---------------------------------------------------------------------- terms

# A term being introduced is already marked in these tutorials: single-asterisk
# emphasis around the word, the first time it means something particular. That
# convention was there before anybody thought to check it, which is what makes
# it usable — it is evidence of what the author considered a new word, not a
# list somebody would have to maintain.
EMPHASIS_RE = re.compile(r"(?<![*\w])\*(?!\s)([^*\n]{2,40}?)(?<!\s)\*(?![*\w])")
FENCE_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
SUBTITLE_RE = re.compile(r"^\*\*Programming Design Principles.*$", re.MULTILINE)

# Emphasis is also used for ordinary stress — "*not* the same", "*exactly* one".
# Those are not terms and listing them buries the ones that are.
STRESS_WORDS = {
    "not", "both", "or", "and", "either", "exactly", "at least one", "can",
    "lot", "is", "without", "except", "how to think", "given that",
    "solutions to homework problems", "another function", "cells",
}


def prose_of(tutorial: Tutorial) -> str:
    """A tutorial's text with the code and the standing subtitle taken out.

    Code because a `*` in a docstring is not emphasis; the subtitle because
    "Programming Design Principles" appears on every page and would make
    "design" look like a word used everywhere from the first tutorial.
    """
    path = next(TUTORIALS.rglob(f"{tutorial.slug}.md"))
    body = FENCE_BLOCK_RE.sub("", path.read_text())
    body = INLINE_CODE_RE.sub("", body)
    return SUBTITLE_RE.sub("", body)


def terms_of(tutorials: list[Tutorial]) -> dict[str, set[str]]:
    """Every emphasised term, and which tutorials emphasise it."""
    found: dict[str, set[str]] = {}
    for tutorial in tutorials:
        for match in EMPHASIS_RE.findall(prose_of(tutorial)):
            term = match.strip().lower()
            if term not in STRESS_WORDS:
                found.setdefault(term, set()).add(tutorial.slug)
    return found


def term_findings(tutorials: list[Tutorial]) -> dict[str, list]:
    """Two questions about vocabulary that the tutorials can answer themselves.

    **Introduced more than once** — the same word presented as new in two
    tutorials. Either it is being re-introduced, or the two places mean
    different things by it. Nothing here can tell which; a person reads the two
    and decides. `index` was the second kind, and cost a rewrite.

    **Used before it was introduced** — a word appearing in an earlier tutorial
    than the one that stops to explain it. Some of these are ordinary English
    doing ordinary work and can be ignored; the ones that are not are places
    where a student met a term as if they already knew it.
    """
    ordered = [t for t in tutorials if t.order and t.module == "mit-pdp-maths-prog-integration"]
    order_of = {t.slug: t.order for t in ordered}
    prose = {t.slug: prose_of(t).lower() for t in ordered}
    terms = terms_of(ordered)

    repeated, late = [], []
    for term in sorted(terms):
        where = sorted(order_of[s] for s in terms[term] if s in order_of)
        if not where:
            continue
        if len(where) > 1:
            repeated.append((term, where))
        word = re.compile(rf"\b{re.escape(term)}\b")
        used = [order_of[s] for s, body in prose.items() if word.search(body)]
        if used and min(used) < where[0]:
            late.append((term, min(used), where[0]))
    return {"repeated": repeated, "late": late, "count": len(terms)}


# ------------------------------------------------------------------ proposals

PROPOSED = ROOT / "planning" / "curriculum" / "proposed.yaml"


def load_proposals() -> list[dict]:
    if not PROPOSED.is_file():
        return []
    return (yaml.safe_load(PROPOSED.read_text()) or {}).get("proposed") or []


def proposal_graph(tutorials: list[Tutorial], proposals: list[dict]) -> str:
    """The existing series with the proposed tutorials slotted into it."""
    ordered = sorted(
        [t for t in tutorials
         if t.order and t.module == "mit-pdp-maths-prog-integration"],
        key=lambda t: t.order,
    )
    node_of = {t.slug: f"T{t.order}" for t in ordered}
    node_of.update({p["id"]: "N" + str(i) for i, p in enumerate(proposals)})

    lines = ["```mermaid", "graph TD"]
    for tutorial in ordered:
        label = tutorial.title.split(":", 1)[-1].strip()
        lines.append(f'  T{tutorial.order}["{tutorial.order}. {label}"]')
    for proposal in proposals:
        lines.append(f'  {node_of[proposal["id"]]}("{proposal["title"]}")')
    lines.append("")
    for a, b in zip(ordered, ordered[1:]):
        lines.append(f"  T{a.order} --> T{b.order}")
    lines.append("")
    for proposal in proposals:
        after = node_of.get(proposal["after"])
        if after:
            lines.append(f"  {after} ==> {node_of[proposal['id']]}")
    lines += [
        "",
        "  classDef new fill:#fdf6ec,stroke:#b5651d,color:#7a4310,"
        "stroke-dasharray:4 3;",
        f"  class {','.join(node_of[p['id']] for p in proposals)} new;",
    ]
    lines.append("```")
    return "\n".join(lines)


def proposal_table(proposals: list[dict], outcomes) -> str:
    rows = ["| Proposed | Goes after | Closes | Size |", "|---|---|---|---|"]
    for proposal in proposals:
        codes = ", ".join(f"`{c}`" for c in proposal.get("covers") or [])
        optional = proposal.get("optional") or []
        if optional:
            codes += "<br/>_if kept:_ " + ", ".join(f"`{c}`" for c in optional)
        rows.append(
            f"| **{proposal['title']}** | after {proposal['after']} "
            f"| {codes} | {proposal['size']} |"
        )
    return "\n".join(rows)


# ------------------------------------------------------------------ document

def render() -> str:
    outcomes, modules = load_outcomes()
    tutorials = load_tutorials(outcomes)
    found = coverage(outcomes, tutorials)
    scope = load_scope()
    proposals = load_proposals()
    refs = back_references(tutorials)

    states = {c: status_of(found[c], c, scope) for c in outcomes}
    counted = {k: sum(1 for s in states.values() if s == k) for k in STATUS}
    wanted = len(outcomes) - counted["excluded"]
    in_place = counted["taught"] + counted["partial"]

    parts = [
        "# Curriculum map",
        "",
        "**Generated — do not edit by hand.** `python3 dev/curriculum_map.py`",
        "rebuilds it from three files, and CI fails if this one is out of date:",
        "",
        "- `planning/curriculum/outcomes.yaml` — every learning outcome in the two",
        "  QQI module descriptors.",
        "- each tutorial's `covers:` frontmatter — which outcome each section",
        "  teaches, and which it only uses.",
        "- `planning/curriculum/out-of-scope.yaml` — what we have decided not to",
        "  teach, so a decision stops looking like a gap.",
        "",
        "Every link below goes to the section of the live site that does the work,",
        "so this doubles as a way of finding where anything is taught.",
        "",
        "## Where we stand",
        "",
        f"**{in_place} of {wanted}** outcomes are in place, once the "
        f"{counted['excluded']} we have ruled out are set aside.",
        "",
        f"- {STATUS['taught'][1]} **{counted['taught']} taught** — a tutorial "
        "section teaches it.",
        f"- {STATUS['partial'][1]} **{counted['partial']} taught in part** — "
        "deliberately narrowed, and the narrowed version is written.",
        f"- {STATUS['touched'][1]} **{counted['touched']} used but not taught** — "
        "students meet it in passing without it ever being the subject. These are "
        "the quiet gaps: they look covered from a distance.",
        f"- {STATUS['absent'][1]} **{counted['absent']} not covered** — nothing "
        "in dewlab touches it.",
        f"- {STATUS['excluded'][1]} **{counted['excluded']} out of scope** — see "
        "`planning/curriculum/out-of-scope.yaml` for why.",
        "",
        "### By strand",
        "",
        strand_table(outcomes, found, scope),
        "",
        strand_graph(outcomes, found, scope),
        "",
    ]

    notes = conflicts(found, scope)
    if notes:
        parts += [
            "### Still taught, though we decided not to",
            "",
            "Each of these is a tutorial section teaching something nobody is going",
            "to assess. Either the section goes, or the decision does.",
            "",
            *notes,
            "",
        ]

    parts += [
        "## The series as it stands",
        "",
        "Solid arrows are the reading order. A dashed arrow means the later",
        "tutorial names the earlier one in its own text — evidence of a real",
        "dependency rather than an intention, found by reading the tutorials",
        "themselves. A tutorial with several dashed arrows into it is",
        "load-bearing and expensive to move; one with none is cheap to move, and",
        "possibly not pulling its weight where it is.",
        "",
        sequence_graph(tutorials, refs),
        "",
        "## What is missing, and where it would go",
        "",
        "Dashed boxes are proposed. Placement is argued in",
        "`planning/curriculum/proposed.yaml` and each has an outline in",
        "`planning/outlines/`.",
        "",
        proposal_graph(tutorials, proposals),
        "",
        proposal_table(proposals, outcomes),
        "",
        "## Every outcome",
        "",
        outcome_tables(outcomes, modules, found, scope),
    ]

    words = term_findings(tutorials)
    parts += [
        "## Vocabulary",
        "",
        f"The tutorials mark a term being introduced by putting it in italics "
        f"the first time it means something particular. **{words['count']} terms** "
        "are marked that way, and asking two questions of them is free.",
        "",
        "### Introduced more than once",
        "",
        "The same word presented as new in two places. Either it is being "
        "introduced twice, or the two places mean different things by it — "
        "nothing here can tell which, and a person reading both decides. "
        "`index` was the second kind and cost a rewrite.",
        "",
        "| Term | Introduced in tutorials |",
        "|---|---|",
    ]
    for term, where in words["repeated"]:
        parts.append(f"| *{term}* | {', '.join(str(n) for n in where)} |")

    parts += [
        "",
        "### Used before it was introduced",
        "",
        "A word appearing in an earlier tutorial than the one that stops to "
        "explain it. Some are ordinary English doing ordinary work and can be "
        "ignored; the rest are places a student met a term as though they "
        "already knew it.",
        "",
        "| Term | First appears in | Introduced in |",
        "|---|---:|---:|",
    ]
    for term, used, introduced in words["late"]:
        parts.append(f"| *{term}* | {used} | {introduced} |")
    parts.append("")

    undecided = scope.get("undecided") or []
    if undecided:
        parts += [
            "## Scope questions still open",
            "",
            "Counted as gaps until they are settled, which is the safer default.",
            "",
        ]
        for entry in undecided:
            parts.append(f"- **{entry['about']}** — "
                         f"{entry['question'].strip().replace(chr(10), ' ')}")
        parts.append("")

    return "\n".join(parts).rstrip("\n") + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="do not write; exit non-zero if the committed map is out of date",
    )
    args = parser.parse_args()
    try:
        text = render()
    except MapError as exc:
        print(f"curriculum map failed — {exc}", file=sys.stderr)
        return 1

    if args.check:
        current = MAP.read_text() if MAP.is_file() else ""
        if current != text:
            print(
                f"{MAP.relative_to(ROOT)} is out of date. "
                "Run: python3 dev/curriculum_map.py",
                file=sys.stderr,
            )
            return 1
        print(f"{MAP.relative_to(ROOT)} is current")
        return 0

    MAP.parent.mkdir(parents=True, exist_ok=True)
    MAP.write_text(text)
    print(f"wrote {MAP.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
