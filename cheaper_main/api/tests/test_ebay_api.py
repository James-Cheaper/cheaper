import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cheaper.settings")  # adjust if your settings module is different
django.setup()


import unittest
from unittest.mock import patch,Mock
import requests
from ...api.ebay_api import EbayAPI
from dotenv import load_dotenv
load_dotenv()


class EbayTestApi(unittest.TestCase):

    def setUp(self):
        self.EbayAPI = EbayAPI


    def test_retrieve_access_token_real(self):
        token = self.EbayAPI.retrieve_access_token()
        self.assertIsInstance(token, str)
        self.assertGreater(len(token), 0)

    def test_search_item_real(self):
        item = self.EbayAPI.search_item("macbook")
        self.assertIsInstance(item.name, str)
        self.assertIsInstance(item.price, float)
        self.assertIsInstance(item.currency, str)
        self.assertTrue(item.url.startswith("http"))
        
    def test_search_item_not_found(self):
        with self.assertRaises(Exception) as context:
            self.EbayAPI.search_item("asdkfjasldfjalskdfj")  # nonsense query

        self.assertIn("Could not parse item", str(context.exception))


    # @patch("webscraper.api.EbayAPI.requests.post")                       
    # def test_retrieve_access_token(self, mock_post):
    #     mock_response = Mock()
    #     mock_response.status_code = 200
    #     mock_response.json.return_value = {"access_token": "mock_token"}
    #     mock_post.return_value = mock_response

    #     token = self.EbayAPI.retrieve_access_token()
    #     self.assertEqual(token, "mock_token")

    @patch("webscraper.api.EbayAPI.requests.post")
    def test_retrieve_access_token_invalid(self,mock_post):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value ={"error": "not found"}
        mock_post.return_value = mock_response

        with self.assertRaises(Exception):
            self.EbayAPI.retrieve_access_token()



    @patch("webscraper.api.EbayAPI.requests.get")
    def test_retrieve_ebay_response_invalid(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Invalid request")
        with self.assertRaises(Exception):
            self.EbayAPI.retrieve_ebay_response("https://test", "item")

    def test_search_item_empty_query(self):
        with self.assertRaises(ValueError):
            self.EbayAPI.search_item("")

    # @patch("webscraper.api.EbayAPI.EbayAPI.retrieve_ebay_response")
    # def test_search_item(self, mock_response):
    #     mock_response.return_value = {
    #         "itemSummaries": [
    #             {
    #                 "title": "Test Product",
    #                 "price": {
    #                     "value": "19.99",
    #                     "currency": "USD"
    #                 }
    #             }
    #         ]
    #     }

    #     result = self.EbayAPI.search_item("test")
    #     self.assertEqual(result["name"], "Test Product")
    #     self.assertEqual(result["price"], "19.99")
    #     self.assertEqual(result["currency"], "USD")



if __name__ == '__main__':
    unittest.main()