from graphicnovelpricescraper.data import GraphicNovel
from graphicnovelpricescraper.scraper import Scraper


class Amazon(Scraper):
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

        title = ""
        price = None
        url = None

        try:
            await page.goto(
                f"https://www.amazon.com/s?k={isbn}&i=stripbooks", timeout=12000
            )

            title = await page.locator(
                "div[data-cy='title-recipe'] h2 span"
            ).first.text_content()
            if title:
                title = title.strip()

            price_whole = await page.locator("span.a-price-whole").first.text_content()
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
            await context.close()

        return GraphicNovel(
            isbn=isbn,
            retailer="Amazon",
            title=title,
            price=price,
            url=url,
        )
