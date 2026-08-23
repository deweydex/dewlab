# Visual Authoring Editor Specification

A browser-based management and editing interface enabling course maintainers to reorder series, insert tutorials, create new modules, edit Markdown content and code cells, and publish versioned releases directly to GitHub via pull requests without local terminal dependencies.

---

## 1. Problem & Architecture

Sequencing in dewlab was historically coupled to frontmatter `order:` fields across individual tutorial files, making insertions and reordering multi-file manual edits.

The editor architecture decouples sequence configuration from content files into dedicated series order files (`<series>.order.yaml`), providing a unified interface for content management and release operations.

## 2. Structural Layer — Order Files

```yaml
# tutorials/mit-pdp-maths-prog-integration/maths-and-programming.order.yaml
series: Maths and programming
order:
  - first-steps
  - storing-and-computing
  - making-decisions
```

- **Single Point of Ordering**: Moving or inserting a tutorial modifies a single line in `order.yaml`.
- **Validation**: The build verifies that every slug in `order.yaml` corresponds to a valid Markdown tutorial, and that unlisted tutorials are not silently included on the active path.

## 3. Editor Interface Architecture (`assets/editor.html`, `assets/editor.js`)

The editor runs as a standalone client-side application in the built site (`editor.html`), interacting with the repository via the GitHub REST API.

### Core Capabilities
- **Series Reordering**: Drag-and-drop or accessible keyboard controls to reorder tutorial cards within a series. Saving writes the updated `order.yaml` as a branch commit.
- **Tutorial Insertion & Creation**: Insert tutorial cards at any position or at the end of a series. Prompting for title generates a slug, initializes frontmatter, and creates a template file with standard sections, executable cells, and reflection blocks.
- **Content & Frontmatter Editing**: In-place editing of Markdown prose, YAML frontmatter, and executable Python code cells with syntax highlighting.
- **Structural Validation Preview**: Rather than maintaining a secondary renderer that could drift from `build.py`, the editor previews structural validity (cell counts, heading levels, syntax correctness, unclosed code fences, and unique cell IDs).

## 4. Authentication & Security Model

The editor authenticates against GitHub using a fine-grained Personal Access Token (PAT) with `contents:write` permissions scoped to `deweydex/dewlab`.

### Security Considerations
- **Storage**: Tokens are stored in browser `localStorage`. A persistent "Forget Token" control is available across all views, and the editor is not linked from student-facing pages.
- **Branch & PR Lifecycle**: The editor commits modifications to a dedicated feature branch and opens a Pull Request on GitHub rather than pushing directly to `main`, ensuring peer review and CI validation before deployment.

## 5. Supported Operations & Safety Tiers

Operations are categorized by their impact on student progress data:

### Safe Operations (Fully Reversible)
- **Reorder Series**: Updates `order.yaml` without mutating tutorial content.
- **Insert / Create Tutorial**: Adds new files from standardized templates.
- **Edit Prose & Cells**: Edits content within existing cell IDs.
- **Edit Frontmatter**: Updates `title`, `module`, `year`, and `packages`.
- **Set Status**: Toggles lifecycle status (`draft`, `beta`, `live`, `archived`).
- **Release New Version**: Freezes current live content and publishes the editor buffer as a new timestamped release (`YYYY.MM.DD.N`). Proposes releases automatically when cell structure or IDs change.

### Guarded Operations (Structural Impact)
- **Duplicate Tutorial**: Clones tutorial structure under a new slug and renames cell IDs to prevent local storage key collisions.
- **Move to Another Series**: Updates both series order files and the tutorial's `series:` frontmatter field.

### Destructive Operations (Restricted & Warned)
- **Rename Slug**: Modifying a slug breaks external links and orphans student progress keyed by `(module, slug)`. The editor requires archiving the old slug and creating a new module.
- **Rename Cell ID**: Renaming a cell ID in an existing release orphans saved student progress for that cell. The editor inspects original versus working cell IDs and provides an explicit warning before commit.
- **Deletion**: Hard deletion of tutorial files is disabled in the UI; tutorials are retired by transitioning status to `archived`.
