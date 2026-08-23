# Pre-Release Data Contracts & Storage Audit

Formal audit of data persistence schemas, slug scoping, cell ID conventions, and versioning interfaces conducted prior to public cohort deployment.

---

## 1. Executive Summary

Client-side data persistence creates long-term data contracts once users save progress locally. Modifying storage keys, cell IDs, or serialization schemas post-launch requires client-side migrations.

This pre-release audit evaluated four critical architectural contracts across all 20 published tutorials (228 runnable cells). Two scoping defects were identified and resolved.

---

## 2. Audit Findings & Resolutions

### 1. Tutorial Slugs & Storage Scoping
- **Contract**: URL paths and `localStorage` keys uniquely identifying a tutorial.
- **Finding**: Tutorial slugs are unique per module, not globally (e.g. `first-steps` exists in both `computational-methods` and `mit-pdp-maths-prog-integration`). Storage keys originally used `dewlab:progress:<slug>`, causing cross-module collision where work in one tutorial overwrote the other.
- **Resolution**: Progress keys are strictly scoped to the `(module, slug)` pair: `dewlab:progress:<module>:<slug>`. Page manifests explicitly include `module` metadata.

### 2. Cell ID Conventions
- **Contract**: Cell identifiers (`task_id`) matching student-authored code and output between Markdown source and local storage.
- **Audit Metrics**: 228 executable cells evaluated across the curriculum.
  - Conformance: 100% compliant with lowercase alphanumeric and hyphen format (`section-slug-n`).
  - Length: 5 to 48 characters (mean 18 characters).
  - Scope: 12 generic IDs reused across different tutorials (e.g. `your-turn-1`). Safe because storage is strictly scoped per `(module, slug)` pair.
- **Resolution**: Verified sound. Editor UI displays active mutation warnings if an author alters existing cell IDs in a live tutorial.

### 3. Save Record Schema & File Import
- **Contract**: JSON format for exported progress records (`{tutorial-slug, tutorial-module, tutorial-version, saved_at, cells[]}`).
- **Finding**: File import previously wrote arbitrary JSON directly to the active tutorial key before validating cell ID compatibility, destroying active work if an incorrect file was loaded.
- **Resolution**:
  - Exported JSON files include explicit `tutorial-module` and `tutorial-slug` headers.
  - Filenames include module prefixes (`<module>-<slug>-progress.json`).
  - Importer validates matching module and slug before writing to storage, safely refusing mismatched files without state mutation.

### 4. Version Field Serialization
- **Contract**: Comparison of tutorial versions during state restoration.
- **Finding**: Runtime state comparison stringifies both operands (`String(record["tutorial-version"]) !== String(currentManifest.version)`).
- **Resolution**: Verified fully compatible with dated semantic string versions (`YYYY.MM.DD.N`).

---

## 3. Summary of Verifications

| Contract Area | Status | Verification Mechanism |
|---|---|---|
| Module-Scoped Slugs | Resolved | Unit tests in `tests/test_tutorial_tools.py` |
| Cell ID Conventions | Verified | Automated crawl of all Markdown frontmatter and code blocks |
| Import Validation | Resolved | Rejection tests for mismatched tutorial payloads |
| Version Serialization | Verified | String-based equality tests during state restoration |
