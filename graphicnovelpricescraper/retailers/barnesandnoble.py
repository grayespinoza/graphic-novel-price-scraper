from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class BarnesAndNoble(Scraper):
    async def scrape(self, isbn: int, title: str) -> GraphicNovel:
        async with self.semaphore:
            if self.context is None:
                raise RuntimeError("Context not initialized!")

            page = await self.context.new_page()

            title = ""
            price = None
            url = None

            try:
                await page.goto(
                    f"https://www.barnesandnoble.com/search?q={isbn}",
                    timeout=12000,
                    wait_until="domcontentloaded",
                )

                title = await page.locator(
                    ".product-item-card__title"
                ).first.text_content()
                if title:
                    title = title.strip()

                price_text = await page.locator(
                    ".product-item-card__current-price"
                ).first.text_content()
                if price_text:
                    price_text = price_text.strip()
                    price = float(price_text.replace("$", ""))

                href = (
                    await page.locator(".product-item-card__title")
                    .first.locator("xpath=ancestor::a")
                    .get_attribute("href")
                )
                if href:
                    href = href.strip().split("?", 1)[0]
                    url = f"https://www.barnesandnoble.com{href}"
            except Exception as e:
                print(f"Unable to scrape {isbn} from Barnes & Noble: {e}")
            finally:
                await page.close()

            return GraphicNovel(
                isbn=isbn,
                retailer="Barnes & Noble",
                title=title,
                price=price,
                url=url,
            )
