"""Covers finding links and reading YouTube's answers; the requests to
YouTube and to GitHub in dev/check_video_links.py need the network."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dev"))

import check_video_links as cvl  # noqa: E402


class TestFindingLinks:
    def test_every_url_form_gives_the_same_id(self):
        text = (
            "<https://www.youtube.com/watch?v=abcdefghijk>\n"
            "https://youtu.be/abcdefghijk and "
            "https://www.youtube.com/embed/abcdefghijk?start=5\n"
            "https://m.youtube.com/watch?feature=share&v=abcdefghijk\n"
            "https://www.youtube.com/shorts/abcdefghijk"
        )
        assert {m["id"] for m in cvl.LINK_RE.finditer(text)} == {"abcdefghijk"}

    def test_a_channel_or_playlist_link_is_not_a_video(self):
        text = ("https://www.youtube.com/@SebastianLague "
                "https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi")
        assert list(cvl.LINK_RE.finditer(text)) == []

    def test_pages_are_grouped_under_each_video_once(self, tmp_path, monkeypatch):
        monkeypatch.setattr(cvl, "ROOT", tmp_path)
        (tmp_path / "tutorials" / "a").mkdir(parents=True)
        (tmp_path / "tutorials" / "b").mkdir(parents=True)
        a = tmp_path / "tutorials" / "a" / "a.md"
        b = tmp_path / "tutorials" / "b" / "b.md"
        a.write_text("youtu.be/x "
                     "https://youtu.be/aaaaaaaaaaa and again https://youtu.be/aaaaaaaaaaa")
        b.write_text("https://www.youtube.com/watch?v=aaaaaaaaaaa "
                     "https://www.youtube.com/watch?v=bbbbbbbbbbb")
        where = cvl.links_by_video([a, b])
        assert where == {
            "aaaaaaaaaaa": ["tutorials/a/a.md", "tutorials/b/b.md"],
            "bbbbbbbbbbb": ["tutorials/b/b.md"],
        }


class TestReadingAnswers:
    def test_each_status_means_one_thing(self):
        assert cvl.classify(200) == cvl.OK
        assert cvl.classify(400) == cvl.GONE
        assert cvl.classify(404) == cvl.GONE
        assert cvl.classify(401) == cvl.PRIVATE
        assert cvl.classify(403) == cvl.PRIVATE
        assert cvl.classify(429) == cvl.CHECK_FAILED
        assert cvl.classify(503) == cvl.CHECK_FAILED
        assert cvl.classify(None) == cvl.CHECK_FAILED

    def test_a_failed_check_is_retried_but_a_firm_answer_is_not(self):
        calls = []
        answers = {"flaky": [503, 200], "gone": [400]}

        def fetch(video_id):
            calls.append(video_id)
            return answers[video_id].pop(0)

        results = cvl.check(["flaky", "gone"], fetch=fetch, pause=0)
        assert results == {"flaky": cvl.OK, "gone": cvl.GONE}
        assert calls == ["flaky", "flaky", "gone"]

    def test_a_video_known_to_have_embedding_off_counts_as_there(self):
        known = next(iter(cvl.EMBEDDING_OFF))
        assert cvl.check([known], fetch=lambda _: 401, pause=0) == {known: cvl.OK}
        assert cvl.check([known], fetch=lambda _: 400, pause=0) == {known: cvl.GONE}


class TestTheReport:
    def test_it_names_each_page_under_its_video_and_carries_the_marker(self):
        results = {"aaaaaaaaaaa": cvl.GONE, "bbbbbbbbbbb": cvl.OK}
        where = {"aaaaaaaaaaa": ["tutorials/a/a.md"], "bbbbbbbbbbb": ["tutorials/b/b.md"]}
        body = cvl.report(results, where)
        assert body.startswith(cvl.MARKER)
        assert "## Gone (1)" in body
        assert "https://www.youtube.com/watch?v=aaaaaaaaaaa\n  - `tutorials/a/a.md`" in body
        assert "bbbbbbbbbbb" not in body
        assert "1 of 2 linked videos answered normally" in body

    def test_an_empty_section_is_left_out(self):
        body = cvl.report({"aaaaaaaaaaa": cvl.OK}, {"aaaaaaaaaaa": ["p.md"]})
        assert "##" not in body
