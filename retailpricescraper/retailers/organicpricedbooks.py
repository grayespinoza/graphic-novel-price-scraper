from retailpricescraper.data import GraphicNovel
from retailpricescraper.scraper import Scraper


class OrganicPricedBooks(Scraper):
    def __init__(self, browser):
        self.browser = browser

    async def scrape(self, isbn: str) -> GraphicNovel:
        page = await self.browser.new_page()

        await page.goto(f"https://www.panelboundcomics.com/search?q={isbn}")

        title = await page.locator("#CardLink--8810742776026").inner_text()
        price_text = await page.locator(
            "span.price-item.price-item--sale.price-item--last"
        ).inner_text()
        href = await page.locator("#CardLink--8810742776026").get_attribute("href")

        await page.close()

        return GraphicNovel(
            isbn=isbn,
            title=title,
            price=float(price_text.replace("$", "").replace("USD", "").strip()),
            retailer="Organic Priced Books",
            url=f"https://www.panelboundcomics.com{href}",
        )
