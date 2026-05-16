#!/usr/bin/env python3
"""Tiny static server for the AnswerLayer embed demo.

Serves index.html from this directory with caching disabled, so edits show
up on reload without a hard refresh. Plain `python3 -m http.server` works
too -- this just adds no-cache headers and a friendlier startup line.

Usage:
    python3 serve.py            # http://localhost:5174
    python3 serve.py 8080       # custom port
    PORT=8080 python3 serve.py  # custom port via env
"""

import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_PORT = 5174


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()


def main() -> None:
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    elif os.environ.get("PORT"):
        port = int(os.environ["PORT"])

    host = os.environ.get("HOST", "127.0.0.1")
    handler = partial(NoCacheHandler, directory=str(ROOT))
    server = ThreadingHTTPServer((host, port), handler)
    print(f"AnswerLayer embed demo: http://{host}:{port}/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
