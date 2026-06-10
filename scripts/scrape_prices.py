import asyncio
import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from playwright.async_api import async_playwright

from graphicnovelpricescraper.retailers.amazon import Amazon
from graphicnovelpricescraper.retailers.barnesandnoble import BarnesAndNoble
from graphicnovelpricescraper.retailers.cheapgraphicnovels import CheapGraphicNovels
from graphicnovelpricescraper.retailers.instocktrades import InStockTrades
from graphicnovelpricescraper.retailers.organicpricedbooks import OrganicPricedBooks

with open(
    "isbns.csv",
    newline="",
    encoding="utf-8",
) as csvfile:
    isbns = list(csv.reader(csvfile))


async def main():
    prices = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        retailers = [
            CheapGraphicNovels(browser),
            BarnesAndNoble(browser),
            OrganicPricedBooks(browser),
            Amazon(browser),
            InStockTrades(browser),
        ]

        for retailer in retailers:
            await retailer.create_context()

        try:
            tasks = [
                retailer.scrape(int(isbn), title)
                for retailer in retailers
                for isbn, title in isbns
            ]
            prices = await asyncio.gather(*tasks)
        finally:
            for retailer in retailers:
                if retailer.context is not None:
                    await retailer.context.close()
            await browser.close()

    with open(
        f"prices_{datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%y%m%d')}.csv",
        "a",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        writer = csv.writer(csvfile)

        if (
            os.stat(
                f"prices_{datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%y%m%d')}.csv"
            ).st_size
            == 0
        ):
            writer.writerow(["date", "isbn", "retailer", "title", "price", "url"])

        for price in prices:
            writer.writerow(
                [
                    datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%y%m%d"),
                    price.isbn,
                    price.retailer,
                    price.title,
                    price.price,
                    price.url,
                ]
            )


if __name__ == "__main__":
    asyncio.run(main())
