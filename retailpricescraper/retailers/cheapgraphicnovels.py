from retailpricescraper.data import GraphicNovel
from retailpricescraper.scraper import Scraper


class CheapGraphicNovels(Scraper):
    def __init__(self, browser):
        self.browser = browser

    async def scrape(self, isbn: str) -> GraphicNovel:
        page = await self.browser.new_page()
        page.set_default_timeout(5000)

        await page.goto(
            f"https://cheapgraphicnovels.com/?target=search&mode=search&substring={isbn}"
        )

        title = None
        price = None
        url = None

        # TODO: filter out (NICK AND DENT)
        # Using ".fn.url:not(:has-text('Nick and Dent'))" works, but we would need a different solution for price.
        # Tried f"https://cheapgraphicnovels.com/?target=search&mode=search&substring={isbn}&sortOrder=asc", but that has no effect.

        try:
            title = (await page.locator(".fn.url").first.text_content()).strip()

            price_text = await page.locator(".price.product-price").first.text_content()
            price = float(price_text.replace("$", "").strip())

            href = (await page.locator(".fn.url").first.get_attribute("href")).strip()
            url = f"https://cheapgraphicnovels.com/{href}"
        except Exception as e:
            print(f"Unable to scrape {isbn} from Cheap Graphic Novels: {e}")

        await page.close()

        return GraphicNovel(
            isbn=isbn,
            retailer="Cheap Graphic Novels",
            title=title,
            price=price,
            url=url,
        )
