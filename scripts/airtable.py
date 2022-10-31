"""This is a script for uploading PDF and Table information to Airtable."""

from esd_crawl.airtable import upsert_pdf, upsert_table
from esd_crawl.items import Table
import json
import os


key = os.environ["AIRTABLE_API_KEY"]
img_prefix = os.environ["IMG_PREFIX"]

with open(os.path.join("results", "pdfs.json")) as f:
    pdfs = json.load(f)

for pdf_url, pdf in pdfs.items():
    pdf_id = upsert_pdf(key, pdf_url, pdf["titles"])

    for table_data in pdf["tables"]:
        table = Table(**table_data)
        table_id = upsert_table(key, table, img_prefix, pdf_id)
        if table_id:
            print(".", end="", flush=True)
