"""This script counts how many of the downloaded files are scanned PDFs."""

from esd_crawl.pdf_lib import pdf_has_text
from glob import glob
import sys

num_files = 0
num_scanned = 0

for filename in glob("downloads/full/*.pdf"):
    num_files += 1
    try:
        has_text = pdf_has_text(filename)
    except Exception as e:
        print(f"\nError parsing file {filename}:", file=sys.stderr)
        print(e, file=sys.stderr)
        continue

    if not has_text:
        num_scanned += 1

    print(".", end="", flush=True)

pct = round(num_scanned / num_files)
print(f"\n{num_scanned} of {num_files} PDFs ({pct}) appear to be scanned.")
