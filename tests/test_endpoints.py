from app import app
from flask import url_for
import unittest
import simplejson as json


class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_server_is_alive(self):
        """Assert that the service is up and running"""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data, b'Server up and running\n')

    def test_404(self):
        """Assert that we are returning 404 on an invalid url"""
        result = self.app.get('/invalid_url')
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(data['error'], 'Not found')


    def test_405(self):
        """Assert that we are returning 405 on an invalid Method"""
        result = self.app.get('/calcula_sueldo')
        self.assertEqual(result.status_code, 405)
        data = json.loads(result.data)
        self.assertEqual(data['error'], 'Method not allowed')

    def test_body_is_json(self):
        """Assert that we are receiving a json"""
        result = self.app.post('/calcula_sueldo',
                data='x')
        self.assertEqual(result.status_code, 422)

    def test_array(self):
        """Assert that the json received includes an array"""
        result = self.app.post('/calcula_sueldo',
                data='{"x":"y"}')
        self.assertEqual(result.status_code, 422)
        data = json.loads(result.data)
        self.assertEqual(data['error'], 'Array expected')

    def test_non_zero_players(self):
        """Assert that we are receiving 1 or more players"""
        result = self.app.post('/calcula_sueldo',
                data='[]')
        self.assertEqual(result.status_code, 422)
        data = json.loads(result.data)
        self.assertEqual(data['error'], 'Zero Players Received')

    def test_missing_fields(self):
        """Assert that the players include all required fields"""
        result = self.app.post('/calcula_sueldo',
                data='[{"x":"y"}]')
        self.assertEqual(result.status_code, 422)
        data = json.loads(result.data)
        self.assertEqual(data['error'][0:14], 'Missing fields')

    def test_non_valild_fields(self):
        """Assert that the player dict does not include an extra field"""
        result = self.app.post('/calcula_sueldo',
                data='[{"nombre":"leonidas", "marzo":"abril", "sueldo": "xx", "bono": "xx", "equipo":"xyz", "nivel":"xx", "sueldo_completo":"xx", "goles":"qqq"}]')
        self.assertEqual(result.status_code, 422)
        data = json.loads(result.data)
        self.assertEqual(data['error'][0:16], 'Non valid fields')

    def test_data_type(self):
        """Assert that the fields have correct data type"""
        result = self.app.post('/calcula_sueldo',
                data='[{"nombre":"leonidas", "sueldo": "xx", "bono": "xx", "equipo":"xyz", "nivel":"xx", "sueldo_completo":"xx", "goles":"qqq"}]')
        self.assertEqual(result.status_code, 422)
        data = json.loads(result.data)
        self.assertEqual(data['error'][0:17], 'Invalid data type')

    def test_a_valid_level_was_specified(self):
        """Assert that the player was specified an existing level"""
        result = self.app.post('/calcula_sueldo',
                data='[{"nombre":"leonidas", "sueldo": 45000.0, "bono": 10000, "equipo":"xyz", "nivel":"ppppp", "sueldo_completo":null, "goles":14}]')
        self.assertEqual(result.status_code, 422)
        data = json.loads(result.data)
        self.assertEqual(data['error'], 'ppppp level not found')

    def test_success(self):
        """Assert that we can compute a success case"""
        result = self.app.post('/calcula_sueldo',
                data="""[
                       {
                          "nombre":"Juan Perez",
                          "nivel":"C",
                          "goles":10,
                          "sueldo":50000,
                          "bono":25000,
                          "sueldo_completo":null,
                          "equipo":"rojo"
                       },
                       {
                          "nombre":"EL Cuauh",
                          "nivel":"Cuauh",
                          "goles":30,
                          "sueldo":100000,
                          "bono":30000,
                          "sueldo_completo":null,
                          "equipo":"azul"
                       },
                       {
                          "nombre":"Cosme Fulanito",
                          "nivel":"A",
                          "goles":7,
                          "sueldo":20000,
                          "bono":10000,
                          "sueldo_completo":null,
                          "equipo":"azul"

                       },
                       {
                          "nombre":"El Rulo",
                          "nivel":"B",
                          "goles":9,
                          "sueldo":30000,
                          "bono":15000,
                          "sueldo_completo":null,
                          "equipo":"rojo"

                       }
                    ]""")
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data[0]['nombre'], "Juan Perez")
        self.assertEqual(data[0]['goles_minimos'], 15)
        self.assertEqual(data[0]['sueldo_completo'], 67833.33)
        self.assertEqual(data[1]['nombre'], "EL Cuauh")
        self.assertEqual(data[1]['goles_minimos'], 20)
        self.assertEqual(data[1]['sueldo_completo'], 130000.00)
        self.assertEqual(data[2]['nombre'], "Cosme Fulanito")
        self.assertEqual(data[2]['goles_minimos'], 5)
        self.assertEqual(data[2]['sueldo_completo'], 30000.00)
        self.assertEqual(data[3]['nombre'], "El Rulo")
        self.assertEqual(data[3]['goles_minimos'], 10)
        self.assertEqual(data[3]['sueldo_completo'], 42450.00)


if __name__ == '__main__':
    unittest.main()
