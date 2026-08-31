# Where we are

A running ledger of the asks in this stretch of work and where each one
stands. Organised by what you asked for, not by what the diff happens to
touch, so you can scan for your own request rather than reverse-engineer
it from a commit list.

Everything below lives on `claude/dewlab-remove-mini-ide-c8c35d`
(**PR #90**, still a draft). The design reasoning is in
`planning/DEWMINI_WORKBENCH.md`; the decision record is `DECISIONS_LOG.md`
7.98–7.101.

Last updated: 2026-08-31.

---

## 1. Remove Mini IDE

> *"make sure that we complete the phase of our plan where we remove
> mini-ide and all references to it… I am a bit nervous that we will miss
> a reference either in documentation or code"*

**Done.** `DECISIONS_LOG.md` 7.98.

- Every Mini IDE file, asset and build path is gone, not just retired.
- The redirect went too, on your follow-up — nothing has been shared with
  students, so there was nobody to redirect.
- Documentation reads as though dewmini is the only workspace there has
  ever been, in the present tense, with no "formerly", no "instead of",
  no comparison to a sibling.
- The one place the old name survives on purpose is `DECISIONS_LOG.md`,
  which is a history and would be false without it.
- The deploy workflow's download-count check had an exclusion naming Mini
  IDE's bundle; it now names what actually exists.

**Your nervousness was justified and the check was mechanical**, not a
read-through: a repo-wide search for every spelling of the name, run again
after each removal.

---

## 2. The workbench build

> *"tabs and maybe some side bars on either side with things like file
> imports and maybe even things like variable inspectors and other
> pedagogical tools… a more complete documentation in the form of
> reference with search and maybe category navigation as the left side
> bar? But the right settings bar maybe we also want to simplify and make
> more into notes and other pedagogical ideas"*

**Done.** `DECISIONS_LOG.md` 7.99. Widgets deferred, as you asked.

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
| Widgets | **Deliberately not done** — you deferred them |

Two calls in there are yours to overrule, and both are one function to
reverse:

- **One Python session shared across every tab.** Per-tab namespaces
  would mean threading a namespace id through every surface that runs
  Python. Instead the sharing is made visible in the Variables list.
- **The reference shows terms from tutorials you haven't reached.** The
  tutorial pages' own Reference deliberately never does this. A workspace
  has no position in a series to protect, so this one drops the rule.
  `planning/DEWMINI_WORKBENCH.md` §4.

---

## 3. Network — can a cell actually reach the web?

> *"Do we have the ability to fetch stuff from our world in data in
> principle? Can a cell handle a request out to another site?"*
> …then the screenshot: `urllib.error.URLError: unknown url type: https`

**Done.** `DECISIONS_LOG.md` 7.100.

**I told you twice that this was impossible, and I was wrong both times.**
I said `requests` "isn't available and can't be", and that pandas could
not read a URL in a browser. Neither is true. Your question — *"can you
check if those libraries are supported and we just need to fetch them
separately?"* — is what caught it.

What's true:

- Pyodide ships `requests`, `httpx`, `aiohttp`, `urllib3` and
  `pyodide-http`. They were simply never loaded.
- `pyodide-http` is **9.6 KB** and covers `urllib`, which is what pandas
  uses. It now loads at boot on both engine paths. OWID's own snippet
  works verbatim, `storage_options` and all.
- **`https` was never missing.** A Pyodide build carries no TLS library,
  so `urllib` registers no HTTPS handler and rejects the scheme before it
  ever connects. Through the patch, the *browser* does the TLS, with its
  own certificate validation. Proven against a real TLS server with
  Chromium pinned to that one certificate by public-key fingerprint —
  not told to ignore certificate errors, which would have proved nothing.
  **The `s` you teach them about is real here.**
- The cost is written down rather than hidden: the patched path blocks
  the Worker, so a hung request can't be stopped. Stop is offered and
  does nothing. That's a new way to be stuck, taken knowingly.

---

## 4. Search categories from the tree

> *"maybe maths and CS as toggles… beginner vs intermediate or advanced?"*
> *"I think the layers are actually a great proxy for beginner
> intermediate advanced! That way if we change the tree later it
> automatically changes the search"*

**Done** (`DECISIONS_LOG.md` 7.101).

- **Subject** comes from the learning-outcome prefixes already in each
  tutorial's `covers:` — MIT is maths, PDP and CMPS are computing. A
  tutorial covering both shows under both.
- **Level** is derived from `topic_tiers()`, the prerequisite depth of the
  `needs:` graph, exactly as you suggested. Nothing is hand-tagged, so
  **rearranging the tree re-files the search on the next build.**
- Bands are depth ≤2 beginner, 3 intermediate, 4+ advanced — 22 / 16 / 5
  tutorials. (An earlier attempt using shallowest-prerequisite put 150 of
  222 terms in "beginner", which told you nothing.)
- Subject and level sit on the surface; topic and kind are behind a
  "Topics" disclosure that summarises its own state ("Topics · 1 on").
- Writing the test for this caught the one place the property leaked: the
  topic row was drawing from a hand-kept list of group keys in
  `dewmini.js`, so a group added to `topic-groups.yaml` would have got no
  chip and nobody would have noticed. The groups now come from the data;
  the curated short labels remain as an override.

---

## 5. Text size

> *"this whole tab should adjust text sizes when the settings slider is
> used… let's double check the smallest text size as I have a feeling
> it's a bit small for tired eyes"*

**Done.**

Your feeling was right, and it was measurable. At the old minimum the
filter chips rendered at **10.2px**, the kind badge 9.6px, the
"introduced in" line 10.8px.

- The slider minimum moved from 15px to 16px.
- Every small UI label in the rails now has a `max(…, 12px)` floor, so
  the slider can't drive it below that.
- The whole rail does scale with the slider — that part was already true
  (everything is in `rem` off `--dl-font-size` on `html`), but it's now
  measured rather than assumed.

**Checking by eye found four things; a test found nine.** I first
measured only the elements I'd just changed and concluded it was done. A
test that walks *every* element in the rail and reports the smallest
computed size then found `<kbd>` at 10.6px, `<code>` inside a panel note
at 11.6px, the "from the web" badge at 11px, and the rail's own section
heading at 11.5px — all `em` sizes compounding inside an already-small
container, which is exactly what eyeballing is worst at. That sweep is
now the test, so the floor holds for anything added later.

Nothing in the rail renders below 12px at the slider's minimum.

The disclosure also expands **in flow**, pushing the results down rather
than floating over them — checked by comparing the row's bottom edge
against the list's top edge, not by eye.

---

## 6. Not done

Nothing here is blocking; these are the honest gaps.

- **Whether Our World in Data permits browser reads (CORS).** The sandbox
  this was built in blocks `ourworldindata.org` by every route — curl,
  browser, fetch — so it was never observed, only expected. This is the
  one thing that needs your machine and takes about a minute:
  `tests/MANUAL_CHECKLIST.md`, "A remote dataset actually loads". If OWID
  refuses, the catalogue's remote entries should be reconsidered, because
  a student shouldn't be offered a dataset that reliably fails.
- **A timeout on the patched network path.** Named as the obvious
  follow-up in 7.100 and deliberately not done — a request that hangs
  currently can't be stopped.
- **Widgets.** Deferred by you, still deferred.
- **Every "needs a real machine" item** in `tests/MANUAL_CHECKLIST.md`:
  a school machine on the school network, a phone, Safari and Firefox, a
  screen reader. None of these can be answered from here.

### Known noise, not regressions

Seven e2e tests fail in this sandbox (two `test_stop_button`, three
`test_custom_cells`, one `test_saved_progress`, one `test_editor`). All
seven fail identically on an unmodified checkout of `main`, verified in a
separate pristine worktree. Environment timing, not something this branch
broke.

---

## 7. On the shape of all this

You apologised for throwing a lot over. It's worth saying that two of the
best outcomes here came from exactly that: the "can you check if those
libraries are supported" question overturned a wrong answer I'd given
twice and confidently, and "the layers are a great proxy" replaced a
hand-tagged category scheme with one that maintains itself. Neither was
in any plan.
