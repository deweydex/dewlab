# Questions for Josh

Where the scheduled build sessions put decisions they cannot make alone, and
where the answers come back.

Sessions run unattended every six hours and work through
`planning/BUILD_PLAN.md`. They have git and no GitHub API, so this file — not
an issue, not a PR thread — is the running list. Three times a day a short
session reads it and notifies Josh only if something is unanswered. Silence
means nothing is waiting on him.

## For a session writing a question

Never stop to wait for an answer. Add the question here, record the assumption
you shipped in the meantime, and carry on with everything the question does not
block. Then commit and push, so the next reader sees it.

Add entries under **Open**, newest last, numbered in sequence. Each one says, in
prose: what is being asked, concretely enough to answer without opening the
repo; what you assumed and shipped meanwhile, so that "that's fine" costs Josh
nothing; what changing it later would cost, in the manner of `DECISIONS_LOG.md`;
and what it blocks, if anything. A question only its author can understand is a
note, not a question.

## For a session reading an answer

Answered questions come before new work. Act on the answer, record the outcome
in `DECISIONS_LOG.md` as a numbered entry, move the question down to
**Answered** with what you did, and push.

## For Josh

Answer wherever suits — in this file directly, or by telling whichever session
you are talking to, which will write it down here. An answer of one line is a
complete answer.

---

## Open

**2 — Are the two sample tutorials meant to stay?**

Phase 1 needed one hand-written tutorial to test the converter end to end, so
`tutorials/computational-methods/first-steps.md` and `working-with-tables.md`
exist and build. They are written as real student-facing material rather than
as lorem ipsum, because a fixture that does not look like the real thing does
not test the real thing — but the teaching is a guess, and pedagogy is your
department, not mine.

Shipped meanwhile: both, as ordinary tutorials in the real tree.

Cost to change: none. Delete them, rewrite them, or keep them; the converter
does not care and no test depends on their content.

Blocks: nothing.

**3 — Should the toolchain move to JavaScript, and should the editor be hosted?**

Josh asked how `build.py` runs without Python on his machine, whether the editor
could be hosted so he can edit remotely through GitHub, and said that doing it
all in JavaScript so no machine needs Python would be ideal.

The direct answer first, because it may dissolve most of the question. Python is
never needed on a student's machine — they get built HTML and a Python that runs
inside their browser. It is needed in GitHub Actions, which has it already, and
on an author's machine only for previewing a build locally. So a hosted editor
that commits markdown to GitHub and lets Actions build already satisfies "no
Python on my machine", with no rewrite at all. What it does not give is an
instant preview: the round trip becomes commit, wait for Actions, reload.

That is the real fork, and it is yours: is a fast local preview worth rewriting
`build.py` in JavaScript for? If it is, the case is decent — Node is already a
repository dependency for `vendor-src/`, so a JavaScript build consolidates the
toolchain rather than adding to it, and the same code could then render a live
preview inside a hosted editor. If it is not, `build.py` stays as it is and the
editor is a separate piece of work.

A hosted editor is the larger change of the two regardless. REPO_AND_EDITOR.md
specifies a *local* GUI on Milkdown; hosting it means a GitHub-authenticated web
application, which is a different thing to build and to secure, and it is not in
any of the five phases.

Shipped meanwhile: `build.py` in Python, as Phase 1 specified, with 49 tests
covering its rules. Nothing about this question blocks Phases 2 or 3, and the
rules are the part that survives a port — the parsing, the link checking, the
manifest contract — so the work is not lost either way.

Cost to change: a rewrite of roughly 400 lines and its tests. Higher the longer
Phases 2 and 3 build on top of it, which is a reason to decide before Phase 3
rather than after.

Blocks: nothing yet. It should be settled before the editor is built, and
ideally before Phase 3.

## Answered

**1 — How should `build.py` render math?** *(answered 21 Aug)*

Josh: there is no need to keep parsing off students' machines; build-time via an
existing JavaScript tool called from `build.py` if that is clean, otherwise a
separate JavaScript file is fine.

Done the second way, and 0.19 is why rather than convenience: the vendor bundle
is committed so that neither CI nor an author previewing locally needs Node, and
shelling out to Node from `build.py` would have undone that for every build.
KaTeX is now bundled at `assets/vendor/katex.bundle.js` and imported by the
runtime only on pages the manifest flags as containing maths. `build.py` finds
and marks the maths; the browser renders it. Recorded as DECISIONS_LOG 1.8.

Josh also asked, in the same exchange, whether Pyodide could do it. It could,
but it would be the most expensive option available: a prose-and-maths tutorial
currently never boots Pyodide at all (0.16), and making one load a Python
runtime to render `$x^2$` costs far more than KaTeX's 266 KB.

And: syntax highlighting on ordinary markdown code blocks, which he called
essential. Those had none — only `exec` cells were highlighted. They now get a
read-only CodeMirror from the same theme as the live cells. Recorded as 1.9.
