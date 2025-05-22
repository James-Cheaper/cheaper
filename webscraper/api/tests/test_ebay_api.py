import unittest
from unittest.mock import patch,Mock
import requests
from webscraper.api.EbayAPI import EbayAPI
from dotenv import load_dotenv
load_dotenv()
from webscraper.database.db import SessionLocal
from webscraper.database.models import EbayItem

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
        
    def test_search_item_stores_to_db(self):
        session = SessionLocal()
        try:
            # Run actual API search
            result = self.EbayAPI.search_item("macbook")

            # Save result to DB
            new_item = EbayItem(
                name=result.name,
                price=result.price,
                currency=result.currency,
                url=result.url,
                user_id=None  # or a test user ID if needed
            )
            session.add(new_item)
            session.commit()

            # Query the DB to check if the item is saved
            item = session.query(EbayItem).filter_by(name=result.name).first()
            self.assertIsNotNone(item)
        finally:
            session.close()

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



    # @patch("webscraper.api.EbayAPI.requests.get")
    # def test_retrieve_ebay_response_invalid(self,mock_get):
    #     self.EbayAPI.retrieve_ebay_response("https://test","item")
    #     self.assertRaises(Exception)

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