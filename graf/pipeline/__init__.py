"""
GRAF ML Processing Pipeline Package
"""

from graf.pipeline.base import PipelineStage, PipelineRunner
from graf.pipeline.music_detection import MusicDetectionStage
from graf.pipeline.source_separation import SourceSeparationStage
from graf.pipeline.fingerprinting import FingerprintingStage
from graf.pipeline.benchmarking import BenchmarkingStage

__all__ = [
    "PipelineStage",
    "PipelineRunner",
    "MusicDetectionStage",
    "SourceSeparationStage",
    "FingerprintingStage",
    "BenchmarkingStage",
]
