# https://docs.scrapy.org/en/latest/topics/items.html#dataclass-objects
from dataclasses import dataclass, field


@dataclass
class Table:
    img_path: str
    page_num: int

    def to_dict(self):
        return {
            "img_path": self.img_path,
            "page_num": self.page_num,
        }

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

    def to_dict(self):
        return {
            "title": self.title,
            "source": self.source,
            "file_urls": self.file_urls,
            "tables": [table.to_dict() for table in self.tables],
        }
