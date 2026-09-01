/* The slice of CodeMirror 6 a dewlab exec cell needs, bundled into one
 * classic-script-free ES module so a generated page can import it with no
 * build step of its own and no CDN round trip.
 *
 * Everything here is stock CodeMirror: line numbers, the standard Python
 * language support, and the default light / one-dark highlight pair. That is
 * what DECISIONS.md means by these affordances being free — built-in
 * extensions, not custom design work.
 */

import { EditorView, ViewPlugin, keymap, lineNumbers, highlightActiveLine,
         highlightActiveLineGutter, drawSelection, highlightSpecialChars,
         rectangularSelection, crosshairCursor, hoverTooltip,
         showTooltip } from "@codemirror/view";
import { EditorState, Compartment, StateField, StateEffect } from "@codemirror/state";
import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
import { python, localCompletionSource, globalCompletion } from "@codemirror/lang-python";
import { html } from "@codemirror/lang-html";
import { css } from "@codemirror/lang-css";
import { javascript } from "@codemirror/lang-javascript";
import { sql } from "@codemirror/lang-sql";
import { syntaxHighlighting, defaultHighlightStyle, indentOnInput,
         bracketMatching, indentUnit } from "@codemirror/language";
import { search, searchKeymap, highlightSelectionMatches } from "@codemirror/search";
import { closeBrackets, closeBracketsKeymap,
         autocompletion, completionKeymap, snippetCompletion } from "@codemirror/autocomplete";
import { oneDark } from "@codemirror/theme-one-dark";

/* Theme lives in a compartment so the texture panel can swap light/dark
 * without tearing the editor down and losing what the student has typed. */
const themeOf = (dark) => (dark ? oneDark : syntaxHighlighting(defaultHighlightStyle));

const baseTheme = EditorView.theme({
  "&": { backgroundColor: "transparent" },
  ".cm-gutters": { backgroundColor: "transparent", border: "none", opacity: "0.65" },
  ".cm-activeLine, .cm-activeLineGutter": { backgroundColor: "transparent" },
});

/* Keyword/builtin completion (`print`, `for`, `len`, —) and local-name
 * completion (whatever the student has already typed in this cell) are both
 * static — no interpreter involved, so they work the instant a cell mounts,
 * before Pyodide has even started loading. `completeNames`, when the caller
 * supplies one, goes first: it is how a booted cell's own runtime namespace
 * (imported modules, names a student defined) reaches the completion list,
 * wired in from tutorial-runtime.js rather than here, since this file has no
 * idea Pyodide exists. `override` rather than adding to CodeMirror's
 * defaults on purpose — the generic any-word-on-the-page fallback suggests
 * things that are not valid Python, which is worse than fewer, correct
 * suggestions for someone meeting the language for the first time.
 *
 * Jedi-based completion is added as an optional source. When `getJediCompletions`
 * is provided, it is used for pre-execution completion (before the cell has run). */
function pythonCompletion(completeNames, getJediCompletions = null) {
  const sources = [completeNames, localCompletionSource, globalCompletion].filter(Boolean);
  
  // Add Jedi-based completion if available
  if (getJediCompletions) {
    sources.unshift(jediCompletionSource(getJediCompletions));
  }
  
  return autocompletion({ override: sources, activateOnTyping: true });
}

/* Jedi completion source for pre-execution autocomplete.
 * This allows completion and hover docs to work before a cell has been executed,
 * using Jedi's static analysis running inside Pyodide. */
function jediCompletionSource(getJediCompletions) {
  return (context) => {
    const { state } = context;
    const { doc } = state;
    const cursorPos = context.pos;
    
    // Get the text up to the cursor
    const textBeforeCursor = doc.sliceString(0, cursorPos);
    const line = doc.lineAt(cursorPos);
    const lineText = line.text;
    const linePos = cursorPos - line.from;
    
    // Find the word at cursor
    let start = linePos;
    let end = linePos;
    while (start > 0 && /[a-zA-Z0-9_]/.test(lineText[start - 1])) start--;
    while (end < lineText.length && /[a-zA-Z0-9_]/.test(lineText[end])) end++;
    
    if (start === end) {
      // No word at cursor, try to get completions for empty string
      return getJediCompletions(textBeforeCursor, linePos).then(completions => {
        return {
          from: cursorPos,
          options: completions.map(c => ({ label: c.name, type: c.type })),
          validFor: /^[a-zA-Z_]$/
        };
      });
    }
    
    const word = lineText.slice(start, end);
    
    // Get completions from Jedi
    return getJediCompletions(textBeforeCursor, linePos, word).then(completions => {
      if (!completions || completions.length === 0) {
        return null;
      }
      
      return {
        from: line.from + start,
        to: line.from + end,
        options: completions.map(c => ({
          label: c.name,
          type: c.type,
          detail: c.description || ''
        })),
        validFor: /^[a-zA-Z0-9_]$/
      };
    });
  };
}

/* A docstring on hover, when the caller can supply one — tutorial-runtime.js
 * wires this to a real, running Pyodide interpreter (a name's actual
 * `inspect.getdoc()`, not bundled documentation, now covering builtins too)
 * with a Jedi static-analysis fallback for a name that has not been executed
 * anywhere yet (planning/CELL_TOOLTIPS.md); the authoring editor has none to
 * offer and passes nothing, which is why this degrades to no extension at
 * all rather than an empty tooltip. `getDoc` is async — the live path
 * resolves immediately, the Jedi path is a real Pyodide call — and
 * CodeMirror's hover source accepts a Promise of a Tooltip natively, so no
 * separate async plumbing is needed here beyond `await`ing it. `getDoc` is
 * called with the hovered word plus the whole cell's source and the word's
 * own (1-indexed line, 0-indexed column) position, in Jedi's own coordinate
 * convention, so a caller that never needs the fallback can ignore the
 * extra arguments entirely — `docFor(name)` in tutorial-runtime.js does
 * exactly that before ever reaching for Jedi. */
function pythonDocTooltip(getDoc) {
  if (!getDoc) return [];
  /* hoverTooltip() returns { active, extension } rather than a plain
   * Extension — .extension is the actual StateField/ViewPlugin bundle
   * CodeMirror needs; `active` is metadata for callers tracking tooltip
   * state elsewhere, which nothing here does. */
  return hoverTooltip(async (view, pos) => {
    const { from, text, number } = view.state.doc.lineAt(pos);
    const rel = pos - from;
    let start = rel;
    let end = rel;
    while (start > 0 && /\w/.test(text[start - 1])) start--;
    while (end < text.length && /\w/.test(text[end])) end++;
    if (start === end) return null;
    const word = text.slice(start, end);
    const doc = await getDoc(word, view.state.doc.toString(), number, start);
    if (!doc) return null;
    
    return {
      pos: from + start,
      end: from + end,
      above: true,
      create() {
        const dom = document.createElement("div");
        dom.className = "cm-dewlab-doc-tooltip";
        dom.textContent = doc;
        return { dom };
      },
    };
  }).extension;
}

/* Signature help: as a student types the "(" of a call, a small tooltip
 * shows the callee's parameters, with the one under the cursor bolded
 * (planning/CELL_TOOLTIPS.md option b). Unlike pythonDocTooltip, which
 * fires on hover, this fires on typing — CodeMirror has no built-in
 * trigger-on-character mechanism the way hoverTooltip triggers on the
 * pointer, so it needs its own: a StateField holding the current tooltip
 * (or none), kept in sync by a ViewPlugin that recomputes on every
 * document or selection change. */

const setSignatureTooltip = StateEffect.define();

const signatureTooltipField = StateField.define({
  create: () => null,
  update(value, tr) {
    for (const effect of tr.effects) {
      if (effect.is(setSignatureTooltip)) value = effect.value;
    }
    /* A tooltip anchored to a position an edit has since invalidated is
     * cleared rather than left pointing at whatever text now sits there;
     * the ViewPlugin below computes a fresh one and re-sets it if the
     * cursor is still inside a call after the edit. */
    if (value && tr.docChanged) value = null;
    return value;
  },
  provide: (field) => showTooltip.from(field),
});

/* Scans backward from `pos` for the nearest enclosing, still-open "(" and
 * the identifier immediately before it, counting top-level commas along the
 * way to know which argument the cursor is in. Not a parser — the same
 * "close enough for a first pass" spirit docFor's own name regex already
 * uses — so a cursor inside a string or a comment that happens to contain
 * unbalanced brackets can misread; scanning is bounded to the last 4000
 * characters for safety, more than any dewlab cell has ever needed. */
function callContextAt(doc, pos) {
  const limit = Math.max(0, pos - 4000);
  let depth = 0;
  let argIndex = 0;
  let i = pos;
  while (i > limit) {
    const ch = doc.sliceString(i - 1, i);
    if (ch === ")" || ch === "]" || ch === "}") {
      depth++;
    } else if (ch === "(" || ch === "[" || ch === "{") {
      if (depth === 0) {
        if (ch !== "(") return null; // inside [...] or {...}, not a call
        let j = i - 1;
        while (j > limit && /\s/.test(doc.sliceString(j - 1, j))) j--;
        const end = j;
        while (j > limit && /\w/.test(doc.sliceString(j - 1, j))) j--;
        const name = doc.sliceString(j, end);
        if (!/^[A-Za-z_]\w*$/.test(name)) return null;
        return { name, argIndex, openParen: i - 1 };
      }
      depth--;
    } else if (ch === "," && depth === 0) {
      argIndex++;
    }
    i--;
  }
  return null;
}

/* Bolds the argIndex-th top-level parameter in a signature string such as
 * "average(numbers, weights=None)" or "len(obj: Sized, /) -> int" — split
 * only the parameters between the *matching* parens, so a default value or
 * type hint containing its own brackets or commas is not split apart. */
function highlightParam(sigText, argIndex) {
  const open = sigText.indexOf("(");
  if (open === -1) return document.createTextNode(sigText);
  let depth = 0;
  let close = -1;
  for (let i = open; i < sigText.length; i++) {
    if (sigText[i] === "(") depth++;
    else if (sigText[i] === ")") {
      depth--;
      if (depth === 0) {
        close = i;
        break;
      }
    }
  }
  if (close === -1) return document.createTextNode(sigText);

  const inner = sigText.slice(open + 1, close);
  const parts = [];
  let innerDepth = 0;
  let start = 0;
  for (let i = 0; i < inner.length; i++) {
    const ch = inner[i];
    if (ch === "(" || ch === "[" || ch === "{") innerDepth++;
    else if (ch === ")" || ch === "]" || ch === "}") innerDepth--;
    else if (ch === "," && innerDepth === 0) {
      parts.push(inner.slice(start, i));
      start = i + 1;
    }
  }
  parts.push(inner.slice(start));

  const frag = document.createDocumentFragment();
  frag.appendChild(document.createTextNode(sigText.slice(0, open + 1)));
  parts.forEach((part, index) => {
    if (index === argIndex) {
      /* Bold only the parameter's own text, not the space `inspect`/Jedi
       * both put after a comma — "second", not " second". */
      const leading = part.match(/^\s*/)[0];
      const trimmed = part.slice(leading.length);
      if (leading) frag.appendChild(document.createTextNode(leading));
      const strong = document.createElement("strong");
      strong.textContent = trimmed;
      frag.appendChild(strong);
    } else {
      frag.appendChild(document.createTextNode(part));
    }
    if (index < parts.length - 1) frag.appendChild(document.createTextNode(","));
  });
  frag.appendChild(document.createTextNode(sigText.slice(close)));
  return frag;
}

/* `getSignature` takes the same shape pythonDocTooltip's `getDoc` does —
 * (name, wholeSource, line, col) — plus the argument index the cursor sits
 * in, so a live-interpreter lookup can ignore the position entirely and a
 * Jedi fallback has everything it needs. Returns a plain signature string
 * or a falsy value; this file owns turning that into a bolded tooltip. */
function pythonSignatureHelp(getSignature) {
  if (!getSignature) return [];
  let debounceTimer = null;
  const plugin = ViewPlugin.fromClass(
    class {
      constructor() {
        this.lastKey = null;
      }
      update(update) {
        if (!update.docChanged && !update.selectionSet) return;
        clearTimeout(debounceTimer);
        const view = update.view;
        debounceTimer = setTimeout(() => this.recompute(view), 40);
      }
      destroy() {
        clearTimeout(debounceTimer);
      }
      async recompute(view) {
        const pos = view.state.selection.main.head;
        const ctx = callContextAt(view.state.doc, pos);
        const key = ctx ? `${ctx.name}:${ctx.argIndex}:${ctx.openParen}` : null;
        if (key === this.lastKey) return;
        this.lastKey = key;
        if (!ctx) {
          view.dispatch({ effects: setSignatureTooltip.of(null) });
          return;
        }
        const line = view.state.doc.lineAt(ctx.openParen + 1);
        const col = ctx.openParen + 1 - line.from;
        const sigText = await getSignature(
          ctx.name, view.state.doc.toString(), line.number, col, ctx.argIndex
        );
        /* The cursor may have moved on while that call was in flight; a
         * stale answer for a question nobody is asking any more is
         * dropped rather than applied. */
        if (this.lastKey !== key) return;
        if (!sigText) {
          view.dispatch({ effects: setSignatureTooltip.of(null) });
          return;
        }
        view.dispatch({
          effects: setSignatureTooltip.of({
            pos,
            above: true,
            create() {
              const dom = document.createElement("div");
              dom.className = "cm-dewlab-signature-tooltip";
              dom.appendChild(highlightParam(sigText, ctx.argIndex));
              return { dom };
            },
          }),
        });
      }
    }
  );
  return [signatureTooltipField, plugin];
}

/* One extension per non-Python language dewlab's cells can hold
 * (planning/CELL_IDENTITY.md §8) — each package supplies its own
 * completion source via CodeMirror's language-data mechanism, so a
 * plain autocompletion() with no override is enough to get tag/
 * attribute completion for HTML, property completion for CSS, and so
 * on, the same "free, built-in" deal Python's own syntax highlighting
 * already is. Python keeps its own richer setup (Jedi-backed hover and
 * signature help, a live namespace to complete names from) below,
 * since those genuinely need this file's own machinery, not just the
 * language package. */
const OTHER_LANGUAGES = {
  html: () => [html(), autocompletion()],
  css: () => [css(), autocompletion()],
  javascript: () => [javascript(), autocompletion()],
  sql: () => [sql(), autocompletion()],
};

export function createCodeEditor(
  parent, doc,
  { dark = false, onChange = null, completeNames = null, getDoc = null,
    getSignature = null, getJediCompletions = null, language = "python" } = {}
) {
  const themeCompartment = new Compartment();
  const isPython = language === "python";

  const extensions = [
    lineNumbers(),
    highlightActiveLineGutter(),
    highlightActiveLine(),
    highlightSpecialChars(),
    drawSelection(),
    rectangularSelection(),
    crosshairCursor(),
    history(),
    indentOnInput(),
    bracketMatching(),
    closeBrackets(),
    ...(isPython
      ? [pythonCompletion(completeNames, getJediCompletions), pythonDocTooltip(getDoc),
         pythonSignatureHelp(getSignature), indentUnit.of("    "), python()]
      : OTHER_LANGUAGES[language]()),
    /* Find and replace (Ctrl/Cmd+F), and a highlight on every other
     * occurrence of whatever is selected. CodeMirror has always supported
     * both; dewmini had never wired them up, which stops mattering the
     * moment a notebook grows past a screen of code. `top: true` puts the
     * panel above the editor rather than below it — below, it would sit
     * over the cell's own output. */
    search({ top: true }),
    highlightSelectionMatches(),
    /* indentWithTab last so Tab indents inside a cell rather than tabbing the
     * browser out of it — with Escape still available to leave, which is what
     * keeps the page keyboard-navigable. completionKeymap ahead of it: Enter
     * and Tab both need to accept an open completion before either falls
     * through to a newline or an indent. */
    keymap.of([...closeBracketsKeymap, ...completionKeymap,
               ...searchKeymap, ...defaultKeymap, ...historyKeymap, indentWithTab]),
    themeCompartment.of(themeOf(dark)),
    /* After the theme compartment, so dewlab's transparent background wins
     * over one-dark's own and the cell panel colour shows through in both
     * themes. Syntax colours still come from the theme. */
    baseTheme,
    EditorView.lineWrapping,
  ];

  if (onChange) {
    extensions.push(
      EditorView.updateListener.of((update) => {
        if (update.docChanged) onChange(update.state.doc.toString());
      })
    );
  }

  const view = new EditorView({
    parent,
    state: EditorState.create({ doc, extensions }),
  });
  view._dewlabTheme = themeCompartment;

  return {
    view,
    getValue: () => view.state.doc.toString(),
    setValue: (text) =>
      view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } }),
    focus: () => view.focus(),
    destroy: () => view.destroy(),
  };
}

export function setEditorTheme(editor, dark) {
  const view = editor.view;
  view.dispatch({ effects: view._dewlabTheme.reconfigure(themeOf(dark)) });
}

/* Illustrative code — an untagged fence — gets the same highlighting as a live
 * cell, from the same theme, so the two never drift apart visually. It is not
 * an editor: no gutter, no cursor, no history, and the document cannot change.
 */
export function createReadOnlyCode(parent, doc, { dark = false, language = "python" } = {}) {
  const themeCompartment = new Compartment();
  const view = new EditorView({
    parent,
    state: EditorState.create({
      doc,
      extensions: [
        EditorState.readOnly.of(true),
        EditorView.editable.of(false),
        highlightSpecialChars(),
        ...(language === "python" ? [python()] : []),
        themeCompartment.of(themeOf(dark)),
        baseTheme,
        EditorView.lineWrapping,
      ],
    }),
  });
  view._dewlabTheme = themeCompartment;
  /* Same shape as createCodeEditor's return, so setEditorTheme works on both
   * and the texture panel does not need to know which kind it is holding. */
  return { view, destroy: () => view.destroy() };
}
