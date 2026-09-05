# Reporting a mistake or a bug

If you have found something wrong, or something that was hard to follow,
telling us is a help. You do not need to be sure it is wrong before you say
so. Half of what turns out to be a real bug starts as somebody saying "this
looked odd to me". That is enough.

---

## The quick way: from the page itself

Most pages carry a line at the foot, "Something wrong on this page? Tell
us." Click it and you get three choices.

**I have a question.** Not wrong, just something you want explained. This
one goes to Discussions rather than an issue, so an answer stays where
somebody with the same question can find it later.

**It gives an error.** For a cell that will not run, a button that does
nothing, or anything else that does not work. Opens GitHub's own issue form,
with the page and its version already filled in and this kind already
picked. See ["Before you report a page that will not
run"](#before-you-report-a-page-that-will-not-run) first.

**The page is wrong, or I could not follow it.** For a mistake or
something confusing. Same form, same fields filled in, this kind picked
instead.

Whichever choice you take, all you need to add is the one thing that
matters: what happened.

If the choices are not there, or your report is not about one particular page
(an idea, a suggestion, something about the site as a whole), opening an
issue yourself works the same way — **[the issue tracker on
GitHub](https://github.com/deweydex/dewlab/issues)**. You need a free
GitHub account to post one. Have a quick look at the open issues first
in case somebody has already reported it — if they have, adding what you
saw to that issue is more useful than starting a new one. The rest of
this page covers what is useful to include, either way.

The reporting line can be turned off for a while if reports need to pause,
for example while something is being fixed. When it is off, this page and
the issue tracker itself still work exactly as before.

---

## An even quicker way: from a cell

Every cell has a small circle in its own bar, next to its hint if it has
one. Click it to open the same three choices, already filled in for this
cell. Choose "It gives an error," and your code exactly as you have it,
and whatever the cell last showed, are both included in the report. You
do not need to copy either one yourself. That report link opens a form
on GitHub.

A very long cell or a very long error is cut short rather than left out,
so the link stays short enough for GitHub's own form to open. Paste the
rest yourself if the missing part matters.

---

## Three kinds of problem

It helps to know which one you are looking at, because what is useful to
include is different for each.

**A mistake in the material.** A wrong answer, a number that does not come
out the way the page says, a spelling error, an explanation that contradicts
itself, a link that goes nowhere useful, a bibliography entry that is out of
date. If you can, say which tutorial and which section, and quote the line.

**Something on the site not working.** A cell that will not run, a chart that
does not appear, a button that does nothing, saved work that vanished, a page
that looks wrong on your phone, an error message you did not cause. See the
checklist below.

**Something confusing.** Not wrong exactly, but you had to read it three
times, or it assumed something it never explained, or the order made no sense.
These are worth reporting too. A tutorial that is technically correct and
impossible to follow is still not doing its job.

---

## What is useful to include

For a mistake in the material, the page and the sentence is usually enough.

For something not working, these five things save a lot of back-and-forth:

1. **Which page** — the address in the browser's address bar, copied and
   pasted.
2. **What you did** — the steps, in order, from opening the page. "I pressed
   Run on the second cell" is enough.
3. **What you expected to happen.**
4. **What happened instead** — including the exact error text, if there was
   any. Copy and paste it rather than describing it, and a screenshot is
   welcome.
5. **Your browser and device** — Chrome on a school PC, Safari on an iPhone,
   Firefox on a Mac. Some problems only happen in one place, and this is often
   the fastest clue.

If it only happens sometimes, say so, and say what was different the times it
did happen. A problem that comes and goes is harder to find, and knowing that
it comes and goes is part of the report.

---

## Before you report a page that will not run

Two things explain most of it, and both are quick to check.

**A page needs the internet the first time.** Python itself is fetched when a
page first opens, including in a downloaded copy. On a slow connection the
first run can take a while.

**You can compare with the original code.** Every cell has a reset button that
restores the code the tutorial started with. If the cell works again after
that, an edit was the cause rather than the page itself. If it helps,
comparing the two versions may show where the difference is. This does not
prove where the problem began, and questions about your own edits are welcome
too.

If neither of those explains it, report it.

---

## Suggestions and questions

The same issue tracker takes ideas, requests and questions, not only faults. A
topic you wish had a tutorial, a practice page that needs more problems, an
explanation you think could be clearer — all of that is welcome, and none of it
needs to be phrased as a complaint.

---

## If you want to fix it yourself

You are welcome to. A small correction is often quicker to send as a pull
request than to describe.

- For a change to a tutorial's text or code, read
  [`WRITING_TUTORIALS.md`](WRITING_TUTORIALS.md) — the format, and what to run
  before you open the pull request.
- For a change to the site's own code, read
  [`../CONTRIBUTING.md`](../CONTRIBUTING.md) and then
  [`../ARCHITECTURE.md`](../ARCHITECTURE.md).

Mentioning the issue number in the pull request ties the two together. If there
is no issue yet, the pull request on its own is fine.
