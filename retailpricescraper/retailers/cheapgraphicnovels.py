from retailpricescraper.data import GraphicNovel
from retailpricescraper.scraper import Scraper


class CheapGraphicNovels(Scraper):
    def __init__(self, browser):
        self.browser = browser

    async def scrape(self, isbn: str) -> GraphicNovel:
        page = await self.browser.new_page()

        await page.goto(
            f"https://cheapgraphicnovels.com/?target=search&mode=search&substring={isbn}"
        )

        title = await page.locator(".fn.url").text_content()
        price_text = await page.locator(".price.product-price").text_content()
        href = await page.locator(".fn.url").get_attribute("href")

        await page.close()

        return GraphicNovel(
            isbn=isbn,
            title=title,
            price=float(price_text.replace("$", "").strip()),
            retailer="Cheap Graphic Novels",
            url=f"https://cheapgraphicnovels.com/{href}",
        )
