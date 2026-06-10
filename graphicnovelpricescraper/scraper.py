import asyncio
from abc import ABC, abstractmethod

from graphicnovelpricescraper.data import GraphicNovel


class Scraper(ABC):
    def __init__(self, browser):
        self.browser = browser
        self.context = None
        self.semaphore = asyncio.Semaphore(5)

    async def create_context(self):
        self.context = await self.browser.new_context(
            locale="en-US",
            timezone_id="America/Los_Angeles",
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        )

    @abstractmethod
    async def scrape(self, isbn: int, title: str) -> GraphicNovel:
        """Scrape a graphic novel and return data."""
        pass
