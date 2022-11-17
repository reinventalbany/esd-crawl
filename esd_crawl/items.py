# https://docs.scrapy.org/en/latest/topics/items.html#dataclass-objects
from dataclasses import asdict, dataclass, field, is_dataclass
import json
from urllib.parse import urljoin


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

    ORIGIN = "https://esd.ny.gov"

    def abs_file_url(self):
        return urljoin(self.ORIGIN, self.file_urls[0])


@dataclass
class Report:
    """Individual record output by ParseHub"""

    report_url: str
    report_name: str
    report_source: str


@dataclass
class BrokenLink:
    url: str
    source: str
    reason: str


class DataClassEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        return json.JSONEncoder.default(self, obj)
