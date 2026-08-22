# The seven decisions, answered

Josh, 2026-08-22. `DECISIONS_NEEDED.md` has the questions and what was at stake;
this is what was decided and what it means for the work.

---

## 1–3. Trigonometry, radians, coordinate geometry — **all in scope**

Right-triangle trigonometry, radians and the unit circle, and coordinate
geometry all come in, in full. Nothing from Section 4 is dropped except surd
form (`MIT-4.7`), and nothing from Section 3 except the pieces named in 6.

With them, a further instruction that changes how everything below is planned:

> There is no problem with having more tutorials or making other things longer
> or connecting different tutorials together so that they refer to each other.

**Length and count are not constraints.** Teachers choose which tutorials they
use; a student who is going well can go further. That reverses the assumption
behind the original outlines, which tried to fit each gap into as few tutorials
as possible.

## 4. Complex roots — **an aside, not a rewrite**

Tutorial 15 keeps its cliff edge and gains a short aside saying that the roots
do exist, with a link to Wikipedia and to a **bonus tutorial on complex
numbers**. So: no rewrite of 15, no full tutorial in the main sequence, one
aside and one optional tutorial off to the side.

## 5. Numbering — **drop it, and build an editor**

The numbers come out of titles entirely. Two things follow that are much larger
than the question asked:

- **Numbers come out of filenames too**, including the downloadable copies. That
  changes every published URL.
- **A graphical editor page**, so that reordering is something Josh does rather
  than something he asks for. Change a tutorial's position, insert one between
  two existing tutorials or at the end, and a button to create a new one.

The editor is new ground — nothing in dewlab has touched it. Planned in
`planning/EDITOR.md`.

## 6. Calculus — **two tutorials and a bonus**

- A **product rule** tutorial (with the sum rule).
- A **substitution** tutorial.
- A **bonus section on the chain rule**.
- **Not** the quotient rule. **Not** integration by parts.
- "Combining everything" becomes applications and fun problems rather than more
  drill. Calculus is not the focus of this course.

**Settled, and the other way round.** I flagged that integration by
substitution *is* the chain rule run backwards, and suggested the chain rule
bonus should therefore come first. Josh chose the opposite, and gave the reason:

> Substitution should come first because it feels algebraic, and substituting
> one function for another is something we've done. So we've done composition of
> functions, and then the chain rule can come out of that as an example. And we
> can discover these in the tutorials, meaning that we don't need to name them
> until after we've done some step by step thinking things through.

So: **composition of functions → substitution → the chain rule as the thing that
falls out of it.** The chain rule is not a prerequisite being withheld; it is a
pattern the students are led to notice in work they have already done.

That last sentence turned out to be a general principle rather than a remark
about calculus, and it now has a decision of its own (DECISIONS_LOG 7.7). It
also changed the dependency data: divide and conquer moved to *after* searching
and sorting, because binary search is what gives a student a reason to name the
idea.

## 7. Splitting tutorials — **yes, and further than proposed**

Not just Tutorial 13. The principle is general:

> It would be worth thinking through whether each of the tutorials can be split
> into smaller tutorials that cover just one thing.

With polynomials named as the case that needs several parts — quadratics and
their kinds as one thing, larger polynomials and representing them in code as
another, graphing them as another. Each tutorial one topic, referring out to the
others.

This is a re-plan of the whole series rather than one split, and it is what the
editor in 5 exists to make survivable.

---

## And a new piece of work, to plan but not build

**Practice problems, one file per tutorial.** Students type answers into boxes
and work through them; they can check an answer; and around the problems sit
short reflection prompts — how they feel about the topic before starting, and
after. Students can also **write their own problems and share them**.

That needs something dewlab does not have: cells created at runtime, by the
student, rather than only at build time. Planned in `planning/PRACTICE.md`.
