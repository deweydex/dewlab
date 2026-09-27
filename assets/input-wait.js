/* input() on a page: Python waits while the reader types.
 *
 * Python runs in a Worker, and input() has to return a line before the
 * next statement can run, so the Worker blocks. It cannot receive a
 * message while it is blocked, so the line comes back through a small
 * SharedArrayBuffer instead: the Worker asks, then waits on the buffer
 * (waitForLine()); the page shows a box in the cell's output (askInOutput())
 * and writes the line into the buffer when the reader presses Enter
 * (answerLine()). Stop ends the wait (endLine()). SharedArrayBuffer needs
 * the page to be cross-origin isolated, which the Stop button already needs
 * too (coi-serviceworker, DECISIONS_LOG 7.77).
 *
 * The buffer: two Int32s, the state and the line's length in bytes, then
 * the line as UTF-8. */

const WAITING = 1;
const ANSWERED = 2;
const ENDED = 3;
const HEADER_BYTES = 8;
const LINE_BYTES = 16 * 1024;

/* What the box and a main-thread dialog say when input() has no prompt. */
export const NO_PROMPT = "Type a line for input()";

export function createInputBuffer() {
  return new SharedArrayBuffer(HEADER_BYTES + LINE_BYTES);
}

/* In the Worker: ask, then block until the page answers or ends the wait.
 * `checkInterrupt` is Pyodide's own, so a Stop pressed while waiting
 * raises KeyboardInterrupt in Python, as it would anywhere else. Returns
 * the line, or undefined for the end of the input. */
export function waitForLine(buffer, ask, checkInterrupt) {
  const state = new Int32Array(buffer, 0, 2);
  Atomics.store(state, 0, WAITING);
  ask();
  while (Atomics.load(state, 0) === WAITING) {
    Atomics.wait(state, 0, WAITING, 100);
    checkInterrupt();
  }
  checkInterrupt();
  if (Atomics.load(state, 0) !== ANSWERED) return undefined;
  /* TextDecoder refuses a view of shared memory, so copy the bytes out. */
  return new TextDecoder().decode(new Uint8Array(buffer, HEADER_BYTES, state[1]).slice());
}

/* On the page: hand the Worker the line the reader typed. */
export function answerLine(buffer, text) {
  const state = new Int32Array(buffer, 0, 2);
  /* TextEncoder refuses to write into shared memory, so encode, then copy.
   * A line longer than the buffer is cut, which may split one character. */
  const bytes = new TextEncoder().encode(text).subarray(0, LINE_BYTES);
  new Uint8Array(buffer, HEADER_BYTES).set(bytes);
  state[1] = bytes.length;
  Atomics.store(state, 0, ANSWERED);
  Atomics.notify(state, 0);
}

/* On the page: whether the Worker is still waiting. A Stop can end the
 * wait after the Worker asked and before the page has read the request,
 * and a box drawn then would belong to a run that has already stopped. */
export function stillWaiting(buffer) {
  return Atomics.load(new Int32Array(buffer, 0, 2), 0) === WAITING;
}

/* On the page: stop a wait with no line, as Stop and Restart do. */
export function endLine(buffer) {
  const state = new Int32Array(buffer, 0, 2);
  if (Atomics.load(state, 0) !== WAITING) return;
  Atomics.store(state, 0, ENDED);
  Atomics.notify(state, 0);
}

/* A text box where the cell's output has got to: inside its printed text,
 * straight after the prompt, the way a terminal shows it. `open` is the
 * page's record ({el, cssClass}) of the <pre> printed text is going into,
 * or undefined; the stream returned is the one the typed line continues,
 * a new <pre> when there was none. Enter removes the box and calls
 * `onEnter` with what was typed. Python prints the line itself after the
 * prompt, so the output keeps a record of it. */
export function askInOutput(outputEl, open, prompt, onEnter) {
  let stream = open && open.cssClass === "dl-stdout" && outputEl.contains(open.el) ? open : null;
  if (!stream) {
    const pre = document.createElement("pre");
    pre.className = "dl-stdout";
    outputEl.appendChild(pre);
    stream = { el: pre, cssClass: "dl-stdout" };
  }
  const box = document.createElement("input");
  box.type = "text";
  box.className = "dl-stdin";
  box.autocomplete = "off";
  box.spellcheck = false;
  box.setAttribute("autocapitalize", "off");
  box.setAttribute("aria-label", prompt.trim() || NO_PROMPT);
  box.addEventListener("keydown", (ev) => {
    if (ev.key !== "Enter" || ev.isComposing) return;
    ev.preventDefault();
    const text = box.value;
    box.remove();
    onEnter(text);
  });
  stream.el.appendChild(box);
  box.focus();
  return { stream, box };
}

/* Where there is no Worker (a downloaded page, or the Notebook when its
 * Worker could not start), Python runs on the page's own thread, and the
 * browser's own dialog is the one thing that can wait there. Cancel is the
 * end of the input, so input() raises EOFError. */
export function askInDialog(prompt) {
  const line = globalThis.prompt(prompt.trim() || NO_PROMPT);
  return line === null ? undefined : line;
}
