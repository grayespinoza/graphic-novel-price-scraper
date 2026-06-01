from retailpricescraper.data import GraphicNovel
from retailpricescraper.scraper import Scraper


class Amazon(Scraper):
    def __init__(self, browser):
        self.browser = browser

    async def scrape(self, isbn: str) -> GraphicNovel:
        page = await self.browser.new_page()

        await page.goto(f"https://www.amazon.com/s?k={isbn}&i=stripbooks")

        title = await page.locator("div[data-cy='title-recipe'] h2 span").text_content()
        price_whole = await page.locator("span.a-price-whole").first.text_content()
        price_fraction = await page.locator(
            "span.a-price-fraction"
        ).first.text_content()
        href = await page.locator("div[data-cy='title-recipe'] a").first.get_attribute(
            "href"
        )

        await page.close()

        return GraphicNovel(
            isbn=isbn,
            title=title,
            price=float(f"{price_whole}{price_fraction}"),
            retailer="Amazon",
            url=f"https://www.amazon.com{href}",
        )
