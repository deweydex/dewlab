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
