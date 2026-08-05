"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Audio Utility Module

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

from graf.utils.system import find_binary

def compute_sha256(filepath: Path) -> str:
    """Calculate SHA-256 checksum of a file."""
    if not filepath.is_file():
        return ""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def compute_md5(filepath: Path) -> str:
    """Calculate MD5 checksum of a file."""
    if not filepath.is_file():
        return ""
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_file_size(filepath: Path) -> int:
    """Return size of file in bytes."""
    if not filepath.is_file():
        return 0
    return filepath.stat().st_size

def probe_audio_properties(filepath: Path, ffprobe_binary: str = "ffprobe") -> Dict[str, Any]:
    """
    Probe audio file metadata and audio stream metrics using ffprobe.
    Returns structured properties: codec, sample_rate, channels, bit_rate, duration, container.
    """
    binary_path = find_binary(ffprobe_binary)
    default_res = {
        "codec": "unknown",
        "sample_rate": 0,
        "channels": 0,
        "bit_rate": 0,
        "container": filepath.suffix.lstrip(".").lower(),
        "duration": 0.0,
        "valid": False,
        "error": None,
    }

    if not filepath.is_file() or filepath.stat().st_size == 0:
        default_res["error"] = "File non-existent or zero byte"
        return default_res

    if not binary_path:
        default_res["error"] = "FFprobe binary not found"
        return default_res

    cmd = [
        binary_path,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(filepath.resolve())
    ]

    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)
        if res.returncode != 0:
            default_res["error"] = f"FFprobe exit code {res.returncode}"
            return default_res

        data = json.loads(res.stdout)
        format_info = data.get("format", {})
        streams = data.get("streams", [])

        audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})

        codec = audio_stream.get("codec_name", format_info.get("format_name", "unknown"))
        sample_rate = int(audio_stream.get("sample_rate", 0))
        channels = int(audio_stream.get("channels", 0))
        
        bit_rate_str = audio_stream.get("bit_rate") or format_info.get("bit_rate") or "0"
        try:
            bit_rate = int(bit_rate_str)
        except ValueError:
            bit_rate = 0

        duration_str = format_info.get("duration") or audio_stream.get("duration") or "0.0"
        try:
            duration = float(duration_str)
        except ValueError:
            duration = 0.0

        container = format_info.get("format_name", filepath.suffix.lstrip(".").lower())

        return {
            "codec": codec,
            "sample_rate": sample_rate,
            "channels": channels,
            "bit_rate": bit_rate,
            "container": container,
            "duration": round(duration, 3),
            "valid": True,
            "error": None,
        }
    except Exception as e:
        default_res["error"] = str(e)
        return default_res
