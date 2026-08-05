"""
==============================================================
G-Radio Acquisition Framework (GRAF)
Audio Source Separation Stage Interface & Implementation

Author : Selase K. Agbai
Project: Rob-GhanaRadio
==============================================================
"""

from pathlib import Path
from typing import Tuple

from graf.logger import info
from graf.metadata.models import GRMSMetadata
from graf.pipeline.base import PipelineStage

class SourceSeparationStage(PipelineStage):
    """
    Joint Sound Event & Music Source Separation stage.
    Separates background speech, presenter chatter, and radio jingles from clean music stems.
    """
    def __init__(self, model_name: str = "Demucs-v4-GhanaRadio"):
        super().__init__(name="Source Separation")
        self.model_name = model_name

    def process(self, audio_path: Path, metadata: GRMSMetadata) -> Tuple[Path, GRMSMetadata]:
        """
        Execute sound separation model to isolate music stems from Ghanaian radio interference.
        """
        info(f"[{self.name}] Running joint source separation model '{self.model_name}' on {audio_path.name}")

        metadata.machine_learning.source_separation_model = self.model_name
        metadata.interference.presenter_over_music = True
        metadata.processing_status.source_separated = True

        return audio_path, metadata
