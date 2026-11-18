"""
Marcha API CLI — interact with the Marcha task launcher over its local HTTP API.

Usage:
    python marcha.py state                          # full app snapshot
    python marcha.py templates                      # list saved templates
    python marcha.py reload                          # re-read templates.json from disk (no restart)
    python marcha.py tasks                          # list active tasks
    python marcha.py task TASK_ID                   # single task + log buffer
    python marcha.py launch TEMPLATE_ID             # launch a template
    python marcha.py input TASK_ID "text"           # send input to a running task
    python marcha.py run TASK_ID                    # start a stopped task
    python marcha.py stop TASK_ID                   # graceful stop (Ctrl+C)
    python marcha.py kill TASK_ID                   # force kill (process tree)
    python marcha.py layout                         # current layout + slots
    python marcha.py assign SLOT_INDEX TYPE [ID]    # assign content to a slot
    python marcha.py history                        # execution history (with IDs)
    python marcha.py tasklog HISTORY_ID [--tail N]  # saved terminal log for a history entry
    python marcha.py resources TASK_ID              # CPU/memory stats
    python marcha.py restart ID[:KILL_S[:START_S]] ... # orchestrated restart with delays
    python marcha.py schedules                      # scheduled jobs: next fire, last run and its exit code
    python marcha.py runs JOB_ID                    # a job's recent runs
    python marcha.py newkey                         # make a signing key; prints the address for Allowed Addresses
    python marcha.py address                        # the address of the signing key

SLOT TYPE values: empty, tasksList, history, terminal, resources
    (terminal and resources require an ID argument)

Default: http://127.0.0.1:7832  (override with MARCHA_PORT env var)
The API is off until you turn it on in Marcha: API in the left bar, the switch under Server.

Signed requests (recommended, Marcha 1.0.1 or newer): run `newkey` once, paste the address it
prints into Marcha's API screen under Allowed Addresses. From then on every request is signed
and Marcha answers nobody else. Signing needs one package: pip install eth-account.
The key is a file, ~/.marcha_api_key (override with MARCHA_KEY_FILE); keep it out of any folder
that is synced or shared. With no key file, requests go unsigned, which only works while
Allowed Addresses is empty.
"""

import argparse
import json
import os
import re
import secrets
import sys
import time
import urllib.request
import urllib.error

# Windows cp1252 can't print emojis — replace with '?'
sys.stdout.reconfigure(errors="replace")


# --- Config ---

DEFAULT_PORT = 7832
BASE = "http://127.0.0.1"


def get_base():
    import os
    port = os.environ.get("MARCHA_PORT", str(DEFAULT_PORT))
    return f"{BASE}:{port}"


# --- Signing ---

KEY_FILE = os.environ.get("MARCHA_KEY_FILE") or os.path.join(os.path.expanduser("~"), ".marcha_api_key")

# (method, path pattern) -> the action Marcha expects for that endpoint.
ROUTES = [
    ("GET", r"/api/state", "get_state"),
    ("GET", r"/api/tasks", "get_tasks"),
    ("GET", r"/api/tasks/[^/]+", "get_task"),
    ("POST", r"/api/tasks/[^/]+/run", "run_task"),
    ("POST", r"/api/tasks/[^/]+/stop", "stop_task"),
    ("POST", r"/api/tasks/[^/]+/kill", "kill_task"),
    ("POST", r"/api/tasks/[^/]+/input", "input_task"),
    ("GET", r"/api/templates", "get_templates"),
    ("POST", r"/api/templates/reload", "reload_templates"),
    ("POST", r"/api/templates/[^/]+/launch", "launch_template"),
    ("GET", r"/api/layout", "get_layout"),
    ("POST", r"/api/layout/assign", "assign_layout"),
    ("GET", r"/api/history", "get_history"),
    ("GET", r"/api/logs/[^/]+", "get_log"),
    ("GET", r"/api/resources/[^/]+", "get_resources"),
    ("POST", r"/api/restart", "restart_tasks"),
    ("GET", r"/api/debug/log", "get_debug_log"),
    ("GET", r"/api/schedules", "get_schedules"),
    ("POST", r"/api/schedules", "upsert_schedule"),
    ("POST", r"/api/schedules/[^/]+/run", "run_schedule"),
    ("GET", r"/api/schedules/[^/]+/runs", "get_schedule_runs"),
]


def _eth():
    try:
        from eth_account import Account
        from eth_account.messages import encode_defunct
        return Account, encode_defunct
    except ImportError:
        print("Signing needs one package:  pip install eth-account")
        sys.exit(1)


def _account():
    """The signing account, or None when there is no key file (requests then go unsigned)."""
    if not os.path.isfile(KEY_FILE):
        return None
    Account, _ = _eth()
    with open(KEY_FILE, encoding="utf-8") as f:
        return Account.from_key(f.read().strip())


def envelope(method, path, data=None):
    """The signed request Marcha checks: one action, one path, one nonce, once."""
    acct = _account()
    if acct is None:
        return None
    _, encode_defunct = _eth()
    path = path.split("?", 1)[0]
    action = next((a for m, pat, a in ROUTES if m == method and re.fullmatch(pat, path)), None)
    if action is None:
        print(f"No Marcha endpoint for {method} {path}")
        sys.exit(1)
    data = data or {}
    client = acct.address.lower()
    ts = int(time.time())
    nonce = secrets.token_hex(16)
    # These six keys, in this order, as compact JSON: what Marcha rebuilds and hashes.
    message = json.dumps({"action": action, "client": client, "data": data, "nonce": nonce, "path": path, "timestamp": ts},
                         separators=(",", ":"), ensure_ascii=False)
    sig = acct.sign_message(encode_defunct(text=message)).signature.hex()
    if not sig.startswith("0x"):
        sig = "0x" + sig
    return {"timestamp": ts, "action": action, "path": path, "nonce": nonce,
            "data": data, "client": client, "signature": sig}


# --- HTTP helpers ---

def _send(req):
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            body = json.loads(body).get("error", body)
        except (json.JSONDecodeError, AttributeError):
            pass
        print(f"Error {e.code}: {body}")
        if e.code == 401 and "Missing X-Signed-Request" in str(body):
            print("Marcha accepts signed requests only. Run `newkey` and add its address to Allowed Addresses.")
        if e.code == 403 and "not allowed" in str(body):
            print("This key's address is not in Marcha's Allowed Addresses (run `address` to see it).")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection failed: {e.reason}")
        print("Is Marcha running with the API server enabled?")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Marcha answered with something that is not JSON.")
        sys.exit(1)


def api_get(path):
    req = urllib.request.Request(f"{get_base()}{path}", method="GET")
    req.add_header("Accept", "application/json")
    env = envelope("GET", path)
    if env is not None:
        req.add_header("X-Signed-Request", json.dumps(env, separators=(",", ":"), ensure_ascii=False))
    return _send(req)


def api_post(path, data=None):
    env = envelope("POST", path, data)
    body = json.dumps(env if env is not None else (data or {}), separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"{get_base()}{path}", data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    return _send(req)


# --- Formatters ---

def print_json(data):
    print(json.dumps(data, indent=2))


def print_templates(templates):
    if not templates:
        print("No templates found.")
        return
    print(f"{'ID':<36}  {'Icon':<4}  {'Name':<30}  {'Command'}")
    print("-" * 100)
    for t in templates:
        icon = t.get("emoji", "")
        name = t.get("name", "?")
        cmd = t.get("command", "")
        args = " ".join(t.get("arguments") or t.get("args") or [])
        tid = t.get("id", "?")
        full_cmd = f"{cmd} {args}".strip()
        if len(full_cmd) > 40:
            full_cmd = full_cmd[:37] + "..."
        print(f"{tid:<36}  {icon:<4}  {name:<30}  {full_cmd}")


def print_tasks(tasks):
    if not tasks:
        print("No active tasks.")
        return
    print(f"{'ID':<36}  {'Status':<10}  {'Name':<30}  {'PID'}")
    print("-" * 90)
    for t in tasks:
        tid = t.get("id", "?")
        status = t.get("status", "?")
        name = t.get("templateName", t.get("name", "?"))
        pid = t.get("pid", "-")
        print(f"{tid:<36}  {status:<10}  {name:<30}  {pid}")


def print_task_detail(data):
    task = data if "id" in data else data.get("task", data)
    print(f"Task:     {task.get('templateName', task.get('name', '?'))}")
    print(f"ID:       {task.get('id', '?')}")
    print(f"Status:   {task.get('status', '?')}")
    print(f"PID:      {task.get('pid', '-')}")
    cmd = task.get("command", "")
    args = " ".join(task.get("arguments") or task.get("args") or [])
    if cmd:
        print(f"Command:  {cmd} {args}".strip())
    wd = task.get("workingDirectory", "")
    if wd:
        print(f"Dir:      {wd}")

    # The API returns the terminal output under "log", as a list of lines.
    log = data.get("log") or task.get("log") or data.get("logBuffer") or task.get("logBuffer")
    if isinstance(log, list):
        log = "\n".join(str(x) for x in log)
    if log:
        tail = log[-4000:]
        print(f"\n--- Terminal output (last {len(tail)} chars) ---")
        print(tail)


def print_history(entries):
    if not entries:
        print("No history entries.")
        return
    print(f"{'ID':<14}  {'Status':<10}  {'Name':<24}  {'Started':<20}  {'Task ID'}")
    print("-" * 100)
    for e in entries:
        hid = e.get("id", "?")
        status = e.get("status", "?")
        name = e.get("name", "?")
        started = e.get("startedAt", "?")[:19] if e.get("startedAt") else "?"
        task_id = e.get("taskId", "-") or "-"
        if len(name) > 22:
            name = name[:19] + "..."
        print(f"{hid:<14}  {status:<10}  {name:<24}  {started:<20}  {task_id}")


# --- Commands ---

def cmd_state(_args):
    data = api_get("/api/state")
    tasks = data.get("tasks", [])
    templates = data.get("templates", [])
    history = data.get("history", [])
    print(f"Tasks: {len(tasks)} active  |  Templates: {len(templates)}  |  History: {len(history)} entries")
    if tasks:
        print("\n-- Active Tasks --")
        print_tasks(tasks)
    if templates:
        print("\n-- Templates --")
        print_templates(templates)


def cmd_templates(_args):
    data = api_get("/api/templates")
    templates = data if isinstance(data, list) else data.get("templates", [])
    print_templates(templates)


def cmd_reload(_args):
    data = api_post("/api/templates/reload")
    print(f"Reloaded templates from disk. Count: {data.get('count', '?')}")


def cmd_tasks(_args):
    data = api_get("/api/tasks")
    tasks = data if isinstance(data, list) else data.get("tasks", [])
    print_tasks(tasks)


def cmd_task(args):
    data = api_get(f"/api/tasks/{args.task_id}")
    print_task_detail(data)


def cmd_launch(args):
    data = api_post(f"/api/templates/{args.template_id}/launch")
    print(f"Launched. Task ID: {data.get('id', data.get('taskId', '?'))}")
    if "templateName" in data or "name" in data:
        print(f"Name: {data.get('templateName', data.get('name'))}")


def cmd_input(args):
    text = " ".join(args.text)
    data = api_post(f"/api/tasks/{args.task_id}/input", {"text": text})
    print(f"Sent to {args.task_id}: {text}")


def cmd_run(args):
    data = api_post(f"/api/tasks/{args.task_id}/run")
    print(f"Started task {args.task_id}")


def cmd_stop(args):
    data = api_post(f"/api/tasks/{args.task_id}/stop")
    print(f"Stopped task {args.task_id}")


def cmd_kill(args):
    data = api_post(f"/api/tasks/{args.task_id}/kill")
    print(f"Killed task {args.task_id}")


def cmd_layout(_args):
    data = api_get("/api/layout")
    print_json(data)


def cmd_assign(args):
    payload = {
        "slotIndex": int(args.slot_index),
        "contentType": args.content_type,
    }
    if args.content_id:
        payload["contentId"] = args.content_id
    data = api_post("/api/layout/assign", payload)
    print(f"Assigned slot {args.slot_index} -> {args.content_type}")


def cmd_history(_args):
    data = api_get("/api/history")
    entries = data if isinstance(data, list) else data.get("history", [])
    print_history(entries)


def cmd_resources(args):
    data = api_get(f"/api/resources/{args.task_id}")
    stats = data.get("latestStats")
    if not stats:
        print("No resource data yet (polling runs every 5s after task start).")
        return
    print(f"CPU:    {stats.get('cpuPercent', 0):.1f}%")
    print(f"Memory: {stats.get('memoryMb', 0):.1f} MB")
    children = stats.get("children", [])
    if children:
        print(f"\nChild processes ({len(children)}):")
        for c in children:
            print(f"  PID {c.get('pid')}: CPU {c.get('cpuPercent', 0):.1f}%, Mem {c.get('memoryMb', 0):.1f} MB  ({c.get('name', '?')})")


def cmd_restart(args):
    """Orchestrated restart: kill tasks in order, then start in order, with delays."""
    tasks = []
    for spec in args.specs:
        parts = spec.split(":")
        task_id = parts[0]
        kill_delay = int(parts[1]) * 1000 if len(parts) > 1 else 0
        start_delay = int(parts[2]) * 1000 if len(parts) > 2 else 0
        tasks.append({
            "taskId": task_id,
            "killDelayMs": kill_delay,
            "startDelayMs": start_delay,
        })

    data = api_post("/api/restart", {"tasks": tasks})
    task_ids = data.get("tasks", [])
    print(f"Restart sequence initiated for {len(task_ids)} tasks: {', '.join(task_ids)}")


def cmd_tasklog(args):
    """Fetch saved terminal log for a history entry."""
    data = api_get(f"/api/logs/{args.history_id}")
    name = data.get("name", "?")
    cmd = data.get("command", "")
    cmd_args = " ".join(data.get("arguments", []))
    started = data.get("startedAt", "?")
    ended = data.get("endedAt", "-")
    exit_code = data.get("exitCode", "-")
    lines = data.get("lines", [])

    print(f"Task:     {name}")
    print(f"Command:  {cmd} {cmd_args}".strip())
    print(f"Started:  {started}")
    print(f"Ended:    {ended}")
    print(f"Exit:     {exit_code}")
    print(f"Lines:    {len(lines)}")

    if lines:
        tail = args.tail
        if tail and tail < len(lines):
            print(f"\n--- Last {tail} lines ---")
            for line in lines[-tail:]:
                print(line)
        else:
            print(f"\n--- Full output ({len(lines)} lines) ---")
            for line in lines:
                print(line)


def cmd_schedules(_args):
    data = api_get("/api/schedules")
    jobs = data if isinstance(data, list) else data.get("schedules", data.get("jobs", []))
    if not jobs:
        print("No scheduled jobs.")
    for j in jobs:
        when = "daily " + str(j.get("scheduleValue")) if j.get("scheduleType") == "daily" else "every %s min" % j.get("scheduleValue")
        print("%-28s %-16s %-3s next %s" % (str(j.get("name"))[:28], when, "on" if j.get("enabled", True) else "off", j.get("nextDue", "")))
        print("    id %s   last run %s (%s) exit %s" % (j.get("id"), j.get("lastFiredAt") or "never", j.get("lastTrigger") or "-", j.get("lastExitCode")))
        print("    " + str(j.get("command")))


def cmd_newkey(_args):
    if os.path.exists(KEY_FILE):
        print(f"A key already exists at {KEY_FILE}. Its address:")
        print(_account().address)
        return
    Account, _ = _eth()
    acct = Account.create()
    key = acct.key.hex()
    with open(KEY_FILE, "w", encoding="utf-8") as f:
        f.write(key if key.startswith("0x") else "0x" + key)
    try:
        os.chmod(KEY_FILE, 0o600)
    except OSError:
        pass
    print(f"Key written to {KEY_FILE} (keep this file private; it is not shown here).")
    print("Add this address in Marcha: API, Allowed Addresses:")
    print(acct.address)


def cmd_address(_args):
    acct = _account()
    print(acct.address if acct else f"No key yet ({KEY_FILE}). Run: newkey")


def cmd_runs(args):
    data = api_get(f"/api/schedules/{args.job_id}/runs")
    runs = data if isinstance(data, list) else data.get("runs", [])
    for r in runs[:15]:
        print("%s  %-9s exit %-5s finished %s  (run id %s)" % (r.get("firedAt"), r.get("trigger"), r.get("exitCode"), r.get("finishedAt"), r.get("id")))
    if not runs:
        print("No runs yet.")


def cmd_debug_log(_args):
    data = api_get("/api/debug/log")
    entries = data.get("entries", [])
    if not entries:
        print("No log entries.")
        return
    for e in entries:
        ts = e.get("timestamp", "?")
        method = e.get("method", "?")
        path = e.get("path", "?")
        code = e.get("statusCode", "?")
        err = e.get("error")
        line = f"[{ts}] {method} {path} -> {code}"
        if err:
            line += f"  ERROR: {err}"
        print(line)


# --- Main ---

def main():
    parser = argparse.ArgumentParser(
        description="Marcha API CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Default: http://127.0.0.1:7832 (override with MARCHA_PORT env var)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("state", help="Full app snapshot")
    sub.add_parser("templates", help="List saved templates")
    sub.add_parser("reload", help="Re-read templates.json from disk (no restart)")
    sub.add_parser("tasks", help="List active tasks")

    p = sub.add_parser("task", help="Single task detail + log")
    p.add_argument("task_id")

    p = sub.add_parser("launch", help="Launch a template")
    p.add_argument("template_id")

    p = sub.add_parser("input", help="Send input to a running task")
    p.add_argument("task_id")
    p.add_argument("text", nargs="+")

    p = sub.add_parser("run", help="Start a stopped task")
    p.add_argument("task_id")

    p = sub.add_parser("stop", help="Graceful stop")
    p.add_argument("task_id")

    p = sub.add_parser("kill", help="Force kill")
    p.add_argument("task_id")

    sub.add_parser("layout", help="Current layout")

    p = sub.add_parser("assign", help="Assign content to a layout slot")
    p.add_argument("slot_index")
    p.add_argument("content_type", choices=["empty", "tasksList", "history", "terminal", "resources"])
    p.add_argument("content_id", nargs="?", default=None)

    sub.add_parser("history", help="Execution history")

    p = sub.add_parser("tasklog", help="Saved terminal log for a history entry")
    p.add_argument("history_id")
    p.add_argument("--tail", type=int, default=None, help="Show only last N lines")

    p = sub.add_parser("resources", help="CPU/memory stats for a task")
    p.add_argument("task_id")

    p = sub.add_parser("restart", help="Orchestrated restart (kill then start in order with delays)")
    p.add_argument("specs", nargs="+", metavar="TASK_ID[:KILL_WAIT[:START_WAIT]]",
                   help="Task specs. Waits in seconds. Example: abc123:5:10 def456:0:0")

    sub.add_parser("log", help="Debug request log (last 100 entries)")
    sub.add_parser("schedules", help="Scheduled jobs")
    sub.add_parser("newkey", help="Make a signing key and print its address")
    sub.add_parser("address", help="The signing key's address")
    p = sub.add_parser("runs", help="A scheduled job's recent runs")
    p.add_argument("job_id")

    args = parser.parse_args()

    commands = {
        "state": cmd_state,
        "templates": cmd_templates,
        "reload": cmd_reload,
        "tasks": cmd_tasks,
        "task": cmd_task,
        "launch": cmd_launch,
        "input": cmd_input,
        "run": cmd_run,
        "stop": cmd_stop,
        "kill": cmd_kill,
        "layout": cmd_layout,
        "assign": cmd_assign,
        "history": cmd_history,
        "tasklog": cmd_tasklog,
        "resources": cmd_resources,
        "restart": cmd_restart,
        "log": cmd_debug_log,
        "schedules": cmd_schedules,
        "runs": cmd_runs,
        "newkey": cmd_newkey,
        "address": cmd_address,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
