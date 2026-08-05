"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Stream Recorder

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import os
import signal
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List

from graf.config import config
from graf.logger import (
    info, warning, error, station_started, station_stopped,
    station_reconnecting, segment_saved, metadata_saved, recording_error
)
from graf.acquisition.station import Station
from graf.metadata.builder import MetadataBuilder
from graf.utils.system import find_binary

class StreamRecorder:
    """
    Stream recorder for a single Ghanaian radio station.
    """
    def __init__(
        self,
        station: Station,
        output_dir: Optional[Path] = None,
        metadata_dir: Optional[Path] = None,
        segment_duration: Optional[int] = None,
    ):
        self.station = station
        self.output_dir = output_dir or config.paths.raw_audio_dir
        self.metadata_dir = metadata_dir or config.paths.metadata_dir
        self.segment_duration = segment_duration or config.audio.segment_duration

        self.ffmpeg_binary = find_binary(config.ffmpeg.ffmpeg_binary) or "ffmpeg"
        self.ffprobe_binary = find_binary(config.ffmpeg.ffprobe_binary) or "ffprobe"

        self.metadata_builder = MetadataBuilder(
            ffmpeg_binary=self.ffmpeg_binary,
            ffprobe_binary=self.ffprobe_binary
        )

        self._running = False
        self._process: Optional[subprocess.Popen] = None
        self._segment_counter = 0

    def is_running(self) -> bool:
        return self._running

    def _generate_filename(self, timestamp: datetime, ext: str = "mp3") -> str:
        """Standardized segment filename: {StationID}_{YYYYMMDD_HHMMSS}.{ext}"""
        clean_name = self.station.id.replace(" ", "_")
        time_str = timestamp.strftime("%Y%m%d_%H%M%S")
        return f"{clean_name}_{time_str}.{ext.lstrip('.')}"

    def record_single_segment(
        self,
        duration_seconds: int = 30,
        stream_url: Optional[str] = None
    ) -> Optional[Path]:
        """
        Records a single segment of specified duration. Useful for validation and testing.
        """
        url = stream_url or self.station.stream_url
        timestamp = datetime.now(timezone.utc)
        filename = self._generate_filename(timestamp)
        audio_path = self.output_dir / filename
        meta_path = self.metadata_dir / f"{audio_path.stem}.json"

        cmd = [
            self.ffmpeg_binary,
            "-y",
            "-nostdin",
            "-loglevel", config.ffmpeg.ffmpeg_loglevel,
            "-i", url,
            "-t", str(duration_seconds),
        ]

        if config.audio.copy_audio_stream:
            cmd.extend(["-c:a", "copy"])
        else:
            cmd.extend([
                "-c:a", "libmp3lame",
                "-b:a", f"{config.audio.bit_rate}",
                "-ar", f"{config.audio.sample_rate}",
                "-ac", f"{config.audio.channels}",
            ])

        cmd.append(str(audio_path.resolve()))

        station_started(self.station.name)
        start_time = datetime.now(timezone.utc)

        try:
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=duration_seconds + 30
            )
            end_time = datetime.now(timezone.utc)

            if res.returncode != 0:
                warning(f"[{self.station.name}] FFmpeg exited code {res.returncode}: {res.stderr}")
                return None

            if not audio_path.exists() or audio_path.stat().st_size == 0:
                error(f"[{self.station.name}] Audio output file is missing or 0 bytes.")
                return None

            self._segment_counter += 1
            segment_saved(self.station.name, audio_path.name)

            # Build and save GRMS metadata
            metadata = self.metadata_builder.build(
                station_name=self.station.name,
                stream_url=url,
                audio_file=audio_path,
                capture_start=start_time,
                capture_end=end_time,
                station_id=self.station.id,
                frequency=self.station.frequency,
                city=self.station.city,
                region=self.station.region,
                languages=self.station.languages,
                genre=self.station.genre,
                owner=self.station.owner,
                segment_number=self._segment_counter,
            )
            metadata.save(meta_path)
            metadata_saved(self.station.name, meta_path.name)

            return audio_path

        except Exception as exc:
            recording_error(self.station.name, exc)
            return None

    def start_continuous(self) -> None:
        """
        Starts a continuous recording loop with exponential backoff reconnects.
        Runs until stop() is called.
        """
        self._running = True
        current_delay = config.reconnect.initial_delay
        stream_urls = self.station.get_all_stream_urls()
        url_idx = 0

        station_started(self.station.name)

        while self._running:
            url = stream_urls[url_idx % len(stream_urls)]
            timestamp = datetime.now(timezone.utc)
            pattern = str(self.output_dir / f"{self.station.id}_%Y%m%d_%H%M%S.mp3")

            cmd = [
                self.ffmpeg_binary,
                "-nostdin",
                "-loglevel", config.ffmpeg.ffmpeg_loglevel,
                "-reconnect", "1",
                "-reconnect_at_eof", "1",
                "-reconnect_streamed", "1",
                "-reconnect_delay_max", "10",
                "-i", url,
                "-f", "segment",
                "-segment_time", str(self.segment_duration),
                "-reset_timestamps", "1",
                "-c:a", "copy" if config.audio.copy_audio_stream else "libmp3lame",
                pattern
            ]

            try:
                self._process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Monitor process execution
                while self._running and self._process.poll() is None:
                    time.sleep(2.0)

                if not self._running:
                    break

                # If process died unexpectedly
                exit_code = self._process.poll()
                warning(f"[{self.station.name}] Stream process terminated with exit code {exit_code}")

            except Exception as exc:
                recording_error(self.station.name, exc)

            if not self._running:
                break

            # Connection lost - retry with backoff logic
            station_reconnecting(self.station.name, current_delay)
            time.sleep(current_delay)

            # Exponential backoff update
            current_delay = min(
                int(current_delay * config.reconnect.multiplier),
                config.reconnect.max_delay
            )
            url_idx += 1  # Cycle to fallback URL if available

        station_stopped(self.station.name)

    def stop(self) -> None:
        """Stop the recording process gracefully."""
        self._running = False
        if self._process and self._process.poll() is None:
            try:
                self._process.terminate()
                self._process.wait(timeout=5)
            except Exception:
                self._process.kill()
        station_stopped(self.station.name)
