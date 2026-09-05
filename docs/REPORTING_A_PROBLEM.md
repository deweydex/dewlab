# Reporting a mistake or a bug

If you have found something wrong, telling us is a help, and you do not need to
be sure it is wrong before you say so. Half of what turns out to be a real bug
starts as somebody saying "this looked odd to me". That is enough.

Everything goes in the same place: **[the issue tracker on
GitHub](https://github.com/deweydex/dewlab/issues)**. You need a free GitHub
account to post one. Have a quick look at the open issues first in case somebody
has already reported it — if they have, adding what you saw to that issue is
more useful than starting a new one.

---

## The quick way: from the page itself

Most pages carry a link at the foot, "Something wrong on this page? Tell
us." It opens the same issue tracker, on GitHub's own form, with the page
and its version already filled in for you. All you need to add is the one
thing that matters: what happened.

If that link is missing, or your report has no one page attached to it
(an idea, a question, something about the site as a whole), opening an
issue yourself works the same way. The rest of this page covers what is
useful to include either way.

The link can be turned off for a while if reports need to pause, for
example while something is being fixed. When it is off, this page and the
issue tracker itself still work exactly as before.

---

## Three kinds of problem

It helps to know which one you are looking at, because what is useful to include
is different for each.

**A mistake in the material.** A wrong answer, a number that does not come out
the way the page says, a spelling error, an explanation that contradicts itself,
a link that goes nowhere useful, a bibliography entry that is out of date. If
you can, say which tutorial and which section, and quote the line.

**Something on the site not working.** A cell that will not run, a chart that
does not appear, a button that does nothing, saved work that vanished, a page
that looks wrong on your phone, an error message you did not cause. See the
checklist below.

**Something confusing.** Not wrong exactly, but you had to read it three times,
or it assumed something it never explained, or the order made no sense. These
are worth reporting too. A tutorial that is technically correct and impossible
to follow is still not doing its job.

---

## What is useful to include

For a mistake in the material, the page and the sentence is usually enough.

For something not working, these five things save a lot of back-and-forth:

1. **Which page** — the address in the browser's address bar, copied and pasted.
2. **What you did** — the steps, in order, from opening the page. "I pressed Run
   on the second cell" is enough.
3. **What you expected to happen.**
4. **What happened instead** — including the exact error text, if there was any.
   Copy and paste it rather than describing it, and a screenshot is welcome.
5. **Your browser and device** — Chrome on a school PC, Safari on an iPhone,
   Firefox on a Mac. Some problems only happen in one place, and this is often
   the fastest clue.

If it only happens sometimes, say so, and say what was different the times it
did happen. An intermittent problem is harder to track down, and knowing that it
is intermittent is part of the report.

---

## Before you report a page that will not run

Two things account for most of it, and both are quick to rule out.

**A page needs the internet the first time.** Python itself is fetched when a
page first opens, including in a downloaded copy. On a slow connection the first
run can take a while.

**Try resetting the cell.** Every cell has a reset button that puts back the
code the tutorial came with. If the cell works again after that, the problem was
in an edit rather than in the page — which is not a bug, and is a normal part of
experimenting.

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
