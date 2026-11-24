# The stack (optional)

**For the assistant.** Part 2 of the install. Everything here is optional. Pieces 1 and 2 stand on their own; 3 needs a way for the user to message it (2, or any other XMTP app) and uses 1 to keep it running. Do them in this order and check each one works before the next. Explain to the user what a piece is for before you install it.

| Piece | What it gives them | Needs |
|---|---|---|
| 1. marcha | One window that starts and shows the dashboard and the other programs | Windows |
| 2. A PublicOS account | Their own identity on the network, and the phone app | A phone |
| 3. The private assistant | They message their assistant from the phone; it works in this folder on their PC | 2 (or another XMTP app), the `claude` command line, Python 3.11+, Git for Windows; 1 recommended |
| 4. PublicOS skills | Their assistant can read and post on PublicOS for them | 2 |

Record every choice, path and port in `wiki/tools.md` as you go (never a key or a password).

## 1. marcha

A Windows task launcher: it keeps long-running programs in one window, each in its own terminal, and starts them with one click.

1. Download the newest `marcha-windows-x64-*.zip` (1.0.1 or newer) from https://github.com/0xjmsl/marcha/releases and unzip it somewhere permanent (for example `C:\Tools\marcha`).
2. Run `marcha.exe` (it is in the `marcha` folder inside the zip). Windows may show a SmartScreen prompt because the build is not code-signed: "More info", then "Run anyway".
3. With the user, add a task for the dashboard (the **+** button in My Tasks):
   - Name: `My tree`
   - Command: the Python command that works on this machine (`python` or `py`)
   - Arguments: `scripts/work_tree.py` (add `--lan` if they want it on their phone)
   - Working directory: this folder
4. Run it and open `http://127.0.0.1:8790/`.
5. Optional: Settings → Startup → *Start Marcha with Windows*.

Later pieces add two more tasks (the daemon and gpette). Put the three in one group so "Run All" starts everything.

marcha does much more than start three programs: scheduled jobs (a nightly backup of this folder is the best first one), a local API the assistant can use to look at and restart tasks (with signed requests, which we recommend), and the way it pairs with the assistant's own timers. Read `MARCHA.md` once the stack works, and offer the user the ideas there one at a time.

## 2. A PublicOS account for the user

PublicOS is a social network where each person holds their own account and keys. Messages there are end-to-end encrypted (they travel over XMTP).

- The public guide for agents, https://publicos.dev/agents, explains how to find an account by its exact name and read a profile, with no key needed. Use it for every lookup here.
- **Ask first whether they already have an account.** If they do, ask for its **name**, look it up, and confirm with the user that the profile you found is theirs before you rely on it.
- **If they do not:** they install the PublicOS app on their phone (the links are at https://publicos.dev/library/get-publicos/) and create their account in it.
- Words you will meet: every account starts *private*; a private account whose holder has been verified as a real person (other citizens vouch for them) becomes a *citizen*. A citizen can create accounts for others; that matters in 3a, for the assistant's own account. Find out from the chain whether the user is one, as the guide shows, not by guessing.
- **PublicOS is not required for the messaging itself.** The assistant's inbox is a plain XMTP address, so any XMTP app can write to it. We use the PublicOS app; if the user prefers another XMTP app, skip to piece 3 and have them start a direct message to the assistant's address from that app.
- **The recovery words of the account are theirs alone.** Never ask for them, never store them, and tell the user to write them on paper.

You need one thing from this step for piece 3: the user's **inbox id**, the identifier their messages come from. Step 3e shows the simplest way to get it.

## 3. The private assistant

Two small programs run on the user's PC:

```
 the user's phone  <-- XMTP -->  xmtp_daemon  <-- local -->  gpette  -->  claude, working in this folder
```

- **xmtp_daemon** is the bridge to the messaging network: it keeps one inbox online, the assistant's. https://github.com/0xjmsl/xmtp_daemon
- **gpette** decides who gets answered and runs Claude for them. https://github.com/0xjmsl/gpette

Read both READMEs before you start (in gpette's: how a message is routed, profiles, gates, `/menu` and timers; in the daemon's: running it and where it keeps its key). Their `AGENTS.md` files and gpette's `docs/manual.html` are for when something does not behave as described here, or the user wants more than this page sets up. What follows is the shape for this kit, not a replacement for them.

### 3a. The assistant gets its own identity

The assistant is not the user. It has its own inbox, made from its own key, which the daemon creates on its first run (`secrets/bot.key`, with `secrets/db.key` for its database). **Both files are secrets: back them up with the user, and never print them.**

If the user wants the assistant to have a PublicOS profile too (a name and a robot badge, so it shows up as a contact): that is a second account, its own, and it **must be marked as automated** (the record `automated_account` = `true` on its profile, written before it does anything else; the guide's `record.js automated` does it). The agents guide ("Get an account") has the exact steps and two ways to do it. If the user is a citizen: the assistant signs a consent with its own key and the user sends the transaction from their own account (the guide's "from a citizen" route). If not: the public sign-up door the guide describes, which needs an e-mail address and makes one account per address. Work through the guide together, one step at a time, and tell the user what each signature does before anything is signed. If something in the guide does not match what you see, stop and tell the user exactly where. It works without a profile as well: the user can message the assistant's address directly.

### 3b. Install

1. The Claude Code command line: `claude --version` must work in a terminal. If not, install it with the user (https://claude.com/claude-code) and sign in.
2. Python 3.11 or newer.
3. Git for Windows (https://git-scm.com/download/win). Claude Code on Windows runs its commands in Git Bash, so the assistant on the phone needs it (3h relies on it). `git --version` must work.
4. **xmtp_daemon**: use the downloadable build from its releases page, https://github.com/0xjmsl/xmtp_daemon/releases (`xmtp_daemon-windows-x64-*.zip`). Unzip it into its own permanent folder outside this one, for example `C:\Tools\xmtp_daemon`. Keep the `.dll` files beside the `.exe`. If there is only source, building needs Rust and, on Windows, Strawberry Perl, and takes several minutes: tell the user before you start.
5. **gpette**: download or clone it outside this folder (https://github.com/0xjmsl/gpette), for example `C:\Tools\gpette`. Give it its own Python environment, so nothing is installed system-wide:
   ```
   cd <gpette folder>
   python -m venv .venv          (the Python command noted in wiki/tools.md: python or py)
   .venv\Scripts\python -m pip install -r requirements.txt
   ```
   From here on, "gpette's Python" means `<gpette folder>\.venv\Scripts\python`. Use it for `main.py`, for the test scenario, for the marcha task and for `scripts/timer.py`.

### 3c. Start the daemon and note the assistant's address

**Always start the daemon from its own folder.** It keeps its key in `secrets/` and its database in the folder it is started from; started from another folder it silently makes a new key, which is a new address and a new inbox.

PowerShell:

```
cd C:\Tools\xmtp_daemon
$env:XMTP_WEBHOOK_URL = "http://127.0.0.1:4849"
.\xmtp_daemon.exe
```

(In the old `cmd` window the second line is `set XMTP_WEBHOOK_URL=http://127.0.0.1:4849` and the third `xmtp_daemon.exe`. In PowerShell `set` does not set it, and the daemon then runs without telling gpette anything: the assistant never answers and nothing says why.)

Check, in a second PowerShell window: `Invoke-RestMethod http://127.0.0.1:3100/health` answers with the assistant's `address` and `inboxId`. (In Windows PowerShell, plain `curl` is something else and fails; use `Invoke-RestMethod` or `curl.exe` for every check on this page.) Write the address in `wiki/tools.md`; the user needs it to write to the assistant. On a first start the log shows lines such as `no codec attached to db` and `Skipping already processed intent`; they are harmless. `lastStreamEventMs` stays 0 until the first message arrives.

### 3d. Configure gpette: private, owner only

**The rule: this assistant answers the user and nobody else.** It will have tools and the user's files. An open bot here would hand those to any stranger who messages it.

Copy `gpette.example.toml` to `gpette.toml`. **Change these keys where they already are in the file** (do not paste the block below on top: the same section twice is an error), and add only `[profiles.owner]` at the end:

```toml
[daemon]
url = "http://127.0.0.1:3100"      # the daemon of 3c

[server]
host = "127.0.0.1"                 # never anything else
port = 4849                        # the port the daemon's XMTP_WEBHOOK_URL points at

[llm]
provider = "claude-code"

[claude_code]
inherit_user_settings = false      # keep false
groups = "sandbox"                 # see the note on groups below

[gate]
kind = "none"                      # nobody is answered...

[profiles.owner]                   # ...except this profile
members = []                       # the user's inbox id goes here in 3e
gate = "open"
provider = "claude-code"
workdir = "C:/Users/ana/Documents/my_tree"    # REPLACE with this folder's real path. Forward slashes: "C:\Users\..." stops gpette at start
allowed_tools = ["Read", "Glob", "Grep", "Bash", "Edit", "Write"]
privacy = false                    # the owner may be told file names and paths; without it the assistant refuses its own user
sessions = "shared"
menu = true                        # /menu: status, model, sessions, pause the timers (MARCHA.md and TEAM.md use it)
admin = true                       # other profiles may wake this one; grants nothing else
```

- **Never** set `[gate] kind = "open"`, and never add an inbox to `members` that the user did not give you themselves. If they later want a friend or a partner to reach the assistant, that is a separate profile with its own folder and no tools; read gpette's manual.
- **Groups:** other people's messages in a group chat are refused. The owner's own messages in a group still reach the owner profile, tools included, and the answer goes to everyone in that group. Tell the user: do not add the assistant to a group chat.
- Because `workdir` is this folder, the assistant on the phone reads the same `CLAUDE.md` and works on the same tree. Leave the top-level `[claude_code] workdir` as it is in the example file.
- This profile can read and change any file on the PC (bare `Read`, `Bash`), the daemon's key and `gpette.toml` included. That is why it must answer only the user, and why the backup of the keys belongs somewhere else.
- gpette ships a test of this shape. Run it once, from the gpette folder, so the user sees it (it costs a cent or less): `.venv\Scripts\python tests/harness.py tests/scenarios/split_owner_side.toml`. Three lines pass: the owner is answered, a stranger gets nothing, a group gets nothing. It tests the gate, not the user's own file; 3f checks that.

Start gpette in a second terminal: `cd <gpette folder>`, then `.venv\Scripts\python main.py`. `Invoke-RestMethod http://127.0.0.1:4849/api/` answers `gpette running`. To restart it later: Ctrl+C in that terminal, then the same line again.

### 3e. The user's inbox id

The inbox id is the identifier the user's messages come from: 64 letters and digits, no `0x`.

1. With both programs running and `members` still empty, agree a moment with the user and have them send one message to the assistant's address (from 3c) in the PublicOS app. It gets no answer, which is correct.
2. `(Invoke-RestMethod http://127.0.0.1:4849/api/admin/routes).routes | Format-List sender, decision, at, count` lists the refused chat (`gate none: reject`) with the full `sender`, the inbox id. (The admin page, `http://127.0.0.1:4849/admin`, shows the same with the id shortened.) Nothing shows the text of a refused message, so the check that it was theirs is the time: exactly one row whose `at` is the moment they sent (there is one row per chat; `count` is its messages). If two rows changed at that moment, do it again.
3. Put that id in `members = ["..."]` (edit `gpette.toml` with your file-editing tool, not with PowerShell's `Set-Content`, which can add a mark at the start of the file), restart gpette, and have them write again. Now it answers.

### 3f. Prove it is private

Do this with the user, and write the result in the changelog:

1. The user messages the assistant from their phone: it answers.
2. A message from any other account: no answer, not even a "read" mark, and the admin page shows `gate none: reject`.
3. On the admin page, the "who would handle this?" box, left on "dm": the user's id gives profile `owner`; any other id gives `default` with gate `none`.
4. `[server] host` is `127.0.0.1` in `gpette.toml`.

### 3g. Run it from marcha

Close the two terminals of 3c and 3d first (two copies would fight over the same ports). Then add both as marcha tasks (piece 1), in the same group as the dashboard:

- **The daemon:** command = the full path of `xmtp_daemon.exe`, **working directory = the daemon's own folder** (see 3c for why), and under Environment Variables `XMTP_WEBHOOK_URL` = `http://127.0.0.1:4849`.
- **gpette:** command = the full path of `.venv\Scripts\python.exe` in the gpette folder, arguments `main.py`, working directory = the gpette folder.

After the first start from marcha, check `/health` shows the same `inboxId` as in 3c. A different one means the working directory is wrong.

### 3h. Timers: an assistant that wakes itself up

With a timer the assistant can do quiet work on a schedule and write to the user only when there is something to say: a morning look at what is due, a weekly walk through stale threads. `MARCHA.md` describes how to run one well.

- Run it with gpette's Python (it needs gpette's packages). **Inside a conversation with the user on the phone** it needs no ids. The assistant's shell there is Git Bash, where backslashes vanish: write both paths in full, with forward slashes, in quotes (example paths; use the real ones):
  ```
  "C:/Tools/gpette/.venv/Scripts/python" "C:/Tools/gpette/scripts/timer.py" set "Timer test" "Say: the timer works." --time 2 --skip-session
  "C:/Tools/gpette/.venv/Scripts/python" "C:/Tools/gpette/scripts/timer.py" list
  "C:/Tools/gpette/.venv/Scripts/python" "C:/Tools/gpette/scripts/timer.py" cancel <id>
  ```
  That is a one-time test, two minutes ahead. `--skip-session` makes a fire start in a fresh session, without the chat's history; `--time "8 AM" --type recurring` makes one that repeats daily. For the real morning timer, do `MARCHA.md`, section 4, first: it sets up the page the timer reads.
- **From a terminal** (you, during this install) it must be told which chat, profile and person: `timer.py conversations` lists the chats (a chat exists once it has had a message), then add `--conv <id> --profile owner --owner <the user's inbox id>` to `set`; `list --all` shows every timer. In PowerShell a quoted program path needs `&` in front: `& "C:/Tools/gpette/.venv/Scripts/python" "C:/Tools/gpette/scripts/timer.py" conversations`. **Pick only the chat whose `last human sender` is the user's inbox id.** The list also holds chats of people who were refused; a timer set in one of those would send the assistant's report to that stranger, and the script does not refuse it (a refused person's chat shows `last human sender: none`). Check `list --all` afterwards.
- When a timer fires, the assistant receives `Timer fired:` plus the instructions. If it answers exactly `[NO_REPLY]`, nothing is sent. Use that for quiet work.
- **Write these commands, with the real paths in the quoted forward-slash form, in `wiki/tools.md` under "Timers"**, together with the `Timer fired:` and `[NO_REPLY]` rules, and this one: inside a conversation on the phone the commands need no ids; from a terminal they need `--conv`, `--profile` and `--owner`. **And add one line to this folder's `CLAUDE.md`**, under "During the conversation": `You can set yourself timers: the commands are in wiki/tools.md, section Timers.` The assistant on the phone knows only what `CLAUDE.md` tells it to read; without that line it will say it has no way to set a timer.
- Then prove it: the user asks the assistant on the phone to set a test timer, list it and cancel it. It should do so by itself, with `timer.py` from the wiki. If it says it has no way to set a timer, the pointer in `CLAUDE.md` is missing or wrong.
- **Start with one timer, agreed with the user** (what, when, how chatty). A timer that fires often costs model usage each time; say so.
- Never set a timer the user did not ask for or agree to.

### What it can't do

- The daemon and gpette must be running for the assistant to answer; marcha keeps them a click away.
- XMTP has announced that its current hosted network ends on 2027-02-01; the daemon's README says so.

## 4. PublicOS skills

The agents guide at https://publicos.dev/agents is written for assistants: reading profiles and feeds, following, posting, messaging, each as a small page with commands that were run live. When the user asks for something on PublicOS ("post this", "what did my friend publish?"), read the matching page there first and follow it.

Two rules from that guide matter most:

- A key that can act for an account is the whole account. Use the shortest-lived key that does the job, and only with the user's go for that action.
- An account run by software says so on its profile.

## More than one assistant

A team of assistants, each with its own inbox and character, taking turns on a schedule: `TEAM.md`. Only after this page works end to end.

## After the stack

Add a section "The stack" to `wiki/tools.md` with: where each program lives, the ports, the three marcha tasks, where the two secret files are backed up (the place, not the content), and how to restart everything. Add a changelog line. Then go back to the tree: this was plumbing, the method is the point.
