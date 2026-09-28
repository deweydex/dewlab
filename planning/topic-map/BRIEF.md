# The dewlab map: brief for the topic search

dewlab's topic tree (`tree.html`, drawn from `planning/curriculum/topics.yaml`)
is being replaced by a map with several levels, and the topics under it are
being rebuilt from what the pages teach. The old topic list has 142 topics
keyed to QQI descriptor outcomes. It misses a great deal: 81 of 274 pages
claim no topic, whole courses (The Zen of Slashes and Surds, Full Stack)
appear nowhere, there is no fractions topic at all, and topic size is wildly
uneven ("Styling pages with CSS" swallows 20 pages; Powers and Logarithms are
separate topics).

Josh, who teaches from this, has said: where earlier decisions (in
`DECISIONS_LOG.md`, `topics.yaml`, `strands.yaml`, `topic-groups.yaml`,
`review/decisions.yaml`) conflict with a clean, unified structure, the unified
structure wins. Treat them as evidence, not as constraints.

**Do not edit anything in the repository.** Write only the file your task
names, under `planning/topic-map/`.

## The levels of the map

1. **Region.** A subject, like a country: number, algebra and graphs, shape
   and angle, chance and data, programming, making software, databases, the
   web, and whatever else the pages turn out to need. The whole site has
   perhaps eight to eleven. Search areas (below) are only a way of splitting
   the work; the integrator decides the final regions.
2. **District.** A neighbourhood inside a region, visible at middle zoom:
   usually three to ten topics, named the way a learner would name the area
   ("Fractions", "Powers and roots", "How a browser works", "Loops").
3. **Topic** (a town). Something a learner can say "I can do this" about,
   which a short check could confirm. Only topics carry `needs`.
4. **Step** (a street). One page, or one section of a page, inside a topic,
   in reading order. Visible when a town is opened. Steps never carry needs.
5. **Landmark.** A page that is not an idea: a project ("Make it: …",
   capstones), orientation ("Before we start", the FAQ, "How this course is
   built"). Attached to the topics it draws on.

## The size rule

**A topic is about the same amount of effort for the learner arriving at
it:** roughly one to three sittings, where a sitting is about one median
page (≈1,450 words with its cells; the inventory gives each page's word and
cell counts). Near the start, steps are small, because a beginner gets stuck
at small steps ("adding fractions with different denominators" is a whole
topic). Deep in, a topic can hold far more content, because the learner
carries earlier ideas as single chunks ("Matrices" can be one topic). Content
grows with depth; effort stays roughly level.

Apply it with these tests:

- **Split** when anything later needs only part of a topic, or when it spans
  more than about four teaching pages that do different things.
- **Merge** when nothing ever needs one without the other and they are always
  taught together.
- **A step, not a topic,** when nothing outside the topic needs it
  specifically ("the zero power" is a step inside the rules of powers unless
  something needs the zero power itself).
- **Not a topic** when the page is not an idea:
  - project or orientation page → a landmark;
  - a "closer look" page (it tackles one misconception) → a step with role
    `closer-look` in the topic whose misconception it addresses;
  - a context page (`kind: context`, background reading hung off an owner
    page) → a step with role `context` in the topic its owner teaches —
    unless it teaches an idea other topics would need, in which case it can
    be (or be part of) a topic of its own, possibly in another district.
- **Descriptor outcomes that are not ideas** (histories, surveys of tools,
  "personal attributes", "listing outcomes", "keeping evidence") come off the
  map. List each in `outcomes_culled` with what it becomes: a `landmark`, or
  `metadata` (kept only for the teacher's coverage view). Every descriptor
  outcome in `outcomes.yaml` must end up either served by a topic
  (`outcomes`) or culled with a reason, so coverage can still be reported.

Hidden topics are the other half of the job. Many pages teach ideas the old
list never named (fractions, the rules of powers, surds, log rules, scientific
notation, the number line, how a browser works, the cascade, Flexbox and
Grid, accessibility, Git, perceptrons, language models, and more). Find them
from what the pages teach — headings, glossary terms, first paragraphs, and
the page text itself when those are not enough — not from the descriptors.

## Needs

- `needs` means *you cannot sensibly start this without that*. Not "is taught
  earlier", not "is related". Every edge closes a door, so use as few as are
  true. Discover first, name afterwards: when a concrete activity is the
  reason to care about a named idea, the concrete one comes first.
- List direct needs only. If C needs B and B needs A, C does not list A.
- A need on a topic in another search area: write `ext:<plain name>`
  (`ext:fractions`, `ext:python-lists`) or, where an old topic still fits,
  `old:<code>` (`old:MIT-1.1a`). The integrator resolves these.
- Course reading order is evidence, not proof. The pair judgements in
  `planning/curriculum/review/` (pair-results*.md, decisions.yaml) are
  evidence about needs between old topics.

## Names and plain descriptions (a learner reads these)

- `name`: what a learner would call it, in one to six common words. No outcome
  codes, no jargon the learner has not met yet. Read
  `planning/PEDAGOGICAL_STYLE_GUIDE.md#voice` and `#plain-language`: a reader
  may be working in a second language.
- `plain`: one or two short sentences saying what it is, in common words.
  Reuse good text from the old `topics.yaml` `plain` where it fits; rewrite
  where it doesn't.
- District names follow the same rules.

## IDs

kebab-case, short, describing the idea: `adding-fractions`, `the-cascade`,
`python-lists`. Never an outcome code. Unique across the whole map, so prefer
specific over generic (`python-lists`, not `lists`; `sql-joins`, not `joins`).

## Evidence you have

- `planning/topic-map/generated/inventory-<area>.json`: your area's pages. Per page: `slug`,
  `title`, `kind` (tutorial, context, closer-look, project, orientation),
  `placements` (course and series), `words`, `cells`, `first_paragraph`,
  `headings` (with `anchor`), `glossary` (terms the page introduces), `covers`
  (the page's current outcome claims, by section anchor), `old_topics` (old
  topic codes those claims map to), `path` (the markdown file — open it when
  the inventory is not enough, especially to tell whether a page teaches one
  idea or several).
- `planning/topic-map/generated/inventory.json`: every page, all areas (to check a page you
  want to name in `elsewhere` or `ext:`).
- `planning/topic-map/generated/old-topics-by-area.json`: the old topics that fall in your
  area. Account for every one: in some new topic's `replaces`, or in
  `outcomes_culled`.
- `planning/curriculum/topics.yaml`, `outcomes.yaml`, `out-of-scope.yaml`,
  `topic-groups.yaml`, `courses/*.yaml`.

Practice pages are not in the inventory: they follow their tutorial.
World variants of a page are the same page.

## The file format (JSON)

```json
{
  "area": "number",
  "districts": [
    {"id": "fractions", "name": "Fractions", "blurb": "One sentence a learner could read."}
  ],
  "topics": [
    {
      "id": "adding-fractions",
      "name": "Adding and subtracting fractions",
      "district": "fractions",
      "plain": "Putting fractions together and taking one from another, first when the bottoms match and then when they don't.",
      "needs": ["equivalent-fractions"],
      "steps": [
        {"tutorial": "adding-slices", "section": null, "role": "teaches"},
        {"tutorial": "taking-slices-away", "section": null, "role": "teaches"},
        {"tutorial": "the-hidden-bracket", "section": null, "role": "closer-look"}
      ],
      "outcomes": ["MIT-2.1"],
      "replaces": [],
      "size": "Two short pages for a beginner; nothing later needs subtraction without addition, so one topic."
    }
  ],
  "landmarks": [
    {"tutorial": "before-we-start", "kind": "orientation", "at": ["fractions-as-parts"], "note": ""}
  ],
  "elsewhere": [
    {"tutorial": "sets-in-databases", "suggest": "databases", "why": "It is about SQL set operations."}
  ],
  "outcomes_culled": [
    {"code": "PDP-LO1", "why": "A history, not an idea.", "becomes": "landmark"}
  ],
  "questions": [
    {"q": "A decision only Josh can make, with the evidence.", "options": ["…", "…"], "lean": "which you'd pick and why"}
  ],
  "notes": "Anything the next stage should know."
}
```

- `steps[].role`: `teaches` (the page, or the named section, teaches this
  topic), `closer-look`, `context`, or `applies` (a later page that puts the
  topic to work without teaching it; use sparingly, only where a learner
  would want to know).
- `steps[].section`: a heading `anchor` from the inventory when only part of
  a page belongs here; `null` for the whole page. A page can be a step in
  several topics when different sections teach different topics.
- `landmarks[].kind`: `project`, `orientation`, `review`, or `context` (a
  context page that fits no topic).
- Every page in your inventory must appear at least once: as a step, a
  landmark, or in `elsewhere` (it belongs to another area; say which).
- `outcomes`: the descriptor outcome codes (from `outcomes.yaml`) this topic
  serves. Empty for topics no descriptor asked for — that is fine.
- `replaces`: old `topics.yaml` codes this topic succeeds (for migration).

## Checking your file

    python3 planning/topic-map/validate.py proposal planning/topic-map/<your file> <area>

(run from the repository root). It must report 0
errors before you finish. Read every warning and act on the ones that are
right. It prints an effort table (median words taught per topic, by depth):
use it to check the size rule — if effort climbs or collapses with depth, look
again.
