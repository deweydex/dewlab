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

`status` is the whole of staged/beta/archive:

- **live** — the normal state. Eligible to be the default.
- **beta** — built, reachable by direct link, never the default, and the page
  says so at the top in a way nobody can miss. This is Josh showing a colleague.
- **archived** — built, reachable, not in the reading order, not in the zip,
  marked as superseded. This is what replaces delete.

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
duplicates do not compete in search.

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
3. **Continuity, the notice, and the picker.** Pin a student to what they
   started; show the "newer version available" line; the conditional marker
   beside the title; the same list plus the site-wide switch in Settings; and
   the "6 of your 8 answers carry over" count on each option.
4. **Beta, and the editor actions.** Release, archive, and mark-beta as things
   Josh can do from the editor rather than by hand.

Each step is useful on its own, and each is a pull request. Step 1 has landed;
step 4 is not worth starting until 2 and 3 have been lived with.

Step 2 is where the cost is. Everything above about resolving a default, building
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
