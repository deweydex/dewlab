import { Crepe } from "@milkdown/crepe";
/* Experimental: Crepe as an in-place editor, with the parts that draw their
 * own furniture switched off, so the page's own styles apply to its elements. */
export function createInPlaceEditor(parent, doc, off = []) {
  const features = {
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
  for (const name of off) features[Crepe.Feature[name]] = false;
  const crepe = new Crepe({ root: parent, defaultValue: doc || "", features });
  const ready = crepe.create();
  return { ready, getMarkdown: () => crepe.getMarkdown(), destroy: () => crepe.destroy(), crepe };
}
export { Crepe };
