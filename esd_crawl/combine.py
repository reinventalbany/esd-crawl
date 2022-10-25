"""This is a script for combining the PDF information from Scrapy and Parsehub."""


from esd_crawl.items import PDF
import json


class PdfSet:
    """Collects and combines PDFs"""

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

    def len(self):
        return len(self.pdfs.keys())

    def num_pdfs_with_tables(self):
        pdfs = self.pdfs.values()
        return sum(1 for pdf in pdfs if len(pdf["tables"]) > 0)

    def num_tables(self):
        pdfs = self.pdfs.values()
        return sum(len(pdf["tables"]) for pdf in pdfs)


class SetEncoder(json.JSONEncoder):
    """JSON encoder that supports set() objects.

    https://bobbyhadz.com/blog/python-typeerror-object-of-type-set-is-not-json-serializable
    """

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def format_num(num: int):
    return "{:,}".format(num)


def print_stats(pdfs: PdfSet):
    num_pdfs = pdfs.len()
    print(f"Number of PDFs: {format_num(num_pdfs)}")

    num_with_tables = pdfs.num_pdfs_with_tables()
    print(f"Number of PDFs with tables: {format_num(num_with_tables)}")

    pct_with_tables = num_with_tables / num_pdfs * 100
    print(f"PDFs with tables: {pct_with_tables:.1f}%")

    num_tables = pdfs.num_tables()
    print(f"Number of tables: {format_num(num_tables)}")

    tables_per_pdf = num_tables / num_pdfs
    print(f"Average tables per PDF: {tables_per_pdf:.1f}")


def run():
    pdfs = PdfSet()

    for data_path in ["scrapy.json", "reports.json"]:
        with open(data_path) as file:
            data = json.load(file)
            for entry in data:
                pdf = PDF(**entry)
                pdfs.add(pdf)

    output_file = "pdfs.json"
    with open(output_file, "w") as file:
        json.dump(pdfs.to_dict(), file, cls=SetEncoder)

    print(f"Wrote PDF records to {output_file}.")
    print_stats(pdfs)


if __name__ == "__main__":
    run()
