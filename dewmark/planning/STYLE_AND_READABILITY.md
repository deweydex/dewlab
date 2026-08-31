# Style and readability

The nitty-gritty: how a dewmark page looks, prints, and reads, and for
whom. The audience is the same as dewlab's — QQI Level 5/6 adult learners,
many returning to education, sitting the highest-stakes hour of their
module — so readability decisions carry more weight here than anywhere
else in the family.

## 1. The visual family, and the exam signal

dewmark inherits the `--dl-*` token system: the navy and orange, the
Georgia-serif reading face, the sans UI face, the spacing scale. A dewmark
page should be recognisable at arm's length as kin to the tutorials — and
distinguishable at the same distance as an exam, because dewlab's own
design rules require that a student can tell practice from assessment at a
glance (planning/DECISIONS.md in the root). Proposed signal, held
loosely: a full-width header band in the navy with the institution and
module lines set formally (the MIT name-card treatment, promoted to the
page header), a small EXAMINATION wordmark, and none of the tutorial
chrome — no series navigation, no progress badges, no texture panel
beyond what §4 keeps. Practice builds of the same paper get the tutorial-
side header treatment and a PRACTICE label. The exact treatment is
DM-14; the requirement — unmistakable at a glance, in both directions —
is not negotiable.

Class prefix: `.dm-*`, own stylesheet built on the shared tokens.
dewmini's `--dm-*` custom-property namespace is already taken; dewmark's
tokens, where it needs its own, use `--dmk-*`.

## 2. Reading the paper

- Body text 17–18px serif, line length capped near dewlab's measure
  (~34rem), left-aligned, never justified.
- Question numbering and marks are typographically loud — the two things
  a student scans for under time pressure. Marks render consistently as
  "(4 marks)" at the question head and "(2)" at part level, generated
  from the model, never hand-typed.
- Maths is KaTeX rendered at build time; inline maths must not change
  line-height (KaTeX CSS embedded, fonts embedded as WOFF2 data URIs in
  offline builds — the size cost, likely 1–2 MB, is accepted for zero
  network).
- Answer areas are visually quiet but unmistakable: a left accent border,
  a background one step off the page ground, and a persistent label. The
  answered state changes the accent (the practice exam's answered-border
  idea, kept) so a scroll-through shows gaps immediately.
- The marks-to-rows rule for text answers: 1–2 marks → 3 rows, 3–5 → 6
  rows, 6+ → 10 rows, always grow-on-type. The box's starting size is
  quiet guidance about expected depth; the growth means it never limits.
- Hover-only affordances are forbidden. The practice exam's glossary
  tooltips worked only with a mouse; anything explanatory opens on
  click/tap/focus and closes with Escape.
- Scaffolds (when the variant ships them) render as placeholder-style
  text that disappears on typing — visually distinct from the prompt so
  a student never mistakes a hint for content that must be preserved.

## 3. Screen layout

Fixed slim header (title, student, save indicators, finish), one main
column, side panel collapsible and remembered. No `100vh`/`overflow:
hidden` shell: the page scrolls as a document, which keeps browser find,
keyboard paging, and OS zoom behaving normally (both experiments trapped
scroll inside inner panes). The runner targets a laptop first — that is
what exam rooms have — but must remain usable at 768px (side panel
becomes a bottom sheet, the reference-panel precedent) because take-home
practice happens on whatever the student owns. Nothing horizontal
scrolls except code and wide tables, each inside its own scroll
container.

## 4. Student-adjustable texture

A reduced texture panel: font size and line-length only, persisted per
browser under `dewmark:texture`. The tutorials' full panel (theme, font
family, link colour) stays tutorial-side; an exam benefits from fewer
knobs. Dark theme on screen is offered (same token-swap mechanism the
family already uses) but print is always light. Motion: the only
animations are save-indicator transitions, all under
`prefers-reduced-motion` guards.

## 5. Print

Print is a first-class output in three places — the student's safety
copy, the snapshot, the graded PDF — and they share one print stylesheet:

- `beforeprint` expands every answer area to full content height;
  nothing is ever clipped by a scroll box.
- Repeating page header (name, id, exam id, page numbers) via
  positioned running elements; identity on every sheet because printed
  pages get separated.
- Page breaks: never inside a part's prompt-plus-answer; long-form
  questions (Section-B scale) start a fresh page.
- Code prints black-on-white regardless of screen theme; figures print
  at layout width; empty answer areas print with a visible border and
  the word "(unanswered)" so a marker reading a PDF sees an absence,
  not a formatting accident.
- Chrome (panels, buttons, indicators, banners — including the assessor
  banner) is hidden in print without exception; the assessor variant
  instead prints "MODEL ANSWERS" in the running header.

## 6. Accessibility

Baseline commitments for phase 1, not aspirations: every input has a
real `<label for>`; the paper is navigable by headings and by a correct
tab order; focus is always visible; colour never carries meaning alone
(answered/unanswered pairs an icon with the accent change); contrast
meets WCAG AA in both themes; all build-generated images carry alt text
supplied in the source (*build error* when missing — the tutorial
build's `check_alt_text` rule, inherited).

Honestly harder, and registered rather than promised: a fully
screen-reader-sittable exam (live code cells, structured sketch fields,
and KaTeX all have real screen-reader friction), and the
`diagram-label` type. DM-17 holds the question of what dewmark commits
to and by when — the institution's existing answer for such cases
(alternative arrangements) is the interim, and the format should at
least never make a question's content *only* available as an image.

## 7. Voice

Instructions and UI copy follow the pedagogical style guide's register,
one notch more formal: calm, specific, no exclamation marks, no idioms,
and every error state says what happened, whether work is safe, and
what to do next, in that order. The finish flow in particular is written
against the reader who has forty seconds left: the checklist leads with
counts, not sentences.
