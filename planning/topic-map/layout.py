"""Lay out a topic-map graph (regions > districts > topics > steps) as an island.

    python3 planning/topic-map/layout.py graph.json out.json

Angle is region, then district inside it; distance from the centre is
prerequisite depth. A force pass untangles, land is a density field contoured
with marching squares, and every page's courses come from courses/*.yaml.
"""
import collections, itertools, json, math, random, sys
from pathlib import Path

sys.path.insert(0, "/home/user/dewlab")
import build  # noqa

random.seed(11)
graph = json.load(open(sys.argv[1]))
out_path = sys.argv[2]
INV = {r["slug"]: r for r in json.load(open(Path(__file__).parent / "generated" / "inventory.json"))}
BASE = "https://deweydex.github.io/dewlab/"

regions = graph["regions"]
rid = [r["id"] for r in regions]
districts = {d["id"]: d for d in graph["districts"]}
topics = {t["id"]: t for t in graph["topics"]}
codes = list(topics)
needs = {c: [n for n in topics[c].get("needs") or [] if n in topics] for c in codes}
dist_of = {c: topics[c]["district"] for c in codes}
reg_of = {c: districts[dist_of[c]]["region"] for c in codes}

tier = {}
def depth(c):
    if c in tier:
        return tier[c]
    tier[c] = 0 if not needs[c] else 1 + max(depth(n) for n in needs[c])
    return tier[c]
for c in codes:
    depth(c)
children = collections.defaultdict(list)
for c in codes:
    for n in needs[c]:
        children[n].append(c)
def descendants(c, seen=None):
    seen = set() if seen is None else seen
    for k in children[c]:
        if k not in seen:
            seen.add(k)
            descendants(k, seen)
    return seen
weight = {c: len(descendants(c)) for c in codes}

# ---------- region order round the circle
cross = collections.Counter()
for c in codes:
    for n in needs[c]:
        a, b = reg_of[n], reg_of[c]
        if a != b:
            cross[frozenset((a, b))] += 1
for pair in graph.get("neighbours") or []:
    if len(pair) == 2 and pair[0] in rid and pair[1] in rid and pair[0] != pair[1]:
        cross[frozenset(pair)] += 2
# A page that is a step in topics of two regions ties them too, more weakly
# than a need does: it is how the web regions, which need nothing outside
# themselves, still show what they sit beside.
page_regions = collections.defaultdict(set)
for c in codes:
    for s_ in topics[c].get("steps") or []:
        page_regions[s_["tutorial"]].add(reg_of[c])
for lm in graph.get("landmarks") or []:
    for a in lm.get("at") or []:
        if a in reg_of:
            page_regions[lm["tutorial"]].add(reg_of[a])
for rs in page_regions.values():
    for a, b in itertools.combinations(sorted(rs), 2):
        cross[frozenset((a, b))] += 0.5

STRANGERS = 40  # the cost of two unrelated regions sharing a border

def ring_cost(order):
    pos = {r: i for i, r in enumerate(order)}
    n = len(order)
    cost = 0
    for pair, k in cross.items():
        a, b = tuple(pair)
        d = abs(pos[a] - pos[b])
        d = min(d, n - d)
        cost += k * d * d
    for i in range(n):
        if not cross.get(frozenset((order[i], order[(i + 1) % n]))):
            cost += STRANGERS
    return cost

if len(rid) <= 9:
    best = min(([rid[0], *p] for p in itertools.permutations(rid[1:])), key=ring_cost)
else:
    # Too many regions to try every order, and one run of reversals stops at
    # the first dead end. So run it from many starting orders and keep the best.
    def two_opt(seq):
        improved = True
        while improved:
            improved = False
            for i in range(1, len(seq) - 1):
                for j in range(i + 1, len(seq)):
                    cand = seq[:i] + seq[i:j + 1][::-1] + seq[j + 1:]
                    if ring_cost(cand) < ring_cost(seq):
                        seq, improved = cand, True
        return seq
    shuffler = random.Random(3)
    best = two_opt(rid[:])
    for _ in range(400):
        start = rid[:1] + shuffler.sample(rid[1:], len(rid) - 1)
        cand = two_opt(start)
        if ring_cost(cand) < ring_cost(best):
            best = cand
order = best

# ---------- district order inside each region
dcross = collections.Counter()
for c in codes:
    for n in needs[c]:
        a, b = dist_of[n], dist_of[c]
        if a != b:
            dcross[frozenset((a, b))] += 1
d_in = collections.defaultdict(list)
for d in districts.values():
    if any(dist_of[c] == d["id"] for c in codes):
        d_in[d["region"]].append(d["id"])

def district_order(r):
    ds = d_in[r]
    i = order.index(r)
    left, right = order[i - 1], order[(i + 1) % len(order)]
    def pull(d, side):
        return sum(1 for c in codes if dist_of[c] == d for n in needs[c] + children[c] if reg_of[n] == side)
    def cost(seq):
        total = 0
        for a_i, a in enumerate(seq):
            for b_i, b in enumerate(seq):
                if a_i < b_i:
                    total += dcross[frozenset((a, b))] * (b_i - a_i) ** 2
            total += pull(a, left) * a_i * 2 + pull(a, right) * (len(seq) - 1 - a_i) * 2
        return total
    if len(ds) <= 7:
        return list(min(itertools.permutations(ds), key=cost))
    return sorted(ds, key=lambda d: pull(d, left) - pull(d, right), reverse=True)

RING0, RING_STEP, SPACING = 480, 170, 150
def radius(t):
    return RING0 + t * RING_STEP

by_dt = collections.Counter((dist_of[c], tier[c]) for c in codes)
d_need = {}
for d in districts:
    ts = [t for (dd, t) in by_dt if dd == d]
    if ts:
        d_need[d] = max(by_dt[(d, t)] * SPACING / radius(t) for t in ts) + 0.05
dseq = {r: district_order(r) for r in order}
r_need = {r: sum(d_need[d] for d in dseq[r]) + 0.08 for r in order}
total = sum(r_need.values())
sector, dsector = {}, {}
a = -math.pi / 2 - r_need[order[0]] / total * math.pi
for r in order:
    w = r_need[r] / total * 2 * math.pi
    sector[r] = (a, a + w)
    inner = w - 0.08 / total * 2 * math.pi
    b = a + 0.04 / total * 2 * math.pi
    for d in dseq[r]:
        dw = d_need[d] / sum(d_need[x] for x in dseq[r]) * inner
        dsector[d] = (b, b + dw)
        b += dw
    a += w

# ---------- initial placement
ang = {}
for t in range(max(tier.values()) + 1):
    for d, (lo, hi) in dsector.items():
        members = [c for c in codes if dist_of[c] == d and tier[c] == t]
        if not members:
            continue
        def bary(c):
            ps = [p for p in needs[c] if p in ang]
            return sum(ang[p] for p in ps) / len(ps) if ps else (lo + hi) / 2
        members.sort(key=lambda c: (bary(c), topics[c]["name"]))
        pad = (hi - lo) * 0.1
        for i, c in enumerate(members):
            ang[c] = lo + pad + (hi - lo - 2 * pad) * (i + 0.5) / len(members)
pos = {c: [radius(tier[c]) * math.cos(ang[c]), radius(tier[c]) * math.sin(ang[c])] for c in codes}

# ---------- force pass
ITER = 380
for it in range(ITER):
    cool = 1 - it / ITER
    move = {c: [0.0, 0.0] for c in codes}
    for i, a_ in enumerate(codes):
        ax, ay = pos[a_]
        for b_ in codes[i + 1:]:
            bx, by = pos[b_]
            dx, dy = ax - bx, (ay - by) * 1.9
            d2 = dx * dx + dy * dy
            if d2 < SPACING * SPACING:
                dd = math.sqrt(d2) or 0.01
                push = (SPACING - dd) / dd * 0.5
                move[a_][0] += dx * push
                move[a_][1] += dy * push / 1.9
                move[b_][0] -= dx * push
                move[b_][1] -= dy * push / 1.9
    for c in codes:
        x, y = pos[c]
        for p in needs[c]:
            px, py = pos[p]
            k = 0.012 if dist_of[p] == dist_of[c] else 0.004
            move[c][0] += (px - x) * k
            move[c][1] += (py - y) * k
            move[p][0] -= (px - x) * k / 2
            move[p][1] -= (py - y) * k / 2
    for c in codes:
        x, y = pos[c]
        x += move[c][0] * 0.35 * cool
        y += move[c][1] * 0.35 * cool
        rad = math.hypot(x, y)
        rad += (radius(tier[c]) - rad) * 0.18
        th = math.atan2(y, x)
        lo, hi = dsector[dist_of[c]]
        mid = (lo + hi) / 2
        while th - mid > math.pi:
            th -= 2 * math.pi
        while th - mid < -math.pi:
            th += 2 * math.pi
        # districts are soft walls, regions hard ones
        rlo, rhi = sector[reg_of[c]]
        slack = (hi - lo) * 0.25
        th = min(max(th, max(lo - slack, rlo + 0.015)), min(hi + slack, rhi - 0.015))
        pos[c] = [rad * math.cos(th), rad * math.sin(th)]

# ---------- landmarks sit beside the first topic they draw on
lm_pos = []
for lm in graph.get("landmarks") or []:
    at = [a for a in lm.get("at") or [] if a in pos]
    if at:
        cx = sum(pos[a][0] for a in at) / len(at)
        cy = sum(pos[a][1] for a in at) / len(at)
    else:
        cx, cy = 0.0, 0.0
    ang0 = math.atan2(cy, cx) + random.uniform(-0.3, 0.3)
    for _ in range(40):
        near = min(math.hypot(cx - p[0], cy - p[1]) for p in list(pos.values()) + [q[1] for q in lm_pos])
        if near > 90:
            break
        cx += 22 * math.cos(ang0)
        cy += 22 * math.sin(ang0)
    lm_pos.append((lm, (cx, cy)))

# ---------- land
pts_all = list(pos.values()) + [p for _, p in lm_pos]
PAD = 260
minx, maxx = min(p[0] for p in pts_all) - PAD, max(p[0] for p in pts_all) + PAD
miny, maxy = min(p[1] for p in pts_all) - PAD, max(p[1] for p in pts_all) + PAD
STEP = 20
nx = int((maxx - minx) / STEP) + 2
ny = int((maxy - miny) / STEP) + 2
SIG = 95.0
dens = {r: [[0.0] * nx for _ in range(ny)] for r in order}
anchors = [(pos[c][0], pos[c][1], reg_of[c], 1.0) for c in codes]
for lm, (x, y) in lm_pos:
    at = [a for a in lm.get("at") or [] if a in reg_of]
    if at:
        anchors.append((x, y, reg_of[at[0]], 0.8))
for r in order:
    lo, hi = sector[r]
    mid = (lo + hi) / 2
    for k in range(3):
        rad = 130 + k * 140
        anchors.append((rad * math.cos(mid), rad * math.sin(mid), r, 0.9))
for c in codes:
    for p in needs[c]:
        (x1, y1), (x2, y2) = pos[p], pos[c]
        if reg_of[p] == reg_of[c]:
            for f in (0.33, 0.66):
                anchors.append((x1 + (x2 - x1) * f, y1 + (y2 - y1) * f, reg_of[c], 0.55))
        elif math.hypot(x2 - x1, y2 - y1) < 520:
            for f in (0.2, 0.4):
                anchors.append((x1 + (x2 - x1) * f, y1 + (y2 - y1) * f, reg_of[p], 0.6))
            for f in (0.6, 0.8):
                anchors.append((x1 + (x2 - x1) * f, y1 + (y2 - y1) * f, reg_of[c], 0.6))
reach = int(3 * SIG / STEP)
for ax, ay, r, w in anchors:
    gi, gj = int((ax - minx) / STEP), int((ay - miny) / STEP)
    grid = dens[r]
    for j in range(max(0, gj - reach), min(ny, gj + reach + 1)):
        yy = miny + j * STEP - ay
        row = grid[j]
        for i in range(max(0, gi - reach), min(nx, gi + reach + 1)):
            xx = minx + i * STEP - ax
            row[i] += w * math.exp(-(xx * xx + yy * yy) / (2 * SIG * SIG))
THRESH = 0.32

def field_for(r):
    others = [dens[s] for s in order if s != r]
    mine = dens[r]
    out = [[0.0] * nx for _ in range(ny)]
    for j in range(ny):
        for i in range(nx):
            m = mine[j][i]
            best_other = max(o[j][i] for o in others)
            tot = m + sum(o[j][i] for o in others)
            out[j][i] = min(tot - THRESH, m - best_other)
    return out

def total_field():
    return [[sum(dens[s][j][i] for s in order) - THRESH for i in range(nx)] for j in range(ny)]

TABLE = {1: [(3, 0)], 2: [(0, 1)], 3: [(3, 1)], 4: [(1, 2)], 5: [(3, 0), (1, 2)], 6: [(0, 2)], 7: [(3, 2)],
         8: [(2, 3)], 9: [(2, 0)], 10: [(0, 1), (2, 3)], 11: [(2, 1)], 12: [(1, 3)], 13: [(1, 0)], 14: [(0, 3)]}

def marching(field):
    segs = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            v = (field[j][i], field[j][i + 1], field[j + 1][i + 1], field[j + 1][i])
            idx = (v[0] > 0) | (v[1] > 0) << 1 | (v[2] > 0) << 2 | (v[3] > 0) << 3
            if idx in (0, 15):
                continue
            p = ((minx + i * STEP, miny + j * STEP), (minx + (i + 1) * STEP, miny + j * STEP),
                 (minx + (i + 1) * STEP, miny + (j + 1) * STEP), (minx + i * STEP, miny + (j + 1) * STEP))
            def edge(e):
                a_, b_ = e, (e + 1) % 4
                t = v[a_] / (v[a_] - v[b_]) if v[a_] != v[b_] else 0.5
                return (p[a_][0] + (p[b_][0] - p[a_][0]) * t, p[a_][1] + (p[b_][1] - p[a_][1]) * t)
            for a_, b_ in TABLE[idx]:
                segs.append((edge(a_), edge(b_)))
    return segs

def chain(segs):
    key = lambda q: (round(q[0], 2), round(q[1], 2))
    nxt = {}
    for a_, b_ in segs:
        nxt.setdefault(key(a_), []).append(b_)
    used, loops = set(), []
    for a_, b_ in segs:
        if (key(a_), key(b_)) in used:
            continue
        line = [a_, b_]
        used.add((key(a_), key(b_)))
        cur = b_
        while True:
            cands = [q for q in nxt.get(key(cur), []) if (key(cur), key(q)) not in used]
            if not cands:
                break
            q = cands[0]
            used.add((key(cur), key(q)))
            line.append(q)
            cur = q
            if key(cur) == key(line[0]):
                break
        if len(line) > 6:
            loops.append(line)
    return loops

def chaikin(pts, rounds=2):
    for _ in range(rounds):
        out = []
        for k in range(len(pts) - 1):
            (x1, y1), (x2, y2) = pts[k], pts[k + 1]
            out += [(0.75 * x1 + 0.25 * x2, 0.75 * y1 + 0.25 * y2), (0.25 * x1 + 0.75 * x2, 0.25 * y1 + 0.75 * y2)]
        out.append(out[0])
        pts = out
    return pts

def to_path(loops):
    return "".join("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in chaikin(lp[::2] + [lp[0]])) + "Z" for lp in loops)

fields = {r: field_for(r) for r in order}
land = {r: to_path(chain(marching(fields[r]))) for r in order}
coast = to_path(chain(marching(total_field())))

def clear_spot(members, inside, cx, cy, hard=90):
    best_l = None
    for j in range(0, ny, 2):
        for i in range(0, nx, 2):
            if not inside(j, i):
                continue
            x, y = minx + i * STEP, miny + j * STEP
            clear = min(math.hypot((x - q[0]) * 0.45, (y - q[1])) for q in pos.values())
            score = min(clear, hard) - 0.12 * math.hypot(x - cx, y - cy)
            if best_l is None or score > best_l[0]:
                best_l = (score, x, y)
    return [round(best_l[1]), round(best_l[2])] if best_l else [round(cx), round(cy)]

# Region names are wide and letter-spaced; at the whole-map zoom one letter
# is about 55 map units, so two small neighbouring regions can print one name
# over the other. Each name keeps clear of the names already placed.
region_label = {}
placed_labels = []
def clear_of_labels(x, y, name):
    half = len(name) * 55 / 2
    return all(abs(x - px) > half + ph or abs(y - py) > 130 for px, py, ph in placed_labels)
for r in sorted(order, key=lambda r: -sum(1 for c in codes if reg_of[c] == r)):
    mem = [pos[c] for c in codes if reg_of[c] == r]
    cx, cy = sum(p[0] for p in mem) / len(mem), sum(p[1] for p in mem) / len(mem)
    name = next(x["name"] for x in regions if x["id"] == r)
    region_label[r] = clear_spot(mem, lambda j, i, f=fields[r], n=name: f[j][i] > 0.08 and clear_of_labels(minx + i * STEP, miny + j * STEP, n), cx, cy)
    placed_labels.append((region_label[r][0], region_label[r][1], len(name) * 55 / 2))
district_label = {}
for d in dsector:
    mem = [pos[c] for c in codes if dist_of[c] == d]
    cx, cy = sum(p[0] for p in mem) / len(mem), sum(p[1] for p in mem) / len(mem)
    district_label[d] = [round(cx), round(cy - 34)]

# ---------- pages, courses
pages = {t.slug: t for t in build.load_all() if not build.VERSION_FILE_RE.match(t.path.stem)}
courses_of = collections.defaultdict(list)
course_routes = []
teaches_in = collections.defaultdict(list)
for c in codes:
    for s in topics[c].get("steps") or []:
        if s.get("role") == "teaches":
            teaches_in[s["tutorial"]].append(c)
for cid, course in build.courses().items():
    seq, count = [], 0
    for s in course.contents:
        for i in s.ids:
            count += 1
            if course.title not in courses_of[i]:
                courses_of[i].append(course.title)
            for c in teaches_in.get(i, []):
                if c not in seq:
                    seq.append(c)
    course_routes.append({"id": cid, "title": course.title, "path": seq, "tutorials": count})

def heading_text(slug, anchor):
    for h in INV.get(slug, {}).get("headings", []):
        if h["anchor"] == anchor:
            return h["text"]
    return None

def step_out(s):
    slug = s["tutorial"]
    title = INV[slug]["title"] if slug in INV else slug
    sec = s.get("section")
    return {"slug": slug, "title": title, "section": heading_text(slug, sec) if sec else None,
            "href": f"{BASE}tutorials/{slug}.html" + (f"#{sec}" if sec else ""),
            "role": s.get("role"), "courses": courses_of.get(slug, [])}

data = {
    "regions": [{"id": r, "name": next(x["name"] for x in regions if x["id"] == r),
                 "blurb": next(x.get("blurb", "") for x in regions if x["id"] == r),
                 "lore": next(x.get("lore", "") for x in regions if x["id"] == r),
                 "label": region_label[r], "land": land[r],
                 "count": sum(1 for c in codes if reg_of[c] == r)} for r in order],
    "districts": [{"id": d, "name": districts[d]["name"], "blurb": districts[d].get("blurb", ""),
                   "region": districts[d]["region"], "label": district_label[d],
                   "count": sum(1 for c in codes if dist_of[c] == d)} for d in dsector],
    "coast": coast,
    "rings": [radius(t) for t in range(max(tier.values()) + 1)],
    "bounds": [round(minx), round(miny), round(maxx - minx), round(maxy - miny)],
    "towns": [{
        "code": c, "name": topics[c]["name"], "plain": topics[c].get("plain", ""),
        "district": dist_of[c], "region": reg_of[c], "needs": needs[c], "tier": tier[c],
        "x": round(pos[c][0]), "y": round(pos[c][1]), "weight": weight[c],
        "state": "taught" if any(s.get("role") == "teaches" for s in topics[c].get("steps") or []) else "planned",
        "steps": [step_out(s) for s in topics[c].get("steps") or [] if s.get("tutorial") in INV],
        "agreement": topics[c].get("agreement", ""),
    } for c in codes],
    "landmarks": [{"slug": lm["tutorial"], "title": INV.get(lm["tutorial"], {}).get("title", lm["tutorial"]),
                   "kind": lm.get("kind"), "at": [a for a in lm.get("at") or [] if a in topics],
                   "href": f"{BASE}tutorials/{lm['tutorial']}.html",
                   "x": round(p[0]), "y": round(p[1])} for lm, p in lm_pos],
    "courses": course_routes,
    "questions": graph.get("questions") or [],
}
json.dump(data, open(out_path, "w"), separators=(",", ":"))
print("regions", order, "ring cost", ring_cost(order), file=sys.stderr)
print("towns", len(codes), "districts", len(dsector), "landmarks", len(lm_pos), "depth", max(tier.values()), file=sys.stderr)
print({c["title"]: len(c["path"]) for c in course_routes}, file=sys.stderr)
