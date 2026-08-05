"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Audio Segment Validation & QA Engine

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

from graf.config import config
from graf.logger import info, warning, error, file_verified
from graf.metadata.models import GRMSMetadata
from graf.utils.audio import (
    compute_sha256, compute_md5, get_file_size, probe_audio_properties
)
from graf.utils.system import find_binary

@dataclass
class ValidationResult:
    is_valid: bool
    audio_path: Path
    metadata_path: Optional[Path] = None
    size_bytes: int = 0
    sha256: str = ""
    md5: str = ""
    duration: float = 0.0
    codec: str = ""
    errors: list = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []

class SegmentValidator:
    """
    Validates captured audio segments for data integrity, checksum accuracy, and ffprobe stream validity.
    Quarantines corrupted files to storage/failed/ directory.
    """
    def __init__(
        self,
        failed_dir: Optional[Path] = None,
        ffprobe_binary: Optional[str] = None
    ):
        self.failed_dir = failed_dir or config.paths.failed_dir
        self.ffprobe_binary = ffprobe_binary or find_binary(config.ffmpeg.ffprobe_binary) or "ffprobe"

    def validate_segment(
        self,
        audio_path: Path,
        metadata_path: Optional[Path] = None,
        quarantine_on_failure: bool = True
    ) -> ValidationResult:
        """
        Validate a single raw audio segment and its associated metadata JSON file.
        """
        errors = []
        resolved_audio = audio_path.resolve()

        if not resolved_audio.exists():
            return ValidationResult(
                is_valid=False,
                audio_path=audio_path,
                metadata_path=metadata_path,
                errors=["Audio file does not exist"]
            )

        # 1. Non-zero byte check
        size_bytes = get_file_size(resolved_audio)
        if size_bytes == 0:
            errors.append("Audio file size is 0 bytes")

        # 2. Compute checksums
        sha256_hash = compute_sha256(resolved_audio)
        md5_hash = compute_md5(resolved_audio)

        # 3. FFprobe media probe check
        probe_res = probe_audio_properties(resolved_audio, ffprobe_binary=self.ffprobe_binary)
        if not probe_res.get("valid", False):
            err_msg = probe_res.get("error") or "Failed FFprobe media stream verification"
            errors.append(err_msg)

        codec = probe_res.get("codec", "unknown")
        duration = probe_res.get("duration", 0.0)

        # 4. Metadata sync validation (if metadata JSON provided)
        resolved_meta = None
        if metadata_path and metadata_path.exists():
            resolved_meta = metadata_path.resolve()
            try:
                meta = GRMSMetadata.load(resolved_meta)
                # Check SHA256 matches metadata record if recorded
                if meta.file.sha256 and meta.file.sha256 != sha256_hash:
                    errors.append(f"SHA256 mismatch: actual={sha256_hash}, recorded={meta.file.sha256}")
            except Exception as e:
                errors.append(f"Corrupt metadata JSON: {e}")

        is_valid = len(errors) == 0
        result = ValidationResult(
            is_valid=is_valid,
            audio_path=resolved_audio,
            metadata_path=resolved_meta,
            size_bytes=size_bytes,
            sha256=sha256_hash,
            md5=md5_hash,
            duration=duration,
            codec=codec,
            errors=errors
        )

        if is_valid:
            file_verified("GRAF-QA", resolved_audio.name)
            # Update processing status if metadata exists
            if resolved_meta and resolved_meta.exists():
                try:
                    meta = GRMSMetadata.load(resolved_meta)
                    meta.processing_status.validated = True
                    meta.file.sha256 = sha256_hash
                    meta.file.md5 = md5_hash
                    meta.file.size_bytes = size_bytes
                    meta.audio.duration = duration
                    meta.audio.codec = codec
                    meta.save(resolved_meta)
                except Exception:
                    pass
        else:
            warning(f"[GRAF-QA] Validation failed for {resolved_audio.name}: {errors}")
            if quarantine_on_failure:
                self.quarantine(resolved_audio, resolved_meta, errors)

        return result

    def quarantine(
        self,
        audio_path: Path,
        metadata_path: Optional[Path] = None,
        reasons: list = None
    ) -> None:
        """Move corrupted or invalid audio segment to quarantine storage."""
        self.failed_dir.mkdir(parents=True, exist_ok=True)
        target_audio = self.failed_dir / audio_path.name
        try:
            shutil.move(str(audio_path), str(target_audio))
            error(f"[GRAF-QA] Quarantined corrupt segment: {audio_path.name} -> {target_audio}")

            if metadata_path and metadata_path.exists():
                target_meta = self.failed_dir / metadata_path.name
                shutil.move(str(metadata_path), str(target_meta))
        except Exception as e:
            error(f"[GRAF-QA] Failed to quarantine segment {audio_path.name}: {e}")
