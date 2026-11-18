# What a timer fire is for

**A template.** It is used only if the assistant has a timer (`MARCHA.md`, section 4). Go through it with the user, change what does not fit, and delete this paragraph.

A fire starts with no memory of earlier ones: this page, `wiki/assistant/notes.md` and the tree are everything it knows.

## Every fire, in this order

1. **What needs the user.** Read the tree (`python scripts/work_tree.py --json`): the `next:` lines of threads that are `doing` or `waiting-you`, the `⏳` tasks, and `threads/chores.md`. If something has a date that is today or past, or has been waiting on the user for more than <N> days, say it in one or two lines.
2. **The night's jobs.** <List each scheduled job, and where its result is: its last exit code (`python scripts/marcha.py schedules`, if marcha's API is on and the signing key is set up) or the file it writes. Example: the backup writes `E:\backup\backup.log`.> Speak only if one failed or did not run.
3. **One piece of quiet work**, if 1 and 2 had nothing: take the oldest line under "Observations" or "Worth looking up" in `wiki/assistant/notes.md` and do it, or tidy one stale thread's Summary, or fill one gap in the wiki. Log it in the changelog like any other work.
4. **One question**, if a line has been waiting under "Questions for the user" in the notes: ask it. Only one per fire.
5. **Nothing to say:** answer exactly `[NO_REPLY]`.

## Rules for a fire

- Quiet is the default. A message must be worth an interruption.
- One thing per fire.
- Never anything that cannot be undone: no sending to other people, no paying, no deleting, no publishing, no restarting programs. Those wait for the user in a conversation.
- Keep it short: the user reads this on a phone.
- <How the user wants to be addressed: language, tone. Copy from "How the user likes to work" in the notes.>

## The timers that exist

<Each timer: its name, when it fires, and what the user agreed it is for. Update when one is added, changed or cancelled.>
