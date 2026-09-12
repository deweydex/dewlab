
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

function pythonCompletion(completeNames, getJediCompletions = null) {
  const sources = [completeNames, localCompletionSource, globalCompletion].filter(Boolean);
  
  // Add Jedi-based completion if available
  if (getJediCompletions) {
    sources.unshift(jediCompletionSource(getJediCompletions));
  }
  
  return autocompletion({ override: sources, activateOnTyping: true });
}

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

function pythonDocTooltip(getDoc) {
  if (!getDoc) return [];
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

const setSignatureTooltip = StateEffect.define();

const signatureTooltipField = StateField.define({
  create: () => null,
  update(value, tr) {
    for (const effect of tr.effects) {
      if (effect.is(setSignatureTooltip)) value = effect.value;
    }
    if (value && tr.docChanged) value = null;
    return value;
  },
  provide: (field) => showTooltip.from(field),
});

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

const OTHER_LANGUAGES = {
  html: () => [html(), autocompletion()],
  css: () => [css(), autocompletion()],
  javascript: () => [javascript(), autocompletion()],
  sql: () => [sql(), autocompletion()],
};

export function createCodeEditor(
  parent, doc,
  { dark = false, onChange = null, completeNames = null, getDoc = null,
    getSignature = null, getJediCompletions = null, language = "python",
    lineNumbersVisible = true, indentWidth = 4 } = {}
) {
  const themeCompartment = new Compartment();
  const lineNumbersCompartment = new Compartment();
  const indentCompartment = new Compartment();
  const isPython = language === "python";

  const extensions = [
    lineNumbersCompartment.of(lineNumbersVisible ? [lineNumbers()] : []),
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
    indentCompartment.of(indentUnit.of(" ".repeat(indentWidth))),
    ...(isPython
      ? [pythonCompletion(completeNames, getJediCompletions), pythonDocTooltip(getDoc),
         pythonSignatureHelp(getSignature), python()]
      : OTHER_LANGUAGES[language]()),
    search({ top: true }),
    highlightSelectionMatches(),
    keymap.of([...closeBracketsKeymap, ...completionKeymap,
               ...searchKeymap, ...defaultKeymap, ...historyKeymap, indentWithTab]),
    themeCompartment.of(themeOf(dark)),
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
  view._dewlabLineNumbers = lineNumbersCompartment;
  view._dewlabIndent = indentCompartment;

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

export function setLineNumbers(editor, visible) {
  const view = editor.view;
  if (!view._dewlabLineNumbers) return;
  view.dispatch({
    effects: view._dewlabLineNumbers.reconfigure(visible ? [lineNumbers()] : []),
  });
}

/* Changes how many spaces Tab inserts (and how indentOnInput reindents) in
 * an already-mounted editor — the Settings panel's "indent width" row. */
export function setIndentWidth(editor, width) {
  const view = editor.view;
  if (!view._dewlabIndent) return;
  view.dispatch({
    effects: view._dewlabIndent.reconfigure(indentUnit.of(" ".repeat(width))),
  });
}

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
