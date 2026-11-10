"""What a command-line build prints: one summary line, then the notes the
build carried on despite, together and last, where a teacher reading the end
of the output sees them. -v gives each page and each note as it happens.
(Before, a build printed a line for each of about 1,250 pages and the notes
were somewhere in the middle.)"""

from __future__ import annotations

import sys

import pytest

from helpers import *  # noqa: F401,F403
from helpers import b

CELL = "```python exec\nid: add-up\ndef total_of(values):\n    ...\n```\n"
A_NOTE = CELL + "```hint\nafter: soon\nX.\n```\n"  # an unreadable after: is a note


@pytest.fixture()
def run(repo, monkeypatch, capsys):
    monkeypatch.setattr(b.cfg, "NOTES_AT_END", False)  # main() sets it; put it back after
    monkeypatch.setattr(b.cfg, "SOURCE_MAP", True)

    def go(*flags):
        monkeypatch.setattr(sys, "argv", ["build.py", "--no-standalone", *flags])
        code = b.main()
        out, err = capsys.readouterr()
        return code, out, err
    return go


def test_a_build_prints_a_summary_and_then_its_notes_together(repo, run):
    write(repo, A_NOTE)
    code, out, err = run()
    assert code == 0
    assert out.strip().endswith("into site/") and "wrote " not in out
    assert err.index("1 note: the build carried on") < err.index("has a term I cannot read")
    assert err.count("has a term I cannot read") == 1


def test_verbose_gives_each_page_and_each_note_as_it_happens(repo, run):
    write(repo, A_NOTE)
    code, out, err = run("-v")
    assert code == 0 and "wrote site/tutorials/sample.html" in out
    assert "has a term I cannot read" in err and "the build carried on" not in err


def test_a_build_with_nothing_to_say_prints_only_its_summary(repo, run):
    write(repo, "Prose.\n")
    code, out, err = run()
    assert code == 0 and "into site/" in out and err == ""


def test_a_failing_build_still_shows_the_notes_before_the_failure(repo, run):
    write(repo, A_NOTE + "\nSee [another page](tutorial:a-page-that-is-not-there).\n")
    code, out, err = run()
    assert code == 1
    assert err.index("has a term I cannot read") < err.index("build failed")


# ------------------------------------------------------------------ --serve

def test_serve_builds_without_downloads_and_then_shows_the_site(repo, monkeypatch):
    """A preview is one command. The downloads are the slow part and a
    preview does not need them, so --serve leaves them out and says so."""
    monkeypatch.setattr(b.cfg, "NOTES_AT_END", False)  # main() sets both; put them back after
    monkeypatch.setattr(b.cfg, "SOURCE_MAP", False)
    shown = []
    monkeypatch.setattr(b.serve, "run", lambda directory, port: shown.append((directory, port)) or 0)
    built = []
    real = b.build
    monkeypatch.setattr(b, "build", lambda **kw: built.append(kw) or real(**kw))
    write(repo, CELL)
    monkeypatch.setattr(sys, "argv", ["build.py", "--serve", "--port", "8123"])  # not --no-standalone
    assert b.main() == 0
    assert shown == [(repo / "site", 8123)]
    assert built and built[0]["standalone"] is False

    # Without --serve the same command still builds the downloads. (A stand-in
    # for the build: the real one needs the real assets on disk.)
    built.clear()
    monkeypatch.setattr(b, "build", lambda **kw: built.append(kw) or [])
    monkeypatch.setattr(sys, "argv", ["build.py"])
    b.main()
    assert built and built[0]["standalone"] is True


def test_a_build_that_fails_is_not_served(repo, run, monkeypatch):
    shown = []
    monkeypatch.setattr(b.serve, "run", lambda directory, port: shown.append(1) or 0)
    write(repo, "```python exec\nid: no-end\nprint(1)\n")  # a fence that never closes
    code, out, err = run("--serve")
    assert code == 1 and not shown


def test_the_preview_server_serves_the_files_to_this_machine_only(tmp_path):
    import threading
    import urllib.request

    (tmp_path / "index.html").write_text("<p>hello</p>")
    server = b.serve.make_server(tmp_path, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address
        assert host == "127.0.0.1"
        assert urllib.request.urlopen(f"http://127.0.0.1:{port}/index.html").read() == b"<p>hello</p>"
        with pytest.raises(OSError):  # a second preview on the same port says so, and run() turns that into words
            b.serve.make_server(tmp_path, port)
    finally:
        server.shutdown()
        server.server_close()


def test_a_port_already_in_use_is_said_in_words(tmp_path, capsys):
    taken = b.serve.make_server(tmp_path, 0)
    try:
        port = taken.server_address[1]
        assert b.serve.run(tmp_path, port) == 1
        assert f"--port {port + 1}" in capsys.readouterr().out
    finally:
        taken.server_close()


def test_ctrl_c_stops_the_preview_cleanly(tmp_path, monkeypatch, capsys):
    closed = []

    class Server:
        server_address = ("127.0.0.1", 8000)

        def serve_forever(self):
            raise KeyboardInterrupt

        def server_close(self):
            closed.append(1)

    monkeypatch.setattr(b.serve, "make_server", lambda directory, port: Server())
    assert b.serve.run(tmp_path, 8000) == 0
    assert closed == [1]
    assert "http://localhost:8000/" in capsys.readouterr().out
