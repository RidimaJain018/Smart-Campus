"""
Smart Campus – Pure Python backend (no third-party libraries)
Run:  python server.py
Then open:  http://localhost:8000
"""

import http.server
import json
import os
import statistics
import urllib.parse
from pathlib import Path

PORT = 8000
BASE_DIR = Path(__file__).parent


# ── Directory Scanner (Lab 7) ─────────────────────────────────
def scan_directory(path):
    if not path.strip():
        return {"error": "Please enter a directory path."}
    if not os.path.exists(path):
        return {"error": f"FileNotFoundError: Invalid directory path: '{path}'"}
    if not os.path.isdir(path):
        return {"error": f"NotADirectoryError: '{path}' is not a directory."}

    tree_text = ""
    total_files = 0
    total_folders = 0
    warnings = []

    class MissingFileOrFolderError(Exception):
        pass

    try:
        for root, dirs, files in os.walk(path):
            level  = root.replace(path, "").count(os.sep)
            indent = "    " * level
            tree_text  += f"{indent}📁 {os.path.basename(root)}/\n"
            total_folders += 1
            for f in files:
                tree_text += f"{'    '*(level+1)}📄 {f}\n"
                total_files += 1
            if not files and not dirs:
                try:
                    raise MissingFileOrFolderError(f"Empty folder: '{root}'")
                except MissingFileOrFolderError as e:
                    warnings.append(str(e))
    except PermissionError:
        return {"error": f"PermissionError: Cannot access '{path}'"}
    except Exception as e:
        return {"error": f"Unexpected Error: {e}"}

    return {"tree": tree_text, "folders": total_folders, "files": total_files, "warnings": warnings}


# ── CSV Analytics (Lab 8) ─────────────────────────────────────
def run_analytics():
    csv_path = BASE_DIR / "student_performance.csv"
    if not csv_path.exists():
        return {"error": f"FileNotFoundError: 'student_performance.csv' not found."}

    try:
        with open(csv_path, "r") as f:
            lines = f.readlines()

        data = []
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) == 4:
                data.append({
                    "name":    parts[0],
                    "math":    float(parts[1]),
                    "science": float(parts[2]),
                    "english": float(parts[3]),
                })

        if not data:
            return {"error": "No data found in CSV."}

        subjects = ["math", "science", "english"]
        stats = {}
        for subj in subjects:
            vals = [d[subj] for d in data]
            stats[subj] = {
                "mean":   round(statistics.mean(vals), 2),
                "median": round(statistics.median(vals), 2),
                "stdev":  round(statistics.stdev(vals), 2) if len(vals) > 1 else 0,
                "top":    max(data, key=lambda d: d[subj])["name"],
                "topVal": max(vals),
            }

        averages = {
            "Math":    stats["math"]["mean"],
            "Science": stats["science"]["mean"],
            "English": stats["english"]["mean"],
        }

        rows = []
        for s in data:
            avg = round((s["math"] + s["science"] + s["english"]) / 3, 1)
            rows.append({**s, "avg": avg})

        return {"stats": stats, "averages": averages, "rows": rows}

    except Exception as e:
        return {"error": str(e)}


# ── Request Handler ───────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} – {fmt % args}")

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path: Path, content_type: str):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            f = BASE_DIR / "index.html"
            if f.exists():
                self.send_file(f, "text/html; charset=utf-8")
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"index.html not found")

        elif path == "/api/scan":
            dir_path = urllib.parse.parse_qs(parsed.query).get("path", [""])[0]
            result   = scan_directory(dir_path)
            self.send_json(result)

        elif path == "/api/analytics":
            result = run_analytics()
            self.send_json(result)

        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()


if __name__ == "__main__":
    with http.server.HTTPServer(("", PORT), Handler) as httpd:
        print(f"\n✅  Smart Campus running → http://localhost:{PORT}\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
