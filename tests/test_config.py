import unittest
from graf.config import config

class TestConfig(unittest.TestCase):
    def test_config_paths_exist(self):
        self.assertTrue(config.paths.base_dir.exists())
        self.assertTrue(config.paths.storage_dir.exists())
        self.assertTrue(config.paths.raw_audio_dir.exists())
        self.assertTrue(config.paths.metadata_dir.exists())

    def test_config_defaults(self):
        self.assertEqual(config.dataset.dataset_name, "G-Radio")
        self.assertEqual(config.dataset.country, "Ghana")
        self.assertGreater(config.audio.segment_duration, 0)

if __name__ == "__main__":
    unittest.main()
