import unittest
from webscraper.api.routes import app

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Cheaper API", response.data)

    def test_scrape_no_params(self):
        response = self.client.get('/scrape')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"No paths provided", response.data)

    def test_scrape_valid_path(self):
        response = self.client.get('/scrape?path=/catalogue/page-1.html')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), dict)

if __name__ == '__main__':
    unittest.main()
