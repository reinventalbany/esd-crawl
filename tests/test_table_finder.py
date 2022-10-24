from esd_crawl.tables import TableFinder
import os
from scrapy.pipelines.media import MediaPipeline
from unittest.mock import Mock


def test_find_tables():
    finder = TableFinder()
    pdf_path = os.path.join("tests", "NYSTAR-2022-Annual-Report.pdf")
    fake_info = Mock(spec=MediaPipeline.SpiderInfo)

    tables = finder.find_tables(pdf_path, fake_info)
    assert len(tables) == 4

    page_numbers = [table.page_num for table in tables]
    assert page_numbers == [5, 6, 7, 8]
