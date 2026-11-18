# Install

**For the assistant.** The user opened this folder and asked to be set up. Run this as a conversation, one step at a time, one question at a time. Don't dump the whole plan on them. Read `START_HERE.md`, `CLAUDE.md` and `wiki/workflow.md` first so you can answer their questions about the method.

The install has three parts. **Part 1** (the method and the dashboard) takes a few minutes and needs only Python. **Part 2** (`STACK.md`: marcha, a private assistant on PublicOS) is optional, bigger, and never required for Part 1 to work. **Part 3** (`TEAM.md`: a team of assistants that take turns) is for later, and only if they ask. Finish Part 1 completely before you mention the details of the others.

## Part 1: the method and the dashboard

### Step 0. How they will run it

Find out how the user is talking to you, and tell them the options in plain words:

- **The Claude desktop app, pointed at this folder.** Works: it reads the same `CLAUDE.md` and the same files. The easiest way to begin.
- **Claude Code in a plain terminal.** Works the same; nothing else to install.
- **Claude Code in the terminal inside VS Code.** What the people who made this kit use daily: the files sit next to the conversation, and you watch them change. Needs VS Code and the Claude Code command line (`claude`). Offer to walk them through installing both now or later; it is not needed today.
- If they want Part 2 later, the `claude` command line will be needed anyway (the PublicOS assistant runs it), so mention that once.

Don't push. Record what they chose in `wiki/tools.md` under "How I run this".

Ask one more thing here, because it shapes the rest of the interview: how do they like to be talked to (short answers or detail, one question at a time, which language)? Follow it from now on; step 7 writes it down.

### Step 1. Check Python

Run `python --version` (on Windows also try `py --version`; on macOS or Linux, `python3 --version`). You need 3.9 or newer. If it is missing, help them install it from python.org (tick "Add python.exe to PATH") and check again. Note in `wiki/tools.md` which command works on this machine (`python`, `py` or `python3`). If it is not `python`, replace `python` with it at the start of every command in `CLAUDE.md` (the dashboard command and the clock command), `wiki/tools.md`, `wiki/assistant/assistant.md`, `.claude/skills/open-thread/SKILL.md` and the troubleshooting lines at the end of this page, so that later conversations run commands that work.

### Step 2. The interview: their top nodes

Explain in two sentences what a top node is (a big area of life that threads hang under). Then ask what theirs are. Offer a starting set to react to rather than a blank page:

> Work · Health · Family (or Children) · Home · Money · Projects (the apps and tools you build) · Learning

Guidance for you:
- Four to seven is a good number. They can add, rename and merge later, and you should say so.
- Use their words. If they say "the kids", the node is "The kids".
- Ask about their mini apps: if they build things, a `Projects` (or `Apps`) node is worth having, with one thread per app later.

Propose a one-line `why:` for every node in one message (what lives under it) and let them correct; do not ask node by node. Then create `threads/<slug>/thread.md` from `threads/_templates/top_node.md`: slug lowercase with underscores (`the_kids`); `name:` and the `# ` heading are their wording; `status:`, `parent:`, `next:` and `closed:` stay empty; `opened:` is today. Top nodes need no changelog line of their own; step 7 writes one for the whole setup.

### Step 3. The first real threads

Ask: *"What are the two or three things on your mind right now?"* For each one:

1. Agree which node it belongs under and what it is called. They pick the name; propose names for all of them in one message and let them correct.
2. Create `threads/<slug>/thread.md` from `threads/_templates/thread.md` (the steps are in `.claude/skills/open-thread/SKILL.md`). Fill every header line: `name`, `parent` (the node's slug), `opened` (today), `why`, `next`, and `status`: `doing` when work can go on, `waiting-you` when the next move is theirs, `blocked` when it waits on someone else (a quote, an answer), `idea` when nothing has started. Write a two or three line Summary and the first tasks from what they told you. Mark what waits on them with `⏳`.
3. Create today's heading in `changelog.md` if it is not there (`## YYYY-MM-DD`, below the intro lines), then add a changelog line for the thread (see `wiki/workflow.md`, Changelog).

If something they mention is small ("call the plumber"), put it in `threads/chores.md` instead and explain the difference: `## <title>`, `status: todo` (use `waiting-you` only when it is stuck on an answer or a decision from them), `why:` one line (say which area it belongs to), then a line of detail if there is any. A chore needs no changelog line until it is done.

Stop at three. The point is to see the system work, not to empty their head on day one.

### Step 4. Start the dashboard

Have them run `python scripts/work_tree.py` from this folder in a second terminal, or start it yourself in the background, and have them open `http://127.0.0.1:8790/`. If you started it, say so, and write in `wiki/tools.md` that it is running and how to stop it: it has no terminal to close, so on Windows `netstat -ano | findstr :8790` gives the process id and `taskkill /PID <id> /F` ends it.

Check with `python scripts/work_tree.py --json` that every thread you made appears and `no_header` is empty. Then walk them through the page:

- **Tree**: their nodes, the threads under them, the "Waiting on you" filter. Click a row to see its summary.
- **Graph**: the same threads as dots and lines.
- **Activity**: it will be nearly empty today; it fills as the changelog grows.

Tell them how to start it again later (the command goes in `wiki/tools.md`), how to stop it (Ctrl+C in its terminal, or close that terminal), and that `--lan` makes it readable, with no password, by every device on the same network: the phone opens `http://<this PC's address>:8790/`, and Windows may ask to allow Python through the firewall.

### Step 5. Make it theirs, right now

Offer to change one thing with them so they see it is editable. If they would rather leave it as it is, say where the settings are and move on. The options:

- the page title (the `TITLE` line in `dashboard/index.html`, the first line under "yours to change"), for example "Ana's tree";
- a colour;
- a filter button of their own (the `FILTERS` list).

Then tell them, in your own words, the message from `START_HERE.md`: this is a base. They should keep moving things, ask for new charts, drop what they don't use, and look at the tree with you every week or two.

### Step 6. Backup

Ask where they keep backups and how often. This folder will hold things they can't recreate. Help them put it somewhere that is copied automatically (a synced folder, an external drive routine, a private git repository). A synced folder or a repository means a copy leaves this computer: say so, and let them choose. Write what they chose in `wiki/tools.md`. If they do not want to decide today, write "None yet" there and add a question to `wiki/assistant/notes.md` so it comes up again. If the folder is inside a cloud-synced directory, note that too.

### Step 7. Close the install

- Add a changelog line in the usual format, with the time from the clock and `[setup]` as the area (it spans every node): `` - `HH:MM` `[setup]` **NOTE** - Set up the tree: <the nodes>. ``  Do not link the first threads here; each already has its own line from step 3.
- Add the first lines to `wiki/assistant/notes.md` under "How the user likes to work": anything they said about that (short answers, a language, mornings only).
- Tell them the three sentences they need to remember: talk to me in this folder; I write things down as we go; open the dashboard when you want the big picture.

Then ask whether they want to hear about Part 2 now or another day.

## Part 2: the stack (optional)

Read `STACK.md` and follow it. In one breath, for the user: marcha is a small Windows app that keeps the dashboard and other programs running with one click; the PublicOS part gives them a private assistant they can message from their phone, running on their own PC, that answers nobody but them and can wake itself up on a schedule.

Do the pieces in the order `STACK.md` gives, and stop after any piece if they have had enough. Each piece is useful on its own. `MARCHA.md` is the follow-up: what else marcha is for (scheduled jobs, the nightly backup), and how an assistant on timers works by itself and stays quiet.

## Part 3: a team of assistants (optional, later)

Read `TEAM.md`. Only when the user asks for it and Part 2 has been working for a while: several assistants, each with its own inbox and character, woken on a schedule, each reporting to the user in its own chat. It costs model usage on every turn; say so before anything is installed.

## If something goes wrong

- **The page says "not connected"**: the script is not running. Start it again.
- **A thread is missing from the tree**: its folder has no `thread.md`, or the file does not start with the `---` header. `--json` lists such folders under `no_header` (the page does not show them).
- **"port 8790 is taken"**: the dashboard is probably already running; open the page. Otherwise `python scripts/work_tree.py --port 8791`.
- **The skills are not offered** (`open-thread`, `close-thread`): read `.claude/skills/<name>/SKILL.md` and follow it as a page.
- **Windows shows odd characters in the terminal**: harmless; the page itself is UTF-8.
