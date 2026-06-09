from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class OrganicPricedBooks(Scraper):
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
                f"https://www.panelboundcomics.com/search?q={title}", timeout=12000
            )

            title_text = await page.locator("a.full-unstyled-link").first.inner_text()
            if title_text:
                title_text = title_text.strip()

            if title.lower() in title_text.lower():
                title = title_text

                price_text = await page.locator(
                    "span.price-item.price-item--sale.price-item--last"
                ).first.inner_text()
                price = float(price_text.replace("$", "").replace("USD", "").strip())

                href = await page.locator("a.full-unstyled-link").first.get_attribute(
                    "href"
                )
                if href:
                    href = href.strip().split("?", 1)[0]
                url = f"https://www.panelboundcomics.com{href}"
            else:
                title = ""
        except Exception as e:
            print(f"Unable to scrape {isbn} from Organic Priced Books: {e}")
        finally:
            await context.close()

        return GraphicNovel(
            isbn=isbn,
            retailer="Organic Priced Books",
            title=title,
            price=price,
            url=url,
        )
