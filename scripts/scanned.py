"""This script counts how many of the downloaded files are scanned PDFs."""

from esd_crawl.pdf_lib import pdf_has_text
from glob import glob

num_files = 0
num_scanned = 0

for filename in glob("downloads/full/*.pdf"):
    num_files += 1
    if not pdf_has_text(filename):
        num_scanned += 1

    print(".", end="", flush=True)

print(
    f"\n{num_scanned} of {num_files} PDFs ({round(num_scanned / num_files)}) appear to be scanned."
)
