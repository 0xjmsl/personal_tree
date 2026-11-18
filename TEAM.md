# A team of assistants (optional)

**For the assistant.** Part 3 of the install. Do it only when the user asks for it, and only after Part 2 (`STACK.md`) works: one private assistant answering the user from their phone. A team is the same pieces, repeated and put on a schedule.

What it is: several assistants, each with its own inbox, its own folder and its own character, each woken on a timer to do a piece of work and send the user a short report. The people who made this kit run ten of them this way. Their ten have accounts on PublicOS, belong to one org there, and work in public; their owner reads ten short chats.

Tell the user plainly before you start:

- **It costs model usage on every turn**, whether or not anything useful happened. Ten assistants taking a turn every three hours is eighty runs a day.
- **Start with two or three**, on a slow schedule. Add more when the reports are worth reading.
- A team needs a clear job. "Be useful" produces noise. Agree the job in one paragraph first, and write it down.
- **Their reports travel as messages.** If the team reads this tree, what is in the tree (health, money, family) will appear in reports that leave this PC, encrypted, to the user's phone. That is the user asking for it to leave the computer; record the go in the team's thread.

## What you need

| Piece | Where | Read |
|---|---|---|
| marcha | https://github.com/0xjmsl/marcha/releases | `STACK.md` piece 1, `MARCHA.md` |
| xmtp_daemon, the bridge to the messaging network: one running copy per assistant | https://github.com/0xjmsl/xmtp_daemon | its README, "Several inboxes on one machine" |
| gpette, the one brain behind all of them | https://github.com/0xjmsl/gpette | `SETUPS.md`, setups 4 and 6; README, "Several inboxes" and "Timers" |
| The PublicOS guide for agents, if the team will act on PublicOS | https://publicos.dev/agents | "Get an account", then the skills the job needs |

Those pages own the details and are kept up to date with the code. This page is the order to do things in, the exact blocks for this kit, and the way to run the team afterwards.

## 1. Design the team with the user

One conversation, written into a new thread in this tree (`threads/<slug>/thread.md`; the user picks the name and the area it hangs under). Add two sections to that thread besides the usual ones: `## The design` (the points below, with the member table) and `## Log` (dated lines: what was changed and why).

- **The job**, in one paragraph. What they do, what they must never do, what a finished turn looks like.
- **The members.** A short id, a name and two lines of character each. Different characters are the point: one that checks, one that organizes, one that doubts, one that writes things up. A team of identical assistants agrees with itself.
- **The schedule.** At which times each one takes a turn.
- **What they may touch.** The default is: their own folder and one notes file. Nothing of the user's. See "A team that reads this tree" below for the obvious first job.
- **Where they act.** Only in their reports to the user, or also in public on PublicOS. The second needs accounts (step 5).

## 2. Folders

A folder of its own, not inside this tree and not inside gpette's folder; anywhere under the user's own profile folder (for example `C:/Users/ana/team`), so that only their login reads it:

```
team/
  setup/base.md              the shared brief: the job, the rules, what a turn is, how a report looks
  setup/personalities.json   {"checker": {"name": "Checker", "character": "two lines"}, ...}
  setup/build.py             writes every agents/<id>/CLAUDE.md
  setup/sync_tree.py         only for step 4: refreshes every agents/<id>/tree/
  agents/<id>/CLAUDE.md      that member's character + base.md (built, never edited by hand)
  agents/<id>/notes.md       its memory; the only file it may write
  daemons/<id>/              that member's xmtp_daemon folder: its secrets/ and its database
```

- The kit does not ship `build.py` or `sync_tree.py`. You write them: 20 to 40 lines each, Python's standard library only.
- **The daemon's folder is not the member's folder.** A member may read everything in `agents/<id>/`; its key must not be there.
- `build.py` writes each `CLAUDE.md` from the member's character and `base.md`, and creates `notes.md` only if it does not exist. It must never overwrite `notes.md`. Changing the team's instructions is then: edit `base.md`, run `build.py`.

What belongs in `base.md`:

- Who they are and who the user is to them. The other members' names, if they should know of each other.
- The job and the limits.
- **How a turn goes:** read `notes.md`, see what changed since last time, do your piece of the job, update `notes.md`, end with the report.
- **The report:** a few lines: what I found, and what the user should look at. Last, and only if it applies: what I am missing to do my job (a file, a permission). If there is nothing to report, one line saying so.
- That `notes.md` is all they will remember next turn.
- If the team reads this tree (step 4): that the copy is in `tree/`, that `tree/SYNCED.txt` says how old it is, and that every report ends with the copy's date.

**If the team reads this tree, do step 4 now**, before the first test turn; a member tested without its copy reports that there is nothing to read.

## 3. Wire it

Do one member end to end (3a to 3e) before you make the second.

### 3a. One daemon per member

Each from its own folder, each with its own port, all pointing at the one gpette. Create the folder first and check the port is free. PowerShell:

```
mkdir <team folder>\daemons\checker
cd <team folder>\daemons\checker
$env:XMTP_HTTP_ADDR = "127.0.0.1:3111"
$env:XMTP_WEBHOOK_URL = "http://127.0.0.1:4849"
& "C:\Tools\xmtp_daemon\xmtp_daemon.exe"
```

The next member gets `3112`, and so on. `Invoke-RestMethod http://127.0.0.1:3111/health` shows that member's `address` and `inboxId`. Each `daemons/<id>/secrets/` holds that member's key: back them up with the user, never print them. On Windows these are ordinary files, which is why the team folder sits inside the user's own profile folder.

In marcha: one task per daemon (working directory = `daemons\<id>`, the two environment variables, command = the full path of `xmtp_daemon.exe`), in a group of their own, "Team". After the first start from marcha, check each `/health` still shows the same `inboxId`; a different one means the working directory is wrong. gpette reads each daemon when it starts, and again when needed, so the order inside the group does not matter.

### 3b. Add the team to the gpette of Part 2

The same `gpette.toml`, the same running gpette. Leave `[daemon]`, `[gate]`, `[server]` and `[profiles.owner]` as they are, and add, **one member at a time** (the second member's two blocks when you reach the second member; each addition is a gpette restart):

```toml
[inboxes.checker]
url = "http://127.0.0.1:3111"

[profiles.checker]
inbox = "checker"
members = ["<the user's inbox id>"]     # the same id as in [profiles.owner]
gate = "open"
provider = "claude-code"
model = "haiku"                          # a small model is enough for a scheduled look; leave the line out for the default
workdir = "C:/Users/ana/team/agents/checker"   # REPLACE with the real path; forward slashes
allowed_tools = ["Read(./**)", "Glob(./**)", "Grep(./**)", "Edit(./notes.md)", "Write(./notes.md)"]
sessions = "fresh"                       # every turn and every reply starts from the current brief
max_turns = 25                           # enough for a look through a small tree
timeout_secs = 300                       # a stuck member holds up everyone else until this passes
```

- `Read(./**)` keeps a member inside its own folder; a bare `Read` can read any file on the PC.
- No `Bash` unless the job needs exactly one command of yours; then `"Bash(yourcommand *)"` and nothing wider (gpette's setup 6).
- Once `[inboxes]` exists, gpette's log warns each time a message arrives at the main assistant's inbox ("not in [inboxes]"). That is expected; the main assistant keeps working as before.
- With several inboxes, the admin page's "who would handle this?" box does not know which inbox a message arrives at and answers `owner` for the user's id whichever member they write to. Trust the member's actual reply in 3c, not the box.
- Restart gpette. Its log names each inbox with its id; a profile that names an inbox that is not listed stops it with a clear message.

### 3c. The user writes to each member first

A timer can only be set in a chat that has had a message. So: give the user each member's `address` (from its `/health`); they start a chat with that address in the PublicOS app and send one word. The first message from a new sender may arrive on their side as a request to accept. Each member should answer as itself, in its own chat. That answer is a model run, and so is every later reply of the user to a report: the cost is not only the scheduled turns.

Then, in the gpette folder, with gpette's Python:

```
.venv\Scripts\python scripts\timer.py conversations
```

lists the chats and their ids. It does not say which member a chat belongs to: `data\conversation_inboxes.json` in the gpette folder maps each chat id to its inbox name.

### 3d. Test one turn now

Do not wait for the schedule to find out. (If the team reads the tree, run `sync_tree.py` once first.) A one-shot timer two minutes ahead, with the instruction every turn will have:

```
.venv\Scripts\python scripts\timer.py set "checker test" "Your turn. Read notes.md, see what changed since your last turn, do your piece of the job, update notes.md, and end with your report." --time 2 --skip-session --conv <checker's conversation id> --profile checker --owner <the user's inbox id>
```

When it has fired: the report is in the user's chat with that member; `agents/checker/notes.md` has changed and nothing else has; and `data\logs\app.log` in the gpette folder has a `run summary` line for it with `cost_usd=`. Read the report with the user. This is the moment to fix the brief.

`--conv` decides where the report goes. Another member's chat is refused ("this chat belongs to inbox ..."), but not every wrong chat is: take the id from `conversation_inboxes.json`, and check the first report arrived where you meant.

### 3e. The schedule

The same command with `--type recurring`. Use **clock times** (the PC's local time), which repeat daily, and one timer per turn of the day; that is how members end up apart from each other:

```
... set "checker 08:00" "<the instruction>" --time "08:00" --type recurring --skip-session --conv <id> --profile checker --owner <inbox id>
... set "checker 20:00" "<the instruction>" --time "20:00" --type recurring --skip-session --conv <id> --profile checker --owner <inbox id>
... set "nudger 11:00"  ...  --profile nudger ...
```

(`--time 360` means every 360 minutes starting 360 minutes from now. Two such timers set together fire together, and `timer.py edit --time` changes the interval, not only the next fire. Clock times avoid both.)

`timer.py list --all` shows every timer; `timer.py cancel <id>` ends one. gpette runs one turn at a time for the whole team: keep turns apart by more than a turn takes.

## 4. A team that reads this tree

The obvious first job for this kit ("tell me what is stale, what waits on me"). Members must not work inside the tree: they would read everything and could be given tools that change it. Give each member a **read-only copy** instead:

- A small script (`team/setup/sync_tree.py`, which takes the tree's path as its argument) rebuilds every `agents/<id>/tree/` from scratch: every open thread's `thread.md`, plus `changelog.md` and `threads/chores.md`, and the time of the copy in `SYNCED.txt`. Leave out `threads/_templates`, `threads/_done`, `threads/_dropped` and every thread's `files/` folder (exports and drafts: large, and often the most private things in the tree) unless the user wants them in.
- Have it run **every hour** as a marcha scheduled job (`MARCHA.md`, section 2). Scheduled jobs are created with the user in marcha's Scheduled screen; give them the line to paste as the Command, with real paths: `py "C:/Users/ana/team/setup/sync_tree.py" "C:/Users/ana/Documents/my_tree"` (or `python`, whichever works on this machine). A member whose copy is old will report old news, which is why every report ends with the copy's date; after the PC was off, the first report may still read the old copy.
- The member can read the copy and write only its `notes.md`. The tree itself is never touched by the team; what they suggest, the user or the main assistant does.

Tell the user again what this means: whatever is in those threads can show up in a report.

## 5. Accounts on PublicOS (only if the team acts there)

Read "Get an account" in the agents guide and follow it one member at a time.

- Words used here, all defined in the guide: an account is *private* until its holder is verified as a person; a verified one is a *citizen*. An org is a shared account with members.
- Each member is its **own account**, made from **its own account key**, and **marked as automated**. An account run by software says so on its profile; that is a rule of the network, not a suggestion. The account key is a separate key made by the guide's steps; it is not the daemon's key in `daemons/<id>/secrets/`. The guide says how a member's inbox is then linked to its account.
- The transaction that creates an account is sent by a verified member (a citizen). If the user is one, they send it, after the member has signed its consent with its own key. If not, each member uses the public sign-up door the guide describes (it needs one e-mail address per account).
- An automated account is never a citizen. So a team's org is a **private org** (the guide's org pages say how one is made and joined); a public org takes citizens only.
- A new private account's name needs seven characters or more. If the guide's name check passes and the creation is still refused for the name, that is why.
- Do this after step 3 works: first a team that reports, then accounts.
- Whoever sends a transaction pays its fee; a member's own actions are paid from that member's account, so each account needs a small balance. The guide says what things cost.
- **Keys stay on the machine that runs the team**, one file per member, outside every `agents/<id>/` folder. Members never read key files. Instead they get one command: a small script of yours that takes the name of one of the guide's scripts and its arguments, refuses anything not on a fixed list, loads the key of the member whose turn it is (gpette sets `GPETTE_PROFILE` to the member's id) and runs it. Put the wrapper on the PATH under one short name and allow only that command in the profile (`"Bash(yourcommand *)"`); the guide's scripts need Node.js. Add this to the list of commands that must be refused, and try it: `GPETTE_PROFILE=<another member> yourcommand ...`, a member trying to act as another. If it runs, change the wrapper so it does not trust that variable.
- **The fixed list is the limit.** A rule written in `base.md` is a request; the list in the wrapper is what actually stops a member. Leave off it anything that creates accounts, changes keys or moves more than small amounts, and agree the list with the user.

## 6. Running the team

This is the part that matters after the first day.

- **Read the reports.** Early reports show what the brief did not say. Fix `base.md`, run `build.py`; with `sessions = "fresh"` and `--skip-session` the next turn starts from the new brief.
- **One change at a time.** Change the brief, wait a full round, read the reports, then change the next thing.
- **Test a new ability before the team gets it.** Run each new command the way a member would, including the ones that must be refused. Keep the list of expected refusals in a file and compare after every change.
- **Ask before you act on a request.** Members will ask for files, data, pictures, more permissions. Each request goes to the user first.
- **Pausing.** Two ways, tell the user both:
  - Quiet for a while, everything still running: the user sends `/menu` to their own assistant (the owner profile is `admin`), Timers, "Pause all". It pauses **every** timer of this gpette, the main assistant's own included. Repeating timers keep their schedule and skip the fires that fall in the pause; a one-time timer that comes due during a pause is lost.
  - Team off, main assistant on: pause or cancel the team's timers, then stop the Team group in marcha (the member daemons). Stopping gpette itself stops the main assistant too.
  - After gpette has been **stopped**, a repeating timer fires once for each turn it missed, one a minute, when gpette comes back: an every-N-minutes timer once per missed interval, a daily one once per missed day. If gpette was off for more than a day, look at `timer.py list --all` before starting it, and cancel and set again what would pile up.
- **Reports are also written to disk.** The daemon's and gpette's logs, and marcha's saved terminal output, contain the text of messages. They stay on this PC, but the user should know the reports are not only on the phone.
- **Watch the cost** for the first week: add up the `cost_usd=` of the `run summary` lines in gpette's `data\logs\app.log`, and tell the user what a day costs.
- **Keep the record here.** The team's thread holds the design, the member table, the decisions and the log. `wiki/tools.md` gets a "The team" section: the folders, the ports, the marcha group, the timers and their times, where the key backups are (the place, not the content), how to pause and how to restart.

## What it can't do

- Members do not hear each other unless you give them a place to talk: a shared group chat (pace it, see gpette's README on group chats, or they answer each other forever) or, as the makers of this kit chose, public posts on PublicOS that everyone can read. Do not have two members write to each other directly in a one-to-one chat; gpette keeps one owner per chat.
- One turn at a time across the whole team. A member that takes long delays the next.
- The PC must be on. A small always-on machine is the usual next step; the same folders move as they are (gpette's and the daemon's pages have the Linux forms).
