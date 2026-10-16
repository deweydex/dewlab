import os
import sys, io, re, random, threading, http.server, socketserver, functools, collections, json
from pathlib import Path
from playwright.sync_api import sync_playwright

def _chromium():
    """CHROMIUM if set, else a Chromium already installed under PLAYWRIGHT_BROWSERS_PATH."""
    import glob as _g
    found = os.environ.get("CHROMIUM") or next(iter(sorted(_g.glob(os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"), "chromium-*/chrome-linux/chrome")))), None)
    return {"executable_path": found} if found else {}

from PIL import Image, ImageChops
ROOT = Path(__file__).resolve().parents[2]; SITE = ROOT / "site"
import os
S = os.environ.get("SPIKE_OUT", "/tmp/editor-spike"); os.makedirs(S, exist_ok=True)
OVERRIDE = open(sys.argv[1]).read(); NPAGES = int(sys.argv[2]); THEMES = sys.argv[3].split(",")
TAGS = __import__("os").environ.get("TAGS","p,h2,h3,ul,ol,blockquote,table").split(",")
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(SITE)))
threading.Thread(target=srv.serve_forever, daemon=True).start(); port = srv.server_address[1]
pages = sorted(p.stem for p in (SITE / "tutorials").glob("*.html") if (ROOT / "tutorials" / p.stem.replace("-practice","") / f"{p.stem}.md").exists())
random.Random(7).shuffle(pages); pages = pages[:NPAGES]
rows = []
def measure(page, idx, tag, block, clip_pad=60):
    def rects():
        return page.evaluate("""() => [...document.querySelectorAll('main#dl-body > [data-md]')].map(el => { const r = el.getBoundingClientRect(); return [el.getAttribute('data-md'), Math.round(r.top + scrollY), Math.round(r.height), Math.round(r.left), Math.round(r.width)] })""")
    els = page.query_selector_all(f"main#dl-body > {tag}[data-md]")
    if idx >= len(els): return None
    target = els[idx]; target.scroll_into_view_if_needed()
    key = target.get_attribute("data-md")
    s, e = map(int, key.split(":"))
    before = rects(); box = target.bounding_box(); sy = page.evaluate("scrollY")
    clip = {"x": 0, "y": max(0, box["y"] + sy - clip_pad), "width": int(__import__("os").environ.get("VW","1100")), "height": min(box["height"], 700) + 2 * clip_pad}
    ib = Image.open(io.BytesIO(page.screenshot(clip=clip, full_page=True))).convert("RGB")
    return before, key, clip, ib, s, e
with sync_playwright() as pw:
    br = pw.chromium.launch(**_chromium(), args=["--no-sandbox"])
    for theme in THEMES:
        import os
        vw = int(os.environ.get("VW", "1100")); mobile = vw < 700
        ctx = br.new_context(viewport={"width": vw, "height": 900 if not mobile else 844}, color_scheme=theme, is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
        for name in pages:
            src_name = name
            src = (ROOT / "tutorials" / re.sub(r"-practice$", "", name) / f"{name}.md").read_text()
            for tag in TAGS:
                for idx in range(2):
                    page = ctx.new_page(); page.on("pageerror", lambda e: None)
                    try:
                        page.goto(f"http://127.0.0.1:{port}/tutorials/{name}.html"); page.wait_for_load_state("networkidle")
                        m = measure(page, idx, tag, None)
                        if not m: page.close(); break
                        before, key, clip, ib, s, e = m
                        # the same preparation the edit page would do: protect maths for the editor
                        text = src[s:e]
                        page.add_style_tag(content=OVERRIDE)
                        page.evaluate("""async ([idx, tag, block]) => {
                            const { createInPlaceEditor } = await import('/assets/vendor/spike.bundle.js');
                            const target = document.querySelectorAll(`main#dl-body > ${tag}[data-md]`)[idx];
                            const wrap = document.createElement('div'); wrap.className = 'dl-spike-edit'; wrap.setAttribute('data-md', target.getAttribute('data-md'));
                            target.after(wrap); target.hidden = true; target.removeAttribute('data-md');
                            const ed = createInPlaceEditor(wrap, block); await ed.ready; }""", [idx, tag, re.sub(r"\$\$?[^$]+\$\$?", lambda m: "dlmathz", text)])
                        page.wait_for_timeout(120)
                        after = {r[0]: r for r in page.evaluate("""() => [...document.querySelectorAll('main#dl-body > [data-md]')].map(el => { const r = el.getBoundingClientRect(); return [el.getAttribute('data-md'), Math.round(r.top + scrollY), Math.round(r.height), Math.round(r.left), Math.round(r.width)] })""")}
                        bmap = {r[0]: r for r in before}
                        others = [abs(after[k][1] - bmap[k][1]) for k in bmap if k in after and k != key]
                        own = (after.get(key) or [0, 0, 0])[2] - bmap[key][2]
                        ia = Image.open(io.BytesIO(page.screenshot(clip=clip, full_page=True))).convert("RGB")
                        d = ImageChops.difference(ib, ia).convert("L"); px = sum(1 for v in d.get_flattened_data() if v > 24) / (d.size[0] * d.size[1]) * 100
                        rows.append(dict(snip=text[:90].replace(chr(10), "⏎"), page=name, tag=tag, theme=theme, own=own, shift=max(others, default=0), px=round(px, 2), maths="dlmathz" in re.sub(r"\$\$?[^$]+\$\$?", "dlmathz", text)))
                    except Exception as exc:
                        rows.append(dict(page=name, tag=tag, theme=theme, error=str(exc)[:100]))
                    finally:
                        page.close()
        ctx.close()
    br.close()
json.dump(rows, open(S + "/swapall_" + __import__("os").environ.get("VW","1100") + "_" + "-".join(THEMES) + ".json", "w"))
by = collections.defaultdict(list)
for r in rows: by[(r["theme"], r["tag"])].append(r)
print(f"{len(rows)} swaps over {len(pages)} pages")
for (theme, tag), rs in sorted(by.items()):
    ok = [r for r in rs if "error" not in r]
    exact = sum(1 for r in ok if r["own"] == 0 and r["shift"] == 0)
    low = sum(1 for r in ok if r["px"] <= 0.5)
    print(f"  {theme:5} {tag:11} n={len(rs):3} errors={len(rs)-len(ok)}  no layout shift: {exact}/{len(ok)}   <=0.5% pixels changed: {low}/{len(ok)}   worst px%: {max((r['px'] for r in ok), default=0)}  worst shift: {max((r['shift'] for r in ok), default=0)}")
