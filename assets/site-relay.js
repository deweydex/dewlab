
const RELAY_KEY = "dlSiteRelay";

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

export function buildSiteDocument(html, css, js) {
  const countLines = (text) => (text.length ? text.split("\n").length : 0);
  const head = `<!DOCTYPE html><html><head>\n<base href="about:srcdoc">\n${SITE_RELAY}\n<style>${css}</style></head>\n<body>`;
  const htmlStart = countLines(head);
  const withHtml = `${head}${html}`;
  const jsStart = countLines(withHtml);
  const safeJs = js.replace(/<\/script/gi, "<\\/script");
  return { doc: `${withHtml}<script>${safeJs}<\/script></body></html>`, htmlStart, jsStart };
}

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
