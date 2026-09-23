---
title: "The Team Project"
year: "2026-2027"
version: 2026.08.23.1
covers:
  what-you-are-being-asked-to-do:
    covers: [PDP-LO12]
  three-releases-not-one-deadline:
    covers: [PDP-LO12]
  working-on-one-thing-at-once:
    covers: [PDP-LO12]
  reviewing-each-others-work:
    covers: [PDP-LO12]
---

# The Team Project

This page is a brief, not a tutorial. A *brief* is a description of a
piece of work you are asked to do. This one is for a project you will
do over several weeks, in a group of three to five. There is no code to
run here, and nothing to work through in an hour. The page is here so
that the plan is written down somewhere you can come back to.

The learning outcome behind the project asks you to design, develop,
release and review software **over time, in a team**. Every word of
that matters. The two that people most often underestimate are *over
time* and *review*.

## What You Are Being Asked to Do

As a group of three to five, you will:

1. build something small;
2. release it three times.

**Small is important.** A project that is too big fails early, in week
two, not at the end. Nobody can see how the pieces fit together, and
everyone quietly stops working on it.

A good size is something one of you could finish alone in a weekend.
For a team over several weeks, that is about right, because most of
what you learn here is not how to write the code.

Here are kinds of project that have worked:

- **A tool that does something you do by hand.** A timetable checker, a
  marks calculator, or a program that renames files the way you keep
  renaming them.
- **A small game.** A guessing game, a quiz, or tic-tac-toe. Everyone
  already knows the rules, so the discussions are about how to build it.
- **Something with data in it.** Find a dataset you can get, and answer
  three questions about it, with plots.

And here are kinds of project that go wrong:

- anything that needs an account with somebody else's service;
- anything with a login;
- anything where the interesting part is a library you have not used
  yet.

## Three Releases, Not One Deadline

Three releases are what make this a project and not an assignment.

A *release* is a version of your program that somebody outside the
team could use on the day you release it. It is a working thing, however
little it does. A plan is not a release, and neither is most of a
program.

| | What it is | The question it answers |
|---|---|---|
| **Release 1** | The smallest thing that does anything at all | Does the shape of this work? |
| **Release 2** | The main feature, done properly | Can we build the thing we described? |
| **Release 3** | Finished, tidied, and documented | Would we hand this to somebody? |

**Every release must:**

- [ ] work, so that somebody outside the team could use it;
- [ ] have a version number;
- [ ] have a date;
- [ ] be kept after the next release comes out. Do not delete or
  overwrite old releases.

Keeping old releases is the same idea as the versions on these
tutorials. A release is a thing somebody could go back to.

**Release 1 is the one most teams get wrong.** It should feel almost
too small to show anyone. Say your project is a quiz game. Release 1
could ask one question, written straight into the code, and say whether
the answer is right. That is enough.

Why is so little enough? Release 1 proves that the pieces connect. It
also means you find out early when two people's code does not fit
together: in week two, not in week six.

## Working on One Thing at Once

When three to five people edit the same project, their changes will
clash. No way of organising the team stops this completely. What you can
do is be ready for it. Here is a way to set up the work.

1. **Split the work by what each piece does.** Do not split it by who
   is good at what. "Ciara does the input, Dev does the calculations,
   Maeve does the output" gives everyone something to build. It also
   gives a clear edge where one person's piece meets the next.
   "Ciara does the hard parts" gives you one person doing the project
   and three people watching.
2. **Agree the edges before anybody writes code.** Say Ciara's code
   will call Dev's function. Decide now:
   - what the function is called;
   - what goes in;
   - what comes out.
3. **Write that agreement down.** Now both people can build against it,
   and neither has to wait for the other.
4. **Tell the team what you are working on.** Two people editing the
   same file at the same time is the most common way a week's work is
   lost. A short message like "I'm in the scoring code this evening"
   prevents nearly all of it.

The agreement in steps 2 and 3 is worth more than any amount of planning
about features. It is what lets four people work at the same time,
instead of one after another.

## Reviewing Each Other's Work

The learning outcome says *review*, and this is the half most teams
skip.

**Before each release, read each other's code.** The point is to find
out whether the code can be read, not to find fault. Suppose you cannot
follow what a function does. That tells you something about the
function, not about you. It is much cheaper to find that out now than
later.

A polite review says "looks fine". A useful review asks questions. For
each piece of code, work through these three:

1. **Can I tell what this does without asking?** If not, the fix is
   usually a better name or one sentence of comment, not more code.
2. **What happens if this gets something unexpected?** For example, an
   empty list, a zero, a negative number, or a word where a number was
   expected. [Reading an error message](tutorial:reading-an-error-message)
   and [Finding bugs in bigger programs](tutorial:when-it-goes-wrong) are
   the tutorials for this. Somebody using your program will hit every one
   of those errors.
3. **Have we already written this somewhere else?** Two people often
   solve the same problem separately. That is normal, and it is worth
   catching.

Then **write down what you agreed**, in a line or two. For example: "We
are keeping the two scoring functions separate for now." In three weeks,
nobody will remember whether that was a decision or an accident.

### After the last release

The review that matters most comes at the end. It is about how you
worked together, more than about what you built. Ask yourself:

- What went differently from what you expected?
- Where did the time go, compared with where you thought it would go?
- With the same brief and a fresh start, what would you do differently?
- What did somebody else in the team do that you would like to be able
  to do?

Take that last question seriously. Building something with three to
five people is the closest this course comes to how software is made in
real jobs. Most of what people take away from it is something they
watched somebody else do.

## What Gets Handed In

**With each release, hand in:**

- [ ] the working code;
- [ ] a short note on what changed;
- [ ] a note on who did what.

**At the end, hand in:**

- [ ] all three releases;
- [ ] a reflection from each person, about a page long, answering the
  questions in [After the last release](#after-the-last-release) in
  your own words.

The reflection is about what you learned, including the parts that did
not go well. It is not a summary of the project. If a project had
nothing go wrong, it was either very small, or it is not being
described accurately.

## A Last Thing

The hardest problem in a team project is almost never technical. It is
almost always somebody who is stuck and does not say so, for two
weeks, because they think everybody else understands.

This happens in professional teams all the time, and it is the most
expensive thing that goes wrong.

If you are stuck, say so on the same day. If somebody in your team has
gone quiet, ask them how they are getting on. Neither of these is just
a small kindness. They are the real skill this learning outcome is
about.

## Where to Read More

Fowler, M. (2006). *Continuous Integration.*
<https://martinfowler.com/articles/continuousIntegration.html>. The
professional version of "release early, release small" — merging and
testing everyone's work together constantly, rather than once at the end.
