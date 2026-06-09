import re
from urllib.parse import quote_plus

from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class InStockTrades(Scraper):
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

        price = None
        url = None

        try:
            await page.goto(
                f"https://www.instocktrades.com/search?term={quote_plus(title)}",
                timeout=180000,
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
            await context.close()

        return GraphicNovel(
            isbn=isbn,
            retailer="In Stock Trades",
            title=title,
            price=price,
            url=url,
        )
