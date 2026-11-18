# personal_tree

A way of working with an AI assistant so that nothing gets lost between conversations, packaged as a folder you open with Claude.

The assistant forgets everything when a conversation ends. This folder gives it a memory made of plain files that you can read too: one folder per thing you are working on, a changelog, a small wiki, and a live page that shows all of it as a tree.

## Start

1. Download this folder (Code, Download ZIP) and unzip it where you keep your documents. Keep your copy private: it will hold your life.
2. Open the folder with Claude (the desktop app, or Claude Code in a terminal).
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

The method and the dashboard need only Python (3.9 or newer). The optional pieces (`STACK.md`, `MARCHA.md`, `TEAM.md`) run on Windows, need a PublicOS account for the phone app, and use three programs, each with its own instructions:

- **marcha**: a Windows launcher that keeps the programs running in one window. https://github.com/0xjmsl/marcha/releases (1.0.1 or newer; if you turn on its local API, use signed requests, as `MARCHA.md` shows)
- **xmtp_daemon**: the bridge to the messaging network; one inbox online. https://github.com/0xjmsl/xmtp_daemon
- **gpette**: decides who gets answered and runs the model. https://github.com/0xjmsl/gpette

And, if you want your assistants to have accounts on PublicOS: https://publicos.dev/agents

## It is a base

Rename things, add charts, drop what you do not use, rewrite the rules. The people who made it change theirs every week.

## Licence

MIT. See `LICENSE`.
