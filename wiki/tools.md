# Tools

The commands and programs this setup uses. Add to it whenever something new is installed or a new command proves useful.

## The dashboard

```
python scripts/work_tree.py            # http://127.0.0.1:8790/
python scripts/work_tree.py --lan      # also reachable from a phone on the home network
python scripts/work_tree.py --port 8791
python scripts/work_tree.py --json     # print the tree once; `no_header` lists thread folders it could not read
```

It re-reads the files on every request. A change to `dashboard/index.html` shows on the next page reload; a change to `scripts/work_tree.py` needs the script restarted.

**Adding a chart:** write a function in `scripts/work_tree.py` that returns a dict, add its route in `H.do_GET`, then add a tab in `dashboard/index.html` (a button in `#tabs`, a `<section id="view-NAME">`, an entry in `VIEWS`). The Activity tab is the worked example.

## How I run this

<Filled during the install: the Claude desktop app, a plain terminal, or the terminal in VS Code; which Python command works on this machine.>

## Backup

<Filled during the install: where this folder is backed up and how often.>
