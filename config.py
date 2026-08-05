"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Configuration File (Top-level Wrapper)

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

from graf.config import config, GRAFConfig, PathConfig, AudioConfig, FFmpegConfig

# Backwards compatibility top-level constants
PROJECT_NAME = config.dataset.project_name
PROJECT_VERSION = config.dataset.project_version
DATASET_NAME = config.dataset.dataset_name
DATASET_VERSION = config.dataset.dataset_version
COUNTRY = config.dataset.country
TIMEZONE = config.dataset.timezone

BASE_DIR = config.paths.base_dir
STORAGE_DIR = config.paths.storage_dir
RAW_AUDIO_DIR = config.paths.raw_audio_dir
METADATA_DIR = config.paths.metadata_dir
LOG_DIR = config.paths.log_dir
REPORT_DIR = config.paths.report_dir
FAILED_DIR = config.paths.failed_dir
CACHE_DIR = config.paths.cache_dir
ANNOTATION_DIR = config.paths.annotation_dir
TEMP_DIR = config.paths.temp_dir
STATIONS_FILE = config.paths.stations_file

DIRECTORIES = [
    STORAGE_DIR, RAW_AUDIO_DIR, METADATA_DIR, LOG_DIR,
    REPORT_DIR, FAILED_DIR, CACHE_DIR, ANNOTATION_DIR, TEMP_DIR
]

SEGMENT_DURATION = config.audio.segment_duration
COPY_AUDIO_STREAM = config.audio.copy_audio_stream
AUDIO_EXTENSION = config.audio.audio_extension

FFMPEG_BINARY = config.ffmpeg.ffmpeg_binary
FFPROBE_BINARY = config.ffmpeg.ffprobe_binary
FFMPEG_LOGLEVEL = config.ffmpeg.ffmpeg_loglevel
HIDE_FFMPEG_BANNER = config.ffmpeg.hide_banner

ENABLE_RECONNECT = config.reconnect.enable_reconnect
INITIAL_RECONNECT_DELAY = config.reconnect.initial_delay
MAX_RECONNECT_DELAY = config.reconnect.max_delay
RECONNECT_MULTIPLIER = config.reconnect.multiplier

LOG_LEVEL = config.logging.log_level
LOG_TO_CONSOLE = config.logging.log_to_console
LOG_TO_FILE = config.logging.log_to_file
ROTATE_LOGS_DAILY = config.logging.rotate_daily
KEEP_LOGS_DAYS = config.logging.keep_days

DATASET_LICENSE = config.dataset.license
DATASET_LANGUAGE = config.dataset.languages
RANDOM_SEED = config.random_seed

def initialize_directories():
    config.paths.initialize_directories()

def print_configuration():
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