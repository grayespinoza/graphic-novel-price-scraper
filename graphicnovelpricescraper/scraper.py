from abc import ABC, abstractmethod

from graphicnovelpricescraper.data import GraphicNovel


class Scraper(ABC):
    @abstractmethod
    async def scrape(self, isbn: str, title: str) -> GraphicNovel:
        """Scrape a graphic novel by ISBN and return data."""
        pass
