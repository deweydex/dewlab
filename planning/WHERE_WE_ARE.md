# Where we are

Status of the current stretch of work, organised by request rather than by
commit. Everything below lives on `claude/dewlab-remove-mini-ide-c8c35d`
(**PR #90**, still a draft). Design reasoning: `planning/DEWMINI_WORKBENCH.md`.
Decision record: `DECISIONS_LOG.md` 7.98–7.104.

Last updated: 2026-08-31.

---

## 1. Remove Mini IDE

**Done.** `DECISIONS_LOG.md` 7.98.

- Every Mini IDE file, asset and build path is gone, not just retired.
- The redirect is gone too — nothing had been shared with students, so there
  was nobody to redirect.
- Documentation reads as though dewmini is the only workspace there has ever
  been, present tense, no comparison to a retired sibling.
- `DECISIONS_LOG.md` is the one place the old name survives, since it is a
  history and would be false without it.
- The deploy workflow's download-count check now names what actually exists,
  not Mini IDE's old bundle.

Verified with a repo-wide search for every spelling of the name, repeated
after each removal.

## 2. The workbench build

**Done.** `DECISIONS_LOG.md` 7.99. Widgets deferred.

| Thing | State |
|---|---|
| Notebook tabs | Done, with a tested migration from the pre-tabs storage key |
| Left rail (Library) | Done — reference, data catalogue, help |
| Right rail (Workbench) | Done — variables, notes, files |
| Both rails open at once | Done; the notebook keeps full width until a rail is asked for |
| Reference search | Done — 248 terms, the union of every tutorial's glossary |
| Variable inspector | Done, in Python (`describe_globals()`), not JavaScript |
| Data catalogue | Done — six datasets, writing real code into the notebook |
| Shift+Enter, find-and-replace | Done |
| Widgets | Deliberately not done — deferred |

Two decisions worth flagging as reversible (one function each):

- **One Python session shared across every tab**, rather than a namespace per
  tab, to avoid threading a namespace id through every surface that runs
  Python. The sharing is visible in the Variables list.
- **The reference shows terms from tutorials not yet reached.** Settled:
  dewmini has no way of knowing what a student has been taught, so hiding
  most of the reference would mean guessing that against someone who may
  have finished the course. `DECISIONS_LOG.md` 7.104.

## 3. Network — can a cell reach the web?

**Done.** `DECISIONS_LOG.md` 7.100.

- Pyodide ships `requests`, `httpx`, `aiohttp`, `urllib3` and `pyodide-http`;
  they were simply never loaded before.
- `pyodide-http` (9.6 KB) covers `urllib`, which is what pandas uses. It now
  loads at boot on both engine paths. OWID's own snippet works verbatim,
  `storage_options` included.
- `https` was never actually missing — a Pyodide build carries no TLS
  library, so `urllib` rejects the scheme before connecting. The patch
  routes the request through the browser instead, which does the TLS and its
  own certificate validation. Verified against a real TLS server with
  Chromium pinned to that certificate by public-key fingerprint.
- Known cost: the patched path blocks the Worker, so a hung request can't be
  stopped — Stop is offered and does nothing.

## 4. Search categories from the tree

**Done.** `DECISIONS_LOG.md` 7.101.

- **Subject** comes from the learning-outcome prefixes already in each
  tutorial's `covers:` — MIT is maths, PDP and CMPS are computing. A
  tutorial covering both shows under both.
- **Level** is derived from `topic_tiers()`, the prerequisite depth of the
  `needs:` graph. Nothing is hand-tagged, so rearranging the tree re-files
  the search on the next build.
- Bands are depth ≤2 beginner, 3 intermediate, 4+ advanced — 22 / 16 / 5
  tutorials. (An earlier attempt using shallowest-prerequisite put 150 of
  222 terms in "beginner", which was uninformative.)
- Subject and level sit on the surface; topic and kind are behind a "Topics"
  disclosure that summarises its own state ("Topics · 1 on").
- The topic-chip labels now come from `topic-groups.yaml` directly rather
  than a hand-kept list in `dewmini.js`, which had been missing an update
  path — a group added to the YAML would previously have got no chip.

## 5. Text size

**Done.**

At the old minimum, the filter chips rendered at 10.2px, the kind badge
9.6px, the "introduced in" line 10.8px — below a comfortable reading size.

- The slider minimum moved from 15px to 16px.
- Every small UI label in the rails now has a `max(…, 12px)` floor.
- The rail already scaled with the slider (everything is in `rem` off
  `--dl-font-size`); that's now covered by a test rather than assumed.

A sweep of every element in the rail — not just the ones directly
changed — also caught `<kbd>` at 10.6px, `<code>` inside a panel note at
11.6px, the "from the web" badge at 11px, and the rail's section heading at
11.5px, all `em` sizes compounding inside an already-small container. That
sweep is now the test, so the floor holds for anything added later. Nothing
in the rail renders below 12px at the slider's minimum.

The disclosure also expands in flow, pushing results down rather than
floating over them.

## 6. The boot patch, everywhere (and the toolbar)

**Done.** `DECISIONS_LOG.md` 7.102.

dewlab starts Pyodide in four places. The network patch had reached two —
the two it had missed were the **downloadable** copies: a downloaded
tutorial and an exported notebook, the files someone opens with no second
machine to compare against. Both are fixed, proved by driving a real
downloaded export against a real TLS server with the certificate pinned by
fingerprint. Found by enumerating every `loadPyodide(` call in the
repository, not by re-reading the earlier fix.

**The toolbar.** Its Python and Text buttons duplicated the insert seams
between cells, and the seams are better — they add a cell where you are
looking. They are gone; the space now holds **See an example**, **Start
with imports** and **Practice**. The first seam is now drawn over an empty
notebook too, so a blank cell still has a way to start.

Also merged main (PR #91 — the insert-divider fix, CDN preconnect, boot
loading indicator). One conflict, in the generated `standalone.bundle.js`,
resolved by rebuilding it.

## 7. Resizable rails

**Done.** `DECISIONS_LOG.md` 7.103.

- Both rails now carry the same full-height drag strip. The right-hand ones
  already did; the left-hand ones (dewmini's Library, and a tutorial page's
  Reference and Series nav) were on the browser's native resize — a small
  corner triangle, not a full-height strip.
- The strips had been hung across the panel's edge, but a docked panel clips
  anything positioned outside it, so half their width was being thrown away.
  On the right edge it still worked by luck; the left-edge one did nothing
  on the first drag test. Both now sit flush inside.
- A width chosen by a reader now survives a reload.

Measured at 1440px wide, Library at 560 and Workbench at 612: the notebook
sits between them at x=598, width 191, overlapping neither.

## 8. Not done

Nothing here is blocking.

- **Whether Our World in Data permits browser reads (CORS).** The sandbox
  this was built in blocks `ourworldindata.org` by every route, so this was
  never observed, only expected. Needs a real machine:
  `tests/MANUAL_CHECKLIST.md`, "A remote dataset actually loads." If OWID
  refuses, the catalogue's remote entries should be reconsidered.
- **A timeout on the patched network path.** Named as a follow-up in 7.100,
  deliberately not done — a hung request currently can't be stopped.
- **Widgets.** Deferred, still deferred.
- **Every "needs a real machine" item** in `tests/MANUAL_CHECKLIST.md`: a
  school machine on the school network, a phone, Safari and Firefox, a
  screen reader.

### Known noise, not regressions

Seven e2e tests fail in this sandbox (two `test_stop_button`, three
`test_custom_cells`, one `test_saved_progress`, one `test_editor`) — and fail
identically on an unmodified checkout of `main`. Environment timing, not
something this branch broke.
