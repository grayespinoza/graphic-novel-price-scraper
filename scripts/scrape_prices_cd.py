import asyncio
import csv
import os

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
    shard_index = int(os.environ["SHARD_INDEX"])
    date = os.environ["DATE"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        retailers_classes = [
            CheapGraphicNovels,
            BarnesAndNoble,
            #OrganicPricedBooks,
            Amazon,
            InStockTrades,
        ]

        retailer = retailers_classes[shard_index](browser)
        await retailer.create_context()

        try:
            tasks = [retailer.scrape(int(isbn), title) for isbn, title in isbns]
            prices = await asyncio.gather(*tasks)
        finally:
            if retailer.context is not None:
                await retailer.context.close()
            await browser.close()

    with open(
        f"prices_{date}_shard{shard_index}.csv",
        "a",
        newline="",
        encoding="utf-8",
    ) as csvfile:
        writer = csv.writer(csvfile)

        if os.stat(f"prices_{date}_shard{shard_index}.csv").st_size == 0:
            writer.writerow(["date", "isbn", "retailer", "title", "price", "url"])

        for price in prices:
            writer.writerow(
                [
                    date,
                    price.isbn,
                    price.retailer,
                    price.title,
                    price.price,
                    price.url,
                ]
            )


if __name__ == "__main__":
    asyncio.run(main())
