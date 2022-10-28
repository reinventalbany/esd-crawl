"""This is a script for combining the PDF information from Scrapy and Parsehub."""


from esd_crawl.formatting import format_num, format_pct
from esd_crawl.items import PDF
from esd_crawl.pdf_set import PdfSet
import json


class SetEncoder(json.JSONEncoder):
    """JSON encoder that supports set() objects.

    https://bobbyhadz.com/blog/python-typeerror-object-of-type-set-is-not-json-serializable
    """

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def print_stats(pdfs: PdfSet):
    num_pdfs = pdfs.len()
    print(f"Number of PDFs: {format_num(num_pdfs)}")

    num_with_tables = pdfs.num_pdfs_with_tables()
    pct_with_tables = format_pct(num_with_tables, num_pdfs)
    print(
        f"Number of PDFs with tables: {format_num(num_with_tables)} ({pct_with_tables})"
    )

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
        json.dump(pdfs.to_dict(), file, cls=SetEncoder, indent=2)

    print(f"Wrote PDF records to {output_file}.")
    print_stats(pdfs)


if __name__ == "__main__":
    run()
