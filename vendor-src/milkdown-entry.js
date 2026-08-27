/* Milkdown's Crepe preset, wrapped as one function the authoring editor calls
 * to get a live block-based prose surface — the block editor
 * planning/REPO_AND_EDITOR.md specified for editor v1 and assets/editor.js
 * never actually got, a bare <textarea> in its place.
 *
 * Crepe's own API is framework-agnostic (it is not a React or Preact
 * component — FAQ only wraps it in one because FAQ itself is a Preact app),
 * so this needs nothing beyond what CodeMirror already needed here: an
 * npm package, bundled once by esbuild and committed, so neither CI nor an
 * author previewing locally needs Node.
 *
 * Only the structural stylesheet is imported, not Crepe's "classic" skin —
 * the skin is a fixed light-mode colour scheme, and dewlab's own CSS
 * (tutorial-style.css, ".dl-editor-body") retextures the same elements from
 * dewlab's --dl-* variables so the editor follows the reader's theme like
 * everything else on the page.
 */
import { Crepe } from "@milkdown/crepe";
import "@milkdown/crepe/theme/common/style.css";
import { keymap } from "@codemirror/view";
import { autocompletion, completionKeymap } from "@codemirror/autocomplete";
import { localCompletionSource, globalCompletion } from "@codemirror/lang-python";

/* A hover-docstring tooltip for `module.name` (plt.plot, pd.DataFrame, …),
 * reading dev/generate_doc_snippets.py's output — assets/editor-doc-snippets.js,
 * real docstrings captured once from a real Pyodide — was attempted here and
 * pulled back out. Wired the same way as pythonCompletion below, using
 * CodeMirrorFeatureConfig's `extensions`, it compiled and ran with no error,
 * but Crepe's code-block CodeMirror instance never actually surfaced it: no
 * tooltip ever appeared, in an author's own hover or in a Playwright-driven
 * one, despite the underlying mousemove event demonstrably reaching the
 * editor's DOM node. The identical hoverTooltip() wiring works correctly in
 * tutorial-runtime.js's own cells (vendor-src/codemirror-entry.js,
 * tests/e2e/test_autocomplete.py's TestHoverDocs) — Crepe's own code-block
 * feature is doing something to the ones it hosts that autocompletion()
 * (confirmed working here) does not run into. Not chased further; the
 * generator script and its output are real and kept, ready for whoever
 * next has a lead on the Crepe side. See DECISIONS_LOG.md for the fuller
 * account and what would need to be true to pick this back up. */

const FEATURES = {
  /* No image upload UI: every <img> in a tutorial needs an alt attribute
   * (build.py's IMG_RE/ALT_RE check), and a drag-and-drop image block has no
   * way to ask for one. An author adding a real image still can, by hand, in
   * a text editor — this only removes the button that would ship one build.py
   * silently rejects. */
  [Crepe.Feature.ImageBlock]: false,
  /* No floating toolbar, no top bar, no AI panel — dewlab's own status bar
   * and structural report (assets/editor.js's #dl-editor-report) already
   * cover what those would duplicate, and there is no AI key to wire up. */
  [Crepe.Feature.Toolbar]: false,
  [Crepe.Feature.TopBar]: false,
  [Crepe.Feature.AI]: false,
  /* Keyword/builtin and locally-defined-name completion inside a `python
   * exec` block, same two static sources tutorial-runtime.js's own cells
   * use (vendor-src/codemirror-entry.js) — an author gets the same
   * completion behaviour writing a cell as a student gets running it.
   * No live-namespace source here: the editor never boots Pyodide
   * (planning/EDITOR.md's own reason for not shipping a live preview
   * applies just as much to a live interpreter), so there is nothing to
   * introspect beyond the cell's own text. `override` for the same reason
   * as codemirror-entry.js: a generic word-list fallback suggests things
   * that are not valid Python. */
  [Crepe.Feature.CodeMirror]: {
    extensions: [
      autocompletion({ override: [localCompletionSource, globalCompletion], activateOnTyping: true }),
      keymap.of(completionKeymap),
    ],
  },
};

/* Crepe reads its starting document once, at construction, and has no
 * supported way to replace it in place afterward — the same constraint
 * FAQ's MilkdownEditor.jsx works around by remounting on a changed `key`
 * rather than trying to push new content into a live instance. There is no
 * setValue here for the same reason: callers that need to load different
 * content destroy this instance and create a new one, exactly as
 * assets/editor.js's render() already does whenever it rebuilds the DOM. */
export function createProseEditor(parent, doc, { onChange = null, spellcheck = true } = {}) {
  const crepe = new Crepe({ root: parent, defaultValue: doc || "", features: FEATURES });

  /* Crepe fires markdownUpdated once while it is still parsing `doc` into a
   * document — hydration, not an edit — and without this guard that first
   * firing reaches the caller as if the reader had typed something the
   * moment the page opened. Concretely: assets/editor.js's release() refuses
   * to release when nothing has changed, and every tutorial opened and left
   * untouched was tripping that refusal, because opening it already looked
   * like an edit. Ignored until `create()` below has actually resolved. */
  let hydrated = false;
  if (onChange) {
    crepe.on((listener) => {
      listener.markdownUpdated((_ctx, markdown) => {
        if (hydrated) onChange(markdown);
      });
    });
  }

  const ready = crepe.create().then(() => {
    hydrated = true;
    /* Crepe/ProseMirror expose no spellcheck option of their own; it is a
     * plain attribute on the contenteditable element underneath. */
    const editable = parent.querySelector("[contenteditable]");
    if (editable) editable.spellcheck = spellcheck;
  });

  return {
    ready,
    /* The markdown as Crepe has it right now. markdownUpdated fires a beat
     * after the keystroke that caused it (internal scheduling, not a bug),
     * so a caller that needs the true current value at a specific moment —
     * about to commit, about to release — reads it here rather than trusting
     * the last onChange it received. */
    getMarkdown: () => crepe.getMarkdown(),
    destroy: () => crepe.destroy(),
  };
}
