import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cheaper_main.Scraper.Cheaper_Scraper import CheaperScraper
import cheaper_main.api.ebay_api


def main():
    EbayAPI = cheaper_main.api.EbayAPI # instantiate because class
    
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
    with open("output.json", "w") as f:
        json.dump(results, f, indent=2)





if __name__ == "__main__":
    main()


