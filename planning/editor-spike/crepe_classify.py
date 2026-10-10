import sys, json, re, collections
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
import build as b
import os
S = os.environ.get("SPIKE_OUT", "/tmp/editor-spike"); os.makedirs(S, exist_ok=True)

def norm_html(x):
    text, maths = b.extract_math(x)
    text = b.loosen_tight_lists(text)
    html, _ = b.to_html(text)
    html = re.sub(r"dlmath(\d+)z", lambda m: f"[{'D' if maths[int(m.group(1))].display else 'I'}:{maths[int(m.group(1))].tex}]", html)
    return re.sub(r"\s+", " ", html).strip()

rows = json.load(open(S + "/fid_all.json" if len(sys.argv) < 2 else sys.argv[1]))
cat = collections.Counter(); ex = collections.defaultdict(list); bykind = collections.defaultdict(collections.Counter)
for r in rows:
    if r["md"] is None: cat["error"] += 1; ex["error"].append(r); bykind[r["kind"]]["error"] += 1; continue
    a, o = r["text"].strip(), r["md"].strip()
    if a == o: c = "byte-identical"
    else:
        try:
            same = norm_html(a) == norm_html(o)
        except Exception as e:
            same = None
        if same is None: c = "unclassified"
        elif same: c = "text differs, page identical"
        else:
            c = "page DIFFERS"
            if re.search(r"\$\$", a) and not re.search(r"\$\$", o): c = "page DIFFERS: display maths"
    cat[c] += 1; ex[c].append(r); bykind[r["kind"]][c] += 1
tot = sum(cat.values())
print("blocks:", tot)
for c, n in cat.most_common(): print(f"  {n:6}  {n/tot*100:5.1f}%  {c}")
print("by kind:")
for k, cs in bykind.items(): print("  ", k, dict(cs))
json.dump({c: ex[c][:400] for c in ex}, open(S + "/fid_classes.json", "w"))
