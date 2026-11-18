---
name: open-thread
description: Open a new thread (a node in the tree) the right way. Use when a subject comes up that will run across conversations or produce files, when the user says "open a thread", "track this", "add this to the tree", or when the conversation shifts to something that has no thread yet.
---

Open a thread in `threads/<slug>/`. Full rules: `wiki/workflow.md` § Threads.

## Steps

1. **Look for a sibling first.** Search `threads/*/thread.md` (names and bodies) for the subject's key words, and look at the tree (`python scripts/work_tree.py --json`). If an existing thread covers it, append there instead and stop. Say which thread you used.
2. **Is it a chore?** One small action with no steps goes in `threads/chores.md`, not a thread.
3. **Propose** a name, a slug (lowercase, underscores, short) and a parent (a top node or an existing thread). If the idea came up inside another thread, that thread is the `origin`. **Wait for the user to pick the name.**
4. Copy `threads/_templates/thread.md` to `threads/<slug>/thread.md` and fill it:
   - header: `name`, `status` (`idea` if nothing has started, `doing` if work begins now, `waiting-you` if the next move is theirs), `parent`, `origin` (only when it differs from parent), `why`, `opened` (today, from the clock), `next`;
   - `## Summary`: two or three lines from what the user said;
   - `## Tasks`: the first steps. `- [ ] ⏳` for what waits on the user.
5. If it came out of another thread, add one line in that thread pointing here (`[[threads/<slug>/thread|name]]`).
6. Add a changelog line under today's heading at the top of `changelog.md`: `` - `HH:MM` `[area]` **THREAD** - Opened [[threads/<slug>/thread|name]]: why. ``
7. Check it shows up: `python scripts/work_tree.py --json` lists it and `no_header` is empty.

Never rename a slug after creating it: links and the changelog point at it. Change `name:` instead (`wiki/workflow.md`, Renaming).
