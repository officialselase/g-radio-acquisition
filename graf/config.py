"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Configuration Module

Author : Selase K. Agbai
Project: Rob-GhanaRadio
Purpose: Centralized, typed configuration for GRAF.
==============================================================
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# Base directory for the repository
BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass
class PathConfig:
    base_dir: Path = BASE_DIR
    storage_dir: Path = field(default_factory=lambda: BASE_DIR / "storage")
    raw_audio_dir: Path = field(default_factory=lambda: BASE_DIR / "storage" / "raw")
    metadata_dir: Path = field(default_factory=lambda: BASE_DIR / "storage" / "metadata")
    log_dir: Path = field(default_factory=lambda: BASE_DIR / "storage" / "logs")
    report_dir: Path = field(default_factory=lambda: BASE_DIR / "storage" / "reports")
    failed_dir: Path = field(default_factory=lambda: BASE_DIR / "storage" / "failed")
    cache_dir: Path = field(default_factory=lambda: BASE_DIR / "storage" / "cache")
    annotation_dir: Path = field(default_factory=lambda: BASE_DIR / "storage" / "annotations")
    temp_dir: Path = field(default_factory=lambda: BASE_DIR / "storage" / "temp")
    stations_file: Path = field(default_factory=lambda: BASE_DIR / "stations" / "ghana_stations.json")

    def initialize_directories(self) -> None:
        """Create all required directories if they do not exist."""
        directories = [
            self.storage_dir,
            self.raw_audio_dir,
            self.metadata_dir,
            self.log_dir,
            self.report_dir,
            self.failed_dir,
            self.cache_dir,
            self.annotation_dir,
            self.temp_dir,
            self.stations_file.parent,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

@dataclass
class AudioConfig:
    segment_duration: int = int(os.getenv("GRAF_SEGMENT_DURATION", "600"))
    copy_audio_stream: bool = os.getenv("GRAF_COPY_STREAM", "True").lower() in ("true", "1", "yes")
    audio_extension: str = os.getenv("GRAF_AUDIO_EXTENSION", "mp3")
    sample_rate: int = int(os.getenv("GRAF_SAMPLE_RATE", "44100"))
    channels: int = int(os.getenv("GRAF_CHANNELS", "2"))
    bit_rate: int = int(os.getenv("GRAF_BIT_RATE", "128000"))

@dataclass
class FFmpegConfig:
    ffmpeg_binary: str = os.getenv("GRAF_FFMPEG_BINARY", "ffmpeg")
    ffprobe_binary: str = os.getenv("GRAF_FFPROBE_BINARY", "ffprobe")
    ffmpeg_loglevel: str = os.getenv("GRAF_FFMPEG_LOGLEVEL", "warning")
    hide_banner: bool = True

@dataclass
class StreamReconnectConfig:
    enable_reconnect: bool = True
    initial_delay: int = 5
    max_delay: int = 60
    multiplier: float = 2.0
    max_retries: int = 10

@dataclass
class DatasetConfig:
    project_name: str = "G-Radio Acquisition Framework"
    project_version: str = "1.0.0"
    dataset_name: str = "G-Radio"
    dataset_version: str = "1.0"
    country: str = "Ghana"
    timezone: str = "Africa/Accra"
    license: str = "Research Only"
    languages: List[str] = field(default_factory=lambda: ["English", "Twi", "Ga", "Ewe"])

@dataclass
class LoggingConfig:
    log_level: str = os.getenv("GRAF_LOG_LEVEL", "INFO")
    log_to_console: bool = True
    log_to_file: bool = True
    rotate_daily: bool = True
    keep_days: int = 30

@dataclass
class GRAFConfig:
    paths: PathConfig = field(default_factory=PathConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    ffmpeg: FFmpegConfig = field(default_factory=FFmpegConfig)
    reconnect: StreamReconnectConfig = field(default_factory=StreamReconnectConfig)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    random_seed: int = 42

    def __post_init__(self):
        self.paths.initialize_directories()

    def print_configuration(self) -> None:
        print("=" * 60)
        print(self.dataset.project_name)
        print("=" * 60)
        print(f"Version           : {self.dataset.project_version}")
        print(f"Dataset           : {self.dataset.dataset_name}")
        print(f"Country           : {self.dataset.country}")
        print(f"Segment Duration  : {self.audio.segment_duration}s")
        print(f"Stations File     : {self.paths.stations_file}")
        print(f"Raw Audio         : {self.paths.raw_audio_dir}")
        print(f"Metadata          : {self.paths.metadata_dir}")
        print(f"Logs              : {self.paths.log_dir}")
        print(f"Reports           : {self.paths.report_dir}")
        print("=" * 60)

# Default global instance
config = GRAFConfig()

def print_configuration() -> None:
    config.print_configuration()

def initialize_directories() -> None:
    config.paths.initialize_directories()


