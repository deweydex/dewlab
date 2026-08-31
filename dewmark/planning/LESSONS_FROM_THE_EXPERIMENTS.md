# Lessons from the exam experiments

Three exam artefacts were built by hand and used (or drafted) in 2025–2026,
before dewmark existed. This document is the audit that grounds the
specifications: what each one was, what worked well enough to keep, and what
broke in ways a designed system must rule out. Where a later spec makes a
choice, the reason usually traces back to a line in this file.

The artefacts (kept outside this repository, with the other private exam
material):

1. **The HVIT database exam** (`hvit_exam_with_loader.html`, plus an
   answers variant) — a Pyodide practical for Database Methods 5N0783. Six
   tasks, 60 marks, SQLite database embedded as base64, an `exam_tools.py`
   widget library, CodeMirror cells, autosave via the File System Access
   API, a task navigator, and a print stylesheet. One self-contained page,
   though it still needed the network for Pyodide and CodeMirror CDNs.
2. **The image-space practice exam** (`5N0554_practice_exam_1_v4.html`) — an
   earlier, simpler cousin: markdown exam content in a
   `<script type="text/exam-content">` block, python/text fences parsed by
   regex, localStorage autosave of written answers only, JSON export button.
3. **The MIT maths paper** (`MIT_5N18396_Backup_Digital_Exam.html` and
   `MIT_5N18396_Assessor.html`) — a 120-mark QQI Level 5 maths exam in two
   variants: a fully offline no-Python backup and a Pyodide-enabled copy
   whose "Assessor" version auto-fills a hard-coded model-answer array. Six
   answer widget types, dual-path autosave, a built-in calculator, formula
   sheet, and notation guide.

## What worked, and is kept

**One file, no build step, no server.** All three could be emailed, put on a
USB stick, or dropped in a shared folder, and the MIT backup paper ran with
the network cable out. For an exam room with unreliable IT this is the
property that matters most. dewmark's runner output stays a single
self-contained file; anything an exam needs is embedded in it.

**The variant strategy.** The MIT paper shipped as student copy, no-Python
backup, and model-answer key — the right product shape, produced the wrong
way (three hand-edited 100 KB files whose only contract was that a
`querySelectorAll` returned elements in the same order). dewmark compiles
variants from one source.

**Structured sketch description.** The MIT paper's best pedagogical idea:
instead of a drawing canvas, a graph sketch becomes a shape picker (four
small rendered plots as visual options) plus a short form of the features
that earn the marks — opens up or down, roots, intercepts, vertex. It is
typeable under time pressure, printable, markable, and it teaches what a
sketch is for. It becomes a first-class question type.

**Belt-and-braces persistence with honest copy.** The MIT paper saved to
localStorage on a debounce *and* to a real file via the File System Access
API, showed two independent save indicators, and explained the browser-data
failure mode in plain words with a "browser only" opt-out. Document-level
event delegation meant new fields needed no save wiring. All kept.

**Print treated as a real output.** `beforeprint` stamped the student's
name into a print header and expanded every textarea to full height;
page-break rules gave the marker one long question per page; the HVIT print
CSS forced dark editor themes to black-on-white. Kept and extended.

**Answer boxes sized by marks.** A one-mark recall got one row; a five-mark
derivation got six. A small thing that quietly tells the student how much is
expected. Kept as a rule, not a hand-tuned habit.

**Marks-proportional scaffolding as a variant switch.** The exam-condition
MIT copy had all 90 placeholder hints stripped; the practice copy kept them.
Scaffolding belongs to the variant, not the question.

**A quiet Python API.** `exam_tools` (`show`, `show_table`, `text_input`,
`dropdown`, `button`…) made ipywidgets-shaped patterns work in the page, with
a documented mapping from the Jupyter idiom students had practised. dewlab's
`tutorial_tools.py` has since become the maintained version of this idea;
the exam runner should share its lineage rather than fork a third one.

## What broke, and the rule each failure buys

**Answers keyed by position.** The MIT save format was a flat array of
strings, restored into whatever `querySelectorAll` returned; the 115-entry
model-answer array aligned with it by counting alone. Insert one input and
every saved paper silently shifts by one, answers landing in the wrong
boxes with no error.
*Rule: every answerable thing has a stable author-assigned id, and every
persisted value is keyed by it. A positional format is forbidden even as an
optimisation.*

**Hand-duplicated knowledge drifts.** The HVIT exam carried three separate
hand-written copies of its own structure — a task navigator array, a files
table, an API quick-reference — beside the markdown that already contained
it. They disagreed in shipping code: the sidebar documented
`number_input(label, min, max, default)`, the real signature was
`min_val`/`max_val`, and the ten-mark model answer used the sidebar's
version and raised `TypeError`. `slider()` was implemented and advertised
but never imported by the setup cell.
*Rule: navigation, mark totals, file lists, and API references are derived
from the source by the compiler. The compiler asserts declared totals
against summed parts and fails on mismatch.*

**Marks as prose.** The MIT paper's 160 part-marks existed only as
`(2 marks)` spans; the choose-10-of-12 rule existed only as a sentence.
Nothing could total, enforce, or export them without regexing the HTML.
*Rule: marks, sections, and choose-N rules are fields in the source format.
Prose renderings of them are generated.*

**Content inside JS template literals.** Both HVIT payloads (the exam
markdown and the whole Python library) lived in backtick strings, so every
backtick needed escaping and one authored `${` would have silently corrupted
the file.
*Rule: embedded content rides in inert containers — `<script type=...>`
blocks or base64 — never in code literals.*

**Half-embedded assets.** The HVIT exam embedded its SQLite database as
base64 but fetched its two Excel files over HTTP relative to the page. On
`file://` the fetch failed with only a console warning, and Tasks 5 and 6
died at `pd.read_excel` with a bare `FileNotFoundError` while the page still
listed the files as available.
*Rule: an exam file embeds every file it names. There is no relative fetch,
and a missing embed fails the build, not the sitting.*

**Silent failure paths in the save machinery.** Cancelling the save-file
picker set the handle to null and showed nothing; a broken handle degraded
to localStorage-only without a word; the run-mutex dropped clicks with no
feedback; the practice exam only ever autosaved *written* answers, and the
HVIT exam only saved on cell run, so code edited but not run was never
persisted anywhere.
*Rule: every save path has a visible state, every degradation announces
itself, and autosave triggers on input (debounced), not only on run.*

**Restore that pretends more than it restores.** HVIT's Load button
repopulated editors and pasted output HTML back into the page — but the
Python heap, database mutations, and widget listeners were gone, so restored
buttons were dead markup and the student had to know to re-run everything.
Separately, restoring a Python-variant MIT save into the backup variant hit
an undeclared variable and aborted mid-restore.
*Rule: the save format is one format across variants, restore is validated
before it touches the page, and the page states plainly what a restore does
and does not bring back (for code exams: your code and its recorded
outputs; re-run to rebuild live state).*

**Output persisted as scraped innerHTML.** Cell output was stored as raw
`innerHTML` and re-injected on load — which carries figures, but also means
a marker opening a student file injects student-controlled markup into their
own page.
*Rule: outputs are persisted as structured data — stdout text, image data
URIs, tables as columns-and-rows — never as HTML. The workbench renders
from structure and treats every submission as data, not markup.*

**Fragile identity plumbing.** Task ids regexed out of headings, navigation
matched by `startsWith` on heading text, magic globals
(`window.examCurrentOutputId`, a `"__setup__"` sentinel that resolves to
nothing), a 200 ms `setTimeout` racing the restore, `clearSaved()` clearing
storage but not the fields on screen, an assessor banner that prints over
the first page of the marking scheme.
*Rule: ids are declared, contracts are explicit, and anything time-based in
the save/restore path is sequenced by promise, not timer.*

**No marking layer at all.** The "Assessor" file was a key, not a tool:
marking meant a printed scheme beside a stack of printed papers, and the
choose-N decision was made by the marker with no record of the student's
intent. The submission JSON filenames from one path didn't even carry the
student's name.
*Rule: the workbench is a first-class piece of the system, submissions are
named by exam, student id, and name, and choose-N is tracked in the
submission and applied, visibly, at marking time.*

## The one-line summary

The experiments proved the room-level idea — a browser exam with no server
survives contact with an exam hall — and demonstrated, one drifted copy at a
time, that everything beyond the room-level idea must be compiled from a
single validated source rather than maintained by hand.
