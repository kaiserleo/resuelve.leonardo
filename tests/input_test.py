import unittest
from nose.tools import *
from decimal import Decimal
from resuelvefc.input import *
from resuelvefc.exceptions import *

class InputValidatorTest(unittest.TestCase):

    @raises(ArrayExpectedException)
    def test_an_array_is_expected(self):
        """Assert that the validator is receiving an array"""
        input_json = '{"a":1}'
        validator = InputValidator(input_json)
        validator.encode()


    @raises(ZeroPlayersReceivedException)
    def test_the_array_is_not_empty(self):
        """Assert that the array received is not empty"""
        input_json = '[]'
        validator = InputValidator(input_json)
        validator.encode()


    @raises(InvalidPlayerFormatException)
    def test_the_json_is_an_array_of_dictionaries(self):
        """Assert that each player is a dictionary"""
        input_json = '[1,{"a":"b"},2,3]'
        validator = InputValidator(input_json)
        validator.encode()


    @raises(MissingFieldsException)
    def test_we_have_the_correct_keys_for_each_player(self):
        """Validate that each player has the expected fields"""
        input_json = '''
            [
                {
                    "goles":10,
                    "sueldo":50000,
                    "bono":25000,
                    "sueldo_completo":null,
                    "equipo":"rojo"
                },
                {
                    "nombre": "x",
                    "nivel":"C",
                    "goles":10,
                    "sueldo":50000,
                    "bono":25000
                }
            ]
        '''
        validator = InputValidator(input_json)
        validator.encode()


    @raises(NonValidFieldsException)
    def test_we_dont_receive_invalid_keys(self):
        """Validate that each player doesn't receive unrequired fields"""
        input_json = '''
            [
                {
                    "nombre": "x",
                    "nivel":"C",
                    "goles":10,
                    "sueldo":50000,
                    "bono":25000,
                    "sueldo_completo":null,
                    "equipo":"rojo",
                    "rey": "leon"
                },
                {
                    "nombre": "x",
                    "nivel":"C",
                    "goles":10,
                    "sueldo":50000,
                    "bono":25000,
                    "sueldo_completo":null,
                    "equipo":"rojo",
                    "playera": "algodon"
                }
            ]
        '''
        validator = InputValidator(input_json)
        validator.encode()


    @raises(InvalidDataTypeFormatException)
    def test_each_field_data_is_valid_type(self):
        """Validate that each field has proper type"""
        input_json = '''
            [
                {
                    "nombre": "x",
                    "nivel":"C",
                    "goles":10,
                    "sueldo":50000,
                    "bono":25000,
                    "sueldo_completo":null,
                    "equipo":"rojo"
                },
                {
                    "nombre": "x",
                    "nivel":"C",
                    "goles":10,
                    "sueldo":50000.00,
                    "bono":25000.00,
                    "sueldo_completo":null,
                    "equipo":"rojo"
                },
                {
                    "nombre": 345,
                    "nivel":  123,
                    "goles":  "Diez",
                    "sueldo": "Mucho",
                    "bono":   "Menos",
                    "sueldo_completo": "null",
                    "equipo": ["Rocket"]
                }
            ]
        '''
        validator = InputValidator(input_json)
        validator.encode()

    def test_it_is_returning_an_array(self):
        """Check that it works on good conditions"""
        input_json = '''
            [
                {
                    "nombre": "x",
                    "nivel":"Alto",
                    "goles":40,
                    "sueldo":50000,
                    "bono":25000,
                    "sueldo_completo":null,
                    "equipo":"azul"
                },
                {
                    "nombre": "Fulano Detal",
                    "nivel":"C",
                    "goles":10,
                    "sueldo":54320.00,
                    "bono":25000.00,
                    "sueldo_completo":null,
                    "equipo":"rojo"
                }
            ]
        '''
        validator = InputValidator(input_json)
        out = validator.encode()
        self.assertTrue(isinstance(out, list))
        self.assertEqual(out[1]["nombre"], "Fulano Detal")
        self.assertEqual(out[0]["sueldo"], 50000)
        self.assertEqual(out[1]["bono"], Decimal('25000.00'))
        self.assertEqual(out[0]["sueldo_completo"], None)
        self.assertEqual(out[1]["goles"], 10)
        self.assertEqual(out[0]["equipo"], "azul")
        self.assertEqual(out[1]["nivel"], "C")


if __name__ == '__main__':
    unittest.main()

