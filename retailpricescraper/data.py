from dataclasses import dataclass


@dataclass
class GraphicNovel:
    isbn: str
    retailer: str
    title: str | None = None
    price: float | None = None
    url: str | None = None
