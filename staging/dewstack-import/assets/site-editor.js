/* The web track's site editor: an HTML, CSS and JavaScript pane beside a
 * live preview and a console, for the fenced `site=name` blocks build.py
 * turns into `.dl-site-editor` elements.
 *
 * Ported in shape from dewmini's Site tab (deweydex/dewlab,
 * compose/dewmini.js, openSiteFile() and renderSiteView(); plan,
 * CONSOLIDATION_PLAN.md section 13), not its code: that version reads and
 * writes a mounted workspace, which a tutorial page does not have. Nothing
 * here is saved. A reader's changes live only in the page until they
 * refresh; the student's own fork is where real work is kept, and the
 * "Download these files" button is the bridge between the two.
 *
 * Two run models, on purpose (planning/CONSOLE_AND_WORKSPACE.md, decided
 * 2026-09-06). HTML and CSS are live: a stylesheet is a state, and the
 * lesson is watching the box change colour under your hand, so the
 * preview redraws on every keystroke in those panes. JavaScript is a
 * program, and a program runs when asked: the JavaScript pane does
 * nothing until Run (or Ctrl/Cmd+Enter inside it), and until then the
 * preview keeps the last script that was run, so retyping a colour does
 * not silently re-run a half-edited program. Half-typed code is a syntax
 * error on most keystrokes, and a console that flashed red between every
 * character would teach a reader to ignore it.
 *
 * The console. The preview document carries a small relay script
 * (RELAY, below) ahead of the reader's own CSS. It replaces console.log
 * and its siblings with versions that also post the formatted arguments
 * to this page, and listens for the window's `error` event (uncaught
 * runtime errors and syntax errors in an inline script alike) and for
 * `unhandledrejection`, posting each with its line and column. This page
 * draws what arrives under the preview. Ported in shape from dewmini's
 * JavaScript cell engine (dewlab, compose/js-cell-engine.js), which runs
 * the same relay headless.
 *
 * Line numbers arrive relative to the whole preview document, not the
 * pane, so buildPreview() counts the newlines ahead of each pane and the
 * console does the subtraction. The relay sits first so its own line
 * count is a constant and the CSS and HTML panes are the only variables.
 * Verified in a headless Chromium for runtime, syntax, async and handler
 * errors (the design document's section 4.1).
 *
 * The preview iframe is sandboxed to "allow-scripts" only: no
 * allow-same-origin, so a script in a reader's experiment cannot reach the
 * rest of this page or anything it can see. Messages are matched to an
 * editor by `event.source`, the frame's own window, so one frame cannot
 * write into another's console.
 *
 * One component, two pages. On a tutorial page every `.dl-site-editor`
 * is mounted here, at load, over its textareas. The workspace page
 * (assets/workspace.js) mounts its own editor by hand through
 * `window.dewstackSiteEditor.mount()`, supplying CodeMirror panes in
 * place of the textareas. What a pane has to be is small: get, set,
 * focus, selectLine, onInput. Everything above that line — the preview,
 * the Run model, the console — is written once, against that surface,
 * and does not know which kind it is holding.
 */

(function () {
  "use strict";

  /* Runs inside the preview document, not this page: read it as a small,
   * separate program. Plain ES5 on purpose, since it is embedded as a
   * string and gets no build step. It reports; it never decides. */
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

  /* A plain-language second line for the errors a first term meets most,
   * matched against the browser's own message. Student-facing text: it
   * goes through the plain-language checks like any other sentence. Data,
   * so a new entry is a line added here, from what students hit in class,
   * not a feature. The first matching entry wins. */
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

  /* Assembles the preview document and records where each pane's first
   * line lands in it, so a reported line can be handed back to the pane
   * it came from. `</script` inside the reader's script is escaped, since
   * left alone it would end the script element early and put the rest of
   * the pane on the page as text; the escaped form runs the same. */
  function buildPreview(html, css, js) {
    /* Without a base tag, a srcdoc document resolves relative addresses,
     * including a same-page link like href="#two", against this page's own
     * address rather than its own. "about:srcdoc" keeps a link inside the
     * preview instead of loading a copy of this page into it. */
    const head = `<!DOCTYPE html><html><head><base href="about:srcdoc">\n${RELAY}\n<style>${css}</style></head>\n<body>`;
    const htmlStart = countLines(head); // the line `<body>` is on; the HTML pane starts there too
    const withHtml = `${head}${html}`;
    const jsStart = countLines(withHtml); // the line `<script>` opens on; the JS pane's first line
    const safeJs = js.replace(/<\/script/gi, "<\\/script");
    const doc = `${withHtml}<script>${safeJs}<\/script></body></html>`;
    return { doc, htmlStart, jsStart };
  }

  /* Rendering treats the frame as one resource. A document is written to
   * `srcdoc` only when no earlier one is still loading; until the frame's
   * load event, later documents wait in `pendingDoc`, newest wins, and
   * flush() writes it. Traced in a real Chromium: four synchronous
   * `srcdoc` writes in one task produced one load, of the *first*
   * document, so the workspace opened on an empty preview. Coalescing
   * on load rather than on a timer keeps a fast typist's last keystroke
   * from being the one that is dropped. The line offsets and the
   * console are reset at write time, so they describe the document the
   * frame is showing, not one that never loaded. */
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

  /* ------------------------------------------------------------ console */

  function clearConsole(state) {
    if (state.consoleOutput) state.consoleOutput.textContent = "";
  }

  function showConsole(state) {
    if (state.console && state.console.hidden) state.console.hidden = false;
  }

  /* Which pane a document line belongs to, and the line within it. The
   * JavaScript pane starts at jsStart; the HTML pane at htmlStart; the
   * relay and the CSS pane before that, where a reader's error cannot
   * come from except through a `<script>` typed into the HTML pane. */
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

  /* --------------------------------------------------------------- mount */

  /* Mounts one `.dl-site-editor`. `createPane(field, lang)` may replace
   * the default textarea pane; it receives the textarea the markup
   * carries and must return the pane surface textareaPane() defines.
   * `onChange(lang, text)` fires on every edit in any pane, for a page
   * that saves. Returns a handle the workspace page drives. */
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
      /* A percentage of the editor's own width, not a fixed pixel count:
       * the reading column itself can be anywhere from 26rem to 60rem,
       * set in Settings, so a fixed width could overflow a narrow one. */
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

    /* Open in the workspace: the three panes go into localStorage under a
     * hand-off key, then the link is followed as normal. workspace.js
     * reads the key on arrival, makes a site from it named after this
     * page and this editor, and removes it. A separate key rather than
     * an edit to the workspace's own saved state, so a workspace tab
     * already open elsewhere is never written under. */
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
