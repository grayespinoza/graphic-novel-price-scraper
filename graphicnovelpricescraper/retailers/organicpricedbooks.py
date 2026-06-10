from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class OrganicPricedBooks(Scraper):
    async def scrape(self, isbn: int, title: str) -> GraphicNovel:
        async with self.semaphore:
            if self.context is None:
                raise RuntimeError("Context not initialized!")

            page = await self.context.new_page()

            price = None
            url = None

            try:
                await page.goto(
                    f"https://www.panelboundcomics.com/search?q={title}",
                    timeout=12000,
                    wait_until="domcontentloaded",
                )

                title_text = await page.locator(
                    "a.full-unstyled-link"
                ).first.inner_text()
                if title_text:
                    title_text = title_text.strip()

                if title.lower() in title_text.lower():
                    title = title_text

                    price_text = await page.locator(
                        "span.price-item.price-item--sale.price-item--last"
                    ).first.inner_text()
                    if price_text:
                        price_text = price_text.strip()
                        price = float(price_text.replace("$", "").replace("USD", ""))

                    href = await page.locator(
                        "a.full-unstyled-link"
                    ).first.get_attribute("href")
                    if href:
                        href = href.strip().split("?", 1)[0]
                        url = f"https://www.panelboundcomics.com{href}"
                else:
                    title = ""
            except Exception as e:
                print(f"Unable to scrape {isbn} from Organic Priced Books: {e}")
            finally:
                await page.close()

            return GraphicNovel(
                isbn=isbn,
                retailer="Organic Priced Books",
                title=title,
                price=price,
                url=url,
            )
