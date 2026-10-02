# The topic map: technical and interaction design

This is the design for replacing the topic tree (`tree.html`, drawn by
`assets/tree.js` from `planning/curriculum/topics.yaml`) with a map that has
levels: continent, region, district, topic, step, and landmarks beside them.
It builds on the prototype that became `assets/map.js`, `assets/map.css` and
`dev/map_layout.py`, and on the topic list the search run produced to the format
in `planning/topic-map/BRIEF.md`. It does not redo that search.

**Status, 2 October 2026.** The prototype is now a page of the site, `map.html`,
beside `tree.html` (`DECISIONS_LOG.md` 7.293). Built: `map/graph.json` and
`map/layout.json`, `dev/map_layout.py`, `write_map_page()`, the script and
styles, a list of every topic for a reader with no script, and the build's
refusals when the map names a page or section that does not exist. Still
planned below, and not built: the check that every page is on a topic (PR 1); the map
in the frame between the docks, as 1.1 describes (it is a wide frame in the page
for now); progress from saved work (PR 4); a link to the map from every tutorial
(PR 5); retiring `covers:` and the tree (PR 6); the teacher's coverage layer
(PR 7); and the topic editor and pair game (PR 8). Where a section below says
what the prototype does, it means the map as built.

A convention for this document: **a path in backticks exists today**. A file
this design proposes is written in italics, for example *map/regions.yaml*,
because `dev/check_doc_links.py` fails any backticked path that is not in the
repository.

Josh has approved the direction: a map with semantic zoom, the warmth of a game
map, and no locks. Where an earlier entry in `DECISIONS_LOG.md` conflicts with
a clean, unified design, the unified design wins; section 6 lists each entry
that is superseded or amended so the log can record it.

The decisions that shape everything else, in one place:

| Question | Decision | Where argued |
|---|---|---|
| Who owns placement: the map or the tutorials? | The map. Topics list their steps; `covers:` and `touches:` retire. | 2.1 |
| Where the map lives | A top-level *map/* folder beside `courses/`, read by the build like the course files. | 2.2 |
| Positions | Committed in `map/layout.json`, written by `dev/map_layout.py`. The build never moves a town. Running the script again may move any town, which is accepted (Josh, 2 October 2026). | 2.4 |
| Land shapes | Contoured at build time in pure Python from the positions, about a second. | 2.5 |
| The page | *map.html*: a static SVG and a full list rendered by `build.py`, a JSON data island, one script (*assets/map.js*). `tree.html` and `topics.html` become redirects. | 4 |
| Progress | Read from the existing `dewlab:progress:<slug>` records. The map says where you have run code, never what you know. | 4.4 |
| The vendor bundle | Nothing in this design edits `assets/tutorial-runtime.js` or anything it imports, so `assets/vendor/standalone.bundle.js` is not rebuilt. | 4.9 |

---

## 1. The levels on screen

### 1.1 The page and its frame

*map.html* is built on the same shell as every page (`assets/shell.html`), so
it inherits the masthead docks, the settings panel, the reader's theme, font,
contrast, motion and pattern settings, and the report doors. That is the
reason 6.3 gave for the tree, and it holds.

The map fills the space between the shell's docks the way the reading column
does since 7.170: its frame is `100dvh` minus `--dl-chrome-h`, and neither the
top-left dock nor the right-hand panels ever sit on top of it. Inside the frame
there are three things and no more: the drawing, a panel (right on a desktop,
a bottom sheet on a phone), and a small control cluster (zoom out, whole map,
zoom in, layers) in the bottom-left corner. The prototype's own search card
and brand header go: the shell already has a site search, and the map's own
"Find a topic" field moves to the top of the panel, where it is the first
thing a keyboard reaches after the skip link.

Nothing on the map is locked. Every town can be opened from anywhere,
directions are suggestions, and dimming (in the course view) never disables
anything.

### 1.2 What each level shows

The prototype chooses its level from the zoom as a multiple of the scale that
shows the whole map (`lodFor()` in `assets/map.js`).
That keeps the first view at continent names on any screen, but further in,
the same multiple means very different things on a 360px phone and a 1400px
desktop, because the phone's whole-map scale is a third of the desktop's. The
design keeps the prototype's thresholds but restates them in **on-screen town
spacing**: `s` is the median nearest-neighbour distance between towns (a
number the build ships, about 150 map units) multiplied by the current zoom.
The level is then the same wherever the reader is.

| Level | When | Shows | Labels |
|---|---|---|---|
| 0. Continents | `s` below 34px (the whole map in view) | The sea, with a few waves, and each continent's coast; land tinted by country, each continent in one family of hues; towns as small dots; the bridges between continents; the tower on the starting island; footprints where the reader has worked; a chosen course's route. | Continent names only, each in the sea beside its coast, never on its land. A name's size depends on the screen, so the page chooses where it goes: of 32 places round the coast (shipped with the map), the one that covers the fewest towns, bridges, other names and controls and stays inside the view. Each name opens its continent. |
| 1. Regions | 34–61px | Everything above, with region borders dashed and county borders dotted. | Region names only, one each, at the clearest spot inside the region. |
| 2. Districts | 61–108px | Everything above, plus district names, town dots sized by how many topics build on them, roads inside each district, drawn faint. | District names first, then the heaviest towns' names where they fit. Region names fade to a watermark. |
| 3. Towns | 108px and up | Every town with its name where it fits, all roads inside the view (bridges dashed in the accent colour), landmarks as small diamonds. Above 165px each town also shows how many pages it holds ("3 pages"). | Town names by priority (1.3). District names at half strength. |
| 4. Streets | A town is open (selected) at level 3 or closer | The open town's steps as a short numbered street leaving the dot: teaching steps as filled stops in reading order, closer-look, context and applies steps as side streets with open stops; its landmarks named; its needs and what it leads to lit as roads in two colours. | The street's page titles always show; other labels give way to it. |

Level 4 is a state, not a zoom band: opening a town zooms to at least level 3
and draws its street. The brief says steps are visible "when a town is opened",
and a street for every town at once would bury the map in text.

Roads are where the old tree became a hairball. Three rules keep them legible.
Between continents, a road crosses the sea on a bridge: one bridge per pair of
continents with roads between them, where it keeps those roads shortest, and
every road across that sea is drawn through it, so roads gather at bridges as
they do on a real map. Two continents with no bridge of their own are joined
by way of the starting island. Inside a continent, roads appear only from
level 2, faint, and only for towns inside the view. When a
town is open, its own roads are drawn strongly (what it needs in the town
colour, what needs it in the accent colour) and every other road fades
further.

### 1.3 How labels give way

The prototype's decluttering stays: labels are placed most important first and
a label that would overlap one already placed is hidden, the way a street map
does it (`render()`, line 453). The priority order is: the open town; stops on
a drawn route (directions or course); towns on the chosen course in the course
view; towns with the reader's footprints; then weight (how many topics build on
the town), then name. Region names are placed before towns at level 1 and
district names before towns at level 2, so the name of the place always wins
over the name of a town in it.

Two changes. Label widths are measured once and re-measured when the reader
changes font or size, or when browser translation changes the text (a
`ResizeObserver` on the overlay); the prototype measures once on the first
frame, which is wrong the moment a page is translated or the reader picks
OpenDyslexic. And decluttering runs once per animation frame at most and not at
all during a pinch, then once when the gesture settles.

Label size follows the reader: `0.72em` of `--dl-font-size`, never below the
12px floor 7.101 set for small text.

### 1.4 What a click does

| Target | Action |
|---|---|
| A region name (level 1) or empty land in a region | Fly to fit that region. |
| A district name (level 2) | Fly to fit that district. |
| A town | Open it: select, fly so it sits in the visible part of the frame at level 3 or closer, draw its street, fill the panel, set the address to *map.html#&lt;topic-id&gt;*. |
| A street (a step) | Open the page, in the same tab, at the section anchor if the step has one. The map keeps its view in `sessionStorage`, so Back returns to the same place. The prototype's `target="_blank"` goes. |
| A landmark | Fill the panel with the landmark: what it is, a link to the page, the towns it draws on. |
| A drag, a pinch, the wheel | Pan and zoom, as the prototype does. A drag never counts as a click. |
| Double-click on land | Zoom in one step at that point. |
| Escape | Close the town (or the landmark) and return the panel to its home state. |

### 1.5 The panel

**Desktop** (wider than 760px): a card on the right of the frame, 380px wide,
full height of the frame, scrolling inside itself. When the map flies to a
town it treats the panel's area and the control corner as off-screen (the
prototype's `viewportBox()`), so a town never lands under either. This is how
7.16's problem (controls stealing clicks from what sits beneath) is answered
for a map that pans: a test asserts the open town is never under a control.

**Phone**: a bottom sheet with three heights. It starts at *peek*, so the first
view is the whole map, and the map's fit leaves room for the bar. *Peek* (about
100px) shows the open town's name and "How do I get here?"; *half* (52% of the frame) shows the
panel's top; *full* (92%) shows all of it. The handle is a real button, at least 28px tall (the prototype's 4px bar was
squeezed to under 1px by the sheet's flex layout, and could not be tapped): a tap
or Enter steps through the heights, a drag snaps to the nearest. The map's
visible area is the part above the sheet, so flying to a town centres it
there, and the control cluster rides above the sheet.

**Home state** (nothing open): the "Find a topic" field; two or three sentences
saying what the map is; a key (a town, a town no page teaches yet, a landmark,
a footprint, a road into another country, a bridge, the plains, the borders); *Places you could go next* when the reader
has worked somewhere (4.5); the layers (courses, roads, where I have worked,
for teachers); and the full list (1.6).

**A town**: an eyebrow line (region, district, "two steps from the start");
the name; the plain description; a line about the reader's own work if there
is any ("You have run code on 1 of 3 pages here"); two actions, *How do I get
here?* and *I already know this* (a toggle, 4.4); the street as a numbered
list of links, each with the page title and, for a section step, the section's
heading, and side streets labelled "a closer look", "background" or "put to
work"; *Needs first* and *Leads to* as buttons that open those towns; the
landmarks that draw on it; and, folded, *Where it turns up in computing* (the
topic's optional `uses`, carried over from the old topics).

Every string in the panel, the key and the list is student-facing and is
written to `planning/PEDAGOGICAL_STYLE_GUIDE.md#voice` and
`planning/PEDAGOGICAL_STYLE_GUIDE.md#plain-language`. That includes the
strings that live in *assets/map.js*, which get the same review as a string in
`build.py`.

### 1.6 Keyboard and screen reader: the list is the map's equivalent

The drawing cannot be the accessible route: 250 town buttons in the tab order
is a trap, and a screen reader walking them in DOM order hears a list with no
structure. So the equivalent is a list, rendered by `build.py` into the page
(it works with no JavaScript at all), and the drawing is presentation over the
same actions.

The list is regions, then districts, then topics, as nested `<details>`: each
topic shows its name as a button ("Show on the map"), its plain description,
the names of what it needs, and its steps as links to the pages, in order, with
roles in words. Landmarks are listed under the district of the first town they
draw on. Every placed page is in it, so the list is also the complete
"everything about one subject" view that `topics.html` was (4.8). The page links
carry `progress_attrs()` inside a `.dl-contents` list, so the runtime's
existing `renderContentsProgress()` puts the same "2/5" badges on them that the
contents page shows, under the same Settings toggle, with no runtime change.

The keyboard route, in tab order:

1. A skip link at the top of the frame: "Skip the map and go to the list of
   topics".
2. The "Find a topic" field: results as a listbox (`aria-activedescendant`),
   arrow keys to move, Enter to open a town.
3. The map itself as one tab stop (`role="region"`, labelled "Map of every
   topic"): arrow keys pan by an eighth of the view, `+` and `-` zoom, `0` shows
   the whole map, Escape closes the open town. Town buttons are
   `tabindex="-1"`: they take clicks and taps, not tab stops.
4. The control cluster and layers.
5. The panel. When a town is opened from the list or from search, focus moves
   to the panel's heading (`tabindex="-1"`), and *Needs first* and *Leads to*
   let a keyboard walk the needs graph from town to town.

For a screen reader the SVG and the town overlay are `aria-hidden="true"`; the
list and the panel carry everything. The prototype puts `aria-live` on the
whole panel (line 316), which re-announces the entire panel on every change.
The design uses one visually hidden status line instead ("Showing Adding
fractions. 3 pages."), and nothing else is live.

### 1.7 Motion, theme, colour and fonts

**Reduced motion.** Flying and easing are skipped, and the view jumps, when
either `prefers-reduced-motion: reduce` matches or the reader's own setting is
on (`data-motion="reduced"` on `<html>`). The prototype checks only the media
query (line 345).

**Light and dark.** The map uses the site's tokens from
`assets/tutorial-style.css`: `--dl-bg` for the land's paper, `--dl-fg` and
`--dl-muted` for text, `--dl-rule` for hairlines, `--dl-heading` for towns,
`--dl-link` for the accent (selection, routes, bridges), `--dl-pass-fg` for
footprints, `--dl-panel-bg` and `--dl-shadow` for the panel. It adds a small
set of map tokens, defined in the same three places every theme token is
defined (the light `:root`, `:root[data-theme="dark"]`, and the
`prefers-color-scheme: dark` block guarded by `:not([data-theme="light"])`):
`--dl-map-sea`, `--dl-map-coast`, `--dl-map-road`, `--dl-map-halo`,
`--dl-map-plains`, `--dl-map-terrain`, and the land's saturation and lightness,
from which each country's tint is made with its hue. The prototype
already copied the site's palette (its navy, orange, paper and muted are the
site's), so this is mostly renaming. High contrast
(`data-contrast="high"`) draws land as `--dl-bg` with a solid region outline in
`--dl-fg`, and turns the patterns on.

**Colour is never the only cue.** Region names are written on the land. Each
continent has one family of hues, and its countries step through that family
in the order they sit round it, so neighbours differ and a continent still
reads as one place from far out. For
readers who cannot tell tints apart, each region also carries an SVG pattern
(stripes one way, the other way, dots), assigned so that neighbouring regions
differ, drawn as `.dl-pattern` copies that the existing rule in
`assets/tutorial-style.css` shows only under *Patterns in pictures* or high
contrast (7.283).

**Fonts.** Labels and the panel use `--dl-font-family`, so Lexend and
OpenDyslexic apply; label widths are measured, never assumed (1.3).

### 1.8 The course view

*map.html?course=&lt;course-id&gt;* is one course's route over the same map.
The build computes the route from the course file (4.6): the topics its pages
teach, in first-taught order, series by series, plus the course's landmarks.

On screen the route is a line through its towns, with numbered stops, drawn
over a map whose other towns are dimmed to about a third (never hidden, never
disabled). The view fits the route. Region and district names show only for
places the route touches. The panel's home state becomes the course: its
title, then each series heading with its towns in order (each a button that
opens the town), its landmarks, and *Pick up here*: the first town on the route
where the reader has not run any code yet. The list in the panel is the
accessible equivalent of the route, as 1.6's list is of the map.

Each course page (`<course>.html`) gets one line linking to its view: "See this
course as a route on the map". The layers menu on the map lists every course;
if the reader is following one (`dewlab:course`, which the runtime already
sets), it is listed first, but nothing is drawn until they choose it.

### 1.9 "On the map" from every tutorial

Every placed page carries a line at the end of its own rung of the
where-you-are tree (the level-4 rung `crumb_trail_html()` writes, after the
practice and context lines): **On the map: Adding fractions**, linking to
*map.html#page:&lt;slug&gt;*. The map opens the topic where that page is a
teaching step (or, failing that, any step, or the landmark) and marks the
page's own stop on the street. The link text names the topic, or the first two
topics if a page teaches sections of several ("On the map: Powers · Roots"). A
practice page's line is its tutorial's. The rung is the right place for two
reasons: the runtime's `drawCourseChrome()` redraws rungs 2 and 3 when the
reader follows another course and leaves rung 4 alone, and
`standalone_html()` already strips cross-file lines from that rung by class,
so a downloaded copy loses the link with one more class in its pattern
(`dl-crumb-map`).

### 1.10 What changes from the prototype

The prototype proves the core idea: continents found from the roads between
regions, a layout that settles from the outside in, land from a contoured
density field, bridges where roads cross the sea, HTML towns over an SVG, priority decluttering, fly-to search, directions and
course routes. All of that stays. What changes, and why:

| Prototype | Design | Why |
|---|---|---|
| Recomputes the whole layout, force pass included, every run. | Positions committed; the force pass runs only in `dev/map_layout.py`, never in the build. | The force pass took 4.5s on a 284-topic test graph (2.5), and a page that is built should not wait for it. |
| `random.uniform()` jitter for landmarks (`dev/map_layout.py`; seeded, but every landmark moves when one is added or reordered). | Deterministic offsets from the landmark's slug. | Two builds of the same input must write the same page. |
| Level from zoom as a multiple of the whole-map scale. | Level from on-screen town spacing (1.2). | Same level on a phone and a desktop. |
| Land, coast and roads as path strings inside the JSON. | Rendered by `build.py` as a static SVG in the page. | A picture without JavaScript, and a smaller island. |
| 367 KB island on the test graph, 292 KB of it towns, each step repeating a full URL, title and course names. | A shared pages table; steps are `[page, anchor, role]`; URLs built in the browser. Roughly 150 KB before compression. | School networks. |
| Its own palette, header and fonts; theme only from the media query. | The shell and the site's tokens, the reader's theme, font, contrast, patterns and motion settings. | 6.3 and 7.283. |
| A sample learner and an `atlas:visited` key; "I have been here" toggles visited. | Footprints from the real `dewlab:progress:<slug>` records; "I already know this" is the learner's own mark, stored apart and drawn differently. | The map must not claim what it cannot see (4.4). |
| Directions: every unvisited ancestor, sorted by depth and name (`orderForTravel()`). | Walk back from the target, stopping at topics the reader has worked on or marked known; topological order with a same-district tie-break. | Shorter, and less zigzag between regions (4.5). |
| `aria-live` on the whole panel; towns in DOM order for a screen reader. | One live status line; overlay hidden from assistive technology; the server-rendered list as the equivalent; a skip link; focus to the panel heading. | 1.6. |
| Its own substring search. | `assets/search-words.js`, the one idea of matching every search box uses (7.174). | "fraction" should find "Fractions". |
| `field_for()` compares each region with every other at every cell (line 267). | One pass keeps the top two densities per cell. | Ten regions would otherwise cost about ten times as much. |
| "How each topic was found" layer and the `agreement` field. | Gone. | A record of the search, not something a learner needs. |

---

## 2. Data model and source of truth

### 2.1 The decision: topics list their steps

There are two ways to say which pages make up a topic. The map can list, for
each topic, its steps in order (the way `courses/*.yaml` lists each series'
pages in order); or each tutorial can claim topics in its frontmatter, as
`covers:` claims outcomes by section today. **The map owns placement.**

The strongest reason is order. A topic's steps are ordered: the brief defines a
step as "one page or one section of a page inside a topic, in order", and the
street on screen is that order. Order is a property of the topic, not of any
one page. Frontmatter claims cannot express it without a sort key on every
page, duplicated across files and renumbered whenever a page is inserted. That
is exactly the `order:` field 7.173 took out of the tutorials, and
`MOVED_FRONTMATTER` in `build.py` still refuses it.

The second reason is the principle 7.173 set and `courses()` states in its
docstring: "A tutorial's own file says nothing about any of this, which is
what lets one tutorial sit on two courses without a second copy of anything."
Which topic a page serves is placement of the same kind. A page whose sections
teach two topics becomes two lines in the map rather than a nested structure in
its frontmatter; moving a page between topics, or splitting a topic, is one
diff in one file.

Third, everything that has to be checked together is in one place. The needs
graph, the size rule (a topic is about the same effort wherever it sits), the
district a topic belongs to and the coverage of descriptor outcomes all
concern a topic as a whole. No single tutorial can check any of them, and a
reviewer cannot see a topic's shape without aggregating 274 files.

Fourth, it removes a class of bug. Frozen releases (`v<version>.md`) carry
their own frontmatter, so a superseded release claims the same coverage as its
replacement; `tests/build/test_releases.py` exists to stop both counting. A
step names a page id, and the build resolves the id to its default release, so
the question never arises.

Fifth, the search run already produces topics with ordered steps, so migrating
is a conversion, not new claims written into 274 files.

The costs are real and worth naming. Locality goes: an author who renames a
heading no longer sees, in the same file, the claim that pointed at it. The
build answers that with an error that names the map file, the topic and the
page's current anchors (2.3), and `check.py` tells an author which topics
their page is on. Adding a page means touching two files, the course file and
the map; today it means touching the course file and writing `covers:`, so
the count is the same. And the authoring editor (`assets/editor.js`), which
already commits a course-file line when it inserts a tutorial, cannot yet add
the map line (section 7, question 3).

**What happens to `covers:` and `touches:`.** Both retire (phase 6).
`covers:` said which sections teach which descriptor outcomes; that is now a
topic's `outcomes` together with its teaching steps and their section anchors.
`touches:` said a section uses an outcome without teaching it; where a learner
would want to know that, the map has an `applies` step, and otherwise it was
only a column in `planning/CURRICULUM_MAP.md`. `covers` joins
`MOVED_FRONTMATTER`, so the build refuses it with a message pointing at
*map/*: an ignored field is a field somebody keeps writing (7.173).

**What happens to the tutorial files.** Only the `covers:` block is deleted,
from about 197 current files and the 8 frozen releases (7.173 set the
precedent of editing frozen frontmatter when a field moved). No version bump,
since no cell's code changes; no heading renamed; no cell id or tutorial id
touched, so no saved work moves (CLAUDE.md's first trap).

### 2.2 Where the map lives, and its files

The map is read by the build and is required for the map page, so it does not
belong under `planning/`, which holds what was decided before code existed and
which the build treats as optional. It sits at the top level beside
`courses/`, and the build reads it the same way: optional as a whole (with no
*map/* folder there is no map page, which is what small test builds want),
strict once present. A path constant `MAP` sits beside `COURSES` so tests can
point it at a fixture.

| File | Holds | Written by |
|---|---|---|
| *map/README.md* | What the files are, the step shorthand, how to put a page on the map, how to move a town. | Hand |
| *map/regions.yaml* | Continents, each with its regions, and each region with its districts. | Hand |
| *map/topics/&lt;region-id&gt;.yaml* | One file per region: that region's topics, keyed by id. | Hand, the topic editor |
| *map/landmarks.yaml* | Landmarks, keyed by page slug. | Hand |
| *map/culled.yaml* | Descriptor outcomes that are not ideas, with what each became. | Hand |
| *map/positions.json* | Town and landmark coordinates. | *dev/map_layout.py*, the topic editor, hand |

One file per region rather than one file keeps diffs and merge conflicts local
(about ten files of 15 to 40 topics). YAML keyed by id, read with
`load_yaml_no_duplicate_keys()`, so a botched merge that repeats an id fails
loudly (the reason that loader exists); the build also refuses an id repeated
across files.

*map/regions.yaml*:

```yaml
# Continents, then regions. A continent names its regions; exactly one
# continent is the start, where the tower and the plains are.
continents:
  mathematics:
    name: Mathematics
    fancy: The Old Country
    regions: [number, algebra, shape-and-space]
regions:
  number:
    name: Number
    blurb: Counting, fractions, powers and the rules numbers follow.
    subject: maths            # the Library rail's Subject filter: maths | computing
    districts:
      fractions:
        name: Fractions
        blurb: What a fraction is, and how to add, compare and share them.
      powers-and-roots:
        name: Powers and roots
        blurb: ...
```

*map/topics/number.yaml*:

```yaml
topics:
  adding-fractions:
    name: Adding and subtracting fractions
    district: fractions               # must be a district of this file's region
    plain: >
      Putting fractions together and taking one from another, first when the
      bottoms match and then when they don't.
    needs: [equivalent-fractions]     # direct needs only; any region
    steps:
      - adding-slices                 # a whole page that teaches this topic
      - taking-slices-away
      - the-hidden-bracket: closer-look
      - drawing-numbers#a-fraction-on-the-line   # one section of a page
      - money-in-a-table#splitting-a-bill: applies
    outcomes: [MIT-2.1]               # descriptor outcomes served (teacher view)
    uses: []                          # optional: where it turns up in computing
    replaces: [MIT-1.1a]              # old topics.yaml codes; the migration record
    aliases: []                       # earlier ids of this topic (7, question 1)
```

A step is a string (a page, or `page#anchor` for a section, role `teaches`) or a
one-key mapping from that string to its role (`closer-look`, `context`,
`applies`). The shorthand mirrors how a course file lists ids: the common case
is one word per line. The search run's `size` rationale does not come across;
it stays in the search's revised map in this folder as the record.

*map/landmarks.yaml*:

```yaml
landmarks:
  before-we-start: {kind: orientation, at: [counting-things]}
  make-a-quiz-game: {kind: project, at: [python-lists, python-functions]}
```

`kind` is `project`, `orientation`, `review` or `context`, as in the brief. A
mixed problem set (`practice_across`) may be a `review` landmark but need not
be placed: practice follows its tutorial.

*map/culled.yaml*:

```yaml
culled:
  PDP-LO1: {becomes: landmark, page: where-programming-came-from, why: A history, not an idea.}
  PDP-LO12: {becomes: metadata, why: Keeping evidence is a course requirement, not something to learn.}
```

*map/positions.json* holds integers in map units, the centre being the
"start here" mark, one entry per line and keys sorted so a diff shows exactly
which towns moved:

```json
{"version": 1,
 "topics": {"adding-fractions": [812, -140], "...": [0, 0]},
 "landmarks": {"make-a-quiz-game": [930, -310]}}
```

Region and district label positions, land and the coast are not stored; the
build derives them from the positions (2.5).

`planning/curriculum/outcomes.yaml` stays where it is: it is the transcription
of the awarding body's descriptors, not ours to reshape, and the teacher view
and `dev/curriculum_map.py` read it. `planning/curriculum/out-of-scope.yaml`
stays too, because "decided not to teach" is a different claim from "not an
idea" (culled). `topics.yaml`, `strands.yaml` and `topic-groups.yaml` retire
(section 3 and phase 8).

### 2.3 What the build checks

`load_map()` reads and validates the files; `check_map()` checks them against
the pages the build loaded. Errors stop the build, as a dead `tutorial:` link
does. Notes are printed and do not, the way "no course lists this tutorial" is
a note today.

| Check | Error or note |
|---|---|
| Unknown field on a region, district, topic, step or landmark; a missing `name`, `district` or `plain`; an id that is not kebab-case; an id used twice, across all files, aliases included. | Error |
| A topic whose district belongs to another region's file; an unknown district; an unknown role or landmark kind. | Error |
| A step naming a page that does not exist, a practice page, or an archived page. The last keeps 7.18's rule (an archived tutorial teaches nothing the map can point at) and enforces it rather than skipping. | Error |
| A section anchor that is not a heading id of the page's default release. Checked against the ids the build itself rendered (`Tutorial.toc`), not a re-implementation of the slug rule, so a repeated heading's `_1` id can be named; 7.146 recorded that `anchor_for()` in `dev/curriculum_map.py` cannot. The message names the map file, the topic, and lists the page's anchors. | Error |
| A need naming an unknown topic; a topic needing itself; a cycle, reported as the path round it. | Error |
| An outcome code on a topic or in *map/culled.yaml* that `planning/curriculum/outcomes.yaml` does not list (the typo guard 7.14 kept). Only when that file is present. | Error |
| A live or beta page placed nowhere (neither a step nor a landmark). A draft is noted only once it is live. | Note |
| A descriptor outcome that no topic serves and that is neither culled nor out of scope. | Note |
| A topic with no teaching step (drawn as a town still being built). | Note |
| A redundant need (C needs A and B, and B already needs A): the brief says direct needs only. | Note |
| A course that reaches a topic before one of its needs (4.6). | Note |
| A topic with no position (placed automatically, 2.4); a position for an id that no longer exists. | Note |

The two notes that matter most are enforced by CI instead of the build, the way
`TestTopicGroupsMatchRealTutorials` in `tests/build/test_courses.py` holds
`topic-groups.yaml` to account today: a test against the real repository
asserts that every live and beta page is placed and every outcome in
`planning/curriculum/outcomes.yaml` is served, culled or out of scope. The
reason for not failing the build: a tutorial inserted through the authoring
editor has no `status` line, so it is live the moment it exists, and an
author's local build should not fail before they have had a chance to place
it. CI failing the pull request is the right moment.

`check.py`'s `check_tutorial()` gains one line: "On the map as a step of:
Adding fractions, Equivalent fractions" or, as a problem, "This page is on no
topic. Add it as a step in map/topics/…". `check_course()` prints the course
order note.

### 2.4 Positions

Positions are data, committed, and the build never moves a town. They are
written by *dev/map_layout.py* into `map/layout.json`, and the build refuses
when the layout and the graph disagree.

**The layout** is the prototype's algorithm. It works from the outside in. The
continents go round the starting island a sea apart, in the order and at the
distances that keep continents with many roads between them close (a small
relaxation of one disc per continent). Each continent's countries get a home on
it, and each country's districts a home in it, turned to face what they have
roads to. Then every town settles from its district's home under a force pass:
towns push apart, harder across a border and hardest across the sea; a need
pulls like a spring; each town is drawn to the middle of its county and
country; depth is a gentle pull away from the tower. Towns that need nothing
first stand on the Prerequisite Plains round the tower. Which regions share a
continent comes from the roads, not by hand: `planning/topic-map/continents.py`
prints the matrix of needs between regions and the groupings with the highest
modularity.

**Running it again lays the whole map out again**, so towns can move, and not
only the one that changed. This plan once held every placed town still and put
a new one beside what it needs (`--keep` and `--only`). Josh dropped that on 2
October 2026: the map may change, and nobody minds a town moving
(`DECISIONS_LOG.md` 7.293). Check `git diff --stat map/layout.json` before
committing, and say in the pull request that the map moved.

**By hand**, through the existing topic editor. `topic_editor/index.html`
already keeps positions, pins them once dragged and exports them under `pos`;
`dev/apply_topic_edits.py` already writes a positions file. Phase 8 points both
at the map: the editor opens on the map's positions (pinned), its columns
become districts grouped by region, its `requires` links become `needs`, and
the four other link kinds (`helps`, `applied_in`, `interdependent`, `involves`)
go, since `topics.yaml` uses none of them and the map has only needs. Export,
then `python3 dev/apply_topic_edits.py topic-graph-edits.json`, rewrites the
region files and the map's positions.

### 2.5 Land at build time, without numpy

`requirements-build.txt` has no numpy, and the prototype shows none is needed.
Measured on a test graph of 284 topics, 34 districts and 6 regions (the current
142 topics doubled, with steps from the inventory): the density field,
marching squares, chaining, Chaikin smoothing and label placement together
took 0.7s; the force pass took 4.5s; building the island took no time beyond
loading the tutorials, which the build does anyway. With the force pass out of
the build and the top-two pass replacing `field_for()`'s every-region
comparison, ten regions should stay near a second. A test holds the real map's
geometry step under a budget (3s on CI) so a regression shows.

The build computes, from positions: one density grid (20-unit cells, Gaussian
of 95 units per town, landmark and road anchor, as in the prototype), each
cell's top two region densities in one pass, a closed smoothed path per
region where it is the strongest and the total clears the threshold, one
coastline from the total, region label spots and district label spots. All
coordinates are rounded to integers so the output is byte-stable.

---

## 3. Every consumer that has to change

Found by searching `build.py`, `check.py`, `dev/`, `assets/`, `compose/`,
`tests/`, `docs/`, `pages/`, `planning/`, `.claude/skills/`, `topic_editor/`,
`topic_tree_game/` and `.github/` for the topic files and functions. The phase
column refers to section 5.

### 3.1 build.py

| Function or constant (line) | Uses it for | Becomes | Phase |
|---|---|---|---|
| `TOPIC_DATA`, `SCOPE_DATA`, `TOPIC_GROUPS_DATA` (3981–3983), `TOPIC_W`…`TREE_PAD` (3986–3992) | Paths and the tree's grid. | `MAP` beside `COURSES`; the grid constants go. | 1, 3 |
| `load_topics()` (3995) | Reads `topics.yaml` for the tree and the facets. | `load_map()`. Deleted once facets move. | 1, 6 |
| `load_topic_groups()` (4004) | Groups for "Browse by topic" and the `groups` facet. | Deleted. | 6 |
| `load_out_of_scope()` (4018) | The tree's "not on this course" state. | Deleted from the build; the teacher layer reads the file in `map_data()`. | 3, 7 |
| `taught_where()` (4026) | Outcome to first section claiming it, for the tree's links. | Deleted: a topic's teaching steps are its links. | 3 |
| `topic_tiers()` (4045) | Depth, for the tree's rows and the Library's levels (7.101). | `map_depths()`, over the map's needs. | 1, 6 |
| `outcome_of()` (4066) | A topic's first outcome, for colour and coverage. | Deleted: a topic lists `outcomes`, and colour is region. | 3 |
| `topic_layout()` (4084), `tier_label()` (4137) | Rows of the tree. | Deleted; the layout is 2.4. | 3 |
| `tree_data()` (4151) | The tree's data island. | `map_data()` (4.2). | 3 |
| `OUTCOME_DATA`, `load_strands()` (4242), `strand_of()` (4222), `map_rows()` (4254), `NODE_W`…`MAP_PAD` | Strands for the tree's colours and the knowledge-map lanes. | Deleted. `OUTCOME_DATA` stays for the outcome typo guard and the teacher layer. | 3 |
| `render_knowledge_map()` (4275) | "How the tutorials relate", first series only. | Deleted (4.8). | 3 |
| Contents-page introduction (4558–4562) | Links to `tree.html` and `topics.html`. | One sentence linking to the map. Student-facing. | 3 |
| Practice and context `covers:` refusals (3202, 3254, 3320) | Companion pages may not claim outcomes. | Subsumed: `covers` is in `MOVED_FRONTMATTER` for every page. | 6 |
| `MOVED_FRONTMATTER` (144) | Refuses fields that moved to `courses/`. | Gains `covers`, pointing at *map/*. | 6 |
| `crumb_trail_html()` (3506) | The where-you-are tree. | Adds the `dl-crumb-map` line to rung 4 (1.9). | 5 |
| `standalone_html()` `keep_contents()` (6142) | Strips cross-file lines from a downloaded copy. | Also strips `dl-crumb-map`. | 5 |
| `render_course_body()` (4580) / `write_course_page()` (6864) | Course pages. | The "route on the map" line. | 5 |
| `warn_about_titles_and_overlap()` (7045) | Notes two pages teaching three or more of the same outcomes. | Compares teaching steps: two live pages that both teach two or more of the same topics. | 6 |
| `strand_key()` (7082), `write_tree_page()` (7109) | The tree page. | `write_map_page()`. | 3 |
| `write_topics_page()` (7211) | "Browse by topic". | Deleted; the map's list replaces it (4.8). | 3 |
| `OUTCOME_SUBJECTS`, `LEVEL_BANDS`, `level_for_tier()`, `tutorial_facets()` (7366–7438) | Subject from outcome prefix, level from `topic_tiers()`, groups from `topic-groups.yaml`, for the Library rail (7.101). | Subject from each taught topic's region `subject`; level from the deepest topic a page teaches (`teaches` steps only), with `LEVEL_BANDS` re-tuned once against the real map for a similar spread; groups are regions. Still derived, never tagged. | 6 |
| `write_reference_index()` (7440) | `assets/reference-index.json` for dewmini's Library. | Shape becomes `{"entries": [...], "groups": [{"id", "name"}]}` so labels travel with the data. | 6 |
| `write_search_index()` (7321) | Site search. | Optionally adds the names of the topics a page teaches to its `terms`. | 5 |
| `build()` (7696–7701) | Calls both page writers. | Calls `load_map()`/`check_map()` after loading, `write_map_page()` in their place. | 1, 3 |
| `write_redirects()` (6956) | Stub pages for old addresses. | Unchanged; `courses/redirects.yaml` gains `tree.html: map.html` and `topics.html: map.html`. | 3 |
| `TOPIC_GAME`, `TOPIC_EDITOR` copies (after 7735) | Publish the pair game and topic editor. | Unchanged. | — |

### 3.2 Scripts, runtime and pages

| File and function | Uses it for | Becomes | Phase |
|---|---|---|---|
| `check.py` `check_tutorial()` (152), the context and practice `covers:` problems (226, 253) | Author checks. | Reports map placement; `covers` joins `OLD_FIELDS`; the two problems go. `check_course()` prints the course order note. | 1, 5, 6 |
| `assets/tree.js` | Draws the tree. | Deleted; *assets/map.js* replaces it. | 3 |
| `assets/tutorial-style.css` (64 `dl-tree`/`dl-map` rules) | Tree and figure styles. | Deleted; map styles and tokens added (1.7). The figure's `.dl-map*` classes are deleted in the same phase, so the `dl-map-` prefix is free for the page. | 3 |
| `assets/my-notes.js` (line 8 comment) | Cites tree.js's data island as its model. | Cites map.js. | 3 |
| `assets/tutorial-runtime.js` `NON_TUTORIAL_PAGES` (line 45) | Pages with no Notes section: index, tree, about, topics. | Unchanged (4.9). | — |
| `compose/dewmini.js` `REFERENCE_TOPIC_LABELS` (2708) and the reference loader | Hand-kept labels for topic-group keys. | Deleted; labels come from the index's `groups`. Not in the standalone bundle. | 6 |
| `dev/curriculum_map.py` `load_tutorials()` (224), `anchor_for()` (78) | `planning/CURRICULUM_MAP.md` from `covers:`; anchor validation. | Reads the map: a topic's `outcomes` and its teaching steps give "where taught", `applies` steps the lighter column, *map/culled.yaml* a new "off the map" state. Anchor checks move to the build. `--check` stays in CI. | 6 |
| `dev/check_doc_links.py` `GENERATED_PAGES` (80) | Pages the build writes, so docs may name them. | Adds *map.html*; drops `tree.html` and `topics.html` once no checked document names them. | 3, 8 |
| `courses/redirects.yaml` | Old addresses. | Two lines (above). The stub cannot carry a `#group` anchor from the old `topics.html`; those land on the map's home state. | 3 |
| `pages/about.md`, `pages/features.md`, `pages/studying.md` | Student-facing mentions and links. | Rewritten for the map. | 3 |

### 3.3 Topic tools and CI

| File | Uses it for | Becomes | Phase |
|---|---|---|---|
| `dev/build_topic_editor.py` | Writes the editor's DATA from `topics.yaml`, the judgements and `strands.yaml` (through `dev/draw_topic_graph.py`). CI runs `--check`. | Writes it from *map/*: topics, districts as columns grouped by region, needs, positions. `--check` stays. | 8 |
| `dev/apply_topic_edits.py` | Export to `topics.yaml`, `strands.yaml`, a positions file. | Export to *map/topics/*, *map/positions.json*. | 8 |
| `topic_editor/index.html`, `topic_editor/help.html`, `topic_editor/README.md` | The editor and its guide. | Regenerated; guide rewritten; the four extra link kinds go. | 8 |
| `dev/build_topic_game.py` | The pair game's topics from `topics.yaml` and `topic-groups.yaml`. CI runs `--check`. | From *map/*: topic id, name, district as the card's section, plain, needs. `--check` stays. | 8 |
| `topic_tree_game/index.html`, `topic_tree_game/help.html`, `topic_tree_game/README.md` | The game. | Regenerated; README says judgements are now about map topics. | 8 |
| `dev/pair_results.py` | Reports judgements against `topics.yaml`; CI regenerates three reports and diffs them. | Reads new judgements (keyed by map ids) against the map. The three existing reports are kept as they are, as the record of the old graph, and their regeneration step leaves CI. | 8 |
| `dev/draw_topic_graph.py` | Draws the old graph the blind judgements imply; imported by the editor builder. | Deleted once the editor no longer imports it. | 8 |
| `.github/workflows/tests.yml` | `curriculum_map.py --check`, `build_topic_game.py --check`, `build_topic_editor.py --check`, pair reports, doc links. | Comments updated; the pair-report step changes as above; the others stay. | 6, 8 |
| `planning/curriculum/topics.yaml`, `strands.yaml`, `topic-groups.yaml` | The old sources. | Deleted in phase 8. Git history, each topic's `replaces`, and the kept pair reports are the record. | 8 |

### 3.4 Tests

| File | What changes | Phase |
|---|---|---|
| `tests/build/test_curriculum.py` | `TestTheKnowledgeMap`, `TestTheTopicTree`, `TestBrowseByTopicPage` deleted; `TestNoDuplicateKeysInCurriculumData` drops the retired files and adds the map's. | 3, 8 |
| `tests/build/test_courses.py` | Tree-data assertions (lines 428, 467) and `TestTopicGroupsMatchRealTutorials` deleted; crumb-line and course-link tests added. | 3, 5 |
| `tests/build/test_releases.py` | The tree check (line 96) becomes: the map resolves a step to the default release and checks its anchors there. | 3 |
| `tests/build/test_reference_index.py` | The 7.101 level test (469) rewritten against a stub map; subject and groups from regions; new index shape. | 6 |
| `tests/build/test_site.py` | The About page's link to `tree.html` (line 129). | 3 |
| `tests/build/test_old_addresses.py` | The two new redirects. | 3 |
| `tests/build/test_check.py` | The map line in `check.py`; `covers` refused. | 1, 6 |
| `tests/build/test_downloads.py` | A downloaded copy has no map line. | 5 |
| `tests/build/test_tutorial.py`, `tests/build/test_practice.py`, `tests/build/test_context.py` | `covers:` refused everywhere; the companion-specific refusals go. | 6 |
| `tests/test_curriculum_map.py` | `TestTheTopicGlossary` goes (its DAG and reference checks are build checks now); coverage read from a fixture map. | 6 |
| `tests/test_pair_results.py` | Judgements keyed by map ids. | 8 |
| `tests/test_from_notebook.py` (line 279), `tests/e2e/test_page_smoke.py` (147–148) | Page lists name `tree.html`/`topics.html`. | 3 |
| `tests/e2e/conftest.py` (97–120) | Copies the curriculum folder and patches topic paths. | Copies a fixture map that places the fixture pages; patches `MAP`. | 3 |
| `tests/e2e/test_phase0_golden_path.py` (406–620) | Nine tree tests. | Deleted; replaced by the new map suites. | 3 |
| `tests/e2e/test_dewmini_workbench.py` (290) | The topics disclosure's labels and count. | Region labels from the index. | 6 |

### 3.5 Documents and skills

| Document | What changes | Phase |
|---|---|---|
| `ARCHITECTURE.md` | §1: a step "Read and check the map"; step 6's page list; the supporting-scripts paragraph. §2: "Two more pieces: `assets/tree.js`…" becomes map.js. The "Where to start" row for the tree. | 1, 3 |
| `docs/build-explained.md` | Its "Topic tree and knowledge map" section (line 62) and the question at line 153. | 1, 2, 3 |
| `docs/WRITING_TUTORIALS.md` | The `covers:` section (about line 1410) replaced by "Putting a page on the map"; the `topic:MIT-3.2` paragraph (line 1030) describes resolution `build.py` does not perform (no `topic:` handling exists and no tutorial uses it) and goes in phase 1; the closer-look paragraph's `topic-groups.yaml` mention (line 108); line 1556. | 1, 6 |
| `docs/tests-explained.md`, `docs/dev-scripts-explained.md`, `docs/tutorial-runtime-explained.md` (line 518), `docs/CHECK_YOUR_WORK.md` | Test map, new and retargeted scripts, the tree.js reference, the new check line. | 1–8 |
| *docs/map-js-explained.md* (new) | The explanation file CONTRIBUTING.md requires for a substantial script. | 3 |
| `docs/FOR_STUDENTS.md` (220–242), `docs/FAQ.md` (22, 61, 114), `docs/DEWMINI.md` (289–297) | Student-facing descriptions of the tree, "Browse by topic" and the Library's levels. | 3, 4, 6 |
| `README.md` (72–74, 150), `CONTRIBUTING.md` ("What runs in CI") | Overview and CI. | 3, 6 |
| `CLAUDE.md` | A row in "Where the rest lives": putting a page on the map, *map/README.md*. | 1 |
| `planning/REFERENCE_PANEL.md` | Names `topics.yaml` as the reachability model. | 6 |
| `.claude/skills/tutorial-glossary/SKILL.md` (line 9) | "`covers:` in its frontmatter already names broad curriculum outcomes." | 6 |
| `planning/topic-map/README.md`, `planning/topic-map/BRIEF.md`, this document | Name files later phases delete, in backticks. When phase 3 deletes `assets/tree.js` and phase 8 the old YAML, that phase either adds `planning/topic-map/` to `ELSEWHERE` in `dev/check_doc_links.py` (the folder becomes a record) or rewrites the references. | 3, 8 |
| `DECISIONS_LOG.md` | New entries per phase; section 6's supersessions. | all |

### 3.6 The downloadable copies and the vendor bundle

A tutorial's standalone copy strips the where-you-are tree except its own
rung, and phase 5 adds `dl-crumb-map` to the classes stripped from that rung.
Series and course zips are built from the same copies. The Notebook's offline
bundle copies `assets/reference-index.json`, whose shape changes in phase 6;
dewmini reads the new shape in the same phase. The map page has no
downloadable copy, as the tree had none. Nothing forces a rebuild of
`assets/vendor/standalone.bundle.js` (4.9).

---

## 4. Build and runtime architecture

### 4.1 In build.py

The map is computed in `build.py`, in the order the build already works:

1. `load_map()` after `load_all()`: parse, expand step shorthand, validate
   schema, return frozen dataclasses (`Region`, `District`, `Topic`, `Step`,
   `Landmark`).
2. `check_map(map, tutorials)`: the checks in 2.3, against `Tutorial.toc`, the
   registry, statuses and `courses()`.
3. `map_depths(map)`: depth per topic (replacing `topic_tiers()`); weight per
   topic (how many topics build on it, for dot size and label priority).
4. `place_new_topics(map, positions)`: 2.4.
5. `map_geometry(map, positions)`: 2.5.
6. `section_cells(tutorial)`: for each heading id, the cell ids under it, found
   by walking the rendered body in order (heading ids from the toc, cell ids
   from the `data-cell-id` attribute `render_cell()` writes). World-variant
   suffixes (`--planets`) are stripped, so a section's cells match whichever
   world the reader chose.
7. `course_routes(map, courses())`: 4.6.
8. `map_data(...)`: the island (4.2).
9. `render_map_svg(geometry, map)` and `render_map_list(map, ...)`: the static
   picture and the list.
10. `write_map_page(shell, ...)`: fills the shell's tokens as
    `write_tree_page()` does, with manifest slug `map`, the report doors for
    `map`, and `{{PAGE_SCRIPT}}` carrying the island and a
    `<script type="module">` for map.js.

### 4.2 The page

The page body holds, in order: the frame with the skip link, the static SVG
(`aria-hidden`; sea, land per region with its pattern copy, coast, bridges,
roads as paths carrying `data-from`/`data-to`, empty groups for routes),
an empty overlay for towns, the control cluster, and the panel whose home
state contains the full list. With no JavaScript the reader gets a picture and
a complete, working list.

The data island, `<script type="application/json" id="dewlab-map">`:

```json
{
  "v": 1,
  "bounds": [-2600, -2400, 5200, 4800],
  "spacing": 150,
  "regions":   [{"id": "number", "name": "Number", "blurb": "…", "tone": 3, "pattern": 1, "label": [x, y]}],
  "districts": [{"id": "fractions", "region": "number", "name": "Fractions", "blurb": "…", "label": [x, y]}],
  "topics": [{
    "id": "adding-fractions", "name": "…", "plain": "…", "district": "fractions",
    "needs": ["equivalent-fractions"], "depth": 2, "weight": 14, "x": 812, "y": -140,
    "steps": [[17, null, "t"], [18, null, "t"], [40, null, "c"], [52, "a-fraction-on-the-line", "t"]],
    "uses": [], "aliases": [], "outcomes": ["MIT-2.1"]
  }],
  "pages": [{"slug": "adding-slices", "title": "…", "status": "live",
             "legacy": "module:slug", "headings": {"anchor": "Heading text"},
             "sections": {"anchor": ["cell-id", "…"]}}],
  "landmarks": [{"page": 3, "kind": "project", "at": ["python-lists"], "x": 930, "y": -310}],
  "courses": [{"id": "zen-of-slashes-and-surds", "title": "…",
               "series": [{"title": "…", "stops": ["…"], "landmarks": [3]}]}],
  "outcomes": {"modules": {"MIT": "Maths for Information Technology"},
               "list": [{"code": "MIT-2.1", "text": "…", "served": ["adding-fractions"],
                         "culled": null, "scope": null}]}
}
```

Pages are a table indexed by position so a page that is a step in three topics
is written once. `headings` carries only the anchors steps name; `sections`
only for those anchors; `legacy` only where the page had an older address (4.4).
Serialised with `<` escaped, as `write_tree_page()` does. A test holds the
real island under 200 KB.

### 4.3 assets/map.js

One ES module with no library, loaded only by the map page, the way tree.js
is today. It imports `assets/search-words.js` for matching; that file is also
imported by the runtime, and importing it changes nothing in it. Its parts,
each small and named in *docs/map-js-explained.md*: read the island; build the
town overlay (buttons, `tabindex="-1"`, inside an `aria-hidden` layer); the
view (pan, pinch, wheel, fly, fit, levels from spacing, reduced motion); the
labeller (1.3); selection and the street; the panel renderer (home, town,
landmark, course); search; the progress index (4.4); directions and open
doors (4.5); layers (roads, courses, where I have worked, for teachers);
address state (`#<topic-id>`, `#page:<slug>`, `?course=<id>`, aliases resolved
to their topic) and view state in `sessionStorage`. It exposes
`globalThis.dewlabMap` for the browser tests, as tree.js exposes
`dewlabTree`.

### 4.4 Progress: what "visited" may claim

The map reads the saved-progress records the runtime already writes
(`saveNow()` in `assets/tutorial-runtime.js`), the same way the contents page's
badges do (`renderContentsProgress()`) and My Notes does (`readAllRecords()`
in `assets/my-notes.js`): once, on load, every `localStorage` key beginning
`dewlab:progress:`, indexed by the record's `tutorial-id` (or `tutorial-slug`).
A record still under an older `module:slug` key, for a page the reader has not
reopened since the runtime's `migrateStorage()` would have renamed it, is found
through the page's `legacy` entry in the island.

**A step is visited** when its page's record shows the reader did something on
it: at least one of the step's cells has saved output (`output_html` not
empty), where the step's cells are the whole page's for a page step and the
section's for a section step. A page with no Python cells counts a site editor
or full-stack cell with `ran: true`, or a question with `checked: true`. A page
with nothing to run cannot be visited by this rule and shows nothing, as a
prose-only page gets no badge on the contents page (7.70: a "0/9" reads as a
judgement on a page nobody opened). If a section step has no cells of its own,
it falls back to the page.

**A topic has footprints** when any of its teaching steps is visited. Closer
looks, background and applies steps show their own marks on the street but do
not count for the town, because they are optional.

**What the map may say**: "You have run code on 1 of 3 pages here", "You have
worked here", footprints on a town, ticks on a street. **What it must never
say or imply**: done, complete, finished, mastered, learned, "you know this".
Running a cell shows the reader was there; it shows nothing about what they
understood, and the style guide's stance on judging words (7.244) applies. A
browser test checks the rendered strings against that list.

The map says where this comes from, once, in the key: "The map reads the work
saved in this browser. Nothing is sent anywhere." Footprints are ambient, so
they obey the reader's existing *Show progress on the tutorials list* setting
(`dewlab:progress-badges`); the map's "Where I have worked" layer toggle writes
the same key, so one setting governs every progress display.

**I already know this.** A returning adult who learned fractions years ago
should not be routed through them. The town's toggle is the reader's own
statement, stored apart under `dewlab:map-known` (an array of topic ids), drawn
as a small tick distinct from footprints, and used by directions and open doors
exactly as footprints are. It is never counted as visited, never shown in the
teacher layer, and the wording is the reader's ("I already know this"), not the
site's. Aliases keep a mark alive if a topic's id changes.

### 4.5 Directions and open doors

*How do I get here?* answers "what comes before this that I have not worked
on", over the needs graph:

1. Walk back from the target along `needs`. A topic with footprints or a
   known mark is treated as reached: it is not a stop, and its own needs are not
   walked. (The prototype lists every unvisited ancestor, including those
   behind a place the reader has already been, which sends a learner who has
   worked on Equivalent fractions back to what that needed.)
2. Order the remaining stops topologically. Among stops that are ready, prefer
   one in the same district as the previous stop, then lower depth, then name.
   The route then finishes a district before crossing a bridge.
3. Each stop shows its first teaching step the reader has not visited, as a
   link: "Start with: Adding slices". A town still being built says "No page
   teaches this yet" and stays on the route, because the need is real.
4. The route is drawn as the prototype draws it, with numbered stops, and the
   view fits it. If nothing is left: "Everything this needs, you have worked
   on" or "Nothing comes first".

*Places you could go next* (open doors) lists, in the home panel, towns without
footprints whose every need has footprints or a known mark, by depth, at most
eight. It shows only once the reader has worked somewhere. This is the "no
locks" map's answer to a locked tree's "unlocked": nothing was ever closed,
these are just the doors that are open for you now.

### 4.6 Course routes

`course_routes()` walks each course file's `contents:` series by series and
page by page. For each page it appends, in step order, every topic in which
that page is a teaching step and that is not already on the route; a page that
is a landmark adds the landmark to that series. The route is the list of
stops per series. While walking, it notes any topic reached before one of its
needs when that need is taught somewhere on the same course: "Course X reaches
Adding fractions before Equivalent fractions". That is evidence for the
course's author, not an error, and `check.py` prints it for a course file.

Because every page is placed, every course has a route: the two courses the
tree could not show (The Zen of Slashes and Surds, Full Stack) appear like the
rest.

### 4.7 The teacher's coverage layer

A layer under *For teachers*, off by default: choose a descriptor (the module
codes in `planning/curriculum/outcomes.yaml`). Towns serving any of its
outcomes are ringed; the rest dim. The panel lists every outcome of that
descriptor with its state: *served by* (the topics, each with its teaching
steps as section links), *off the map* (from *map/culled.yaml*: became a
landmark, with the link, or kept as a record for coverage, with the reason),
*not taught here* (from `planning/curriculum/out-of-scope.yaml`, with what is
kept and why). A build note, and the CI test, make sure no outcome is in none
of these. The strings are plain even though teachers are the audience, because
students see the page.

`planning/CURRICULUM_MAP.md` stays the teacher's full report, generated by
`dev/curriculum_map.py` from the same data (phase 6), with its sequence graph
of back-references (`back_references()`) intact.

### 4.8 topics.html, topic-groups.yaml and the knowledge-map figure

**`topics.html` ("Browse by topic")** was the one page where everything about a
subject sat together. The map's list does that job better: every placed page
is in it, grouped by region and district and ordered within each topic, where
`topic-groups.yaml`'s 34 hand-kept groups missed pages and needed a test to say
so. `write_topics_page()` goes; `topics.html` redirects to the map.

**`topic-groups.yaml`** has three readers: the browse page (gone in phase 3),
the Library's `groups` facet (regions from phase 6), and the pair game's
section labels (districts from phase 8). It is deleted in phase 8. Its intros
are worth reading when district blurbs are written; the search run already
had them as evidence.

**The knowledge-map figure** ("How the tutorials relate",
`render_knowledge_map()`) showed one series only. 6.2 kept it because its
dashed "builds on" arrows recorded evidence found nowhere else. That evidence
now lives in two places: the course routes on the map, and the sequence graph
in `planning/CURRICULUM_MAP.md`, built from the same back-references. The
figure is deleted.

### 4.9 The vendor bundle

`assets/vendor/standalone.bundle.js` is built from `assets/tutorial-runtime.js`
and everything it imports (`vendor-src/build-vendor.mjs`). This design adds a
new, separate module (map.js), edits only `build.py`-generated markup on
tutorial pages (the crumb line, which the runtime does not redraw), and
reads `localStorage` directly, so the runtime is untouched and no phase needs
Node.

One consequence is accepted rather than fixed here. `NON_TUTORIAL_PAGES` in
the runtime (line 45) is a hard-coded list of page slugs that get no Notes
section: `index`, `tree`, `about`, `topics`. The map's slug is `map`, so the
map page shows the Notes section, as course pages, All tutorials and the
features page already do, because the list never covered them either. Adding
`map` would force a bundle rebuild for one slug; the better fix is a manifest
flag for every generated page, done once with one rebuild (section 7,
question 4).

---

## 5. Phased implementation plan

Eight pull requests, each leaving the site working. Each lists what it changes,
the tests it adds, and the documents it must update under CONTRIBUTING.md's
rule. Proposed test files are in italics.

**PR 1 — The map's data, read and checked.** Adds *map/* (README, regions,
region files, landmarks, culled), converted from the search's revised map by a
one-off converter kept in this folder (not read by the build). Adds `MAP`,
`load_map()`, `check_map()`, `map_depths()` to `build.py`; `build()` calls them.
The tree still draws from `topics.yaml`; nothing a student sees changes.
`check.py` reports map placement. Lands only after Josh has read the revised
map's open questions.
*Tests*: *tests/build/test_map_data.py*: schema and shorthand; unknown page,
practice page, archived page; anchor checks including a repeated heading's `_1`;
cycles reported as a path; outcome typo guard; placement, redundant-need and
unserved-outcome notes; a `TestTheRealMap` class holding the real repository to
every live and beta page placed and every outcome served, culled or out of
scope. `tests/build/test_check.py` for the new line.
*Documents*: *map/README.md*; `ARCHITECTURE.md` §1; `docs/build-explained.md`;
`docs/WRITING_TUTORIALS.md` ("Putting a page on the map"; the `topic:`
paragraph goes); `docs/CHECK_YOUR_WORK.md`; `CLAUDE.md`'s table;
`planning/topic-map/README.md`; a `DECISIONS_LOG.md` entry recording 2.1.

**PR 2 — Positions and land.** Adds *dev/map_layout.py* (built, and deterministic) and the committed layout
(built, as *map/layout.json*) from one run. Adds
`place_new_topics()` and `map_geometry()` to `build.py`, with notes for placed,
drifted and stale towns. No page yet.
*Tests*: *tests/build/test_map_geometry.py*: the same input gives the same
bytes; a new topic lands inside its own county, at least the spacing from
every town, and no other town moves; every town is
inside its region's land; paths are closed; the real map's geometry stays under
the time budget. *tests/test_map_layout_script.py* for the dev script (a
different name from the build test, since pytest refuses two test modules with
one basename).
*Documents*: `docs/dev-scripts-explained.md`; `docs/build-explained.md`;
*map/README.md* (positions, moving a town); a `DECISIONS_LOG.md` entry
(positions are source; the build never moves a town).

**PR 3 — map.html replaces tree.html and topics.html.** Adds `section_cells()`
(for PR 4, cheap here), `map_data()`, `render_map_svg()`, `render_map_list()`,
`write_map_page()`; *assets/map.js* (levels, labels, selection, street, panel,
bottom sheet, search, keyboard route, reduced motion, roads layer); map tokens
and styles in `assets/tutorial-style.css`. Deletes `assets/tree.js`, the tree
and figure code and CSS listed in 3.1, and `write_topics_page()`; keeps
`load_topics()`, `topic_tiers()` and `load_topic_groups()` for the Library
facets until PR 6 (and rewrites `topic-groups.yaml`'s header to say so).
Redirects for `tree.html` and `topics.html`. Contents-page sentence.
`GENERATED_PAGES`. Deletes or rewrites the doc references to `assets/tree.js`
(3.5).
*Tests*: *tests/build/test_map_page.py*: the page, island, SVG and list are
written; every topic and every step link is in the list; list links carry
progress attributes inside `.dl-contents`; no leftover tokens; report doors for
`map`; island under 200 KB; two builds identical; `tree.html` and `topics.html`
not written as pages. `tests/build/test_old_addresses.py` for the redirects.
The deletions in 3.4. *tests/e2e/test_map.py*: region names at the whole
map, district names at the middle, town names close up, and no two visible
labels overlap at any level; opening a town fills the panel, draws the street
and sets the address; search finds "Fractions" from "fraction"; the skip link,
arrow-key panning, Escape, and a list button that opens a town and moves focus
to the panel heading; the bottom sheet's three heights at 390px and the town
staying above the sheet; no animation frames under either reduced-motion
signal; dark theme uses the dark tokens; no sideways scroll at 360, 768 and
1400px; the open town is never under a control.
*Documents*: `ARCHITECTURE.md` §1 and §2 and the "Where to start" table;
`docs/build-explained.md`; *docs/map-js-explained.md*;
`docs/tests-explained.md`; `docs/tutorial-runtime-explained.md`;
`assets/my-notes.js`'s comment; `README.md`; `pages/about.md`,
`pages/features.md`, `pages/studying.md`; `docs/FOR_STUDENTS.md`;
`docs/FAQ.md`; a `DECISIONS_LOG.md` entry with section 6's supersessions for
the tree and figure.

**PR 4 — Where you have worked, directions and open doors.** Adds `sections`,
`headings` and `legacy` to the island; the progress index, footprints, the
street's ticks, "I already know this", directions and open doors to map.js.
*Tests*: *tests/build/test_map_page.py* additions: a section's cell list;
world-variant ids reduced to base ids; `legacy` for a page with an old address.
*tests/e2e/test_map_progress.py*, seeding records the way
`tests/e2e/test_saved_progress.py` does: footprints only where a step's cell
ran; a section step counts only its own cells; a prose-only page shows
nothing; the badges setting off hides footprints; a legacy-keyed record counts;
directions stop at visited and known towns and keep a same-district order; the
rendered strings contain none of the forbidden words.
*Documents*: *docs/map-js-explained.md*; `docs/FOR_STUDENTS.md` (what the map
shows about your work, and that it stays in this browser); a
`DECISIONS_LOG.md` entry on what the map may claim.

**PR 5 — From every page to the map, and courses as routes.** Adds the
`dl-crumb-map` line in `crumb_trail_html()`, its stripping in
`standalone_html()`, the course page line, `course_routes()` with the
course-order note, the course view in map.js, the note in `check_course()`,
and optionally topic names in the search index.
*Tests*: `tests/build/test_courses.py`: the line for a page teaching one topic,
two topics, a landmark, a practice page (its tutorial's), and none for an
unplaced draft; the course page link. `tests/build/test_downloads.py`: no map
line in a downloaded copy. *tests/build/test_map_page.py*: routes in series
order; the course-order note. *tests/e2e/test_map.py*: `#page:<slug>` opens the
right topic and marks its stop; `?course=` fits the route, dims the rest and
lists it by series. `tests/e2e/test_multi_course_pages.py`: redrawing the
course and series rungs leaves the map line in place.
*Documents*: `docs/FOR_STUDENTS.md`; `docs/WRITING_TUTORIALS.md`;
`ARCHITECTURE.md` §1 step 5; `docs/CHECK_YOUR_WORK.md`; a `DECISIONS_LOG.md`
entry.

**PR 6 — `covers:` and `touches:` retire; coverage and the Library come from
the map.** `dev/curriculum_map.py` reads the map and regenerates
`planning/CURRICULUM_MAP.md`. `tutorial_facets()`, `LEVEL_BANDS` (re-tuned,
counts recorded), `write_reference_index()`'s new shape, and
`warn_about_titles_and_overlap()` move to the map; `load_topics()`,
`topic_tiers()` and `load_topic_groups()` go. `compose/dewmini.js` reads group
labels from the index. `covers` joins `MOVED_FRONTMATTER` and `OLD_FIELDS`; the
companion refusals go. One mechanical commit removes every `covers:` block. The
pull request carries a one-off comparison, per outcome, of the old claimed
sections against the map's teaching steps, for review; it is not kept.
*Tests*: `tests/test_curriculum_map.py` against a fixture map;
`tests/build/test_reference_index.py` (level from depth, subject and groups
from regions, rearranging needs re-files a term, the new shape);
`tests/build/test_tutorial.py` (`covers:` refused with the message);
`tests/build/test_check.py`; `tests/build/test_practice.py` and
`tests/build/test_context.py`; `tests/e2e/test_dewmini_workbench.py`.
*Documents*: `docs/WRITING_TUTORIALS.md` (the `covers:` section goes; the
outcomes paragraph is rewritten); `.claude/skills/tutorial-glossary/SKILL.md`;
`docs/DEWMINI.md`; `planning/REFERENCE_PANEL.md`; `CONTRIBUTING.md`;
`.github/workflows/tests.yml`'s comment; `docs/dev-scripts-explained.md`; a
`DECISIONS_LOG.md` entry amending 7.36 and 7.101.

**PR 7 — The teacher's coverage layer.** Adds the `outcomes` block to the
island and the layer to map.js.
*Tests*: *tests/build/test_map_page.py*: every outcome is in exactly one state.
*tests/e2e/test_map.py*: the layer rings exactly the serving towns and lists a
culled outcome with its landmark link.
*Documents*: *docs/map-js-explained.md*; `README.md`'s section for teachers; a
`DECISIONS_LOG.md` entry.

**PR 8 — The tools follow the map; the old files go.**
`dev/build_topic_editor.py`, `dev/apply_topic_edits.py`,
`dev/build_topic_game.py` and `dev/pair_results.py` read and write *map/*;
`topic_editor/index.html` and `topic_tree_game/index.html` regenerated;
`dev/draw_topic_graph.py` deleted; the pair-report CI step changes (3.3);
`topics.yaml`, `strands.yaml` and `topic-groups.yaml` deleted; `tree.html` and
`topics.html` leave `GENERATED_PAGES` if nothing names them.
*Tests*: `tests/test_pair_results.py`; *tests/test_topic_editor_round_trip.py*
(export then apply reproduces the map and positions); `tests/build/test_site.py`
(both tools still published); `tests/build/test_curriculum.py`'s duplicate-key
test.
*Documents*: `topic_editor/README.md` and `topic_editor/help.html`;
`topic_tree_game/README.md` and `topic_tree_game/help.html`;
`docs/dev-scripts-explained.md`; `ARCHITECTURE.md`; `planning/topic-map/README.md`
and `planning/topic-map/BRIEF.md`; a `DECISIONS_LOG.md` entry.

**Follow-ups, not part of the replacement.** A manifest flag for generated
pages in place of `NON_TUTORIAL_PAGES`, with one bundle rebuild (question 4).
The authoring editor adding a new page to a topic in the same commit that adds
its course line (question 3).

---

## 6. Superseded and amended decisions

| Entry | Status | One line |
|---|---|---|
| 5.9 | Superseded | The contents-page map, already moved by 6.1, is deleted; the map page is the picture of the material. |
| 5.10 | Superseded | The figure it sized is gone; the map fills the frame between the docks. |
| 6.1 | Superseded | The topic tree is replaced by the map (regions, districts, topics, steps); still its own page, now *map.html*. |
| 6.2 | Superseded | "How the tutorials relate" is deleted; course routes and CURRICULUM_MAP.md's sequence graph keep what it showed. |
| 6.3 | Amended | Still the shell, so theme is still free; the map adds land tokens to the site stylesheet. |
| 7.6 | Amended | "Needs means you cannot start without it; use as few as are true" stands (the brief's rule); Tree C's edges are replaced by the new topics' needs. |
| 7.8 | Superseded | Depth is distance from the centre, not rows down the page. |
| 7.13 | Superseded | Divide and conquer's place is whatever the new map says; the entry is evidence, not a constraint. |
| 7.14 | Superseded | No `PRE-` codes or groundwork state; a topic no descriptor asked for has empty `outcomes`. |
| 7.15 | Amended | Region names are on the land and the key is in the panel; colour is never the only cue (patterns, 7.283). |
| 7.16 | Amended | Controls float over the map, but fitting treats their corner as off-screen and a test keeps them off the open town. |
| 7.18 | Amended | Still true; a step naming an archived page now fails the build instead of being skipped. |
| 7.36 | Amended | CURRICULUM_MAP.md is generated from the map's `outcomes` and steps, not `covers:`. |
| 7.82 | Amended | "Browse by topic" is retired into the map's list; the search box part stands. |
| 7.101 | Amended | Subject from the region's `subject`, level from map depth with re-tuned bands, groups are regions; still derived, never tagged. |
| 7.141 | Amended | Its `topic-groups.yaml`, `strands.yaml` and `topics.yaml` additions are superseded by map placement; the DBM outcomes stand. |
| 7.144 | Amended | Its two browse groups are superseded; the pages are placed on the map (orientation pages as landmarks). |
| 7.145 | Amended | Its five browse groups are superseded by map districts. |
| 7.146 | Amended | Its `covers:` mappings and `strands.yaml` columns are superseded by map placement; the WA outcomes stand. The repeated-heading gap it recorded is closed by checking real heading ids. |
| 7.170 | Amended | The map's frame sits between the docks as the reading column does; the tree-page centring it fixed is gone. |
| 7.173 | Extended | Topic placement joins reading order outside the tutorial files. |
| 7.208 | Amended | "A context page carries no `covers:`" is moot; a context page is a `context` step or a landmark. |
| 8.2 | Amended | The map page carries the report doors (`map`); `tree.html` and `topics.html` are redirects. |

---

## 7. Risks and open questions for Josh

Each with a recommendation.

**1. Topic ids become a small contract.** They appear in addresses
(*map.html#adding-fractions*, and in any link a teacher pastes into a class
page) and in learners' "I already know this" marks. Saved work does not depend
on them (footprints come from pages), so this is milder than a cell id.
*Recommendation*: treat ids as stable once PR 3 ships; rename only through
`aliases:`, which the map resolves.

**2. Should learners be able to mark "I already know this"?** It makes
directions useful to returning adults and costs a second glyph. The risk is a
learner skipping something they half know.
*Recommendation*: yes, as the learner's own statement, drawn apart from
footprints and invisible to the teacher layer.

**3. Enforcing "every page placed".** A build failure would break an author's
local build the moment they create a page (the editor's template has no
`status`, so a new page is live); a CI test fails the pull request instead.
*Recommendation*: build note plus CI test, as `topic-groups.yaml` is held to
account today, and a follow-up teaching `assets/editor.js` to add the page to
a topic in the same commit that adds its course line.

**4. The Notes section on the map page.** Leaving `NON_TUTORIAL_PAGES` alone
avoids a bundle rebuild, and course pages already show Notes.
*Recommendation*: accept it for the replacement; then one small pull request
that replaces the slug list with a manifest flag set on every generated page,
with the one rebuild that needs.

**5. Towns no page teaches yet.** The old tree drew planned topics; the map
could show them dashed ("No page teaches this yet") or hide them from learners.
Showing them tells the truth about gaps, and directions stay correct about what comes first.
*Recommendation*: show them, dashed, and let directions include them as stops
that say so.

**6. Re-layout moves every town.** Learners build spatial memory; a full
layout run erases it.
*Decision, 2 October 2026 (Josh)*: this is accepted. The map may change, so the
script lays everything out again each time and there is no mode that holds
towns still.

**7. The pair game and the old judgements.** Retargeting the game is cheap and
gives a way to test the new needs; the old judgements are keyed to codes that
no longer exist.
*Recommendation*: retarget the game and `dev/pair_results.py` to map ids; keep
the three existing reports unchanged as the record; take their regeneration
out of CI.

**8. Deleting the old YAML.** Keeping `topics.yaml` "as a record" invites edits
that change nothing.
*Recommendation*: delete `topics.yaml`, `strands.yaml` and `topic-groups.yaml`
in PR 8. Git history, `replaces`, and the kept pair reports are the record.

**9. The teacher layer on a student page, or its own page?** A separate page
means a second drawing to keep in step.
*Recommendation*: a layer, off by default, labelled *For teachers*, with plain
wording; `planning/CURRICULUM_MAP.md` stays the full report.

**10. The `topic:` link form.** `docs/WRITING_TUTORIALS.md` documents
`topic:MIT-3.2` links resolved by `taught_where()`, but `build.py` has no such
resolution and no tutorial uses one.
*Recommendation*: delete the paragraph in PR 1. If an author later wants
"link to whichever page teaches this", *topic:&lt;id&gt;* against the map is a
small addition.

**11. Levels for the Library rail will shift.** The new graph is deeper near the
start (fractions are several topics), so the old bands would put too much in
"beginner".
*Recommendation*: re-tune `LEVEL_BANDS` once in PR 6 for a spread like 7.101's,
and record the counts in the entry.

**12. Weight on slow networks.** About 150 KB of island and 60 KB of SVG before
compression, perhaps 50 KB over the wire.
*Recommendation*: accept, with the size test in PR 3 as the guard.

**13. The search run's output is the input.** PR 1 converts whatever the
revised map says; a weak district or a wrong need becomes the site.
*Recommendation*: PR 1 waits until the revised map validates with no errors
(`python3 planning/topic-map/validate.py graph …`) and Josh has read its
`questions`; PR 1's converter refuses a map that does not validate.
