"""This script is meant for parsing an individual PDF from a URL."""

import argparse
from esd_crawl.items import PDF, Report
from esd_crawl.tables import TableFinder
from scrapy.pipelines.media import MediaPipeline


def get_pdf(finder: TableFinder, report: Report):
    url = report.report_url

    info = MediaPipeline.SpiderInfo(None)
    tables = finder.find_tables_from_url(url, info)

    return PDF(
        title=report.report_name,
        source=report.report_source,
        file_urls=[url],
        tables=tables,
    )


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("URL", help="URL of the PDF to parse")
    args = parser.parse_args()

    finder = TableFinder()
    report = Report(report_url=args.URL, report_name="unknown", report_source="unknown")
    pdf = get_pdf(finder, report)
    print(pdf)


if __name__ == "__main__":
    run()
