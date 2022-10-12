import os
import pdfplumber
from scrapy.pipelines.files import FilesPipeline


def pages_with_tables(path):
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            if len(tables) > 0:
                yield page


class FindTablePipeline(FilesPipeline):
    def item_completed(self, results, item, info):
        for ok, result in results:
            if not ok:
                continue

            path = os.path.join(self.store.basedir, result["path"])
            pages = pages_with_tables(path)

            for page in pages:
                img = page.to_image()
                finder = img.debug_tablefinder()
                # preview
                finder.show()

        return item
