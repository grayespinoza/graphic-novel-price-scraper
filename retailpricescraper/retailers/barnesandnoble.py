from retailpricescraper.data import GraphicNovel
from retailpricescraper.scraper import Scraper


class BarnesAndNoble(Scraper):
    def __init__(self, browser):
        self.browser = browser

    async def scrape(self, isbn: str) -> GraphicNovel:
        page = await self.browser.new_page()

        await page.goto(f"https://www.barnesandnoble.com/search?q={isbn}")

        title = await page.locator(".product-item-card__title").text_content()
        price_text = await page.locator(
            ".product-item-card__current-price"
        ).text_content()
        href = (
            await page.locator(".product-item-card__title")
            .locator("xpath=ancestor::a")
            .get_attribute("href")
        )

        await page.close()

        return GraphicNovel(
            isbn=isbn,
            title=title,
            price=float(price_text.replace("$", "").strip()),
            retailer="Barnes & Noble",
            url=f"https://www.barnesandnoble.com{href}",
        )
