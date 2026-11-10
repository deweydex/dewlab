"""Show the built site in a browser, from this machine.

`python3 build.py --serve` builds the site and then runs this, so a preview
is one command. The page is served the way the hosted site serves it: as
plain files, with no step in between.

The server listens on 127.0.0.1 only. Nobody else on the network can reach
it, which matters on a school network where a teacher's laptop is on the
same network as a room of students.
"""

from __future__ import annotations

import functools
import http.server
from pathlib import Path

HOST = "127.0.0.1"


class _Quiet(http.server.SimpleHTTPRequestHandler):
    """The files, without a line for each one. Something that went wrong (a
    link to a page that is not there) is still said."""

    def log_request(self, code="-", size="-"):  # noqa: D102
        pass


def make_server(directory: Path, port: int = 8000) -> http.server.ThreadingHTTPServer:
    """A server for `directory`, not yet running. Port 0 takes any free port,
    which is what a test wants; the one it got is `server.server_address[1]`.
    Raises OSError when the port is in use."""
    handler = functools.partial(_Quiet, directory=str(directory))
    return http.server.ThreadingHTTPServer((HOST, port), handler)


def run(directory: Path, port: int = 8000) -> int:
    """Serve `directory` until Ctrl-C. Returns the exit code for the command."""
    try:
        server = make_server(directory, port)
    except OSError:
        print(f"Port {port} is already in use, perhaps by an earlier preview. "
              f"Stop that one, or use another port: python3 build.py --serve --port {port + 1}")
        return 1
    print()
    print(f"The site is at  http://localhost:{server.server_address[1]}/")
    print("Press Ctrl-C to stop. After you change a file, stop and run it again.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()
    return 0
