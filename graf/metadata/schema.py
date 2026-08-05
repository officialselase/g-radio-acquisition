"""
==============================================================
G-Radio Acquisition Framework (GRAF)
GRMS Schema & Validation Helper

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

from typing import Dict, Any, Tuple
from graf.metadata.models import GRMSMetadata

GRMS_SCHEMA_VERSION = "1.0"

def validate_grms_dict(data: Dict[str, Any], require_station: bool = False) -> Tuple[bool, str]:
    """Validate python dictionary against GRMS-1.0 structural expectations."""
    required_sections = ["capture_id", "dataset", "station", "capture", "file", "audio", "processing_status"]
    for section in required_sections:
        if section not in data:
            return False, f"Missing required GRMS metadata section: {section}"

    station_data = data.get("station", {})
    if not isinstance(station_data, dict):
        return False, "Station section must be a dictionary"

    if require_station and not station_data.get("name"):
        return False, "Station section must contain a non-empty 'name' field"

    file_data = data.get("file", {})
    if not isinstance(file_data, dict):
        return False, "File section must be a dictionary"

    return True, "Valid GRMS-1.0 Metadata"

def validate_metadata(metadata: GRMSMetadata, require_station: bool = False) -> Tuple[bool, str]:
    """Validate GRMSMetadata instance."""
    return validate_grms_dict(metadata.to_dict(), require_station=require_station)
