"""
==============================================================
G-Radio Acquisition Framework (GRAF)
System Information Utility

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import platform
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

COMMON_BINARY_PATHS = [
    Path("/usr/local/bin"),
    Path("/opt/homebrew/bin"),
    Path("/usr/bin"),
]

def find_binary(binary_name: str) -> Optional[str]:
    """Find absolute path of binary, searching standard PATH and common locations."""
    path = shutil.which(binary_name)
    if path:
        return path

    for common_dir in COMMON_BINARY_PATHS:
        candidate = common_dir / binary_name
        if candidate.exists() and candidate.is_file():
            return str(candidate)

    return None

def get_ffmpeg_version(binary: str = "ffmpeg") -> str:
    """Retrieve installed FFmpeg version string."""
    binary_path = find_binary(binary)
    if not binary_path:
        return "Not Installed"

    try:
        res = subprocess.run(
            [binary_path, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
        )
        if res.returncode == 0:
            first_line = res.stdout.splitlines()[0] if res.stdout else ""
            return first_line.strip()
    except Exception as e:
        return f"Error: {e}"
    return "Unknown"

def get_ffprobe_version(binary: str = "ffprobe") -> str:
    """Retrieve installed FFprobe version string."""
    binary_path = find_binary(binary)
    if not binary_path:
        return "Not Installed"

    try:
        res = subprocess.run(
            [binary_path, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
        )
        if res.returncode == 0:
            first_line = res.stdout.splitlines()[0] if res.stdout else ""
            return first_line.strip()
    except Exception as e:
        return f"Error: {e}"
    return "Unknown"

def system_information() -> Dict[str, Any]:
    """Collect platform hardware, OS, and Python details."""
    return {
        "os_name": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version.split()[0],
        "python_implementation": platform.python_implementation(),
        "hostname": platform.node(),
        "ffmpeg_binary": find_binary("ffmpeg"),
        "ffprobe_binary": find_binary("ffprobe"),
    }
