import unittest
from graf.acquisition.station import StationRegistry

class TestStationRegistry(unittest.TestCase):
    def test_station_registry_load(self):
        registry = StationRegistry()
        stations = registry.get_all()
        self.assertGreater(len(stations), 0, "No stations loaded from registry")

        peace_fm = registry.get_by_id("peace_fm")
        self.assertIsNotNone(peace_fm)
        self.assertEqual(peace_fm.name, "Peace FM")
        self.assertIn("Twi", peace_fm.languages)

    def test_station_filtering(self):
        registry = StationRegistry()
        twi_stations = registry.filter(language="Twi")
        self.assertGreater(len(twi_stations), 0)

        accra_stations = registry.filter(city="Accra")
        self.assertGreater(len(accra_stations), 0)

if __name__ == "__main__":
    unittest.main()
