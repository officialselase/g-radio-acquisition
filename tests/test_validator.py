import unittest
import tempfile
from pathlib import Path
from graf.validation.validator import SegmentValidator

class TestValidator(unittest.TestCase):
    def test_validator_zero_byte_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            zero_file = Path(tmpdir) / "empty.mp3"
            zero_file.write_bytes(b"")

            validator = SegmentValidator(failed_dir=Path(tmpdir) / "failed")
            res = validator.validate_segment(zero_file, quarantine_on_failure=False)

            self.assertFalse(res.is_valid)
            self.assertIn("Audio file size is 0 bytes", res.errors)

    def test_validator_non_existent_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing_file = Path(tmpdir) / "missing.mp3"
            validator = SegmentValidator(failed_dir=Path(tmpdir) / "failed")
            res = validator.validate_segment(missing_file, quarantine_on_failure=False)

            self.assertFalse(res.is_valid)
            self.assertIn("Audio file does not exist", res.errors)

if __name__ == "__main__":
    unittest.main()
