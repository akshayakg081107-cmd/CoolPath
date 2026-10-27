"""CoolPath demo web server. Uses only the Python standard library."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote
import json
import mimetypes

from app.routing import load_network, recommend_routes

ROOT = Path(__file__).resolve().parent
NETWORK = load_network(ROOT / "data" / "sample_network.json")
HOST = "127.0.0.1"
PORT = 8000

class CoolPathHandler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type="text/plain; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path == "/":
            self._send(200, (ROOT / "templates" / "index.html").read_text(encoding="utf-8"), "text/html; charset=utf-8")
            return
        if path.startswith("/static/"):
            relative = path.removeprefix("/static/")
            candidate = (ROOT / "static" / relative).resolve()
            static_root = (ROOT / "static").resolve()
            if static_root not in candidate.parents or not candidate.is_file():
                self._send(404, "Not found")
                return
            content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
            self._send(200, candidate.read_bytes(), f"{content_type}; charset=utf-8")
            return
        if path == "/api/routes":
            query = parse_qs(parsed.query)
            start = query.get("start", ["A"])[0]
            end = query.get("end", ["D"])[0]
            try:
                payload = {"routes": recommend_routes(NETWORK, start, end),
                           "notice": "Illustrative prototype scores only; not a safety guarantee."}
                self._send(200, json.dumps(payload), "application/json; charset=utf-8")
            except (ValueError, KeyError) as exc:
                self._send(400, json.dumps({"error": str(exc)}), "application/json; charset=utf-8")
            return
        self._send(404, "Not found")

    def log_message(self, fmt, *args):
        print("[CoolPath] " + (fmt % args))

if __name__ == "__main__":
    print(f"CoolPath running at http://{HOST}:{PORT}")
    print("Demo data only; do not use as a real-world safety guarantee.")
    ThreadingHTTPServer((HOST, PORT), CoolPathHandler).serve_forever()
