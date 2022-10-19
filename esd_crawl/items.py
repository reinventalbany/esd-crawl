# https://docs.scrapy.org/en/latest/topics/items.html#dataclass-objects
from dataclasses import dataclass, field


@dataclass
class PDF:
    title: str
    source: str
    file_urls: list[str]
    img_paths: list[str] = field(default_factory=list)
