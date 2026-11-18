# Start here

This folder is a way of working with an AI assistant so that nothing gets lost between conversations. The people who made it use it every day to run a large project. This copy is set up for a person's life instead: work, health, family, money, the small apps you build, whatever you decide.

You don't have to learn it first. Open the folder with Claude and say **"read INSTALL.md and set me up"**. The assistant asks you a few questions and builds your tree with you. This page is the "why" so you know what you are getting.

## The problem it solves

An assistant forgets everything when a conversation ends. You end up explaining the same things again, and half-finished ideas vanish. This method gives the assistant a memory made of plain files that you can also read:

| File or folder | What it holds | Think of it as |
|---|---|---|
| `threads/` | One folder per thing you are working on or thinking about | Your open loops |
| `changelog.md` | One dated line for each thing that got done | Your diary of work |
| `wiki/` | What is true and worth keeping: contacts, routines, how your apps work | Your reference shelf |
| `threads/chores.md` | Small things that don't deserve a folder | Your sticky notes |

The assistant reads these before it answers, and updates them as you work. You never have to ask "did you write that down?".

## Threads make a tree

Every thread says where it belongs. At the top are a few big areas you pick, for example **Work**, **Health**, **Children**, **Home**, **Money**. Under each one hang the threads: "Find a new dentist", "Kitchen renovation", "Tax return 2026", "My recipe app". A thread that grows gets split into smaller ones under it.

Each thread carries a status (idea, doing, waiting on you, blocked, parked, done, or dropped for an idea you decided against), one line on why it exists, one line on what comes next, a short summary, and a task list.

## The dashboard

Run one command, open the address it prints, and you get a page with three views:

- **Tree**: every thread under its area, with its status and to-dos. The "Waiting on you" button shows the threads that need you; small things that wait on you are in the Chores card under the tree.
- **Graph**: the same threads as dots joined by lines, so you can see what is connected to what and where ideas came from.
- **Activity**: where your attention went, week by week.

It reads your files live. There is no database and no account.

## A normal day

1. You open Claude in this folder and talk about whatever is on your mind.
2. The assistant finds the thread it belongs to, or proposes a new one. **You pick the name.**
3. You work. As each piece gets done, the assistant writes one line in the changelog and updates the thread.
4. Anything it learns that will stay true (your doctor's hours, how your app deploys) goes into the wiki.
5. You glance at the dashboard when you want the big picture.

## Ways to run it

Talk these over with the assistant during the install; it will help you choose and set it up.

- **The Claude desktop app, pointed at this folder.** The simplest start. It reads the same rules file (`CLAUDE.md`).
- **Claude Code in a terminal inside VS Code.** This is what the makers use every day: you see the files change next to the conversation. Worth installing once you are comfortable.
- **From your phone, through PublicOS.** Optional and more work: your own private assistant that you message like a contact, running on your PC. See `STACK.md`.
- **A team.** Later, if you want it: several assistants with different characters that take turns on a schedule and report to you. See `TEAM.md`.

## This is a base, not a rulebook

The people who made this changed their own setup every week for months, and still do. Do the same.

- **Move things.** Rename areas, merge them, add one. Reorder the dashboard's columns.
- **Add charts.** Ask the assistant: "add a chart of how many threads I close per month", or "show me which area has the oldest untouched threads". The dashboard is one file, built to be edited.
- **Drop what you don't use.** If chores never get used, delete the section. If the changelog feels too detailed, tell the assistant what level you want.
- **Review it.** Every week or two, look at the tree with the assistant and ask: what is stale, what should be closed, what should be split?
- **Change the rules.** The rules live in `CLAUDE.md` and `wiki/workflow.md`. When something annoys you twice, say so, and have the assistant rewrite the rule.

The only part worth protecting is the habit underneath: **write it down where the next conversation will find it.**

## What is in the folder

```
START_HERE.md      this page
INSTALL.md         the setup the assistant follows with you
STACK.md           optional: marcha, your private assistant on PublicOS
MARCHA.md          optional: what marcha does, scheduled jobs, an assistant on timers
TEAM.md            optional, later: a team of assistants that take turns
README.md          the one-page description of this kit
CLAUDE.md          the rules the assistant reads every time
changelog.md       what got done, newest first
wiki/              what is true (workflow.md holds the method itself)
threads/           your threads (the tree), plus chores.md
dashboard/         the page you look at
scripts/           the small program that serves the dashboard (and marcha.py, see MARCHA.md)
.claude/skills/    two routines the assistant uses: open a thread, close a thread
```

## Privacy

Everything stays in this folder on your computer, plus the backup you choose. The dashboard is only reachable from your own machine unless you start it with `--lan`. Keep a backup of the folder: it will become valuable.
