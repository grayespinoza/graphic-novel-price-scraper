from retailpricescraper.data import GraphicNovel
from retailpricescraper.scraper import Scraper


class OrganicPricedBooks(Scraper):
    def __init__(self, browser):
        self.browser = browser

    async def scrape(self, isbn: str) -> GraphicNovel:
        page = await self.browser.new_page()
        page.set_default_timeout(5000)

        await page.goto(
            f"https://www.panelboundcomics.com/search?q={isbn}", timeout=10000
        )

        title = None
        price = None
        url = None

        try:
            title = (
                await page.locator("a.full-unstyled-link").first.inner_text()
            ).strip()

            price_text = await page.locator(
                "span.price-item.price-item--sale.price-item--last"
            ).first.inner_text()
            price = float(price_text.replace("$", "").replace("USD", "").strip())

            href = (
                await page.locator("a.full-unstyled-link").first.get_attribute("href")
            ).strip()
            url = f"https://www.panelboundcomics.com{href}"
        except Exception as e:
            print(f"Unable to scrape {isbn} from Organic Priced Books: {e}")

        await page.close()

        return GraphicNovel(
            isbn=isbn,
            retailer="Organic Priced Books",
            title=title,
            price=price,
            url=url,
        )
