"""This script is meant to mirror the FindTablePipeline, but can be run outside of Scrapy."""

import csv
from esd_crawl.items import PDF, DataClassEncoder
from esd_crawl.tables import TableFinder
import json
from pdfminer.pdfparser import PDFSyntaxError
from scrapy.pipelines.media import MediaPipeline
import sys


def get_pdf(finder: TableFinder, entry: dict):
    url = entry["report_url"]

    info = MediaPipeline.SpiderInfo(None)
    tables = finder.find_tables_from_url(url, info)

    return PDF(
        title=entry["report_name"],
        source=entry["report_source"],
        file_urls=[url],
        tables=tables,
    )


def run():
    finder = TableFinder()
    pdfs = []

    with open("parsehub.csv") as file:
        reader = csv.DictReader(file)
        for entry in reader:
            url = entry["report_url"]

            # The report will contain links to both PDFs and other pages. The latter will be covered by the sitemap crawl, so we can ignore them here.
            if url.endswith(".pdf"):
                try:
                    pdf = get_pdf(finder, entry)
                except PDFSyntaxError:
                    print("\nPDF could not be processed:", url, file=sys.stderr)
                else:
                    pdfs.append(pdf)

            print(".", end="", flush=True)

    with open("reports.json", "w") as file:
        json.dump(pdfs, file, cls=DataClassEncoder)


if __name__ == "__main__":
    run()
