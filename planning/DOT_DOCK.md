# The masthead dot, grown into a dock

Design note, not a spec ready to build from — an exploration of replacing
the masthead's Panels disclosure (`assets/shell.html`'s `<details
class="dl-panels">`, shipped in #186) with the wordmark's own orange dot,
grown from a 7px flourish into a real control that up to six panels fan out
from. Nothing here is built. Four rounds of mockups, in order:

1. [Radial Curriculum Navigation](https://claude.ai/code/artifact/36c7d9e5-66ac-4d98-8b7d-ecac29a442a2)
   — sunburst, semicircular dial, and orbital explorations of the
   curriculum itself (module → tutorial → cell), not this dock. The
   starting point for "radial" as a shape worth trying.
2. [Edge-Docked Panel Controls](https://claude.ai/code/artifact/4b358f33-fa02-4522-b5cd-b3bdb0461e3a)
   — Panels moved off the masthead entirely, onto a screen edge: a fan
   tab (Concept A), a corner pie, a hairline rail, and a half-orbit
   handle (Concept D).
3. [More Edge Panel Controls](https://claude.ai/code/artifact/af7a0002-e52a-4fa5-b445-12c8a75e0215)
   — six variations on A and D: a straight vertical reveal, both moved to
   the top corner/edge, an explicit auto-retract sequence, a two-stage
   icon-then-label disclosure, and a phone-vs-desktop size comparison.
   Concept 7 (the half-orbit docked to the masthead's own rule) is the one
   that led here.
4. [Dot-Dock Panel Explorations](https://claude.ai/code/artifact/8fde9602-234c-488a-86c8-ee14f84662c5)
   — the dot itself as the control: a three-zone master diagram (up to
   six panels, left/right/bottom), an icon+label+sentence card variant,
   the all-icon density extreme, and the bottom zone at phone width.

## 1. The three zones, and what's actually settled

Nothing below is settled — this is the shape of the idea, not a decision.
The rough split that fell out of round 4's master diagram:

- **Left**, fanning into the page's left margin: things a reader consults
  *alongside* what they're reading — Series, Reference, Documentation.
  This is where `.dl-reference`/`.dl-seriesnav` already dock today, so
  little changes there beyond how they're opened.
- **Right**: things about the reader and their own work — Notes,
  Settings. Matches `.dl-settings`'s existing right dock.
- **Bottom**: a full-width bar, for anything that wants room rather than
  a circle — Search is the one clear candidate, since a search box needs
  space to type into that a 40px chip doesn't have.

On a phone there's no room either side of the dot to fan into (round 4's
phone mockup found this directly), so the three zones probably collapse
into one on narrow screens: everything opens as the same bottom sheet,
stacked. That's a real simplification, not a downgrade — dewlab's mobile
treatment already does this for `.dl-reference`/`.dl-settings` today.

**Icon and text size**: round 3 already established these should track
the same root font-size Settings' texture panel controls, not a separate
number — that holds here too, for whichever of round 4's three densities
(icon+description cards, plain chips, icon-only) ships. Round 3's
phone-vs-desktop target sizing (44px touch floor vs. 32px for a mouse)
also carries over unchanged.

## 2. Panel catalog

| Panel | Status | Notes |
|---|---|---|
| **Reference** | Exists (`.dl-reference`) | Unchanged in substance — this-page-and-earlier's own glossary, Math Basics, Python Basics. Only how it's opened is in question. |
| **Series** | Exists (`.dl-seriesnav`) | Unchanged. |
| **Settings** | Exists (`.dl-settings`) | Proposed narrowing: appearance and functionality only (theme, font, size, cell behaviour) — see §4. |
| **Documentation** | New idea | The real Python docs, not this course's own glossary. Feasibility question — see §3a. |
| **Notes** | Exists, inside Settings | Candidate to promote to its own dock panel, since it gets used often enough that a level of burial may cost more than a panel of its own is worth. Roadmap, not this round: highlights and reader comments alongside free-text notes — noted so it doesn't get lost, not scoped here. |
| **Search** | New idea | Site-wide, not per-page — likely extends `assets/search.js`'s existing contents/topics index rather than building a second one. Bottom zone's clearest candidate. |
| **Report / feedback** | Exists (footer doors, cell icon) | Moving it into a global dock raises a real question, since today's mechanism is build-time, not runtime — see §3b. |

## 3. Two open questions, with a proposed answer each

### 3a. Pulling Python's own documentation into a sidebar

Harder than "embed docs.python.org in an iframe" sounds, for two reasons
specific to this project:

- **CLAUDE.md's own constraint**: "no backend, no database, no API."
  An iframe fits that (still client-side-only) but adds a *live network
  dependency at read time* that nothing else in the reading surface has —
  and it breaks outright in the standalone/offline export, the same way
  `standalone_html()` already has to strip `assets/search.js` for needing
  a fetch that fails offline. A reader working from a downloaded copy
  would get a blank pane.
- **Framing may simply be refused.** Many sites send headers that block
  being embedded in someone else's page; this would need checking against
  the real site, not assumed.

The alternative — vendoring a static copy of the docs into `assets/`,
the way `assets/vendor/` already works for CodeMirror and KaTeX — solves
the offline problem but is a real content-maintenance commitment: the
Python docs are thousands of pages, they change every release, and a
license check (Python Software Foundation License; redistribution looks
permitted but wants confirming, not assuming) comes before any of that.

**Proposed instead: don't embed or vendor — link out.** A Documentation
panel that is a short, curated list of deep links into the real
docs.python.org, opening in a new tab. Costs nothing to build, nothing to
keep in sync, works identically online or off (a dead link offline is an
honest failure, not a blank pane), and it draws the Reference/Documentation
line cleanly: Reference is "what this course taught you," Documentation is
"the real thing, elsewhere, for what it hasn't." The tradeoff, stated
plainly: this is a bookmarks list, not a sidebar that shows real doc
content in place — worth being honest with ourselves about before calling
it "documentation in a sidebar."

### 3b. What a report or feedback door refers to

This is a real architectural mismatch, not just a UI question. Today's
mechanism (`build.py`'s `report_doors_html()`/`report_issue_url()`) is
entirely **build-time**: a report door is a plain link to a prefilled
GitHub issue, with `page`, `version`, and — for a cell's own report icon
— that cell's `id`, baked into the URL when the page is built. No
JavaScript constructs it and no JavaScript could ask it "what am I
looking at right now."

A Report entry living in a dock that opens from anywhere on the page has
no cell to bake a link around at build time. Three ways to give it scope
anyway, cheapest first:

1. **Always page-level** — exactly what the footer's doors already do.
   Costs nothing, loses per-cell precision.
2. **Nearest cell, at open time** — every cell's `id` is already in
   `manifest.cells`; find whichever `.dl-cell` sits nearest the current
   scroll position when the dock's Report opens, and build the same
   `report_issue_url()` shape client-side (it's a plain URL with query
   params — nothing secret about its construction, so porting the logic
   to `tutorial-runtime.js` is straightforward). Falls back to page-level
   when nothing's in view yet.
3. **Whatever's selected** — reuse `initReferenceLookup()`'s existing
   selection-detection (the "Look up" offer that appears when a reader
   selects a taught term) to scope a report to the selected passage
   specifically. More precise, but a bigger retrofit: today that
   mechanic only matches glossary terms, not arbitrary prose.

**Proposed: (2).** It's automatic without asking the reader to select
anything first, reuses data the page already ships, and needs no new
build-time machinery — only a small client-side rebuild of a URL-building
function that already exists in Python.

## 4. Settings, narrowed

Floated alongside the panel catalog, not decided: Settings currently
holds appearance (theme, font, size, motion), functionality (staged
hints, run-button labels), *and* Your Work (notes, export, custom cells,
progress). If Notes gets promoted to its own dock panel (§2), Settings
could narrow to appearance and functionality only — a real question is
where Export, Progress, and Custom Cells land if that split happens; not
answered here.

## 5. The sticky footer

Raised without a specific proposal. `build.py`'s `site_footer()` holds
exactly two things today: the copyright/licence line, and the report
doors (dropped if reporting moves into the dock — see §3b). If it moves
into the dock, whatever replaces the report doors' current always-visible
placement is the real question — not addressed here, worth its own pass
once §3b is settled either way.

## 6. If this goes ahead, roughly in this order

1. Settle the panel catalog and zone assignment for real — this document
   picks a plausible split, not a final one.
2. Spike the enlarged dot plus one zone in actual code, reusing
   `.dl-reference`/`.dl-seriesnav` exactly as they exist today — proves
   the mechanism before anything new gets built behind it.
3. Search, as its own piece of work — almost certainly extends
   `assets/search.js`'s existing index rather than a new one.
4. Documentation, only once §3a's license question is actually checked,
   not assumed.
5. The Report scope fix (§3b's option 2).
6. The Settings/Notes split (§4), if wanted.

Each a PR of its own, the same reasoning `REFERENCE_PANEL.md` §7 and
`SIDEBAR_CONTENT.md` §6 gave for staging those features the same way.
