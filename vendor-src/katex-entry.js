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
