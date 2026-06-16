import pytest
from playwright.async_api import async_playwright

from graphicnovelpricescraper.retailers.barnesandnoble import BarnesAndNoble


@pytest.mark.asyncio
async def test_scrape():
    isbn = 9781779515681

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        retailer = BarnesAndNoble(browser)
        await retailer.create_context()

        try:
            data = await retailer.scrape(isbn, "")

            assert data.isbn == isbn
            assert data.retailer == "Barnes & Noble"

            if data.title is not None:
                assert isinstance(data.title, str)
            if data.price is not None:
                assert data.price > 0.0
            if data.url is not None:
                assert data.url.startswith("https://www.barnesandnoble.com")
        finally:
            if retailer.context is not None:
                await retailer.context.close()
            await browser.close()
