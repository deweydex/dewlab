# Open questions — dewmark

The register, in the repository's usual form: what is asked, what is
assumed and being built meanwhile, what changing the assumption later
would cost, and what the question blocks. Numbered DM-n so specs and
code can cite them. Answers land here, in the root DECISIONS_LOG as
numbered entries, and in the code.

---

**DM-1 — Where do exam sources and submissions live?**
Asked: dewlab is public; exam sources are secret until sat and
submissions are personal data always, so neither can be committed here.
Everlearning already holds the private teaching corpus and is the
obvious home for sources; submissions may belong outside git entirely.
Assumed meanwhile: sources in a private location of the author's
choosing, submissions in local folders only; this repo carries tooling
and openly-shareable samples in `dewmark/samples/`.
Cost of changing later: low — nothing in the tooling knows where files
live. Blocks: nothing technical; blocks writing the teacher-facing
"how to organise your exam folder" documentation.

**DM-2 — Graded-PDF generation mechanism.**
Asked: per-student print-to-PDF works everywhere but is thirty manual
print dialogs; a vendored client-side PDF library gives one-click zips
but must reproduce KaTeX maths and figures faithfully.
Assumed meanwhile: phase 2 ships the print flow with a next-paper
loop; a library spike (pdf-lib or paged.js rendering path) is scheduled
after the graded layout stabilises.
Cost: low — the graded HTML layout is the input to either mechanism.
Blocks: the one-click export promise in GRADING_WORKBENCH §6.

**DM-3 — Marks sheet: CSV only, or also real xlsx?**
Asked: CSV opens in Excel but multi-region layouts (marks + the id
descriptions) are clumsy across two files; xlsx would carry both as
sheets but costs a vendored writer.
Assumed meanwhile: two CSVs with shared naming.
Cost: trivial to add xlsx later. Blocks: nothing.

**DM-4 — Timer.**
Asked: should the runner show elapsed/remaining time, and should
`duration_minutes` do anything beyond display? A countdown raises
stress and lies whenever a room grants extra time; no timer means the
wall clock governs, as on paper.
Assumed meanwhile: no timer in phase 1; `duration_minutes` renders on
the start screen only.
Cost: a timer is additive. Blocks: nothing.

**DM-5 — Identity entry: typed, or roster-backed?**
Asked: typed names produce "agnes nitt"/"Agnes Nitt"/"A. Nitt"
variance and typo'd ids; a roster compiled into the exam would fix
matching but puts a class list inside a distributed file.
Assumed meanwhile: typed name + student id, workbench matches on id
and reports unknowns; no roster in the exam file (privacy beats
convenience). A roster CSV loaded into the *workbench* for
cross-checking is uncontroversial and planned.
Cost: low. Blocks: nothing.

**DM-6 — Choose-N marking policy.**
Asked: when a student attempts more than N, does the marker count the
best N (kindest, and what the workbench defaults to), the first N, or
a student-declared selection at finish time?
Assumed meanwhile: mark everything attempted, count best-N, marker can
override; the finish checklist reports the overrun to the student.
Cost: policy-only — the submission records attempts, so any policy is
computable later. Blocks: the exact finish-screen copy; QQI/IV
guidance should be consulted before first real use.

**DM-7 — Pyodide delivery in exam rooms.**
Asked: CDN needs internet and a school network that doesn't block
jsDelivr (root planning Q32 already flags this); alternatives are a
room-local server (`serve.py` + `DEWLAB_PYODIDE_BASE`, both existing)
or per-machine pre-caching.
Assumed meanwhile: CDN default, override honoured, and a pre-exam
checklist document for the room ("open the paper the day before on
each machine" warms every cache).
Cost: none — the override exists. Blocks: confidence, not code; a real
room rehearsal is the answer.

**DM-8 — `python provided` cells: auto-run or student-run?**
Asked: auto-running provided cells (HVIT setup style) hides state
mutations; requiring the student to run them adds a failure mode
("nothing works because you skipped the first cell").
Assumed meanwhile: `setup` auto-runs and is invisible; `provided` is
visible and auto-runs at start with its output shown, so the page
never depends on a student ritual.
Cost: low. Blocks: runner implementation detail only.

**DM-9 — Main-thread Pyodide (no Stop button) in exams.**
Asked: single-file `file://` pages preclude the worker + COI apparatus,
so an infinite student loop freezes the tab; is reload-and-restore an
acceptable recovery in exam conditions?
Assumed meanwhile: yes, because persistence makes reload cheap — the
page states "if the page stops responding, close and reopen; your work
is saved." A hosted (non-file) exam build could regain the worker.
Cost: medium if wrong — a worker-capable exam build is real work.
Blocks: nothing in phase 1 (maths exams have no cells).

**DM-10 — Handwritten working.**
Asked: some maths marking wants to see working that typing flattens;
options include photographing paper working into the submission
(image answer type), or accepting typed-notation working as
sufficient (the MIT stance).
Assumed meanwhile: typed working plus the sketch type; no camera
path — it reintroduces filenames, sizes, and upload friction that the
one-zip design removed.
Cost: an `image` answer type is additive if wanted. Blocks: which
maths questions are askable; authors should know the constraint.

**DM-11 — One parser, two hosts.**
Asked: the composer page needs the builder's parser/validator; a JS
port would drift, running the Python builder in Pyodide inside the
composer keeps one implementation but couples the composer to a 30 MB
load.
Assumed meanwhile: builder is written import-cleanly so it can run
under Pyodide; the decision is deferred until the composer page
exists.
Cost: high if a JS port is written first and drifts — so it won't be.
Blocks: composer phase 3 architecture.

**DM-12 — Naming.**
Asked: is dewmark the name, and are runner / workbench / composer the
right component names? ("marking" vs "grading" is also unsettled;
these specs use both, leaning on "marks" for the quantity and
"grading workbench" for the tool.)
Assumed meanwhile: dewmark; rename cost is a find-and-replace while
nothing is published. Blocks: nothing yet; must settle before storage
keys and filenames ship (they embed the name).

**DM-13 — How much marking support on Firefox/Safari?**
Asked: the workbench leans on `showDirectoryPicker` (Chromium-only)
for folder-as-database; the fallback is read-only files + manual
export.
Assumed meanwhile: Chromium is the supported marking environment,
stated plainly; the fallback exists but is not polished.
Cost: revisit if a real marker can't use Chromium. Blocks: nothing.

**DM-14 — The exam signal (visual).**
Asked: exactly how an exam page announces itself against the tutorial
family — header band, wordmark, palette shift?
Assumed meanwhile: STYLE §1's proposal.
Cost: CSS. Blocks: nothing; settle during the first runner build with
real pages side by side.

**DM-15 — Restore precedence.**
Asked: when localStorage and a save file disagree, newest-wins is
assumed — but "newest" depends on machine clocks, and a student moving
machines mid-exam is exactly when clocks disagree.
Assumed meanwhile: newest `saved_at` wins with both offered
explicitly (timestamps and answer counts shown) when they differ by
more than the debounce interval.
Cost: low. Blocks: runner restore implementation.

**DM-16 — Assisted marking, ever?**
Asked: numeric and MCQ parts could be auto-scored, and an LLM could
draft feedback; both change the tool's character and the trust
teachers and assessors place in it.
Assumed meanwhile: no — GRADING_WORKBENCH §7's line holds until the
human workflow has run a real session; any later step here gets its
own specification, consent story, and accuracy evaluation.
Cost: none now. Blocks: nothing.

**DM-17 — Accessibility commitment.**
Asked: what does dewmark promise a screen-reader user or a student
with alternative-arrangement needs, and by when (STYLE §6)?
Assumed meanwhile: the §6 baseline in phase 1; full non-visual
sittability investigated with the institution's disability support
practice rather than guessed at.
Cost: retrofitting semantics is expensive — which is why the baseline
is phase 1, not later. Blocks: honest claims in teacher-facing docs.

**DM-18 — Relation to dewlab ROADMAP phases 3 and 4.**
Asked: seeded practice generators (phase 3) and the portfolio export
(phase 4) brush against assessment; does dewmark share machinery with
either?
Assumed meanwhile: the Python builder (SOURCE_FORMAT §8) and phase-3
generators should converge on one seeding idiom eventually; the
portfolio export stays tutorial-side. No shared code yet.
Cost: divergent seeding idioms would be a nuisance, not a break.
Blocks: nothing.
