# https://docs.scrapy.org/en/latest/topics/items.html#dataclass-objects
from dataclasses import dataclass, field


@dataclass
class Table:
    img_path: str
    page_num: int

    def to_airtable_record(self, img_prefix: str, pdf_id: str):
        # https://airtable.com/appdrqXSd2JNXkLp7/api/docs#curl/table:tables:create
        img_url = img_prefix + self.img_path
        return {
            "fields": {
                "Image": [{"url": img_url}],
                "Page": self.page_num,
                "PDF": [pdf_id],
            }
        }


@dataclass
class PDF:
    title: str
    source: str
    file_urls: list[str]
    tables: list[Table] = field(default_factory=list)
