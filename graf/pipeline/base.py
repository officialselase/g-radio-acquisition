"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Abstract Pipeline Base Class & Execution Runner

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

from graf.logger import info, error, warning
from graf.metadata.models import GRMSMetadata

class PipelineStage(ABC):
    """
    Abstract interface for every processing stage in the G-Radio pipeline.
    Ensures models and algorithms can be swapped seamlessly without changing pipeline glue code.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process(
        self,
        audio_path: Path,
        metadata: GRMSMetadata
    ) -> Tuple[Path, GRMSMetadata]:
        """
        Execute processing stage on target audio segment.
        Returns updated (audio_path, metadata).
        """
        pass

class PipelineRunner:
    """
    Sequential runner that executes ordered PipelineStages on an audio segment.
    """
    def __init__(self, stages: Optional[List[PipelineStage]] = None):
        self.stages: List[PipelineStage] = stages or []

    def add_stage(self, stage: PipelineStage) -> "PipelineRunner":
        self.stages.append(stage)
        return self

    def run(
        self,
        audio_path: Path,
        metadata: GRMSMetadata
    ) -> Tuple[Path, GRMSMetadata]:
        """Execute all registered pipeline stages sequentially."""
        current_audio = audio_path
        current_meta = metadata

        info(f"Starting pipeline execution ({len(self.stages)} stages) for {audio_path.name}")

        for stage in self.stages:
            info(f"Executing Pipeline Stage: [{stage.name}]...")
            try:
                current_audio, current_meta = stage.process(current_audio, current_meta)
            except Exception as e:
                error(f"Error in Pipeline Stage [{stage.name}]: {e}")
                raise e

        info(f"Pipeline execution completed successfully for {audio_path.name}")
        return current_audio, current_meta
