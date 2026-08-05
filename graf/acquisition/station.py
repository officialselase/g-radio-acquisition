"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Station Registry & Data Model

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from graf.config import config

@dataclass
class Station:
    id: str
    name: str
    frequency: str
    city: str
    region: str
    country: str
    stream_url: str
    fallback_urls: List[str] = field(default_factory=list)
    broadcast_type: str = "FM"
    languages: List[str] = field(default_factory=list)
    genre: str = ""
    owner: str = ""
    active: bool = True

    def get_all_stream_urls(self) -> List[str]:
        """Return primary stream URL followed by fallback URLs."""
        urls = [self.stream_url]
        urls.extend([u for u in self.fallback_urls if u != self.stream_url])
        return urls

class StationRegistry:
    """
    Loads, filters, and manages Ghanaian radio station configurations.
    """
    def __init__(self, stations_file: Optional[Path] = None):
        self.stations_file = stations_file or config.paths.stations_file
        self.stations: List[Station] = []
        self.load()

    def load(self) -> None:
        """Load stations from JSON file."""
        if not self.stations_file.is_file():
            raise FileNotFoundError(f"Station registry file not found: {self.stations_file}")

        with open(self.stations_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.stations = [Station(**item) for item in data if item.get("active", True)]

    def get_all(self) -> List[Station]:
        return [s for s in self.stations if s.active]

    def get_by_id(self, station_id: str) -> Optional[Station]:
        for station in self.stations:
            if station.id.lower() == station_id.lower():
                return station
        return None

    def filter(
        self,
        language: Optional[str] = None,
        city: Optional[str] = None,
        region: Optional[str] = None
    ) -> List[Station]:
        """Filter stations matching language, city, or region."""
        filtered = self.get_all()
        if language:
            lang_lower = language.lower()
            filtered = [s for s in filtered if any(lang_lower in l.lower() for l in s.languages)]
        if city:
            city_lower = city.lower()
            filtered = [s for s in filtered if city_lower in s.city.lower()]
        if region:
            region_lower = region.lower()
            filtered = [s for s in filtered if region_lower in s.region.lower()]
        return filtered
