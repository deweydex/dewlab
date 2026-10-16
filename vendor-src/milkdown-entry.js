import { Crepe } from "@milkdown/crepe";
import "@milkdown/crepe/theme/common/style.css";
import { keymap } from "@codemirror/view";
import { autocompletion, completionKeymap } from "@codemirror/autocomplete";
import { localCompletionSource, globalCompletion } from "@codemirror/lang-python";
import { editorViewCtx, schemaCtx } from "@milkdown/core";

const FEATURES = {
  [Crepe.Feature.ImageBlock]: false,
  [Crepe.Feature.Toolbar]: false,
  [Crepe.Feature.TopBar]: false,
  [Crepe.Feature.AI]: false,
  [Crepe.Feature.CodeMirror]: {
    extensions: [
      autocompletion({ override: [localCompletionSource, globalCompletion], activateOnTyping: true }),
      keymap.of(completionKeymap),
    ],
  },
};

export function createProseEditor(parent, doc, { onChange = null, spellcheck = true } = {}) {
  const crepe = new Crepe({ root: parent, defaultValue: doc || "", features: FEATURES });

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
    getMarkdown: () => crepe.getMarkdown(),
    insertLink: (title, href) => crepe.editor.action((ctx) => {
      const view = ctx.get(editorViewCtx);
      const schema = ctx.get(schemaCtx);
      const node = schema.text(title, [schema.marks.link.create({ href })]);
      view.dispatch(view.state.tr.replaceSelectionWith(node, false).scrollIntoView());
    }),
    destroy: () => crepe.destroy(),
  };
}

/* The in-page editor (assets/inpage-edit.js): Crepe as one block of a page that
 * is being edited where it stands. Every feature that draws its own markup is
 * off, and Crepe's stylesheet is not imported (the import at the top of this
 * file is the old editor's), so the page's own styles reach the editor's
 * paragraphs and headings. See planning/IN_PAGE_EDITOR_SPIKE.md. */
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
