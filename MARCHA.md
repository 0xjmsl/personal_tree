# marcha, and an assistant that runs itself

**For the assistant.** `STACK.md` installs marcha and uses it to start three programs. This page is what else it is for, and how the people who made this kit use it every day together with timers, so that their assistant works on its own and speaks up only when it has something to say.

Nothing here is required. Take one idea at a time, agree it with the user, and write what you set up in `wiki/tools.md`.

## What marcha is

A Windows app that keeps the user's programs in one window. https://github.com/0xjmsl/marcha/releases

It does three jobs:

1. **Tasks.** Every program you start often is saved once and launched with a click, each in its own terminal that you can read and type into.
2. **Scheduled jobs.** Its own clock: run a command every day at a time, or every so many minutes, with no terminal open.
3. **A local API.** Other programs on the same PC, the assistant included, can ask marcha to start, stop, restart and read tasks.

## 1. Tasks: what you can set

The **+** button in My Tasks opens "New Template". Fill it and press Create.

| Field | What it is for |
|---|---|
| Task Name, emoji, Description | How it shows in the list |
| Command, Arguments | What runs (`python`, `scripts/work_tree.py`). Arguments are split at spaces: a path with a space in it will break, so use the Working Directory and a short relative path |
| Working Directory | The folder it runs in |
| Environment Variables | Values only this task sees (a port, a config path). Open the section, press "Add Variable", give a name and a value. This is how the daemon gets `XMTP_WEBHOOK_URL`. They are saved as plain text: no passwords here |
| `{{placeholders}}` | Write `{{name}}` in the command, an argument or a variable, and marcha asks for the value each time you launch **from the window**. Launched through the API it is not asked and `{{name}}` is passed as written, so keep placeholders out of tasks the assistant starts |
| Automation Steps | "Wait until the terminal shows this pattern, then type that and press Enter." For programs that ask a question at start. The pattern is a regular expression: use a plain word from the prompt, or escape `? ( ) [ ] .`. A step gives up after 30 seconds unless you change its timeout. Saved as plain text: **never a password** |

Around the tasks:

- **Quick Actions**: emoji buttons on a task's terminal that type a command you use often. Add one with the + on the terminal's header while the task is open.
- **Groups** with **Run All**: the dashboard, the daemon and gpette start together.
- **Layouts**: several terminals side by side; drag the dividers.
- **History**: every run with its start, end and status; "View Log" opens the saved output of a run that has ended.
- **Stop** sends Ctrl+C; **Kill** ends the program and everything it started.
- A task is a terminal that the command was typed into. If the program inside crashes, the terminal stays open with the error on screen, and the task still shows as running. So "running" means the terminal is open, not that the program is alive.
- Settings, Startup, **Start Marcha with Windows**: marcha comes back after a reboot. It does not start yesterday's tasks again by itself; scheduled jobs do run (below). It remembers where its `.exe` was: if you move marcha's folder, switch this off and on again.

What we keep there: the dashboard of our tree, the assistant's two programs, local servers while we work on them, and one-click tasks for things we do often (a deploy, a build, opening a remote machine).

## 2. Scheduled jobs: marcha's own clock

**Scheduled** in the left bar, then **New**. A job is a Name, a Command, a "Working directory (optional)", and either "Daily at" (HH:MM, 24-hour) or "Every (min)". Save. The pencil edits a job (Delete is inside that dialog); the arrow shows its runs, and a click on a run shows its output.

- The command is one line, run by Windows' `cmd`. It has no window.
- Every run is recorded: when, why (`schedule`, `manual`, `catch-up`), the exit code and the output. The last 30 runs of each job are kept. An exit code other than 0 shows as a failed run.
- **Catch-up:** if the PC was off or marcha was closed at the time, the job runs once when marcha is next up. Five missed nights make one run, not five.
- One copy at a time: if a job is still running at its next time, that run waits and starts once, right after the current one ends.
- Each row has an on/off switch and a run-now button.

Use it for anything that needs no thinking, because it costs nothing to run:

- **Backups.** Ours copies our own tree to another disk every night at 03:00. This is the best first job for this kit. Ask the user where the copy should go, then, as the Command (one line; change the two folders and the log's place):
  ```
  robocopy "C:\Users\ana\Documents\my_tree" "E:\backup\my_tree" /E /R:1 /W:1 /NP /LOG+:"E:\backup\backup.log" & if errorlevel 8 (exit /b 1) else (exit /b 0)
  ```
  The ending matters: `robocopy` reports "files were copied" with a code that marcha would show as a failure; this turns real errors into 1 and everything else into 0. It adds and updates files and never deletes from the copy. When it has run once, update "Backup" in `wiki/tools.md` and remove the open question about backups from `wiki/assistant/notes.md` if there is one. The assistant's two key files live in the daemon's folder (`STACK.md`, 3a), not in the tree: back those up separately, with the user.
- Exports and downloads on a schedule (a bank export, a calendar file).
- A small check that writes its result to a file: is a disk full, did a website change, is a document due.

**How to know it worked:** the run's record says it fired. The copy on the other disk proves it worked. Check the proof, not only the record, the first few times.

## 3. The local API: the assistant can drive marcha

**Security first: use signed requests.** The API can do what the user can do in marcha's window: start saved tasks, type into a running terminal, create a scheduled job that runs any command. By itself it has no password, so anything on this PC could use it. We recommend, and use ourselves, **signed requests**: marcha then answers only requests signed by a key the user has allowed, and nobody else.

Use marcha **1.0.1 or newer**. Older builds also answered web pages open in a browser on the same PC; 1.0.1 refuses those always, signed or not.

Set it up in this order, with the user:

1. `pip install eth-account` (the one package signing needs), then `python scripts/marcha.py newkey`. It makes a key file in the user's home folder (`.marcha_api_key`; it never leaves the PC and is not shown) and prints an address.
2. In marcha: **API** in the left bar. Paste that address under **Allowed Addresses**. Then the switch under Server; it reads "Running on 127.0.0.1:7832".
3. `python scripts/marcha.py tasks` must answer. Then prove the lock: rename the key file for a moment and run it again; it must be refused ("signed requests only"). Put the file back.
4. In the same screen's **Endpoints** list, switch off what you will not use.

Tell the user what was turned on and why, and write in `wiki/tools.md` where the key file is (the place, not the content). The key is only for marcha; it is not an account anywhere. If the file is lost, make a new one and swap the address.

Leave the API off if nothing uses it. Everything else on this page works without it.

The kit's command for it is `scripts/marcha.py`. Once a key exists it signs every request by itself:

```
python scripts/marcha.py templates              the saved tasks and their ids
python scripts/marcha.py tasks                  every open task with its status and id
python scripts/marcha.py task <id>              one task and the end of its terminal output
python scripts/marcha.py history                past runs
python scripts/marcha.py tasklog <history id> --tail 50      the saved output of an ended run
python scripts/marcha.py schedules              the scheduled jobs: next fire, last run and its exit code
python scripts/marcha.py runs <job id>          a job's recent runs
python scripts/marcha.py launch <template id>   start a saved task
python scripts/marcha.py stop <id>              Ctrl+C
python scripts/marcha.py kill <id>              end it and what it started
python scripts/marcha.py input <id> "text"      type into its terminal
python scripts/marcha.py restart <id>:<seconds to wait after ending it>:<seconds to wait after starting it> ...
python scripts/marcha.py newkey                 make the signing key (once); prints the address to allow
python scripts/marcha.py address                the address of the signing key
```

What this gives the assistant:

- **It can look before it asks.** `tasks` shows what is open; `task <id>` shows the end of a terminal, where a crash leaves its error. For a server, "is it up?" is answered by the server itself (the dashboard: does `http://127.0.0.1:8790/` answer?), not by the word "running".
- **It can check the night's jobs**: `schedules` shows each job's last run and exit code.
- **It can restart its own programs.** The assistant that the user messages from the phone runs inside gpette; after a change to gpette's config it has to restart the very program it is running in. The way we do it, **with the user's go for that restart**: first set a one-minute timer for itself ("you were restarted; check that you are back and tell the user"), then `restart <daemon id>:2:5 <gpette id>`. marcha ends both in that order (it kills them, there is no Ctrl+C), then starts both again from their saved tasks, with the waits given. The reply of the turn that asked for the restart never arrives, because that turn dies with gpette; the timer's message is the one the user sees.
- Take the ids from `tasks` every time: a restarted task is a new task with a new id. Write task **names** in `wiki/tools.md`, not ids.

Rules:

- The key file lets whoever holds it drive marcha. It stays in the user's home folder, out of this tree and out of anything synced or shared.
- Launch, input, stop, kill and restart change what is running: get the user's go, unless they have told you a specific one is always fine (write that in `wiki/tools.md`).
- Creating or changing a scheduled job is done with the user, in the Scheduled screen.

## 4. Timers: an assistant that wakes itself up

This needs the private assistant of `STACK.md` (gpette and the daemon). A timer there is different from a marcha job:

| | marcha scheduled job | gpette timer |
|---|---|---|
| What fires | A command | The assistant, with instructions you wrote |
| Cost | Nothing | One model run each time |
| Good for | Copying, exporting, checking a number | Anything that needs judgement or words |
| Where the result goes | A file, a log | A message to the user's phone, or nothing |
| After the PC was off | One catch-up run | One fire for **each** turn it missed, a minute apart: a daily timer once per missed day, an every-N-minutes timer once per missed interval |

What a fire reports travels, encrypted, as a message to the user's phone. If it reports on the tree, things from the tree leave this PC that way: agree that with the user once and record their go.

### Set it up

1. **Fill in `wiki/assistant/assistant.md` first.** The kit ships it as a template: the page that says what a fire is for. Go through it with the user and make it theirs. A fire starts with no memory; this page and the notes are all it knows.
2. Have the user ask the assistant on the phone to set one timer, in the quoted forward-slash form of `STACK.md`, 3h (example paths):
   ```
   "C:/Tools/gpette/.venv/Scripts/python" "C:/Tools/gpette/scripts/timer.py" set "Morning look" "Read wiki/assistant/assistant.md and do what it says for this fire." --time "8 AM" --type recurring --skip-session
   ```
3. When it fires, the assistant gets `Timer fired:` plus those instructions. If its whole answer is `[NO_REPLY]`, nothing is sent. That one rule is what makes a frequent timer bearable.

To change it later: `timer.py list --all`, `timer.py cancel <id>`, and set it again with the new time. (`timer.py edit <id> --time 120` on a repeating timer changes how often it fires.) To silence every repeating timer for a while without losing them: the user sends `/menu` to the assistant, Timers, "Pause all" (a one-time timer that comes due during the pause is lost).

### How we run ours

One timer that fires through the day. Each fire is short and usually silent. Our page is the template in `wiki/assistant/assistant.md`: what needs the user, the night's jobs, one piece of quiet work, one question, and otherwise `[NO_REPLY]`.

During any conversation the assistant drops a line in `wiki/assistant/notes.md` instead of interrupting; the timer picks those up later, one at a time.

What we learned running it:

- **Quiet is the default.** An assistant that reports every fire gets muted in a day.
- **Re-read the page every fire.** A fresh session (`--skip-session`) remembers nothing of the last one.
- **One thing per fire.** Small steps, each logged in the changelog like any other work.
- **Never anything that cannot be undone.** A timer turn has nobody watching. It reads, writes notes and drafts; it does not send, pay, delete or publish. Those wait for the user.
- **Start slow.** One fire a day, in the morning. Add a second clock time when the first one is useful. Prefer clock times to "every N minutes": they are easy to reason about and pile up far less after the PC was off (one fire per missed day, against one per missed interval). Every fire costs a model run; tell the user what a day costs.
- **Change the rhythm when life changes.** A user on holiday does not need a loop: pause it from `/menu`.

### The two clocks together

The pattern we use most: **the cheap clock does the work, the thinking clock reads the result.**

- A marcha job runs the backup at 03:00. The assistant's morning fire looks at its last exit code and says nothing unless it failed.
- A marcha job downloads the bank export on the 1st. The assistant's next fire sorts it into the Money threads and asks about the three lines it could not place.
- A marcha job checks a web page every hour and writes "changed" to a file. The assistant tells the user what changed, in words.

For the second and third, the job must leave a file. Write in `wiki/assistant/assistant.md` which file each job leaves and where.

## Where to go next

- A team of assistants on timers: `TEAM.md`.
- Tasks and steps in more detail: marcha's README. The API's full list: the Endpoints section of marcha's API screen.
