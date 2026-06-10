import re
from urllib.parse import quote_plus

from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class InStockTrades(Scraper):
    async def scrape(self, isbn: int, title: str) -> GraphicNovel:
        async with self.semaphore:
            if self.context is None:
                raise RuntimeError("Context not initialized!")

            page = await self.context.new_page()

            price = None
            url = None

            try:
                await page.goto(
                    f"https://www.instocktrades.com/search?term={quote_plus(title)}",
                    wait_until="domcontentloaded",
                )

                title_text = await page.locator(".title").first.inner_text()

                if title_text:
                    title_text = title_text.lower()
                    title_text = re.sub(r"\b(tp|hc)\b", "", title_text)
                    title_text = re.sub(r"[^a-z0-9\s]", " ", title_text)
                    title_text = re.sub(r"\s+", " ", title_text).strip()

                title = title.lower()
                title = re.sub(r"[^a-z0-9\s]", " ", title)
                title = re.sub(r"\s+", " ", title).strip()

                if title in title_text:
                    title = await page.locator(".title").first.inner_text()

                    price_text = await page.locator(".price").first.inner_text()
                    if price_text:
                        price_text = price_text.strip()
                        price = float(price_text.replace("$", ""))

                    href = await page.locator(".title a").first.get_attribute("href")
                    if href:
                        href = href.strip().split("?", 1)[0]
                        url = f"https://www.instocktrades.com{href}"
                else:
                    title = ""
            except Exception as e:
                print(f"Unable to scrape {isbn} from In Stock Trades: {e}")
            finally:
                await page.close()

            return GraphicNovel(
                isbn=isbn,
                retailer="In Stock Trades",
                title=title,
                price=price,
                url=url,
            )
