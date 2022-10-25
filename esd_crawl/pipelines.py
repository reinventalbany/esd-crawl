import os
from esd_crawl.items import PDF
from esd_crawl.tables import TableFinder
from scrapy.pipelines.files import FilesPipeline


class FindTablePipeline(FilesPipeline):
    """For each item, download the PDF, detect the tables within it, and return the item with that extra information."""

    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        self.finder = TableFinder()

    def item_completed(self, results, item: PDF, info):
        for ok, result in results:
            if not ok:
                continue

            pdf_path = os.path.join(self.store.basedir, result["path"])
            tables = self.finder.find_tables(pdf_path, info)
            item.tables.extend(tables)

        return item
