import requests
import time
from bs4 import BeautifulSoup
import logging
from robot_check import RoboCheck

class CheaperScraper:
    def __init__(self, base_url:str, user_agent: str= "CheaperBot/0.1", delay: float=2.0):
        self.base_url = base_url.rstrip('/')
        self.delay = delay
        self.user_agent = user_agent

        #initialize session
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

        # robot logic checks if there are instances not able to be 
        self.robots = RoboCheck(base_url, user_agent)

    def fetch(self, path: str="/"):
        #Fetch a URL path if allowed
        if not self.robots.can_fetch(path):
            logging.warning(f"Disallowed by robots.txt: {path}")
            return None

        url = self.base_url + path
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            time.sleep(self.delay)  # delay to simulate a user
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None
        
    # def parse(self, html: str):
    #     soup = BeautifulSoup(html, "html.parser")
    #     return [item.get_text(strip=True) for item in soup.find_all("h2")]

    def parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        results = []
    
        for book in soup.find_all("article", class_="product_pod"):
            title = book.h3.a["title"]
            results.append(title)
    
        return results
    
    

    def scrape(self, paths):
        #Fetch and parse a list of URLs
        results = {}
        for path in paths:
            html = self.fetch(path)
            if html:
                results[path] = self.parse(html)
        return results