import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheaper.settings')
django.setup()

from flask import Flask, jsonify, request
from webscraper.src.Cheaper_Scraper import CheaperScraper
from flask import Blueprint, request, jsonify
from webscraper.api.EbayAPI import EbayAPI

ebay_bp = Blueprint("ebay", __name__, url_prefix="/api/ebay")

@ebay_bp.route("/category", methods=["GET"])
def get_items_by_category():
    query = request.args.get("q")
    category_id = request.args.get("category_id", default=0, type=int)

    if not query:
        return jsonify({"error": "Missing required query parameter 'q'"}), 400

    try:
        results = EbayAPI.retrieve_ebay_response(
            "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search",
            query,
            category_id
        )
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

app = Flask(__name__)
app.register_blueprint(ebay_bp)


app = Flask(__name__)
scraper = CheaperScraper(base_url="https://books.toscrape.com")

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Cheaper API!"})

@app.route('/scrape', methods=['GET'])
def scrape_books():
    paths = request.args.getlist('path')
    if not paths:
        return jsonify({"error": "No paths provided"}), 400

    results = scraper.get_scraped_data(paths)    
    return jsonify(results)

@app.route('/sample-product', methods=['GET'])
def get_sample_product():
    sample_product = {
        "product_name": "Sample Book",
        "price": 19.99
    }
    return jsonify(sample_product)

if __name__ == '__main__':
    app.run(debug=True)

