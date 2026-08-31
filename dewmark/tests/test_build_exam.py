"""Tests for the exam builder's checks and outputs.

Each test writes a small exam file and asserts either that the builder
accepts it or that it refuses it for the documented reason. The sample
exam in samples/ is built in full as the end-to-end case.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
import build_exam  # noqa: E402  (path set up on the line above)

SAMPLES = Path(__file__).parent.parent / "samples"

MINIMAL = """\
```exam
title: Tiny Paper
exam_code: tiny-2027
version: 2027.01.01.1
total_marks: {total}
student_details: [full name, student number]
instructions: |
  Answer both questions.{extra_instructions}
```

```section
name: A
```

### Question A1

```question
name: a1
marks: 2
```

```answer
name: a1.def
type: short-written-answer
marks: 2
prompt: State what is meant by a variable.
model_answer: A named place that stores a value which can change.
```

{more}
"""

SECOND_QUESTION = """\
### Question A2

```question
name: a2
marks: 3
```

```answer
name: a2.blanks
type: fill-in-the-blank
marks: 3
text: |
  A loop repeats. A {while} loop repeats until its condition fails, a
  {for} loop repeats over a sequence, and stopping early uses {break}.
```
"""


def build_text(tmp_path, text):
    exam_file = tmp_path / "exam.md"
    exam_file.write_text(text, encoding="utf-8")
    return build_exam.build(exam_file, tmp_path / "out")


def minimal(total=5, more=SECOND_QUESTION, extra_instructions=""):
    return MINIMAL.format(total=total, more=more,
                          extra_instructions=extra_instructions)


def test_a_valid_file_builds_all_four_outputs(tmp_path):
    written = build_text(tmp_path, minimal())
    names = sorted(path.name for path in written)
    assert names == ["dewmark_tiny-2027_marking_scheme.json",
                     "tiny-2027.answer-key.html",
                     "tiny-2027.practice.html",
                     "tiny-2027.student.html"]


def test_building_twice_gives_identical_output(tmp_path):
    build_text(tmp_path, minimal())
    first = (tmp_path / "out" / "tiny-2027.student.html").read_text()
    build_text(tmp_path, minimal())
    second = (tmp_path / "out" / "tiny-2027.student.html").read_text()
    assert first == second


def test_model_answers_stay_out_of_the_student_page(tmp_path):
    build_text(tmp_path, minimal())
    for variant in ("student", "practice"):
        page = (tmp_path / "out" / f"tiny-2027.{variant}.html").read_text()
        assert "named place that stores" not in page.lower()
    key = (tmp_path / "out" / "tiny-2027.answer-key.html").read_text()
    assert "named place that stores" in key.lower()


def test_wrong_total_marks_is_refused(tmp_path):
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, minimal(total=9))
    assert "adds up to 5" in str(caught.value)


def test_duplicate_names_are_refused(tmp_path):
    text = minimal(more=SECOND_QUESTION.replace("name: a2.blanks",
                                                "name: a1.def"))
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, text)
    assert "already used" in str(caught.value)


def test_unknown_question_type_is_refused(tmp_path):
    text = minimal().replace("type: short-written-answer",
                             "type: mystery-question")
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, text)
    assert "unknown question type" in str(caught.value)


def test_python_code_is_named_as_not_built_yet(tmp_path):
    text = minimal().replace("type: short-written-answer",
                             "type: python-code")
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, text)
    assert "not built yet" in str(caught.value)


def test_a_choose_rule_missing_from_instructions_is_refused(tmp_path):
    text = minimal(total=3,
                   more=SECOND_QUESTION).replace("name: A\n",
                                                 "name: A\nchoose: 1\n")
    # total under choose 1 of two unequal questions also trips the
    # equal-marks rule, so both messages are acceptable evidence here.
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, text)
    message = str(caught.value)
    assert ("never mention" in message) or ("same marks" in message)


def test_an_answer_word_visible_in_the_question_is_refused(tmp_path):
    giveaway = SECOND_QUESTION.replace(
        "A loop repeats.", "A break statement stops a loop.")
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, minimal(more=giveaway))
    assert "give away its own answer" in str(caught.value)


def test_a_missing_picture_is_refused(tmp_path):
    more = """\
### Question A2

```question
name: a2
marks: 3
```

```answer
name: a2.labels
type: label-the-diagram
marks: 3
image: pictures/absent.svg
image_description: A diagram that does not exist.
labels:
  - number: 1
    expected: something
```
"""
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, minimal(more=more))
    assert "does not exist" in str(caught.value)


def test_a_picture_without_a_description_is_refused(tmp_path):
    picture_dir = tmp_path / "pictures"
    picture_dir.mkdir()
    (picture_dir / "square.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><rect/></svg>')
    more = """\
### Question A2

```question
name: a2
marks: 3
```

```answer
name: a2.labels
type: label-the-diagram
marks: 3
image: pictures/square.svg
labels:
  - number: 1
    expected: something
```
"""
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, minimal(more=more))
    assert "image_description" in str(caught.value)


def test_points_that_cannot_reach_the_limit_are_refused(tmp_path):
    more = SECOND_QUESTION + """\

```marking
limit: 3
points:
  - 1 mark - mentions repetition
```
"""
    with pytest.raises(build_exam.BuildError) as caught:
        build_text(tmp_path, minimal(more=more))
    assert "full marks would be unreachable" in str(caught.value)


def test_the_sample_exam_builds(tmp_path):
    written = build_exam.build(SAMPLES / "sample-mixed-paper.exam.md",
                               tmp_path / "out")
    assert len(written) == 4
    scheme = json.loads(
        (tmp_path / "out" / "dewmark_sample-mixed-2027_marking_scheme.json")
        .read_text())
    assert scheme["total_marks"] == 50
    section_b = scheme["sections"][1]
    assert section_b["choose"] == 1
    essay = section_b["questions"][0]["answers"][0]
    assert essay["marking"]["method"] == "a-criteria-grid"
    assert sum(c["marks"] for c in essay["marking"]["criteria"]) == 20


def test_the_sample_student_page_contains_no_expected_values(tmp_path):
    build_exam.build(SAMPLES / "sample-mixed-paper.exam.md",
                     tmp_path / "out")
    page = (tmp_path / "out" / "sample-mixed-2027.student.html").read_text()
    lowered = page.lower()
    for fragment in ("cell wall", "counterexample is a single case",
                     "names the optimum", "sustained line of argument"):
        assert fragment not in lowered
