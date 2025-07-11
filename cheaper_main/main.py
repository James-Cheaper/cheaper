from flask import Flask, request , jsonify
import json
#import time  # for testing
# i added these imports below because when i ran it it wasnt finding the folders
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cheaper_main.Scraper.Cheaper_Scraper import CheaperScraper

app = Flask(__name__)

#python main.py will run it in the background git bash
#to stop put pm2 stop Cheaper in git bash
@app.route('/')
def scrape():

    # Set up the scraper for a simple legal-to-scrape website
    scraper = CheaperScraper("https://books.toscrape.com",
                             user_agent="CheaperBot/0.1",
                             delay=2.0)
    
    # Define which pages you want to scrape (you can use "/" for homepage)
    pages = ["/"]

    # Use the scraper to fetch and parse the pages
    results = scraper.scrape(pages)

    # Show the output in the terminal
    for path, items in results.items():
        print(f"\nScraped from {path}:")
        for item in items:
            print("-", item)

    # Save the output to a JSON file
    #with open("output.json", "w") as f:
        #json.dump(results, f, indent=2)
    return jsonify(results)

@app.route('/api/products/search', methods=['GET'])
def ebay_search():
    try:
        from api.ebay_api.EbayAPI import EbayAPI
        #instantiate object
        ebay_api = EbayAPI()

        product = request.args.get('product')
        #The route will look like this
        # http://127.0.0.1:5000/api/products/search?product=
        #after product= type any generic item to receive json like ?product=clothes
        #put that in the address bar
        
        print(f"product = {product}")
        if not product:
            return jsonify({"error": "missing ?product=parameter"}),400
        response = ebay_api.search_item(product)

        return jsonify({
            "name": response.name,
            "price": response.price,
            "currency": response.currency,
            "url": response.url
        })

    except Exception as e:
        print("failed to import",e)
        return jsonify({"error": str(e)}), 500
    



if __name__ == "__main__":#
    app.run(debug=True)
