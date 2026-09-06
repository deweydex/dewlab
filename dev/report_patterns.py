#!/usr/bin/env python3
"""Groups open student reports by page and by cell, and opens or updates
one `pattern` issue per page that crosses a threshold — three or more open
reports on the page, or two or more naming the same cell, both within the
last fourteen days.

A pattern issue is the request for a larger look, not a fix in itself
(planning conversation behind DECISIONS_LOG.md Phase 8): the job can only
count, so it names what it found and leaves the reading — whether a fix
already covers some of the gathered reports, whether they share a root
cause — to whoever picks it up (`.claude/skills/triage-report/SKILL.md`'s
own "Working a pattern issue" section).

Idempotent by page: a hidden `<!-- pattern-key: <page> -->` marker in the
issue body is how a second run finds the issue it already opened for a
page, rather than opening a second one — the body is replaced each run
with the current count and the current list of gathered issues, so an
existing pattern issue never goes stale even if nobody has looked at it
between two runs.

    python3 dev/report_patterns.py

Needs `GITHUB_TOKEN` (`issues: write`) and `GITHUB_REPOSITORY`
(`owner/repo`) in the environment, same as label_report.py.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

API = "https://api.github.com"
WINDOW_DAYS = 14
PAGE_THRESHOLD = 3
CELL_THRESHOLD = 2
NO_RESPONSE = "_No response_"
PATTERN_LABEL = "pattern"
PATTERN_LABEL_COLOR = "a371f7"

FIELD_RE = re.compile(r"^### (?P<label>[^\n]+)\n+(?P<value>.+?)(?=\n### |\Z)", re.S | re.M)
MARKER_RE = re.compile(r"<!-- pattern-key: (?P<page>.+?) -->")


def api(method: str, path: str, body: dict | None = None):
    req = urllib.request.Request(f"{API}{path}", method=method)
    req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if body is not None:
        req.data = json.dumps(body).encode()
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


def paginated_issues(repo: str, **params) -> list[dict]:
    found = []
    page = 1
    while True:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        batch = api("GET", f"/repos/{repo}/issues?per_page=100&page={page}&{query}")
        if not batch:
            break
        found.extend(i for i in batch if "pull_request" not in i)
        if len(batch) < 100:
            break
        page += 1
    return found


def parse_fields(body: str) -> dict[str, str]:
    return {m.group("label").strip(): m.group("value").strip() for m in FIELD_RE.finditer(body or "")}


def ensure_label(repo: str, name: str, color: str, description: str) -> None:
    if api("GET", f"/repos/{repo}/labels/{urllib.parse.quote(name)}") is not None:
        return
    api("POST", f"/repos/{repo}/labels", {"name": name, "color": color, "description": description})


def gather(repo: str) -> dict[str, list[dict]]:
    """Every open report issue, in the last WINDOW_DAYS, grouped by page."""
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=WINDOW_DAYS)
    by_page: dict[str, list[dict]] = defaultdict(list)
    for issue in paginated_issues(repo, state="open"):
        if not (issue.get("title") or "").startswith("[report]"):
            continue
        created = datetime.datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
        if created < cutoff:
            continue
        fields = parse_fields(issue.get("body") or "")
        page = fields.get("Page", "").strip()
        if not page or page == NO_RESPONSE:
            continue
        cell = fields.get("Cell", "").strip()
        by_page[page].append(
            {
                "number": issue["number"],
                "title": issue["title"],
                "cell": cell if cell and cell != NO_RESPONSE else "",
            }
        )
    return by_page


def worth_a_pattern(issues: list[dict]) -> bool:
    if len(issues) >= PAGE_THRESHOLD:
        return True
    by_cell: dict[str, int] = defaultdict(int)
    for issue in issues:
        if issue["cell"]:
            by_cell[issue["cell"]] += 1
    return any(count >= CELL_THRESHOLD for count in by_cell.values())


def pattern_body(page: str, issues: list[dict]) -> str:
    by_cell: dict[str, list[dict]] = defaultdict(list)
    page_wide = []
    for issue in issues:
        (by_cell[issue["cell"]] if issue["cell"] else page_wide).append(issue)

    lines = [
        f"<!-- pattern-key: {page} -->",
        f"{len(issues)} open report(s) on `{page}` in the last {WINDOW_DAYS} days.",
        "",
    ]
    for cell, cell_issues in sorted(by_cell.items()):
        refs = ", ".join(f"#{i['number']}" for i in cell_issues)
        flag = " — at or over the per-cell threshold" if len(cell_issues) >= CELL_THRESHOLD else ""
        lines.append(f"- Cell `{cell}`: {refs}{flag}")
    if page_wide:
        refs = ", ".join(f"#{i['number']}" for i in page_wide)
        lines.append(f"- Not tied to one cell: {refs}")
    lines += [
        "",
        "This issue only counts. See `.claude/skills/triage-report/SKILL.md`,"
        " \"Working a pattern issue,\" for what to do with it — in particular,"
        " whether a merged fix already covers some of the reports above before"
        " assuming they are all still live.",
    ]
    return "\n".join(lines)


def find_existing_pattern_issue(repo: str, page: str) -> dict | None:
    for issue in paginated_issues(repo, state="open", labels=PATTERN_LABEL):
        match = MARKER_RE.search(issue.get("body") or "")
        if match and match.group("page") == page:
            return issue
    return None


def main() -> None:
    repo = os.environ["GITHUB_REPOSITORY"]
    by_page = gather(repo)
    patterns = {page: issues for page, issues in by_page.items() if worth_a_pattern(issues)}

    if not patterns:
        print("no page or cell crosses the pattern threshold right now")
        return

    ensure_label(repo, PATTERN_LABEL, PATTERN_LABEL_COLOR, "Opened by dev/report_patterns.py — gathers several reports, not one.")

    for page, issues in patterns.items():
        body = pattern_body(page, issues)
        existing = find_existing_pattern_issue(repo, page)
        if existing:
            api("PATCH", f"/repos/{repo}/issues/{existing['number']}", {"body": body})
            print(f"updated pattern issue #{existing['number']} for {page} ({len(issues)} reports)")
        else:
            title = f"Pattern · {page} has {len(issues)} report(s) in {WINDOW_DAYS} days"
            created = api(
                "POST",
                f"/repos/{repo}/issues",
                {"title": title, "body": body, "labels": [PATTERN_LABEL]},
            )
            print(f"opened pattern issue #{created['number']} for {page} ({len(issues)} reports)")


if __name__ == "__main__":
    main()
