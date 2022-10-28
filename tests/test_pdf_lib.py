from esd_crawl.items import Report
from esd_crawl.pdf_lib import process_report
from esd_crawl.tables import TableFinder
from tests.helpers import mock_pdf_download


def test_process_report_non_pdf():
    finder = TableFinder()
    report = Report(
        report_url="https://something.gov/page",
        report_name="",
        report_source="https://something.gov/",
    )

    pdf = process_report(finder, report)
    assert pdf is None


def test_process_report_pdf(r_mock, pdf_path):
    pdf_url = "https://something.gov/report.pdf"

    mock_pdf_download(r_mock, pdf_url, pdf_path)
    finder = TableFinder()
    report = Report(
        report_url=pdf_url,
        report_name="",
        report_source="https://something.gov/",
    )

    pdf = process_report(finder, report)
    assert pdf is not None
    assert pdf.abs_file_url() == pdf_url


def test_process_report_bad_pdf(r_mock):
    pdf_url = "https://something.gov/report.pdf"

    mock_pdf_download(r_mock, pdf_url, "README.md")
    finder = TableFinder()
    report = Report(
        report_url=pdf_url,
        report_name="",
        report_source="https://something.gov/",
    )

    pdf = process_report(finder, report)
    assert pdf is None
