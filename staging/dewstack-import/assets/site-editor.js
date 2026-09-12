
(function () {
  "use strict";

  const RELAY = [
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
    "  ['log', 'info', 'warn', 'error'].forEach(function (level) {",
    "    var real = console[level] ? console[level].bind(console) : function () {};",
    "    console[level] = function () {",
    "      var args = Array.prototype.slice.call(arguments);",
    "      real.apply(console, args);",
    "      send({ dlSite: 'console', level: level, text: args.map(fmt).join(' ') });",
    "    };",
    "  });",
    "  window.addEventListener('error', function (ev) {",
    "    send({ dlSite: 'error', message: ev.message, line: ev.lineno, column: ev.colno });",
    "  });",
    "  window.addEventListener('unhandledrejection', function (ev) {",
    "    var r = ev.reason;",
    "    send({ dlSite: 'error', message: (r && r.name ? r.name + ': ' + r.message : String(r)), line: 0, column: 0 });",
    "  });",
    "})();",
    "<\/script>",
  ].join("\n");

  const FRIENDLY = [
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

  const editors = [];

  /* Where "Open in the workspace" leaves a site for workspace.js. */
  const INCOMING_KEY = "dewstack:workspace:incoming";

  /* A pane over a plain <textarea>: the tutorial-page default, and the
   * shape a CodeMirror pane has to match (workspace.js). */
  function textareaPane(field) {
    return {
      get: () => field.value,
      set: (text) => { field.value = text; },
      focus: () => field.focus(),
      /* The nearest a textarea gets to a marker: select the whole line. */
      selectLine: (line) => {
        const lines = field.value.split("\n");
        let pos = 0;
        for (let i = 0; i < Math.min(line - 1, lines.length); i += 1) pos += lines[i].length + 1;
        field.focus();
        field.setSelectionRange(pos, pos + (lines[line - 1] || "").length);
      },
      onInput: (cb) => field.addEventListener("input", () => cb(field.value)),
      onRun: (cb) => field.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); cb(); }
      }),
    };
  }

  function valueOf(state, lang) {
    const pane = state.panes[lang];
    return pane ? pane.get() : "";
  }

  function countLines(text) {
    return text.length ? text.split("\n").length : 0;
  }

  function buildPreview(html, css, js) {
    const head = `<!DOCTYPE html><html><head><base href="about:srcdoc">\n${RELAY}\n<style>${css}</style></head>\n<body>`;
    const htmlStart = countLines(head); // the line `<body>` is on; the HTML pane starts there too
    const withHtml = `${head}${html}`;
    const jsStart = countLines(withHtml); // the line `<script>` opens on; the JS pane's first line
    const safeJs = js.replace(/<\/script/gi, "<\\/script");
    const doc = `${withHtml}<script>${safeJs}<\/script></body></html>`;
    return { doc, htmlStart, jsStart };
  }

  function render(state) {
    state.pendingDoc = buildPreview(valueOf(state, "html"), valueOf(state, "css"), state.lastRunJs);
    flush(state);
  }

  function flush(state) {
    if (state.loading || !state.pendingDoc) return;
    const built = state.pendingDoc;
    state.pendingDoc = null;
    state.htmlStart = built.htmlStart;
    state.jsStart = built.jsStart;
    clearConsole(state);
    state.loading = true;
    /* A load event that never comes (a frame detached mid-navigation)
     * must not wedge the preview: give up waiting after a moment. */
    clearTimeout(state.loadTimer);
    state.loadTimer = setTimeout(() => { state.loading = false; flush(state); }, 2000);
    state.frame.srcdoc = built.doc;
  }

  function run(state) {
    state.lastRunJs = valueOf(state, "js");
    render(state);
  }

  function clearConsole(state) {
    if (state.consoleOutput) state.consoleOutput.textContent = "";
  }

  function showConsole(state) {
    if (state.console && state.console.hidden) state.console.hidden = false;
  }

  function locate(state, docLine) {
    if (!docLine) return null;
    if (docLine >= state.jsStart) return { lang: "js", label: "JavaScript", line: docLine - state.jsStart + 1 };
    if (docLine >= state.htmlStart) return { lang: "html", label: "HTML", line: docLine - state.htmlStart + 1 };
    return null;
  }

  function friendlyHint(message) {
    for (const entry of FRIENDLY) {
      const m = entry.test.exec(message);
      if (m) return entry.hint(m);
    }
    return null;
  }

  function appendConsoleLine(state, msg) {
    const out = state.consoleOutput;
    if (!out) return;
    showConsole(state);
    if (msg.dlSite === "console") {
      const line = document.createElement("div");
      line.className = `dl-site-console-line dl-site-console-${msg.level}`;
      line.textContent = msg.text;
      out.appendChild(line);
      return;
    }
    const where = locate(state, msg.line);
    const message = String(msg.message).replace(/^Uncaught /, "");
    const line = document.createElement("div");
    line.className = "dl-site-console-line dl-site-console-error";
    const text = document.createElement("span");
    text.textContent = where ? `${message} (${where.label}, line ${where.line})` : message;
    line.appendChild(text);
    if (where && state.panes[where.lang]) {
      /* Name the line, and make the entry a button that lands on it. */
      const go = document.createElement("button");
      go.type = "button";
      go.className = "dl-site-console-goto";
      go.textContent = "Go to line";
      go.addEventListener("click", () => state.panes[where.lang].selectLine(where.line));
      line.appendChild(go);
    }
    out.appendChild(line);
    const hint = friendlyHint(message);
    if (hint) {
      const hintEl = document.createElement("div");
      hintEl.className = "dl-site-console-hint";
      hintEl.textContent = hint;
      out.appendChild(hintEl);
    }
  }

  window.addEventListener("message", (ev) => {
    const msg = ev.data;
    if (!msg || !msg.dlSite) return;
    const state = editors.find((s) => s.frame.contentWindow === ev.source);
    if (state) appendConsoleLine(state, msg);
  });

  function mount(editor, { createPane = null, onChange = null } = {}) {
    const frame = editor.querySelector(".dl-site-frame");
    const fields = editor.querySelectorAll(".dl-site-input");
    const original = {};
    const panes = {};
    fields.forEach((field) => {
      const lang = field.dataset.lang;
      original[lang] = field.value;
      panes[lang] = (createPane && createPane(field, lang)) || textareaPane(field);
    });

    const state = {
      editor, frame, panes, original,
      lastRunJs: panes.js ? panes.js.get() : "",
      console: editor.querySelector(".dl-site-console"),
      consoleOutput: editor.querySelector(".dl-site-console-output"),
      htmlStart: 0, jsStart: 0,
      pendingDoc: null, loading: false, loadTimer: null,
    };
    editors.push(state);
    frame.addEventListener("load", () => {
      clearTimeout(state.loadTimer);
      state.loading = false;
      flush(state);
    });

    Object.entries(panes).forEach(([lang, pane]) => {
      if (lang === "js") {
        pane.onRun(() => run(state));
        if (onChange) pane.onInput((text) => onChange(lang, text));
      } else {
        pane.onInput((text) => { if (onChange) onChange(lang, text); render(state); });
      }
    });

    const runButton = editor.querySelector(".dl-site-run");
    if (runButton) runButton.addEventListener("click", () => run(state));

    const widthControl = editor.querySelector(".dl-site-width");
    const frameWrap = editor.querySelector(".dl-site-frame-wrap");
    const widthReadout = editor.querySelector(".dl-site-preview-controls output");
    if (widthControl && frameWrap) {
      const applyWidth = () => {
        frameWrap.style.width = `${widthControl.value}%`;
        if (widthReadout) widthReadout.textContent = `${widthControl.value}%`;
      };
      widthControl.addEventListener("input", applyWidth);
      applyWidth();
    }

    const resetButton = editor.querySelector(".dl-site-reset");
    if (resetButton) {
      resetButton.addEventListener("click", () => {
        Object.entries(panes).forEach(([lang, pane]) => pane.set(original[lang]));
        if (onChange) Object.keys(panes).forEach((lang) => onChange(lang, original[lang]));
        run(state);
      });
    }

    const downloadButton = editor.querySelector(".dl-site-download");
    if (downloadButton) {
      downloadButton.addEventListener("click", () => downloadFiles(editor, panes));
    }

    const openLink = editor.querySelector(".dl-site-open-workspace");
    if (openLink) {
      openLink.addEventListener("click", () => {
        const slug = (document.querySelector('meta[name="tutorial-slug"]') || {}).content || "";
        const name = [slug, editor.dataset.siteName || "site"].filter(Boolean).join(" ");
        try {
          localStorage.setItem(INCOMING_KEY, JSON.stringify({
            name,
            html: valueOf(state, "html"), css: valueOf(state, "css"), js: valueOf(state, "js"),
          }));
        } catch (e) { /* storage blocked: the workspace opens on its own sites instead */ }
      });
    }

    render(state);

    return {
      values: () => Object.fromEntries(Object.entries(panes).map(([lang, pane]) => [lang, pane.get()])),
      /* Replaces every pane's text at once (a different site, a loaded
       * file) and runs, so the preview and console show the new site. */
      load: (files) => {
        Object.entries(panes).forEach(([lang, pane]) => pane.set(files[lang] || ""));
        run(state);
      },
      run: () => run(state),
      focus: (lang) => panes[lang] && panes[lang].focus(),
    };
  }

  const EXTENSIONS = { html: "html", css: "css", js: "js" };

  /* One file per pane, named after the page: "card.html", "card.css",
   * "card.js". A reader drops these straight into their own fork. */
  function downloadFiles(editor, panes) {
    const base = editor.dataset.siteName || "site";
    Object.entries(panes).forEach(([lang, pane]) => {
      const ext = EXTENSIONS[lang] || "txt";
      const blob = new Blob([pane.get()], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `${base}.${ext}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    });
  }

  /* Tutorial pages: every editor, over its textareas, now. The workspace
   * page marks its editor `data-mount="manual"` and mounts it itself. */
  document.querySelectorAll('.dl-site-editor:not([data-mount="manual"])').forEach((el) => mount(el));

  window.dewstackSiteEditor = { mount, textareaPane };
})();
