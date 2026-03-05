# autopush

When you're actively working across multiple projects, it's easy to leave good work sitting local. This tool makes sure it all gets pushed.

## What it does

Scans all subdirectories (depth 1) of a target directory, finds every folder with a `.git` repo, checks if there are uncommitted changes or unpushed commits, and if so: stages everything, commits, and pushes.

One command. All repos. Done.

### File structure:

```
autopush/
├── main.py     # orchestration only
├── config.py   # env/config loading and validation
├── scanner.py  # find git repos at max depth 1
└── git_ops.py  # git status checks and operations
```

### Run with defaults (scans current directory):

```sh
cd autopush
python main.py 
```

### Override via environment variables:

```sh
AUTOPUSH_SCAN_DIR=$HOME/projects \
AUTOPUSH_COMMIT_MESSAGE="chore: sync local work" \
AUTOPUSH_LOG_LEVEL=DEBUG \
python main.py
```

### Dry run (no changes made, just logs what would happen):

```sh
AUTOPUSH_SCAN_DIR=$HOME/projects \
AUTOPUSH_DRY_RUN=true \
python main.py
```

<br>
