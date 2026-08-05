import unittest
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from graf.metadata import GRMSMetadata, MetadataBuilder, validate_metadata

class TestMetadata(unittest.TestCase):
    def test_metadata_instantiation_and_serialization(self):
        metadata = GRMSMetadata()
        self.assertEqual(metadata.dataset.name, "G-Radio")
        self.assertEqual(metadata.dataset.country, "Ghana")

        valid, msg = validate_metadata(metadata)
        self.assertTrue(valid, f"Validation failed: {msg}")

        with tempfile.TemporaryDirectory() as tmpdir:
            json_path = Path(tmpdir) / "test_meta.json"
            metadata.save(json_path)
            self.assertTrue(json_path.exists())

            loaded = GRMSMetadata.load(json_path)
            self.assertEqual(loaded.capture_id, metadata.capture_id)
            self.assertEqual(loaded.dataset.name, metadata.dataset.name)

    def test_metadata_builder(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_file = Path(tmpdir) / "sample.mp3"
            audio_file.write_bytes(b"\x00" * 1024)

            builder = MetadataBuilder()
            now = datetime.now(timezone.utc)
            metadata = builder.build(
                station_name="Peace FM",
                stream_url="https://stream.example.com",
                audio_file=audio_file,
                capture_start=now,
                capture_end=now,
                station_id="peace_fm",
                city="Accra",
                languages=["Twi", "English"],
            )

            self.assertEqual(metadata.station.name, "Peace FM")
            self.assertEqual(metadata.file.filename, "sample.mp3")
            self.assertEqual(metadata.file.size_bytes, 1024)
            self.assertEqual(len(metadata.file.sha256), 64)

if __name__ == "__main__":
    unittest.main()
