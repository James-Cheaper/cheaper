from abc import ABC, abstractmethod
from typing import Dict

class ScraperAPIInterface(ABC):

    @abstractmethod
    def get_scraped_data(self, paths: list[str]) -> dict:
        """Given a list of paths, return scraped results."""
        pass

    @abstractmethod
    def search_item(self, query: str) -> Dict[str, str]:
        pass
