# Project Implementation Status & Technical Roadmap

This document provides a factual record of completed implementations, active development items, roadmap milestones, and complex architectural considerations in dewlab.

---

## 1. What Has Been Built (Completed)

The following components, runtime engines, and curriculum modules are fully implemented, tested, and verifiable in the repository:

### Core Runtime & Client Architecture (`assets/`, `setup/`, `data/`)
- **Pyodide Browser-Side Python Runtime**: Zero-install local Python execution in the browser tab with built-in support for `numpy`, `pandas`, `matplotlib`, and `sympy` (`assets/tutorial-runtime.js`).
- **Interactive Tools & Widget Bridge**: Python-side helper library providing `show`, `show_table`, `check`, `text_input`, `dropdown`, `button`, and `load_csv` (`assets/tutorial_tools.py`).
- **Clean Exception Traceback Formatting**: Exception handler in runtime tools that trims internal framework frames, presenting students with clear, unintimidating syntax errors and line-accurate tracebacks.
- **Client-Side Progress Persistence**: Local storage state persistence strictly scoped by `(module, slug)` pair, saving student code and execution outputs across browser sessions without central servers or tracking.
- **Deterministic Multi-Version State Restoration**: Version-aware progress restoration matching stable per-cell IDs, preserving student work across tutorial releases.

### Static Site Generator & Build Pipeline (`build.py`, `dev/`)
- **Markdown & Frontmatter Engine**: Robust parsing of tutorial frontmatter, executable code fences (`python exec`), hints (`hint:`), and include directives (`{{include: ...}}`).
- **LaTeX Math Pre-Processing**: Extraction of LaTeX math blocks before Markdown parsing to prevent character collisions, rendering in the browser via KaTeX.
- **Cross-Tutorial & Conceptual Link Validation**: Build-time resolution of `tutorial:<slug>#<anchor>` and `topic:<outcome-code>` links with automated build failure on dead references.
- **Multi-Version Static Generation**: Build pipeline generating canonical unversioned pages for the latest live release, alongside timestamped historical release pages (`<slug>/v<version>.html`) with search engine canonical tags.
- **Offline Standalone Bundles**: Automated compilation of standalone, single-file HTML tutorials and per-series ZIP archives (`site/download/`).

### User Interface & Navigation System (`assets/`, `shell.html`, `tree.html`, `editor.html`)
- **Responsive Reading Surface**: Accessible typography, serif prose base, distraction-free margins, and custom reader texture controls (light/dark/auto themes, font families, line-width scaling, minimal header mode).
- **Table of Contents & Navigation**: Dynamic table of contents with automatic filtering of repetitive prompts, sticky mastheads, and declared module ordering (`tutorials/modules.yaml`).
- **Interactive Curriculum Dependency Tree**: Visual graph viewer displaying learning outcome strands, prerequisite dependencies, zoom/pan navigation, and direct tutorial links (`assets/tree.js`, `assets/tree.html`).
- **GitHub API-Backed Visual Authoring Editor**: Browser-based management interface supporting series reordering, tutorial creation, frontmatter editing, cell-ID mutation warnings, structural linting, and release publishing via GitHub API pull requests (`assets/editor.js`, `assets/editor.html`).

### Comprehensive Curriculum Modules (`tutorials/`)
- **71 Published Tutorial & Practice Pages** — 35 tutorials, 32 practice pages
  (one per tutorial, except the three that are already problems or reflection),
  and 4 mixed sets drawing on several tutorials at once. See
  `planning/EXERCISES.md` for where the problems came from.
  - `computational-methods` (2 tutorials, 2 practice pages): `first-steps.md`,
    `working-with-tables.md`.
  - `mit-pdp-maths-prog-integration` (67 tutorial and practice files):
    - *Foundations & Programming Spine*: `first-steps.md`, `storing-and-computing.md`, `making-decisions.md`, `repeating-yourself.md`, `lists-and-sequences.md`, `finding-things.md`, `putting-things-in-order.md`, `building-reusable-tools.md`, `how-we-got-here.md`, `when-it-goes-wrong.md`, `the-team-project.md`.
    - *Discrete Math & Statistics*: `counting-carefully.md`, `what-are-the-chances.md`, `making-sense-of-data.md`, `pictures-worth-numbers.md`, `numbers-and-their-families.md`, `sets-as-sorted-lists.md`, `logic-and-truth.md`, `venn-diagrams.md`.
    - *Algebra, Functions & Calculus*: `expressions-come-alive.md`, `cracking-equations.md`, `rearranging-formulae.md`, `complex-roots.md`, `drawing-functions.md`, `parabolas.md`, `approaching-a-limit.md`, `rates-of-change.md`.
    - *Geometry & Trigonometry*: `lines-and-distances.md`, `the-unit-circle.md`, `sine-and-cosine-waves.md`, `solving-triangles.md`.
    - *Synthesis & Review*: `bringing-it-all-together.md`, `critique-and-reflection.md`.
    - *Interactive Practice Companions*: one `<slug>-practice.md` beside every
      tutorial above except `bringing-it-all-together`, `critique-and-reflection`
      and `the-team-project`.
    - *Mixed Problem Sets*: `mixed-programming.md`, `mixed-algebra.md`,
      `mixed-trigonometry.md`, `mixed-data.md` — problems that draw on several
      tutorials at once, declared with `practice_across:` and listed on the
      contents page under their module.

### Curriculum Coverage Status (`planning/CURRICULUM_MAP.md`)
- **100% of Descriptor Outcomes Covered**: All 67 learning outcomes across *Mathematics for IT (5N18396)* and *Programming and Design Principles (5N2927)* are fully authored, mapped, and tested with zero gaps.

---

## 2. Active Roadmap & Next Phases

### Phase 7: Computational Methods (5N0554) Curriculum Expansion
- **Objective**: Full curriculum specification, mapping, and authoring for *Computational Methods and Problem Solving 5N0554* (15 credits, 13 learning outcomes across 7 sections).
- **Status, as of the run that closed the first strand**: all 13 outcomes are
  transcribed into `outcomes.yaml` under a new `CMPS` module, with the
  descriptor's own "e.g." examples moved to `topics.yaml`'s `uses:` rather than
  folded into what coverage is measured against (DECISIONS_LOG 7.55). The
  first target strand is written and released; the other four are not.
- **Target Strands**:
  1. *Linear Algebra & Matrix Operations*: **done.** Six tutorials —
     *A Grid of Numbers*, *Multiplying Grids*, *What a Matrix Does to a
     Picture*, *Undoing It*, *Solving Systems*, *Where Chains Lead* — under
     `tutorials/computational-methods/`, series `matrices`, each with a
     practice page. `Where Chains Lead` folds in Markov chains, word-level
     text generation, and a worked small-scale PageRank, closing what were
     planned as strands 1 and 2 (and part of 3) into one series — see
     `planning/outlines/matrices.md`'s resolved open question and
     DECISIONS_LOG 7.56. `CMPS-LO4` is fully taught; `CMPS-LO1` and `CMPS-LO2`
     are touched but not taught, since only the data-structures half of LO1
     and the randomness half of LO2 came up along the way.
  2. *Markov Chains & Text Generation*: **folded into strand 1** — see above,
     rather than written as a separate strand.
  3. *Link Graph Analysis & PageRank*: **partly done**, as the closing section
     of *Where Chains Lead* — a hand-checkable three-page example rather than
     a dedicated tutorial on crawling or a real link graph, which remains
     unwritten.
  4. *Discrete Simulation & Monte Carlo Methods*: **not started.** Estimation
     of $\pi$, queuing models, randomness in computing — this is `CMPS-LO3`,
     `CMPS-LO6`, and touches `CMPS-LO2`'s randomness half.
  5. *Algorithmic Complexity & Systems Modeling*: **not started.** Complexity
     bounds, cache prediction, thermal simulation — `CMPS-LO5`, `CMPS-LO7`
     through `CMPS-LO13`, all still red on the curriculum map.

### Phase 8: Automated Worksheet Practice Converter (`dev/from_worksheet.py`)
- **Status**: on hold, and possibly not needed. The worksheets whose material is
  taught have already been converted by hand; the ones that remain (`07a`–`08b`,
  matrices, Markov chains, Bayes, distributions) cover material no tutorial
  teaches yet, and six of those carry their answer keys only as PDFs. The
  converter has nothing to convert until Phase 7 is written.

### Phase 9: Dynamic Student-Authored Runtime Cells (`planning/PRACTICE.md`)
- **Objective**: Implement client-side dynamic cell insertion in `assets/tutorial-runtime.js`, allowing students to author custom practice challenges, write verification tests, and export them as JSON snippets for peer exchange.

### Phase 10: Automated CI/CD Deployment
- **Status**: done. `.github/workflows/deploy.yml` builds and publishes the
  148-page site to GitHub Pages on every push to `main`, and has since Phase 5.
  Two further workflows guard it: `tests` runs the unit suite, and
  `standalone-bundle-is-current` fails if the vendored bundle has drifted from
  `vendor-src/`.

---

## 3. Pedagogical & Technical Complexities

### 1. Data Contracts on Live Cohort Launch
- **Pedagogical Rationale**: Students returning to a tutorial over a multi-month course must never experience lost work or broken progress indicators.
- **Implementation Guarantee**: Storage keys are strictly scoped to `dewlab:progress:<module>:<slug>`, and all cell IDs are immutable once published. The authoring editor actively intercepts and warns against cell ID modifications.

### 2. Multi-Version Isolation
- **Pedagogical Rationale**: Cohorts working in an earlier version (e.g. `2026.08.20.1`) should experience an undisturbed, stable environment throughout their term, even as new revisions are released.
- **Implementation Guarantee**: Canonical unversioned URLs serve the latest release, while returning students are automatically pinned to their last active working release with clear, deterministic carryover counts.

### 3. Student-Authored Code Sandboxing
- **Pedagogical Rationale**: Peer code sharing must be approachable and friction-free, yet safe for shared classroom machines.
- **Implementation Guarantee**: Pyodide executes entirely inside the browser tab WebAssembly sandbox without local OS filesystem access.
