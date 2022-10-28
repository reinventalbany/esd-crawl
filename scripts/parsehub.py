"""This script is meant to mirror the FindTablePipeline, but can be run outside of Scrapy."""

import csv
from esd_crawl.items import PDF, DataClassEncoder, Report
from esd_crawl.pdf_lib import process_report
from esd_crawl.tables import TableFinder
import json
import sys


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
