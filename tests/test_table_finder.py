from esd_crawl.items import Table
from esd_crawl.tables import TableFinder
import pytest
from scrapy.pipelines.media import MediaPipeline
from tests.helpers import mock_pdf_download
from unittest.mock import Mock


@pytest.fixture
def fake_info():
    return Mock(spec=MediaPipeline.SpiderInfo)


def assert_tables(tables: list[Table]):
    assert len(tables) == 4

    page_numbers = [table.page_num for table in tables]
    assert page_numbers == [5, 6, 7, 8]


def test_find_tables(fake_info, pdf_path):
    finder = TableFinder()
    tables = finder.find_tables(pdf_path, fake_info)
    assert_tables(tables)


def test_find_tables_from_url(r_mock, fake_info, pdf_path):
    url = "https://foo.com/bar.pdf"

    mock_pdf_download(r_mock, url, pdf_path)

    finder = TableFinder()
    tables = finder.find_tables_from_url(url, fake_info)
    assert_tables(tables)
