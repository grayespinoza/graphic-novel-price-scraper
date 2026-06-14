from urllib.parse import quote_plus

from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class InStockTrades(Scraper):
    async def scrape(self, isbn: int, title: str) -> GraphicNovel:
        async with self.semaphore:
            if self.context is None:
                raise RuntimeError("Context not initialized!")

            page = await self.context.new_page()
            page.set_default_timeout(12000)

            price = None
            url = None

            try:
                await page.goto(
                    f"https://www.instocktrades.com/search?term={quote_plus(title)}",
                    wait_until="domcontentloaded",
                )

                title = await page.locator(".title").first.inner_text()

                price_text = await page.locator(".price").first.inner_text()
                if price_text:
                    price_text = price_text.strip()
                    price = float(price_text.replace("$", ""))

                href = await page.locator(".title a").first.get_attribute("href")
                if href:
                    href = href.strip().split("?", 1)[0]
                    url = f"https://www.instocktrades.com{href}"

                try:
                    await page.goto(url, wait_until="domcontentloaded")

                    upc = await page.locator(".upc").text_content()
                    if upc:
                        upc = int(upc.replace("UPC:", "").strip())

                    if upc != isbn:
                        title = ""
                        price = None
                        url = None
                except Exception as e:
                    print(f"Unable to verify {isbn} from In Stock Trades: {e}")
                    title = ""
                    price = None
                    url = None
            except Exception as e:
                print(f"Unable to scrape {isbn} from In Stock Trades: {e}")
                title = ""
                price = None
                url = None
            finally:
                await page.close()

            return GraphicNovel(
                isbn=isbn,
                retailer="In Stock Trades",
                title=title,
                price=price,
                url=url,
            )
