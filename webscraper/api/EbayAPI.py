import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import logging
from webscraper.api.interface import ScraperAPIInterface

# Load environment variables and configure logging
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

class EbayItem:
    def __init__(self, name, price, currency, url, date, user_id=None):
        self.name = name
        self.price = price
        self.currency = currency
        self.url = url
        self.date = date
        self.user_id = user_id

class EbayAPI(ScraperAPIInterface):
    client_secret_key = os.getenv("clientsecret")
    client_id_key = os.getenv("clientid")
    get_user_key = HTTPBasicAuth(client_id_key, client_secret_key)

    @staticmethod
    def search_item(query: str) -> list[EbayItem]:
        """Search for items on eBay and return a list of EbayItem objects."""
        if not isinstance(query, str) or not query.strip():
            logger.warning("Invalid query input.")
            raise ValueError("Query must be a non-empty string.")

        logger.info(f"Searching eBay for: {query}")
        response_json = EbayAPI.retrieve_ebay_response(
            "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search", query
        )

        results = []
        try:
            item_summaries = response_json["itemSummaries"]
            for item in item_summaries:
                ebay_item = EbayItem(
                    name=item.get("title"),
                    price=float(item["price"]["value"]),
                    currency=item["price"]["currency"],
                    url=item.get("itemWebUrl"),
                    date=item.get("itemCreationDate"),
                    user_id=None
                )
                results.append(ebay_item)
            return results
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Item list not found or response invalid: {response_json}")
            raise Exception("Could not parse items from eBay response.") from e
        finally:
            logger.debug(f"Search attempt complete for query: {query}")

    @staticmethod
    def retrieve_access_token() -> str:
        """Fetch access token from eBay API."""
        logger.info("Requesting eBay access token...")
        try:
            response = requests.post(
                "https://api.sandbox.ebay.com/identity/v1/oauth2/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "client_credentials",
                    "scope": "https://api.ebay.com/oauth/api_scope"
                },
                auth=EbayAPI.get_user_key
            )
            response.raise_for_status()
            token = response.json().get("access_token")
            if not token:
                logger.error("Access token missing from response.")
                raise Exception("Access token not found in response.")
            logger.info("Access token successfully retrieved.")
            return token
        except requests.exceptions.RequestException as e:
            logger.exception("Failed to retrieve token.")
            raise

    @staticmethod
    def retrieve_ebay_response(httprequest: str, query: str, category_id: int = 0) -> dict:
        """Perform GET request to eBay API."""
        auth = EbayAPI.retrieve_access_token()
        logger.info(f"Making GET request to eBay API: {httprequest} with query: {query} and category_id: {category_id}")
        try:
            response = requests.get(
                httprequest,
                headers={
                    "Authorization": f"Bearer {auth}",
                    "Content-Type": "application/json"
                },
                params={
                    "q": query,
                    "category_ids": category_id if category_id else None  # send only if nonzero
                }
            )
            if response.status_code == 429:
                logger.warning("Rate limit exceeded.")
                raise Exception("Rate limit exceeded.")
            response.raise_for_status()
            logger.debug(f"Raw eBay API response: {response.text}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.exception("Error retrieving eBay response.")
            raise Exception(f"Error retrieving eBay response: {str(e)}") from e
