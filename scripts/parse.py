import argparse
from esd_crawl.items import Report
from esd_crawl.pdf_lib import get_pdf, pdf_has_text


parser = argparse.ArgumentParser(description="Parse an individual PDF from a URL.")
parser.add_argument("URL", help="URL of the PDF to parse")
args = parser.parse_args()

if not pdf_has_text(args.URL):
    print("No text found; presumably a scanned PDF.")

report = Report(report_url=args.URL, report_name="unknown", report_source="unknown")
pdf = get_pdf(report)
print(pdf)
