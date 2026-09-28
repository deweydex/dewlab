"""Check a topic-map file.

    python3 validate.py proposal <file> <area>     one area's proposal or reconciliation
    python3 validate.py graph <file>               the whole map

Exit 0 when there are no errors. Warnings are for judgement, not failure.
"""
import collections, json, re, sys
from pathlib import Path
import yaml

HERE = Path(__file__).parent
REPO = Path("/home/user/dewlab")
ROLES = {"teaches", "closer-look", "context", "applies"}
LANDMARKS = {"project", "orientation", "review", "context"}
ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

mode, path = sys.argv[1], Path(sys.argv[2])
area = sys.argv[3] if len(sys.argv) > 3 else None
errors, warns = [], []
E = errors.append
W = warns.append

GEN = HERE / "generated"
inv = {r["slug"]: r for r in json.load(open(GEN / "inventory.json"))}
try:
    doc = json.load(open(path))
except Exception as exc:
    print(f"ERROR: {path} is not valid JSON: {exc}")
    sys.exit(1)

topics = doc.get("topics") or []
districts = {d.get("id"): d for d in doc.get("districts") or []}
tids = [t.get("id") for t in topics]
tset = set(tids)
for d in districts:
    if not d or not ID.match(d):
        E(f"district id {d!r} is not kebab-case")
if mode == "graph":
    regions = {r.get("id") for r in doc.get("regions") or []}
    if not regions:
        E("graph has no regions")
    for d in districts.values():
        if d.get("region") not in regions:
            E(f"district {d.get('id')} names region {d.get('region')!r}, which is not in regions")
    # Continents are optional; when there are any, every region is on exactly one.
    conts = doc.get("continents") or []
    if conts:
        on = collections.Counter(r for c in conts for r in c.get("regions") or [])
        for r in sorted(regions):
            if on[r] != 1:
                E(f"region {r} is on {on[r]} continents, not one")
        for r in on:
            if r not in regions:
                E(f"a continent names region {r!r}, which is not in regions")
        if sum(1 for c in conts if c.get("kind") == "start") > 1:
            E("more than one continent is the start")
        for c in conts:
            if not ID.match(c.get("id") or ""):
                E(f"continent id {c.get('id')!r} is not kebab-case")
for i, dup in collections.Counter(tids).items():
    if dup > 1:
        E(f"topic id {i} is used {dup} times")

def ref_ok(n):
    if n in tset:
        return True
    if mode == "proposal" and isinstance(n, str) and (n.startswith("ext:") or n.startswith("old:")):
        return True
    return False

placed = collections.defaultdict(list)
for t in topics:
    tid = t.get("id")
    for f in ("id", "name", "district", "plain", "needs", "steps", "outcomes", "replaces", "size"):
        if f not in t:
            E(f"topic {tid}: missing field {f}")
    if tid and not ID.match(tid):
        E(f"topic id {tid!r} is not kebab-case")
    if t.get("district") not in districts:
        E(f"topic {tid}: district {t.get('district')!r} is not declared")
    for n in t.get("needs") or []:
        if not ref_ok(n):
            E(f"topic {tid}: needs {n!r}, which does not resolve" + ("" if mode == "graph" else " (use ext:<name> or old:<code> for another area)"))
        if n == tid:
            E(f"topic {tid} needs itself")
    name = t.get("name") or ""
    if re.search(r"\b(MIT|PDP|CMPS|WA|DBM|FOOP)-", name):
        E(f"topic {tid}: name carries an outcome code")
    if len(name.split()) > 8:
        W(f"topic {tid}: name is {len(name.split())} words long")
    teaches = 0
    for s in t.get("steps") or []:
        slug = s.get("tutorial")
        if slug not in inv:
            E(f"topic {tid}: step names page {slug!r}, which is not in the inventory")
            continue
        role = s.get("role")
        if role not in ROLES:
            E(f"topic {tid}: step {slug} has role {role!r}; use one of {sorted(ROLES)}")
        if role == "teaches":
            teaches += 1
        sec = s.get("section")
        if sec and sec not in {h["anchor"] for h in inv[slug]["headings"]}:
            W(f"topic {tid}: step {slug} names section {sec!r}, not among that page's heading anchors")
        placed[slug].append(("step", tid, role, sec))
    if teaches == 0:
        W(f"topic {tid}: no page teaches it yet (planned)")
    if teaches > 5:
        W(f"topic {tid}: {teaches} pages teach it; check the split test")

for lm in doc.get("landmarks") or []:
    slug = lm.get("tutorial")
    if slug not in inv:
        E(f"landmark names page {slug!r}, which is not in the inventory")
        continue
    if lm.get("kind") not in LANDMARKS:
        E(f"landmark {slug}: kind {lm.get('kind')!r}; use one of {sorted(LANDMARKS)}")
    for a in lm.get("at") or []:
        if not ref_ok(a):
            E(f"landmark {slug}: at {a!r} does not resolve")
    placed[slug].append(("landmark", None, lm.get("kind"), None))
for el in doc.get("elsewhere") or []:
    slug = el.get("tutorial")
    if mode == "graph":
        E(f"graph still lists {slug} as elsewhere")
    elif slug not in inv:
        E(f"elsewhere names page {slug!r}, which is not in the inventory")
    else:
        placed[slug].append(("elsewhere", None, None, None))

# every page in scope placed
scope = [s for s, r in inv.items() if mode == "graph" or r["area"] == area]
missing = [s for s in scope if s not in placed]
for s in missing:
    E(f"page {s} ({inv[s]['title']}) is not placed as a step, landmark" + (" or elsewhere" if mode != "graph" else ""))

# the needs graph
g = {t["id"]: [n for n in t.get("needs") or [] if n in tset] for t in topics if t.get("id")}
state, stack, cycle = {}, [], None
def visit(n):
    global cycle
    state[n] = 1; stack.append(n)
    for m in g.get(n, []):
        if state.get(m) == 1 and cycle is None:
            cycle = stack[stack.index(m):] + [m]
        elif m not in state:
            visit(m)
    stack.pop(); state[n] = 2
sys.setrecursionlimit(10000)
for n in g:
    if n not in state:
        visit(n)
if cycle:
    E("needs has a cycle: " + " -> ".join(cycle))
else:
    reach = {}
    def anc(n):
        if n in reach: return reach[n]
        out = set()
        for m in g[n]:
            out.add(m); out |= anc(m)
        reach[n] = out; return out
    for n in g:
        for m in g[n]:
            others = [o for o in g[n] if o != m]
            if any(m in anc(o) for o in others):
                W(f"topic {n}: needs {m} directly and through another need; drop the direct one")
    tier = {}
    def depth(n):
        if n in tier: return tier[n]
        tier[n] = 0 if not g[n] else 1 + max(depth(m) for m in g[n]); return tier[n]
    for n in g: depth(n)

# old topics and outcomes
old = yaml.safe_load(open(REPO / "planning/curriculum/topics.yaml"))["topics"]
replaced = {c for t in topics for c in t.get("replaces") or []}
culled = {c.get("code") for c in doc.get("outcomes_culled") or []}
for c in replaced:
    if c not in old:
        W(f"replaces names {c}, which is not an old topic code")
if mode == "proposal":
    mine = json.load(open(GEN / "old-topics-by-area.json")).get(area, [])
    for c in mine:
        if c not in replaced and c not in culled:
            W(f"old topic {c} ({old[c]['name']}) is not in any replaces or outcomes_culled")
else:
    for c in old:
        o = old[c].get("outcome")
        if c not in replaced and c not in culled and not (o and (set([o] if isinstance(o, str) else o) & culled)):
            E(f"old topic {c} ({old[c]['name']}) is not in any replaces or outcomes_culled")
    outs = yaml.safe_load(open(REPO / "planning/curriculum/outcomes.yaml"))["outcomes"]
    scope_out = {e["code"] for e in (yaml.safe_load(open(REPO / "planning/curriculum/out-of-scope.yaml")) or {}).get("outcomes") or []}
    served = {o for t in topics for o in t.get("outcomes") or []}
    for e in outs:
        if e["code"] not in served and e["code"] not in culled and e["code"] not in scope_out:
            E(f"outcome {e['code']} is served by no topic and not culled")

# report
print(f"{len(topics)} topics, {len(districts)} districts, {len(doc.get('landmarks') or [])} landmarks, "
      f"{len(doc.get('elsewhere') or [])} elsewhere, {len(scope)} pages in scope")
if not cycle and g:
    words_of = collections.defaultdict(float)
    teach_count = collections.Counter(s for s, ps in placed.items() for p in ps if p[0] == "step" and p[2] == "teaches")
    for t in topics:
        for s in t.get("steps") or []:
            if s.get("role") == "teaches" and s.get("tutorial") in inv:
                words_of[t["id"]] += inv[s["tutorial"]]["words"] / max(1, teach_count[s["tutorial"]])
    by_tier = collections.defaultdict(list)
    for n, d in tier.items():
        by_tier[d].append(words_of.get(n, 0))
    print("depth  topics  median words taught per topic (effort proxy)")
    for d in sorted(by_tier):
        v = sorted(by_tier[d]); med = v[len(v) // 2]
        print(f"{d:5}  {len(v):6}  {med:8.0f}")
    per_d = collections.Counter(t.get("district") for t in topics)
    print("topics per district:", dict(per_d))
for w in warns:
    print("WARN:", w)
for e in errors:
    print("ERROR:", e)
print(f"{len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
