import asyncio
import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from playwright.async_api import async_playwright

from retailpricescraper.retailers.amazon import Amazon
from retailpricescraper.retailers.barnesandnoble import BarnesAndNoble
from retailpricescraper.retailers.cheapgraphicnovels import CheapGraphicNovels
from retailpricescraper.retailers.organicpricedbooks import OrganicPricedBooks

with open("isbns.csv") as csvfile:
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
        ]

        for retailer in retailers:
            for isbn in isbns:
                price = await retailer.scrape(isbn[0])
                prices.append(price)

        await browser.close()

    with open("prices.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        if os.stat("prices.csv").st_size == 0:
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
