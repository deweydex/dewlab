# The edges: a phone, a screen reader, and no network

`planning/ROADMAP.md` Phase 6 called this the equity work, and the reason is
in `PEDAGOGICAL_STYLE_GUIDE.md` §1: adult learners in Dublin further
education, many balancing work and family, some reading on a bus on a phone
with poor signal. A site that works beautifully on a desktop with a good
connection and badly everywhere else is not serving the people this project
exists for.

Three things had been asserted and never tested. This is what testing them
found. Every measurement below was taken against a real Chromium, and the
fixes are in the same change as this document.

---

## 1. Does the offline bundle actually work?

**Claim:** `write_mini_ide_bundle()` produces a folder a student can save and
reopen with no connection at all.

**Never tested.** `planning/MINI_IDE_AND_DEWMINI_NEXT.md` §2 said so
plainly: "nothing currently proves the downloaded folder actually boots with
the network disconnected on a fresh machine."

**Now tested, and it is true.** The bundle was built with a vendored Pyodide
(`dev/fetch_pyodide.py --out assets/vendor/pyodide`), served from a loopback
address, and loaded in a browser with every request to anything other than
that address aborted at the network layer.

- The page loaded with **zero** blocked outbound requests — nothing it needs
  comes from the network.
- A cell running `print(6*7)` returned `42`, and `sys.version` reported
  Python 3.13.2, with the network still fully blocked.

The claim stands. `tests/MANUAL_CHECKLIST.md` now carries the check so it
keeps standing.

*(Later note: the bundle this section tested belonged to the since-removed
second workspace — `DECISIONS_LOG.md` 7.98. The checklist's version of the
check now runs against dewmini's own bundle, which shares the same serve.py
mechanism this audit proved.)*

---

## 2. Does it work on a phone?

**Rule** (`README.md`, and the artifact guidance the project follows): the
page body must never scroll horizontally.

**It did.** At 375px — an iPhone SE, the small end of what a student
actually carries — tutorial and practice pages both scrolled sideways. Two
separate causes, both invisible at desktop width, and both are URLs, because
a URL has no space to wrap at:

- **A bibliography DOI.** `https://doi.org/10.1080/01621459.1949.10483310`
  pushed the page to 381px against a 375px viewport. Every tutorial ends
  with a "Where to Read More" section, so this affected the whole site.
- **A failure message.** When Pyodide cannot load, the error names the URL
  that failed — and that message pushed the page to **511px**, 136px of
  sideways scroll.

The second is the one worth dwelling on, because the failures compound.
A reader on a poor connection is exactly the reader who sees that message,
and the message itself then made the page unreadable on their screen. One
problem became two, for precisely the person least able to absorb it.

**Fixed** in `assets/tutorial-style.css`: `#dl-body` breaks inside a word
when a word cannot fit on a line by itself, and `.dl-status` wraps anywhere.
Every page now fits 375px exactly — tutorials, practice pages, contents,
topics.

`tests/e2e/test_narrow_screen.py` holds the line. It was checked against the
un-fixed stylesheet first: two of its three tests fail without the fix,
which is the only way to know a regression test is worth having.

**Still open, and not fixed here:** several controls are below the 24×24px
minimum target size — the previous/next navigation links, the cell insert
button, the hint icon. That is a design change rather than a bug fix and
belongs to whoever owns the visual system.

---

## 3. Does it work with a screen reader?

**Partly checked, and honestly, only partly.** What can be checked
programmatically was, across a tutorial, the contents page and the topic
page:

| Check | Result |
|---|---|
| Controls with no accessible name | none |
| Images without `alt` | none (the build already fails on this) |
| Exactly one `h1` per page | yes |
| `lang` on `<html>` | `en` |
| Landmarks (`header`/`nav`/`main`/`footer`) | present on every page |
| Heading levels without a skip | **one failure, now fixed** |

The contents page jumped from `h1` straight to `h3`, which a reader
navigating by heading level hears as a missing section. It was `h3` on
purpose — a comment in `build.py` explained that every `h2` on that page was
read as a module heading by its own markup and by a test helper. That is a
convenience for people reading the code, paid for by everyone navigating the
page by ear. Module headings now carry `.dl-module-heading`, so telling them
apart no longer depends on the heading level, and the outline is correct.

**What this is not.** None of the above is a screen-reader test. It is a
structural check, and structure is necessary rather than sufficient — it
says nothing about whether the reading order makes sense, whether the
sidebars announce themselves usefully when they open, or whether running a
cell says anything at all to someone who cannot see the output appear. That
needs a person and a real screen reader.

The pair proposed in `planning/ROADMAP.md` Phase 6 — VoiceOver with Safari,
NVDA with Firefox — is a guess at what a Dublin classroom contains and is
worth someone's disagreement before it hardens into the standard.

---

## What to do next

1. **A real screen-reader pass**, by a person, on a tutorial page with cells.
   The panels and the run/output cycle are where the risk is, and none of it
   is reachable by the checks above.
2. **Tap target sizes**, as a deliberate design decision rather than a
   patch.
3. **Re-run §1 before each release** — it is in `tests/MANUAL_CHECKLIST.md`
   now, and it is the check most likely to break silently, since nothing in
   CI builds the bundle with a vendored Pyodide.
