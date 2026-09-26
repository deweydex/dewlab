---
title: "The Team Project"
year: "2026-2027"
version: 2026.09.26.1
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
piece of work you are asked to do. This one is for a project you will do
over several weeks, in a group of three to five. It is written down here
so that you can come back to it. How your class runs the project, the
dates, what is handed in and how it is assessed, is your teacher's to say.
This page is the part that stays the same: what to build, how to build it
together, and questions to look back with.

The learning outcome behind the project asks you to design, develop,
release and review software **over time, in a team**. Every word of that
matters. The two that people most often underestimate are *over time* and
*review*.

## What you are being asked to do

As a group of three to five, you will build a small game or tool in one
of the worlds, and release it three times. Here are some that fit:

- **A text adventure.** Rooms kept in a dictionary, and a `while True`
  loop that asks where to go next.
- **A cipher tool.** Code, decode and crack messages, from a menu.
- **A pixel-art editor.** A picture kept as a list of lists, with commands
  to draw on it, mirror it and print it.
- **A quiz** about dinosaurs, planets, or anything your team knows well:
  questions in a list, answers checked with care, and a score.

Or propose your own, with the same shape: a loop, a way to quit, and some
data the program keeps. Everything these need is in Programming
Foundations and [From cells to a program](tutorial:from-cells-to-a-program).

**Small is important.** A project that is too big fails early, in week
two, not at the end. Nobody can see how the pieces fit together, and
everyone quietly stops working on it. A good size is something one of you
could finish alone in a weekend. For a team over several weeks, that is
about right, because most of what you learn here is not how to write the
code.

Some ideas go wrong in the same ways, whoever tries them: anything that
needs a login, anything that depends on somebody else's service, and
anything where the interesting part is a library you have not used yet.

## Three releases, not one deadline

Three releases are what make this a project and not an assignment. A
*release* is a version of your program that somebody outside the team
could use on the day it comes out. It is a working thing, however little
it does. A plan is not a release, and neither is most of a program.

| | What it is | The question it answers |
|---|---|---|
| **Release 1** | The smallest thing that does anything at all | Does the shape of this work? |
| **Release 2** | The main feature, done properly | Can we build the thing we described? |
| **Release 3** | Finished, tidied, and documented | Would we hand this to somebody? |

**Every release:**

- [ ] works, so that somebody outside the team could use it;
- [ ] has a version number and a date;
- [ ] has a line in the change log saying what changed;
- [ ] is kept after the next release comes out.

**Release 1 is the one most teams get wrong.** It should feel almost too
small to show anyone. Here is a Release 1 of a text adventure: two rooms,
one way between them, and a way to quit.

```python exec
id: three-releases-not-one-deadline-1
typed = ["north", "east", "south", "quit"]

def ask(prompt):
    """Stand in for input(): give back the next typed answer."""
    answer = typed.pop(0)
    print(prompt + answer)
    return answer

exits = {
    "hall": {"north": "library"},
    "library": {"south": "hall"},
}

room = "hall"
while True:
    print("You are in the", room + ". Exits:", ", ".join(exits[room]))
    move = ask("Where now? ")
    if move == "quit":
        break
    if move in exits[room]:
        room = exits[room][move]
    else:
        print("You cannot go", move)
print("Goodbye.")
```

That is enough. It proves the pieces connect: the rooms, the loop, the
asking, the moving. Release 2 might add rooms, things to pick up, and a
way to win. Release 3 adds docstrings, tests for the parts that can be
tested, and a change log a stranger could follow. Because Release 1 was
so small, you find out in week two, not week six, when two people's code
does not fit together.

## Working on one thing at once

When three to five people edit the same project, their changes will
clash. No way of organising a team stops this completely, but you can be
ready for it.

1. **Split the work by what each piece does,** not by who is good at what.
   "Ciara does the rooms, Dev does the menu, Maeve does the score" gives
   everyone something to build, and a clear edge where one piece meets
   the next. "Ciara does the hard parts" gives you one person doing the
   project and three watching.
2. **Agree the edges before anybody writes code.** If Dev's menu will call
   Ciara's function, decide now what it is called, what goes in, and what
   comes out.
3. **Write that agreement down,** in the interface agreement from
   [From cells to a program](tutorial:from-cells-to-a-program#templates-for-a-team).
   Now both people can build against it, and neither has to wait.
4. **Tell the team what you are working on.** Two people editing the same
   file at the same time is the most common way a week's work is lost. A
   short message like "I'm in the scoring code this evening" prevents
   nearly all of it.

The agreement in steps 2 and 3 is worth more than any amount of planning
about features. It is what lets four people work at the same time, instead
of one after another.

## Reviewing each other's work

**Before each release, read each other's code.** The point is to find out
whether the code can be read, not to find fault. If you cannot follow what
a function does, that tells you something about the function, not about
you, and it is much cheaper to find out now than later.

A polite review says "looks fine". A useful one asks questions:

1. **Can I tell what this does without asking?** If not, the fix is
   usually a better name or one sentence of docstring, not more code.
2. **What happens if this gets something unexpected?** An empty list, a
   zero, a word where a number was expected.
   [Reading an error message](tutorial:reading-an-error-message) and
   [Finding bugs in bigger programs](tutorial:when-it-goes-wrong) are the
   pages for this. Somebody using your program will meet every one of
   them.
3. **Have we already written this somewhere else?** Two people often solve
   the same problem separately. That is normal, and worth catching.

Then **write down what you agreed**, in a line or two: "We are keeping the
two scoring functions separate for now." In three weeks, nobody will
remember whether that was a decision or an accident. The review checklist
on [From cells to a program](tutorial:from-cells-to-a-program#templates-for-a-team)
has these questions ready to copy.

### After the last release

The review that matters most comes at the end, and it is about how you
worked together, more than about what you built. These are for you to
answer, in your own words:

- What went differently from what you expected?
- Where did the time go, compared with where you thought it would go?
- With the same brief and a fresh start, what would you do differently?
- What did somebody else in the team do that you would like to be able to
  do?

Take the last one seriously. Building something with three to five people
is the closest this course comes to how software is made in real jobs, and
most of what people take away from it is something they watched somebody
else do.

## A last thing

The hardest problem in a team project is almost never technical. It is
almost always somebody who is stuck and does not say so, for two weeks,
because they think everybody else understands. It happens in professional
teams all the time, and it is the most expensive thing that goes wrong.

If you are stuck, say so on the same day. If somebody in your team has
gone quiet, ask them how they are getting on. Neither is only a small
kindness: together, they are the skill this learning outcome is about.

## Where to read more

Fowler, M. (2006). *Continuous Integration*.
<https://martinfowler.com/articles/continuousIntegration.html>. The
professional version of "release early, release small": merging and
testing everyone's work together all the time, rather than once at the
end.
