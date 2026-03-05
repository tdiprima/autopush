"""Scan a directory (max depth 1) for subfolders that contain a .git directory."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def find_git_repos(scan_dir: str) -> list[Path]:
    """Return a list of subdirectories (depth 1) that contain a .git folder."""
    parent = Path(scan_dir).resolve()
    repos = []

    try:
        entries = list(parent.iterdir())
    except PermissionError as exc:
        logger.error("Cannot read directory %s: %s", parent, exc)
        return repos

    for entry in sorted(entries):
        if not entry.is_dir():
            continue
        git_dir = entry / ".git"
        if git_dir.exists() and git_dir.is_dir():
            logger.debug("Found git repo: %s", entry)
            repos.append(entry)

    logger.info("Found %d git repo(s) under %s", len(repos), parent)
    return repos
