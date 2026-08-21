/* KaTeX, bundled as one ES module the runtime imports only when a page
 * actually contains maths.
 *
 * build.py marks every maths span it finds and records `math: true` in the
 * manifest; a tutorial with no maths never fetches this file. The auto-render
 * contrib script is deliberately not used — the build already knows exactly
 * which elements are maths and what TeX each one holds, so there is nothing
 * for a delimiter scan to find that we do not already know.
 */
import katex from "katex";

export function renderMath(element, tex, displayMode) {
  try {
    katex.render(tex, element, { displayMode, throwOnError: false, output: "html" });
    return true;
  } catch (error) {
    /* Leave the source TeX visible rather than an empty gap: a reader can
     * still see what was meant, and the author can see what broke. */
    element.classList.add("dl-math-error");
    element.title = String(error && error.message ? error.message : error);
    return false;
  }
}
