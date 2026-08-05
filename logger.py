"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Central Logging Module (Top-level Wrapper)

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

from graf.logger import (
    logger,
    LOGGER_NAME,
    setup_logger,
    info,
    warning,
    error,
    critical,
    debug,
    station_started,
    station_reconnecting,
    station_stopped,
    segment_saved,
    metadata_saved,
    file_verified,
    checksum_created,
    recording_error,
    startup,
    shutdown,
)

if __name__ == "__main__":
    startup()
    info("Logger initialized.")
    warning("This is a warning.")
    error("Example error.")
    station_started("Peace FM")
    segment_saved("Peace FM", "PeaceFM_20260727_010000.mp3")
    metadata_saved("Peace FM", "PeaceFM_20260727_010000.json")
    file_verified("Peace FM", "PeaceFM_20260727_010000.mp3")
    shutdown()