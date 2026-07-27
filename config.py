"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Configuration File

Author : Selase K. Agbai
Project: Rob-GhanaRadio
Purpose: Central configuration for dataset acquisition.

This file should contain ALL configurable parameters used by
the framework.

No other module should hardcode paths or recording settings.

==============================================================
"""

from pathlib import Path
import multiprocessing

# ============================================================
# PROJECT INFORMATION
# ============================================================

PROJECT_NAME = "G-Radio Acquisition Framework"

PROJECT_VERSION = "1.0.0"

DATASET_NAME = "G-Radio"

COUNTRY = "Ghana"

TIMEZONE = "Africa/Accra"

# ============================================================
# STORAGE DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

STORAGE_DIR = BASE_DIR / "storage"

RAW_AUDIO_DIR = STORAGE_DIR / "raw"

METADATA_DIR = STORAGE_DIR / "metadata"

LOG_DIR = STORAGE_DIR / "logs"

REPORT_DIR = STORAGE_DIR / "reports"

FAILED_DIR = STORAGE_DIR / "failed"

CACHE_DIR = STORAGE_DIR / "cache"

ANNOTATION_DIR = STORAGE_DIR / "annotations"

TEMP_DIR = STORAGE_DIR / "temp"

# ============================================================
# AUTOMATIC DIRECTORY CREATION
# ============================================================

DIRECTORIES = [

    STORAGE_DIR,

    RAW_AUDIO_DIR,

    METADATA_DIR,

    LOG_DIR,

    REPORT_DIR,

    FAILED_DIR,

    CACHE_DIR,

    ANNOTATION_DIR,

    TEMP_DIR

]

# ============================================================
# STATION CONFIGURATION
# ============================================================

# The JSON file containing all stations.
# This keeps stations out of the source code.

STATIONS_FILE = BASE_DIR / "stations" / "ghana_stations.json"

# ============================================================
# AUDIO CAPTURE SETTINGS
# ============================================================

# Segment duration (seconds)

SEGMENT_DURATION = 600

# Save audio directly without re-encoding.
# Faster and preserves original stream quality.

COPY_AUDIO_STREAM = True

# Desired audio extension

AUDIO_EXTENSION = "mp3"

# ============================================================
# FFMPEG CONFIGURATION
# ============================================================

FFMPEG_BINARY = "ffmpeg"

FFPROBE_BINARY = "ffprobe"

FFMPEG_LOGLEVEL = "warning"

# Hide FFmpeg startup banner

HIDE_FFMPEG_BANNER = True

# ============================================================
# STREAM RECONNECTION
# ============================================================

ENABLE_RECONNECT = True

INITIAL_RECONNECT_DELAY = 5

MAX_RECONNECT_DELAY = 60

RECONNECT_MULTIPLIER = 2

# ============================================================
# THREADING
# ============================================================

# One recording thread per station

THREAD_PER_STATION = True

MAX_THREADS = multiprocessing.cpu_count() * 2

THREAD_DAEMON = True

# ============================================================
# FILE VALIDATION
# ============================================================

VERIFY_FILE_EXISTS = True

VERIFY_NON_ZERO_SIZE = True

VERIFY_WITH_FFPROBE = True

GENERATE_SHA256 = True

# ============================================================
# METADATA
# ============================================================

GENERATE_METADATA = True

SAVE_STREAM_INFORMATION = True

SAVE_CAPTURE_STATISTICS = True

SAVE_FFMPEG_VERSION = True

SAVE_SYSTEM_INFORMATION = True

# ============================================================
# DATASET VERSIONING
# ============================================================

DATASET_VERSION = "1.0"

DATASET_LICENSE = "Research Only"

DATASET_LANGUAGE = [

    "English",

    "Twi",

    "Ga",

    "Ewe",

]

# ============================================================
# LOGGING
# ============================================================

LOG_LEVEL = "INFO"

LOG_TO_CONSOLE = True

LOG_TO_FILE = True

ROTATE_LOGS_DAILY = True

KEEP_LOGS_DAYS = 30

# ============================================================
# REPORT GENERATION
# ============================================================

GENERATE_DAILY_REPORT = True

GENERATE_DATASET_MANIFEST = True

GENERATE_CAPTURE_STATISTICS = True

# ============================================================
# MACHINE LEARNING PIPELINE FLAGS
# (Reserved for future versions)
# ============================================================

RUN_DEEP_MUSIC_DETECTOR = False

RUN_SOURCE_SEPARATOR = False

RUN_FINGERPRINT_GENERATOR = False

# ============================================================
# RANDOMNESS
# ============================================================

RANDOM_SEED = 42

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def initialize_directories():
    """
    Creates every directory required by the framework.
    """

    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)


def print_configuration():
    """
    Prints the current configuration.
    Useful for debugging.
    """

    print("=" * 60)
    print(PROJECT_NAME)
    print("=" * 60)

    print(f"Version           : {PROJECT_VERSION}")
    print(f"Dataset           : {DATASET_NAME}")
    print(f"Country           : {COUNTRY}")
    print(f"Segment Duration  : {SEGMENT_DURATION}s")
    print(f"Stations File     : {STATIONS_FILE}")
    print(f"Raw Audio         : {RAW_AUDIO_DIR}")
    print(f"Metadata          : {METADATA_DIR}")
    print(f"Logs              : {LOG_DIR}")
    print(f"Reports           : {REPORT_DIR}")

    print("=" * 60)


if __name__ == "__main__":

    initialize_directories()

    print_configuration()