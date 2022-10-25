from esd_crawl.items import PDF
import json


class PdfSet:
    def __init__(self):
        self.pdfs = {}

    def add(self, pdf: PDF):
        if len(pdf.file_urls) != 1:
            raise RuntimeError("PDF should have exactly one file URL")

        url = pdf.abs_file_url()
        if url not in self.pdfs:
            # first time being seen
            self.pdfs[url] = {
                "titles": set(),
                "sources": set(),
                "tables": [],
            }

        info = self.pdfs[url]
        info["titles"].add(pdf.title.strip())
        info["sources"].add(pdf.source)
        # assuming the same tables will be found each time
        info["tables"] = pdf.tables

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

    for data_path in ["scrapy.json", "reports.json"]:
        with open(data_path) as file:
            data = json.load(file)
            for entry in data:
                pdf = PDF(**entry)
                pdfs.add(pdf)

    with open("pdfs.json", "w") as file:
        json.dump(pdfs.to_dict(), file, cls=SetEncoder)


if __name__ == "__main__":
    run()
