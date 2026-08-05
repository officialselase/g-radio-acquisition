"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Command Line Interface (CLI)

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

import argparse
import sys
from pathlib import Path

from graf.config import config, print_configuration
from graf.logger import info, warning, error
from graf.acquisition.station import StationRegistry
from graf.acquisition.recorder import StreamRecorder
from graf.acquisition.manager import AcquisitionManager
from graf.validation.validator import SegmentValidator
from graf.pipeline.base import PipelineRunner
from graf.pipeline.music_detection import MusicDetectionStage
from graf.pipeline.source_separation import SourceSeparationStage
from graf.pipeline.fingerprinting import FingerprintingStage
from graf.pipeline.benchmarking import BenchmarkingStage
from graf.metadata.models import GRMSMetadata

def cmd_info(args):
    """Print configuration and framework status."""
    print_configuration()
    registry = StationRegistry()
    print(f"Registered Active Ghanaian Stations: {len(registry.get_all())}")
    for station in registry.get_all():
        print(f" - [{station.id}] {station.name} ({station.frequency}) - {station.city} [{', '.join(station.languages)}]")

def cmd_stations(args):
    """List registered Ghanaian radio stations."""
    registry = StationRegistry()
    stations = registry.filter(language=args.language, city=args.city, region=args.region)
    print("=" * 70)
    print(f"G-Radio Station Registry ({len(stations)} matched)")
    print("=" * 70)
    for s in stations:
        print(f"ID         : {s.id}")
        print(f"Name       : {s.name} ({s.frequency})")
        print(f"City/Region: {s.city}, {s.region}")
        print(f"Stream URL : {s.stream_url}")
        print(f"Languages  : {', '.join(s.languages)}")
        print(f"Genre      : {s.genre}")
        print("-" * 70)

def cmd_test_record(args):
    """Perform a short timed test recording of a station stream."""
    registry = StationRegistry()
    station = registry.get_by_id(args.station_id)
    if not station:
        print(f"Error: Station with ID '{args.station_id}' not found in registry.")
        sys.exit(1)

    print(f"Initiating {args.duration}s test capture for [{station.name}] ({station.stream_url})...")
    recorder = StreamRecorder(station)
    audio_path = recorder.record_single_segment(duration_seconds=args.duration)

    if audio_path:
        print(f"SUCCESS: Captured audio segment -> {audio_path}")
        meta_path = config.paths.metadata_dir / f"{audio_path.stem}.json"
        if meta_path.exists():
            print(f"SUCCESS: Created GRMS metadata -> {meta_path}")
            # Run validator
            validator = SegmentValidator()
            val_res = validator.validate_segment(audio_path, meta_path)
            print(f"Validation Result: Valid={val_res.is_valid}, Codec={val_res.codec}, SHA256={val_res.sha256[:16]}...")
    else:
        print(f"FAILURE: Recording failed for station {station.name}")
        sys.exit(1)

def cmd_record(args):
    """Start continuous acquisition manager."""
    registry = StationRegistry()
    manager = AcquisitionManager(registry)
    station_ids = args.stations.split(",") if args.stations else None

    try:
        manager.start_all(station_ids=station_ids)
        print("Continuous acquisition running. Press Ctrl+C to terminate.")
        while True:
            import time
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\nTermination signal received.")
        manager.stop_all()

def cmd_validate(args):
    """Validate captured raw audio segments."""
    raw_dir = config.paths.raw_audio_dir
    validator = SegmentValidator()
    audio_files = list(raw_dir.glob("*.mp3")) + list(raw_dir.glob("*.wav"))

    print(f"Validating {len(audio_files)} audio segments in {raw_dir}...")
    valid_count = 0
    for audio_file in audio_files:
        meta_file = config.paths.metadata_dir / f"{audio_file.stem}.json"
        res = validator.validate_segment(audio_file, meta_file if meta_file.exists() else None)
        if res.is_valid:
            valid_count += 1

    print(f"Validation Complete: {valid_count}/{len(audio_files)} valid segments.")

def cmd_pipeline(args):
    """Execute ML pipeline on captured and validated segments."""
    raw_dir = config.paths.raw_audio_dir
    audio_files = list(raw_dir.glob("*.mp3")) + list(raw_dir.glob("*.wav"))

    if not audio_files:
        print(f"No audio files found in {raw_dir} to process.")
        return

    runner = PipelineRunner([
        MusicDetectionStage(),
        SourceSeparationStage(),
        FingerprintingStage(),
        BenchmarkingStage(),
    ])

    for audio_file in audio_files:
        meta_file = config.paths.metadata_dir / f"{audio_file.stem}.json"
        meta = GRMSMetadata.load(meta_file) if meta_file.exists() else GRMSMetadata()
        audio_out, meta_out = runner.run(audio_file, meta)
        if meta_file.exists():
            meta_out.save(meta_file)
            print(f"Processed & updated metadata for {audio_file.name}")

def main():
    parser = argparse.ArgumentParser(
        description="G-Radio Acquisition Framework (GRAF) CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # info
    subparsers.add_parser("info", help="Display GRAF framework status and configuration")

    # stations
    p_stations = subparsers.add_parser("stations", help="List active Ghanaian radio stations")
    p_stations.add_argument("--language", help="Filter by broadcast language (e.g. Twi, English)")
    p_stations.add_argument("--city", help="Filter by city (e.g. Accra, Kumasi)")
    p_stations.add_argument("--region", help="Filter by region (e.g. Greater Accra, Ashanti)")

    # test-record
    p_test = subparsers.add_parser("test-record", help="Perform short test capture of a station")
    p_test.add_argument("--station-id", required=True, help="Station ID (e.g. peace_fm, citi_fm)")
    p_test.add_argument("--duration", type=int, default=15, help="Test duration in seconds")

    # record
    p_rec = subparsers.add_parser("record", help="Start continuous stream acquisition")
    p_rec.add_argument("--stations", help="Comma-separated station IDs to record (default: all)")

    # validate
    subparsers.add_parser("validate", help="Validate integrity of captured audio segments")

    # pipeline
    subparsers.add_parser("pipeline", help="Run ML pipeline on captured audio segments")

    args = parser.parse_args()

    if args.command == "info":
        cmd_info(args)
    elif args.command == "stations":
        cmd_stations(args)
    elif args.command == "test-record":
        cmd_test_record(args)
    elif args.command == "record":
        cmd_record(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "pipeline":
        cmd_pipeline(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
