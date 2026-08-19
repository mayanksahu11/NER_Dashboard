"""Dashboard server: serves static files and generates manifest.json on the fly.

Run:  python serve.py [port]
Then open http://localhost:8000/
"""
import json
import re
import sys
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).parent
PATTERN = re.compile(
    r"^(?P<classifier>.+?)_(?P<day>\d{1,2})(?P<mon>[A-Za-z]{3})(?P<year>\d{4})_(?:(?P<blind>Blind)_)?Report\.md$"
)
MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}


def build_manifest() -> dict:
    entries = []
    for p in sorted(HERE.glob("*_Report.md")):
        m = PATTERN.match(p.name)
        if not m:
            continue
        mon = m.group("mon").capitalize()
        if mon not in MONTHS:
            continue
        d = datetime(int(m.group("year")), MONTHS[mon], int(m.group("day")))
        blind = m.group("blind") is not None
        entries.append({
            "file": p.name,
            "classifier": m.group("classifier"),
            "date": d.strftime("%Y-%m-%d"),
            "date_label": f"{int(m.group('day'))} {mon} {m.group('year')}",
            "blind": blind,
        })
    entries.sort(key=lambda e: (e["classifier"], e["date"]))
    return {"reports": entries}


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        # Strip query string for path matching
        path = self.path.split("?", 1)[0]
        if path in ("/manifest.json", "/manifest.json/"):
            body = json.dumps(build_manifest(), indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def end_headers(self):
        # Prevent stale reports being served from cache
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("[dashboard] " + fmt % args + "\n")


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Dashboard running at http://localhost:{port}/ (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
