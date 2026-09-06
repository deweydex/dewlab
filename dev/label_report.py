#!/usr/bin/env python3
"""Labels a freshly opened report issue by its page and its kind, creating
either label the first time either is needed.

The issue form (`.github/ISSUE_TEMPLATE/report.yml`) already applies
`source: page` on every report, but it cannot apply a label whose *value*
depends on what the student actually filled in — which page, which kind —
since a GitHub issue form's own `labels:` key is fixed text, not a template.
This does that second half, called once, right after an issue opens, by
`.github/workflows/label-report.yml`.

No `kind:` label exists for "a question, an idea, or something else" on
purpose: that kind is meant to leave through Discussions rather than land
here as an issue at all (DECISIONS_LOG.md 8.4) — if one does turn up, it
gets `kind: question` all the same, since a mislabelled report is still
better found than lost.

    python3 dev/label_report.py <issue-number>

Needs `GITHUB_TOKEN` (an `issues: write` token — the job's own default
`GITHUB_TOKEN` already has this) and `GITHUB_REPOSITORY` (`owner/repo`) in
the environment, which is exactly what a GitHub Actions job already sets.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"

# GitHub renders each issue-form field as "### <label>\n\n<value>" in the
# issue body, in field order, so this is the one pattern that reads all of
# them back out regardless of which fields a given report actually filled.
FIELD_RE = re.compile(r"^### (?P<label>[^\n]+)\n+(?P<value>.+?)(?=\n### |\Z)", re.S | re.M)

NO_RESPONSE = "_No response_"

LABEL_COLORS = {
    "kind: error": "d73a4a",
    "kind: unclear": "fbca04",
    "kind: question": "0075ca",
}
PAGE_LABEL_COLOR = "ededed"


def api(method: str, path: str, body: dict | None = None):
    req = urllib.request.Request(f"{API}{path}", method=method)
    req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        req.data = data
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


def parse_fields(body: str) -> dict[str, str]:
    return {m.group("label").strip(): m.group("value").strip() for m in FIELD_RE.finditer(body or "")}


def kind_label(kind_text: str) -> str:
    lowered = kind_text.lower()
    if "error" in lowered:
        return "kind: error"
    if "wrong" in lowered or "could not follow" in lowered:
        return "kind: unclear"
    return "kind: question"


def ensure_label(repo: str, name: str, color: str, description: str) -> None:
    if api("GET", f"/repos/{repo}/labels/{urllib.parse.quote(name)}") is not None:
        return
    api("POST", f"/repos/{repo}/labels", {"name": name, "color": color, "description": description})


def page_label(page: str) -> str:
    # GitHub caps a label name at 50 characters. "page: " is 6 of them.
    return f"page: {page}"[:50]


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: label_report.py <issue-number>")
    issue_number = sys.argv[1]
    repo = os.environ["GITHUB_REPOSITORY"]

    issue = api("GET", f"/repos/{repo}/issues/{issue_number}")
    if issue is None:
        sys.exit(f"issue #{issue_number} not found in {repo}")
    if not (issue.get("title") or "").startswith("[report]"):
        print(f"#{issue_number} is not a report issue ({issue.get('title')!r}); nothing to do")
        return

    fields = parse_fields(issue.get("body") or "")
    kind_text = fields.get("What kind of thing is this?", "")
    page = fields.get("Page", "")

    to_add = []
    if kind_text and kind_text != NO_RESPONSE:
        name = kind_label(kind_text)
        ensure_label(repo, name, LABEL_COLORS[name], "Applied automatically from a report's own 'kind' field.")
        to_add.append(name)
    if page and page != NO_RESPONSE:
        name = page_label(page)
        ensure_label(repo, name, PAGE_LABEL_COLOR, "Applied automatically — every report naming this page carries it.")
        to_add.append(name)

    if not to_add:
        print(f"#{issue_number}: nothing to label (empty kind and page)")
        return

    api("POST", f"/repos/{repo}/issues/{issue_number}/labels", {"labels": to_add})
    print(f"#{issue_number}: added {to_add}")


if __name__ == "__main__":
    main()
