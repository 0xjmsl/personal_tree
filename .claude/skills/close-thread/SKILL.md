---
name: close-thread
description: Close a finished thread, or drop an idea that was decided against. Use when the user says "close this", "we're done with X", "drop that idea", or when a thread's work has clearly finished.
---

Close a thread in `threads/<slug>/`. Full rules: `wiki/workflow.md` § Closing.

## Steps

1. **Check the work really happened.** Read the thread's tasks. For each open one, ask: done, not needed, or still to do? Don't close over real open work without the user saying so. Small leftovers can move to `threads/chores.md`.
2. **Children.** If other threads have `parent: <this slug>`, they must be closed first or re-pointed at this thread's parent. Ask the user.
3. **Finish `## Summary`**: the outcome, what was done, what was not, anything learned.
4. **Move lasting knowledge to the wiki.** Anything in the thread that will stay true and be needed again (contacts, how something works, a decision that sets a rule) goes to the right `wiki/<area>/<topic>.md` page. Say what you moved.
5. **Files.** Walk `threads/<slug>/files/`: keep with the thread, move to the wiki or the user's documents, or delete (ask before deleting).
6. **Header:** `status: done`, `closed: <today>`, `next:` empty. Tick the finished tasks; a task that turned out not to be needed is ticked too, with "(not needed)" after it.
7. **Move the folder** to `threads/_done/<slug>/` (create `threads/_done/` if it is not there yet; the same for `threads/_dropped/`).
8. **Fix links:** replace `threads/<slug>/` with `threads/_done/<slug>/` in other threads and wiki pages (leave old changelog lines as they are; the dashboard understands both).
9. **Changelog:** `` - `HH:MM` `[area]` **THREAD** - Closed [[threads/_done/<slug>/thread|name]]: the outcome in one sentence. ``

## Dropping an idea instead

When the user decides against something: `status: dropped`, `closed: <today>`, and add a `## Why we dropped it` section (the reason, what would make us reconsider, ideally the user's own words). Move the folder to `threads/_dropped/<slug>/`, fix links the same way (to `threads/_dropped/<slug>/`), and add the changelog line: `` - `HH:MM` `[area]` **THREAD** - Dropped [[threads/_dropped/<slug>/thread|name]]: why, in one sentence. `` This keeps the answer to "why don't we do X?".
