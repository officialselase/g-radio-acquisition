import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

{
    "capture_id": "UUID",

    "dataset": {
        "name": "G-Radio",
        "version": "1.0",
        "country": "Ghana",
        "timezone": "Africa/Accra"
    },

    "framework": {
        "name": "GRAF",
        "version": "1.0.0"
    },

    "station": {
        "name": "Peace FM",
        "stream_url": "...",
        "broadcast_type": "FM",
        "city": "Accra",
        "language": [
            "Twi",
            "English"
        ]
    },

    "capture": {
        "start_time": "...",
        "end_time": "...",
        "duration_seconds": 600
    },

    "file": {
        "filename": "...",
        "extension": ".mp3",
        "size_bytes": 12345678,
        "sha256": "...",
        "duration": 600.04
    },

    "audio": {
        "codec": "mp3",
        "sample_rate": 44100,
        "channels": 2,
        "bit_rate": 128000
    },

    "annotation": {

        "annotated": false,

        "annotator": null,

        "reviewer": null,

        "annotation_date": null,

        "quality_score": null,

        "confidence": null,

        "notes": null,

        "primary_language": null,

        "secondary_language": null,

        "program_type": null,

        "contains_music": null,

        "contains_speech": null,

        "contains_advertisement": null,

        "contains_jingle": null,

        "contains_news": null,

        "contains_phone_call": null,

        "contains_laughter": null,

        "contains_applause": null,

        "contains_background_noise": null,

        "contains_live_event": null,

        "contains_commentary": null,

        "contains_silence": null
    },

    "research": {

        "speech_music_ratio": null,

        "estimated_snr": null,

        "music_detector_score": null,

        "speech_detector_score": null,

        "interference_level": null,

        "broadcast_overlap": null,

        "source_separation_model": null,

        "fingerprint_embedding_id": null
    },

    "system": {},

    "ffmpeg": {}
}
# ============================================================
# Annotation
# ============================================================

@dataclass
class AnnotationInfo:
    """
    Human annotation information.
    These values are intentionally left as None until
    the sample has been manually annotated.
    """

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


# ============================================================
# Broadcast Interference
# ============================================================

@dataclass
class InterferenceInfo:
    """
    Labels describing real-world broadcast interference.
    These labels are one of the key contributions of
    the Rob-GhanaRadio dataset.
    """

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


# ============================================================
# Fingerprinting
# ============================================================

@dataclass
class FingerprintingInfo:
    """
    Ground-truth and fingerprint matching information.
    Filled during benchmarking, not acquisition.
    """

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


# ============================================================
# Machine Learning
# ============================================================

@dataclass
class MachineLearningInfo:
    """
    Information used during model development.
    """

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


# ============================================================
# Provenance
# ============================================================

@dataclass
class ProvenanceInfo:
    """
    Dataset provenance.
    Critical for reproducibility.
    """

    dataset_release: str = "v1.0"

    metadata_version: str = "GRMS-1.0"

    generated_by: str = "GRAF"

    generated_on: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    verified: bool = False

    verification_date: Optional[str] = None

    verification_method: Optional[str] = None


# ============================================================
# FFmpeg
# ============================================================

@dataclass
class FFmpegInfo:

    version: str = ""

    ffprobe_version: str = ""

    command: str = ""

    capture_method: str = "Stream Copy"


# ============================================================
# Root Metadata Object
# ============================================================
@dataclass
class ProcessingStatus:
    captured: bool = True
    validated: bool = False
    annotated: bool = False
    music_detected: bool = False
    separated: bool = False
    fingerprinted: bool = False
    matched: bool = False
    published: bool = False

@dataclass
class GRMSMetadata:
    """
    Root object for the G-Radio Metadata Specification (GRMS).
    """

    capture_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    dataset: DatasetInfo = field(default_factory=DatasetInfo)

    framework: FrameworkInfo = field(default_factory=FrameworkInfo)

    station: StationInfo = field(default_factory=StationInfo)

    capture: CaptureInfo = field(default_factory=CaptureInfo)

    audio: AudioInfo = field(default_factory=AudioInfo)

    file: FileInfo = field(default_factory=FileInfo)

    annotation: AnnotationInfo = field(default_factory=AnnotationInfo)

    interference: InterferenceInfo = field(default_factory=InterferenceInfo)

    fingerprinting: FingerprintingInfo = field(
        default_factory=FingerprintingInfo
    )

    machine_learning: MachineLearningInfo = field(
        default_factory=MachineLearningInfo
    )

    provenance: ProvenanceInfo = field(
        default_factory=ProvenanceInfo
    )

    system: Dict[str, Any] = field(
        default_factory=system_information
    )

    ffmpeg: FFmpegInfo = field(default_factory=FFmpegInfo)

    processing_status: ProcessingStatus = field(default_factory=ProcessingStatus)