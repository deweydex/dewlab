# How dewlab thinks

*A first draft, September 2026. Written to be argued with.*

dewlab has a great deal of written guidance. There is a style guide, a
writing guide of sixteen hundred lines, a decisions log of more than five
thousand, and a build that checks a couple of hundred things before it will
publish a page. Read end to end, all of that can look like a body of law, and
a new author could fairly conclude that the way to write a dewlab page is to
satisfy every clause of it.

That is not how the good pages were written. They were written by somebody
with one reader in mind, and most of the rules came afterwards, as notes on
what had worked on a real page and what had not. This document tries to put
the reasons back in front of the rules. Each chapter says what the project
believes about teaching this reader, where that belief came from, and how
far it bends.

Two kinds of rule are mixed together in the other documents, and the
difference between them is the reason this one exists. A page can break a
good number of the house habits and still be an excellent page. A page
cannot lose a student's saved work, publish a link to nowhere, or show an
answer that does not run. The first kind is advice, and an author with a
better idea should use it and say so. The second kind is enforced by the
build, and [What the machine holds you to](#what-the-machine-holds-you-to)
lists it, with the reason for each.

The mechanics — fences, cell ids, frontmatter — are in
[`WRITING_TUTORIALS.md`](WRITING_TUTORIALS.md). The short version of the
reasons, meant to be held up against a page before it ships, is the
[style guide](../planning/PEDAGOGICAL_STYLE_GUIDE.md). This is the long
version, for someone deciding whether to write for dewlab at all, or
wondering why a page they admire does something the guide seems to forbid.

---

<a id="the-reader"></a>
## The reader at ten at night

Everything here starts from one reader, described in the style guide's
[first section](../planning/PEDAGOGICAL_STYLE_GUIDE.md#who-reads-this): an
adult on a QQI Level 5 course in Dublin, often back in education after
years away, fitting study around work and family. In one room there is
somebody who has never programmed, somebody who has a degree in something
else, somebody reading in their second language, and somebody who has not
done mathematics since school and expects to be bad at it.

The guide asks you to write for that reader at home, at ten at night, when
nobody is there to ask. A page that works for them alone works in class too,
where a teacher can fill the gaps. The reverse is not true.

Most of what follows is a consequence of taking that person seriously, and
the same picture is the fairest test of any rule in this document. If a rule
serves that reader on your page, keep it. If following it would leave them
more confused or more alone, the rule is wrong for your page, and you should
break it and write down why.

---

<a id="being-wrong"></a>
## Being wrong is cheap here

The strongest belief in the project is that the site never tells a reader
they are right or wrong
([no verdicts](../planning/PEDAGOGICAL_STYLE_GUIDE.md#no-verdicts)). It shows
what their code did and, when they ask, what a solution does with the same
inputs. A mismatch is information about a line, not a judgement of a
person.

This was not the first design. The runtime once had a `check()` function that
ticked an answer, and it was retired (#314) because a tick is a verdict and
so is its absence. The comparison view that replaced it shows two values side
by side and draws no conclusion (`DECISIONS_LOG.md` 7.232). A prediction
always offers "I'm not sure yet", which leads to a hint rather than a
penalty (#313).

The reason is the reader. Many adults returning to education carry a verdict
from school that they have never put down, and a site that marks their
answers reopens it. Code offers something paper cannot: being wrong costs one
click, and the error message is a fact about one line on one run. The pages
lean on that. They make mistakes on purpose, say that they are doing it, and
enjoy what the mistake shows
([mistakes](../planning/PEDAGOGICAL_STYLE_GUIDE.md#mistakes)). They ask the
reader to write a guess down before running a cell, and then they wait,
because a guess made in writing turns the output into an answer to the
reader's own question
([predict, then run](../planning/PEDAGOGICAL_STYLE_GUIDE.md#predict-then-run)).

How far this bends: not far, as a principle. But the style guide's list of
quiet verdicts (*not yet*, *fair*, *strong*, *sound*) is a set of examples of
how judgement creeps into kind prose, not a list of banned words. Nothing
scans a page for them, and nothing should. The test is to reread your page as
the reader who has just got something wrong, and notice where it stings.

---

<a id="discover-then-name"></a>
## Discover, then name

Let a reader halve a sorted list until nothing is left to search, and then
say *binary search*. A name given before the experience is a word to
memorise; a name given after it is a handle for something the reader already
has ([discover, then name](../planning/PEDAGOGICAL_STYLE_GUIDE.md#discover-then-name)).

The same idea shapes a page and a series. A page moves from an example the
reader runs and changes, to one with a gap to fill, to a task with no
scaffold at all
([worked, completed, your own](../planning/PEDAGOGICAL_STYLE_GUIDE.md#worked-completed-own)).
Practice pages bring back two or three problems from earlier pages, because
remembering something a week later teaches more than a second example today
([nothing is taught once](../planning/PEDAGOGICAL_STYLE_GUIDE.md#nothing-taught-once)).
Every task has a first step anyone can take and no top
([low floor, high ceiling](../planning/PEDAGOGICAL_STYLE_GUIDE.md#low-floor-high-ceiling)).
A misconception worth teaching gets a "closer look" page of its own,
experiment first, instead of being flagged on somebody's answer
([closer look](../planning/PEDAGOGICAL_STYLE_GUIDE.md#closer-look)).

How far this bends: further than the guide's tone suggests. Some ideas need
their name early, because the reader will meet it in an error message or a
search result before the page can build up to it. A page that has to use a
word first can define it plainly and move on. The strong default is that a
page opens by running or showing something and asking about it. A page that
opens with a short story, or a question with no code in it, can work just as
well, and several good ones do.

---

<a id="plain-words"></a>
## Plain words

The readers include people working in their second language, and the guide
asks for prose a reader with about two thousand common English words can
follow ([plain language](../planning/PEDAGOGICAL_STYLE_GUIDE.md#plain-language)).
Its most useful single observation is that phrasal verbs — *work out*,
*carry on*, *turn out*, *set up* — are the main barrier for that reader, and
that a native speaker cannot see them. *Find*, *continue*, *happen* and
*prepare* each mean one thing. In Dublin, *out of order* means *broken*.

The guide's [say it directly](../planning/PEDAGOGICAL_STYLE_GUIDE.md#say-it-directly)
section comes from real pages: sentences that read well to the writer and
cost a second-language reader two readings. A verb instead of a noun made
from one; the point first, not after a colon; no closing line that restates
the paragraph cleverly. Tasks are invitations, not orders
([invitations](../planning/PEDAGOGICAL_STYLE_GUIDE.md#invitations)):
*Can you make the loop count backwards?* and not *Explain why…*

How far this bends: these are editing passes, not grammar. They are there to
catch the sentence you would not have written if you could see it through
the reader's eyes. The guide also asks for a voice that is
[plain and alive](../planning/PEDAGOGICAL_STYLE_GUIDE.md#plain-and-alive), and
the second word matters as much as the first. A page that reads as though a
person wrote it, and enjoyed writing it, is worth more than a page that
passes every check and reads like a form. When the two pull against each
other, keep the life and fix the sentence that loses the reader.

---

<a id="help-that-waits"></a>
## Help that waits

Help given too early saves a moment of frustration and costs the learning.
Help given after a real attempt teaches the habit of asking a question before
reaching for an answer. So a first hint asks — *what does the last line of
the error name?* — and only a later one gives steps. An answer sits in a fold
the reader opens for themselves, and says it is one good answer among others
([when a reader is stuck](../planning/PEDAGOGICAL_STYLE_GUIDE.md#stuck)).

A page may say, once, that a step is hard, as long as it says what to do
about it. A feeling named with nothing under it becomes a verdict on the
reader ([feelings](../planning/PEDAGOGICAL_STYLE_GUIDE.md#feelings);
`DECISIONS_LOG.md` 7.229).

How far this bends: the number of hints, their order, and whether a worked
cell gets one are judgement calls. The guide's advice to ration hints comes
from seeing pages where every cell grew one and readers learned to ignore
them. If your reader needs more help than that, give it.

---

<a id="code-on-the-page"></a>
## Code on the page

The [code section](../planning/PEDAGOGICAL_STYLE_GUIDE.md#code) of the guide
reads like a list of preferences, and most of it is: cells of five to fifteen
lines, names that read as words (`total`, not `s`), comments that say why
rather than what, shared setup written once instead of pasted again
([show only what changed](../planning/PEDAGOGICAL_STYLE_GUIDE.md#show-what-changed)).
Each came from a page where the opposite made a reader work harder than the
idea deserved. None is checked by a machine, and a thirty-line cell that
tells one story well is fine. The `cell-code-review` skill in
`.claude/skills/` exists to help an author look at their own cells, not to
gate them.

One line in that section is different in kind: every number is run. A number
in a page or an answer is executed before it is published, never reasoned
about. A test checks code, not prose, so a wrong number in an answer is the
one mistake nothing else would catch. That is why the build runs every
solution on every page before it publishes (#312), and why a handful of tests
read particular pages and check that the numbers their prose states still
follow from their own code. If you change such a page and one of those tests
fails, it is telling you that the prose and the code have drifted apart.
Change whichever is wrong, the test included.

---

<a id="worlds"></a>
## Worlds and wonder

A series offers several worlds — planets, the sea floor, pixel art, ciphers,
games — and the reader picks one. Wonder beats worthiness: a dinosaur's mass
beats a bank balance. Invented data is fine when the page says it is
invented ([the reader chooses the world](../planning/PEDAGOGICAL_STYLE_GUIDE.md#choice-of-world)).

The reason is that a reader who chose the context has a question of their
own about it, and a question of your own is where attention comes from.

How far this bends: worlds are a lot of work, and a page with one context
chosen well teaches better than a page with four thin ones. Start with one.
The mechanics of adding more are in
[`WRITING_TUTORIALS.md`](WRITING_TUTORIALS.md#worlds), and they can wait until
the page is good.

---

<a id="what-the-machine-holds-you-to"></a>
## What the machine holds you to

Here is the other kind of rule. There are three tiers, and it helps to know
which one you are looking at when something complains.

**What blocks a pull request.** The build refuses to publish, and the tests
fail, when a page would break for somebody. In practice that means:

- **Ids are contracts.** A cell's id, together with the tutorial's id (its
  folder name), is the key a student's saved work lives under. Rename either
  after a class has used the page and that work is gone. So every runnable
  cell needs an `id:`, no two cells on a page share one, and a cell in a world
  variant carries its world in its id (`DECISIONS_LOG.md` 7.23;
  [`WRITING_TUTORIALS.md`](WRITING_TUTORIALS.md#cell-ids)).
- **The page has to parse.** Frontmatter the build can read, fences that
  close, a hint or a solution that names a cell the page has.
- **What a page points at has to exist.** A link to another tutorial, an
  image, a dataset, an include.
- **Every solution runs.** For the reason in
  [Code on the page](#code-on-the-page).
- **Every image says what it shows.** An `alt` on every `<img>` tag, so a
  reader with a screen reader is not left out; `alt=""` marks one as
  decoration, and a markdown image gets that by default.

The test for putting something on this list is whether a reader's page breaks
without it: it does not load, a cell cannot run, a link or file points at
nothing, a number the page states is wrong, or the interface shows an error or
a broken layout. Anything that depends on what the author meant belongs in
the next two tiers.

A fold with none of the three styles the site draws (`DECISIONS_LOG.md` 7.52)
used to be on this list and is not any more: it still opens and its markdown
still converts, it just looks like the browser's own triangle, so the build
says so and carries on (7.295). If another refusal stops you writing the page
you want, and the page would still work, that is worth raising.

**What is reported and never blocks.** Some checks look after the project's
own planning rather than any page: the curriculum map in
`planning/CURRICULUM_MAP.md` staying current, the topic descriptions being
long enough to be worth reading, the outlines index listing every outline,
the links inside documents about the project. Some are house preferences
about tutorial prose, such as not naming an institution's assessments. These
are marked `advisory` in the test suite (`DECISIONS_LOG.md` 7.291). A pull
request shows them as a warning, and a maintainer tidies them up. To see them
yourself, run `python3 -m pytest -m advisory`.

**What is not checked at all, on purpose.** Everything in the chapters before
this one. Voice, verdict words, phrasal verbs, how many hints a cell has, how
long a cell is. A checker for most of these would be easy to write, and it
would make the pages worse, because authors would write to pass it. They are
for a person reading the page: you, a reviewer, and the
[checklist](../planning/PEDAGOGICAL_STYLE_GUIDE.md#checklist) at the end of
the style guide.

`python3 check.py tutorials/<id>` runs the first tier in about a second and
says in plain words what to fix
([`CHECK_YOUR_WORK.md`](CHECK_YOUR_WORK.md)). dewnote, the editor, draws the
same line in its own problems list: a problem is *blocking* only when the
build would refuse the page, and *worth fixing* otherwise.

---

<a id="disagreeing"></a>
## Disagreeing with this document

The decisions log records every choice "somebody could reasonably have made
differently", each with what it would cost to change. That phrase is an
invitation. The style guide has already been rewritten once from scratch,
from 579 lines to under 390, because the old one, however accurate, was not
doing its job: it had come to carry its own history, and the reasons were
hard to find under it (`DECISIONS_LOG.md` 7.189).

If a rule got in your way and your page is better for breaking it, say so: in
the pull request, in [`QUESTIONS.md`](../QUESTIONS.md), or as a new entry in
the log. A rule that good pages keep breaking is a rule that should change.
