"""
==============================================================
G-Radio Acquisition Framework (GRAF)

Central Logging Module

Author : Selase K. Agbai
Project: Rob-GhanaRadio

==============================================================
"""

from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from config import (
    LOG_DIR,
    LOG_LEVEL,
    LOG_TO_CONSOLE,
    LOG_TO_FILE,
)

# ------------------------------------------------------------
# Ensure log directory exists
# ------------------------------------------------------------

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# Logger Name
# ------------------------------------------------------------

LOGGER_NAME = "GRAF"

logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

logger.propagate = False

# Prevent duplicate handlers

if logger.handlers:
    logger.handlers.clear()

# ------------------------------------------------------------
# Common Formatter
# ------------------------------------------------------------

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(threadName)-15s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ------------------------------------------------------------
# Console Logger
# ------------------------------------------------------------

if LOG_TO_CONSOLE:

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

# ------------------------------------------------------------
# Daily Rotating Log
# ------------------------------------------------------------

if LOG_TO_FILE:

    log_file = LOG_DIR / "capture.log"

    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

# ------------------------------------------------------------
# Error Log
# ------------------------------------------------------------

error_file = LOG_DIR / "errors.log"

error_handler = TimedRotatingFileHandler(
    filename=error_file,
    when="midnight",
    interval=1,
    backupCount=60,
    encoding="utf-8",
)

error_handler.setLevel(logging.ERROR)

error_handler.setFormatter(formatter)

logger.addHandler(error_handler)

# ------------------------------------------------------------
# Convenience Functions
# ------------------------------------------------------------

def info(message: str):
    logger.info(message)


def warning(message: str):
    logger.warning(message)


def error(message: str):
    logger.error(message)


def critical(message: str):
    logger.critical(message)


def debug(message: str):
    logger.debug(message)

# ------------------------------------------------------------
# Station Logging Helpers
# ------------------------------------------------------------

def station_started(station: str):
    info(f"[{station}] Recording started.")


def station_reconnecting(station: str, delay: int):
    warning(
        f"[{station}] Stream disconnected. Reconnecting in {delay} seconds..."
    )


def station_stopped(station: str):
    warning(f"[{station}] Recording stopped.")


def segment_saved(station: str, filename: str):
    info(f"[{station}] Segment saved: {filename}")


def metadata_saved(station: str, filename: str):
    info(f"[{station}] Metadata saved: {filename}")


def file_verified(station: str, filename: str):
    info(f"[{station}] Verified: {filename}")


def checksum_created(station: str):
    info(f"[{station}] SHA256 checksum generated.")


def recording_error(station: str, exc: Exception):
    error(f"[{station}] {type(exc).__name__}: {exc}")

# ------------------------------------------------------------
# Startup Banner
# ------------------------------------------------------------

def startup():

    logger.info("=" * 70)

    logger.info("G-Radio Acquisition Framework (GRAF)")

    logger.info(f"Started: {datetime.now()}")

    logger.info("=" * 70)


# ------------------------------------------------------------
# Shutdown Banner
# ------------------------------------------------------------

def shutdown():

    logger.info("=" * 70)

    logger.info("Stopping GRAF...")

    logger.info("=" * 70)


# ------------------------------------------------------------
# Example
# ------------------------------------------------------------

if __name__ == "__main__":

    startup()

    info("Logger initialized.")

    warning("This is a warning.")

    error("Example error.")

    station_started("Peace FM")

    segment_saved(
        "Peace FM",
        "PeaceFM_20260727_010000.mp3",
    )

    metadata_saved(
        "Peace FM",
        "PeaceFM_20260727_010000.json",
    )

    file_verified(
        "Peace FM",
        "PeaceFM_20260727_010000.mp3",
    )

    shutdown()