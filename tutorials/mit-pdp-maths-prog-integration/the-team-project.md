---
title: "The Team Project"
slug: the-team-project
module: mit-pdp-maths-prog-integration
module_title: "Programming and Maths, Integrated"
year: "2026-2027"
series: reflections-and-review
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

**Programming Design Principles**

This one is not a tutorial. There is no code to run and nothing to work through in an hour — it is a brief for a piece of work you will do over several weeks, in a group of three to five, and it is here so that the shape of it is written down somewhere you can go back to.

The learning outcome behind it asks you to design, develop, release and review software **over time, in a team**. Every word of that matters, and the two that people underestimate are *over time* and *review*.

## What You Are Being Asked to Do

Build something small, in a group of three to five, and release it three times.

Small is important. A project that is too ambitious does not fail at the end; it fails in week two, when nobody can see how the pieces fit and everyone quietly stops. Something you could reasonably finish alone in a weekend is about right for a team over several weeks — because most of what you are learning here is not how to write the code.

Things that have worked:

- **A tool that does something you actually do by hand.** A timetable checker, a marks calculator, something that renames files the way you keep renaming them.
- **A small game.** Guessing, quizzes, noughts and crosses. The rules are known so the arguments are about the building.
- **Something with data in it.** Take a dataset you can get hold of and answer three questions about it, with plots.

Things that go wrong: anything needing an account with somebody else's service, anything with a login, and anything where the interesting part is a library you have not used yet.

## Three Releases, Not One Deadline

This is the part that makes it a project rather than an assignment.

**You will release three times.** Each release is a version somebody outside the team could use, at the point you release it. Not a plan for one, not most of one — a working thing, however little it does.

| | What it is | The question it answers |
|---|---|---|
| **Release 1** | The smallest thing that does anything at all | Does the shape of this work? |
| **Release 2** | The main feature, done properly | Can we build the thing we described? |
| **Release 3** | Finished, tidied, and documented | Would we hand this to somebody? |

Release 1 is the one teams get wrong. It should feel embarrassingly small. If your project is a quiz game, release 1 asks one hard-coded question and says whether you got it right. That is enough — it proves that the pieces connect, and it means the first time you find out that two people's code does not fit together is week two rather than week six.

**Each release gets a version number and a date**, and you keep the old ones. That is the same idea as the versions on these tutorials: a release is a thing somebody could go back to.

## Working on One Thing at Once

Three to five people editing the same project will collide. There is no arrangement that prevents this; there is only being ready for it.

**Split by what a piece does, not by who is good at what.** "Ciara does the input, Dev does the calculations, Maeve does the output" gives everyone something to build and a clear edge where their piece meets the next. "Ciara does the hard parts" gives you one person doing a project and three people watching.

**Agree the edges before you write anything.** If Dev's function is going to be called by Ciara's code, decide now what it is called, what goes in, and what comes out. Write that down. Both people can then build against it without waiting.

That agreement is worth more than any amount of planning about features. It is the thing that lets four people work at once instead of in a queue.

**Talk about what you are touching.** Two people editing the same file at the same time is the most common way a week's work disappears, and a message saying "I'm in the scoring code this evening" prevents nearly all of it.

## Reviewing Each Other's Work

The outcome says *review*, and this is the half most teams skip.

**Before each release, read each other's code.** Not to find fault — to find out whether it can be read. If you cannot follow what a function does, that is information about the function rather than about you, and it is much cheaper to find out now.

Three questions that make a review useful rather than polite:

**Can I tell what this does without asking?** If the answer is no, the fix is usually a better name or a sentence of comment, not more code.

**What happens if this gets something unexpected?** An empty list, a zero, a negative number, a word where a number was expected. *When It Goes Wrong* is the tutorial for this, and every one of those errors is one somebody will hit.

**Is there something here we have already written somewhere else?** Two people solving the same problem separately is normal and worth catching.

**Write down what you agreed**, briefly. "We are keeping the two scoring functions separate for now" is worth a line, because in three weeks nobody will remember whether that was a decision or an accident.

### After the last release

The review that matters most is the one at the end, and it is about the process rather than the product.

- What went differently from what you expected?
- Where did the time actually go, against where you thought it would?
- What would you do differently with the same brief and a fresh start?
- What did somebody else in the team do that you would like to be able to do?

That last one is worth taking seriously. Three to five people building something together is the closest this course comes to how software is actually made, and most of what people take away from it is something they watched somebody else do.

## What Gets Handed In

Per release: the working code, a short note on what changed, and who did what.

At the end: the three releases, and a reflection of a page or so per person, answering the questions above in your own words.

The reflection is not a summary of the project. It is what you learned, including the parts that did not go well — and a project where nothing went wrong is either very small or not being described honestly.

## A Last Thing

The hardest problem in a team project is almost never technical.

It is somebody being stuck and not saying so, for a fortnight, because they think everybody else understands it. This happens in professional teams constantly and it is the single most expensive thing that goes wrong.

If you are stuck, say so on the day. If somebody has gone quiet, ask them. Neither of those is a small kindness — they are the actual skill this outcome is about.

## Where to Read More

Fowler, M. (2006). *Continuous Integration.*
<https://martinfowler.com/articles/continuousIntegration.html>. The
professional version of "release early, release small" — merging and
testing everyone's work together constantly, rather than once at the end.
