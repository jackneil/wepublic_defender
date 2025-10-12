import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


DEFAULT_LOG_RELATIVE = Path(".wepublic_defender") / "logs" / "wpd.log"


def ensure_log_path(log_path: Optional[Path] = None) -> Path:
    """Ensure the log file path exists and return it.

    Defaults to CWD/.wepublic_defender/logs/wpd.log
    """
    path = log_path or (Path.cwd() / DEFAULT_LOG_RELATIVE)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _level_from_env() -> int:
    lvl = os.getenv("WPD_LOG_LEVEL", "").upper().strip()
    if not lvl and os.getenv("WPD_DEBUG"):
        lvl = "DEBUG"
    mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    return mapping.get(lvl, logging.INFO)


def get_logger(name: str = "wepublic_defender", log_path: Optional[Path] = None) -> logging.Logger:
    """Return a configured logger that writes UTF-8 logs to the case directory.

    Uses a rotating file handler (10 MB, 5 backups).
    """
    logger = logging.getLogger(name)
    if getattr(logger, "_wpd_configured", False):
        return logger

    logger.setLevel(_level_from_env())
    logger.propagate = False

    path = ensure_log_path(log_path)
    handler = RotatingFileHandler(path, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8")
    handler.setLevel(_level_from_env())
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    # Avoid duplicate handlers if get_logger called multiple times
    logger._wpd_configured = True  # type: ignore[attr-defined]
    logger.info(f"Logging to {path}")
    return logger


def enable_console_logging(level: Optional[int] = None) -> None:
    """Attach a console StreamHandler to the main logger.

    Respects WPD_LOG_LEVEL/WPD_DEBUG unless a specific level is provided.
    """
    logger = logging.getLogger("wepublic_defender")
    # Check if console already attached
    for h in logger.handlers:
        if isinstance(h, logging.StreamHandler) and getattr(h, "_wpd_console", False):
            return

    sh = logging.StreamHandler()
    sh.setLevel(level if level is not None else _level_from_env())
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%H:%M:%S")
    sh.setFormatter(fmt)
    sh._wpd_console = True  # type: ignore[attr-defined]
    logger.addHandler(sh)
