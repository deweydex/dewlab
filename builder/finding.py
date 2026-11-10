"""Finding a topic: the topic tree, Browse by topic, the topic map, the
knowledge map on a course page, the filters, and the search and reference
indexes.

Everything here answers one question, "where is the page about this?", from
the pages and courses the build has already read. `build()` in main.py calls
the `write_*` functions; nothing else in the build depends on this module, so
a change to how topics are found stays in this file.

It still borrows the build's own helpers (the shell, notes and refusals, a
page's glossary), imported from main.py below. main.py imports this module
last, once those exist.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

from builder.config import cfg
from builder.main import (
    Course,
    Tutorial,
    companion_buttons_html,
    courses,
    fail,
    fill_shell,
    load_yaml_no_duplicate_keys,
    nav_search_html,
    note,
    own_glossary,
    progress_attrs,
    render_search_box,
    report_doors_panel_html,
    say,
    series_of,
    site_footer,
    versioned,
)


# One node is a comfortable tap target with room for a two-line name.
TOPIC_W, TOPIC_H = 178, 66
# How many topics a tier fits before it wraps onto another line. Five keeps the
# whole tree about a thousand pixels wide, which a phone can zoom to fit.
TREE_COLUMNS = 5
TIER_GAP, ROW_GAP = 56, 22
BAND_GAP = 34
TREE_PAD = 40


def load_topics() -> dict:
    """The glossary: what each topic is, where it is used, what it needs first.

    Optional, like the outcome data — the site has to build from the tutorials
    alone, and without this there is simply no topic tree.
    """
    if not cfg.TOPIC_DATA.is_file():
        return {}
    return (load_yaml_no_duplicate_keys(cfg.TOPIC_DATA.read_text()) or {}).get("topics") or {}


def load_topic_groups() -> list[dict]:
    """Broader, cross-module groupings for the "browse by topic" page
    (`write_topics_page()`) — see `planning/curriculum/topic-groups.yaml`'s
    own header comment for what these are and why they're a separate file
    from `topics.yaml` above. Optional, the same way the topic tree's own
    data is: without the file, there's simply no topics page."""
    if not cfg.TOPIC_GROUPS_DATA.is_file():
        return []
    data = load_yaml_no_duplicate_keys(cfg.TOPIC_GROUPS_DATA.read_text()) or {}
    return data.get("groups") or []


def load_out_of_scope() -> set[str]:
    """Outcomes we have decided not to teach. Shown, and shown as decided."""
    if not cfg.SCOPE_DATA.is_file():
        return set()
    data = load_yaml_no_duplicate_keys(cfg.SCOPE_DATA.read_text()) or {}
    return {entry["code"] for entry in data.get("outcomes") or []}


def taught_where(tutorials: list[Tutorial]) -> dict[str, dict]:
    """Outcome code to the tutorial section that teaches it.

    Read from each tutorial's own `covers:` frontmatter, so a topic's link
    cannot point somewhere the tutorial does not claim. A claim for a section
    the page no longer has is left out, as dev/curriculum_map.py leaves it out.
    """
    where: dict[str, dict] = {}
    for tutorial in tutorials:
        if tutorial.archived or tutorial.status != "live" or not tutorial.is_default:
            continue
        for anchor, claim in (tutorial.meta.get("covers") or {}).items():
            if anchor not in tutorial.anchors:
                note(tutorial.path, f"declares `covers:` for {anchor!r}, which is not a section "
                                    "of it now, so the topic tree leaves that claim out. Move it "
                                    "to the section that teaches it, or delete it")
                continue
            for code in claim.get("covers") or []:
                where.setdefault(code, {
                    "title": tutorial.title,
                    "href": f"tutorials/{tutorial.slug}.html#{anchor}",
                })
    return where


def topic_tiers(topics: dict) -> dict[str, int]:
    """How much you need to know before a topic — its column in the tree.

    A topic with no prerequisites is tier 0; anything else is one past the
    deepest thing it needs. The glossary's tests guarantee no cycles, so this
    always terminates.
    """
    tier: dict[str, int] = {}

    def depth(code: str) -> int:
        if code in tier:
            return tier[code]
        needs = [n for n in (topics[code].get("needs") or []) if n in topics]
        tier[code] = 0 if not needs else 1 + max(depth(n) for n in needs)
        return tier[code]

    for code in topics:
        depth(code)
    return tier


def outcome_of(topics: dict, code: str) -> str:
    """Which learning outcome a topic serves, for looking it up in anything
    keyed by outcome — coverage, strands, the out-of-scope list.

    A topic code and an outcome code were once the same string. They are not
    any more: several topics may serve one outcome where the descriptor bundles
    ideas a student meets weeks apart, and one topic may serve several where it
    folds in what a thin neighbouring outcome asked for. Where a topic serves
    several, the first is the one the tree colours and links by. Falling back
    to the topic's own code keeps `PRE-` groundwork, which serves none, working
    as it did.
    """
    claimed = (topics.get(code) or {}).get("outcome")
    if not claimed:
        return code
    return claimed if isinstance(claimed, str) else claimed[0]


def topic_layout(topics: dict, strands: dict[str, str]) -> tuple[dict, float, float]:
    """Where every topic sits: one row per tier, reading downwards.

    `strands` is keyed by topic code, already resolved by the caller.

    **Top to bottom is dependency.** Nothing in the top row needs anything, and
    nothing ever points upwards, so how far down a topic sits is how much has to
    come first. That is the one thing the layout has to make obvious.

    Vertical because that is how a page scrolls. The first attempt at this gave
    each subject its own column, which is the direct flip of the old horizontal
    tree — and measured 5854px wide against 756px tall, which is a horizontal
    tree wearing a hat. With twelve subjects there is no width to spare, so
    subject stops being an axis and becomes a sort: a tier wider than
    ``TREE_COLUMNS`` wraps onto more lines, and within a tier topics are grouped
    by subject so like still sits beside like.

    Lines are centred, which is what makes it read as a tree rather than a
    left-aligned list — a narrow tier looks like a narrow tier.
    """
    tier = topic_tiers(topics)
    rows: dict[int, list[str]] = {}
    for code in topics:
        rows.setdefault(tier[code], []).append(code)

    span = TOPIC_W + ROW_GAP
    width = TREE_PAD * 2 + TREE_COLUMNS * span - ROW_GAP

    place: dict[str, dict] = {}
    y = TREE_PAD
    for level in sorted(rows):
        members = sorted(
            rows[level],
            key=lambda c: (strands.get(c, "other"), topics[c]["name"]),
        )
        lines = [members[i:i + TREE_COLUMNS] for i in range(0, len(members), TREE_COLUMNS)]
        top = y
        for line in lines:
            left = (width - (len(line) * span - ROW_GAP)) / 2
            for column, code in enumerate(line):
                place[code] = {
                    "x": left + column * span,
                    "y": y,
                    "tier": level,
                    "strand": strands.get(code, "other"),
                }
            y += TOPIC_H + ROW_GAP
        place[f"band:{level}"] = {"y": top, "height": y - top - ROW_GAP}
        y += TIER_GAP

    return place, width, y - TIER_GAP + TREE_PAD


def tier_label(level: int) -> str:
    """What a tier stripe says, in words a student can act on.

    "Tier 3" is a number about the data structure. "Three layers down" is a
    number about how much has to come first, which is the only reason anybody
    is reading the stripe.
    """
    if level == 0:
        return "start anywhere here"
    words = ["", "one", "two", "three", "four", "five", "six", "seven", "eight"]
    count = words[level] if level < len(words) else str(level)
    return f"{count} layer{'' if level == 1 else 's'} down"


def tree_data(tutorials: list[Tutorial]) -> dict:
    """Everything the topic tree page needs, as one blob of data.

    Assembled here rather than fetched by the page, because the page is static
    and a fetch would be one more thing to fail on a school network.
    """
    topics = load_topics()
    if not topics:
        return {}
    by_outcome = load_strands()
    strands = {
        code: str(topic["strand"]) if topic.get("strand")
        else by_outcome.get(outcome_of(topics, code), "other")
        for code, topic in topics.items()
    }
    excluded = load_out_of_scope()
    taught = taught_where(tutorials)
    place, width, height = topic_layout(topics, strands)

    nodes = []
    for code, topic in sorted(topics.items()):
        at = place[code]
        where = taught.get(outcome_of(topics, code))
        if code.startswith("PRE-"):
            state = "groundwork"
        elif outcome_of(topics, code) in excluded:
            state = "excluded"
        else:
            state = "taught" if where else "planned"
        nodes.append({
            "code": code,
            "name": topic["name"],
            "plain": " ".join(topic["plain"].split()),
            "uses": [" ".join(u.split()) for u in topic.get("uses") or []],
            "needs": [n for n in (topic.get("needs") or []) if n in topics],
            "strand": at["strand"],
            "tier": at["tier"],
            "x": at["x"],
            "y": at["y"],
            "state": state,
            "where": where,
        })

    bands = [
        {
            "tier": int(key[5:]),
            "label": tier_label(int(key[5:])),
            "y": value["y"],
            "height": value["height"],
        }
        for key, value in place.items() if key.startswith("band:")
    ]
    return {
        "nodes": nodes,
        "bands": sorted(bands, key=lambda b: b["y"]),
        "width": width,
        "height": height,
        "node": {"w": TOPIC_W, "h": TOPIC_H},
    }



# Nodes wide enough for two short lines of title, spaced so an arrow between
# them is visibly an arrow rather than a join.
NODE_W, NODE_H = 132, 46
GAP_X, GAP_Y = 34, 30
LANE_LABEL_W = 96
MAP_PAD = 14


def strand_of(codes: list[str], outcomes: dict[str, str]) -> str:
    """The strand a tutorial mostly belongs to.

    Mostly, not only: a tutorial that teaches four algorithm outcomes and one
    programming one belongs on the algorithms row, and putting it in both would
    make a diagram nobody can follow. Ties break alphabetically, which is
    arbitrary but stable — and a genuine tie is worth noticing in itself, since
    it usually means the tutorial is about two things.
    """
    counts: dict[str, int] = {}
    for code in codes:
        strand = outcomes.get(code)
        if strand:
            counts[strand] = counts.get(strand, 0) + 1
    if not counts:
        return "other"
    best = max(counts.values())
    return sorted(s for s, n in counts.items() if n == best)[0]


def load_strands() -> dict[str, str]:
    """Outcome code to strand, from the curriculum data if it is there.

    Optional on purpose: the site has to build without the planning folder, so
    a missing file means a map without lanes rather than a failed build.
    """
    if not cfg.OUTCOME_DATA.is_file():
        return {}
    data = load_yaml_no_duplicate_keys(cfg.OUTCOME_DATA.read_text()) or {}
    return {e["code"]: e["strand"] for e in data.get("outcomes") or []}


def map_rows(members: list[Tutorial], strands: dict[str, str]) -> list[tuple[str, list]]:
    """Tutorials grouped into strand bands, bands in teaching order.

    A band is broken and started again if the series leaves it and comes back —
    programming runs 1 to 4, goes away for algorithms and probability, and
    returns at 17. Drawing that as one row would put an arrow across the whole
    diagram and suggest a continuity that is not there.
    """
    rows: list[tuple[str, list]] = []
    for tutorial in members:
        declared = (tutorial.meta.get("covers") or {}).values()
        covered = [c for claim in declared for c in (claim.get("covers") or [])]
        touched = [c for claim in declared for c in (claim.get("touches") or [])]
        strand = strand_of(covered or touched, strands)
        if rows and rows[-1][0] == strand:
            rows[-1][1].append(tutorial)
        else:
            rows.append((strand, [tutorial]))
    return rows


def render_knowledge_map(members: list[Tutorial], strands: dict[str, str]) -> str:
    """The series as nodes and arrows: what follows what, and what leans on what.

    A contents list says what order to read in. It does not say that Tutorial 17
    leans on five earlier ones, or that the course spends four tutorials on
    programming before mathematics appears. The map is for the reader deciding
    where they are and what they need first.
    """
    if len(members) < 3:
        return ""

    rows = map_rows(members, strands)
    widest = max(len(row) for _, row in rows)
    width = LANE_LABEL_W + widest * NODE_W + (widest - 1) * GAP_X + MAP_PAD * 2
    height = len(rows) * NODE_H + (len(rows) - 1) * GAP_Y + MAP_PAD * 2

    place: dict[str, tuple[float, float]] = {}
    for index, (_, row) in enumerate(rows):
        y = MAP_PAD + index * (NODE_H + GAP_Y)
        for column, tutorial in enumerate(row):
            place[tutorial.slug] = (LANE_LABEL_W + column * (NODE_W + GAP_X), y)

    parts = [
        f'<svg class="dl-map" viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="Map of the tutorials, grouped by subject, '
        f'with arrows for what follows what">',
        '<defs><marker id="dl-arrow" viewBox="0 0 8 8" refX="7" refY="4" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L8 4 L0 8 z" fill="currentColor"/></marker>'
        '<marker id="dl-arrow-back" viewBox="0 0 8 8" refX="7" refY="4" '
        'markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
        '<path d="M0 0 L8 4 L0 8 z" fill="currentColor"/></marker></defs>',
    ]

    for tutorial in members:
        for fan, target in enumerate(back_links(tutorial, members)):
            parts.append(
                arrow_between(place, tutorial.slug, target, "dl-map-back", fan)
            )
    for before, after in zip(members, members[1:]):
        parts.append(arrow_between(place, before.slug, after.slug, "dl-map-next"))

    for index, (strand, row) in enumerate(rows):
        y = MAP_PAD + index * (NODE_H + GAP_Y)
        parts.append(
            f'<text class="dl-map-lane" x="{MAP_PAD}" y="{y + NODE_H / 2 + 4}">'
            f"{html.escape(strand)}</text>"
        )
        for tutorial in row:
            x, _ = place[tutorial.slug]
            href = tutorial.out_path.relative_to(cfg.OUT).as_posix()
            label = tutorial.title.split(":", 1)[-1].strip()
            parts.append(
                f'<a class="dl-map-node" href="{href}">'
                f'<title>{html.escape(tutorial.title)}</title>'
                f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="5"/>'
                f'<text x="{x + NODE_W / 2}" y="{y + NODE_H / 2 + 4}">'
                f"{html.escape(shorten(label))}</text></a>"
            )

    parts.append("</svg>")
    return "".join(p for p in parts if p)


def shorten(label: str, limit: int = 22) -> str:
    """Node labels are one line. A title that will not fit is cut at a word."""
    if len(label) <= limit:
        return label
    cut = label[:limit].rsplit(" ", 1)[0]
    return (cut or label[:limit]) + "…"


def back_links(tutorial: Tutorial, members: list[Tutorial]) -> list[str]:
    """Earlier tutorials this one names in its own text, skipping its neighbour.

    By title rather than by number, because the numbers are gone — and because
    a title is what a tutorial would say anyway. Evidence rather than intention:
    nobody maintains this list, it is found by reading. The tutorial immediately
    before is left out, since the reading-order arrow already says that one.
    """
    text = tutorial.body_html
    return [
        earlier.slug
        for earlier in members
        if 0 < earlier.order < tutorial.order - 1
        and len(earlier.title) > 6
        and earlier.title in text
    ]


def arrow_between(place: dict, a: str, b: str, css: str, fan: int = 0) -> str:
    """One arrow, routed so it can be told apart from the others.

    `fan` separates several arrows leaving the same node. Tutorial 17 names five
    earlier tutorials, and without this they would all leave the same point,
    travel the same column and arrive as one thick unreadable line. Each is bowed
    a little further out than the last.
    """
    if a not in place or b not in place:
        return ""
    (ax, ay), (bx, by) = place[a], place[b]

    if ay == by:
        # Same row: straight across, edge to edge.
        x1, x2 = (ax + NODE_W, bx) if ax < bx else (ax, bx + NODE_W)
        y = ay + NODE_H / 2
        return f'<path class="{css}" d="M{x1} {y} L{x2} {y}"/>'

    # Different rows: leave the side nearer the destination and arrive on the
    # matching side, bowed outwards so the path is a curve rather than a spine.
    going_up = by < ay
    y1 = ay if going_up else ay + NODE_H
    y2 = by + NODE_H if going_up else by
    x1, x2 = ax + NODE_W / 2, bx + NODE_W / 2
    reach = abs(y2 - y1) / 2 + fan * 22
    side = NODE_W * 0.7 + fan * 26 if going_up else 0
    return (
        f'<path class="{css}" d="M{x1} {y1} '
        f"C{x1 + side} {y1 - reach if going_up else y1 + reach}, "
        f"{x2 + side} {y2 + reach if going_up else y2 - reach}, "
        f'{x2} {y2}"/>'
    )


def strand_key(data: dict) -> str:
    """The colour on each node, said out loud.

    Every node carries its subject as a coloured edge and, until this, the only
    way to find out what a colour meant was to choose a topic and read the
    panel — which is the wrong way round for a key. Generated from the strands
    actually on the tree, so it cannot list a colour nothing uses or miss one
    that is there.
    """
    strands = sorted({node["strand"] for node in data.get("nodes") or []})
    if not strands:
        return ""
    items = "".join(
        f'<span class="dl-tree-key-strand">'
        f'<span class="dl-tree-hue" data-strand="{html.escape(strand)}"></span>'
        f"{html.escape(strand)}</span>"
        for strand in strands
    )
    return (
        '<details class="dl-tree-strands"><summary>What the colours mean</summary>'
        '<p class="dl-tree-strands-note">The stripe down the left of each topic '
        "shows its subject. The columns do not group subjects; only depth does. "
        "So the colour is how you follow one subject down the tree.</p>"
        f'<p class="dl-tree-key-list">{items}</p></details>'
    )


def write_tree_page(shell: str, tutorials: list[Tutorial]) -> Path | None:
    """The topic tree: every topic in both descriptors, and what needs what.

    Its own page rather than part of the contents, because it wants the whole
    window and the contents page wants to be a list. It uses the same shell, so
    it gets the masthead, the settings panel and the reader's theme for free —
    which is most of what "light and dark" would otherwise cost.
    """
    data = tree_data(tutorials)
    if not data:
        return None

    body = (
        '<h1>The topic tree</h1>'
        '<p class="dl-tree-intro">Every topic both modules cover, and the order '
        "they build in. <strong>The tree reads downwards.</strong> Topics in the "
        "top row need nothing before them, so you could start any of them today. "
        "The further down a topic sits, the more you need to know first. Drag to "
        "move around, scroll to zoom, and choose any topic to see what it is, "
        "where it comes up in computing, and where it is taught."
        + (' The <a href="map.html">topic map</a> shows these topics as a map.'
           if (cfg.ROOT / "map" / "graph.json").is_file() else "")
        + "</p>"
        '<div class="dl-tree-layout">'
        '<div class="dl-tree-main">'
        '<div class="dl-tree-controls">'
        '<button type="button" id="dl-tree-out" aria-label="Zoom out">−</button>'
        '<button type="button" id="dl-tree-fit" aria-label="Fit the width and return to the top">fit</button>'
        '<button type="button" id="dl-tree-in" aria-label="Zoom in">+</button>'
        "</div>"
        '<div class="dl-tree-frame" id="dl-tree">'
        '<div class="dl-tree-canvas" id="dl-tree-canvas"></div>'
        "</div>"
        '<p class="dl-tree-key">'
        '<span class="dl-tree-swatch" data-state="taught"></span>taught here'
        '<span class="dl-tree-swatch" data-state="planned"></span>planned'
        '<span class="dl-tree-swatch" data-state="groundwork"></span>groundwork'
        '<span class="dl-tree-swatch" data-state="excluded"></span>not on this course'
        "</p>"
        + strand_key(data)
        + "</div>"
        '<aside class="dl-tree-detail" id="dl-tree-detail" aria-live="polite"></aside>'
        "</div>"
    )

    strands = load_strands()
    for (_, _), members in sorted(series_of(tutorials).items()):
        svg = render_knowledge_map(members, strands)
        if svg:
            body += (
                '<h2 class="dl-tree-second">How the tutorials relate</h2>'
                '<figure class="dl-map-figure">' + svg +
                "<figcaption>Solid arrows show the reading order. A dashed arrow "
                "means the later tutorial builds on the earlier one and says so "
                "in its own text. Choose any box to open that "
                "tutorial.</figcaption></figure>"
            )
            break

    manifest = {"slug": "tree", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "The topic tree",
        "{{VERSION}}": "1",
        "{{SLUG}}": "tree",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": '<span class="dl-crumbs">topic tree</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": (
            '<script type="application/json" id="dewlab-tree">'
            + json.dumps(data).replace("<", "\\u003c")
            + "</script>\n"
            + f'<script type="module" src="{versioned("assets/", "tree.js")}"></script>'
        ),
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": body,
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("tree", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("tree", "1"),
    }
    page = fill_shell(shell, tokens, "the tree page")

    cfg.OUT.mkdir(parents=True, exist_ok=True)
    target = cfg.OUT / "tree.html"
    target.write_text(page)
    return target


def load_map() -> tuple[dict, dict]:
    """The map's graph (map/graph.json, edited by hand) and its committed
    layout (map/layout.json, written by dev/map_layout.py)."""
    graph_path, layout_path = cfg.ROOT / "map" / "graph.json", cfg.ROOT / "map" / "layout.json"
    for path in (graph_path, layout_path):
        if not path.is_file():
            fail(path, "is missing. map/README.md says what the map's two files are.")
    try:
        return json.loads(graph_path.read_text()), json.loads(layout_path.read_text())
    except json.JSONDecodeError as exc:
        fail(cfg.ROOT / "map", f"is not valid JSON: {exc}")


def toc_name(tutorial: Tutorial, anchor: str) -> str | None:
    """The heading a section anchor belongs to, from the page's own contents."""
    stack = list(tutorial.toc)
    while stack:
        entry = stack.pop()
        if entry.get("id") == anchor:
            return str(entry.get("name", ""))
        stack.extend(entry.get("children") or [])
    return None


def map_data(registry: dict[str, Tutorial], catalog: dict[str, "Course"]) -> dict:
    """What the map page draws, from the committed graph and layout and from the
    tutorials as they are now.

    Titles, sections and courses are read here rather than stored, so the map
    cannot name a page the site does not have: a topic that points at a missing
    tutorial or section stops the build, the same as a link in a tutorial does.
    """
    graph, layout = load_map()
    graph_path = cfg.ROOT / "map" / "graph.json"
    topics = {t["id"]: t for t in graph["topics"]}
    districts = {d["id"]: d for d in graph["districts"]}
    regions = {r["id"]: r for r in graph["regions"]}
    problems: list[str] = []

    def need(ok: bool, message: str) -> None:
        if not ok:
            problems.append(message)

    for code, topic in topics.items():
        need(topic["district"] in districts, f"topic {code}: district {topic['district']!r} is not declared")
        for n in topic.get("needs") or []:
            need(n in topics, f"topic {code} needs {n!r}, which is not a topic")
        need(code in layout["towns"], f"topic {code} has no place in map/layout.json")
        for step in topic.get("steps") or []:
            target = registry.get(step["tutorial"])
            need(target is not None, f"topic {code}: step names {step['tutorial']!r}, which is not a tutorial")
            if target is not None and step.get("section") and step["section"] not in target.anchors:
                note(graph_path, f"topic {code} points at {step['tutorial']}#{step['section']}, a "
                                 "section that page no longer has, so the map links to the top of the page")
                del step["section"]
    for code in layout["towns"]:
        if code not in topics:
            note(cfg.ROOT / "map" / "layout.json", f"places {code!r}, which is not a topic; "
                                               "it is ignored. Re-run dev/map_layout.py to tidy it")
    for lm in graph["landmarks"]:
        need(lm["tutorial"] in registry, f"landmark {lm['tutorial']!r} is not a tutorial")
        need(lm["tutorial"] in layout["landmarks"], f"landmark {lm['tutorial']} has no place in map/layout.json")
        for a in lm.get("at") or []:
            need(a in topics, f"landmark {lm['tutorial']} draws on {a!r}, which is not a topic")
    for c in graph["continents"]:
        need(c["id"] in layout["continents"], f"continent {c['id']} has no place in map/layout.json")
    if problems:
        shown = "\n  ".join(problems[:12])
        more = f"\n  ...and {len(problems) - 12} more" if len(problems) > 12 else ""
        fail(graph_path, f"does not match the tutorials or the layout:\n  {shown}{more}\n"
                         "Fix map/graph.json, or run python3 dev/map_layout.py if a topic, district "
                         "or continent was added.")

    placed = {s["tutorial"] for t in topics.values() for s in t["steps"]} | {lm["tutorial"] for lm in graph["landmarks"]}
    unplaced = sorted(slug for slug, t in registry.items()
                      if slug not in placed and not t.archived and not t.is_practice)
    if unplaced:
        say(f"note: {len(unplaced)} tutorials are on no topic of the map yet "
              f"(first: {', '.join(unplaced[:3])}). Add them under map/graph.json.")

    course_titles: dict[str, list[str]] = {}
    for course in catalog.values():
        for series in course.contents:
            for slug in series.ids:
                if course.title not in course_titles.setdefault(slug, []):
                    course_titles[slug].append(course.title)
        for slug in course.mixed:
            if course.title not in course_titles.setdefault(slug, []):
                course_titles[slug].append(course.title)

    def step_out(step: dict) -> dict:
        target = registry[step["tutorial"]]
        section = step.get("section")
        return {"slug": target.slug, "title": target.title,
                "section": toc_name(target, section) if section else None,
                "href": f"tutorials/{target.slug}.html" + (f"#{section}" if section else ""),
                "role": step.get("role"), "courses": course_titles.get(target.slug, [])}

    teaches: dict[str, list[str]] = {}
    for code, topic in topics.items():
        for step in topic["steps"]:
            if step.get("role") == "teaches":
                teaches.setdefault(step["tutorial"], []).append(code)
    routes = []
    for course in catalog.values():
        path: list[str] = []
        count = 0
        for series in course.contents:
            for slug in series.ids:
                count += 1
                path.extend(c for c in teaches.get(slug, []) if c not in path)
        routes.append({"id": course.id, "title": course.title, "path": path, "tutorials": count})

    land_order = [c["id"] for c in graph["continents"]]
    region_order = [r for c in graph["continents"] for r in c["regions"]]
    district_order = [d["id"] for r in region_order for d in graph["districts"] if d["region"] == r]
    town_at = layout["towns"]
    count_in: dict[str, int] = {}
    for topic in topics.values():
        for key in (topic["district"], districts[topic["district"]]["region"]):
            count_in[key] = count_in.get(key, 0) + 1

    def town_order(code: str) -> tuple:
        d = districts[topics[code]["district"]]
        return (land_order.index(town_at[code]["land"]), region_order.index(d["region"]),
                district_order.index(d["id"]), town_at[code]["tier"], topics[code]["name"])

    return {
        "bounds": layout["bounds"], "coast": layout["coast"], "waves": layout["waves"],
        "bridges": layout["bridges"], "tower": graph["tower"],
        "plains": layout["plains"],
        # a continent that is one country with no name of its own takes the country's
        "continents": [{"id": c["id"], "kind": c.get("kind", "continent"),
                        **{k: c.get(k) or (regions[c["regions"][0]].get(k, "") if len(c["regions"]) == 1 else "")
                           for k in ("name", "fancy", "blurb", "lore")},
                        "regions": c["regions"], **layout["continents"][c["id"]]}
                       for c in graph["continents"]],
        "regions": [{"id": r, "name": regions[r]["name"], "fancy": regions[r].get("fancy", ""),
                     "blurb": regions[r].get("blurb", ""), "lore": regions[r].get("lore", ""),
                     "terrain": regions[r].get("terrain", ""), "count": count_in.get(r, 0),
                     "continent": next(c["id"] for c in graph["continents"] if r in c["regions"]),
                     **layout["regions"][r]} for r in region_order],
        "districts": [{"id": d, "name": districts[d]["name"], "blurb": districts[d].get("blurb", ""),
                       "region": districts[d]["region"], "count": count_in.get(d, 0),
                       **layout["districts"].get(d, {"shade": 0, "land": "", "label": [0, 0]})}
                      for d in district_order],
        "towns": [{"code": code, "name": topics[code]["name"], "plain": topics[code].get("plain", ""),
                   "district": topics[code]["district"], "region": districts[topics[code]["district"]]["region"],
                   "needs": topics[code].get("needs") or [],
                   "state": "taught" if any(s.get("role") == "teaches" for s in topics[code]["steps"]) else "planned",
                   "steps": [step_out(s) for s in topics[code]["steps"]],
                   **town_at[code]} for code in sorted(topics, key=town_order)],
        "landmarks": [{"slug": lm["tutorial"], "title": registry[lm["tutorial"]].title, "kind": lm.get("kind"),
                       "at": lm.get("at") or [], "tower": bool(lm.get("tower")),
                       "href": f"tutorials/{lm['tutorial']}.html", "x": layout["landmarks"][lm["tutorial"]][0],
                       "y": layout["landmarks"][lm["tutorial"]][1]} for lm in graph["landmarks"]],
        "courses": routes,
    }


def map_list_html(data: dict) -> str:
    """Every topic as a nested list: continents, countries, districts, topics.
    It is the map for a reader with no script, a screen reader or a keyboard,
    and it names every page a topic teaches."""
    by_district: dict[str, list[dict]] = {}
    for town in data["towns"]:
        by_district.setdefault(town["district"], []).append(town)
    out = []
    for continent in data["continents"]:
        title = continent["fancy"] or continent["name"]
        if continent["fancy"] and continent["name"]:
            title = f"{continent['fancy']} ({continent['name']})"
        out.append(f'<h3>{html.escape(title)}</h3>')
        for region in (r for r in data["regions"] if r["continent"] == continent["id"]):
            rtitle = f"{region['fancy']} ({region['name']})" if region["fancy"] else region["name"]
            out.append(f'<details class="dl-tmap-list-country"><summary>{html.escape(rtitle)}</summary>')
            for district in (d for d in data["districts"] if d["region"] == region["id"]):
                out.append(f'<h4>{html.escape(district["name"])}</h4><ul>')
                for town in by_district.get(district["id"], []):
                    pages = [s for s in town["steps"] if s["role"] == "teaches"]
                    links = "".join(
                        f'<li><a href="{html.escape(s["href"], quote=True)}">{html.escape(s["title"])}</a></li>'
                        for s in pages)
                    note = "" if pages else " <em>(page still to be written)</em>"
                    out.append(f'<li id="topic-{html.escape(town["code"])}"><strong>{html.escape(town["name"])}</strong>{note}'
                               f'<br>{html.escape(town["plain"])}'
                               + (f"<ul>{links}</ul>" if links else "") + "</li>")
                out.append("</ul>")
            out.append("</details>")
    return "".join(out)


def write_map_page(shell: str, registry: dict[str, Tutorial], catalog: dict[str, "Course"]) -> Path:
    """The topic map: every topic as a town, in countries on continents, with
    the roads between them. The picture is drawn by assets/map.js from a data
    block in the page; the list under it is the same map without a script.
    """
    data = map_data(registry, catalog)
    body = (
        "<h1>The topic map</h1>"
        '<p class="dl-tmap-intro">Every topic on dewlab is a town. Towns that belong '
        "together are in the same country, and countries that share many roads are on the "
        "same continent. Drag the map to move, scroll to zoom, and choose a town to see what it is, "
        "what comes before it and where it is taught.</p>"
        '<div class="dl-tmap" id="dl-tmap" hidden></div>'
        '<noscript><p class="dl-tmap-intro">The picture needs JavaScript. The list below has every topic.</p></noscript>'
        '<h2 id="dl-tmap-list-title">Every topic, as a list</h2>'
        '<div class="dl-tmap-list" aria-labelledby="dl-tmap-list-title">' + map_list_html(data) + "</div>"
    )
    manifest = {"slug": "map", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "The topic map",
        "{{VERSION}}": "1",
        "{{SLUG}}": "map",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": '<span class="dl-crumbs">topic map</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": (
            f'<link rel="stylesheet" href="{versioned("assets/", "map.css")}">'
            '<script type="application/json" id="dewlab-map">'
            + json.dumps(data, separators=(",", ":")).replace("<", "\\u003c")
            + "</script>\n"
            + f'<script type="module" src="{versioned("assets/", "map.js")}"></script>'
        ),
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": body,
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("map", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("map", "1"),
    }
    page = fill_shell(shell, tokens, "the map page")
    cfg.OUT.mkdir(parents=True, exist_ok=True)
    target = cfg.OUT / "map.html"
    target.write_text(page)
    return target


def write_topics_page(
    shell: str,
    registry: dict[str, Tutorial],
    practice: dict[str, list[Tutorial]],
    context: dict[str, list[Tutorial]] | None = None,
) -> Path | None:
    """"Browse by topic" — the topic tree's sibling, and a genuinely
    different question. The tree says what a topic needs before it, for
    a reader moving through the course in order; this page is for a
    reader who already has some of it behind them and wants to jump
    straight to, say, everything about trigonometry, in whatever order
    suits them (planning/curriculum/topic-groups.yaml's own header
    comment goes into more depth on the two files' different jobs).

    A group naming a tutorial `registry` doesn't have (a typo, a rename,
    or — same as `topics.yaml`'s own module-level path — simply a test
    building a small, sandboxed set of tutorials that was never going to
    contain dewlab's real ones) is skipped rather than fatal, with a note
    on stderr. `tests/test_build.py`'s own
    `TestTopicGroupsMatchRealTutorials` is what actually holds this file
    accountable against the genuine tutorials on disk, the same way nothing
    checks `topics.yaml` against a build's tutorials either.
    """
    groups = load_topic_groups()
    if not groups:
        return None

    body = [
        "<h1>Browse by topic</h1>",
        '<p class="dl-topics-intro">The tutorials list reads top to bottom '
        "in the order the course teaches them. This page cuts across that "
        "— everything about one topic, gathered in one place, for "
        "practicing in whatever order suits you rather than paging "
        "through the whole course to find it. A tutorial that genuinely "
        "spans two topics is listed under both.</p>",
        render_search_box("Search — e.g. loops, probability, sorting…"),
    ]
    any_group_rendered = False
    for group in groups:
        items = []
        for ident in group["tutorials"]:
            member = registry.get(str(ident))
            if member is None:
                say(f'note: topic-groups.yaml group "{group["key"]}" names '
                    f"{ident}, which this build has no tutorial for")
                continue
            href = member.out_path.relative_to(cfg.OUT).as_posix()
            extra = companion_buttons_html(member, practice, context)
            items.append(
                f'<li><a class="dl-contents-btn" href="{href}"{progress_attrs(member)}>'
                f'<span class="dl-contents-kicker">Explore</span>'
                f"{html.escape(member.title)}</a>{extra}</li>"
            )
        if not items:
            continue
        any_group_rendered = True
        body.append(f'<h2 id="{html.escape(group["key"], quote=True)}">'
                     f'{html.escape(group["name"])}</h2>')
        body.append(f'<p class="dl-panel-note">{html.escape(group["intro"].strip())}</p>')
        body.append('<ol class="dl-contents">')
        body.extend(items)
        body.append("</ol>")

    if not any_group_rendered:
        return None

    manifest = {"slug": "topics", "version": 1, "assetBase": "assets/",
                "dataBase": "data/", "cells": [], "assetVersions": {}}
    tokens = {
        "{{TITLE}}": "Browse by topic",
        "{{VERSION}}": "1",
        "{{SLUG}}": "topics",
        "{{MODULE}}": "",
        "{{YEAR}}": "",
        "{{SERIES}}": "",
        "{{CRUMBS}}": '<span class="dl-crumbs">browse by topic</span>',
        "{{ASSET_BASE}}": "assets/",
        "{{STYLE_URL}}": versioned("assets/", "tutorial-style.css"),
        "{{FAVICON_URL}}": versioned("assets/", "favicon.svg"),
        "{{SEARCH_JS_URL}}": versioned("assets/", "search.js"),
        "{{NAV_SEARCH}}": nav_search_html(),
        "{{KATEX_CSS_URL}}": versioned("assets/", "vendor/katex.min.css"),
        "{{ACCESSIBLE_FONTS_CSS_URL}}": versioned("assets/", "vendor/accessible-fonts.css"),
        "{{RUNTIME_URL}}": versioned("assets/", "tutorial-runtime.js"),
        "{{ROOT_BASE}}": "",
        "{{NAV_PREV_NEXT}}": '<a class="dl-nav-up" href="all-tutorials.html">All tutorials</a>',
        "{{PAGE_SCRIPT}}": "",
        "{{CANONICAL}}": "",
        "{{DOWNLOAD}}": "",
        "{{BODY}}": "".join(body),
        "{{MANIFEST_JSON}}": json.dumps(manifest).replace("<", "\\u003c"),
        "{{FOOTER}}": site_footer("topics", "1"),
        "{{REPORT_DOORS}}": report_doors_panel_html("topics", "1"),
    }
    page = fill_shell(shell, tokens, "the topics page")

    cfg.OUT.mkdir(parents=True, exist_ok=True)
    target = cfg.OUT / "topics.html"
    target.write_text(page)
    return target


def write_search_index(
    tutorials: list[Tutorial],
    registry: dict[str, Tutorial],
    groups: dict[tuple[str, str], list[Tutorial]],
) -> Path:
    """One JSON file, `assets/search-index.json`, listing every live
    tutorial with what a reader might actually search for: its title,
    which course and series it belongs to, and — this is the part that
    makes it more than a title search — the terms its own glossary
    entry says it *introduces* (`own_glossary()`, not the cumulative
    one: a later tutorial in the same series has already inherited an
    earlier term, and searching for it should point at where it was
    actually taught, not at every page downstream of that).

    `assets/search.js` loads this once and does the actual matching
    client-side — nothing server-side to run, consistent with the rest
    of a site that is just static files. Archived, practice and
    context pages are left out: a search result should be something
    worth sending a reader to first, and all three already sit off the
    main reading order for the same reason.
    """
    documents = []
    for tutorial in tutorials:
        if tutorial.archived or not tutorial.is_default or tutorial.is_companion:
            continue
        terms = sorted({entry["term"] for entry in own_glossary(tutorial) if entry.get("term")})
        course = courses().get(tutorial.course)
        documents.append({
            "id": tutorial.slug,
            "title": tutorial.title,
            # The default course, under the names search.js reads; every
            # course, by id, for whoever needs the whole picture.
            "module": tutorial.course,
            "moduleTitle": course.title if course else "",
            "series": course.series_title(tutorial.series) if course and tutorial.series else "",
            "courses": tutorial.courses,
            "url": tutorial.out_path.relative_to(cfg.OUT).as_posix(),
            "terms": terms,
        })
    target = cfg.OUT / "assets" / "search-index.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(documents, ensure_ascii=False))
    return target


OUTCOME_SUBJECTS = {
    "MIT": "maths",       # Maths for Information Technology, 5N18396
    "PDP": "computing",   # Programming and Design Principles, 5N2927
    "CMPS": "computing",  # Computational Methods and Problem Solving, 5N0554
}

LEVEL_BANDS = ((2, "beginner"), (3, "intermediate"), (99, "advanced"))


def level_for_tier(tier: int) -> str:
    for ceiling, name in LEVEL_BANDS:
        if tier <= ceiling:
            return name
    return "advanced"


def tutorial_facets(
    tutorials: list[Tutorial],
) -> dict[str, dict]:
    """What each tutorial can be filtered by, keyed by id.

    Three facets, none of them invented here — each is read from data that
    already exists for another purpose, so none can drift from the thing it
    describes:

      * `subjects` — from the outcome codes a tutorial claims in `covers:`.
        A tutorial covering both an MIT and a PDP outcome gets both, which is
        not a fudge: seven of them genuinely do, and a term introduced there
        belongs to both subjects.
      * `level` — from the *deepest* outcome it covers, since that is the
        one gating how far in you need to be to follow the whole thing.
        The shallowest was tried first and is worse in both directions: it
        rates a tutorial by its easiest moment, so 150 of 222 terms came
        out "beginner", and it would cheerfully tell someone at the start
        of the course that a tutorial needing four layers of groundwork is
        approachable. Erring deep is the kinder error.
      * `groups` — the curated topic groups from topic-groups.yaml, which
        already allow a tutorial in more than one group by design.

    A tutorial claiming no outcomes (two real ones, plus every practice and
    context page)
    simply has no subject and no level. That is left as absence rather than
    guessed at, and the panel offers it as "unfiled" instead of hiding it.
    """
    topics = load_topics()
    tiers = topic_tiers(topics) if topics else {}

    groups_by_tutorial: dict[str, list[str]] = {}
    for group in load_topic_groups():
        for member in group.get("tutorials") or []:
            groups_by_tutorial.setdefault(str(member), []).append(group["key"])

    facets: dict[str, dict] = {}
    for tutorial in tutorials:
        codes = [
            code
            for claim in (tutorial.meta.get("covers") or {}).values()
            for code in (claim.get("covers") or [])
        ]
        subjects = sorted({
            OUTCOME_SUBJECTS[code.split("-")[0]]
            for code in codes
            if code.split("-")[0] in OUTCOME_SUBJECTS
        })
        depths = [tiers[code] for code in codes if code in tiers]
        facet = {"subjects": subjects}
        if depths:
            facet["level"] = level_for_tier(max(depths))
        groups = groups_by_tutorial.get(tutorial.slug)
        if groups:
            facet["groups"] = sorted(set(groups))
        facets[tutorial.slug] = facet
    return facets


def write_reference_index(tutorials: list[Tutorial]) -> Path:
    """One JSON file, `assets/reference-index.json`: every term every
    tutorial introduces, in one list, for dewmini's Library rail.

    Deliberately drops the rule a tutorial page's own Reference panel is
    built around — never show a reader a term they haven't been taught yet
    (`cumulative_glossary()`, assembled per page and series position).
    dewmini has no position in a series; it's the workspace a reader opens
    outside the curriculum, so this index is the plain union instead.

    Built from `own_glossary()` so each entry names the tutorial that
    introduced it — a reader meeting an unfamiliar term can see where it's
    actually taught. Deduplicated on `(term, kind)`, first definition
    winning, the same key `cumulative_glossary()` dedupes on.

    Names the tutorial's *title*, not a link: this file ships inside
    dewmini's offline bundle, which carries no tutorials, so a link would
    404 for every offline reader.
    """
    facets = tutorial_facets(tutorials)
    seen: dict[tuple[str, str], dict] = {}
    for tutorial in sorted(tutorials, key=lambda t: t.slug):
        if tutorial.archived or not tutorial.is_default or tutorial.is_companion:
            continue
        facet = facets.get(tutorial.slug, {})
        for entry in own_glossary(tutorial):
            key = (entry["term"], entry["kind"])
            if key in seen:
                continue
            record = {
                "term": entry["term"],
                "kind": entry["kind"],
                "definition": entry["definition"],
                "origin": tutorial.title,
            }
            if facet.get("subjects"):
                record["subjects"] = facet["subjects"]
            if facet.get("level"):
                record["level"] = facet["level"]
            if facet.get("groups"):
                record["groups"] = facet["groups"]
            if entry.get("example"):
                record["example"] = entry["example"]
            if entry.get("signatures"):
                record["signatures"] = entry["signatures"]
            seen[key] = record

    entries = sorted(seen.values(), key=lambda e: e["term"].lower())
    target = cfg.OUT / "assets" / "reference-index.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(entries, ensure_ascii=False))
    return target
