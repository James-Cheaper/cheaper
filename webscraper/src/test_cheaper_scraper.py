import unittest
from webscraper.src.Cheaper_Scraper import CheaperScraper

class TestCheaperScraper(unittest.TestCase):

    def setUp(self):
        self.scraper = CheaperScraper("https://books.toscrape.com")

    def test_can_fetch_root_path(self):
        self.assertTrue(self.scraper.robots.can_fetch("/"))

    def test_fetch_returns_html(self):
        html = self.scraper.fetch("/")
        self.assertIsInstance(html, str)
        self.assertIn("<html", html)

    def test_parse_returns_list(self):
        html = self.scraper.fetch("/")
        result = self.scraper.parse(html)
        self.assertIsInstance(result, list)

    def test_scrape_structure(self):
        paths = ["/"]
        result = self.scraper.scrape(paths)
        self.assertIn("/", result)
        self.assertIsInstance(result["/"], list)

if __name__ == '__main__':
    unittest.main()
