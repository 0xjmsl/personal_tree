"""Work tree: serves your threads as a live tree, a graph and a few charts.

Every request re-reads the files, so the page is always current. Nothing is cached
and nothing is written. Python standard library only.

A thread is a folder threads/<slug>/ with a thread.md that starts with a header:

    ---
    name: <short display name>
    status: idea | doing | blocked | waiting-you | done | parked | dropped   (empty = a container)
    parent: <slug>      where it belongs; empty = a top node (Work, Health, ...)
    origin: <slug>      where the idea came up; leave out when it equals parent
    why: "<one line>"
    opened: YYYY-MM-DD
    closed:
    next: "<one line>"
    ---

The page also reads, from the same file:
    ## Summary   the short story of the thread (shown in the details panel)
    ## Tasks     checkboxes: "- [ ]" open, "- [x]" done, "- [ ] <hourglass>" waits on you

"Last worked on" = the newest changelog.md entry that links the thread
([[threads/<slug>/thread]]). Small items live in threads/chores.md.

    python scripts/work_tree.py            # http://127.0.0.1:8790/
    python scripts/work_tree.py --lan      # also reachable from your phone on the home network
    python scripts/work_tree.py --port 9000
    python scripts/work_tree.py --json     # print the tree once and exit

To add your own chart: write a function that returns a dict, add a route for it in
H.do_GET, and draw it in dashboard/index.html (see the "Activity" tab for the pattern).
"""
import json, os, re, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THREADS = os.path.join(ROOT, "threads")
PAGE = os.path.join(ROOT, "dashboard", "index.html")
CHORES = os.path.join(THREADS, "chores.md")
CHANGELOG = os.path.join(ROOT, "changelog.md")
ARCHIVE = os.path.join(ROOT, "changelog_archive")
PORT = 8790
HOURGLASS = "⏳"
FIELDS = ("name", "status", "parent", "origin", "why", "opened", "closed", "next")
CHORE_STATUS = ("todo", "doing", "waiting-you", "done")

LINK = re.compile(r"threads/(?:_done/|_dropped/)?([A-Za-z0-9_.\-]+)")
DAY = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$")
TIME = re.compile(r"^-\s+`(\d{1,2}):(\d{2})`")


def read(path):
    try:
        with open(path, encoding="utf-8-sig", errors="replace") as f:   # -sig: Windows editors add a BOM
            return f.read()
    except OSError:
        return None


def parse(path):
    """One thread.md -> (header, title, tasks, summary, linked slugs), or None without a header."""
    text = read(path)
    if text is None or not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    head = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*?)\s*$", line)
        if not m or m.group(1) not in FIELDS:
            continue
        v = m.group(2).strip()
        if v[:1] not in "\"'":                    # a quoted value keeps its "#" (next: "Fix issue #12")
            v = re.sub(r"\s+#.*$", "", v).strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        head[m.group(1)] = v
    body = text[end + 4:]
    tm = re.search(r"^#\s+(.+)$", body, re.M)
    title = tm.group(1).strip() if tm else ""
    sm = re.search(r"^##\s+Summary\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    summary = sm.group(1).strip() if sm else ""
    tasks = []
    sec = re.search(r"^##\s+Tasks\s*$(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    if sec:
        for tl in sec.group(1).splitlines():
            km = re.match(r"^\s*[-*]\s+\[([ xX])\]\s+(.*)$", tl)
            if not km:
                continue
            txt = km.group(2).strip()
            done = km.group(1).lower() == "x"
            you = (not done) and txt.startswith(HOURGLASS)
            if you:
                txt = txt[len(HOURGLASS):].strip()
            tasks.append({"t": txt, "done": done, "you": you})
    return head, title, tasks, summary, sorted(set(LINK.findall(body)))


def parse_chores():
    """threads/chores.md: one chore per '## <title>', then 'status:' and 'why:' lines, then a description."""
    text = read(CHORES)
    if text is None:
        return []
    out = []
    for block in re.split(r"^##\s+", text, flags=re.M)[1:]:
        lines = block.strip("\n").splitlines()
        item = {"title": lines[0].strip(), "status": "todo", "why": "", "desc": ""}
        rest = []
        for ln in lines[1:]:
            m = re.match(r"^(status|why):\s*(.*?)\s*$", ln.strip())
            if m:
                item[m.group(1)] = m.group(2)
            else:
                rest.append(ln)
        item["desc"] = "\n".join(rest).strip()
        if item["status"] not in CHORE_STATUS:
            item["status"] = "todo"
        out.append(item)
    return out


def changelog_files():
    files = [CHANGELOG]
    if os.path.isdir(ARCHIVE):
        files += [os.path.join(ARCHIVE, n) for n in sorted(os.listdir(ARCHIVE)) if n.endswith(".md")]
    return files


def changelog_entries():
    """Every changelog line that links a thread: (day, 'HH:MM', [slugs])."""
    for path in changelog_files():
        text = read(path)
        if text is None:
            continue
        day = ""
        for line in text.splitlines():
            m = DAY.match(line)
            if m:
                day = m.group(1)
                continue
            if not day or not line.startswith("- "):
                continue
            slugs = sorted(set(LINK.findall(line)))
            if not slugs:
                continue
            tm = TIME.match(line)
            yield day, ("%02d:%s" % (int(tm.group(1)), tm.group(2)) if tm else "00:00"), slugs


def last_worked():
    last = {}
    for day, hhmm, slugs in changelog_entries():
        stamp = day + " " + hhmm
        for s in slugs:
            if stamp > last.get(s, ""):
                last[s] = stamp
    return last


def threads():
    nodes, no_header = [], []
    worked = last_worked()
    for folder, base in (("open", THREADS), ("done", os.path.join(THREADS, "_done")),
                         ("dropped", os.path.join(THREADS, "_dropped"))):
        if not os.path.isdir(base):
            continue
        for slug in sorted(os.listdir(base), key=str.lower):
            if slug.startswith("_"):
                continue
            p = os.path.join(base, slug, "thread.md")
            if not os.path.isfile(p):
                if os.path.isdir(os.path.join(base, slug)):
                    no_header.append(slug)          # a folder with no thread.md
                continue
            r = parse(p)
            if r is None:
                no_header.append(slug)
                continue
            head, title, tasks, summary, links = r
            node = {k: head.get(k, "") for k in FIELDS}
            node.update(slug=slug, folder=folder, title=title, tasks=tasks, summary=summary,
                        links=[s for s in links if s != slug], last=worked.get(slug, ""),
                        path=os.path.relpath(p, ROOT).replace("\\", "/"))
            nodes.append(node)
    return nodes, no_header


def build():
    nodes, no_header = threads()
    return {"nodes": nodes, "no_header": no_header, "chores": parse_chores()}


def graph():
    """Threads as a graph. Three kinds of edge, all read from thread.md:
    parent (where it belongs), origin (where the idea came up), link (one thread mentions another)."""
    nodes, _ = threads()
    known = {n["slug"] for n in nodes}
    out_nodes = [{"id": n["slug"], "name": n["name"] or n["slug"], "status": n["status"],
                  "folder": n["folder"], "parent": n["parent"],
                  "open": sum(1 for t in n["tasks"] if not t["done"]), "last": n["last"]} for n in nodes]
    edges, seen = [], set()
    for n in nodes:
        for kind, target in (("parent", n["parent"]), ("origin", n["origin"])):
            if target and target in known and target != n["slug"]:
                edges.append({"a": n["slug"], "b": target, "kind": kind})
                seen.add(frozenset((n["slug"], target)))
    for n in nodes:
        for target in n["links"]:
            key = frozenset((n["slug"], target))
            if target in known and key not in seen:
                edges.append({"a": n["slug"], "b": target, "kind": "link"})
                seen.add(key)
    return {"nodes": out_nodes, "edges": edges}


def activity():
    """Changelog entries per day per thread: {"days": {"YYYY-MM-DD": {"<slug>": count}}}.
    The page rolls each thread up to its top node, so you see where your attention went."""
    days = {}
    for day, _, slugs in changelog_entries():
        d = days.setdefault(day, {})
        for s in slugs:
            d[s] = d.get(s, 0) + 1
    return {"days": days}


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data):
        self._send(200, json.dumps(data).encode("utf-8"), "application/json")

    def do_GET(self):
        path = self.path.split("?")[0]
        try:
            if path == "/api/tree":
                self._json(build())
            elif path == "/api/graph":
                self._json(graph())
            elif path == "/api/activity":
                self._json(activity())
            elif path in ("/", "/index.html"):
                with open(PAGE, "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            else:
                self._send(404, b"not found", "text/plain")
        except Exception as e:  # the page shows the error instead of going blank
            self._send(500, json.dumps({"error": str(e)[:300]}).encode("utf-8"), "application/json")

    def log_message(self, *a):
        pass


def main():
    if "--json" in sys.argv:
        sys.stdout.write(json.dumps(build(), indent=1, ensure_ascii=True) + "\n")
        return
    port = PORT
    if "--port" in sys.argv:
        try:
            port = int(sys.argv[sys.argv.index("--port") + 1])
        except (IndexError, ValueError):
            sys.exit("--port needs a number, for example --port 8791")
    host = "0.0.0.0" if "--lan" in sys.argv else "127.0.0.1"
    ThreadingHTTPServer.allow_reuse_address = False      # so a second copy on the same port fails loudly
    try:
        srv = ThreadingHTTPServer((host, port), H)
    except OSError:
        sys.exit("port %d is taken (is the dashboard already running?). Try: --port %d" % (port, port + 1))
    print("work tree on http://%s:%d/  (Ctrl+C stops it)" % ("127.0.0.1" if host == "0.0.0.0" else host, port), flush=True)
    if host == "0.0.0.0":
        print("on your network: http://<this PC's address>:%d/  (no password: anyone on the network can read it)" % port, flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
