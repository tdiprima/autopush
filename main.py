"""Orchestrate scanning for git repos and pushing any pending changes."""

import logging
import sys

from config import load_config, validate_config
from scanner import find_git_repos
from git_ops import needs_push, add_commit_push


def setup_logging(log_level: str) -> None:
    """Configure the root logger with the given level."""
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=log_level.upper(),
    )


def process_repos(repos: list, commit_message: str, dry_run: bool) -> dict:
    """Check each repo and push if needed. Return a summary of results."""
    results = {"pushed": [], "skipped": [], "failed": []}
    logger = logging.getLogger(__name__)

    for repo in repos:
        if not needs_push(repo):
            logger.info("Skipping %s — nothing to push", repo.name)
            results["skipped"].append(repo)
            continue

        logger.info("Repo %s has changes to push", repo.name)

        if dry_run:
            logger.info("[DRY RUN] Would push: %s", repo)
            results["skipped"].append(repo)
            continue

        success = add_commit_push(repo, commit_message)
        if success:
            results["pushed"].append(repo)
        else:
            results["failed"].append(repo)

    return results


def log_summary(results: dict) -> None:
    """Log a human-readable summary of what was pushed, skipped, and failed."""
    logger = logging.getLogger(__name__)
    logger.info(
        "Done. Pushed: %d | Skipped: %d | Failed: %d",
        len(results["pushed"]),
        len(results["skipped"]),
        len(results["failed"]),
    )
    for repo in results["failed"]:
        logger.error("Failed to push: %s", repo)


def main() -> int:
    """Entry point. Returns exit code 0 on success, 1 if any push failed."""
    config = load_config()
    setup_logging(config["log_level"])
    logger = logging.getLogger(__name__)

    try:
        validate_config(config)
    except ValueError as exc:
        logger.error("Configuration error: %s", exc)
        return 1

    logger.info(
        "Scanning %s (dry_run=%s)", config["scan_dir"], config["dry_run"]
    )

    repos = find_git_repos(config["scan_dir"])
    if not repos:
        logger.info("No git repositories found. Exiting.")
        return 0

    results = process_repos(repos, config["commit_message"], config["dry_run"])
    log_summary(results)

    return 1 if results["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
