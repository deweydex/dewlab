"""Per-page inventory for the topic search: one record per non-archived,
non-practice page, plus the search area it is handed to."""
import collections, json, re, sys
from pathlib import Path
import yaml
sys.path.insert(0, "/home/user/dewlab")
import build

OUT = Path(__file__).parent / "generated"
OUT.mkdir(exist_ok=True)
topics = build.load_topics()
strands_fine = build.load_strands()
strands = yaml.safe_load(open("/home/user/dewlab/planning/curriculum/strands.yaml"))

def old_region(code):
    prefix = code.split("-")[0]
    if prefix == "DBM": return "databases"
    if prefix == "WA": return "web"
    t = topics[code]
    fine = t.get("strand") or strands_fine.get(build.outcome_of(topics, code), "other")
    col = (strands["topics"].get(code) or {}).get("column") or strands["from_strand"].get(fine)
    return {"sets-and-number": "number", "equations-and-functions": "algebra-geometry",
            "geometry": "algebra-geometry", "chance-and-data": "chance-data",
            "programming": "programming", "software-development": "programming"}.get(col, "programming")

outcome_topics = collections.defaultdict(list)
for c, t in topics.items():
    o = t.get("outcome")
    for oc in ([o] if isinstance(o, str) else (o or [c])):
        outcome_topics[oc].append(c)

def slugify(h):
    h = re.sub(r"[`*_]", "", h)
    h = re.sub(r"[^\w\s-]", "", h.lower()).strip()
    return re.sub(r"[\s]+", "-", h)

pages = [t for t in build.load_all() if not build.VERSION_FILE_RE.match(t.path.stem)]
by_slug = {t.slug: t for t in pages}
placements = collections.defaultdict(list)
for cid, course in build.courses().items():
    for s in course.contents:
        for i in s.ids:
            placements[i].append({"course": course.title, "series": s.title})
    for m in course.mixed:
        placements[m].append({"course": course.title, "series": "mixed problems"})

def kind_of(t):
    title = t.title.lower()
    if t.is_context: return "context"
    if title.startswith("make it") or title.startswith("capstone"): return "project"
    if "a closer look" in title: return "closer-look"
    if t.slug in {"before-we-start", "faq", "how-this-course-is-built", "running-python-in-a-cell"} or title.startswith("before we start"):
        return "orientation"
    return "tutorial"

AREA_BY_COURSE = {
    "The Zen of Slashes and Surds": "number", "Web Authoring": "web", "Full Stack": "web",
    "Database Methods": "databases", "Machine Learning": "chance-data",
    "Fundamentals of Object Oriented Programming": "programming",
    "Programming and Design Principles": "programming",
}
KEYWORDS = [
    ("number", r"fraction|power|surd|root|logarithm|\blog\b|hops|number line|scientific notation|slide rule|drake|a4 paper|prime|stores a number"),
    ("web", r"browser|html|css|flexbox|grid\?|page|accessib|colour, contrast|screens|image formats|who else reads|form is sent"),
    ("databases", r"database|sql|query|table"),
    ("chance-data", r"chance|sample|probab|statist|chart|model|perceptron|classif|language model|bots?\b|data"),
    ("algebra-geometry", r"equation|parabola|graph|coordinat|angle|degrees|radian|squar|season|triangle|trig|sine|vector|matri|3d|dividing: a closer look at \(2x"),
]

records = []
for t in pages:
    if t.archived or t.is_practice:
        continue
    text = t.path.read_text()
    body = text.split("---", 2)[2] if text.startswith("---") else text
    heads = []
    for line in body.splitlines():
        m = re.match(r"^(##|###) (.+?)\s*(\{#([\w-]+)\})?\s*$", line)
        if m and not line.startswith("####"):
            heads.append({"level": len(m.group(1)), "text": m.group(2).strip(), "anchor": m.group(4) or slugify(m.group(2))})
    first = ""
    for para in re.split(r"\n\s*\n", body):
        p = para.strip()
        if p and not p.startswith(("#", "```", "<", "|", "!", "-", ">")):
            first = " ".join(p.split())[:320]
            break
    words = len(re.findall(r"[A-Za-z']+", re.sub(r"```.*?```", " ", body, flags=re.S)))
    cells = len(re.findall(r"^```(python|exec|sql|html|question)", body, flags=re.M))
    gl = t.path.parent / f"{t.slug}.glossary.yaml"
    terms = []
    if gl.is_file():
        for e in (yaml.safe_load(gl.read_text()) or {}).get("entries") or []:
            if e.get("kind") in ("concept", "formula", "function", "keyword", "operator"):
                terms.append(f"{e.get('term')} ({e.get('kind')})")
    covers = {a: (c or {}).get("covers") or [] for a, c in (t.meta.get("covers") or {}).items()}
    touches = sorted({x for c in (t.meta.get("covers") or {}).values() for x in ((c or {}).get("touches") or [])})
    codes = [x for v in covers.values() for x in v]
    votes = collections.Counter(old_region(tc) for oc in codes for tc in outcome_topics.get(oc, []))
    kind = kind_of(t)
    if kind == "context" and t.owners:
        area = None  # decided below from its owner
    elif votes:
        area = votes.most_common(1)[0][0]
    else:
        area = None
        for p in placements.get(t.slug, []):
            if p["course"] in AREA_BY_COURSE:
                area = AREA_BY_COURSE[p["course"]]; break
        if area is None:
            low = t.title.lower()
            for a, rx in KEYWORDS:
                if re.search(rx, low):
                    area = a; break
        area = area or "programming"
    records.append({
        "slug": t.slug, "title": t.title, "kind": kind, "status": t.status,
        "context_for": list(t.context_for), "placements": placements.get(t.slug, []),
        "words": words, "cells": cells, "first_paragraph": first,
        "headings": heads, "glossary": terms[:40], "covers": covers, "touches": touches,
        "old_topics": sorted({tc for oc in codes for tc in outcome_topics.get(oc, [])}),
        "area": area, "path": str(t.path.relative_to(build.ROOT)),
    })
OVERRIDE = {"issues-and-pull-requests": "programming"}
for r in records:
    if r["slug"] in OVERRIDE: r["area"] = OVERRIDE[r["slug"]]
rec_by = {r["slug"]: r for r in records}
for r in records:
    if r["area"] is None:
        owner = next((rec_by[o] for o in r["context_for"] if o in rec_by and rec_by[o]["area"]), None)
        r["area"] = owner["area"] if owner else "programming"

AREAS = ["number", "algebra-geometry", "chance-data", "programming", "databases", "web"]
json.dump(records, open(OUT / "inventory.json", "w"), indent=1)
for a in AREAS:
    mine = [r for r in records if r["area"] == a]
    json.dump(mine, open(OUT / f"inventory-{a}.json", "w"), indent=1)
    old = sorted({c for c in topics if old_region(c) == a})
    print(a, "pages", len(mine), "kinds", dict(collections.Counter(r["kind"] for r in mine)), "old topics", len(old))
json.dump({a: sorted(c for c in topics if old_region(c) == a) for a in AREAS}, open(OUT / "old-topics-by-area.json", "w"), indent=1)
print("total", len(records), collections.Counter(r["kind"] for r in records))
