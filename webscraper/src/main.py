# from Cheaper_Scraper import CheaperScraper

# def main():
#     scraper = CheaperScraper("https://www.walmart.com",
#                              user_agent="CheaperBot/0.1",
#                              delay=2.0)
#     pages = ["/", 
#              "/about", 
#              "/shop/clothing-and-accessories/new-arrivals",
#              "/ip/Siilsaa-Womens-Tops-2024-Soft-Short-Sleeve-Casual-Blouses-Shirt-Crewneck-Fashion-Knit-Pullover-Sweater-White-M/13496269884?classType=VARIANT&athbdg=L1600"]
#     results = scraper.scrape(pages)
#     for path, items in results.items():
#         print(path, items)

# if __name__ == "__main__":
#     main()

from Cheaper_Scraper import CheaperScraper
import json

def main():
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
