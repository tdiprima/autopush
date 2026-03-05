# autopush

When you're actively working across multiple projects, it's easy to leave good work sitting local. This tool makes sure it all gets pushed.

## What it does

Scans all subdirectories (depth 1) of a target directory, finds every folder with a `.git` repo, checks if there are uncommitted changes or unpushed commits, and if so: stages everything, commits, and pushes.

One command. All repos. Done.

## Usage

```bash
# Scan the current directory
python main.py

# Scan a specific directory with a custom commit message
AUTOPUSH_SCAN_DIR=~/projects \
AUTOPUSH_COMMIT_MESSAGE="chore: sync local work" \
python main.py

# Preview what would happen without touching anything
AUTOPUSH_SCAN_DIR=~/projects AUTOPUSH_DRY_RUN=true python main.py
```

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `AUTOPUSH_SCAN_DIR` | current directory | Directory to scan for git repos |
| `AUTOPUSH_COMMIT_MESSAGE` | `Auto-commit: sync local changes` | Commit message to use |
| `AUTOPUSH_LOG_LEVEL` | `INFO` | Log verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `AUTOPUSH_DRY_RUN` | `false` | Set to `true` to preview without making changes |
