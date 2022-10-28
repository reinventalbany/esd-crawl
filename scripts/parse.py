import argparse
from esd_crawl.items import Report
from esd_crawl.pdf_lib import get_pdf, pdf_has_text
from esd_crawl.tables import pdf_from_url


parser = argparse.ArgumentParser(description="Parse an individual PDF from a URL.")
parser.add_argument("URL", help="URL of the PDF to parse")
args = parser.parse_args()

reader = pdf_from_url(args.URL)
if not pdf_has_text(reader):
    print("No text found; presumably a scanned PDF.")

report = Report(report_url=args.URL, report_name="unknown", report_source="unknown")
pdf = get_pdf(report)
print(pdf)
