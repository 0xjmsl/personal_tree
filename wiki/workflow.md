# Workflow

How we keep track of things. Three places, three jobs. Don't mix them.

| Place | Holds | Lives in |
|---|---|---|
| **Wiki** | What is true and will stay true | `wiki/` |
| **Threads** | What we are thinking about or working on | `threads/<slug>/` |
| **Changelog** | What happened, at `HH:MM`, today | `changelog.md` |

The test: *"X is how it is"* goes to the wiki. *"We are working on X"* is a thread. *"I just did X"* is a changelog line.

## Threads

A thread is a folder:

```
threads/
  <slug>/
    thread.md     header + Summary + Tasks + notes
    files/        drafts, exports, screenshots, scripts (only when needed)
  _done/<slug>/   closed threads
  _dropped/<slug>/  ideas we decided against, with the reason
  _templates/     the starting files
  chores.md       small things that don't deserve a thread
```

### Every thread is a node in the tree

The dashboard reads three parts of every `thread.md`. Whoever touches the thread keeps all three true, in the same step.

**1. The header**, first thing in the file:

```yaml
---
name: <short display name>   # the user picks it; the folder slug never changes
status: doing                # idea · doing · blocked · waiting-you · done · parked · dropped
parent: <slug>               # where it belongs: a top node (work, health, ...) or another thread
origin: <slug>               # where the idea came up; leave out when it equals parent
why: "<one line>"
opened: YYYY-MM-DD
closed:
next: "<one line>"
---
```

- **Top nodes** (the big areas) are threads too: a folder with a `thread.md` whose `status:` and `parent:` are empty. The dashboard counts what is under them.
- `doing` also covers "done, with follow-ups still open".
- `idea` means nothing has started; `parked` means stopped on purpose, to come back to.
- `waiting-you` means the next move is the user's. `blocked` means it waits on someone or something else (a quote, an answer, a date).
- `parent` builds the tree. `origin` records where an idea came from when that is somewhere else: "the budget spreadsheet idea came up while planning the trip" has `parent: money`, `origin: summer_trip`. The Graph view draws both.

**2. `## Summary`**: the short story. What we did, what it produced, why. Updated every time the thread is touched; finished at close.

**3. `## Tasks`**: checkboxes. `- [ ]` open, `- [x]` done, `- [ ] ⏳` waiting on the user.

Mentioning another thread as `[[threads/<slug>/thread|name]]` anywhere in the body draws a line between the two in the Graph.

### Opening a thread

1. **Look for a sibling first.** Search `threads/*/thread.md` for the subject. Most ideas belong in an existing thread: append there. A new thread earns itself when it has a different outcome or a different owner, not merely a different sub-topic.
2. Propose a name and a parent. **The user decides.** Slugs are short, lowercase, with underscores (`new_dentist`, `tax_2026`).
3. Copy `threads/_templates/thread.md`, fill the header, write the first lines of Summary and Tasks.
4. Add a changelog line that links it.

### Splitting and tidying

A thread with several separate pieces of work gets child threads (`parent: <this slug>`). Check for this whenever a branch is reviewed. Tidy often: it is cheaper than one big cleanup.

### Closing

Use the `close-thread` skill. In short: check the work really happened, finish the Summary (outcome, what landed, what didn't), move anything lasting to the wiki, set `status: done` and `closed:`, move the folder to `threads/_done/`, add a changelog line. An idea we decided against goes to `threads/_dropped/` with `status: dropped` and a line on why, so that "why don't we do X?" has an answer later.

### Renaming

The folder name (the slug) never changes. To rename a thread: change `name:` in its header and the `# ` heading under it, and update the name where other threads and wiki pages link to it (`[[threads/<slug>/thread|New name]]`). Old changelog lines stay as they were. Add one changelog line: `**NOTE** - Renamed "Old" to "New"`, linking the thread.

### An idea that never had a thread

When the user decides against something that was only ever mentioned: one changelog line is the whole record, under the area it would have belonged to: `**DECISION** - Decided against <the idea>: <why, if they said>.` No folder, no questions about a name. If the same idea keeps coming back, that is the moment to give it a folder in `threads/_dropped/` with the reason.

### Dates

A thread has no deadline field. A deadline goes in `next:` in words (`next: "Send the proposal by 2026-03-20"`) and in the task it belongs to. An appointment or a routine that will stay true for a while (physio on Mondays at 9:00, the clinic's phone) goes on a wiki page for that area, and the thread links it.

### Chores

`threads/chores.md`, one `## <title>` per chore, then `status:` (`todo` · `doing` · `waiting-you` · `done`) and `why:` lines, then a short description. A chore that grows steps becomes a thread. Done chores are removed after a while; the changelog keeps the record.

## Changelog

One file, newest day first, newest entry first inside the day.

```markdown
## 2026-03-14
- `16:20` `[health]` **DONE** - Booked the dentist for the 21st at 10:00 ([[threads/new_dentist/thread|New dentist]]). Clinic details added to wiki/health/contacts.
- `09:05` `[work]` **DECISION** - We send the proposal without the third option ([[threads/acme_proposal/thread|Acme proposal]]).
```

- A new entry goes directly under today's heading at the top. Create the heading if the day is new. Never add at the bottom of the file.
- The time comes from the clock. The area in brackets is the top node's folder name (`[the_kids]`); for something that spans the whole tree use a word of your own (`[setup]`, `[tree]`).
- Types: `DONE` · `DECISION` · `FIX` · `NOTE` · `THREAD` (opened or closed) · `WIKI`. Add your own if they help.
- **Link the thread.** The dashboard's "last worked on" and the Activity chart read these links.
- Log as each piece closes, not at the end of the conversation. Skip trivia and things undone in the same sitting.
- When the file gets long, move finished months to `changelog_archive/YYYY-MM.md`. The dashboard reads both.
- Re-read the file right before adding a line, and add only that line. Never write back a copy you read earlier.

## Wiki

`wiki/` is the reference shelf. One topic per page.

- `wiki/workflow.md`: this page.
- `wiki/tools.md`: the commands we use (the dashboard, backups, anything added later).
- `wiki/<area>/<topic>.md`: per area. Examples: `wiki/health/contacts.md`, `wiki/home/appliances.md`, `wiki/apps/recipe_app.md`. Create the folders as they are needed; don't build an empty structure up front.
- `wiki/assistant/notes.md`: the assistant's own notes and open questions for the user.

Rules:

- **Read first.** Before working on something, load its page.
- **Write as you learn.** A lasting fact you had to find out goes on its page in the same task.
- **Reality wins.** If the page and the world disagree, fix the page.
- Link pages by path: `[[wiki/health/contacts]]`.
- For the apps and tools the user builds, give each one a page: what it is for, where the code is, how to run it, how to deploy it, what broke before. The app's code is the truth; the page is the map to it.

## Reviewing the tree

Every week or two, open the dashboard together and walk it:

- **Waiting on you**: can any be answered now?
- **Doing** threads not touched in weeks: still doing, or parked?
- Threads with many tasks: split?
- **Ideas**: start one, or drop some?
- Is there something in your head that is not in the tree?

## Changing this page

These rules are a starting point. When one gets in the way, change it here, add a changelog line of type `NOTE` saying what changed and why, and carry on.
