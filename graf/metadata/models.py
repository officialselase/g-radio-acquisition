"""
==============================================================
G-Radio Acquisition Framework (GRAF)
G-Radio Metadata Specification (GRMS-1.0) Models

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

from graf.config import config
from graf.utils.system import system_information

@dataclass
class DatasetInfo:
    name: str = config.dataset.dataset_name
    version: str = config.dataset.dataset_version
    country: str = config.dataset.country
    timezone: str = config.dataset.timezone
    license: str = config.dataset.license

@dataclass
class FrameworkInfo:
    name: str = config.dataset.project_name
    version: str = config.dataset.project_version

@dataclass
class StationInfo:
    id: str = ""
    name: str = ""
    stream_url: str = ""
    broadcast_type: str = "FM"
    frequency: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: str = "Ghana"
    language: List[str] = field(default_factory=list)
    genre: Optional[str] = None
    owner: Optional[str] = None

@dataclass
class CaptureInfo:
    start_time: str = ""
    end_time: str = ""
    utc_time: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    duration_seconds: float = 0.0
    segment_number: int = 1
    sequence: Dict[str, Any] = field(default_factory=lambda: {"index": 1, "previous": None, "next": None})

@dataclass
class FileInfo:
    filename: str = ""
    extension: str = ".mp3"
    absolute_path: str = ""
    size_bytes: int = 0
    sha256: str = ""
    md5: str = ""

@dataclass
class AudioInfo:
    codec: str = ""
    sample_rate: int = 0
    channels: int = 0
    bit_rate: int = 0
    container: str = "mp3"
    duration: float = 0.0

@dataclass
class AnnotationInfo:
    annotated: bool = False
    annotation_version: str = "1.0"
    annotator: Optional[str] = None
    reviewer: Optional[str] = None
    reviewed: bool = False
    annotation_date: Optional[str] = None
    confidence: Optional[float] = None
    quality_score: Optional[float] = None
    notes: Optional[str] = None
    primary_language: Optional[str] = None
    secondary_language: Optional[str] = None
    program_type: Optional[str] = None
    contains_music: Optional[bool] = None
    contains_speech: Optional[bool] = None
    contains_advertisement: Optional[bool] = None
    contains_news: Optional[bool] = None
    contains_jingle: Optional[bool] = None
    contains_phone_call: Optional[bool] = None
    contains_applause: Optional[bool] = None
    contains_laughter: Optional[bool] = None
    contains_live_event: Optional[bool] = None
    contains_background_noise: Optional[bool] = None
    contains_silence: Optional[bool] = None

@dataclass
class InterferenceInfo:
    presenter_over_music: Optional[bool] = None
    multiple_speakers: Optional[bool] = None
    caller_audio: Optional[bool] = None
    advertisement_overlay: Optional[bool] = None
    station_jingle_overlay: Optional[bool] = None
    crossfade: Optional[bool] = None
    background_music: Optional[bool] = None
    crowd_noise: Optional[bool] = None
    vehicle_noise: Optional[bool] = None
    microphone_noise: Optional[bool] = None
    microphone_clipping: Optional[bool] = None
    echo: Optional[bool] = None
    reverb: Optional[bool] = None
    compression_artifacts: Optional[bool] = None
    packet_loss: Optional[bool] = None
    signal_dropout: Optional[bool] = None
    signal_distortion: Optional[bool] = None
    simultaneous_music: Optional[bool] = None
    interference_score: Optional[float] = None

@dataclass
class FingerprintingInfo:
    reference_song: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    label: Optional[str] = None
    genre: Optional[str] = None
    is_ground_truth: bool = False
    ground_truth_start: Optional[float] = None
    ground_truth_end: Optional[float] = None
    matched: bool = False
    matched_song: Optional[str] = None
    matched_artist: Optional[str] = None
    match_confidence: Optional[float] = None
    embedding_id: Optional[str] = None
    embedding_dimension: Optional[int] = None
    top5_candidates: List[str] = field(default_factory=list)

@dataclass
class MachineLearningInfo:
    dataset_split: Optional[str] = None
    fold: Optional[int] = None
    excluded: bool = False
    exclusion_reason: Optional[str] = None
    speech_music_ratio: Optional[float] = None
    estimated_snr: Optional[float] = None
    music_detector_score: Optional[float] = None
    speech_detector_score: Optional[float] = None
    source_separation_model: Optional[str] = None
    fingerprint_model: Optional[str] = None
    embedding_generated: bool = False
    embedding_path: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class ProvenanceInfo:
    dataset_release: str = "v1.0"
    metadata_version: str = "GRMS-1.0"
    generated_by: str = "GRAF"
    generated_on: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    verified: bool = False
    verification_date: Optional[str] = None
    verification_method: Optional[str] = None

@dataclass
class FFmpegInfo:
    version: str = ""
    ffprobe_version: str = ""
    command: str = ""
    capture_method: str = "Stream Copy"

@dataclass
class ProcessingStatus:
    captured: bool = True
    validated: bool = False
    annotated: bool = False
    music_detected: bool = False
    source_separated: bool = False
    fingerprint_generated: bool = False
    fingerprint_matched: bool = False
    benchmarked: bool = False
    archived: bool = False
    published: bool = False

@dataclass
class GRMSMetadata:
    """
    Root object for the G-Radio Metadata Specification (GRMS-1.0).
    """
    capture_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    dataset: DatasetInfo = field(default_factory=DatasetInfo)
    framework: FrameworkInfo = field(default_factory=FrameworkInfo)
    station: StationInfo = field(default_factory=StationInfo)
    capture: CaptureInfo = field(default_factory=CaptureInfo)
    audio: AudioInfo = field(default_factory=AudioInfo)
    file: FileInfo = field(default_factory=FileInfo)
    annotation: AnnotationInfo = field(default_factory=AnnotationInfo)
    interference: InterferenceInfo = field(default_factory=InterferenceInfo)
    fingerprinting: FingerprintingInfo = field(default_factory=FingerprintingInfo)
    machine_learning: MachineLearningInfo = field(default_factory=MachineLearningInfo)
    provenance: ProvenanceInfo = field(default_factory=ProvenanceInfo)
    system: Dict[str, Any] = field(default_factory=system_information)
    ffmpeg: FFmpegInfo = field(default_factory=FFmpegInfo)
    processing_status: ProcessingStatus = field(default_factory=ProcessingStatus)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata dataclass tree into a python dict."""
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        """Serialize metadata object to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, json_path: Path) -> None:
        """Save metadata JSON to file."""
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GRMSMetadata":
        """Reconstruct GRMSMetadata from dict."""
        instance = cls()
        if "capture_id" in data:
            instance.capture_id = data["capture_id"]
        if "dataset" in data and isinstance(data["dataset"], dict):
            instance.dataset = DatasetInfo(**data["dataset"])
        if "framework" in data and isinstance(data["framework"], dict):
            instance.framework = FrameworkInfo(**data["framework"])
        if "station" in data and isinstance(data["station"], dict):
            instance.station = StationInfo(**data["station"])
        if "capture" in data and isinstance(data["capture"], dict):
            instance.capture = CaptureInfo(**data["capture"])
        if "audio" in data and isinstance(data["audio"], dict):
            instance.audio = AudioInfo(**data["audio"])
        if "file" in data and isinstance(data["file"], dict):
            instance.file = FileInfo(**data["file"])
        if "annotation" in data and isinstance(data["annotation"], dict):
            instance.annotation = AnnotationInfo(**data["annotation"])
        if "interference" in data and isinstance(data["interference"], dict):
            instance.interference = InterferenceInfo(**data["interference"])
        if "fingerprinting" in data and isinstance(data["fingerprinting"], dict):
            instance.fingerprinting = FingerprintingInfo(**data["fingerprinting"])
        if "machine_learning" in data and isinstance(data["machine_learning"], dict):
            instance.machine_learning = MachineLearningInfo(**data["machine_learning"])
        if "provenance" in data and isinstance(data["provenance"], dict):
            instance.provenance = ProvenanceInfo(**data["provenance"])
        if "system" in data and isinstance(data["system"], dict):
            instance.system = data["system"]
        if "ffmpeg" in data and isinstance(data["ffmpeg"], dict):
            instance.ffmpeg = FFmpegInfo(**data["ffmpeg"])
        if "processing_status" in data and isinstance(data["processing_status"], dict):
            instance.processing_status = ProcessingStatus(**data["processing_status"])
        return instance

    @classmethod
    def load(cls, json_path: Path) -> "GRMSMetadata":
        """Load GRMSMetadata from a JSON file."""
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
