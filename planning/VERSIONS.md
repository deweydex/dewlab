# Versions, archives, and what a student sees

Josh's proposal, in his words:

> What if each page (meaning each tutorial) had a version number dropdown at the
> top which would allow students to roll back to previous versions and for us to
> mark versions as staged or beta and select a default version in settings based
> on date (so that users have continuity but also see there are other options of
> the tutorial)? That means instead of delete we would just have an archive with
> deprecated tutorials and versions.

Yes, and the last sentence is the best part of it. This is a plan, not a build.

---

## First, a fact that changes the arithmetic

**Nothing has been published to a class yet.** No student has saved work in
dewlab, because dewlab has not been in front of anyone. Josh said so while this
was being written, and it is worth stating at the top because several arguments
below are about protecting saved work, and right now there is none to protect.

Two things follow, and the second is the useful one.

**The problems below are real but not yet painful.** Deleting a tutorial would
strand a student's work; today it strands nobody. That does not make the design
wrong — it means the fix is cheap now and expensive later, which is the best
possible time to make it.

**The window for breaking changes is open, and it closes on the day the first
class uses this.** Everything keyed to a slug, a cell id, or a version can be
changed today for free. From first use, each of those becomes a contract:

- **Slugs** are in every URL and every saved record. Renaming one after first use
  breaks links and orphans work; renaming one today costs a `git mv`.
- **Cell ids** are the keys a student's answers are stored under. The convention
  — `section-slug-n` — is fixed from first use. If it should be something else,
  now.
- **The save record format** itself. It carries a version, a saved-at time, and
  an array of cells. Changing its shape later means either migrating records in
  the browser or dropping them.
- **The version field**, which is changing to a dated string anyway, and can do
  so at no cost precisely because of this.

None of those obviously needs changing. But they should be looked at once,
deliberately, before the window shuts — and that look is worth scheduling rather
than assuming.

---

## What it is actually solving

Three separate problems, worth keeping separate because they have different
answers.

**Continuity.** A student halfway through a tutorial should not have the ground
move. Today, if a tutorial is edited between two sittings, the student gets the
new one with a notice saying their work "may not line up". That notice is an
apology for a thing we could simply not do to them.

**Reversibility.** Right now the only way to remove a tutorial is to delete the
file, and deleting it strands every student who saved work in it — their work
sits in local storage keyed to a page that no longer exists. There is no way
back and no trace that it ever existed. That is the worst property in the whole
system, and it is why I left a delete button out of the editor.

**Trying something without inflicting it.** Josh wants to draft a replacement
for a tutorial and show it to one group, or to a colleague, without it becoming
what everyone sees.

The version dropdown addresses the first, the archive addresses the second, and
staged/beta addresses the third. They share machinery, which is why they belong
in one plan, but they are not one feature and should not ship as one.

---

## The distinction the whole thing rests on

**A version is a release, not a save.**

If every edit made a version, the dropdown would list forty entries per tutorial
within a term, the repository would be unreadable, and nobody could answer "which
one should I be on?". The proposal only works if versions are rare and
deliberate: the ones a cohort actually saw.

That is already close to the rule in `VERSIONING_AND_PROGRESS.md`, which says
`version` is incremented "whenever executable-cell content changes — not for
prose-only edits". The new rule is stricter and simpler:

> A new version exists when we decide a student should be able to go back to the
> old one. Everything else is an edit.

Fixing a typo is an edit. Rewriting section 3 and replacing two exercises is a
version. In practice that means two to four versions per tutorial over a year,
not one per commit — which makes a dropdown legible and the repository still
readable.

Git already holds every edit. This is not a replacement for git; it is a much
smaller, curated, student-facing set on top of it.

---

## The control on the page: not hidden, but conditional

I first argued the picker belonged in Settings and the page should carry only a
quiet line. Josh pushed back — he wants a clue, on the page, that other versions
exist — and he is right. What I was avoiding was clutter, and there is a better
way to avoid it than hiding the control.

His sketch was an invisible triangle beside the title that appears on hover.
**The invisibility is the problem, not the placement.**

- **Hover does not exist on touch.** A good share of these students read on a
  phone. An affordance that only appears on hover is not subtle to them, it is
  absent — which defeats the one thing it is for.
- It is also awkward for keyboard and screen-reader users, who get either
  nothing or a control that announces itself with no visible counterpart.

The fix is to make the control **conditional rather than invisible**:

> A tutorial with one version shows nothing at all. A tutorial with more than
> one shows a small, always-visible marker beside the title.

That gives exactly the clue Josh wants, on the page, where he wants it — and it
costs nothing on single-version tutorials, which is most of them most of the
time. The clutter problem solves itself, because the control only exists where
there is something to choose.

So both, and they are not alternatives:

- **Beside the title**, when and only when there is more than one version: the
  current version's date, and a marker that opens the list. Current version
  marked, others in date order, newest first.
- **In Settings**, always: the same list, plus the one site-wide switch that has
  no natural home on a page — *stay on the version I started* against *always
  show me the newest*.

## Version numbers that carry their date

Josh: *"version should be user readable, perhaps using numbers and dots that
correspond to dates and the number of the change at the end — 2026.08.20.5 for
example."*

**Yes, and I was wrong to resist it.** I argued the integer had to stay because
it is written into every saved record and compared on restore, so changing its
type would break records already in students' browsers. That is not what the
code does. The comparison is:

```js
versionChanged: String(record["tutorial-version"]) !== String(currentManifest.version)
```

Both sides are stringified and compared for equality — not ordering. A string
version works with it unchanged. And the restore itself matches on cell id, not
on version, so nothing about a student's saved work depends on the type at all.

The real migration cost is one spurious notice: a student who saved against
`version: 1` and returns to `2026.08.20.1` is told once that the tutorial has
been updated, when it has not. Their work still comes back. That is a fair price
for a field a person can read.

So the field becomes `2026.08.20.1` — year, month, day, and which release of that
day. Zero-padded, so it sorts by date on sight.

**This removes a field rather than adding one.** The layout above proposed both
`version:` and `released:`. If the version *is* the date, `released:` is
redundant, and two fields that can disagree become one that cannot. Where they
would have differed — a beta prepared on one day and made live on another — the
date is when the version was made, and `status:` carries the rest.

The trailing number earns its place only occasionally: with a version being a
release rather than a save, two in one day happens when you publish, spot
something, and publish again. Rare, but the case that would otherwise collide.

**Sorted on its parts, not as a string.** `2026.08.20.10` sorts before
`2026.08.20.9` lexically, which is wrong the first time it ever matters. Parse
the four numbers and sort on those.

And the label a student reads stays prose: **"20 August 2026"** in the list, with
the dotted form kept for the file, the frontmatter and the URL. A date they can
read beats a date they have to parse, and neither of us wants `2026.08.20.1`
above a tutorial title.

## Instead of warning, tell them what will happen

Josh's sketch has a warning on switching: going back *should* keep their work,
but they might want to export first, just in case.

I would not ship that sentence. If we are not confident the work survives, the
feature is not ready; and "just in case" teaches a student to distrust a thing
that is actually deterministic. The restore matches on cell id — it either
matches or it does not, and we can know which **before** they switch rather than
after.

The manifest already carries every cell's id. Adding each version's ids to it
costs a few hundred bytes, and then the page can say the true thing:

> **15 September 2026** — 6 of your 8 answers carry over. Two cells are not in
> that version, so their answers will not appear. *(Export a copy first.)*

Specific, checkable, and it turns a vague anxiety into a decision. The export
link stays, as an offer rather than an apology.

## What already works in our favour

**Saved work is keyed by cell id, not by version.** The restore logic in
`tutorial-runtime.js` matches on `task_id`, so a student rolling back to an
earlier version sees the work they did in any cell the two versions share. A
cell that only exists in the newer one is simply absent; one that only exists in
the older one comes back. Nothing needs to change for that to be true.

This sharpens something the editor already warns about. A cell id is not a
filename — **it is a promise that this is the same exercise**. Keeping the id
across a version means "your answer still applies". Changing it means "this is a
different question now". The rename warning I built for the editor is really
enforcing a contract between versions, and the plan should say so.

**Hosted pages are cheap; downloads are not.** Measured on the current site: a
hosted tutorial page is 19KB, a standalone downloadable copy is 0.7MB — forty
times larger, because it inlines everything. The whole `site/download/` tree is
45MB against 460KB for the hosted pages.

That settles a question before it is asked. **Every live version gets a hosted
page. Only the default gets a standalone copy and a place in the series zip.**
Four versions of nineteen tutorials costs about 1.5MB hosted, and nothing extra
to download.

---

## The file layout

A tutorial becomes a folder once it has more than one version, and not before:

```
tutorials/mit-pdp-maths-prog-integration/
  first-steps.md                  # one version: unchanged, as today
  cracking-equations/             # more than one: a folder
    cracking-equations.md         # the current one
    v1.md                         # frozen when v2 was released
    v2.md
```

The single-file form stays legal and stays the common case. Nothing has to move
until it needs to, which means this change costs nothing on the day it lands.

Each frozen file keeps the frontmatter it had, with the version now carrying
its own date (see below) and one field added:

```yaml
version: 2026.09.15.1       # year, month, day, which release of that day
status: live                # live | beta | archived
supersedes: 2026.06.02.1    # optional, for the "what changed" note
```

`status` carries the whole lifecycle. Josh asked for *"draft, archive,
published"*; the set below is those three plus one, and the reason to separate
draft from beta is worth stating because it is a property of the site rather
than a preference.

**The site is static and public. Anything built has a URL, and a URL is
public.** There is no server, no login, and no way to show a page to one person.
So "not finished yet" has exactly two honest meanings, and they differ by
whether a URL exists at all:

| Status | Built? | In the reading order | What it is |
|---|---|---|---|
| **draft** | **no** | no | In the repository, not on the internet. Nobody can reach it, including you — you read it in the editor or a local build. |
| **beta** | yes | no | Reachable by anyone with the link, never the default, and the page says so unmissably. This is showing a colleague, or one group. |
| **live** | yes | yes | The normal state. Eligible to be the default. |
| **archived** | yes | no | Was on the course, is not now. Still holds saved work, still answers old links. |

Beta and archived are the same shape pointing opposite ways: not yet, and no
longer. Draft is the one that is genuinely different, because it is the only
state where no page exists.

If that distinction turns out not to earn its keep, **beta is the one to keep**:
a draft nobody can look at is less useful than a draft you can send to someone.
Collapsing them costs one line.

Actually deleting a file remains possible and remains a deliberate act, for the
case where something was published in error. Archiving is the default gesture.

---

## URLs, which are the part that can go wrong

The current path is the default version and does not change:

```
tutorials/<module>/<slug>.html          → whatever the default resolves to
tutorials/<module>/<slug>/v1.html       → a specific version
tutorials/<module>/<slug>/v2.html
```

Every link that exists today keeps working and keeps meaning "the current one".
That matters more than it sounds: the `tutorial:` links inside tutorials, the
topic tree's "taught in" links, the curriculum map, and anything a student
bookmarked all point at the unversioned path, and all of them want the default.

A versioned page carries `<link rel="canonical">` at the default, so the
duplicates do not compete in search. **This shipped in step 3 rather than step
2, where it is written** — step 2 landed without it and nobody noticed until the
step 3 review. See DECISIONS_LOG 7.34.

---

## The default, and what "based on date" means

Josh said the default should be selectable in settings, based on date. Pulling
that apart, there are two different things wearing one name.

**A cohort pin** is what a teacher wants: everyone in this class sees the
material as it stood on the first of September, so the term is stable and two
students comparing screens see the same thing. That is not a per-student
preference — it is a property of the course, and a student should not be able to
drift off it by accident.

**A personal choice** is what an individual wants: "show me the newest", or
"leave me on what I started".

The site is static, so there is no server to hold a cohort setting. But the
cohort pin already exists in the data and is barely used: **`year: "2026-2027"`
is in every tutorial's frontmatter.** A build is for a year. So the honest
mechanism is:

- The **build** resolves, for each tutorial, the newest `live` version whose
  own date is on or before the year's cut-off. That is the default, and
  it is baked in rather than computed in the browser.
- The **student** may override it per tutorial, and their override sticks. The
  default of that override is "the version I started", which is the continuity
  Josh is after.
- **Settings** carries one switch for the whole site — *stay on the version I
  started* (the default) or *always show me the newest* — plus the per-tutorial
  list.

That gives a teacher a stable term without any server, and gives a student who
wants the latest a way to get it.

---

## What has to change, honestly

This is the largest structural change since the order file, and larger than the
editor. It touches:

- **`build.py`** — resolve the default per tutorial, build a page per live
  version, write the version list into the manifest, keep the unversioned path,
  restrict standalone copies and zips to the default, and teach `series_of` that
  archived tutorials are not in the reading order.
- **`tutorial-runtime.js`** — remember the version a student started, honour the
  pin, render the "newer version available" line, draw the marker beside the
  title when there is more than one version, count how many saved answers carry
  over to each option, and put the same list plus the site-wide switch in
  Settings.
- **The editor** — "release a new version" as an explicit action distinct from
  saving an edit, "archive this tutorial", and "mark this version beta". This is
  where the feature is actually used, and it is the reason the editor came
  first.
- **The curriculum map** — coverage is read from the default version only.
  Reading `covers:` from every version would make an outcome look taught by four
  things.
- **The topic tree** — links point at the default.
- **Tests** — the resolution rules are the kind of logic that is wrong in ways
  nobody notices for a term.

## The order to do it in

1. ~~**Archive.**~~ **Done.** `status: archived` in the frontmatter. The page
   stays built and reachable and still holds whatever a student saved in it; it
   leaves the reading order, loses its previous and next, drops out of the
   series archive, is listed under *Archive* on the contents page, and opens
   with a notice. It no longer counts as coverage, and listing it in an order
   file stops the build. See DECISIONS_LOG 7.17 to 7.19.
2. **Versions as releases.** The folder layout, the `released`/`status` fields,
   the default resolved at build time, versioned pages built, unversioned paths
   unchanged. No student-facing control yet — the default is simply correct.
3. ~~**Continuity, the notice, and the picker.**~~ **Done.** A reader goes back
   to the release they last worked in; the marker sits under the title on the
   tutorials that have more than one release and nowhere else; Settings carries
   the same list plus the one site-wide switch; and every option says how many
   of that reader's answers carry over to it. See DECISIONS_LOG 7.30 to 7.33.

   Two things came out differently from what is written above. The pin is **the
   release you last worked in**, not the one you started — working somewhere has
   to outrank an older pick, or a stale pick keeps pulling a reader off the page
   they are on. And there is **no separate "newer version available" line**: the
   notice build.py already writes on a superseded page says which release this is
   and links to the current one, so the runtime adds the carry-over count to that
   box rather than putting a second box beside it saying nearly the same thing.
4. ~~**Beta, and the editor actions.**~~ **Done.** Archive and mark-beta landed
   with the status control (DECISIONS_LOG 7.27); release is the new part.

   Releasing freezes the release students have and publishes the buffer as a
   new one dated today. A tutorial becomes a folder of releases the moment it
   has a second, and not before. The editor **proposes** rather than acts: it
   knows whether cells appeared, disappeared or changed id since the last
   release, and says so when they did — which is Josh's automatic bump with the
   one decision that needs a person left to the person.

   Step 4 also had to fix something step 2 left behind: the editor did not know
   versioned folders existed, so a tutorial with a second release opened as an
   empty buffer. See DECISIONS_LOG 7.39 to 7.41.

Each step is useful on its own, and each is a pull request. Steps 1 to 3 have
landed, and step 4 follows them directly — Josh's call on 23 August, against my
suggestion of waiting.

He is right that waiting had no content to it. The argument for a pause was that
2 and 3 might teach us something before the editor commits to their shape, but
neither has been in front of anyone yet, so a pause would produce no information
and delay the part that makes the feature usable. Releasing, archiving and
marking a beta by hand means editing frontmatter and moving a slug between two
lists in an order file — which is exactly the two-file edit the editor exists to
stop anybody doing by hand.

Step 2 was where the cost was. Everything above about resolving a default, building
a page per version, and keeping the unversioned URL meaning "the current one"
happens there, and steps 3 and 4 are comparatively small on top of it.

---

## What I would want decided before step 2

**Three of these are now settled**, and the sections above have been rewritten
rather than annotated: the editor archives rather than deletes; it may edit
frontmatter; and the version field itself is the readable date.

1. **Is "a version is a release" the right rule**, or do you want a version per
   meaningful edit? The first keeps the dropdown short; the second keeps a fuller
   history but needs the picker to be collapsible by date.
2. ~~Does a student get to pick a version at all?~~ **Settled: yes.** Josh chose
   a picker on the page, and the conditional marker above is how it avoids
   cluttering the tutorials that have only one version. Worth knowing that the
   picker is the cheap half — perhaps forty lines of script and some styling.
   The cost of this whole feature is in the build resolving versions, and both
   designs pay it in full. "Settings is the easy win" is not quite true.
3. **The "what changed" note.** Written by hand per release, or generated from
   the diff? By hand is better to read and one more thing to write.
4. **Does an archived tutorial keep its place in the topic tree**, marked as
   archived, or leave the map entirely? It still teaches the outcome it taught.
5. **How long do archived versions live?** Forever is the honest default and
   costs 19KB each. A cut-off would need a reason.


---

## Storing it: one field, not two

Josh: *"how do you suggest we store and manage versions and dates? Just two
fields?"*

**One.** A dotted date carries three of the things we need at once:

| What we need it for | Where it comes from |
|---|---|
| Identity — which version is this, in a URL and a saved record | the string itself |
| Order — which is newer | the four numbers, parsed |
| When — the date a student reads | the first three numbers |
| State — draft, beta, live, archived | `status:` |
| Lineage — what it replaced, for "what changed" | `supersedes:`, optional |

So the whole of it is `version:` and `status:`, with `supersedes:` where a
"what changed" note is worth writing. A separate `released:` would only be a
second copy of the first three numbers, and two fields that can disagree are
worse than one that cannot.

### The bump is the release, and it is a proposal rather than an act

Fully automatic bumping would produce a version per save, which is the thing
this whole plan rejects. So:

- **The date is stamped when you release, not when you start editing.** An edit
  that takes a fortnight is dated the day it goes out.
- **The live file keeps its version between releases.** Editing the current
  tutorial does not change its version — the version students are seeing and the
  version in the file stay the same thing.
- **The editor proposes.** It knows what changed since the last release: whether
  cells were added, removed, or renamed. When they were, it says so and offers
  to release. When only prose moved, it stays quiet. That is Josh's automatic
  bump, with the one decision that needs a person left to the person.
- **The trailing number is computed**, not typed: if a version already carries
  today's date, the next one is the next number.
- **Today means today where you are.** The date comes from the browser's local
  clock, so a release at half past midnight in Dublin is dated the day Josh
  thinks it is, not the day UTC thinks it is.

### Where one field strains, and it is worth knowing

A beta made on the 20th and promoted to live on the 25th has a version saying
the 20th, but students first saw it on the 25th. That matters for exactly one
thing: a cohort pin resolving "the newest live version released on or before the
22nd" would include it, wrongly.

**The fix is to re-stamp on promotion.** A version's date becomes the day it
became the thing students get. The cost is that promoting a beta changes its
URL and orphans any work saved against it — and betas are seen by a handful of
people by definition, so that cost is small and bounded.

If that trade reads badly, the alternative is the second field after all:
`version` as the date it was written, `released` as the date it went live. It
buys accuracy for betas and costs the guarantee that the two can never disagree.
I would take the re-stamp.

---

## Linking a new tutorial to an old one

Josh, raising it as a later task:

> I'm not sure how we can get a new tutorial to link to the older ones without
> some sort of automatic glossary?

**Most of that glossary already exists**, which makes this smaller than it
sounds and worth doing sooner than "later".

`planning/curriculum/topics.yaml` holds 68 topics with plain-English
descriptions. Each tutorial's `covers:` frontmatter says which section teaches
which outcome. `taught_where()` in `build.py` already turns that into *outcome
code → the exact tutorial section that teaches it*, and the topic tree already
draws links from it. Nothing new has to be written down; it has to be made
linkable.

**The proposal is one new link form**, beside the `tutorial:` one that exists:

```markdown
As we saw when we met [graphing functions](topic:MIT-3.2) …
```

The build resolves it through `taught_where()` and fails if nothing teaches that
topic — the same bargain `tutorial:` already makes, and the same reason to trust
it.

**Why this matters more once versions exist.** A `tutorial:` link points at a
page. A `topic:` link points at a *concept*, and the build works out which page
currently teaches it. So:

- Archiving the tutorial that taught something does not break the link. It
  breaks the *build*, loudly, which is the correct outcome: the link now points
  at a gap in the course, and somebody should know.
- Re-releasing a tutorial as a new version does not break the link at all.
- Splitting one tutorial into two moves the link to whichever now teaches the
  topic, without touching the prose that refers to it.

That last property is the one that pays for the whole idea. The re-plan of the
series — splitting tutorials, adding the maths ones, slotting the conversions in
— is exactly the operation that breaks hand-written cross-references, and this
is the thing that survives it.

**In the editor**, the same data becomes a list to insert from while writing,
which is the half Josh was actually asking for.

**Not yet decided:** what a `topic:` link does when a topic is taught in two
places (nearest earlier one, or the first?), and whether it should be allowed to
point at a topic nothing teaches yet — useful while drafting a series, and a
hole in the guarantee.
