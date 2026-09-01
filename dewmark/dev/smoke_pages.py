#!/usr/bin/env python3
"""A browser rehearsal for the exam page and the marking workbench.

The script builds the sample exam, sits part of it in a headless
browser — answers several question types, finishes, downloads the
submission, reloads and restores — then opens the marking workbench,
loads the scheme and the submission, marks with all three marking
methods, and checks the exports. It exists because the pieces it
exercises only fail together: a change to how answers are saved shows
up here, in the round trip, before it shows up in an exam room.

Run it by hand:

    python dewmark/dev/smoke_pages.py

It needs the playwright package and a Chromium browser. If Playwright's
own browser download is present it is used; otherwise set the
DEWMARK_CHROMIUM environment variable to a Chromium executable.
"""

import csv
import glob
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import build_exam  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("playwright is not installed; see the note at the top of this "
          "script")
    sys.exit(1)

DEWMARK = Path(__file__).parent.parent
SAMPLE = DEWMARK / "samples" / "sample-mixed-paper.exam.md"


def find_chromium():
    if os.environ.get("DEWMARK_CHROMIUM"):
        return os.environ["DEWMARK_CHROMIUM"]
    roots = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "")]
    for root in [r for r in roots if r]:
        for candidate in sorted(glob.glob(
                root + "/chromium-*/chrome-linux/chrome")):
            return candidate
    return None  # let Playwright use its own download


def main():
    workdir = Path(tempfile.mkdtemp(prefix="dewmark-smoke-"))
    build_exam.build(SAMPLE, workdir)
    student_page = workdir / "sample-mixed-2027.student.html"
    scheme_file = workdir / "dewmark_sample-mixed-2027_marking_scheme.json"
    errors = []

    with sync_playwright() as playwright:
        launch = {}
        chromium = find_chromium()
        if chromium:
            launch["executable_path"] = chromium
        browser = playwright.chromium.launch(**launch)
        context = browser.new_context(accept_downloads=True)

        # ---- the sitting -------------------------------------------------
        page = context.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(student_page.resolve().as_uri())
        page.fill('[data-detail="full name"]', "Agnes Nitt")
        page.fill('[data-detail="student number"]', "S12345")
        page.click("#dm-begin")
        page.wait_for_selector("#dm-app:not([hidden])")

        # the calculator panel: buttons, typing, a degree function, and
        # an error message rather than a surprise
        page.click("#dm-calc button[data-insert='(']")
        page.fill("#dm-calc-display", "sind(30) + 2^3 / 4")
        page.click("#dm-calc button[data-action='equals']")
        assert page.text_content("#dm-calc-result").strip() == "= 2.5"
        page.fill("#dm-calc-display", "sqrt(2")
        page.click("#dm-calc button[data-action='equals']")
        assert "bracket" in page.text_content("#dm-calc-result")
        print("calculator: ok")

        # the mathematics in the paper is typeset, not italic dollars
        assert page.locator("#dm-paper math").count() > 0
        print("typeset mathematics: ok")

        page.check('[data-answer="a1.choice"] input[value="2"]')
        page.fill('[data-answer="a2.blanks"] .dm-blank[data-blank="1"]',
                  "premises")
        page.fill('[data-answer="a3.roots"] input[data-box="1"]', "4")
        page.fill('[data-answer="b1.essay"] .dm-essay',
                  "Screens are fine. " * 30)
        page.wait_for_timeout(300)
        assert "dm-answered" in page.get_attribute(
            '[data-answer="a1.choice"]', "class")

        page.click("#dm-finish")
        assert "will count" in page.text_content("#dm-finish-report")
        with page.expect_download() as caught:
            page.click("#dm-submit")
        submission = workdir / caught.value.suggested_filename
        caught.value.save_as(submission)
        archive = zipfile.ZipFile(submission)
        assert sorted(archive.namelist()) == ["answers.json",
                                              "your-exam.html"]
        answers = json.loads(archive.read("answers.json"))
        assert answers["finished_at"]
        readable = archive.read("your-exam.html").decode()
        assert "<script" not in readable.lower()
        print("sitting and submission: ok "
              f"({caught.value.suggested_filename})")

        # ---- restoring ---------------------------------------------------
        # Close the first window before reopening, as a real crash or an
        # accidental close would; a still-open first window would rightly
        # trip the second-window guard.
        page.close()
        again = context.new_page()
        again.on("pageerror", lambda e: errors.append(str(e)))
        again.goto(student_page.resolve().as_uri())
        again.wait_for_selector(".dm-restore-note")
        again.click(".dm-restore-note button")
        again.wait_for_selector("#dm-app:not([hidden])")
        assert again.input_value(
            '[data-answer="a3.roots"] input[data-box="1"]') == "4"
        print("restore after reload: ok")

        # ---- marking -----------------------------------------------------
        bench = context.new_page()
        bench.on("pageerror", lambda e: errors.append(str(e)))
        bench.goto((DEWMARK / "workbench" / "index.html")
                   .resolve().as_uri())
        with bench.expect_file_chooser() as chooser:
            bench.click("#load-scheme")
        chooser.value.set_files(str(scheme_file))
        bench.wait_for_selector("#scheme-pill.ok")
        with bench.expect_file_chooser() as chooser:
            bench.click("#load-subs")
        chooser.value.set_files(str(submission))
        bench.wait_for_selector("#class-table tr.clickable")
        bench.click("#class-table tr.clickable")
        bench.wait_for_selector("#view-paper .marking-row")

        bench.locator("#view-paper .marking-row").first \
            .locator("input[type=number]").fill("2")
        points_row = bench.locator(".marking-row", has_text="a8.spacing")
        points_row.locator("input[type=checkbox]").nth(0).check()
        points_row.locator("input[type=checkbox]").nth(1).check()
        assert points_row.locator("input[type=number]") \
            .input_value() == "4", "ticked points should add to 4"
        essay_row = bench.locator(".marking-row", has_text="b1.essay")
        for index, value in enumerate(["7", "5", "3"]):
            essay_row.locator(".criterion input[type=number]") \
                .nth(index).fill(value)
        bench.wait_for_timeout(200)
        assert "21" in bench.text_content("#view-paper .totals")
        print("marking with all three methods: ok (total 21)")

        downloads = []
        bench.on("download", lambda item: downloads.append(item))
        bench.click("#export-csv")
        bench.wait_for_timeout(800)
        assert len(downloads) == 2
        for item in downloads:
            item.save_as(workdir / item.suggested_filename)
        rows = list(csv.reader(
            open(workdir / "sample-mixed-2027_marks.csv")))
        assert rows[1][0] == "S12345" and rows[1][-2] == "21"
        print("marks export: ok")
        browser.close()

    if errors:
        print("PAGE ERRORS:", errors)
        sys.exit(1)
    print("everything held up; working files in", workdir)


if __name__ == "__main__":
    main()
