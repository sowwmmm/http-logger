from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timezone
import os


class RequestHandler(BaseHTTPRequestHandler):

    def log_request_details(self, body=None):
        timestamp = datetime.now(timezone.utc).isoformat()

        print("\n" + "=" * 60)
        print(f"[{timestamp}] HTTP REQUEST")
        print(f"IP      : {self.client_address[0]}")
        print(f"Method  : {self.command}")
        print(f"Path    : {self.path}")
        print(f"Protocol: {self.request_version}")

        print("Headers:")
        for name, value in self.headers.items():
            print(f"  {name}: {value}")

        if body:
            print(f"Body    : {body!r}")

        print("=" * 60, flush=True)

    def handle_request(self):
        body = None

        content_length = self.headers.get("Content-Length")

        if content_length:
            try:
                length = int(content_length)
                if length > 0:
                    body = self.rfile.read(length)
            except (ValueError, OverflowError):
                pass

        self.log_request_details(body)

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Request received.\n")

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_PATCH(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def do_HEAD(self):
        self.log_request_details()

        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Disable BaseHTTPRequestHandler's default duplicate logging
        pass


host = "0.0.0.0"
port = int(os.environ.get("PORT", 8080))

server = HTTPServer((host, port), RequestHandler)

print(f"[*] Server listening on 0.0.0.0:{port}", flush=True)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
