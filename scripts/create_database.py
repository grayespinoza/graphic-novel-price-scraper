import csv
import sqlite3

conn = sqlite3.connect("graphic_novels.db")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS graphic_novels")
cur.execute("DROP TABLE IF EXISTS prices")

cur.execute("""
CREATE TABLE graphic_novels (
    isbn INTEGER PRIMARY KEY,
    title TEXT
)
""")

cur.execute("""
CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date INTEGER,
    isbn INTEGER,
    retailer TEXT,
    price REAL,
    url TEXT,
    FOREIGN KEY (isbn) REFERENCES graphic_novels(isbn)
)
""")

cur.execute("""
CREATE INDEX idx_prices_date
ON prices(date)
""")

cur.execute("""
CREATE INDEX idx_prices_isbn
ON prices(isbn)
""")

cur.execute("""
CREATE INDEX idx_prices_retailer
ON prices(retailer)
""")

with open(
    "prices.csv",
    newline="",
    encoding="utf-8",
) as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        isbn = int(row["isbn"])
        if row["title"] and row["title"].strip():
            title = row["title"].strip()
        else:
            title = None

        if title:
            cur.execute(
                """
                INSERT OR IGNORE INTO graphic_novels (isbn, title)
                VALUES (?, ?)
                """,
                (isbn, title),
            )

        cur.execute(
            """
            INSERT INTO prices (
                date,
                isbn,
                retailer,
                price,
                url
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(row["date"]),
                isbn,
                row["retailer"],
                float(row["price"]) if row["price"] else None,
                row["url"] if row["url"] else None,
            ),
        )

conn.commit()
conn.close()
