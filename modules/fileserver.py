from os import curdir, mkdir
from os.path import join, isdir
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import asyncio

class StoreHandler(BaseHTTPRequestHandler):
    route = '/upload'
    store_path = join(curdir, 'data')
    if not isdir(store_path):
        print('Storage directory not exists! Creating...')
        mkdir(store_path)

    def not_found(self):
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Error 404. Not Found.")

    def do_GET(self):
        self.not_found()

    def do_POST(self):
        url = urlparse(self.path)
        if url.path == self.route:            
            length = self.headers['Content-Length']
            data = self.rfile.read(int(length))
            fn = parse_qs(url.query)['filename'][0]
            name = join(self.store_path, ''.join([x if x.isalnum() or x == '.' else "_" for x in fn]))
            with open(name, 'wb') as fh:
                fh.write(data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.end_headers()
            self.wfile.write(b"OK")
            print(f'Saved as {name}')
        else:
            self.not_found()


class FileServer:
    server = HTTPServer
    def __init__(self, port):
        self.server = HTTPServer(('', port), StoreHandler)
    
    def start(self):
        self.server.serve_forever()