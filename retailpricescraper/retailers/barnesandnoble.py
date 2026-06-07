from retailpricescraper.data import GraphicNovel
from retailpricescraper.scraper import Scraper


class BarnesAndNoble(Scraper):
    def __init__(self, browser):
        self.browser = browser

    async def scrape(self, isbn: str, title: str) -> GraphicNovel:
        context = await self.browser.new_context(
            user_agent="Mozilla/5.0 ... Chrome/137",
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )

        page = await context.new_page()
        page.set_default_timeout(8000)

        await page.goto(
            f"https://www.barnesandnoble.com/search?q={isbn}", timeout=12000
        )

        title = ""
        price = None
        url = None

        try:
            title = (
                await page.locator(".product-item-card__title").first.text_content()
            ).strip()

            price_text = await page.locator(
                ".product-item-card__current-price"
            ).first.text_content()
            price = float(price_text.replace("$", "").strip())

            href = (
                (
                    await page.locator(".product-item-card__title")
                    .first.locator("xpath=ancestor::a")
                    .get_attribute("href")
                )
                .strip()
                .split("?", 1)[0]
            )
            url = f"https://www.barnesandnoble.com{href}"
        except Exception as e:
            print(f"Unable to scrape {isbn} from Barnes & Noble: {e}")

        await page.close()

        return GraphicNovel(
            isbn=isbn,
            retailer="Barnes & Noble",
            title=title,
            price=price,
            url=url,
        )
