# What to build next in dewmini, and the two questions still open

dewmini lets a student write Python in cells and in a file. It does not let
them spread one program across several files that call each other, which is
the step this work exists for. Steps 1 to 3 of that shipped in #100: the
percent format, the workspace on Python's import search list, and cell outputs
carried through the `.ipynb` reader and writer.

This is the brief for what comes next. It records decisions already taken so
they are not re-argued, and states the two questions that are still open.

---

## Already decided

**A notebook is saved as a `.ipynb` file in the workspace**, with dewmini's own
information under a `dewmini` key in nbformat's metadata. The specification
requires a tool to preserve metadata keys it does not recognise, so the file
stays a valid Jupyter notebook that other programs open normally. No new file
format is invented, because that key is the only thing a new format would have
provided.

**Saving as a `.py` file stays**, without outputs, with one line said at the
moment the file is written. A `.py` file is a program another file can import.
A `.ipynb` file is a notebook with its results.

**The left panel is the project, the right panel is everything outside it.** So
the file manager, the table of contents and the variable list go left, and the
glossary and settings go right. The variable list and the glossary each move
across, which invalidates the parts of `DEWMINI_WORKBENCH.md` §2 and of the
browser tests that name a panel's side.

**A tutorial's `workspace` folder opens by itself.** This is a deliberate
exception to the rule in `DEWMINI_WORKBENCH.md` §1 that nothing opens on a
first visit. That rule exists so a student is not met with panels they did not
ask for, and a workspace folder is not a panel. It is the material the
tutorial's own instructions refer to.

**The tutorials stay markdown documents.** Across 91 files they hold 6,076
lines of code and 17,306 lines of prose, so storing them as Python would put
three lines in four inside a comment block.

---

## The work

1. Add the file view, extend the Files panel into a file manager that can open,
   create and rename, and move the panels to the sides above. One to two weeks.
2. Let a tutorial carry a `workspace` folder. Small, and independent of the
   rest.
3. Store notebooks in the workspace as `.ipynb` files. Blocked on the first
   question below.

---

## The two questions still open

**Does a file written to the workspace survive a reload on each of the three
filesystem backends?** One of the three, IDBFS, writes to permanent storage
only when it is explicitly told to, and a notebook lost that way would be worse
than anything moving notebooks out of `localStorage` fixes. The check is in
`tests/MANUAL_CHECKLIST.md` and needs a real machine, because the headless
browser the tests use only ever reaches one of the three. Step 3 waits on it.

**What does a tab hold?** Today it holds a notebook. It would have to hold
either a notebook or a file, and everything reading or writing a tab's contents
is affected. If a tab is described as a document with storage behind an
interface, rather than as JSON in `localStorage`, then step 3 becomes a change
in one place instead of everywhere. This is answered by writing the code, not
by another document, but it should be answered first.

---

## Two things not to propose again

**Magics**, meaning `%%time`, `%matplotlib inline` and `!pip install`. They are
invisible non-Python syntax that works inside a notebook and fails everywhere
else. Our students write real `.py` files on both PDP and CMPS. `%%time` has a
plain Python answer, `time.perf_counter`, that teaches something transferable.

**Modal keyboard commands**, meaning Jupyter's Escape and Enter modes. Press
Escape by accident and typing stops working, with nothing on screen to explain
why. Jupyter itself needs a help overlay for it. Plain shortcuts that always
mean the same thing are the safer half of the idea.
