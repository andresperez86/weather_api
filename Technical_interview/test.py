import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_weather_success(self):
        response = self.app.get('/weather/1')
        self.assertEqual(response.status_code, 200)

    def test_weather_failure(self):
        response = self.app.get('/weather/9999')
        self.assertEqual(response.status_code, 404)

    def test_history(self):
        response = self.app.get('/history')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()