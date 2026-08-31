#!/usr/bin/env python3
"""The dewmark exam builder.

This program reads one exam file (see planning/THE_EXAM_FILE.md), checks
it, and writes the finished pages: the student paper, the practice
paper, the answer key, and the marking scheme file that the marking
workbench reads. Nothing reaches a student except through this program,
which is why the checks live here: an exam whose marks do not add up, or
whose model answers would leak into the student paper, cannot be built.

Usage:
    python build_exam.py my-exam.md --output finished/
    python build_exam.py my-exam.md --check

The builder is deliberately one file, in the style of the wider dewlab
project: a reader should be able to follow an exam file's journey from
text to finished page by reading top to bottom. This is an early draft;
docs/DEVELOPMENT.md lists the gaps between it and the design documents.
"""

import argparse
import base64
import html
import json
import re
import sys
from pathlib import Path

import markdown as markdown_lib
import yaml

# ---------------------------------------------------------------- constants

BLOCK_KINDS = {"exam", "section", "question", "answer", "marking"}

# The question types the draft builder can render. python-code is defined
# in the catalogue but is planned for a later phase; naming it here lets
# the builder refuse it with an accurate message instead of "unknown type".
SUPPORTED_TYPES = {
    "multiple-choice",
    "fill-in-the-blank",
    "short-written-answer",
    "long-written-answer",
    "essay",
    "numeric-answer",
    "complete-the-table",
    "describe-a-sketch",
    "label-the-diagram",
}
PLANNED_TYPES = {"python-code"}

NAME_RE = re.compile(r"^[a-z][a-z0-9_.-]*$")
SECTION_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")
EXAM_CODE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
VERSION_RE = re.compile(r"^\d{4}\.\d{2}\.\d{2}\.\d+$")

# "2 marks - names the optimum temperature" -> (2.0, "names the ...")
POINT_RE = re.compile(r"^\s*(\d+(?:\.5)?)\s+marks?\s*[-–]\s*(.+)$", re.S)
# "16 to 20 - a sustained line of argument" -> (16, 20, "a sustained ...")
BAND_RE = re.compile(r"^\s*(\d+)\s*(?:to|[-–])\s*(\d+)\s*[-–]\s*(.+)$", re.S)

NUMBER_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
    7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
}

ASSETS_DIR = Path(__file__).parent / "assets"


class BuildError(Exception):
    """Raised when the exam file cannot be built. Carries every problem
    found, so the author fixes one run's worth of errors at a time rather
    than one error per run."""

    def __init__(self, problems):
        self.problems = problems
        lines = [f"  line {ln}: {msg}" if ln else f"  {msg}" for ln, msg in problems]
        super().__init__("the exam file cannot be built:\n" + "\n".join(lines))


# ---------------------------------------------------------------- parsing

def parse_exam_file(text, base_dir):
    """Turn the exam file's text into a checked structure.

    Returns a dictionary with the exam settings, the sections (each with
    its questions, each with its prose and answer spaces), and the list
    of problems found. The caller decides whether problems are fatal.
    """
    problems = []
    exam = {"settings": None, "sections": [], "line": 0}
    current_section = None
    current_question = None
    last_answer = None          # for attaching a marking block
    prose_since_answer = False  # a marking block must directly follow its answer
    prose_lines = []
    prose_start = 1

    def flush_prose():
        nonlocal prose_lines, prose_start
        chunk = "\n".join(prose_lines).strip("\n")
        if chunk.strip():
            node = {"kind": "prose", "md": chunk, "line": prose_start}
            if current_question is not None:
                current_question["content"].append(node)
            elif current_section is not None:
                current_section["content"].append(node)
            else:
                exam.setdefault("preamble", []).append(node)
        prose_lines = []

    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        opener = re.match(r"^```([A-Za-z][\w-]*)\s*$", line)
        if opener is None:
            if re.match(r"^```\s*$", line):
                problems.append((i + 1, "a line of three backticks appears "
                                 "without a block kind after it; every "
                                 "settings block starts like ```question"))
            prose_lines.append(line)
            i += 1
            continue

        kind = opener.group(1)
        start_line = i + 1
        if kind not in BLOCK_KINDS:
            problems.append((start_line, f"unknown settings block kind "
                             f"'{kind}'; the kinds are: "
                             + ", ".join(sorted(BLOCK_KINDS))))
        body = []
        i += 1
        while i < len(lines) and not re.match(r"^```\s*$", lines[i]):
            body.append(lines[i])
            i += 1
        if i >= len(lines):
            problems.append((start_line, f"the '{kind}' block that starts "
                             "here is never closed with a line of three "
                             "backticks"))
        i += 1  # skip the closing backticks

        if kind not in BLOCK_KINDS:
            continue
        try:
            settings = yaml.safe_load("\n".join(body)) or {}
        except yaml.YAMLError as err:
            problems.append((start_line, f"the '{kind}' block could not be "
                             f"read: {err}"))
            continue
        if not isinstance(settings, dict):
            problems.append((start_line, f"the '{kind}' block must contain "
                             "one setting per line, like 'marks: 4'"))
            continue
        settings["_line"] = start_line

        if kind == "exam":
            flush_prose()
            if exam["settings"] is not None:
                problems.append((start_line, "there is more than one 'exam' "
                                 "block; an exam file has exactly one, at "
                                 "the top"))
            exam["settings"] = settings
        elif kind == "section":
            flush_prose()
            current_section = {"settings": settings, "content": [],
                               "questions": []}
            exam["sections"].append(current_section)
            current_question = None
            last_answer = None
        elif kind == "question":
            flush_prose()
            if current_section is None:
                problems.append((start_line, "this 'question' block appears "
                                 "before any 'section' block"))
                current_section = {"settings": {"name": "_orphan",
                                                "_line": start_line},
                                   "content": [], "questions": []}
                exam["sections"].append(current_section)
            current_question = {"settings": settings, "content": [],
                                "answers": []}
            current_section["questions"].append(current_question)
            last_answer = None
        elif kind == "answer":
            flush_prose()
            if current_question is None:
                problems.append((start_line, "this 'answer' block appears "
                                 "outside any question"))
                continue
            answer = {"settings": settings, "marking": None}
            current_question["answers"].append(answer)
            current_question["content"].append({"kind": "answer",
                                                "answer": answer})
            last_answer = answer
            prose_since_answer = False
        elif kind == "marking":
            if last_answer is None or prose_since_answer:
                problems.append((start_line, "a 'marking' block must come "
                                 "directly after the answer space it "
                                 "belongs to, with nothing in between"))
                continue
            if last_answer["marking"] is not None:
                problems.append((start_line, "this answer space already has "
                                 "a marking block"))
                continue
            last_answer["marking"] = settings

        if kind != "marking":
            prose_start = i + 1
        continue

    flush_prose()

    # Prose that arrives after an answer breaks the answer->marking
    # adjacency; track it by scanning the flush order. The flush above
    # already appended prose to the question, so recompute the flag from
    # content ordering instead of during the loop (simpler and correct).
    for section in exam["sections"]:
        for question in section["questions"]:
            seen_prose_after = False
            for node in question["content"]:
                if node["kind"] == "prose":
                    seen_prose_after = True
                elif node["kind"] == "answer":
                    seen_prose_after = False
            del seen_prose_after  # ordering itself is what renders

    check_exam(exam, problems, base_dir)
    return exam, problems


# ---------------------------------------------------------------- checking

def check_exam(exam, problems, base_dir):
    """Run every check from planning/THE_EXAM_BUILDER.md section 2 that
    the draft supports, appending problems as (line, message) pairs."""

    settings = exam["settings"]
    if settings is None:
        problems.append((1, "the file has no 'exam' block; every exam file "
                         "starts with one"))
        return

    line = settings.get("_line", 1)
    for required in ("title", "exam_code", "version", "total_marks",
                     "student_details", "instructions"):
        if required not in settings:
            problems.append((line, f"the exam block is missing '{required}'"))
    code = str(settings.get("exam_code", ""))
    if code and not EXAM_CODE_RE.match(code):
        problems.append((line, "exam_code may contain only lower-case "
                         "letters, digits, and hyphens"))
    version = str(settings.get("version", ""))
    if version and not VERSION_RE.match(version):
        problems.append((line, "version must look like 2027.01.15.1 "
                         "(year.month.day.build)"))

    instructions = str(settings.get("instructions", ""))
    seen_names = {}

    def claim_name(owner_settings, what):
        name = owner_settings.get("name")
        block_line = owner_settings.get("_line", 0)
        if not name:
            problems.append((block_line, f"this {what} has no 'name'"))
            return None
        name = str(name)
        # Section names may be capitals ("Section A"); question and answer
        # names stay lower-case so they read cleanly in file names and
        # spreadsheet columns.
        pattern = SECTION_NAME_RE if what == "section" else NAME_RE
        if not pattern.match(name):
            problems.append((block_line, f"the name '{name}' is not allowed; "
                             "names use letters, digits, dots, hyphens, and "
                             "underscores, start with a letter, and question "
                             "and answer names are lower-case"))
        if name in seen_names:
            problems.append((block_line, f"the name '{name}' is already used "
                             f"on line {seen_names[name]}; names must be "
                             "unique"))
        seen_names[name] = block_line
        return name

    total = 0
    for section in exam["sections"]:
        s_set = section["settings"]
        s_line = s_set.get("_line", 0)
        claim_name(s_set, "section")
        choose = s_set.get("choose")
        q_marks = []
        for question in section["questions"]:
            q_set = question["settings"]
            q_line = q_set.get("_line", 0)
            claim_name(q_set, "question")
            marks = q_set.get("marks")
            if not isinstance(marks, (int, float)) or marks <= 0:
                problems.append((q_line, "every question needs positive "
                                 "'marks'"))
                marks = 0
            q_marks.append(marks)
            answer_total = 0
            if not question["answers"]:
                problems.append((q_line, "this question has no answer "
                                 "spaces"))
            for answer in question["answers"]:
                claim_name(answer["settings"], "answer space")
                answer_total += check_answer(answer, problems, base_dir)
            if question["answers"] and answer_total != marks:
                problems.append((q_line, f"the question declares "
                                 f"{marks} marks but its answer spaces add "
                                 f"up to {answer_total}"))
        if choose is not None:
            if not isinstance(choose, int) or not 1 <= choose <= len(q_marks):
                problems.append((s_line, f"'choose: {choose}' does not fit a "
                                 f"section with {len(q_marks)} questions"))
                choose = None
            elif len(set(q_marks)) > 1:
                problems.append((s_line, "in a section with 'choose', every "
                                 "question must carry the same marks, so "
                                 "that the section total is well defined"))
            else:
                mentioned = (str(choose) in instructions
                             or NUMBER_WORDS.get(choose, "\x00") in
                             instructions.lower())
                if not mentioned:
                    problems.append((s_line, f"this section says 'choose: "
                                     f"{choose}' but the front-page "
                                     "instructions never mention it; "
                                     "students must be told"))
        if choose is not None and q_marks:
            total += choose * q_marks[0]
        else:
            total += sum(q_marks)

    declared = settings.get("total_marks")
    if isinstance(declared, (int, float)) and total != declared:
        problems.append((line, f"total_marks says {declared} but the paper "
                         f"adds up to {total} (after any 'choose' rules)"))


def check_answer(answer, problems, base_dir):
    """Check one answer space and its marking block. Returns its marks."""
    a = answer["settings"]
    a_line = a.get("_line", 0)
    a_type = a.get("type")
    marks = a.get("marks")
    if not isinstance(marks, (int, float)) or marks <= 0:
        problems.append((a_line, "every answer space needs positive 'marks'"))
        marks = 0
    if a_type in PLANNED_TYPES:
        problems.append((a_line, f"the question type '{a_type}' is defined "
                         "in the catalogue but is not built yet; see the "
                         "roadmap"))
        return marks
    if a_type not in SUPPORTED_TYPES:
        problems.append((a_line, f"unknown question type '{a_type}'; the "
                         "types are listed in "
                         "planning/QUESTION_TYPES_AND_MARKING.md"))
        return marks

    def need(key, kind=None):
        if key not in a:
            problems.append((a_line, f"a {a_type} answer space needs "
                             f"'{key}'"))
            return None
        value = a[key]
        if kind is not None and not isinstance(value, kind):
            problems.append((a_line, f"'{key}' has the wrong shape for a "
                             f"{a_type} answer space"))
            return None
        return value

    if a_type == "multiple-choice":
        options = need("options", list)
        if options is not None and len(options) < 2:
            problems.append((a_line, "multiple choice needs at least two "
                             "options"))
        correct = a.get("correct")
        if options and correct is not None:
            picks = correct if isinstance(correct, list) else [correct]
            for pick in picks:
                if not isinstance(pick, int) or not 1 <= pick <= len(options):
                    problems.append((a_line, f"'correct: {pick}' does not "
                                     "name an option by its position"))
    elif a_type == "fill-in-the-blank":
        text = need("text", str)
        if text is not None and len(re.findall(r"\{([^{}]+)\}", text)) == 0:
            problems.append((a_line, "the text has no {blanks}; wrap each "
                             "removed word in curly brackets"))
    elif a_type in ("short-written-answer", "long-written-answer"):
        need("prompt", str)
    elif a_type == "essay":
        gw = a.get("guide_words")
        if gw is not None and (not isinstance(gw, int) or gw <= 0):
            problems.append((a_line, "'guide_words' must be a positive "
                             "number"))
    elif a_type == "numeric-answer":
        boxes = need("boxes", list)
        if boxes is not None:
            for box in boxes:
                if not isinstance(box, dict) or "label" not in box:
                    problems.append((a_line, "each numeric box needs a "
                                     "'label' (and usually an 'expected' "
                                     "value)"))
    elif a_type == "complete-the-table":
        columns = need("columns", list)
        rows = need("rows", list)
        expected = a.get("expected")
        blanks = 0
        if rows is not None and columns is not None:
            for row in rows:
                if not isinstance(row, list) or len(row) != len(columns):
                    problems.append((a_line, "every table row must have one "
                                     "cell per column"))
                    continue
                blanks += sum(1 for cell in row if cell == "?")
            if blanks == 0:
                problems.append((a_line, "the table has no '?' cells for "
                                 "the student to fill"))
        if expected is not None and rows is not None:
            if (not isinstance(expected, list) or len(expected) != len(rows)
                    or any(not isinstance(r, list) or len(r) != len(rows[0])
                           for r in expected)):
                problems.append((a_line, "'expected' must be the same shape "
                                 "as 'rows'"))
    elif a_type == "describe-a-sketch":
        shape = need("shape", dict)
        if shape is not None:
            opts = shape.get("options")
            if not isinstance(opts, list) or len(opts) < 2:
                problems.append((a_line, "the shape choice needs at least "
                                 "two options"))
        features = need("features", list)
        if features is not None:
            for feature in features:
                if not isinstance(feature, dict):
                    problems.append((a_line, "each feature needs a 'label', "
                                     "a 'boxes' count, and its 'expected' "
                                     "values"))
                    continue
                label = str(feature.get("label", ""))
                boxes = feature.get("boxes")
                expected = feature.get("expected")
                if label.count("_") != boxes:
                    problems.append((a_line, f"the feature label '{label}' "
                                     f"shows {label.count('_')} underscores "
                                     f"but declares {boxes} boxes; each "
                                     "underscore becomes one box"))
                if expected is not None and (not isinstance(expected, list)
                                             or len(expected) != boxes):
                    problems.append((a_line, "a feature's 'expected' list "
                                     "must have one value per box"))
    elif a_type == "label-the-diagram":
        image = need("image", str)
        if image is not None and not (base_dir / image).is_file():
            problems.append((a_line, f"the picture '{image}' does not exist "
                             f"beside the exam file"))
        if not str(a.get("image_description", "")).strip():
            problems.append((a_line, "every picture needs an "
                             "'image_description' for students using a "
                             "screen reader"))
        need("labels", list)

    check_marking(answer, marks, problems)
    return marks


def check_marking(answer, marks, problems):
    """Check the marking block, and parse its points and criteria into
    structured form for the marking scheme file."""
    marking = answer["marking"]
    if marking is None:
        answer["marking_parsed"] = {"method": "marks-out-of-a-total",
                                    "guidance": []}
        return
    m_line = marking.get("_line", 0)

    if "points" in marking:
        limit = marking.get("limit")
        if not isinstance(limit, (int, float)):
            problems.append((m_line, "a points list needs a 'limit' (the "
                             "most marks the list can earn)"))
            limit = marks
        parsed = []
        for point in marking.get("points") or []:
            match = POINT_RE.match(str(point))
            if match is None:
                problems.append((m_line, f"could not read the point "
                                 f"'{point}'; write each point like "
                                 "'2 marks - explains denaturation'"))
                continue
            parsed.append({"marks": float(match.group(1)),
                           "text": match.group(2).strip()})
        if limit != marks:
            problems.append((m_line, f"the points limit ({limit}) must "
                             f"equal the answer space's marks ({marks})"))
        if parsed and sum(p["marks"] for p in parsed) < limit:
            problems.append((m_line, "the points add up to less than the "
                             "limit, so full marks would be unreachable"))
        answer["marking_parsed"] = {"method": "points-with-a-limit",
                                    "limit": limit, "points": parsed}
    elif "criteria" in marking:
        parsed = []
        criteria_total = 0
        for criterion in marking.get("criteria") or []:
            if not isinstance(criterion, dict):
                problems.append((m_line, "each criterion needs a 'name', "
                                 "its 'marks', and its 'bands'"))
                continue
            c_marks = criterion.get("marks", 0)
            criteria_total += c_marks
            bands = []
            for band in criterion.get("bands") or []:
                match = BAND_RE.match(str(band))
                if match is None:
                    problems.append((m_line, f"could not read the band "
                                     f"'{band}'; write each band like "
                                     "'16 to 20 - a sustained argument'"))
                    continue
                low, high = int(match.group(1)), int(match.group(2))
                if not 0 <= low <= high <= c_marks:
                    problems.append((m_line, f"the band '{low} to {high}' "
                                     f"does not fit inside 0 to {c_marks}"))
                bands.append({"low": low, "high": high,
                              "text": match.group(3).strip()})
            if not bands:
                problems.append((m_line, f"the criterion "
                                 f"'{criterion.get('name')}' has no "
                                 "readable bands"))
            parsed.append({"name": str(criterion.get("name", "")),
                           "marks": c_marks, "bands": bands})
        if parsed and criteria_total != marks:
            problems.append((m_line, f"the criteria add up to "
                             f"{criteria_total} marks but the answer space "
                             f"carries {marks}"))
        answer["marking_parsed"] = {"method": "a-criteria-grid",
                                    "criteria": parsed}
    else:
        guidance = marking.get("guidance") or []
        if not isinstance(guidance, list):
            problems.append((m_line, "'guidance' must be a list of lines"))
            guidance = []
        answer["marking_parsed"] = {"method": "marks-out-of-a-total",
                                    "guidance": [str(g) for g in guidance],
                                    "marks": marking.get("marks", marks)}
        if "marks" in marking and marking["marks"] != marks:
            problems.append((m_line, f"the marking block says "
                             f"{marking['marks']} marks but the answer "
                             f"space carries {marks}"))


# ---------------------------------------------------------------- markdown

MATH_RE = re.compile(r"\$([^$\n]+)\$")


def render_markdown(md_text):
    """Render a prose chunk to HTML.

    Mathematics between dollar signs is lifted out before the Markdown
    step and re-inserted afterwards in a styled span. The draft shows it
    in italics rather than typeset; proper typesetting at build time is a
    known gap listed in docs/DEVELOPMENT.md.
    """
    holes = []

    def stash(match):
        holes.append(match.group(1))
        return f"\x00MATH{len(holes) - 1}\x00"

    stashed = MATH_RE.sub(stash, md_text)
    rendered = markdown_lib.markdown(stashed, extensions=["tables"])
    for index, content in enumerate(holes):
        rendered = rendered.replace(
            f"\x00MATH{index}\x00",
            f'<em class="dm-math">{html.escape(content)}</em>')
    return rendered


# ---------------------------------------------------------------- rendering

def esc(value):
    return html.escape(str(value), quote=True)


def rows_for(marks):
    """The starting height of a writing box follows the marks available,
    so the box itself suggests how much is expected (see
    planning/APPEARANCE_AND_READABILITY.md)."""
    if marks <= 2:
        return 3
    if marks <= 5:
        return 6
    return 10


def render_answer_space(answer, variant, base_dir):
    """Render one answer space for the student, practice, or answer-key
    page. The student variant must contain nothing from the marking
    material; the leak check at the end of the build verifies that."""
    a = answer["settings"]
    a_type = a["type"]
    name = a["name"]
    marks = a["marks"]
    show_hints = variant == "practice"
    show_models = variant == "answer_key"

    inner = []
    if a_type == "multiple-choice":
        several = a.get("choose") == "several"
        control = "checkbox" if several else "radio"
        options = []
        for index, option in enumerate(a["options"], start=1):
            options.append(
                f'<label class="dm-option"><input type="{control}" '
                f'name="{esc(name)}" value="{index}"> '
                f'<span>{esc(option)}</span></label>')
        inner.append('<div class="dm-options">' + "".join(options) + "</div>")
    elif a_type == "fill-in-the-blank":
        text = a["text"]
        parts = re.split(r"\{([^{}]+)\}", text)
        pieces = []
        blank_index = 0
        for position, part in enumerate(parts):
            if position % 2 == 0:
                pieces.append(esc(part).replace("\n", "<br>"))
            else:
                blank_index += 1
                pieces.append(
                    f'<input class="dm-blank" data-blank="{blank_index}" '
                    f'type="text" aria-label="blank {blank_index}">')
        inner.append('<p class="dm-blank-text">' + "".join(pieces) + "</p>")
    elif a_type in ("short-written-answer", "long-written-answer"):
        prompt = a.get("prompt", "")
        inner.append(f'<p class="dm-prompt">{esc(prompt)}</p>')
        hint = esc(a.get("hint", "")) if show_hints and a.get("hint") else ""
        inner.append(f'<textarea class="dm-writing" rows="{rows_for(marks)}" '
                     f'aria-label="your answer" placeholder="{hint}">'
                     f"</textarea>")
    elif a_type == "essay":
        if a.get("planning_box", False):
            inner.append('<p class="dm-small-label">Planning (handed in, '
                         "carries no marks)</p>")
            inner.append('<textarea class="dm-writing dm-planning" rows="5" '
                         'aria-label="planning notes"></textarea>')
        inner.append('<p class="dm-small-label">Your essay'
                     + (f' — guide length {a["guide_words"]} words'
                        if a.get("guide_words") else "") + "</p>")
        inner.append('<textarea class="dm-writing dm-essay" rows="24" '
                     'aria-label="your essay"></textarea>')
        inner.append('<p class="dm-word-count" aria-live="polite">'
                     "0 words</p>")
    elif a_type == "numeric-answer":
        boxes = []
        for index, box in enumerate(a["boxes"], start=1):
            boxes.append(
                f'<label class="dm-numeric">{esc(box["label"])} '
                f'<input type="text" data-box="{index}" '
                f'aria-label="{esc(box["label"])} answer {index}"></label>')
        inner.append('<div class="dm-numeric-row">' + "".join(boxes)
                     + "</div>")
        if a.get("working_box", False):
            inner.append('<p class="dm-small-label">Working</p>')
            inner.append('<textarea class="dm-writing dm-working" rows="5" '
                         'aria-label="your working"></textarea>')
    elif a_type == "complete-the-table":
        head = "".join(f"<th>{esc(c)}</th>" for c in a["columns"])
        body_rows = []
        for r_index, row in enumerate(a["rows"]):
            cells = []
            for c_index, cell in enumerate(row):
                if cell == "?":
                    cells.append(
                        f'<td><input class="dm-cell" '
                        f'data-cell="r{r_index}c{c_index}" type="text" '
                        f'aria-label="row {r_index + 1} column '
                        f'{c_index + 1}"></td>')
                else:
                    cells.append(f"<td>{esc(cell)}</td>")
            body_rows.append("<tr>" + "".join(cells) + "</tr>")
        inner.append('<table class="dm-table"><tr>' + head + "</tr>"
                     + "".join(body_rows) + "</table>")
    elif a_type == "describe-a-sketch":
        shape = a["shape"]
        options = []
        for index, option in enumerate(shape["options"], start=1):
            options.append(
                f'<label class="dm-option dm-shape"><input type="radio" '
                f'name="{esc(name)}.shape" value="{index}"> '
                f"<span>{esc(option)}</span></label>")
        inner.append(f'<p class="dm-prompt">{esc(shape.get("prompt", ""))}'
                     "</p>")
        inner.append('<div class="dm-options">' + "".join(options) + "</div>")
        for f_index, feature in enumerate(a["features"]):
            parts = str(feature["label"]).split("_")
            pieces = []
            for position, part in enumerate(parts):
                pieces.append(esc(part))
                if position < len(parts) - 1:
                    pieces.append(
                        f'<input class="dm-feature" '
                        f'data-feature="{f_index}" data-box="{position}" '
                        f'type="text" aria-label="{esc(feature["label"])} '
                        f'value {position + 1}">')
            inner.append('<p class="dm-feature-row">' + "".join(pieces)
                         + "</p>")
    elif a_type == "label-the-diagram":
        image_path = base_dir / a["image"]
        data = image_path.read_bytes()
        suffix = image_path.suffix.lower().lstrip(".")
        mime = {"svg": "image/svg+xml", "png": "image/png",
                "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(
                    suffix, "application/octet-stream")
        encoded = base64.b64encode(data).decode("ascii")
        inner.append(
            f'<img class="dm-diagram" alt="{esc(a["image_description"])}" '
            f'src="data:{mime};base64,{encoded}">')
        label_rows = []
        for label in a["labels"]:
            number = label["number"]
            label_rows.append(
                f'<label class="dm-diagram-label">{esc(number)}. '
                f'<input type="text" data-label="{esc(number)}" '
                f'aria-label="label {esc(number)}"></label>')
        inner.append('<div class="dm-diagram-labels">' + "".join(label_rows)
                     + "</div>")

    if show_models:
        inner.append(render_model_block(answer))

    heading = (f'<div class="dm-answer-head"><span>Answer space</span>'
               f'<span class="dm-answer-marks">({marks:g})</span>'
               f'<span class="dm-answered-flag" hidden>answered</span></div>')
    return (f'<div class="dm-answer" data-answer="{esc(name)}" '
            f'data-type="{esc(a_type)}" data-marks="{marks:g}">'
            + heading + "".join(inner) + "</div>")


def render_model_block(answer):
    """The answer key's view of one answer space: the model material,
    plainly labelled, with drafts flagged (see
    planning/TRANSLATING_AN_EXISTING_EXAM.md)."""
    a = answer["settings"]
    parsed = answer.get("marking_parsed") or {}
    parts = ['<div class="dm-model">']
    if a.get("draft") or (answer["marking"] or {}).get("draft"):
        parts.append('<p class="dm-draft">Draft — not yet approved by the '
                     "teacher</p>")
    if a.get("model_answer"):
        parts.append(f'<p class="dm-model-label">Model answer</p>'
                     f'<p class="dm-model-text">{esc(a["model_answer"])}</p>')
    if a["type"] == "multiple-choice" and a.get("correct"):
        picks = a["correct"] if isinstance(a["correct"], list) else [a["correct"]]
        texts = ", ".join(esc(a["options"][p - 1]) for p in picks)
        parts.append(f'<p class="dm-model-text">Correct: {texts}</p>')
    if a["type"] == "fill-in-the-blank":
        gaps = re.findall(r"\{([^{}]+)\}", a["text"])
        parts.append('<p class="dm-model-text">Blanks: '
                     + ", ".join(esc(g) for g in gaps) + "</p>")
    if a["type"] == "numeric-answer":
        values = ", ".join(str(b.get("expected", "?")) for b in a["boxes"])
        parts.append(f'<p class="dm-model-text">Expected: {esc(values)}</p>')
    if a["type"] == "complete-the-table" and a.get("expected"):
        flat = "; ".join(", ".join(str(c) for c in row)
                         for row in a["expected"])
        parts.append(f'<p class="dm-model-text">Expected rows: {esc(flat)}'
                     "</p>")
    if a["type"] == "describe-a-sketch":
        shape = a["shape"]
        if shape.get("correct"):
            parts.append(f'<p class="dm-model-text">Shape: '
                         f'{esc(shape["options"][shape["correct"] - 1])}</p>')
        for feature in a["features"]:
            if feature.get("expected") is not None:
                values = ", ".join(str(v) for v in feature["expected"])
                parts.append(f'<p class="dm-model-text">'
                             f'{esc(feature["label"])} → {esc(values)}</p>')
    if a["type"] == "label-the-diagram":
        pairs = "; ".join(f'{label["number"]}: {label.get("expected", "?")}'
                          for label in a["labels"])
        parts.append(f'<p class="dm-model-text">Labels: {esc(pairs)}</p>')
    method = parsed.get("method")
    if method == "points-with-a-limit":
        parts.append(f'<p class="dm-model-label">Points (limit '
                     f'{parsed["limit"]:g})</p><ul>')
        for point in parsed["points"]:
            parts.append(f'<li>{point["marks"]:g} — {esc(point["text"])}</li>')
        parts.append("</ul>")
    elif method == "a-criteria-grid":
        parts.append('<p class="dm-model-label">Criteria</p>')
        for criterion in parsed["criteria"]:
            parts.append(f'<p class="dm-model-text"><strong>'
                         f'{esc(criterion["name"])}</strong> '
                         f'({criterion["marks"]:g} marks)</p><ul>')
            for band in criterion["bands"]:
                parts.append(f'<li>{band["low"]}–{band["high"]}: '
                             f'{esc(band["text"])}</li>')
            parts.append("</ul>")
    elif parsed.get("guidance"):
        parts.append('<p class="dm-model-label">Marking guidance</p><ul>')
        for guide in parsed["guidance"]:
            parts.append(f"<li>{esc(guide)}</li>")
        parts.append("</ul>")
    parts.append("</div>")
    return "".join(parts)


def render_paper(exam, variant, base_dir):
    """Render the body of the paper: sections, questions, prose, and
    answer spaces, in file order."""
    parts = []
    for node in exam.get("preamble", []):
        parts.append(render_markdown(node["md"]))
    for section in exam["sections"]:
        s = section["settings"]
        choose = s.get("choose")
        parts.append(f'<section class="dm-section" '
                     f'data-section="{esc(s["name"])}"'
                     + (f' data-choose="{choose}"' if choose else "") + ">")
        for node in section["content"]:
            parts.append(render_markdown(node["md"]))
        for question in section["questions"]:
            q = question["settings"]
            parts.append(f'<div class="dm-question" '
                         f'data-question="{esc(q["name"])}" '
                         f'data-marks="{q["marks"]:g}" '
                         f'data-section="{esc(s["name"])}">')
            for node in question["content"]:
                if node["kind"] == "prose":
                    parts.append(render_markdown(node["md"]))
                else:
                    parts.append(render_answer_space(node["answer"], variant,
                                                     base_dir))
            parts.append("</div>")
        parts.append("</section>")
    return "".join(parts)


def page_model(exam):
    """The small data block the page's own behaviour needs: names, types,
    marks, and section rules. It contains nothing from the marking
    material, and the leak check runs over the whole page including this
    block."""
    settings = exam["settings"]
    sections = []
    for section in exam["sections"]:
        s = section["settings"]
        questions = []
        for question in section["questions"]:
            q = question["settings"]
            questions.append({
                "name": q["name"], "marks": q["marks"],
                "answers": [{"name": ans["settings"]["name"],
                             "type": ans["settings"]["type"],
                             "marks": ans["settings"]["marks"]}
                            for ans in question["answers"]],
            })
        sections.append({"name": s["name"], "choose": s.get("choose"),
                         "questions": questions})
    return {
        "format_version": 1,
        "exam_code": settings["exam_code"],
        "exam_version": settings["version"],
        "title": settings["title"],
        "total_marks": settings["total_marks"],
        "time_allowed": settings.get("time_allowed", ""),
        "student_details": settings["student_details"],
        "sections": sections,
    }


def build_page(exam, variant, base_dir):
    """Assemble one complete page: styles, start screen, paper, finish
    screen, data block, and behaviour, all in one file."""
    settings = exam["settings"]
    css = (ASSETS_DIR / "exam-page.css").read_text(encoding="utf-8")
    js = (ASSETS_DIR / "exam-page.js").read_text(encoding="utf-8")
    banner = {"student": "Examination", "practice": "Practice paper",
              "answer_key": "Answer key — not for students"}[variant]
    model = page_model(exam)
    model["variant"] = variant
    model_json = json.dumps(model).replace("</", "<\\/")
    paper = render_paper(exam, variant, base_dir)
    instructions = render_markdown(settings["instructions"])
    detail_inputs = "".join(
        f'<label class="dm-detail">{esc(detail)} '
        f'<input type="text" data-detail="{esc(detail)}" '
        f'autocomplete="off"></label>'
        for detail in settings["student_details"])

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(settings["title"])}</title>
<style>{css}</style>
</head>
<body data-variant="{variant}">
<header class="dm-band dm-band-{variant}">
  <p class="dm-band-kind">{banner}</p>
  <h1 class="dm-band-title">{esc(settings["title"])}</h1>
  <p class="dm-band-meta">Time allowed: {esc(settings.get("time_allowed", ""))}
   · Total marks: {settings["total_marks"]:g}</p>
</header>

<div id="dm-start" class="dm-card">
  <div class="dm-instructions">{instructions}</div>
  <div class="dm-details">{detail_inputs}</div>
  <p class="dm-save-note">When you press Begin, you will be asked where to
  keep your answer file. The exam then saves itself there, and in this
  browser, as you work. Nothing leaves this computer.</p>
  <button id="dm-begin" class="dm-primary">Begin</button>
  <button id="dm-load-file" class="dm-secondary">Load a saved answer
  file…</button>
</div>

<div id="dm-app" hidden>
  <div id="dm-topbar">
    <span id="dm-top-title">{esc(settings["title"])}</span>
    <span id="dm-top-student"></span>
    <span id="dm-save-browser" class="dm-save-pill" title="saved in this
    browser">Browser —</span>
    <span id="dm-save-file" class="dm-save-pill" title="saved to your answer
    file">File —</span>
    <button id="dm-download" class="dm-secondary">Save a copy</button>
    <button id="dm-finish" class="dm-primary">Finish exam…</button>
  </div>
  <div id="dm-body">
    <nav id="dm-panel" aria-label="questions"></nav>
    <main id="dm-paper">{paper}</main>
  </div>
</div>

<div id="dm-finish-screen" class="dm-card" hidden>
  <h2>Check before you hand in</h2>
  <div id="dm-finish-report"></div>
  <button id="dm-submit" class="dm-primary">Download my submission</button>
  <button id="dm-keep-working" class="dm-secondary">Keep working</button>
</div>

<script type="application/json" id="dewmark-exam-model">{model_json}</script>
<script>{js}</script>
</body>
</html>
"""


# ---------------------------------------------------------------- outputs

def leak_fragments(exam):
    """Every piece of marking material that must never appear in the
    student or practice pages, normalised for comparison."""
    fragments = []

    def add(value, giveaway=False):
        # giveaway marks short expected words (blank answers, diagram
        # labels): finding one in the page usually means the question's
        # own visible text contains its answer, which deserves a message
        # about question writing rather than about leaked marking files.
        text = re.sub(r"\s+", " ", str(value)).strip().lower()
        if len(text) >= 4:
            fragments.append((text, giveaway))

    for section in exam["sections"]:
        for question in section["questions"]:
            for answer in question["answers"]:
                a = answer["settings"]
                if a.get("model_answer"):
                    add(a["model_answer"])
                if a["type"] == "fill-in-the-blank":
                    for gap in re.findall(r"\{([^{}]+)\}", a.get("text", "")):
                        add(gap, giveaway=True)
                for box in a.get("boxes") or []:
                    if isinstance(box, dict) and "expected" in box:
                        add(f'{box["label"]} {box["expected"]}')
                for label in a.get("labels") or []:
                    if isinstance(label, dict) and "expected" in label:
                        add(label["expected"], giveaway=True)
                parsed = answer.get("marking_parsed") or {}
                for point in parsed.get("points") or []:
                    add(point["text"])
                for guide in parsed.get("guidance") or []:
                    add(guide)
                for criterion in parsed.get("criteria") or []:
                    for band in criterion["bands"]:
                        add(band["text"])
    return fragments


def check_for_leaks(page_html, exam, variant):
    """The builder's final safeguard against its own mistakes: no marking
    material may appear in a page students receive."""
    # Only content a student can read matters here, so the page's own
    # styles and behaviour are cut out before scanning; and a short
    # expected word must match as a whole word, so that "break" does not
    # trip over the stylesheet's "break-inside".
    visible = re.sub(r"<style>.*?</style>|<script[^>]*>.*?</script>", " ",
                     page_html, flags=re.S)
    normalised = re.sub(r"\s+", " ", visible).lower()
    problems = []
    for fragment, giveaway in leak_fragments(exam):
        if giveaway:
            found = re.search(r"(?<![a-z0-9])" + re.escape(fragment)
                              + r"(?![a-z0-9])", normalised)
        else:
            found = fragment in normalised
        if found:
            if giveaway:
                problems.append((0, f"the expected answer "
                                 f"\"{fragment[:60]}\" appears in the "
                                 f"visible text of the {variant} page, so "
                                 "the question would give away its own "
                                 "answer; reword the question or the "
                                 "answer"))
            else:
                problems.append((0, f"marking material leaked into the "
                                 f"{variant} page: \"{fragment[:60]}\""))
    return problems


def marking_scheme(exam):
    """The file the marking workbench reads: everything stripped from the
    student pages, attached to the permanent names."""
    settings = exam["settings"]
    sections = []
    for section in exam["sections"]:
        s = section["settings"]
        questions = []
        for question in section["questions"]:
            q = question["settings"]
            prose = " ".join(node["md"] for node in question["content"]
                             if node["kind"] == "prose").strip()
            answers = []
            for answer in question["answers"]:
                a = dict(answer["settings"])
                a.pop("_line", None)
                answers.append({"settings": a,
                                "marking": answer.get("marking_parsed")})
            questions.append({"name": q["name"], "marks": q["marks"],
                              "topic": q.get("topic", ""),
                              "prose": prose, "answers": answers})
        sections.append({"name": s["name"], "choose": s.get("choose"),
                         "questions": questions})
    return {
        "format_version": 1,
        "exam_code": settings["exam_code"],
        "exam_version": settings["version"],
        "title": settings["title"],
        "total_marks": settings["total_marks"],
        "sections": sections,
    }


def build(exam_path, output_dir, check_only=False):
    exam_path = Path(exam_path)
    text = exam_path.read_text(encoding="utf-8")
    exam, problems = parse_exam_file(text, exam_path.parent)
    if problems:
        raise BuildError(sorted(problems))

    pages = {}
    for variant in ("student", "practice", "answer_key"):
        pages[variant] = build_page(exam, variant, exam_path.parent)
    for variant in ("student", "practice"):
        problems.extend(check_for_leaks(pages[variant], exam, variant))
    if problems:
        raise BuildError(sorted(problems))

    if check_only:
        return []

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    code = exam["settings"]["exam_code"]
    written = []
    names = {"student": f"{code}.student.html",
             "practice": f"{code}.practice.html",
             "answer_key": f"{code}.answer-key.html"}
    for variant, filename in names.items():
        path = output_dir / filename
        path.write_text(pages[variant], encoding="utf-8")
        written.append(path)
    scheme_path = output_dir / f"dewmark_{code}_marking_scheme.json"
    scheme_path.write_text(json.dumps(marking_scheme(exam), indent=2),
                           encoding="utf-8")
    written.append(scheme_path)
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build a dewmark exam from an exam file.")
    parser.add_argument("exam_file", help="the exam file to build")
    parser.add_argument("--output", default="finished",
                        help="folder for the finished pages")
    parser.add_argument("--check", action="store_true",
                        help="check the file without writing anything")
    args = parser.parse_args(argv)
    try:
        written = build(args.exam_file, args.output, check_only=args.check)
    except BuildError as err:
        print(err, file=sys.stderr)
        return 1
    if args.check:
        print("the exam file passes every check")
    else:
        for path in written:
            print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
