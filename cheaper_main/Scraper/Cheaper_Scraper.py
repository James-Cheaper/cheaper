import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging
from typing import Dict, List, Optional
from cheaper_main.ABC.base_scraper import BaseScraper
from cheaper_main.Scraper.robot_check import RoboCheck
from cheaper_main.Scraper.fetch_utils import cached_get
from functools import lru_cache
<<<<<<< HEAD:cheaper_main/Scraper/Cheaper_Scraper.py
=======

>>>>>>> primary:webscraper/src/Cheaper_Scraper.py




class CheaperScraper(BaseScraper):
    def __init__(self, base_url: str = "", user_agent: str = "CheaperBot/0.1", delay: float = 2.0) -> None:
        """Initialize the scraper with base parameters.
       
        Args:
            base_url: The base URL to scrape
            user_agent: User agent string to identify the scraper
            delay: Time in seconds to wait between requests
        """
        parsed_url = urlparse(base_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Invalid base URL: {base_url}")
        
        self.base_url = base_url.rstrip('/')
        self.delay = delay
        self.user_agent = user_agent


        #initialize session
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})


        # robot logic checks if there are instances not able to be
        self.robots = RoboCheck(base_url, user_agent)


    

    def fetch(self, path: str = "/") -> Optional[str]:
        """Fetch content from a specific path.
       
        Args:
            path: The URL path to fetch
           
        Returns:
            HTML content as string if successful, None otherwise
        """
        #Fetch a URL path if allowed
        if not self.robots.can_fetch(path):
            logging.warning(f"Disallowed by robots.txt: {path}")
            return None

        url = self.base_url + path
        cached_before = cached_get.cache_info().hits
        html = cached_get(url, self.user_agent)
        cached_after = cached_get.cache_info().hits

        if cached_after == cached_before:
            time.sleep(self.delay)

        return html
       
    def parse(self, html: str) -> List[str]:
        """Parse HTML content.
       
        Args:
            html: The HTML content to parse
           
        Returns:
            List of parsed items from the HTML
        """
        soup = BeautifulSoup(html, "html.parser")
        results = []
   
        for book in soup.find_all("article", class_="product_pod"):
            title = book.h3.a["title"]
            results.append(title)
   
        return results
   
   


    def scrape(self, paths: List[str]) -> Dict[str, List[str]]:
        """Scrape multiple paths.
       
        Args:
            paths: List of URL paths to scrape
           
        Returns:
            Dictionary mapping paths to their parsed results
        """
        #Fetch and parse a list of URLs
        results: Dict[str, List[str]] = {}
        for path in paths:
            html = self.fetch(path)
            if html:
                results[path] = self.parse(html)
        return results
    
    def get_scraped_data(self, paths: List[str]) -> Dict[str, List[str]]:
        return self.scrape(paths)
