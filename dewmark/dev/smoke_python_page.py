#!/usr/bin/env python3
"""A browser rehearsal for Python code questions, end to end.

The script builds the database practical sample, opens it in a headless
browser, waits for the Python system to come up, runs real cells — an
SQLite query, a pandas table, a matplotlib chart, a spreadsheet read —
then finishes the exam, checks the recorded outputs inside the
submission, and opens the marking workbench to confirm a code answer
displays with its output. It is the round trip THE_EXAM_PAGE.md
promises for code questions, run without a person.

Run it by hand:

    python dewmark/dev/smoke_python_page.py

It needs the playwright package and a Chromium browser (found the same
way as smoke_pages.py). The Python system itself is thirty-plus
megabytes, so by default the page downloads it from its network
address; to rehearse the offline exam-room path instead, point
DEWMARK_PYTHON_DIR at an unpacked Pyodide distribution and the script
serves it from a local address, no internet needed for the runtime.
Packages that are not in the distribution (openpyxl, for one) are
still fetched from the package index. If a TLS-intercepting proxy
breaks that fetch, set DEWMARK_INSECURE_CERTS=1 to let the test
browser through it — never set this outside a test harness.
"""

import functools
import http.server
import json
import os
import sys
import tempfile
import threading
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import build_exam  # noqa: E402
from smoke_pages import find_chromium  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("playwright is not installed; see the note at the top of this "
          "script")
    sys.exit(1)

DEWMARK = Path(__file__).parent.parent
SAMPLE = DEWMARK / "samples" / "hvit-database-practical.exam.md"

COUNT_CELL = """\
for table in ["students", "courses", "supervisors", "labs"]:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table}: {cursor.fetchone()[0]} records")
"""
GROUP_CELL = """\
df = pd.read_sql(
    "SELECT programme, COUNT(*) AS count FROM students"
    " GROUP BY programme", conn)
show(df)
"""
CHART_CELL = """\
fig, ax = plt.subplots()
ax.bar(df["programme"], df["count"])
show(fig)
"""
EXCEL_CELL = """\
df_late = pd.read_excel("late_arrivals.xlsx")
print(df_late.shape)
"""


def serve(directory):
    """A throwaway local web server for the built page and, when
    DEWMARK_PYTHON_DIR is set, the Python system beside it."""
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *ignored):
            pass

    handler = functools.partial(QuietHandler, directory=str(directory))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def run_cell(page, answer_name, code, expect_selector):
    cell = page.locator(f'[data-answer="{answer_name}"]')
    cell.locator(".dm-code").fill(code)
    cell.locator(".dm-run").click()
    cell.locator(expect_selector).wait_for(timeout=120_000)
    return cell


def main():
    workdir = Path(tempfile.mkdtemp(prefix="dewmark-pysmoke-"))
    build_exam.build(SAMPLE, workdir)
    python_dir = os.environ.get("DEWMARK_PYTHON_DIR")
    if python_dir:
        (workdir / "pyodide").symlink_to(Path(python_dir).resolve())
    server, base = serve(workdir)
    errors = []

    with sync_playwright() as playwright:
        launch = {}
        chromium = find_chromium()
        if chromium:
            launch["executable_path"] = chromium
        if os.environ.get("DEWMARK_INSECURE_CERTS"):
            launch["args"] = ["--ignore-certificate-errors"]
        browser = playwright.chromium.launch(**launch)
        context = browser.new_context(accept_downloads=True)

        # ---- the sitting -------------------------------------------------
        page = context.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))
        if python_dir:
            page.add_init_script(
                f"window.DEWMARK_PYTHON_BASE = '{base}/pyodide/'")
        page.goto(base + "/hvit-registry-2026.student.html")
        page.fill('[data-detail="full name"]', "Agnes Nitt")
        page.fill('[data-detail="student number"]', "S12345")
        page.click("#dm-begin")
        page.wait_for_selector("#dm-app:not([hidden])")

        page.wait_for_function(
            "document.getElementById('dm-python-status').textContent"
            " === 'Python ready'", timeout=240_000)
        print("python system: ready")

        cell = run_cell(page, "task1.counts", COUNT_CELL, ".dm-out-text")
        assert "students: 20 records" in cell.locator(
            ".dm-out-text").inner_text()
        print("sqlite query: ok")

        cell = run_cell(page, "task4.groupby", GROUP_CELL, ".dm-out-table")
        assert cell.locator(".dm-out-table tr").count() == 6, \
            "five programmes plus a header row"
        print("pandas table: ok")

        run_cell(page, "task4.chart", CHART_CELL, ".dm-out-image")
        print("matplotlib picture: ok")

        cell = run_cell(page, "task5.load", EXCEL_CELL, ".dm-out-text")
        assert "(5, 5)" in cell.locator(".dm-out-text").inner_text()
        print("spreadsheet read: ok")

        # editing after a run must flag the recorded output as stale
        page.fill('[data-answer="task5.load"] .dm-code', EXCEL_CELL + "#")
        page.wait_for_timeout(400)
        note = page.locator('[data-answer="task5.load"] .dm-code-note')
        assert "earlier version" in note.inner_text()
        print("stale-output note: ok")

        # ---- the submission ----------------------------------------------
        page.click("#dm-finish")
        with page.expect_download() as caught:
            page.click("#dm-submit")
        submission = workdir / caught.value.suggested_filename
        caught.value.save_as(submission)
        answers = json.loads(zipfile.ZipFile(submission)
                             .read("answers.json"))["answers"]
        counts = answers["task1.counts"]
        assert counts["code"].strip() == COUNT_CELL.strip()
        assert counts["run_matches_code"] is True
        assert any(record["kind"] == "stdout"
                   for record in counts["outputs"])
        assert answers["task5.load"]["run_matches_code"] is False
        kinds = {record["kind"]
                 for value in answers.values() if isinstance(value, dict)
                 for record in value.get("outputs", [])}
        assert {"stdout", "table", "image"} <= kinds, kinds
        print("submission records code, text, tables, and pictures: ok")

        # ---- the workbench -----------------------------------------------
        bench = context.new_page()
        bench.on("pageerror", lambda e: errors.append(str(e)))
        bench.goto((DEWMARK / "workbench" / "index.html")
                   .resolve().as_uri())
        with bench.expect_file_chooser() as chooser:
            bench.click("#load-scheme")
        chooser.value.set_files(
            str(workdir / "dewmark_hvit-registry-2026_marking_scheme.json"))
        bench.wait_for_selector("#scheme-pill.ok")
        with bench.expect_file_chooser() as chooser:
            bench.click("#load-subs")
        chooser.value.set_files(str(submission))
        bench.wait_for_selector("#class-table tr.clickable")
        bench.click("#class-table tr.clickable")
        bench.wait_for_selector("#view-paper .marking-row")

        row = bench.locator(".marking-row", has_text="task1.counts")
        assert "SELECT COUNT" in row.locator(".code-block").first \
            .inner_text()
        assert "students: 20 records" in row.locator(".run-output").first \
            .inner_text()
        stale = bench.locator(".marking-row", has_text="task5.load")
        assert stale.locator(".stale-run").count() == 1
        print("workbench shows code, output, and the stale warning: ok")
        browser.close()

    server.shutdown()
    if errors:
        print("PAGE ERRORS:", errors)
        sys.exit(1)
    print(f"everything held up; working files in {workdir}")


if __name__ == "__main__":
    main()
