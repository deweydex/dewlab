"""Lay out the topic map (continents > regions > districts > topics) and write
where everything goes.

    python3 dev/map_layout.py [map/graph.json [map/layout.json]]

Run it when the map's shape changes (a topic, a district, a need, a continent)
and commit the result. The build never runs it: positions are data, so a
learner who has found a town finds it in the same place tomorrow, and the build
only refuses when the committed layout and the graph disagree.

The map is drawn from the outside in. First the continents are placed round
the starting island, a sea apart, with continents that share many roads side
by side. Then each continent's countries get a home on it, and each country's
districts a home in it, turned to face the countries and continents they have
roads to. Only then do the towns settle, under forces. Land is a density field
contoured with marching squares, a bridge crosses the sea wherever roads
between two continents need one, and the page chooses where to put each name.
The output is geometry only. Titles, sections and courses come from the
tutorials themselves, at build time, so a link cannot go stale.
"""
import collections
import itertools
import json
import math
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
random.seed(11)
graph = json.load(open(sys.argv[1] if len(sys.argv) > 1 else REPO / "map" / "graph.json"))
out_path = sys.argv[2] if len(sys.argv) > 2 else REPO / "map" / "layout.json"

regions = graph["regions"]
rid = [r["id"] for r in regions]
region_rec = {r["id"]: r for r in regions}
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

# ---------- continents, and who lives where
conts = graph.get("continents") or [{"id": "comath", "regions": rid}]
if not any(c.get("kind") == "start" for c in conts):
    conts = [{"id": "start", "kind": "start", "regions": []}] + conts
cont_rec = {c["id"]: c for c in conts}
START = next(c["id"] for c in conts if c.get("kind") == "start")
cont_of = {r: c["id"] for c in conts for r in c["regions"]}
# A town that needs nothing first stands on the Prerequisite Plains, round
# the tower on the starting island, whatever its country. The starting
# island's own countries keep their towns.
plains = {c for c in codes if tier[c] == 0 and cont_of[reg_of[c]] != START}
land_of = {c: START if c in plains else cont_of[reg_of[c]] for c in codes}
unit_of = {c: "@plains" if c in plains else reg_of[c] for c in codes}
def land_of_unit(u):
    return START if u == "@plains" else cont_of[u]
lands = [c["id"] for c in conts]
outer = [cid for cid in lands if cid != START]
members = {cid: [c for c in codes if land_of[c] == cid] for cid in lands}
regions_on = {cid: [r for r in cont_rec[cid]["regions"] if any(unit_of[c] == r for c in codes)] for cid in lands}
dlist = [d for d in districts if any(dist_of[c] == d and c not in plains for c in codes)]
d_in = {r: [d for d in dlist if districts[d]["region"] == r] for r in rid}
islands = {cid for cid in lands if cont_rec[cid].get("kind") == "islands"}

# How strongly two places are tied: a need between them counts 1, a page
# they share a half, and a pair the integrator named as neighbours 1. The
# same ties, one level down, hold between districts.
def tally(key):
    t = collections.Counter()
    def add(a, b, w):
        if a != b:
            t[frozenset((a, b))] += w
    for c in codes:
        for n in needs[c]:
            add(key(c), key(n), 1)
    shared = collections.defaultdict(set)
    for c in codes:
        for s_ in topics[c].get("steps") or []:
            shared[s_["tutorial"]].add(key(c))
    for lm in graph.get("landmarks") or []:
        for a in lm.get("at") or []:
            if a in topics:
                shared[lm["tutorial"]].add(key(a))
    for ks in shared.values():
        for a, b in itertools.combinations(sorted(ks), 2):
            add(a, b, 0.5)
    return t
tie = tally(lambda c: unit_of[c])
for pair in graph.get("neighbours") or []:
    if len(pair) == 2 and pair[0] in rid and pair[1] in rid and pair[0] != pair[1]:
        tie[frozenset(pair)] += 1
dtie = tally(lambda c: "@plains" if c in plains else dist_of[c])
land_tie = collections.Counter()
for pair, w in tie.items():
    a, b = tuple(pair)
    if land_of_unit(a) != land_of_unit(b):
        land_tie[frozenset((land_of_unit(a), land_of_unit(b)))] += w

# ---------- the shape: continents first
TOWN = 108      # about the room one town needs, as the radius of a circle
SEA = 330       # the narrowest sea between two continents
PLAINS_R = 400  # the ring of plains towns round the tower
size_of = {cid: len(members[cid]) for cid in lands}
R_land = {cid: TOWN * math.sqrt(size_of[cid]) for cid in lands}
R_land[START] = max(R_land[START], PLAINS_R + 150)

def arrange(items, centre, rho, size, ties, ext, circle=False):
    """Give each item a home on a circle round centre, in sectors sized by
    size(item), in the order and turn that keep tied items close and face
    each item towards what lies outside (ext)."""
    if len(items) == 1 and not circle:
        return {items[0]: centre}
    tot = sum(size(i) for i in items)
    best = None
    for perm in itertools.permutations(items[1:]):
        seq = (items[0],) + perm
        for k in range(36):
            a = 2 * math.pi * k / 36
            homes = {}
            for it in seq:
                w = 2 * math.pi * size(it) / tot
                homes[it] = (centre[0] + rho(it) * math.cos(a + w / 2), centre[1] + rho(it) * math.sin(a + w / 2))
                a += w
            cost = sum(ties[frozenset((x, y))] * math.dist(homes[x], homes[y]) for x, y in itertools.combinations(seq, 2))
            cost += sum(ext(it, homes[it]) for it in seq)
            if best is None or cost < best[0]:
                best = (cost, homes)
    return best[1]

anchor = {START: (0.0, 0.0)}
anchor.update(arrange(outer, (0.0, 0.0), lambda cid: R_land[START] + SEA + R_land[cid], lambda cid: R_land[cid],
                      land_tie, lambda cid, h: 0))
# Then the continents draw together. A continent is a disc of its size: tied
# continents pull towards each other, all of them drift towards the island,
# and no two discs come closer than a sea.
P = {cid: list(anchor[cid]) for cid in outer}
for it in range(900):
    for cid in outer:
        fx, fy = -P[cid][0] * 0.01, -P[cid][1] * 0.01
        for m in outer:
            if m != cid:
                w = land_tie[frozenset((cid, m))]
                fx += (P[m][0] - P[cid][0]) * 0.0015 * w
                fy += (P[m][1] - P[cid][1]) * 0.0015 * w
        P[cid][0] += fx
        P[cid][1] += fy
    for _ in range(3):
        for a_, b_ in itertools.combinations(lands, 2):
            pa = P.get(a_, [0.0, 0.0])
            pb = P.get(b_, [0.0, 0.0])
            dx, dy = pb[0] - pa[0], pb[1] - pa[1]
            d = math.hypot(dx, dy) or 0.01
            need = R_land[a_] + R_land[b_] + SEA
            if d < need:
                push = (need - d) / d
                if a_ == START:
                    pb[0] += dx * push
                    pb[1] += dy * push
                elif b_ == START:
                    pa[0] -= dx * push
                    pa[1] -= dy * push
                else:
                    pa[0] -= dx * push / 2
                    pa[1] -= dy * push / 2
                    pb[0] += dx * push / 2
                    pb[1] += dy * push / 2
# Turn the whole map so that it is wider than it is tall, as a screen is.
def extent(turn):
    xs, ys = [], []
    for cid in lands:
        x, y = P.get(cid, [0.0, 0.0])
        c_, s_ = math.cos(turn), math.sin(turn)
        x, y = x * c_ - y * s_, x * s_ + y * c_
        xs += [x - R_land[cid], x + R_land[cid]]
        ys += [y - R_land[cid], y + R_land[cid]]
    return max(xs) - min(xs), max(ys) - min(ys)
turn = min((k * math.pi / 36 for k in range(72)), key=lambda t: abs(extent(t)[0] / extent(t)[1] - 1.5))
for cid in outer:
    x, y = P[cid]
    anchor[cid] = (x * math.cos(turn) - y * math.sin(turn), x * math.sin(turn) + y * math.cos(turn))

# ---------- then countries on each continent, and districts in each country
n_unit = collections.Counter(unit_of[c] for c in codes)
def pull_out(ties_to, here, homes_of):
    return sum(w * math.dist(here, homes_of(u)) for u, w in ties_to.items())
home = {}
for cid in lands:
    rs = regions_on[cid]
    if not rs:
        continue
    def ext(r, h, cid=cid):
        out = collections.Counter()
        for pair, w in tie.items():
            if r in pair:
                (u,) = pair - {r} or {r}
                if land_of_unit(u) != cid:
                    out[land_of_unit(u)] += w
        return sum(w * math.dist(h, anchor[m]) for m, w in out.items())
    if cid == START:
        home.update(arrange(rs, anchor[cid], lambda r: PLAINS_R * 0.62, lambda r: n_unit[r], tie, ext, circle=True))
    else:
        home.update(arrange(rs, anchor[cid], lambda r, cid=cid: 0.5 * R_land[cid] if len(rs) > 1 else 0, lambda r: n_unit[r], tie, ext))
# a plains town faces its own country, across the sea
def unit_home(u):
    return (0.0, 0.0) if u == "@plains" else home[u]
dhome = {}
n_dist = collections.Counter(dist_of[c] for c in codes if c not in plains)
for r in rid:
    ds = d_in[r]
    if not ds:
        continue
    R_r = TOWN * math.sqrt(n_unit[r])
    spread = 0.95 if cont_of[r] in islands else 0.45
    def dext(d, h, r=r):
        s = 0.0
        for pair, w in dtie.items():
            if d in pair:
                (u,) = pair - {d} or {d}
                if u == "@plains":
                    s += w * math.dist(h, (0.0, 0.0))
                elif districts[u]["region"] != r:
                    s += w * math.dist(h, home[districts[u]["region"]])
        return s
    dhome.update(arrange(ds, home[r], lambda d, R_r=R_r, spread=spread: spread * R_r if len(ds) > 1 else 0,
                         lambda d: n_dist[d], dtie, dext))

# ---------- initial placement: every town starts in its district, shallow
# towns on the side facing the tower
pos = {}
for d in dlist:
    ms = sorted((c for c in codes if dist_of[c] == d and c not in plains), key=lambda c: (tier[c], topics[c]["name"]))
    hx, hy = dhome[d]
    rr = math.hypot(hx, hy) or 1.0
    ux, uy = hx / rr, hy / rr
    R_d = TOWN * math.sqrt(len(ms))
    lo, hi = tier[ms[0]], tier[ms[-1]]
    for i, c in enumerate(ms):
        f = (tier[c] - lo) / (hi - lo) - 0.5 if hi > lo else 0.0
        side = (i % 3 - 1) * 0.5 + random.uniform(-0.2, 0.2)
        pos[c] = [hx + ux * f * R_d + -uy * side * R_d, hy + uy * f * R_d + ux * side * R_d]
for c in sorted(plains):
    hx, hy = home[reg_of[c]]
    rr = math.hypot(hx, hy) or 1.0
    a = math.atan2(hy, hx) + random.uniform(-0.25, 0.25)
    pos[c] = [PLAINS_R * math.cos(a), PLAINS_R * math.sin(a)]

tier_span = {}
for cid in lands:
    ts = [tier[c] for c in members[cid] if c not in plains]
    if ts:
        tier_span[cid] = (min(ts), max(ts))

# ---------- settling: the map finds a low-energy state
# Every town pushes every other away: harder across a county or country
# border, and hardest across the sea, which keeps continents apart. A
# prerequisite pulls like a spring, weakly when it crosses the sea. Each town
# is drawn to the middle of its county and, more weakly, of its country; each
# country is held at its home; and depth is a gentle pull away from the tower.
R_SEA = 560
edges = [(p_, c) for c in codes for p_ in needs[c]]
ITER = 700
for it in range(ITER):
    temp = 1 - it / ITER
    fx = {c: 0.0 for c in codes}
    fy = {c: 0.0 for c in codes}
    for i, a_ in enumerate(codes):
        ax, ay = pos[a_]
        da, ra, la, pa = dist_of[a_], reg_of[a_], land_of[a_], a_ in plains
        for b_ in codes[i + 1:]:
            bx, by = pos[b_]
            dx, dy = ax - bx, (ay - by) * 1.6  # labels are wide, so vertical neighbours count as closer
            if land_of[b_] != la:
                R = R_SEA
            elif pa and b_ in plains:
                R = 175  # the plains are shared ground, with no borders
            elif pa or b_ in plains:
                R = 240
            elif dist_of[b_] == da:
                R = 190
            elif reg_of[b_] == ra:
                R = 420 if la in islands else 240
            else:
                R = 330
            d2 = dx * dx + dy * dy
            if d2 < R * R:
                d = math.sqrt(d2) or 0.01
                f = (R - d) / d * 0.5
                fx[a_] += dx * f
                fy[a_] += dy * f / 1.6
                fx[b_] -= dx * f
                fy[b_] -= dy * f / 1.6
    for p_, c in edges:
        (x1, y1), (x2, y2) = pos[p_], pos[c]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy) or 0.01
        if land_of[p_] != land_of[c]:
            L, k = R_SEA + 160, 0.002
        elif p_ in plains or c in plains:
            L, k = 300, 0.01  # a road out of the plains is long and pulls gently
        else:
            same_d, same_r = dist_of[p_] == dist_of[c], reg_of[p_] == reg_of[c]
            L = 150 if same_d else 230 if same_r else 380
            k = 0.04 if same_r else 0.008
        f = (d - L) * k / d
        fx[c] -= dx * f
        fy[c] -= dy * f
        fx[p_] += dx * f
        fy[p_] += dy * f
    cen_d, cen_r = {}, {}
    for d_ in dlist:
        m = [pos[c] for c in codes if dist_of[c] == d_ and c not in plains]
        cen_d[d_] = (sum(q[0] for q in m) / len(m), sum(q[1] for q in m) / len(m))
    for r in home:
        m = [pos[c] for c in codes if unit_of[c] == r]
        cen_r[r] = (sum(q[0] for q in m) / len(m), sum(q[1] for q in m) / len(m))
    for c in codes:
        x, y = pos[c]
        if c in plains:
            # on the plains: keep to the ring round the tower, on the side
            # facing its own country
            hx, hy = home[reg_of[c]]
            hr = math.hypot(hx, hy) or 1.0
            fx[c] += (hx / hr * PLAINS_R - x) * 0.015
            fy[c] += (hy / hr * PLAINS_R - y) * 0.015
            rad = math.hypot(x, y) or 0.01
            pull = (PLAINS_R - rad) * 0.05
            if rad < 220:
                pull += (220 - rad) * 0.3
            fx[c] += x / rad * pull
            fy[c] += y / rad * pull
            continue
        cx, cy = cen_d[dist_of[c]]
        fx[c] += (cx - x) * 0.03
        fy[c] += (cy - y) * 0.03
        rx, ry = cen_r[reg_of[c]]
        fx[c] += (rx - x) * 0.008
        fy[c] += (ry - y) * 0.008
        hx, hy = home[reg_of[c]]
        fx[c] += (hx - rx) * 0.03
        fy[c] += (hy - ry) * 0.03
        cid = land_of[c]
        if cid != START and cid in tier_span:
            lo, hi = tier_span[cid]
            ax_, ay_ = anchor[cid]
            f = (tier[c] - lo) / (hi - lo) - 0.5 if hi > lo else 0.0
            target = math.hypot(ax_, ay_) + f * R_land[cid]
            rad = math.hypot(x, y) or 0.01
            pull = (target - rad) * 0.006
            fx[c] += x / rad * pull
            fy[c] += y / rad * pull
        if cid == START:
            rad = math.hypot(x, y) or 0.01
            if rad < 220:  # the tower keeps its own ground
                fx[c] += x / rad * (220 - rad) * 0.3
                fy[c] += y / rad * (220 - rad) * 0.3
    cap = 4 + 36 * temp
    for c in codes:
        mx, my = fx[c] * 0.35, fy[c] * 0.35
        m = math.hypot(mx, my)
        if m > cap:
            mx, my = mx / m * cap, my / m * cap
        pos[c] = [pos[c][0] + mx, pos[c][1] + my]

land_centre = {}
for cid in lands:
    ms = [pos[c] for c in members[cid]] or [[0.0, 0.0]]
    land_centre[cid] = (sum(q[0] for q in ms) / len(ms), sum(q[1] for q in ms) / len(ms))

# ---------- landmarks sit beside the towns they draw on, on the continent
# where most of those towns are
lm_pos = []
for lm in graph.get("landmarks") or []:
    at = [a for a in lm.get("at") or [] if a in pos]
    if lm.get("tower") or not at:
        lm_pos.append((lm, (0.0, 0.0), START))
        continue
    home_land = collections.Counter(land_of[a] for a in at).most_common(1)[0][0]
    near_at = [a for a in at if land_of[a] == home_land]
    cx = sum(pos[a][0] for a in near_at) / len(near_at)
    cy = sum(pos[a][1] for a in near_at) / len(near_at)
    lx, ly = land_centre[home_land]
    ang0 = math.atan2(cy - ly, cx - lx) + random.uniform(-0.3, 0.3)
    for _ in range(40):
        near = min(math.hypot(cx - p[0], cy - p[1]) for p in list(pos.values()) + [q[1] for q in lm_pos if q[2] != START])
        if near > 90:
            break
        cx += 22 * math.cos(ang0)
        cy += 22 * math.sin(ang0)
    lm_pos.append((lm, (cx, cy), home_land))

# ---------- land
order = [r for cid in lands for r in regions_on[cid]]
pts_all = list(pos.values()) + [p for _, p, _ in lm_pos]
PAD = 380  # sea round the outer coasts, with room for the continent names
minx, maxx = min(p[0] for p in pts_all) - PAD, max(p[0] for p in pts_all) + PAD
miny, maxy = min(p[1] for p in pts_all) - PAD, max(p[1] for p in pts_all) + PAD
STEP = 20
nx = int((maxx - minx) / STEP) + 2
ny = int((maxy - miny) / STEP) + 2
SIG = 95.0
keys = order + ["plains"]
dens = {r: [[0.0] * nx for _ in range(ny)] for r in keys}
anchors = [(pos[c][0], pos[c][1], "plains" if c in plains else reg_of[c], 1.0) for c in codes]
anchors.append((0.0, 0.0, "plains", 1.3))
for k in range(10):
    a_ = 2 * math.pi * k / 10
    anchors.append((190 * math.cos(a_), 190 * math.sin(a_), "plains", 1.0))
for lm, (x, y), cid in lm_pos:
    at = [a for a in lm.get("at") or [] if a in reg_of and land_of[a] == cid]
    if at and not lm.get("tower"):
        anchors.append((x, y, "plains" if at[0] in plains else reg_of[at[0]], 0.8))
for c in codes:
    for p in needs[c]:
        (x1, y1), (x2, y2) = pos[p], pos[c]
        if p in plains or c in plains or land_of[p] != land_of[c]:
            continue
        if reg_of[p] == reg_of[c]:
            if land_of[c] in islands and dist_of[p] != dist_of[c]:
                continue  # the sea between two islands stays open
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
total = [[sum(dens[s][j][i] for s in keys) for i in range(nx)] for j in range(ny)]

def field_for(r):
    others = [dens[s] for s in keys if s != r]
    mine = dens[r]
    out = [[0.0] * nx for _ in range(ny)]
    for j in range(ny):
        for i in range(nx):
            m = mine[j][i]
            if m < 1e-3:
                out[j][i] = -1.0
                continue
            best_other = max(o[j][i] for o in others)
            out[j][i] = min(total[j][i] - THRESH, m - best_other)
    return out

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
    def key(q):
        return (round(q[0], 2), round(q[1], 2))
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

def to_path(loops):
    """The outlines as paths, every other point of each loop. They are left
    angular here and smoothed by the page (assets/map.js, smooth()), which is a
    quarter the size to ship."""
    return "".join("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in lp[::2] + [lp[0]]) + "Z" for lp in loops)

fields = {r: field_for(r) for r in order}
land = {r: to_path(chain(marching(fields[r]))) for r in order}

# A county is the part of its country nearest its own towns. Its density
# comes from its towns and the needs between them; it wins a patch of the
# country where it beats every other county of that country.
ddens = {d: [[0.0] * nx for _ in range(ny)] for d in dlist}
d_anchors = [(pos[c][0], pos[c][1], dist_of[c], 1.0) for c in codes if c not in plains]
for c in codes:
    for p_ in needs[c]:
        if dist_of[p_] == dist_of[c] and p_ not in plains and c not in plains:
            (x1, y1), (x2, y2) = pos[p_], pos[c]
            d_anchors.append(((x1 + x2) / 2, (y1 + y2) / 2, dist_of[c], 0.6))
for ax, ay, d_, w in d_anchors:
    gi, gj = int((ax - minx) / STEP), int((ay - miny) / STEP)
    grid = ddens[d_]
    for j in range(max(0, gj - reach), min(ny, gj + reach + 1)):
        yy = miny + j * STEP - ay
        row = grid[j]
        for i in range(max(0, gi - reach), min(nx, gi + reach + 1)):
            xx = minx + i * STEP - ax
            row[i] += w * math.exp(-(xx * xx + yy * yy) / (2 * SIG * SIG))
county = {}
for r in order:
    ds = d_in[r]
    rf = fields[r]
    for d_ in ds:
        others = [ddens[o] for o in ds if o != d_]
        mine = ddens[d_]
        f = [[0.0] * nx for _ in range(ny)]
        for j in range(ny):
            rrow, mrow = rf[j], mine[j]
            orows = [o[j] for o in others]
            for i in range(nx):
                if rrow[i] <= 0:
                    f[j][i] = rrow[i]
                    continue
                best = max((o[i] for o in orows), default=-1.0)
                f[j][i] = min(rrow[i], mrow[i] - best)
        county[d_] = to_path(chain(marching(f)))
coast = to_path(chain(marching([[v - THRESH for v in row] for row in total])))
plains_field = field_for("plains")
plains_land = to_path(chain(marching(plains_field)))

# ---------- which continent owns each patch of land, and where the sea is
land_key = {r: cont_of[r] for r in order}
land_key["plains"] = START
owner = [[None] * nx for _ in range(ny)]
for j in range(ny):
    for i in range(nx):
        if total[j][i] > THRESH:
            by = collections.Counter()
            for s in keys:
                by[land_key[s]] += dens[s][j][i]
            owner[j][i] = by.most_common(1)[0][0]
def cell_xy(j, i):
    return (minx + i * STEP, miny + j * STEP)
def owner_at(x, y):
    i, j = int(round((x - minx) / STEP)), int(round((y - miny) / STEP))
    return owner[j][i] if 0 <= j < ny and 0 <= i < nx else None
shore = collections.defaultdict(list)
for j in range(1, ny - 1):
    for i in range(1, nx - 1):
        o = owner[j][i]
        if o and (owner[j - 1][i] is None or owner[j + 1][i] is None or owner[j][i - 1] is None or owner[j][i + 1] is None):
            shore[o].append(cell_xy(j, i))

# ---------- bridges: one wherever roads between two continents cross the
# sea, at the place that keeps those roads shortest
crossing = collections.defaultdict(list)
for c in codes:
    for n in needs[c]:
        if land_of[n] != land_of[c]:
            crossing[tuple(sorted((land_of[n], land_of[c])))].append((n, c))
MAX_BRIDGE = 900
bridges = []
for (A, B), pairs in sorted(crossing.items()):
    a_side = [pos[n] if land_of[n] == A else pos[c] for n, c in pairs]
    b_side = [pos[c] if land_of[c] == B else pos[n] for n, c in pairs]
    def mean_to(p, towns):
        return sum(math.dist(p, t) for t in towns) / len(towns)
    ca = sorted(((mean_to(p, a_side), p) for p in shore[A]))[:160]
    cb = sorted(((mean_to(p, b_side), p) for p in shore[B]))[:160]
    cands = sorted((sa + sb + 0.8 * math.dist(pa, pb), pa, pb) for sa, pa in ca for sb, pb in cb
                   if math.dist(pa, pb) <= MAX_BRIDGE)
    for _, pa, pb in cands:
        length = math.dist(pa, pb)
        steps = max(2, int(length / 12))
        clear = True
        for s_ in range(steps + 1):
            t = s_ / steps
            if t * length < 30 or (1 - t) * length < 30:
                continue
            if owner_at(pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t) is not None:
                clear = False
                break
        if clear:
            ux, uy = (pb[0] - pa[0]) / length, (pb[1] - pa[1]) / length
            bridges.append({"a": A, "b": B, "count": len(pairs),
                            "ends": [[round(pa[0] - ux * 24), round(pa[1] - uy * 24)],
                                     [round(pb[0] + ux * 24), round(pb[1] + uy * 24)]]})
            break
    else:
        print(f"no bridge between {A} and {B}; its {len(pairs)} roads go by way of {START}", file=sys.stderr)

# ---------- waves, far out in the open sea
waves = []
wave_rng = random.Random(5)
open_sea = [cell_xy(j, i) for j in range(8, ny - 8, 3) for i in range(8, nx - 8, 3) if total[j][i] < 0.004]
wave_rng.shuffle(open_sea)
for p in open_sea:
    if all(math.dist(p, q) > 420 for q in waves):
        waves.append(p)
    if len(waves) >= 36:
        break

# ---------- labels
# Region names are wide and letter-spaced, and how wide one is on screen
# depends on the screen. So each country ships a few places that are well
# inside its land and clear of its towns, best first, and the page takes the
# one where its name covers the fewest towns.
def spots_for(field, members, taken):
    found = []
    for j in range(0, ny, 2):
        for i in range(0, nx, 2):
            if field[j][i] <= 0.15:
                continue
            x, y = minx + i * STEP, miny + j * STEP
            clear = min(math.hypot((x - q[0]) * 0.45, (y - q[1])) for q in pos.values())
            found.append((clear, x, y))
    found.sort(reverse=True)
    out = []
    for clear, x, y in found:
        if all(math.hypot(x - ox, y - oy) > 110 for ox, oy in out) and all(math.hypot(x - ox, y - oy) > 60 for ox, oy in taken):
            out.append((x, y))
        if len(out) == 24:
            break
    return [[round(x), round(y)] for x, y in out]

region_spots = {}
for r in order:
    region_spots[r] = spots_for(fields[r], [c for c in codes if unit_of[c] == r], [(0.0, 0.0)])
plains_spots = spots_for(plains_field, [c for c in plains], [(0.0, 0.0), (0.0, 40.0)])
district_label = {}
for d in dlist:
    mem = [pos[c] for c in codes if dist_of[c] == d and c not in plains]
    cx, cy = sum(p[0] for p in mem) / len(mem), sum(p[1] for p in mem) / len(mem)
    district_label[d] = [round(cx), round(cy - 34)]
# A continent's name goes in the sea beside its coast, where it covers no
# town. How big a name is on screen depends on the screen, so the page chooses
# the place. Here each continent gives it 32 places to choose from: the point
# on its coast in each direction, found by walking out from its middle to the
# last cell of its own land.
SHORE_RAYS = 32
cont_shore = {}
for cid in lands:
    cx, cy = land_centre[cid]
    pts = []
    for k in range(SHORE_RAYS):
        a_ = 2 * math.pi * k / SHORE_RAYS
        last, r_ = (cx, cy), 0.0
        while r_ < 2.2 * R_land[cid] + 400:
            r_ += STEP / 2
            x_, y_ = cx + r_ * math.cos(a_), cy + r_ * math.sin(a_)
            if owner_at(x_, y_) == cid:
                last = (x_, y_)
        pts.append([round(last[0]), round(last[1])])
    cont_shore[cid] = pts

# Colours: each continent has a family of hues and its countries share it,
# so a continent reads as one place from far out.
FAMILY = [42, 24, 205, 128, 285, 330, 170]
hue = {}
cont_hue = {}
for k, cid in enumerate(lands):
    base = FAMILY[k % len(FAMILY)]
    cont_hue[cid] = base
    rs = regions_on[cid]
    for i, r in enumerate(sorted(rs, key=lambda r: math.atan2(home[r][1] - anchor[cid][1], home[r][0] - anchor[cid][0]))):
        hue[r] = round((base + (i - (len(rs) - 1) / 2) * 24) % 360)

data = {
    "bounds": [round(minx), round(miny), round(maxx - minx), round(maxy - miny)],
    "coast": coast,
    "plains": {"land": plains_land, "spots": plains_spots},
    "bridges": bridges,
    "waves": [[round(x), round(y)] for x, y in waves],
    "continents": {cid: {"hue": cont_hue[cid], "shore": cont_shore[cid]} for cid in lands},
    "regions": {r: {"hue": hue[r], "land": land[r], "spots": region_spots[r]} for r in order},
    "districts": {d: {"shade": d_in[districts[d]["region"]].index(d), "land": county.get(d, ""),
                      "label": district_label[d]} for d in dlist},
    "towns": {c: {"x": round(pos[c][0]), "y": round(pos[c][1]), "tier": tier[c], "weight": weight[c],
                  "land": land_of[c], "plains": c in plains} for c in codes},
    "landmarks": {lm["tutorial"]: [round(p[0]), round(p[1])] for lm, p, _ in lm_pos},
}
json.dump(data, open(out_path, "w"), separators=(",", ":"), sort_keys=False)
for cid in lands:
    ms = members[cid]
    cx, cy = land_centre[cid]
    reach_ = max(math.dist((cx, cy), pos[c]) for c in ms)
    print(f"{cid:22} towns {len(ms):3}  anchor {tuple(round(v) for v in anchor[cid])}  radius planned {R_land[cid]:.0f} settled {reach_:.0f}", file=sys.stderr)
print("bridges", [(b["a"], b["b"], b["count"], round(math.dist(*b["ends"]))) for b in bridges], file=sys.stderr)
print("towns", len(codes), "districts", len(dlist), "landmarks", len(lm_pos), "depth", max(tier.values()), file=sys.stderr)
