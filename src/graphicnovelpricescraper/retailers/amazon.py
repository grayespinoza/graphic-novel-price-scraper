from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class Amazon(Scraper):
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
                    f"https://www.amazon.com/s?k={isbn}&i=stripbooks",
                    wait_until="domcontentloaded",
                )

                title = await page.locator(
                    "div[data-cy='title-recipe'] h2 span"
                ).first.text_content()
                if title:
                    title = title.strip()

                price_whole = await page.locator(
                    "span.a-price-whole"
                ).first.text_content()
                price_fraction = await page.locator(
                    "span.a-price-fraction"
                ).first.text_content()
                if price_whole and price_fraction:
                    price_whole = price_whole.strip()
                    price_fraction = price_fraction.strip()
                    price = float(f"{price_whole}{price_fraction}")

                href = await page.locator(
                    "div[data-cy='title-recipe'] a"
                ).first.get_attribute("href")
                if href:
                    href = href.strip().split("?", 1)[0]
                    url = f"https://www.amazon.com{href}"
            except Exception as e:
                print(f"Unable to scrape {isbn} from Amazon: {e}")
            finally:
                await page.close()

            return GraphicNovel(
                isbn=isbn,
                retailer="Amazon",
                title=title,
                price=price,
                url=url,
            )
