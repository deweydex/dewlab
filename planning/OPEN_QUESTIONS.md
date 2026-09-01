# Questions this project had to answer

Thirty-three questions were raised before any code was written. Most are now
settled; a handful are not, and are fine to answer during the pilot rather than
in advance.

They are kept numbered rather than tidied away because other documents point at
them by number, and because the reasoning is often more useful than the answer.
A question that turned out not to matter is worth knowing about too — it stops
the next person spending an afternoon on it.

Questions raised *since* the build began live in `QUESTIONS.md` at the root of
the repository.

---

## Still open

These need answering eventually. None of them blocks current work, and each
says what it would change.

**A text cell collapsing on blur swallows the next click.**
A text cell's editing box hides when it loses focus and its rendered
markdown takes its place. The rendered form is usually shorter, so
everything below the cell moves up at that moment. A reader who finishes
typing a note and then clicks an insert seam below it presses the mouse
on the button and releases it over whatever has slid into that position,
and the click is lost. They click again and it works, so it reads as a
stray misclick rather than as a defect.

Found while writing the tests for the percent format, not looked for. A
fix would keep the cell's height stable across the swap, or render on a
change rather than on blur. The browser tests work around it
deliberately — `add_text_cell()` leaves the cell and waits for the
collapse — so the workaround is not mistaken for ceremony and removed.

**9. Does the mathematics content need symbolic computation?**
A library like sympy would give algebra that works with symbols rather than
numbers — factorising, solving, simplifying. numpy covers numeric work already.
Adding sympy later is a single line in one tutorial's frontmatter, not a
redesign, so this can wait until a tutorial actually needs it.

**10. Do any topics need interactive plots?**
A slider that redraws a graph as a student moves it teaches something a static
picture cannot — but it is real work, and static matplotlib output may well be
enough for everything planned.

**14. How often does content change once a class is running?**
The difference between a rare bugfix and weekly revision decides how much the
saved-progress machinery has to carry. If tutorials are edited often, students
will meet the version-mismatch path regularly, and it has to be reassuring
rather than alarming.

**15. Is a "preview as a new student" mode worth having?**
A way to open a tutorial as though no progress had ever been saved. Cheap to
add, and it catches a whole class of authoring mistake — but only if authors
would use it.

**17. Should anyone be able to see student progress, even in aggregate?**
Currently nothing leaves the student's browser, which is the strongest possible
privacy position and the easiest one to explain to a class. Even a count of who
opened a tutorial would change that, so it is a decision to make deliberately.

**20. One visual style across programming and mathematics, or two?**
Whether a mathematics tutorial should look different from a programming one, or
whether the consistency is worth more than the distinction.

**21. Does a single tutorial ever mix programming and mathematics content?**
The tracks are currently separate. If a tutorial needs to teach both at once,
nothing prevents it — the question is whether that ever happens in practice.

**22. Do the real-dataset conventions carry over to mathematics?**
Programming tutorials work from real published data. Mathematics may be better
served by generated values, where the numbers can be chosen to make the idea
visible.

**32. Could school network restrictions block the tutorials?**
Devices and connections were checked and are fine. Network *policy* was not:
content filtering or an allowed-domains list could block the Python runtime's
download, or the published site itself. This is assumed fine rather than
verified. If it turns out to bite, the runtime can be hosted from the site
itself instead — a one-line change, at the cost of about 30 MB in the
repository.

**33. Should the build check more than markdown conversion?**
Partly answered already: dead cross-links and missing image descriptions both
fail the build. Whether it should check more — reading level, dataset
availability, anything else — is open.

---

## Settled

### What this is and who it is for

**1. What is it called?** dewlab. Deliberately not tied to any one module.

**2. Which classes use it?** Not a fixed list. A tutorial declares its own
module, so a new module is a new folder rather than a code change. The
starting set is Computational Methods, Mathematics for IT, Programming and
Design Principles, and Database Methods, with a pilot in a colleague's
object-oriented programming module.

**3. Does it replace the older standalone tutorial style?** Yes. A tutorial
with no runnable code — prose, or prose and mathematics — is an ordinary
dewlab tutorial in the same format with the same navigation. One format covers
both cases, so there is no second thing to maintain.

**4. Does assessment tooling merge into this?** No. Anything exam-shaped stays
separate and offline, on its own track, though it should look like it belongs
to the same family of materials.

**5. Who are the students?** The same adult learners as the rest of the
programme, so no different consent or privacy considerations apply. Worth
flagging if any module reaches a different group.

**6. What machines will they use?** School and personal machines are both fine.
No special tolerance for old or locked-down devices is needed.

**7. Class time or homework?** Both, and neither constrains how much the first
load can cost.

### Mathematics and answers

**8. Does mathematical notation need to render?** Yes — confirmed necessary for
Mathematics for IT. KaTeX does it.

**11. Should cells check a student's answer?** Yes, for some. `check()` gives
pass-or-not-yet feedback and records nothing. It is formative, and unrelated to
any grade.

### Authoring

**12. One series across all modules, or one per module?** One per module. A
single series spanning four unrelated subjects does not match how a student
actually moves through them.

**13. Who writes tutorials?** Two authors, both comfortable with git. That is
why the planned editor is a GUI rather than command-line only.

### What a student's work does

**16. Is there a notion of "done"?** No. Nothing is submitted and nothing is
recorded. `check()` gives informal feedback and that is all.

**18. What if a student loses their saved file?** Starting over is acceptable.
Autosave in the browser is the real safety net; an exported file is a
convenience on top of it.

**19. Manual save or autosave?** Autosave, with manual export as a secondary
option for moving between devices.

### Look and feel

**23. Its own palette, or the existing one?** The existing one — navy, orange,
and a serif base. Students already read materials that look like this.

**24. A texture panel for readers?** Yes: theme, font, size, line width, link
colour. It applies to both the student pages and the authoring editor.

**25. Is dark mode a first-version feature?** Yes. It arrives as part of the
texture panel rather than as separate work.

**26. A custom syntax-highlighting theme?** No — a standard light and dark
pair, tied to the texture panel. Familiar beats bespoke here.

**27. How much visual structure on a page?** Light. Prose stays borderless and
serif; runnable cells get line numbers, syntax highlighting, and a subtle
border. Enough to make the page scannable, not so much that it fights the
reading surface. Live hover documentation — real docstrings on hover — is
real work and is deferred.

### Assessment

**28. Do these feed into a grade?** No. Ungraded formative practice.

**29. Is work ever handed in?** Not by default. Export exists for portability,
not for submission.

### Hosting

**30. One repository or several?** One. The build, the publishing workflow, and
the module folders all assume it, and splitting would multiply the setup for no
clear gain.

**31. Default address or a custom domain?** The default for now. Costs nothing
to revisit later.
