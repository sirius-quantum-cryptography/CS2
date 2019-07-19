__author__ = "mashed-potatoes"

from os import curdir, mkdir, _exit
from os.path import join, isdir
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pymitter import EventEmitter
from modules.config import HOME_PATH


class StoreHandler(BaseHTTPRequestHandler):
    route = "/upload"
    emitter = None
    debug = False

    def accepted(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Accepted")

    def not_found(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Error 404. Not Found.")
        self.wfile.close()

    def log_message(self, format, *args):
        if self.debug:
            return super().log_message(format, *args)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/emit" and self.emitter:
            qs = parse_qs(url.query)
            self.accepted()

            def payload():
                self.emitter.emit(
                    qs["event"][0], qs["args"][0] if "args" in qs else None
                )

            Thread(target=payload).start()
        elif url.path == "/exit":
            _exit(0xEE)
        else:
            self.not_found()

    def do_POST(self):
        url = urlparse(self.path)
        if url.path == self.route:
            length = self.headers["Content-Length"]
            data = self.rfile.read(int(length))
            fn = parse_qs(url.query)["filename"][0]
            name = join(
                HOME_PATH, "".join([x if x.isalnum() or x == "." else "_" for x in fn])
            )
            with open(name, "wb") as fh:
                fh.write(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.not_found()


class NetIO:
    server = HTTPServer
    emitter = None
    handler = StoreHandler

    def __init__(self, port: int) -> NetIO:
        self.server = HTTPServer(("", port), self.handler)
        if not isdir(HOME_PATH):
            mkdir(HOME_PATH)

    def set_emitter(self, emitter: EventEmitter) -> None:
        self.handler.emitter = emitter

    def start(self) -> None:
        self.server.serve_forever()
