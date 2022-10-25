import csv
from esd_crawl.items import PDF, DataClassEncoder
from esd_crawl.tables import TableFinder
import json


finder = TableFinder("parsehub_tables")
pdfs = []

with open("parsehub.csv") as file:
    reader = csv.DictReader(file)
    for entry in reader:
        url = entry["report_url"]

        # The report will contain links to both PDFs and other pages. The latter will be covered by the sitemap crawl, so we can ignore them here.
        if url.endswith(".pdf"):
            fake_info = {}
            tables = finder.find_tables_from_url(url, fake_info)

            pdf = PDF(
                title=entry["report_name"],
                source=entry["report_source"],
                file_urls=[url],
                tables=tables,
            )
            pdfs.append(pdf)

with open("reports.json", "w") as file:
    json.dump(pdfs, file, cls=DataClassEncoder)
