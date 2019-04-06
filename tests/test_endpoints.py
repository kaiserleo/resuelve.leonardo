from app import app
from flask import url_for
import unittest


class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_server_is_alive(self):
        """Assert that the service is up and running"""
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_404(self):
        """Assert that we are returning 404 on an invalid url"""
        result = self.app.get('/invalid_url')
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()
