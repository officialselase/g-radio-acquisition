"""
==============================================================
G-Radio Metadata Specification (GRMS-1.0)
Top-Level Module Wrapper

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

from graf.metadata import (
    GRMSMetadata,
    DatasetInfo,
    FrameworkInfo,
    StationInfo,
    CaptureInfo,
    FileInfo,
    AudioInfo,
    AnnotationInfo,
    InterferenceInfo,
    FingerprintingInfo,
    MachineLearningInfo,
    ProvenanceInfo,
    FFmpegInfo,
    ProcessingStatus,
    MetadataBuilder,
    validate_metadata,
    validate_grms_dict,
)
from graf.utils.system import system_information, get_ffmpeg_version
from graf.utils.audio import (
    compute_sha256 as sha256,
    compute_md5 as md5,
    get_file_size as file_size,
    probe_audio_properties as audio_properties,
)

ffmpeg_version = get_ffmpeg_version

if __name__ == "__main__":
    builder = MetadataBuilder()
    print("GRMS Metadata Module initialized successfully.")