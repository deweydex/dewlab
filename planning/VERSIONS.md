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

## Where I disagree, and it is about the dropdown

**A version picker at the top of a student-facing page is the wrong default.**

Most students will never touch it, and a control they do not understand sitting
above the title is noise on a page whose job is to teach. Worse, it invites the
one behaviour we do not want: a student idly picking an old version and working
in it for a fortnight.

But the reason underneath the proposal is right. So invert it:

- **Continuity should be automatic.** The first time a student opens a tutorial,
  they are pinned to the version they started. A later release does not move
  them. No control, no decision, nothing to understand.
- **A new release announces itself, quietly.** A line under the title: *"A newer
  version of this tutorial is available. See what changed."* That is where the
  choice lives — at the moment it is relevant, phrased as an offer.
- **The full list lives in Settings**, with the other things a reader might want
  once and then never again. Same place as the theme and the width.

So: keep every capability Josh described, move the prominence. The picker is the
escape hatch, not the front door. If that reads as too subtle in practice, the
line under the title can become a small inline control later — but starting
prominent and retreating is harder than the reverse.

---

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

Each frozen file keeps the frontmatter it had, plus:

```yaml
version: 2
released: 2026-09-15        # when students first saw it
status: live                # live | beta | archived
supersedes: 1               # optional, for the "what changed" note
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
  `released` date is on or before the year's cut-off. That is the default, and
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
  pin, render the "newer version available" line, and put the version list in
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

1. **Archive.** No versions at all: a tutorial can be marked archived, drops out
   of the reading order, stays built and reachable, and says what it is. Small,
   self-contained, and it removes the worst property in the system today.
2. **Versions as releases.** The folder layout, the `released`/`status` fields,
   the default resolved at build time, versioned pages built, unversioned paths
   unchanged. No student-facing control yet — the default is simply correct.
3. **Continuity and the notice.** Pin a student to what they started; show the
   "newer version available" line; the full list in Settings.
4. **Beta, and the editor actions.** Release, archive, and mark-beta as things
   Josh can do from the editor rather than by hand.

Each step is useful on its own, and each is a pull request. Step 1 could land
this week; step 4 is not worth starting until 2 and 3 have been lived with.

---

## What I would want decided before step 2

1. **Is "a version is a release" the right rule**, or do you want a version per
   meaningful edit? The first keeps the dropdown short; the second keeps a fuller
   history but needs the picker to be collapsible by date.
2. **Does a student get to pick a version at all, or only to stay put?** I have
   argued for both, with the picker in Settings. The simpler system — pinned to
   what you started, no picker, no list — is genuinely defensible and about a
   third of the work.
3. **The "what changed" note.** Written by hand per release, or generated from
   the diff? By hand is better to read and one more thing to write.
4. **Does an archived tutorial keep its place in the topic tree**, marked as
   archived, or leave the map entirely? It still teaches the outcome it taught.
5. **How long do archived versions live?** Forever is the honest default and
   costs 19KB each. A cut-off would need a reason.
