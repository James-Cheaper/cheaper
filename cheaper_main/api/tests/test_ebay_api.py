import unittest
from unittest.mock import patch,Mock
import requests
from ebay_api import EbayAPI

class EbayTestApi(unittest.TestCase):

    def setUp(self):
        self.EbayAPI = EbayAPI


    def test_retrieve_access_token(self):
        self.EbayAPI.retrieve_access_token()
        self.assertEqual(type(self.EbayAPI.retrieve_access_token()),str)

    @patch("webscraper.api.EbayAPI.requests.post")
    def test_retrieve_access_token_invalid(self,mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value ={"error": "not found"}
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            self.EbayAPI.retrieve_access_token()



    @patch("webscraper.api.EbayAPI.requests.get")
    def test_retrieve_ebay_response_invalid(self,mock_get):
        self.EbayAPI.retrieve_ebay_response("https://test","item")
        self.assertRaises(Exception)


if __name__ == '__main__':
    unittest.main()