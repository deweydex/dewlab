# Tutorial Multi-Version Release Architecture

Technical specification for tutorial multi-version release lifecycles, dated semantic versioning, archive retention, and client-side progress compatibility in dewlab.

---

## 1. Core Architecture & Objectives

dewlab tutorials evolve over academic terms. The versioning system satisfies three fundamental requirements:
1. **Student Progress Continuity**: Updating or revising a tutorial must not disrupt an active student's session or invalidate saved cell answers.
2. **Deterministic Version History**: Prior releases remain accessible via persistent URLs, enabling cohorts to reference exact course snapshots.
3. **Draft & Staged Previews**: Authors can develop and stage new tutorials or releases (`draft`, `beta`) without prematurely replacing the default curriculum route.

A **version** represents a formal, published release of a tutorial rather than an incremental commit. Minor prose or typo fixes occur in-place; structural revisions (modifying exercises, re-architecting sections) warrant a timestamped release.

---

## 2. Release Identification & Lifecycle States

### Version Identifier Format
Versions are identified by a human-readable release timestamp: `YYYY.MM.DD.N` (e.g. `2026.09.15.1`), indicating year, month, day, and the sequence number for that day.

- **Identity & URLs**: Used in versioned URLs (`<slug>/v2026.09.15.1.html`) and manifest metadata.
- **Sorting**: Parsed numerically as four integers to ensure correct chronological sorting (`2026.08.20.10` sorts after `2026.08.20.9`).
- **Reader UI Presentation**: Rendered as standard date prose (e.g. "15 September 2026") in browser selection menus.

### Lifecycle Status Matrix

| Status | Static Page Built? | Listed in Reading Order? | Description & Access |
|---|---|---|---|
| **`draft`** | **No** | No | Internal repository work-in-progress; visible only in local development builds and the authoring editor. |
| **`beta`** | Yes | No | Publicly accessible via direct URL for testing/preview; marked with a prominent preview banner; never serves as default route. |
| **`live`** | Yes | Yes | Active canonical release; candidate for default unversioned route. |
| **`archived`** | Yes | No | Retired curriculum module; remains built at historical URL to preserve past student work; excluded from active reading order. |

---

## 3. Directory Layout & Build Resolution

Tutorials exist either as a single Markdown file (when only one release exists) or as a versioned directory (once a second release is published):

```
tutorials/mit-pdp-maths-prog-integration/
  first-steps.md                  # Single-version tutorial (standard form)
  cracking-equations/             # Multi-version tutorial directory
    cracking-equations.md         # Active working release
    v2026.06.02.1.md              # Historical frozen release
    v2026.09.15.1.md              # Historical frozen release
```

### Static Routing & SEO Structure
- **Canonical Default**: `tutorials/<module>/<slug>.html` serves the newest `live` release.
- **Historical Releases**: Built to `tutorials/<module>/<slug>/v<version>.html`.
- **Search Engine Canonicalization**: Historical release pages carry `<link rel="canonical" href=".../<slug>.html">` pointing to the canonical default URL.
- **Standalone Offline Bundles**: To maintain reasonable archive sizes, only the default `live` release is compiled into single-file offline HTML and included in series download ZIPs.

---

## 4. Client-Side Progress & State Resolution

### State Restoration Matching
Student cell state is keyed by `task_id` rather than tutorial version string. When a student opens a tutorial:
1. `localStorage` progress is retrieved using the scoped `dewlab:progress:<module>:<slug>` key.
2. The runtime matches saved cell records against active cell IDs on the page.
3. If an answer belongs to a cell ID absent from the current release, the data remains safely preserved in local storage and re-appears if the student navigates to a release containing that cell.

### Version Transition Feedback
When switching versions via the UI picker, dewlab analyzes cell ID sets in the manifest and provides exact deterministic counts:
> **15 September 2026** — 6 of your 8 answers carry over. 2 cells are not present in that version (data remains preserved in storage).

### Cohort Pinning & User Preference
- **First-time Visitors**: Default to the newest `live` release built at the unversioned URL.
- **Returning Students**: The runtime detects the release the student last saved work in and automatically maintains continuity on that version.
- **Reader Settings**: Readers can configure global preferences in the settings panel (*Stay on version last worked in* vs. *Always navigate to latest live*).

---

## 5. Editor Release Workflow (`assets/editor.js`)

1. **Working Copy vs. Original**: The editor maintains `state.original` (the fetched baseline) and the working buffer.
2. **Release Execution**: Freezes `state.original` into a new timestamped file (`v<previous-version>.md`) and publishes the working buffer under today's timestamp (`YYYY.MM.DD.1`).
3. **Change Analysis**: The editor inspects cell IDs between working and baseline text, actively prompting the author to release a new version when cell IDs have been added, removed, or mutated.

---

## 6. Semantic Cross-Referencing

In addition to static `tutorial:<slug>#<anchor>` links, dewlab supports conceptual outcome links:

```markdown
As introduced in [Linear Functions](topic:MIT-3.2) ...
```

- **Build Resolution**: `build.py` maps outcome codes (`MIT-X.Y`) to the active tutorial currently teaching that outcome via `taught_where()`.
- **Integrity Guarantee**: If an outcome is removed or archived without a successor, `build.py` raises a build failure, preventing broken pedagogical references across the curriculum.
