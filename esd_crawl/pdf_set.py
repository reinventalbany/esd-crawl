from esd_crawl.items import PDF


class PdfSet:
    """Collects and combines PDFs"""

    def __init__(self):
        self.pdfs: dict[str, dict] = {}

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

    def get(self, url: str):
        return self.pdfs[url]

    def urls(self):
        return list(self.pdfs.keys())

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
