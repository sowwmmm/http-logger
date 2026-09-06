```python
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timezone
import os


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        output = params.get("output", [None])[0]

        timestamp = datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )

        if output is not None:
            print(f"[{timestamp}] OUTPUT: {output}", flush=True)
        else:
            print(
                f"[{timestamp}] REQUEST: {self.path}",
                flush=True
            )

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        self.wfile.write(b"OK\n")

    def log_message(self, format, *args):
        # Prevent duplicate default HTTP logging
        pass


port = int(os.environ.get("PORT", 8080))

server = HTTPServer(("0.0.0.0", port), Handler)

print(f"[*] Listening on port {port}", flush=True)

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
```
