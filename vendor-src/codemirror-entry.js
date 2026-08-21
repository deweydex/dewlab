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
         rectangularSelection, crosshairCursor } from "@codemirror/view";
import { EditorState, Compartment } from "@codemirror/state";
import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { syntaxHighlighting, defaultHighlightStyle, indentOnInput,
         bracketMatching, indentUnit } from "@codemirror/language";
import { closeBrackets, closeBracketsKeymap } from "@codemirror/autocomplete";
import { oneDark } from "@codemirror/theme-one-dark";

/* Theme lives in a compartment so the texture panel can swap light/dark
 * without tearing the editor down and losing what the student has typed. */
const themeOf = (dark) => (dark ? oneDark : syntaxHighlighting(defaultHighlightStyle));

const baseTheme = EditorView.theme({
  "&": { backgroundColor: "transparent" },
  ".cm-gutters": { backgroundColor: "transparent", border: "none", opacity: "0.65" },
  ".cm-activeLine, .cm-activeLineGutter": { backgroundColor: "transparent" },
});

export function createCodeEditor(parent, doc, { dark = false, onChange = null } = {}) {
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
    indentUnit.of("    "),
    python(),
    /* indentWithTab last so Tab indents inside a cell rather than tabbing the
     * browser out of it — with Escape still available to leave, which is what
     * keeps the page keyboard-navigable. */
    keymap.of([...closeBracketsKeymap, ...defaultKeymap, ...historyKeymap, indentWithTab]),
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
