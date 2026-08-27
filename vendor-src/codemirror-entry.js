/* The slice of CodeMirror 6 a dewlab exec cell needs, bundled into one
 * classic-script-free ES module so a generated page can import it with no
 * build step of its own and no CDN round trip.
 *
 * Everything here is stock CodeMirror: line numbers, the standard Python
 * language support, and the default light / one-dark highlight pair. That is
 * what DECISIONS.md means by these affordances being free — built-in
 * extensions, not custom design work.
 */

import { EditorView, keymap, lineNumbers, highlightActiveLine,
         highlightActiveLineGutter, drawSelection, highlightSpecialChars,
         rectangularSelection, crosshairCursor, hoverTooltip } from "@codemirror/view";
import { EditorState, Compartment } from "@codemirror/state";
import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
import { python, localCompletionSource, globalCompletion } from "@codemirror/lang-python";
import { syntaxHighlighting, defaultHighlightStyle, indentOnInput,
         bracketMatching, indentUnit } from "@codemirror/language";
import { closeBrackets, closeBracketsKeymap,
         autocompletion, completionKeymap } from "@codemirror/autocomplete";
import { oneDark } from "@codemirror/theme-one-dark";

/* Theme lives in a compartment so the texture panel can swap light/dark
 * without tearing the editor down and losing what the student has typed. */
const themeOf = (dark) => (dark ? oneDark : syntaxHighlighting(defaultHighlightStyle));

const baseTheme = EditorView.theme({
  "&": { backgroundColor: "transparent" },
  ".cm-gutters": { backgroundColor: "transparent", border: "none", opacity: "0.65" },
  ".cm-activeLine, .cm-activeLineGutter": { backgroundColor: "transparent" },
});

/* Keyword/builtin completion (`print`, `for`, `len`, …) and local-name
 * completion (whatever the student has already typed in this cell) are both
 * static — no interpreter involved, so they work the instant a cell mounts,
 * before Pyodide has even started loading. `completeNames`, when the caller
 * supplies one, goes first: it is how a booted cell's own runtime namespace
 * (imported modules, names a student defined) reaches the completion list,
 * wired in from tutorial-runtime.js rather than here, since this file has no
 * idea Pyodide exists. `override` rather than adding to CodeMirror's
 * defaults on purpose — the generic any-word-on-the-page fallback suggests
 * things that are not valid Python, which is worse than fewer, correct
 * suggestions for someone meeting the language for the first time. */
function pythonCompletion(completeNames) {
  const sources = [completeNames, localCompletionSource, globalCompletion].filter(Boolean);
  return autocompletion({ override: sources, activateOnTyping: true });
}

/* A docstring on hover, when the caller can supply one — tutorial-runtime.js
 * wires this to a real, running Pyodide interpreter (a name's actual
 * `inspect.getdoc()`, not bundled documentation); the authoring editor has
 * none to offer and passes nothing, which is why this degrades to no
 * extension at all rather than an empty tooltip. `getDoc` is a plain
 * synchronous function so this stays framework-agnostic about where the
 * answer comes from — CodeMirror accepts either a Tooltip or a Promise of
 * one from a hover source, but nothing here needs the async form. */
function pythonDocTooltip(getDoc) {
  if (!getDoc) return [];
  /* hoverTooltip() returns { active, extension } rather than a plain
   * Extension — .extension is the actual StateField/ViewPlugin bundle
   * CodeMirror needs; `active` is metadata for callers tracking tooltip
   * state elsewhere, which nothing here does. */
  return hoverTooltip((view, pos) => {
    const { from, text } = view.state.doc.lineAt(pos);
    const rel = pos - from;
    let start = rel;
    let end = rel;
    while (start > 0 && /\w/.test(text[start - 1])) start--;
    while (end < text.length && /\w/.test(text[end])) end++;
    if (start === end) return null;
    const doc = getDoc(text.slice(start, end));
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

export function createCodeEditor(
  parent, doc, { dark = false, onChange = null, completeNames = null, getDoc = null } = {}
) {
  const themeCompartment = new Compartment();

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
    pythonCompletion(completeNames),
    pythonDocTooltip(getDoc),
    indentUnit.of("    "),
    python(),
    /* indentWithTab last so Tab indents inside a cell rather than tabbing the
     * browser out of it — with Escape still available to leave, which is what
     * keeps the page keyboard-navigable. completionKeymap ahead of it: Enter
     * and Tab both need to accept an open completion before either falls
     * through to a newline or an indent. */
    keymap.of([...closeBracketsKeymap, ...completionKeymap,
               ...defaultKeymap, ...historyKeymap, indentWithTab]),
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
