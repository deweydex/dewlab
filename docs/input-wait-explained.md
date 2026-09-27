# `assets/input-wait.js`, explained

This small module is how `input()` waits for the reader. It has two
halves that never run in the same place: one runs inside the Web Worker
where Python lives (`assets/pyodide-worker.js`), and the other on the
page, in both `assets/tutorial-runtime.js` and `assets/pyodide-engine.js`
(the Notebook). Both import it, so the two ends of the conversation are
written once, side by side.

---

## The big idea: a thread that is waiting cannot read a message

Everything else between the page and the Worker travels as a message.
`input()` cannot work that way. It has to return a line before the next
line of the program runs, so the Worker's thread stops and waits, and a
waiting thread never gets to read the page's messages. The line comes
back through shared memory instead: a small `SharedArrayBuffer` both
threads can see, the same kind of memory the Stop button already uses.
That is also why it needs the same thing Stop needs: a cross-origin
isolated page, which `coi-serviceworker` arranges on the hosted site.

Python's side is in `tutorial_tools.py`: `_Stdin`, which `_begin()` puts
in place of `sys.stdin` for each run, asks whatever function the engine
set with `_set_live_reader()`. In the Worker, that function is
`readLine()`, which calls `waitForLine()` here.

---

## Reading order

1. **The constants** — the buffer's three states (`WAITING`, `ANSWERED`,
   `ENDED`) and its layout: two 32-bit numbers, the state and the line's
   length in bytes, then the line itself as UTF-8. `NO_PROMPT` is what the
   box and the dialog say when `input()` was called with no prompt.
2. **`createInputBuffer()`** — the page makes one per Worker, in its
   `bootWorker()`, and posts it as `"set-input-buffer"`.
3. **`waitForLine()`** — the Worker's half. It marks the buffer
   `WAITING`, asks the page (posting `"input-request"`), then sleeps on
   the buffer with `Atomics.wait()`, a tenth of a second at a time,
   calling Pyodide's `checkInterrupt()` between sleeps and once more at the
   end. It returns the line, or `undefined` for the end of the input.
4. **`answerLine()`**, **`endLine()`** and **`stillWaiting()`** — the
   page's half of the buffer. `answerLine()` writes the line and wakes the
   Worker; `endLine()` wakes it with no line, which Stop and Restart use.
   `stillWaiting()` lets the page skip drawing a box when a Stop has
   already ended the wait before the page read the request.
5. **`askInOutput()`** — the box. It goes inside the cell's open `<pre>`
   of printed text, straight after the prompt, the way a terminal shows
   it, or in a new `<pre>` when nothing is open. Enter removes it and
   hands the page the line. Python then prints the line after the prompt
   itself, so the output keeps a record of what was typed.
6. **`askInDialog()`** — where Python runs on the page's own thread (a
   downloaded page, or the Notebook when its Worker could not start),
   nothing on the page can draw a box while Python waits, so the browser's
   own dialog asks instead. Cancel is the end of the input.

---

## Two patterns worth understanding on their own

**Stop while waiting.** A Stop press does two things, in this order: it
sets the interrupt buffer, then ends the wait (`endLine()`). The Worker
wakes, and `waitForLine()` calls `checkInterrupt()` before it returns, so
Python gets a `KeyboardInterrupt` at the `input()` call, and the cell says
"Stopped." as it would for any loop. If the order were the other way
round, `input()` could return first and the program would carry on for a
moment with no line.

**Shared memory and text.** `TextEncoder.encodeInto()` refuses to write
into shared memory, and `TextDecoder.decode()` refuses to read from it,
so each side copies: `answerLine()` encodes into ordinary memory and then
copies the bytes in; `waitForLine()` copies the bytes out before it
decodes them. A line longer than the buffer (16 KB) is cut, which may
split its last character.

---

## Where to look for something specific

- **"Why does `input()` say this browser has not let the page wait?"** —
  the page is not cross-origin isolated, so it never sent an input buffer,
  and `tutorial_tools._Stdin` has no reader. The same condition turns off
  Stop (`canStop()`).
- **"Why doesn't the comparison ask me to type?"** — it never waits:
  `tutorial_tools.compare()` reads the cell's ```` ```typed ```` lines
  instead ([`WRITING_TUTORIALS.md`](WRITING_TUTORIALS.md#typed)).
- **"Where is the box styled?"** — `input.dl-stdin` in
  `assets/tutorial-style.css`, which both the tutorial pages and the
  Notebook load.
