"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Central Logging Module

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path
from typing import Optional

from graf.config import config

LOGGER_NAME = "GRAF"

def setup_logger(
    name: str = LOGGER_NAME,
    log_dir: Optional[Path] = None,
    log_level: Optional[str] = None,
    log_to_console: Optional[bool] = None,
    log_to_file: Optional[bool] = None
) -> logging.Logger:
    """Set up and configure the GRAF logger instance."""
    logger_inst = logging.getLogger(name)

    level_str = log_level or config.logging.log_level
    logger_inst.setLevel(getattr(logging, level_str.upper(), logging.INFO))
    logger_inst.propagate = False

    if logger_inst.handlers:
        logger_inst.handlers.clear()

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(threadName)-15s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    target_log_dir = log_dir or config.paths.log_dir
    target_log_dir.mkdir(parents=True, exist_ok=True)

    use_console = log_to_console if log_to_console is not None else config.logging.log_to_console
    if use_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger_inst.addHandler(console_handler)

    use_file = log_to_file if log_to_file is not None else config.logging.log_to_file
    if use_file:
        log_file = target_log_dir / "capture.log"
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",
            interval=1,
            backupCount=config.logging.keep_days,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger_inst.addHandler(file_handler)

        error_file = target_log_dir / "errors.log"
        error_handler = TimedRotatingFileHandler(
            filename=error_file,
            when="midnight",
            interval=1,
            backupCount=60,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger_inst.addHandler(error_handler)

    return logger_inst

logger = setup_logger()

# Global helper functions
def info(message: str) -> None:
    logger.info(message)

def warning(message: str) -> None:
    logger.warning(message)

def error(message: str) -> None:
    logger.error(message)

def critical(message: str) -> None:
    logger.critical(message)

def debug(message: str) -> None:
    logger.debug(message)

# Station Logging Helpers
def station_started(station: str) -> None:
    info(f"[{station}] Recording started.")

def station_reconnecting(station: str, delay: int) -> None:
    warning(f"[{station}] Stream disconnected. Reconnecting in {delay} seconds...")

def station_stopped(station: str) -> None:
    warning(f"[{station}] Recording stopped.")

def segment_saved(station: str, filename: str) -> None:
    info(f"[{station}] Segment saved: {filename}")

def metadata_saved(station: str, filename: str) -> None:
    info(f"[{station}] Metadata saved: {filename}")

def file_verified(station: str, filename: str) -> None:
    info(f"[{station}] Verified: {filename}")

def checksum_created(station: str) -> None:
    info(f"[{station}] SHA256 checksum generated.")

def recording_error(station: str, exc: Exception) -> None:
    error(f"[{station}] {type(exc).__name__}: {exc}")

def startup() -> None:
    logger.info("=" * 70)
    logger.info("G-Radio Acquisition Framework (GRAF)")
    logger.info(f"Started: {datetime.now()}")
    logger.info("=" * 70)

def shutdown() -> None:
    logger.info("=" * 70)
    logger.info("Stopping GRAF...")
    logger.info("=" * 70)
