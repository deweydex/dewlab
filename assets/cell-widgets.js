/* The page's half of a cell's widgets, shared by tutorial pages
 * (tutorial-runtime.js) and the Notebook (pyodide-engine.js), so both
 * behave the same (#329; 7.264, 7.268).
 *
 * Python never reads a widget's element. Before each run the page reads
 * what every text box, menu and slider of the cell holds and hands those
 * values in (`widgetValues()`), which works the same whether Python runs
 * in a Worker or on the page's own thread.
 *
 * A slider runs its own cell again when it moves, and a run clears the
 * output, which would take the thumb from under the reader's pointer
 * halfway through a drag. So after each run `reconcileSliders()` moves a
 * new slider up into the cell's strip, a row just above the output that
 * no run clears, and drops the copy of one already there. `holder` is
 * whatever object the caller keeps per cell; this file keeps its state on
 * it (`sliderStrip`, `sliderPending`, `sliderFollowing`). */

const RANGE = 'input[type="range"]';

/* A control's DOM id is `dl-w-<cellId>-<widgetId>`; the cell id is known,
 * so the widget id is whatever follows. */
function widgetIdOf(cellId, control) {
  const prefix = `dl-w-${cellId}-`;
  return control.id.startsWith(prefix) ? control.id.slice(prefix.length) : null;
}

/* Every text box, menu and slider value the cell's widgets hold, as
 * [{widgetId, value}]. Read before the run clears the output. */
export function widgetValues(holder, cellId, outputEl) {
  const roots = [holder.sliderStrip, outputEl].filter(Boolean);
  const values = [];
  for (const root of roots) {
    for (const control of root.querySelectorAll('.dl-widget input:not([type="file"]), .dl-widget select')) {
      const widgetId = widgetIdOf(cellId, control);
      if (widgetId) values.push({ widgetId, value: control.value });
    }
  }
  return values;
}

function sliderStrip(holder, outputEl) {
  if (!holder.sliderStrip) {
    holder.sliderStrip = document.createElement("div");
    holder.sliderStrip.className = "dl-slider-strip";
  }
  /* A page that redraws its cells (the Notebook) may have given the cell
   * a new output element; the strip follows it, sliders and all. */
  if (holder.sliderStrip.nextElementSibling !== outputEl) outputEl.before(holder.sliderStrip);
  return holder.sliderStrip;
}

function showSliderValue(widget) {
  const control = widget.querySelector(RANGE);
  const shown = widget.querySelector("output");
  if (shown) shown.textContent = control.value;
  /* The attribute, not only the property, so saved HTML carries where
   * the thumb was. */
  control.setAttribute("value", control.value);
}

function wireSlider(widget, onMove) {
  const control = widget.querySelector(RANGE);
  if (!control) return;
  control.addEventListener("input", () => {
    showSliderValue(widget);
    onMove();
  });
}

/* After a run: move new sliders up into the strip, keep the ones already
 * there, and remove any the run did not make. */
export function reconcileSliders(holder, outputEl, onMove) {
  if (holder.sliderStrip) sliderStrip(holder, outputEl);
  const kept = new Map();
  if (holder.sliderStrip) {
    for (const widget of holder.sliderStrip.querySelectorAll(".dl-slider")) {
      kept.set(widget.querySelector(RANGE).id, widget);
    }
  }
  const seen = new Set();
  for (const widget of [...outputEl.querySelectorAll(".dl-slider")]) {
    const fresh = widget.querySelector(RANGE);
    seen.add(fresh.id);
    const old = kept.get(fresh.id);
    if (!old) {
      sliderStrip(holder, outputEl).appendChild(widget);
      wireSlider(widget, onMove);
      continue;
    }
    /* Edited code may have changed the ends, the step or the label. The
     * value stays where the reader left it: it went in before this run. */
    const control = old.querySelector(RANGE);
    for (const name of ["min", "max", "step"]) control.setAttribute(name, fresh.getAttribute(name));
    const label = old.querySelector("label");
    const freshLabel = widget.querySelector("label");
    if (label && freshLabel) label.textContent = freshLabel.textContent;
    showSliderValue(old);
    widget.remove();
  }
  for (const [id, widget] of kept) if (!seen.has(id)) widget.remove();
}

/* Reset, Clear and "start again" empty the strip along with the output. */
export function clearSliders(holder) {
  if (holder.sliderStrip) holder.sliderStrip.replaceChildren();
}

export function sliderMarkup(holder) {
  return holder.sliderStrip?.childElementCount ? holder.sliderStrip.innerHTML : "";
}

export function restoreSliders(holder, outputEl, markup, onMove) {
  if (typeof markup !== "string" || !markup) return;
  const strip = sliderStrip(holder, outputEl);
  strip.innerHTML = markup;
  for (const widget of strip.querySelectorAll(".dl-slider")) wireSlider(widget, onMove);
}

/* At most one run in flight. A drag fires `input` far faster than a cell
 * that draws a plot can run, so each run takes wherever the thumb is when
 * it starts, and one more runs after the last move. `isBusy()` says
 * whether any cell is running; `run()` runs this one. */
export function followSlider(holder, isBusy, run) {
  holder.sliderPending = true;
  if (holder.sliderFollowing) return;
  holder.sliderFollowing = (async () => {
    try {
      while (holder.sliderPending) {
        if (isBusy()) {
          await new Promise((resolve) => setTimeout(resolve, 50));
          continue;
        }
        holder.sliderPending = false;
        await run();
      }
    } finally {
      holder.sliderFollowing = null;
    }
  })();
}
