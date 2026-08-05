import unittest
import tempfile
from pathlib import Path
from graf.metadata import GRMSMetadata
from graf.pipeline.base import PipelineRunner
from graf.pipeline.music_detection import MusicDetectionStage
from graf.pipeline.source_separation import SourceSeparationStage
from graf.pipeline.fingerprinting import FingerprintingStage
from graf.pipeline.benchmarking import BenchmarkingStage

class TestPipeline(unittest.TestCase):
    def test_pipeline_execution(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_file = Path(tmpdir) / "test_audio.mp3"
            audio_file.write_bytes(b"\x00" * 512)

            metadata = GRMSMetadata()
            metadata.file.filename = audio_file.name

            runner = PipelineRunner([
                MusicDetectionStage(),
                SourceSeparationStage(),
                FingerprintingStage(),
                BenchmarkingStage(),
            ])

            out_audio, out_meta = runner.run(audio_file, metadata)

            self.assertTrue(out_meta.processing_status.music_detected)
            self.assertTrue(out_meta.processing_status.source_separated)
            self.assertTrue(out_meta.processing_status.fingerprint_generated)
            self.assertTrue(out_meta.processing_status.benchmarked)
            self.assertIsNotNone(out_meta.fingerprinting.embedding_id)

if __name__ == "__main__":
    unittest.main()
