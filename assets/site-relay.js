/* The live-preview engine behind every HTML/CSS/JS site editor on this
 * site — dewmini's Site tab (compose/dewmini.js) and the tutorial-page
 * site editor (assets/tutorial-runtime.js) both mount one of these per
 * editor rather than each keeping their own copy of the relay, the
 * friendly-error map, and the document-assembly/flush logic
 * (DECISIONS_LOG.md 7.142). Before this file existed, that logic was
 * written twice: once here, ported in shape into dewstack's own
 * assets/site-editor.js (2026-09-04), and once again ported back in
 * shape from dewstack's console-and-Run addition into dewmini.js
 * (DECISIONS_LOG.md 7.134, 2026-09-06). Porting in shape rather than
 * sharing code is the right call across the dewlab/dewstack boundary,
 * where the two repositories share no code by design
 * (DECISIONS_LOG.md, planning/DEWSTACK_MERGE.md §1) — it is the wrong
 * call *within* dewlab, where the second copy was heading for exactly
 * the drift two copies of anything eventually have. This file is what
 * both products import instead.
 *
 * What stays outside this file, on purpose: DOM structure, CSS classes,
 * pane labels, the Run button, and how a console line actually gets
 * drawn. dewmini's `dm-siteview-*` chrome and the tutorial page's own
 * `dl-site-*` chrome differ, and should keep differing — a tutorial
 * page's editor lives beside prose and other cells, dewmini's fills a
 * whole tab. `mountSitePreview()` below takes a bare `<iframe>` and two
 * callbacks and reports console lines and errors through them; it never
 * touches a label or a button.
 */

/* The key a relayed message carries, so a page's own `message` listener
 * (there may be several sites' worth on one tutorial page) can tell a
 * site preview's own traffic apart from anything else `postMessage`
 * might carry. dewmini's original called this `dmSite`, dewstack's own
 * port called it `dlSite`; one shared file only needs one name. */
const RELAY_KEY = "dlSiteRelay";

/* Runs inside the preview document, not the page that mounts it — read
 * it as a small, separate program, the same way js-cell-engine.js's own
 * RUNTIME_SRC is one. Plain ES5 on purpose: embedded as a string, it
 * gets none of the vendor build's transpilation. It reports; it never
 * decides. */
export const SITE_RELAY = [
  "<script>",
  "(function () {",
  "  var send = function (m) { parent.postMessage(m, '*'); };",
  "  function fmt(v) {",
  "    if (typeof v === 'string') return v;",
  "    if (v === undefined) return 'undefined';",
  "    if (v === null) return 'null';",
  "    if (typeof v === 'function') return '[Function' + (v.name ? ': ' + v.name : '') + ']';",
  "    if (v instanceof Error) return v.name + ': ' + v.message;",
  "    if (v && v.nodeType === 1) return '<' + v.tagName.toLowerCase() + (v.id ? ' id=\"' + v.id + '\"' : '') + '>';",
  "    try { return JSON.stringify(v); } catch (e) { return String(v); }",
  "  }",
  `  var KEY = ${JSON.stringify(RELAY_KEY)};`,
  "  ['log', 'info', 'warn', 'error'].forEach(function (level) {",
  "    var real = console[level] ? console[level].bind(console) : function () {};",
  "    console[level] = function () {",
  "      var args = Array.prototype.slice.call(arguments);",
  "      real.apply(console, args);",
  "      var m = {}; m[KEY] = 'console'; m.level = level; m.text = args.map(fmt).join(' ');",
  "      send(m);",
  "    };",
  "  });",
  "  window.addEventListener('error', function (ev) {",
  "    var m = {}; m[KEY] = 'error'; m.message = ev.message; m.line = ev.lineno; m.column = ev.colno;",
  "    send(m);",
  "  });",
  "  window.addEventListener('unhandledrejection', function (ev) {",
  "    var r = ev.reason;",
  "    var m = {}; m[KEY] = 'error'; m.message = (r && r.name ? r.name + ': ' + r.message : String(r)); m.line = 0; m.column = 0;",
  "    send(m);",
  "  });",
  "})();",
  "<\/script>",
].join("\n");

/* A plain-language second line for the errors a first term meets most,
 * matched against the browser's own message — the JavaScript counterpart
 * of tutorial_tools.py's _ERROR_HINTS for Python, drawn the same way
 * (.dl-error, then .dl-error-hint). Data, so a new entry is a line added
 * here from what students hit in class. The first match wins. */
const SITE_FRIENDLY = [
  {
    test: /^(Uncaught )?ReferenceError: (.+?) is not defined/,
    hint: (m) => `The page does not know a name called ${m[2]}. Check the spelling, and check that the line that creates ${m[2]} runs before this one.`,
  },
  {
    test: /^(Uncaught )?SyntaxError/,
    hint: () => "Something on this line is not written the way JavaScript expects. Look along the line for a missing bracket, quote or comma.",
  },
  {
    test: /^(Uncaught )?TypeError: Cannot (read|set) properties of null/,
    hint: () => "The page looked for an element and found nothing. Check that the id in the JavaScript matches the id in the HTML exactly, and that the script runs after the element exists.",
  },
  {
    test: /^(Uncaught )?TypeError: (.+?) is not a function/,
    hint: (m) => `${m[2]} is not something the page can call. Check the spelling, and check what ${m[2]} holds.`,
  },
];

export function siteFriendlyHint(message) {
  for (const entry of SITE_FRIENDLY) {
    const m = entry.test.exec(message);
    if (m) return entry.hint(m);
  }
  return null;
}

/* Assembles the preview document and records where each pane's first
 * line lands in it, so a reported line can be handed back to the pane it
 * came from. The relay sits first so its own line count is a constant.
 * `<base href="about:srcdoc">` keeps a relative link (an anchor, an
 * image, a fetch) resolving inside the preview document instead of
 * against the page that mounted it — without it, a plain `href="#two"`
 * inside the preview navigates the mounting page itself, since a
 * `srcdoc` frame's base URL is otherwise its parent's. Found only once
 * this file gave dewmini's own copy and dewstack's a side-by-side read
 * (DECISIONS_LOG.md 7.142): dewstack's site-editor.js already carried
 * this line, dewmini's never had it. `</script` inside the reader's own
 * script is escaped, since left alone it would end the script element
 * early. */
export function buildSiteDocument(html, css, js) {
  const countLines = (text) => (text.length ? text.split("\n").length : 0);
  const head = `<!DOCTYPE html><html><head>\n<base href="about:srcdoc">\n${SITE_RELAY}\n<style>${css}</style></head>\n<body>`;
  const htmlStart = countLines(head);
  const withHtml = `${head}${html}`;
  const jsStart = countLines(withHtml);
  const safeJs = js.replace(/<\/script/gi, "<\\/script");
  return { doc: `${withHtml}<script>${safeJs}<\/script></body></html>`, htmlStart, jsStart };
}

/* Mounts the engine half of one site editor onto a bare `<iframe>`:
 * building the preview document, writing it to `srcdoc` no faster than
 * the frame can load one, and turning the relay's messages back into a
 * console line or a located, friendly-hinted error. Everything about
 * *drawing* those — labels, buttons, a console's own DOM — is the
 * caller's, via `onConsole(level, text)` and
 * `onError({message, where, hint})`, where `where` is
 * `{lang, label, line}` for `html`/`js` or `null` when the error can't be
 * placed (a CSS-only page has no script to blame a line in).
 *
 * One document in flight at a time, newest wins: several synchronous
 * `srcdoc` writes in one task load only the first in a real browser
 * (traced on dewstack's own twin of this view before this file existed;
 * DECISIONS_LOG.md 7.121), so a second write while the frame is still
 * loading the previous one is held and re-flushed once the `load` event
 * fires or a two-second watchdog gives up waiting for it.
 *
 * `run(html, css, js)` and `render(html, css)` both take the current
 * pane text rather than reading it from anywhere, the same choice
 * dewmini's own Web cell preview already made: showing what is typed
 * right now costs nothing extra and needs no debounced read-back. `run`
 * remembers the JavaScript it was given until the next `run` — retyping
 * a stylesheet re-renders live without silently re-running a half-edited
 * script.
 *
 * `onReset()`, when given, fires right as a new document is actually
 * about to be written — not when `render`/`run` is called, which may be
 * held back by the in-flight coalescing above — so a caller clearing its
 * own console between documents clears it at the moment the old one
 * stops being what the frame shows, not before. */
export function mountSitePreview(iframe, { onConsole, onError, onReset } = {}) {
  const state = { lastRunJs: "", htmlStart: 0, jsStart: 0, pendingDoc: null, loading: false, loadTimer: null };

  const locate = (docLine) => {
    if (!docLine) return null;
    if (docLine >= state.jsStart) return { lang: "js", label: "JavaScript", line: docLine - state.jsStart + 1 };
    if (docLine >= state.htmlStart) return { lang: "html", label: "HTML", line: docLine - state.htmlStart + 1 };
    return null;
  };

  const flush = () => {
    if (state.loading || !state.pendingDoc) return;
    const built = state.pendingDoc;
    state.pendingDoc = null;
    state.htmlStart = built.htmlStart;
    state.jsStart = built.jsStart;
    onReset?.();
    state.loading = true;
    clearTimeout(state.loadTimer);
    state.loadTimer = setTimeout(() => { state.loading = false; flush(); }, 2000);
    iframe.srcdoc = built.doc;
  };
  const onLoad = () => { clearTimeout(state.loadTimer); state.loading = false; flush(); };
  iframe.addEventListener("load", onLoad);

  const onMessage = (ev) => {
    if (ev.source !== iframe.contentWindow) return;
    const msg = ev.data;
    if (!msg || !msg[RELAY_KEY]) return;
    if (msg[RELAY_KEY] === "console") {
      onConsole?.(msg.level, msg.text);
      return;
    }
    const where = locate(msg.line);
    const message = String(msg.message).replace(/^Uncaught /, "");
    onError?.({ message, where, hint: siteFriendlyHint(message) });
  };
  window.addEventListener("message", onMessage);

  return {
    render(html, css) {
      state.pendingDoc = buildSiteDocument(html, css, state.lastRunJs);
      flush();
    },
    run(html, css, js) {
      state.lastRunJs = js;
      state.pendingDoc = buildSiteDocument(html, css, state.lastRunJs);
      flush();
    },
    destroy() {
      window.removeEventListener("message", onMessage);
      iframe.removeEventListener("load", onLoad);
      clearTimeout(state.loadTimer);
    },
  };
}
