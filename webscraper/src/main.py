from CheaperScraper import CheaperScraper

def main():
    scraper = CheaperScraper("https://youtube.com",
                             user_agent="CheaperBot/0.1",
                             delay=2.0)
    pages = ["/", "/about", "/blog"]
    results = scraper.scrape(pages)
    for path, items in results.items():
        print(path, items)

if __name__ == "__main__":
    main()