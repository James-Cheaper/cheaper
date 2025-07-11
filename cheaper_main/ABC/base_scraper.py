from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseScraper(ABC):

    @abstractmethod
    def __init__(self, base_url: str, user_agent: str, delay: float) -> None:
        """Initialize the scraper with base parameters.
        
        Args:
            base_url: The base URL to scrape
            user_agent: User agent string to identify the scraper
            delay: Time in seconds to wait between requests
        """
        pass

    @abstractmethod
    def fetch(self, path: str) -> Optional[str]:
        """Fetch content from a specific path.
        
        Args:
            path: The URL path to fetch
            
        Returns:
            HTML content as string if successful, None otherwise
        """
        pass

    @abstractmethod
    def parse(self, html: str) -> List[str]:
        """Parse HTML content.
        
        Args:
            html: The HTML content to parse
            
        Returns:
            List of parsed items from the HTML
        """
        pass

    @abstractmethod
    def scrape(self, paths: List[str]) -> Dict[str, List[str]]:
        """Scrape multiple paths.
        
        Args:
            paths: List of URL paths to scrape
            
        Returns:
            Dictionary mapping paths to their parsed results
        """
        pass
