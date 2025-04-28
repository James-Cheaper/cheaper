import unittest
import time

from webscraper.src.Cheaper_Scraper import CheaperScraper
from webscraper.src.fetch_utils import cached_get

#to test, be in the webscraper directory and use the following command in terminal
# python -m unittest webscraper.src.tests.test_fetch_and_cache -v



class TestCheaperScraperFetchCache(unittest.TestCase):
    
    def setUp(self):
        self.scraper = CheaperScraper("https://books.toscrape.com")
        cached_get.cache_clear()  # Reset cache before each test

    def test_valid_fetch(self):
        html = self.scraper.fetch("/")
        self.assertIsInstance(html, str)
        self.assertIn("<html", html.lower())

    def test_invalid_path_fetch(self):
        html = self.scraper.fetch("/this-page-does-not-exist")
        # Even though it doesn't exist, the site may return a 200 with a 404 page
        self.assertTrue(html is None or "<html" in html.lower())

    def test_cache_effectiveness(self):
        start = time.time()
        self.scraper.fetch("/")  # First fetch
        time1 = time.time() - start

        start = time.time()
        self.scraper.fetch("/")  # Second fetch (should be cached)
        time2 = time.time() - start

        cache_info = cached_get.cache_info()
        self.assertLess(time2, time1)
        self.assertGreaterEqual(cache_info.hits, 1)

    def test_non_http_url(self):
        with self.assertRaises(ValueError):
            CheaperScraper("not_a_real_url")
    
    def test_cache_timing_and_stats(self):
        print("\n=== Cache Timing and Stats Test ===")

        # First fetch (expected to be slow and hit the network)
        start = time.time()
        html1 = self.scraper.fetch("/")
        time1 = round(time.time() - start, 2)
        print(f"First fetch took: {time1} seconds")

        # Second fetch (expected to be fast due to cache)
        start = time.time()
        html2 = self.scraper.fetch("/")
        time2 = round(time.time() - start, 2)
        print(f"Second fetch took: {time2} seconds")

        # Confirm that the second fetch was faster
        self.assertLess(time2, time1, "Second fetch should be faster due to caching")

        # Print and assert cache stats
        stats = cached_get.cache_info()
        print("Cache stats:", stats)
        self.assertGreaterEqual(stats.hits, 1, "There should be at least 1 cache hit")




if __name__ == "__main__":
    unittest.main()