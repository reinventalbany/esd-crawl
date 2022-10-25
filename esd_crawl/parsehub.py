"""This script is meant to mirror the FindTablePipeline, but can be run outside of Scrapy."""

import csv
from esd_crawl.items import PDF, DataClassEncoder
from esd_crawl.tables import TableFinder
import json
from pdfminer.pdfparser import PDFSyntaxError
from scrapy.pipelines.media import MediaPipeline
import sys


def get_pdf(finder: TableFinder, report: dict):
    url = report["report_url"]

    info = MediaPipeline.SpiderInfo(None)
    tables = finder.find_tables_from_url(url, info)

    return PDF(
        title=report["report_name"],
        source=report["report_source"],
        file_urls=[url],
        tables=tables,
    )


def process_report(finder: TableFinder, report: dict):
    url = report["report_url"]

    # The report will contain links to both PDFs and other pages. The latter will be covered by the sitemap crawl, so we can ignore them here.
    if url.endswith(".pdf"):
        try:
            return get_pdf(finder, report)
        except PDFSyntaxError:
            print("\nPDF could not be processed:", url, file=sys.stderr)
            return None

    return None


def get_pdfs(parsehub_output_csv: str):
    finder = TableFinder()
    pdfs = []

    with open(parsehub_output_csv) as file:
        reader = csv.DictReader(file)
        for report in reader:
            pdf = process_report(finder, report)
            if pdf:
                pdfs.append(pdf)

            print(".", end="", flush=True)

    return pdfs


def run():
    pdfs = get_pdfs("parsehub.csv")
    with open("reports.json", "w") as file:
        json.dump(pdfs, file, cls=DataClassEncoder)


if __name__ == "__main__":
    run()
