"""Load and validate configuration from environment variables."""

import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_COMMIT_MESSAGE = "Auto-commit: sync local changes"
DEFAULT_LOG_LEVEL = "INFO"


def load_config() -> dict:
    """Read configuration from environment variables with sane defaults."""
    config = {
        "scan_dir": os.environ.get("AUTOPUSH_SCAN_DIR", os.getcwd()),
        "commit_message": os.environ.get("AUTOPUSH_COMMIT_MESSAGE", DEFAULT_COMMIT_MESSAGE),
        "log_level": os.environ.get("AUTOPUSH_LOG_LEVEL", DEFAULT_LOG_LEVEL),
        "dry_run": os.environ.get("AUTOPUSH_DRY_RUN", "false").lower() == "true",
    }
    return config


def validate_config(config: dict) -> None:
    """Raise ValueError if any required config values are invalid."""
    scan_dir = config["scan_dir"]
    if not os.path.isdir(scan_dir):
        raise ValueError(f"AUTOPUSH_SCAN_DIR is not a valid directory: {scan_dir!r}")

    commit_message = config["commit_message"]
    if not commit_message or not commit_message.strip():
        raise ValueError("AUTOPUSH_COMMIT_MESSAGE must not be empty.")

    valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if config["log_level"].upper() not in valid_log_levels:
        raise ValueError(
            f"AUTOPUSH_LOG_LEVEL must be one of {valid_log_levels}, "
            f"got: {config['log_level']!r}"
        )
