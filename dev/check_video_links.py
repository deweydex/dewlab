#!/usr/bin/env python3
"""Checks every YouTube link on a page students read, and says which
videos have gone.

A video on YouTube can be deleted, made private or taken down at any
time, and the build never looks at outside links, so a dead one would
sit under "Where to read more" until a student clicked it. This asks
YouTube's oEmbed endpoint about each video, the same small request a
site makes before embedding one, and needs no key:

- 200: the video is there.
- 400 or 404: YouTube knows no such video. It has gone.
- 401 or 403: the video exists but will not describe itself, which is
  what a private video and one with embedding turned off both look
  like. Listed separately, for a person to open and check. A video
  already checked and found to play, with only embedding off, goes in
  `EMBEDDING_OFF` below and counts as there.

Anything else (a timeout, a 429, a 5xx) means the check itself failed,
never that the video has gone: those are retried, and a video still
failing after the retries is reported as not checked. If more than a
quarter fail that way, the run says it could not check and changes no
issue, so a bad day on YouTube's side never opens a false alarm.

Pages read are every tutorial and practice page under `tutorials/`,
frozen releases included (they are still served), and the site's own
pages under `pages/`. `planning/video-library/` is not checked: it is a
list for authors, and a dead video there costs nobody anything.

    python3 dev/check_video_links.py            # report, exit 1 if any have gone
    python3 dev/check_video_links.py --issue    # also open, update or close the issue

With `--issue`, it keeps one open `video-link` issue, found again on the
next run by a hidden `<!-- video-links -->` marker in its body, the same
arrangement dev/report_patterns.py uses: opened when a video goes,
rewritten each run with the current list, and closed with a comment once
nothing is missing. Needs `GITHUB_TOKEN` (`issues: write`) and
`GITHUB_REPOSITORY` (`owner/repo`) in the environment.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"
OEMBED = "https://www.youtube.com/oembed?format=json&url="
LABEL = "video-link"
LABEL_COLOR = "d93f0b"
MARKER = "<!-- video-links -->"
RETRIES = 3
UNCHECKED_LIMIT = 0.25

# watch?v=ID, youtu.be/ID, /embed/ID and /shorts/ID all name the same
# eleven-character ID.
LINK_RE = re.compile(
    r"https?://(?:www\.|m\.)?(?:youtube\.com/(?:watch\?(?:[^\s)>\"']*&)?v=|embed/|shorts/)"
    r"|youtu\.be/)(?P<id>[A-Za-z0-9_-]{11})"
)

GONE, PRIVATE, CHECK_FAILED, OK = "gone", "private", "check-failed", "ok"

# Videos that answer 401 only because their creator turned embedding off.
# Each was opened by hand and plays on YouTube; add one here, with the
# date, rather than leave it reopening the issue every week. A video on
# this list that is later deleted answers 400 and is still reported gone.
EMBEDDING_OFF = {
    "rQtRK-AJOGg",  # Random Noise, Lights Out; checked 2026-09-26
}


def pages() -> list[Path]:
    """Every markdown file a student can reach, in a stable order."""
    found = sorted((ROOT / "tutorials").glob("*/*.md"))
    found += sorted((ROOT / "pages").glob("*.md"))
    return found


def links_by_video(files: list[Path]) -> dict[str, list[str]]:
    """Video id -> the pages that link to it, as repository paths."""
    where: dict[str, list[str]] = defaultdict(list)
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        for video_id in dict.fromkeys(m["id"] for m in LINK_RE.finditer(path.read_text())):
            where[video_id].append(rel)
    return dict(where)


def classify(status: int | None) -> str:
    """One oEmbed answer -> what it says about the video."""
    if status == 200:
        return OK
    if status in (400, 404):
        return GONE
    if status in (401, 403):
        return PRIVATE
    return CHECK_FAILED


def oembed_status(video_id: str) -> int | None:
    url = OEMBED + urllib.parse.quote(f"https://www.youtube.com/watch?v={video_id}", safe="")
    req = urllib.request.Request(url, headers={"User-Agent": "dewlab-video-link-check"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status
    except urllib.error.HTTPError as err:
        return err.code
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def check(video_ids: list[str], fetch=oembed_status, pause: float = 0.2) -> dict[str, str]:
    """Video id -> ok, gone, private or check-failed. A failed check is
    retried, with a longer wait each time; a firm answer is not."""
    results = {}
    for video_id in video_ids:
        verdict = CHECK_FAILED
        for attempt in range(RETRIES):
            verdict = classify(fetch(video_id))
            if verdict == PRIVATE and video_id in EMBEDDING_OFF:
                verdict = OK
            if verdict != CHECK_FAILED:
                break
            time.sleep(pause * 10 * (attempt + 1))
        results[video_id] = verdict
        time.sleep(pause)
    return results


def report(results: dict[str, str], where: dict[str, list[str]]) -> str:
    """The issue body, and what a person running it by hand reads."""
    lines = [MARKER, ""]
    sections = [
        (GONE, "Gone",
         "YouTube knows no such video any more. Each page below needs a "
         "replacement from `planning/video-library/picks.csv`, or the entry "
         "taken out."),
        (PRIVATE, "Private, or not describing itself",
         "The video exists but YouTube would not describe it: usually private, "
         "sometimes only embedding turned off. Open each one to see which."),
        (CHECK_FAILED, "Not checked",
         "The check itself failed for these, after retries. Nothing is known "
         "about the video; the next run will try again."),
    ]
    total = len(results)
    for key, heading, note in sections:
        ids = sorted(v for v, r in results.items() if r == key)
        if not ids:
            continue
        lines += [f"## {heading} ({len(ids)})", "", note, ""]
        for video_id in ids:
            lines.append(f"- https://www.youtube.com/watch?v={video_id}")
            for page in where[video_id]:
                lines.append(f"  - `{page}`")
        lines.append("")
    ok = sum(1 for r in results.values() if r == OK)
    lines.append(f"{ok} of {total} linked videos answered normally. "
                 "Written by `dev/check_video_links.py`, which runs weekly "
                 "(`.github/workflows/video-links.yml`).")
    return "\n".join(lines) + "\n"


# --- the issue ----------------------------------------------------------------


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


def ensure_label(repo: str) -> None:
    if api("GET", f"/repos/{repo}/labels/{LABEL}") is None:
        api("POST", f"/repos/{repo}/labels", {
            "name": LABEL, "color": LABEL_COLOR,
            "description": "A linked video has gone or gone private",
        })


def find_open_issue(repo: str) -> dict | None:
    issues = api("GET", f"/repos/{repo}/issues?state=open&labels={LABEL}&per_page=100") or []
    return next((i for i in issues if MARKER in (i.get("body") or "")), None)


def update_issue(repo: str, results: dict[str, str], where: dict[str, list[str]]) -> str:
    """Open, rewrite or close the one issue. Returns what it did."""
    existing = find_open_issue(repo)
    missing = [v for v, r in results.items() if r in (GONE, PRIVATE)]
    if not missing:
        if existing:
            api("POST", f"/repos/{repo}/issues/{existing['number']}/comments",
                {"body": "Every linked video answers normally again. Closing."})
            api("PATCH", f"/repos/{repo}/issues/{existing['number']}", {"state": "closed"})
            return f"closed #{existing['number']}"
        return "nothing to do"
    body = report(results, where)
    title = f"{len(missing)} linked video{'s' if len(missing) != 1 else ''} to check"
    if existing:
        api("PATCH", f"/repos/{repo}/issues/{existing['number']}", {"title": title, "body": body})
        return f"updated #{existing['number']}"
    ensure_label(repo)
    made = api("POST", f"/repos/{repo}/issues", {"title": title, "body": body, "labels": [LABEL]})
    return f"opened #{made['number']}"


def main(argv: list[str]) -> int:
    where = links_by_video(pages())
    results = check(sorted(where))
    print(report(results, where))
    failed = sum(1 for r in results.values() if r == CHECK_FAILED)
    if results and failed / len(results) > UNCHECKED_LIMIT:
        print(f"{failed} of {len(results)} checks failed; not touching any issue.")
        # By hand, say the check itself failed; on the schedule, a bad day
        # on YouTube's side is not worth a red run and an email.
        return 0 if "--issue" in argv else 2
    if "--issue" in argv:
        # The issue is the signal, so the run itself stays green.
        print(update_issue(os.environ["GITHUB_REPOSITORY"], results, where))
        return 0
    return 1 if any(r in (GONE, PRIVATE) for r in results.values()) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
