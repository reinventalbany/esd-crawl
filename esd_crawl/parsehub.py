"""This script is meant to mirror the FindTablePipeline, but can be run outside of Scrapy."""

import csv
from esd_crawl.items import PDF, DataClassEncoder, Report
from esd_crawl.tables import TableFinder
import json
from pdfminer.pdfparser import PDFSyntaxError
from scrapy.pipelines.media import MediaPipeline
import sys


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


def process_report(finder: TableFinder, report: Report):
    url = report.report_url

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
    pdfs: list[PDF] = []

    with open(parsehub_output_csv) as file:
        reader = csv.DictReader(file)
        for entry in reader:
            report = Report(**entry)
            pdf = process_report(finder, report)
            if pdf:
                pdfs.append(pdf)

            print(".", end="", flush=True)

    return pdfs


def run():
    pdfs = get_pdfs("parsehub.csv")

    output_file = "reports.json"
    with open(output_file, "w") as file:
        json.dump(pdfs, file, cls=DataClassEncoder, indent=2)

    print(f"Wrote {len(pdfs)} PDF records to {output_file}")


if __name__ == "__main__":
    run()
