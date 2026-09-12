
import { applyOutputEvent, clearOutput } from "../assets/pyodide-engine.js";

let frame = null; // the sandboxed <iframe> itself, once created
let readyPromise = null; // resolves once the iframe's own runtime script has loaded
let pendingRun = null; // { cellId, resolve } for the one cell currently running, if any

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

export function sessionReady() {
  return frame !== null;
}

export async function runCell(cellId, code) {
  await ensureSession();
  clearOutput(cellId);
  return new Promise((resolve) => {
    pendingRun = { cellId, resolve };
    frame.contentWindow.postMessage({ type: "run", cellId, code }, "*");
  });
}

export function canStop() {
  return false;
}

export function requestInterrupt() {}

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
