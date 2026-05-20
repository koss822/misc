#!/usr/bin/env python3
"""
RAM Monitor — HTTP server
Serves the D3.js sunburst dashboard and a /api/ram JSON endpoint.
Reads process memory from /proc without any external dependencies.
"""

import json
import os
import pwd
from http.server import HTTPServer, BaseHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIND_HOST = "127.0.0.1"
BIND_PORT = 7777
MIN_RSS_BYTES = 512 * 1024  # skip processes using less than 512 KB


def collect():
    """Return a D3 hierarchy dict describing current RAM usage."""
    meminfo = {}
    with open("/proc/meminfo") as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 2:
                meminfo[parts[0].rstrip(":")] = int(parts[1]) * 1024

    total   = meminfo.get("MemTotal", 0)
    free    = meminfo.get("MemFree", 0)
    buffers = meminfo.get("Buffers", 0)
    cached  = meminfo.get("Cached", 0) + meminfo.get("SReclaimable", 0)

    by_user: dict[str, dict[str, int]] = {}
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            status: dict[str, str] = {}
            with open(f"/proc/{pid}/status") as f:
                for line in f:
                    k, _, v = line.partition("\t")
                    status[k.rstrip(":")] = v.strip()

            rss = int(status.get("VmRSS", "0 kB").split()[0]) * 1024
            if rss < MIN_RSS_BYTES:
                continue

            uid = int(status.get("Uid", "0").split()[0])
            try:
                user = pwd.getpwuid(uid).pw_name
            except KeyError:
                user = f"uid:{uid}"

            name = status.get("Name", f"pid{pid}")
            by_user.setdefault(user, {})
            by_user[user][name] = by_user[user].get(name, 0) + rss
        except (OSError, ValueError, KeyError):
            continue

    users = []
    for user, procs in sorted(by_user.items(), key=lambda x: -sum(x[1].values())):
        children = [
            {"name": name, "value": val}
            for name, val in sorted(procs.items(), key=lambda x: -x[1])
        ]
        if children:
            users.append({"name": user, "children": children})

    return {
        "name": f"RAM {total / 2**30:.1f} GB",
        "total": total,
        "children": [
            {"name": "Processes", "children": users},
            {"name": "Buffers+Cache", "value": buffers + cached},
            {"name": "Free",         "value": free},
        ],
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # suppress per-request access log

    def do_GET(self):
        if self.path == "/api/ram":
            body = json.dumps(collect()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

        elif self.path in ("/", "/index.html"):
            with open(os.path.join(BASE_DIR, "index.html"), "rb") as f:
                body = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    server = HTTPServer((BIND_HOST, BIND_PORT), Handler)
    print(f"RAM monitor running at http://{BIND_HOST}:{BIND_PORT}")
    server.serve_forever()
