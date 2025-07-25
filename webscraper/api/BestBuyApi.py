import os
from dotenv import load_dotenv
import requests
from webscraper.api.interface import EbayABC

load_dotenv()

class BestBuyAPI(EbayABC):
    def __init__(self):
        try: 
            self.api_key = os.getenv("BESTBUY_API_KEY")
            self.base_url = "https://api.bestbuy.com/v1/products"
        finally: 
            if not self.api_key:
                raise Exception ("BESTBUY_API_KEY not found.")
                
    def retrieve_access_token(self) -> str:
        return self.api_key

    def retrieve_response(self, httprequest: str, query: str) -> dict:
        token = self.retrieve_access_token()
        url = f"{httprequest}((categoryPath.id{query}))"
        params = {
            "apiKey": token,
            "format": "json"
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    


