"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Metadata Builder

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from graf.metadata.models import (
    GRMSMetadata, StationInfo, CaptureInfo, FileInfo, AudioInfo, FFmpegInfo
)
from graf.utils.system import get_ffmpeg_version, get_ffprobe_version, system_information
from graf.utils.audio import (
    compute_sha256, compute_md5, get_file_size, probe_audio_properties
)

class MetadataBuilder:
    """
    Constructs comprehensive GRMSMetadata objects for acquired audio segments.
    """
    def __init__(self, ffmpeg_binary: str = "ffmpeg", ffprobe_binary: str = "ffprobe"):
        self.ffmpeg_binary = ffmpeg_binary
        self.ffprobe_binary = ffprobe_binary
        self.ffmpeg_version_str = get_ffmpeg_version(ffmpeg_binary)
        self.ffprobe_version_str = get_ffprobe_version(ffprobe_binary)

    def build(
        self,
        station_name: str,
        stream_url: str,
        audio_file: Path,
        capture_start: datetime,
        capture_end: datetime,
        station_id: str = "",
        frequency: Optional[str] = None,
        city: Optional[str] = None,
        region: Optional[str] = None,
        languages: Optional[List[str]] = None,
        genre: Optional[str] = None,
        owner: Optional[str] = None,
        segment_number: int = 1,
        sequence_info: Optional[Dict[str, Any]] = None,
    ) -> GRMSMetadata:
        """Construct full GRMSMetadata object for an audio segment."""
        metadata = GRMSMetadata()

        # Station info
        metadata.station.id = station_id
        metadata.station.name = station_name
        metadata.station.stream_url = stream_url
        metadata.station.frequency = frequency
        metadata.station.city = city
        metadata.station.region = region
        metadata.station.language = languages or []
        metadata.station.genre = genre
        metadata.station.owner = owner

        # Capture info
        duration_sec = (capture_end - capture_start).total_seconds()
        metadata.capture.start_time = capture_start.isoformat()
        metadata.capture.end_time = capture_end.isoformat()
        metadata.capture.duration_seconds = max(0.0, duration_sec)
        metadata.capture.segment_number = segment_number
        if sequence_info:
            metadata.capture.sequence = sequence_info

        # File info
        resolved_path = audio_file.resolve()
        metadata.file.filename = audio_file.name
        metadata.file.extension = audio_file.suffix
        metadata.file.absolute_path = str(resolved_path)
        metadata.file.size_bytes = get_file_size(resolved_path)
        metadata.file.sha256 = compute_sha256(resolved_path)
        metadata.file.md5 = compute_md5(resolved_path)

        # Audio properties
        audio_props = probe_audio_properties(resolved_path, self.ffprobe_binary)
        metadata.audio.codec = audio_props.get("codec", "unknown")
        metadata.audio.sample_rate = audio_props.get("sample_rate", 0)
        metadata.audio.channels = audio_props.get("channels", 0)
        metadata.audio.bit_rate = audio_props.get("bit_rate", 0)
        metadata.audio.container = audio_props.get("container", audio_file.suffix.lstrip("."))
        metadata.audio.duration = audio_props.get("duration", 0.0)

        # FFmpeg & system provenance
        metadata.ffmpeg.version = self.ffmpeg_version_str
        metadata.ffmpeg.ffprobe_version = self.ffprobe_version_str
        metadata.ffmpeg.capture_method = "Stream Copy"
        metadata.system = system_information()

        return metadata
