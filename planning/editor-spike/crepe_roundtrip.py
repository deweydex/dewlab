import os
import sys, json, re, threading, http.server, socketserver, functools, time, random, collections
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from pathlib import Path
import source_map as sm
from playwright.sync_api import sync_playwright

def _chromium():
    """CHROMIUM if set, else a Chromium already installed under PLAYWRIGHT_BROWSERS_PATH."""
    import glob as _g
    found = os.environ.get("CHROMIUM") or next(iter(sorted(_g.glob(os.path.join(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"), "chromium-*/chrome-linux/chrome")))), None)
    return {"executable_path": found} if found else {}


ROOT = Path(__file__).resolve().parents[2]
KINDS = {"paragraph", "heading", "list", "quote", "table"}

def collect(limit_pages=None, per_page=None, seed=1):
    out = []
    files = sorted(p for p in (ROOT / "tutorials").glob("*/*.md"))
    random.Random(seed).shuffle(files)
    for p in files[:limit_pages]:
        t = p.read_text(); base = t.find("\n---", 3) + 4
        bl = [k for k in sm.blocks(t[base:]) if k.kind in KINDS]
        random.Random(seed).shuffle(bl)
        for k in bl[:per_page]:
            out.append({"page": p.name, "kind": k.kind, "text": t[base + k.start: base + k.end]})
    return out

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def serve():
    handler = functools.partial(Quiet, directory=str(ROOT))
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, srv.server_address[1]

HTML = """<!doctype html><meta charset=utf-8><body><div id=host></div>
<script type=module>
import { createProseEditor } from "/assets/vendor/milkdown.bundle.js";
window.roundtrip = async (blocks) => {
  const out = [];
  for (const b of blocks) {
    const host = document.getElementById("host");
    host.replaceChildren();
    const el = document.createElement("div"); host.append(el);
    let md = null, err = null;
    try {
      const ed = createProseEditor(el, b, {});
      await ed.ready;
      md = ed.getMarkdown();
      ed.destroy();
    } catch (e) { err = String(e).slice(0, 120); }
    out.push({ md, err });
  }
  return out;
};
window.ready = true;
</script>"""

import build as B

def protect(text):
    """Lift maths out for Crepe, as the build does for Python-Markdown."""
    found = []
    t = text.replace("\\$", "\x00ESC\x00")
    t = B.DISPLAY_MATH_RE.sub(lambda m: (found.append(m.group(0)), f"dlmath{len(found)-1}z")[1], t)
    t = B.INLINE_MATH_RE.sub(lambda m: (found.append(m.group(0)), f"dlmath{len(found)-1}z")[1], t)
    return t.replace("\x00ESC\x00", "\\$"), found

def restore(md, found):
    return re.sub(r"dlmath(\d+)z", lambda m: found[int(m.group(1))], md)

def tidy(original, md, kind):
    """What the in-page editor would do to Crepe's output before splicing it back."""
    if kind == "list":
        marker = re.match(r"\s*([-*+])\s", original)
        tight = not re.search(r"\n[ \t]*\n", original)
        if marker:
            md = re.sub(r"(?m)^(\s*)[*+-](\s)", lambda m: m.group(1) + marker.group(1) + m.group(2), md)
        if tight:
            md = re.sub(r"\n[ \t]*\n(?=[ \t]*(?:[-*+]|\d+[.)])\s)", "\n", md)
    if kind == "table" and "<br" not in original:
        md = re.sub(r"<br\s*/?>", "", md)
    return md

def run(blocks, batch=100):
    srv, port = serve()
    results = []
    with sync_playwright() as pw:
        br = pw.chromium.launch(**_chromium(), args=["--no-sandbox"])
        page = br.new_page()
        errs = []
        page.on("pageerror", lambda e: errs.append(str(e)[:150]))
        page.route(f"http://127.0.0.1:{port}/__f.html", lambda r: r.fulfill(body=HTML, content_type="text/html"))
        page.goto(f"http://127.0.0.1:{port}/__f.html")
        page.wait_for_function("window.ready === true", timeout=60000)
        t0 = time.time()
        for i in range(0, len(blocks), batch):
            chunk = [b["text"] for b in blocks[i:i + batch]]
            results += page.evaluate("(bs) => window.roundtrip(bs)", chunk)
        dt = time.time() - t0
        br.close()
    srv.shutdown()
    return results, dt, errs

if __name__ == "__main__":
    n_pages, per = int(sys.argv[1]), int(sys.argv[2])
    blocks = collect(n_pages, per)
    prot = [protect(b["text"]) for b in blocks]
    res, dt, errs = run([dict(b, text=p[0]) for b, p in zip(blocks, prot)])
    for b, p, r in zip(blocks, prot, res):
        if r["md"] is not None:
            r["md"] = tidy(b["text"], restore(r["md"], p[1]), b["kind"])
    print(f"{len(blocks)} blocks in {dt:.1f}s ({dt/len(blocks)*1000:.0f} ms each); page errors: {errs[:3]}")
    json.dump([dict(b, **r) for b, r in zip(blocks, res)], open(sys.argv[3] if len(sys.argv) > 3 else "/dev/null", "w"))
    same = sum(1 for b, r in zip(blocks, res) if r["md"] is not None and r["md"].strip() == b["text"].strip())
    errc = sum(1 for r in res if r["err"])
    print(f"exactly equal (ignoring surrounding whitespace): {same}/{len(blocks)}; errors: {errc}")
