# https://docs.scrapy.org/en/latest/topics/items.html#dataclass-objects
from dataclasses import dataclass, field


@dataclass
class Table:
    img_path: str
    page_num: int


@dataclass
class PDF:
    title: str
    source: str
    file_urls: list[str]
    tables: list[Table] = field(default_factory=list)
