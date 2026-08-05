"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Acquisition Manager

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import signal
import sys
import threading
import time
from typing import Dict, List, Optional, Any

from graf.logger import info, warning, startup, shutdown
from graf.acquisition.station import Station, StationRegistry
from graf.acquisition.recorder import StreamRecorder

class AcquisitionManager:
    """
    Supervises concurrent acquisition across registered Ghanaian radio stations.
    """
    def __init__(self, registry: Optional[StationRegistry] = None):
        self.registry = registry or StationRegistry()
        self.recorders: Dict[str, StreamRecorder] = {}
        self.threads: Dict[str, threading.Thread] = {}
        self._shutdown_event = threading.Event()

    def start_all(self, station_ids: Optional[List[str]] = None) -> None:
        """Start acquisition threads for specified or all active stations."""
        startup()
        stations = self.registry.get_all()

        if station_ids:
            selected_ids = set(s.lower() for s in station_ids)
            stations = [s for s in stations if s.id.lower() in selected_ids]

        if not stations:
            warning("No active stations matched request for acquisition.")
            return

        info(f"Initiating acquisition across {len(stations)} station streams...")

        for station in stations:
            recorder = StreamRecorder(station)
            thread = threading.Thread(
                target=recorder.start_continuous,
                name=f"Worker-{station.id}",
                daemon=True
            )
            self.recorders[station.id] = recorder
            self.threads[station.id] = thread
            thread.start()
            info(f"Launched acquisition thread for [{station.name}] ({station.frequency})")

    def stop_all(self) -> None:
        """Stop all running acquisition threads gracefully."""
        shutdown()
        self._shutdown_event.set()
        for station_id, recorder in self.recorders.items():
            info(f"Stopping acquisition for station {station_id}...")
            recorder.stop()

        for station_id, thread in self.threads.items():
            if thread.is_alive():
                thread.join(timeout=3)
        info("All station acquisition threads terminated cleanly.")

    def get_status(self) -> Dict[str, Dict[str, Any]]:
        """Return operational status summary for all monitored stations."""
        status = {}
        for station_id, recorder in self.recorders.items():
            status[station_id] = {
                "station_name": recorder.station.name,
                "running": recorder.is_running(),
                "segments_captured": recorder._segment_counter,
                "thread_alive": self.threads[station_id].is_alive() if station_id in self.threads else False,
            }
        return status
