/* dewmini's JavaScript cell engine (DECISIONS_LOG.md 7.119,
 * planning/CELL_IDENTITY.md §8) — one persistent sandboxed iframe
 * standing in for the whole notebook's shared JS session, the way
 * assets/pyodide-engine.js is for Python. Created lazily on first run
 * (ensureSession()) and torn down and recreated on Restart Python
 * (restart(), called from compose/dewmini.js's own restartPython())
 * exactly the way the Pyodide interpreter itself is.
 *
 * sandbox="allow-scripts", no allow-same-origin — the same isolation
 * dewmini.js's own HTML cell preview already uses: whatever a cell's
 * code does, it does inside an opaque-origin document that cannot reach
 * this page's own DOM, localStorage, or any other cell. Unlike HTML's
 * preview iframe, this one is never shown — it is a headless execution
 * session, and its own output is relayed back into a cell's ordinary
 * `.dm-cell-output` area (via applyOutputEvent, imported from
 * assets/pyodide-engine.js) the same way Python's output already is.
 *
 * No Worker, unlike Python: a sandboxed iframe with no allow-same-origin
 * is already a separate realm with no shared memory to this page, so
 * there is no interpreter boundary left for a Worker to add, and every
 * browser already has a JS engine (nothing to download). What a Worker
 * buys Python — a genuine Stop button, via a shared interrupt buffer —
 * has no equivalent here: this iframe still executes on the tab's own
 * main thread, so a runaway cell's loop freezes the page exactly the way
 * Pyodide's own main-thread fallback does. canStop() below is always
 * false for that reason, not because it was left unfinished.
 *
 * Persistence across cells, and why `let`/`const` don't get it. Each
 * cell's code runs through indirect eval — `(0, eval)(code)`, called
 * from the iframe's own top level — rather than through a `<script>`
 * tag inserted fresh for each run. That choice is deliberate: a
 * `<script>` tag's own top-level `let`/`const` declarations join the
 * realm's single, permanent global lexical environment, so re-running an
 * edited cell a second time — an entirely ordinary thing to do — would
 * throw "Identifier has already been declared" the moment it tried to
 * redeclare its own `let`. Indirect eval's top-level `let`/`const`
 * bindings live in a fresh scope private to that one eval() call
 * instead, so a cell can always be re-run safely, at the cost of those
 * bindings not being visible to a *later* cell either — only `var` and
 * `function` declarations, which indirect eval still attaches to the
 * real global object exactly like a `<script>` tag would, persist across
 * cells the way a Python cell's own names do. A real fix (parsing each
 * cell to hoist top-level `let`/`const` onto the shared session by hand)
 * would need an actual JS parser vendored in for it — out of scope here,
 * the same way SQL's own multi-statement split is a plain string split
 * rather than a real SQL parser.
 *
 * Top-level `await` is not supported for the same reason async output
 * generally isn't: indirect eval runs as an ordinary classic script, and
 * wrapping a cell's code in an async function to allow it would swallow
 * its own top-level `var`/`function` declarations into that function's
 * scope instead of the global one, losing the one form of persistence
 * this file *does* support. A cell can still use `async function`/
 * `.then()` internally; `console.log`/an uncaught rejection from that
 * async work still reports into the cell's output whenever it actually
 * happens, just after "done" has already fired for the run that started
 * it — the same "output can still arrive late" shape a slow Python cell
 * running inside a batch does not have to worry about, since Python's
 * own run genuinely stays pending until the code finishes.
 */

import { applyOutputEvent, clearOutput } from "../assets/pyodide-engine.js";

let frame = null; // the sandboxed <iframe> itself, once created
let readyPromise = null; // resolves once the iframe's own runtime script has loaded
let pendingRun = null; // { cellId, resolve } for the one cell currently running, if any

/* Runs inside the sandboxed iframe, not this page — read this as a
 * small, separate program. It owns: relaying console.log() calls and
 * uncaught errors back to the parent as this cell's output, and running
 * a cell's code via indirect eval on a "run" message. Plain ES5-ish
 * syntax throughout on purpose — this is embedded as a string, not
 * bundled, so it gets none of the vendor build's own transpilation. */
const RUNTIME_SRC = `<!doctype html>
<html><head></head><body><script>
(function () {
  var parentWindow = window.parent;
  var currentCellId = null;

  function send(msg) { parentWindow.postMessage(msg, "*"); }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // Mirrors Python's own print(): each argument turned into readable
  // text, joined with a single space — a string passes through as-is,
  // an object gets a short JSON rendering rather than "[object Object]".
  function formatArg(v) {
    if (typeof v === "string") return v;
    if (v === undefined) return "undefined";
    if (v === null) return "null";
    if (typeof v === "function") return "[Function" + (v.name ? ": " + v.name : "") + "]";
    if (typeof v === "bigint") return v.toString() + "n";
    if (v instanceof Error) return v.name + ": " + v.message;
    try {
      return JSON.stringify(v, null, 2);
    } catch (e) {
      return String(v);
    }
  }

  var realLog = console.log.bind(console);
  console.log = function () {
    var args = Array.prototype.slice.call(arguments);
    realLog.apply(console, args);
    if (currentCellId) {
      send({
        type: "output", cellId: currentCellId, kind: "stream", cssClass: "dl-stdout",
        text: args.map(formatArg).join(" ") + "\\n"
      });
    }
  };

  function reportError(err) {
    if (!currentCellId) return;
    var message = (err && err.name) ? (err.name + ": " + err.message) : String(err);
    send({
      type: "output", cellId: currentCellId, kind: "append",
      markup: '<pre class="dl-error">' + escapeHtml(message) + "<\\/pre>"
    });
  }

  // Only for a rejection nothing inside the cell's own code caught —
  // synchronous errors are caught around eval() itself, below, and
  // reported (with an accurate "ok") as part of that same run.
  window.addEventListener("unhandledrejection", function (ev) {
    reportError(ev.reason);
    ev.preventDefault();
  });

  window.addEventListener("message", function (ev) {
    if (ev.source !== parentWindow) return;
    var msg = ev.data;
    if (!msg || msg.type !== "run") return;
    currentCellId = msg.cellId;
    var ok = true;
    try {
      (0, eval)(msg.code);
    } catch (err) {
      ok = false;
      reportError(err);
    }
    send({ type: "done", cellId: msg.cellId, ok: ok });
  });

  send({ type: "ready" });
})();
<\/script></body></html>`;

function handleMessage(ev) {
  if (!frame || ev.source !== frame.contentWindow) return;
  const msg = ev.data;
  if (!msg) return;
  if (msg.type === "output") {
    applyOutputEvent(msg.cellId, msg.kind, msg.cssClass, msg.text, msg.markup);
  } else if (msg.type === "done" && pendingRun && pendingRun.cellId === msg.cellId) {
    const { resolve } = pendingRun;
    pendingRun = null;
    resolve({ ok: msg.ok });
  }
}

/* Creates the session iframe the first time a JS cell actually runs, and
 * does nothing on later calls (readyPromise memoizes it, the same
 * pattern engine.ensureBooted() uses for Pyodide). Never shown —
 * `display: none` — this is a headless execution session, not a preview
 * the way an HTML cell's own sandboxed iframe is. */
export function ensureSession() {
  if (readyPromise) return readyPromise;
  frame = document.createElement("iframe");
  frame.setAttribute("sandbox", "allow-scripts");
  frame.setAttribute("aria-hidden", "true");
  frame.style.display = "none";
  frame.srcdoc = RUNTIME_SRC;
  document.body.appendChild(frame);
  window.addEventListener("message", handleMessage);
  readyPromise = new Promise((resolve) => {
    const onReady = (ev) => {
      if (ev.source === frame.contentWindow && ev.data?.type === "ready") {
        window.removeEventListener("message", onReady);
        resolve();
      }
    };
    window.addEventListener("message", onReady);
  });
  return readyPromise;
}

/* Whether the session iframe has been created at all — read by
 * compose/dewmini.js to decide whether "JavaScript ready." is worth
 * announcing the way "Python ready." is the first time Pyodide boots. */
export function sessionReady() {
  return frame !== null;
}

/* Runs one cell's code in the session iframe and waits for it to finish
 * — the JS counterpart of engine.runCell(). clearOutput() first, same as
 * a Python cell's own run_cell() clears its output the moment it starts
 * (_begin()'s sink.clear()), so a re-run replaces what's there rather
 * than appending underneath it. */
export async function runCell(cellId, code) {
  await ensureSession();
  clearOutput(cellId);
  return new Promise((resolve) => {
    pendingRun = { cellId, resolve };
    frame.contentWindow.postMessage({ type: "run", cellId, code }, "*");
  });
}

/* Always false — see the file banner above for why a same-thread
 * sandboxed iframe has no genuine way to interrupt a running cell, the
 * same limitation Pyodide's own main-thread fallback has. Exists so
 * compose/dewmini.js can ask either engine the same question without a
 * special case for this one. */
export function canStop() {
  return false;
}

/* A no-op paired with canStop() always being false above — nothing ever
 * calls this expecting it to do anything, but compose/dewmini.js's own
 * runCell() dispatches to it unconditionally rather than checking cell
 * type twice. */
export function requestInterrupt() {}

/* Tears the session down entirely — the JS counterpart of
 * engine.restart(). A pending run (there should never really be one:
 * restart() is only ever called between runs, not during one) resolves
 * as failed rather than hanging forever, the same reasoning
 * engine.restart() itself gives for rejecting what was in flight. */
export function restart() {
  if (frame) {
    window.removeEventListener("message", handleMessage);
    frame.remove();
  }
  frame = null;
  readyPromise = null;
  if (pendingRun) {
    const { resolve } = pendingRun;
    pendingRun = null;
    resolve({ ok: false });
  }
}
