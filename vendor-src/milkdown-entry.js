import { Crepe } from "@milkdown/crepe";
import { editorViewCtx } from "@milkdown/core";

/* The in-page editor (assets/inpage-edit.js): Crepe as one block of a page that
 * is being edited where it stands. Every feature that draws its own markup is
 * off, and Crepe's stylesheet is not imported, so the page's own styles reach
 * the editor's paragraphs and headings. */
const IN_PLACE_FEATURES = {
  [Crepe.Feature.ImageBlock]: false,
  [Crepe.Feature.Toolbar]: false,
  [Crepe.Feature.TopBar]: false,
  [Crepe.Feature.AI]: false,
  [Crepe.Feature.BlockEdit]: false,
  [Crepe.Feature.ListItem]: false,
  [Crepe.Feature.CodeMirror]: false,
  [Crepe.Feature.Latex]: false,
  [Crepe.Feature.Table]: false,
};

export function createInPlaceEditor(parent, doc, { onChange = null } = {}) {
  const crepe = new Crepe({ root: parent, defaultValue: doc || "", features: IN_PLACE_FEATURES });
  let hydrated = false;
  if (onChange) {
    crepe.on((listener) => {
      listener.markdownUpdated((_ctx, markdown) => {
        if (hydrated) onChange(markdown);
      });
    });
  }
  const ready = crepe.create().then(() => { hydrated = true; });
  return {
    ready,
    getMarkdown: () => crepe.getMarkdown(),
    setEditable: (editable) => crepe.setReadonly(!editable),
    focus: () => crepe.editor.action((ctx) => ctx.get(editorViewCtx).focus()),
    destroy: () => crepe.destroy(),
  };
}
