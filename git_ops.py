"""Git operations: check status, add, commit, and push."""

import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def _run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    """Run a git command in the given directory and return the result."""
    cmd = ["git"] + args
    logger.debug("Running: %s in %s", " ".join(cmd), cwd)
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )


def has_working_tree_changes(repo: Path) -> bool:
    """Return True if there are any staged or unstaged changes in the working tree."""
    result = _run_git(["status", "--porcelain"], repo)
    if result.returncode != 0:
        logger.warning("git status failed in %s: %s", repo, result.stderr.strip())
        return False
    return bool(result.stdout.strip())


def has_unpushed_commits(repo: Path) -> bool:
    """Return True if there are local commits ahead of the upstream branch."""
    result = _run_git(["rev-list", "@{u}..HEAD", "--count"], repo)
    if result.returncode != 0:
        # No upstream configured or other error — treat as needing attention
        logger.debug(
            "Could not compare with upstream in %s: %s", repo, result.stderr.strip()
        )
        return False
    count = result.stdout.strip()
    return count.isdigit() and int(count) > 0


def needs_push(repo: Path) -> bool:
    """Return True if the repo has uncommitted changes or unpushed commits."""
    return has_working_tree_changes(repo) or has_unpushed_commits(repo)


def stage_all(repo: Path) -> bool:
    """Run `git add --all`. Return True on success."""
    result = _run_git(["add", "--all"], repo)
    if result.returncode != 0:
        logger.error("git add failed in %s: %s", repo, result.stderr.strip())
        return False
    return True


def commit(repo: Path, message: str) -> bool:
    """Run `git commit -m <message>`. Return True on success, False if nothing to commit."""
    result = _run_git(["commit", "-m", message], repo)
    if result.returncode == 0:
        logger.info("Committed in %s", repo)
        return True
    output = (result.stdout + result.stderr).lower()
    if "nothing to commit" in output:
        logger.info("Nothing new to commit in %s", repo)
        return True  # Not an error — just no staged changes
    logger.error("git commit failed in %s: %s", repo, result.stderr.strip())
    return False


def push(repo: Path) -> bool:
    """Run `git push`. Return True on success."""
    result = _run_git(["push"], repo)
    if result.returncode != 0:
        logger.error("git push failed in %s: %s", repo, result.stderr.strip())
        return False
    logger.info("Pushed %s successfully", repo)
    return True


def add_commit_push(repo: Path, message: str) -> bool:
    """Stage all changes, commit, and push. Return True only if all steps succeed."""
    if not stage_all(repo):
        return False
    if not commit(repo, message):
        return False
    if not push(repo):
        return False
    return True
