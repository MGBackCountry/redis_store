"""Unit test data strorage energy"""
import unittest
from energy_usage.energy import EnergyData


class MyEnergyData(unittest.TestCase):
    """Unit test energy data"""

    def setUp(self):
        """Setup unittest"""
        self.energy_data = EnergyData()

    def test_constructor(self):
        """Test constructor"""
        self.assertEqual(self.energy_data.location, b'Tolakkerweg136E')


if __name__ == '__main__':
    unittest.main()
