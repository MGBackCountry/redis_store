import unittest
from unittest.mock import MagicMock, patch

from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException

from home.electricity.model.home import EnergyModel
from home.electricity.schemas import ElectricitySchema


class TestElectricity(unittest.TestCase):
    def test_creates_new_electricity_entry_when_not_exists(self):
        mock_home = MagicMock()
        mock_home.json().get.return_value = None
        mock_home.json().set.return_value = True
        with patch('home.electricity.model.home.home', mock_home):
            model = EnergyModel(address_id='123', body_params={'date': '2024-06-01', 'usage': 10})
            result = model.create_electricity()
            self.assertEqual(result, {'date': '2024-06-01', 'usage': 10})
            mock_home.json().set.assert_called_once()

    def test_aborts_when_electricity_entry_already_exists(self):
        mock_home = MagicMock()
        mock_home.json().get.return_value = {'date': '2024-06-01', 'usage': 10}
        with patch('home.electricity.model.home.home', mock_home), \
             patch('home.electricity.model.home.abort') as mock_abort:
            model = EnergyModel(address_id='123', body_params={'date': '2024-06-01', 'usage': 10})
            model.create_electricity()
            mock_abort.assert_called_once_with(400, message='Entry already exists')

    def test_validates_correct_data(self):
        data = {'date': '2024-06-01', 'consume': {'low': 140, 'high': 250}, 'supply': {'low': 50, 'high': 120}}
        schema = ElectricitySchema()
        result = schema.load(data)
        self.assertEqual(result['date'],'2024-06-01')
        self.assertEqual(result['consume'], {'low': 140, 'high': 250})
        self.assertEqual(result['supply'], {'low': 50, 'high': 120})

    def test_raises_error_for_missing_field(self):
        data = {'date': '2024-06-01', 'consume': {'low': 140, 'high': 250}, 'supply': {'low': 50}}
        schema = ElectricitySchema()
        with self.assertRaises(ValidationError) as context:
            schema.load(data)
        self.assertEqual(str(context.exception), "{'supply': {'high': ['Missing data for required field.']}}")

    def test_raises_error_for_missing_consume(self):
        data = {'date': '2024-06-01', 'supply': {'low': 50, 'high': 120}}
        schema = ElectricitySchema()
        with self.assertRaises(ValidationError) as context:
            schema.load(data)
        self.assertEqual(str(context.exception), "{'consume': ['Missing data for required field.']}")

    def test_raises_error_for_invalid_number_type(self):
        data = {'date': '2024-06-01', 'consume': {'low': 'not a number', 'high': 250},
                'supply': {'low': 50, 'high': 120}}
        schema = ElectricitySchema()
        with self.assertRaises(ValidationError) as context:
            schema.load(data)
        self.assertIn('Not a valid integer', str(context.exception))

    def test_raises_error_for_invalid_date_format(self):
        data = {'date': '31-06-2024', 'consume': {'low': 120, 'high': 250}, 'supply': {'low': 50, 'high': 120}}
        schema = ElectricitySchema()
        with self.assertRaises(HTTPException) as context:
            schema.load(data)
        self.assertIn('400 Bad Request', str(context.exception))


if __name__ == "__main__":
    unittest.main()
