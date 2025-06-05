import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, jsonify, request
from webscraper.src.Cheaper_Scraper import CheaperScraper

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

