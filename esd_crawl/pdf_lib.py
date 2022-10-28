from esd_crawl.items import PDF, Report
from esd_crawl.tables import TableFinder
from pdfminer.pdfparser import PDFSyntaxError
from scrapy.pipelines.media import MediaPipeline
import sys


def get_pdf(report: Report, finder: TableFinder = None):
    if finder is None:
        finder = TableFinder()

    url = report.report_url
    info = MediaPipeline.SpiderInfo(None)
    tables = finder.find_tables_from_url(url, info)

    return PDF(
        title=report.report_name,
        source=report.report_source,
        file_urls=[url],
        tables=tables,
    )


def process_report(finder: TableFinder, report: Report):
    url = report.report_url

    # The report will contain links to both PDFs and other pages. The latter will be covered by the sitemap crawl, so we can ignore them here.
    if url.endswith(".pdf"):
        try:
            return get_pdf(report, finder)
        except PDFSyntaxError:
            print("\nPDF could not be processed:", url, file=sys.stderr)
            return None

    return None
