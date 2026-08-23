# Planning and Architecture Specifications

This directory contains foundational architecture specifications, design rationale, pedagogical style guides, and curriculum planning documents for dewlab.

## Document Index

### Pedagogical & Authoring Guidelines
- **[`PEDAGOGICAL_STYLE_GUIDE.md`](./PEDAGOGICAL_STYLE_GUIDE.md)** — Core teaching philosophy ("Discover first, name afterwards"), anatomy of an ideal tutorial, concrete code-and-math integration examples, cognitive load principles, and author checklist.
- **[`EXERCISES.md`](./EXERCISES.md)** — Specification for practice problem sets, fold-hidden solutions, and automated worksheet conversion from [`deweydex/Mathematics`](https://github.com/deweydex/Mathematics).
- **[`PRACTICE.md`](./PRACTICE.md)** — Interactive practice architecture and student-authored runtime cell sandboxing.

### Architecture & Engine Specifications
- **[`STATUS.md`](./STATUS.md)** — Comprehensive record of completed systems, active 100% curriculum coverage status, and upcoming roadmap phases.
- **[`DECISIONS.md`](./DECISIONS.md)** — Architectural decision matrix (libraries, visual style, hosting, versioning, editor, mathematics).
- **[`BUILD_PLAN.md`](./BUILD_PLAN.md)** — Staged implementation phases from runtime foundations to curriculum rollout.
- **[`CONTENT_AND_FILE_ARCHITECTURE.md`](./CONTENT_AND_FILE_ARCHITECTURE.md)** — Specification for tutorial Markdown source format, executable code blocks, setup inclusions, and dataset references.
- **[`VERSIONING_AND_PROGRESS.md`](./VERSIONING_AND_PROGRESS.md)** — Specification for client-side state storage, progress restoration, and schema compatibility.
- **[`VERSIONS.md`](./VERSIONS.md)** — Multi-version release lifecycle, release date versioning, canonical URLs, and archive design.
- **[`WINDOW_AUDIT.md`](./WINDOW_AUDIT.md)** — Pre-release contract audit (URL slugs, cell IDs, local storage schema, version types).
- **[`REPO_AND_EDITOR.md`](./REPO_AND_EDITOR.md)** — Repository layout, GitHub Actions deployment workflow, and authoring architecture.
- **[`EDITOR.md`](./EDITOR.md)** — Specification for the GitHub-integrated visual tutorial editor and release management interface.

### Curriculum & Syllabus Planning
- **[`CURRICULUM_MAP.md`](./CURRICULUM_MAP.md)** — Automated mapping of all curriculum learning outcomes across active tutorials (100% covered across MIT and PDP).
- **[`CURRICULUM_NOTES.md`](./CURRICULUM_NOTES.md)** — Curricular structure notes, modularization analysis, and terminology rules.
- **[`WHAT_IS_LEFT_TO_WRITE.md`](./WHAT_IS_LEFT_TO_WRITE.md)** — Curriculum writing roadmap and upcoming 5N0554 expansion.
- **[`OPEN_QUESTIONS.md`](./OPEN_QUESTIONS.md)** — Initial architectural questions, trade-off evaluations, and resolution records.
- **[`curriculum/`](./curriculum/)** — Machine-readable outcome descriptors, scope limits, topic dependency graphs, and curriculum decisions.
- **[`outlines/`](./outlines/)** — Structured outlines for all curriculum tutorial modules.

## Architectural & Educational Principles

1. **Integrated Computation & Mathematics**: Computing acts as an interactive laboratory for building mathematical intuition, while mathematics provides the analytical structure for computational modeling.
2. **Deterministic, Zero-Install Execution**: Real Python execution runs locally in the browser tab via Pyodide without server-side execution, data harvesting, or tracking.
3. **Explicit Dependency & Scope Accounting**: Curriculum coverage and scope limits are tracked in machine-readable files (`outcomes.yaml`, `out-of-scope.yaml`, `proposed.yaml`) and validated via automated CI tests.
4. **Decisions with Explicit Costs & Pedagogical Rationale**: Major technical and pedagogical choices are documented alongside their educational rationale and cost-to-change accounting.
