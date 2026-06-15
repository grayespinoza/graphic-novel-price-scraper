from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class CheapGraphicNovels(Scraper):
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
                    f"https://cheapgraphicnovels.com/?target=search&mode=search&substring={isbn}",
                    wait_until="domcontentloaded",
                )

                title = await page.locator(".fn.url").first.text_content()
                if title:
                    title = title.strip()

                price_text = await page.locator(
                    ".price.product-price"
                ).first.text_content()
                if price_text:
                    price_text = price_text.strip()
                    price = float(price_text.replace("$", ""))

                href = await page.locator(".fn.url").first.get_attribute("href")
                if href:
                    href = href.strip().split("?", 1)[0]
                    url = f"https://cheapgraphicnovels.com/{href}"
            except Exception as e:
                print(f"Unable to scrape {isbn} from Cheap Graphic Novels: {e}")
            finally:
                await page.close()

            return GraphicNovel(
                isbn=isbn,
                retailer="Cheap Graphic Novels",
                title=title,
                price=price,
                url=url,
            )
