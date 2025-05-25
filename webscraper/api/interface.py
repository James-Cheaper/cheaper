from abc import ABC, abstractmethod
from typing import Dict
from accounts.models import Product


class EbayABC(ABC):

    @abstractmethod
    def get_scraped_data(self, paths: list[str]) -> Product:
        """Given a list of paths, return scraped results."""
        pass

    @abstractmethod
    def search_item(self, query: str) -> Product:
        pass
