# personal_tree

A way of working with an AI assistant so that nothing gets lost between conversations, packaged as a folder you open with Claude.

The assistant forgets everything when a conversation ends. This folder gives it a memory made of plain files that you can read too: one folder per thing you are working on, a changelog, a small wiki, and a live page that shows all of it as a tree.

## What you need

| For | You need | Time |
|---|---|---|
| The method and the dashboard (Part 1) | **Claude Code**: the `claude` command in a terminal, or the Claude desktop app in its Code mode (plain chat cannot run commands or edit files), on a Claude plan that includes it. **Python 3.9+** | 20 to 30 minutes |
| A private assistant you message from your phone (Part 2, `STACK.md`) | Windows. **Python 3.11+**. **Git for Windows** (Claude Code on Windows runs its commands in Git Bash). A phone with the PublicOS app, or any other app that messages over XMTP | 2 to 4 hours, with the assistant doing most of it |
| A team of assistants (Part 3, `TEAM.md`) | Part 2 working. Node.js if the team gets PublicOS accounts | An evening, then a week of tuning |

The assistant installs what is missing with you, step by step; you do not need to be a developer for Part 1. Part 2 edits a config file and runs two programs; the assistant does it, but expect to approve a lot of steps.

## Start

1. Download this folder (Code, Download ZIP) and unzip it where you keep your documents. Keep your copy private: it will hold your life. If you clone it with git instead, cut the link to this public repository before the folder holds anything personal (`git remote remove origin`), so nothing of yours can ever be pushed here.
2. Open the folder with Claude Code (in a terminal: `cd` into the folder, then `claude`; or open the folder in the desktop app's Code mode).
3. Say: **read INSTALL.md and set me up**.

The assistant asks a few questions and builds your tree with you. `START_HERE.md` explains what you are getting and why.

## What is in it

| File | What it is |
|---|---|
| `START_HERE.md` | The idea, for you |
| `INSTALL.md` | The setup, for the assistant: your areas, your first threads, the dashboard |
| `CLAUDE.md`, `wiki/workflow.md` | The rules the assistant works by. Yours to change |
| `scripts/work_tree.py`, `dashboard/` | The live page: Tree, Graph, Activity. Python only, no database, no account |
| `scripts/marcha.py` | A small command for marcha's local API (see `MARCHA.md`) |
| `STACK.md` | Optional: a private assistant you message from your phone, running on your own PC |
| `MARCHA.md` | Optional: what marcha is for, and how to make the assistant work on a schedule by itself |
| `TEAM.md` | Optional, later: a team of assistants that take turns and report to you |

## The optional pieces

The method and the dashboard need only Python (3.9 or newer). The optional pieces (`STACK.md`, `MARCHA.md`, `TEAM.md`) run on Windows, need an app on the phone that speaks XMTP (we use PublicOS), and use three programs, each with its own instructions:

- **marcha**: a Windows launcher that keeps the programs running in one window. https://github.com/0xjmsl/marcha/releases (1.0.1 or newer; if you turn on its local API, use signed requests, as `MARCHA.md` shows)
- **xmtp_daemon**: the bridge to the messaging network; one inbox online. https://github.com/0xjmsl/xmtp_daemon
- **gpette**: decides who gets answered and runs the model. https://github.com/0xjmsl/gpette

And, if you want your assistants to have accounts on PublicOS, the guide written for them: https://publicos.dev/skill.md (the same guide as a plain index: https://publicos.dev/llms.txt)

## It is a base

Rename things, add charts, drop what you do not use, rewrite the rules. The people who made it change theirs every week.

## Licence

MIT. See `LICENSE`.
