import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from webscraper.api.interface import ScraperAPIInterface

load_dotenv() #initialize

class EbayAPI(ScraperAPIInterface):
    
      client_secret_key = os.getenv("clientsecret")
      client_id_key = os.getenv("clientid")

      get_user_key = HTTPBasicAuth(client_id_key, client_secret_key)

      @staticmethod
      def search_item(query: str) -> dict:
            response_json = EbayAPI.retrieve_ebay_response(
                  "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search",
                  query
            )

            try:
                  # Grab the first item from the results
                  item = response_json["itemSummaries"][0]
                  title = item.get("title")
                  price = item.get("price", {}).get("value")
                  currency = item.get("price", {}).get("currency")
                  return {"name": title, "price": price, "currency": currency}
            except (KeyError, IndexError):
                  raise Exception("Could not parse item from eBay response.")


      @staticmethod
      def retrieve_access_token():
            try:
                  response = requests.post("https://api.sandbox.ebay.com/identity/v1/oauth2/token",
                                          headers = {"Content-Type":"application/x-www-form-urlencoded"},
                                          data = {
                                                "grant_type": "client_credentials",
                                                "scope": "https://api.ebay.com/oauth/api_scope"
                                                      },
                                                auth=EbayAPI.get_user_key
                                          )
                  access_token = response.json().get("access_token")
                  status_code = response.status_code
                  if(status_code == 404):
                        raise Exception("404 error here")
                  return access_token
            except Exception as e:
                  raise e

      @staticmethod
      def retrieve_ebay_response(httprequest:str,query:str):
            auth = EbayAPI.retrieve_access_token()
            try:
                  response = requests.get(httprequest,
                  headers={
                        "Authorization": f"Bearer {auth}",
                        "Content-Type": "application/json"
                        },
                  params= {
                        "q": query,
                        "category_tree_id": 0
                        }
                  ) 
                  status_code = response.status_code
                  if(status_code == 404):
                        raise Exception("not found 404 error")
            
                  return response.json()
            except Exception as e:
                  raise e

