from Cheaper_Scraper import CheaperScraper

def main():
    scraper = CheaperScraper("https://www.walmart.com",
                             user_agent="CheaperBot/0.1",
                             delay=2.0)
    pages = ["/", 
             "/about", 
             "/shop/clothing-and-accessories/new-arrivals",
             "/ip/Siilsaa-Womens-Tops-2024-Soft-Short-Sleeve-Casual-Blouses-Shirt-Crewneck-Fashion-Knit-Pullover-Sweater-White-M/13496269884?classType=VARIANT&athbdg=L1600"]
    results = scraper.scrape(pages)
    for path, items in results.items():
        print(path, items)

if __name__ == "__main__":
    main()