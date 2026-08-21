# Open Questions

Thirty-three questions, grouped by theme. No fixed order to answer them in, but the first two clusters — scope and math-specific needs — are the ones most likely to change earlier decisions in DECISIONS.md, so they're worth taking first.

Twenty-three of these are resolved or assumed below (1–8, 11–13, 16, 18, 19, 23–27, 28–31); one is assumed-but-flagged rather than fully closed (32). The remaining handful (9, 10, 14, 15, 17, 20–22, 33) are fine to answer as they come up during the pilot rather than now.

## Identity and scope

1. ~~What should the tool be called? Something that isn't tied to Database Methods, HVIT, or any single course.~~ — resolved: dewlab.
2. ~~Which specific classes use it in year one — programming and math only, or others too?~~ — resolved: not a fixed list — see the `module`/`year` frontmatter fields in CONTENT_AND_FILE_ARCHITECTURE.md. Year-one working set: Computational Methods, Mathematics for IT, Programming and Design Principles, Database Methods, plus a pilot in a colleague's Foundations of Object-Oriented Programming LV5.
3. ~~Does this replace the standalone style already used in index.html, or run alongside it for cases that don't need Python execution at all?~~ — resolved: replaces it. A tutorial with zero exec cells — pure prose, or prose plus math content — is a fully valid file in the same format, same template, same navigation. No separate style needed.
4. ~~Does exam tooling stay on its own permanently separate, offline, single-file architecture, or is there a future where exams and tutorials converge on the same platform?~~ — resolved: stays separate and offline, specified later on its own track — but should share a visual family with the tutorial house style rather than looking unrelated.

## Audience and context

5. ~~Are the students in these classes the same QQI Level 5 adult learners as Database Methods and Web Authoring, or does "programming and math classes" reach a different age group with different privacy or consent considerations?~~ — assumed: same QQI Level 5 adult cohort as the rest of Josh's teaching, no different consent considerations. Flag if any of the four modules reach a different group.
6. ~~Can the students be relied on to have a modern browser on a laptop they control, or does the tool need to tolerate older or locked-down school machines?~~ — resolved: school and personal machines are good; no special tolerance needed.
7. ~~Is this mostly used during class time on a shared network, or mostly as homework on students' own connections? Matters for how much the first Pyodide load can cost.~~ — resolved: not a constraint in either setting.

## Math-specific content needs

8. ~~Does math notation need to render (LaTeX via MathJax or KaTeX) alongside code, or does Python code and its output cover what's needed?~~ — resolved: yes, needed. KaTeX, matching the toolchain already in use elsewhere — see DECISIONS.md.
9. Does the math content need symbolic computation — a library like sympy — or is numeric computation with numpy enough?
10. Do any topics need interactive plots (a slider that redraws a graph live), or is static matplotlib output sufficient?
11. ~~Should any cells check a student's numeric answer against a correct value, or does every cell just run arbitrary code with no right-answer checking?~~ — resolved: yes, some will. See "Answer checking" in DECISIONS.md — a `check()` function, formative feedback only, separate from grading.

## Teacher / authoring workflow

12. ~~One shared tutorial series across programming and math, or separate series each with its own table of contents?~~ — assumed: separate series per module, following the module-subfolder structure already settled. A single series spanning four unrelated modules doesn't map to how a student actually moves through them.
13. ~~Is Josh the sole author, or will anyone else write tutorials? This changes whether the CLI-only editor from last time is still the right call.~~ — resolved: two authors, both comfortable with git. Editor v1 is a GUI, not CLI-only — see DECISIONS.md and REPO_AND_EDITOR.md.
14. How often does content actually change once a class is underway — a rare bugfix, or active week-to-week revision? Changes how much the versioning system needs to carry.
15. Is a "preview as a fresh student" mode — simulating a browser with no saved progress — worth having before publishing a tutorial?

## Student workflow

16. ~~Is there a notion of "done" or submission for a tutorial, or is this purely self-paced practice with no record kept anywhere?~~ — resolved: no formal submission. `check()` cells give informal pass/fail feedback, but nothing is recorded or handed in.
17. Does Josh want any visibility into student progress, even in aggregate (for example, how many students have opened a given tutorial), or should this stay entirely private to each student's own browser and downloads?
18. ~~If a student loses their saved JSON file, is starting over acceptable, or does that need a recovery path?~~ — assumed: yes, acceptable. Autosave to `localStorage` (see 19) is the real safety net; losing an exported JSON file on top of that doesn't justify building a separate recovery path for ungraded practice.
19. ~~Manual "click Save" only, or an autosave layer (to localStorage, as a lightweight fallback alongside the JSON export) to reduce the chance of lost work?~~ — resolved: autosave to `localStorage` is the primary mechanism; manual JSON export is a secondary backup/portability option. See VERSIONING_AND_PROGRESS.md.

## Cross-subject content structure

20. Do programming and math tutorials share one visual house style, or does math get its own look, the way exams and tutorials are already kept visually separate?
21. Does a single tutorial ever need to mix programming-class and math-class content in one page, or do the two stay as clean, separate tracks?
22. Does the OWID real-dataset convention carry over to math content, or does math mostly work with generated or synthetic data instead?

## Aesthetics and visual identity

23. ~~Does dewlab extend the existing navy (#1B2A4A) / orange (#D4692A) / Georgia identity already used in Josh's teaching materials, or get its own distinct palette and typeface, since this is a different medium — interactive code — from static documents?~~ — resolved: extends it. See "Palette and texture" in DECISIONS.md.
24. ~~The writing-app project's "texture panel" (theme: system/light/dark; font: serif/sans/mono; text size; line width; link color — all via CSS custom properties) — carry the same pattern into dewlab, for the authoring GUI, the student-facing pages, or both?~~ — resolved: yes, carried over. Applies to both the GUI and the student-facing pages.
25. ~~If carried to the student side: is dark mode a v1 feature, or a later addition?~~ — resolved: v1 — it comes as part of adopting the texture panel in 24, not as separate work.
26. ~~Code cells: a syntax-highlighting theme built to match dewlab's own palette, or a familiar standard CodeMirror theme students may already recognize from elsewhere?~~ — assumed: a standard theme, light/dark pair tied to the texture panel. See "Code cell theme" in DECISIONS.md.
27. ~~Tutorial pages themselves: the same borderless, minimal-chrome reading surface as the writing app, or more visual structure — borders, color-blocking — to clearly separate prose, code, and output for students newer to this format than Josh is?~~ — resolved: light distinction, not heavy. Prose stays borderless serif; exec cells get line numbers, standard syntax highlighting, and a subtle border/tint — all "free" via CodeMirror's built-in extensions, not custom design work. See "Cell visual treatment" and "Code cell affordances" in DECISIONS.md. Live IDE-style hover documentation (real docstrings on hover) is a separate, non-free feature, deferred past v1.

## Assessment and grading

28. ~~Do any of these tutorials feed into a graded outcome, or are they closer to ungraded formative practice?~~ — resolved: not graded. Some cells include checks (see 11) giving pass/fail feedback, but nothing is recorded or tied to a grade. This settles Phase 2 toward the lighter save/versioning design in VERSIONING_AND_PROGRESS.md.
29. ~~If work is ever handed in for marking, is the existing download-JSON, upload-to-Moodle pattern from the exam tool the intended path here too, or does that change for ungraded practice tutorials?~~ — resolved: not the default path — these aren't submitted for grading. JSON export remains available as an optional backup/portability feature only.

## Technical and hosting

30. ~~One GitHub repo for everything, or a separate repo (and separate Pages site) per subject?~~ — assumed: one repo. Everything else — one build script, one Actions workflow, module folders doing the separating — already assumes this; splitting repos would multiply the CI/Pages setup for no clear gain.
31. ~~Default GitHub Pages URL, or a custom domain — worth considering given students will return to this repeatedly across a term, not just once for an exam.~~ — assumed: default Pages URL for now. Costs nothing to revisit later; not worth spending any of the one-month window on.
32. Are there school or ETB IT restrictions (content filtering, allowed domains) that could block a Pyodide CDN load or a Pages URL on school machines? Assumed fine, per the same call that resolved 6 and 7 — but this is a different risk (network policy, not device speed or bandwidth), and hasn't specifically been checked. Left open rather than resolved; worth a quick look if a CDN or Pages URL ever misbehaves on a school connection.
33. Should the build script also check for things like missing alt text or broken cross-links as part of the build, or stay narrowly focused on markdown-to-HTML conversion?
