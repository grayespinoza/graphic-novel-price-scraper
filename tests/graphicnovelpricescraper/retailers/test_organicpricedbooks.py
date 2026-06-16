import pytest
from playwright.async_api import async_playwright

from graphicnovelpricescraper.retailers.organicpricedbooks import OrganicPricedBooks


@pytest.mark.asyncio
async def test_scrape():
    isbn = 9781779515681
    title = "Supergirl: Woman of Tomorrow"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        retailer = OrganicPricedBooks(browser)
        await retailer.create_context()

        try:
            data = await retailer.scrape(isbn, title)

            assert data.isbn == isbn
            assert data.retailer == "Organic Priced Books"

            if data.title is not None:
                assert isinstance(data.title, str)
            if data.price is not None:
                assert data.price > 0.0
            if data.url is not None:
                assert data.url.startswith("https://www.panelboundcomics.com")
        finally:
            if retailer.context is not None:
                await retailer.context.close()
            await browser.close()
