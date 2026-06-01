from dataclasses import dataclass


@dataclass
class GraphicNovel:
    isbn: str
    title: str
    price: float
    retailer: str
    url: str
