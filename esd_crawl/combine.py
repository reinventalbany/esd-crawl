import csv
from esd_crawl.items import PDF
import json

ORIGIN = "https://esd.ny.gov"


class PdfSet:
    def __init__(self):
        self.pdfs = {}

    def add(self, pdf: PDF):
        if len(pdf.file_urls) > 1:
            raise RuntimeError("PDF has more than one file URL")

        url = pdf.file_urls[0]

        if url.startswith("/"):
            # use absolute URLs
            url = ORIGIN + url

        if url not in self.pdfs:
            # first time being seen
            self.pdfs[url] = {
                "titles": set(),
                "sources": set(),
                "img_paths": set(),
            }

        info = self.pdfs[url]
        info["titles"].add(pdf.title.strip())
        info["sources"].add(pdf.source)
        info["img_paths"].update(pdf.img_paths)

    def to_dict(self):
        return self.pdfs


# https://bobbyhadz.com/blog/python-typeerror-object-of-type-set-is-not-json-serializable
class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def run():
    pdfs = PdfSet()

    with open("scrapy.json") as file:
        data = json.load(file)
        for entry in data:
            pdf = PDF(**entry)
            pdfs.add(pdf)

    with open("parsehub.csv") as file:
        reader = csv.DictReader(file)
        for entry in reader:
            url = entry["report_url"]

            # The report will contain links to both PDFs and other pages. The latter will be covered by the sitemap crawl, so we can ignore them here.
            if url.endswith(".pdf"):
                pdf = PDF(
                    title=entry["report_name"],
                    source=entry["report_source"],
                    file_urls=[url],
                    img_paths=[],
                )
                pdfs.add(pdf)

    with open("pdfs.json", "w") as file:
        json.dump(pdfs.to_dict(), file, cls=SetEncoder)


if __name__ == "__main__":
    run()
