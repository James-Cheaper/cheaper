from abc import ABC, abstractmethod

class ScraperAPIInterface(ABC):

    @abstractmethod
    def get_scraped_data(self, paths: list[str]) -> dict:
        """Given a list of paths, return scraped results."""
        pass
