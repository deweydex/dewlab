"""The glossary's Python entries, checked against Python itself.

`dev/glossary_python.py` is the only thing standing between a glossary
entry and a function that was misspelled, removed, or shown with an example
Python would reject. These tests make sure it still notices, and that the
build carries its signatures through to the reference. The real glossary is
checked by the script itself, `--check` in CI's glossary-python job.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "dev"))
sys.path.insert(0, str(ROOT))

import build  # noqa: E402
import glossary_python as gp  # noqa: E402


class TestResolving:
    def test_a_method_is_found_on_its_type(self):
        obj, owner = gp.resolve("list.append")
        assert obj is list.append and owner is list

    def test_a_keyword_needs_no_import(self):
        assert gp.resolve("elif")[0] is gp.KEYWORD

    def test_a_misspelling_is_named(self):
        with pytest.raises(LookupError, match="apend"):
            gp.resolve("list.apend")

    def test_an_unknown_bare_name_is_refused(self):
        with pytest.raises(LookupError):
            gp.resolve("prnt")


class TestExamples:
    def test_a_call_that_fits_passes(self):
        assert gp.example_problems("len(scores)", "len", len, None) == []

    def test_too_many_arguments_is_caught(self):
        assert gp.example_problems("len(scores, 2)", "len", len, None)

    def test_a_keyword_the_function_does_not_take_is_caught(self):
        import random
        assert gp.example_problems(
            "random.sample(deck, size=5)", "random.sample", random.sample, None)

    def test_a_method_call_passes_its_object_as_self(self):
        """`scores.append(50)` is one argument from the reader and two
        from the signature's point of view; counting it as one would
        reject every method example there is."""
        assert gp.example_problems("scores.append(50)", "list.append", list.append, list) == []

    def test_an_example_that_is_not_python_is_left_alone(self):
        assert gp.example_problems("transform: rotateX(90deg);", "len", len, None) == []

    def test_a_block_header_is_read_as_a_whole_statement(self):
        assert gp.example_problems(
            "for index, name in enumerate(names):", "enumerate", enumerate, None) == []


class TestSignatures:
    def test_a_methods_self_is_left_out(self):
        assert gp.display("list.append", list.append, list) == "list.append(object, /)"

    def test_the_courses_own_helpers_show_their_bare_names(self):
        obj, owner = gp.resolve("tutorial_tools.show_table")
        shown = gp.display("tutorial_tools.show_table", obj, owner)
        assert shown.startswith("show_table(")
        assert ":" not in shown, "type hints are left out"

    def test_a_third_party_library_gets_no_signature(self):
        pandas = pytest.importorskip("pandas")
        obj, owner = gp.resolve("pandas.DataFrame.to_csv")
        assert obj is pandas.DataFrame.to_csv
        assert not gp.gets_a_signature(obj, owner)


class TestTheBuild:
    def test_an_entry_carries_the_signatures_python_gives(self):
        entries = [{"term": "len()", "kind": "function", "definition": "d",
                    "python": "len"},
                   {"term": "elif", "kind": "keyword", "definition": "d",
                    "python": "elif"}]
        build.with_python(entries, ROOT / "tutorials" / "x" / "x.glossary.yaml")
        assert entries[0]["signatures"] == [gp.display("len", len, None)]
        assert "signatures" not in entries[1]

    def test_a_python_field_of_the_wrong_shape_shows_no_signature_and_says_so(self, capsys):
        entries = [{"term": "len()", "kind": "function", "definition": "d",
                    "python": {"name": "len"}}]
        shown = build.with_python(entries, ROOT / "tutorials" / "x" / "x.glossary.yaml")
        assert "signatures" not in shown[0]
        assert "not a dotted name" in capsys.readouterr().err
