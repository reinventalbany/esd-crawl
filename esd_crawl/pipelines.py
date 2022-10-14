from hashlib import md5
from io import BytesIO
from itemadapter import ItemAdapter
import os
from esd_crawl.tables import TableFinder
from scrapy.pipelines.files import FilesPipeline


class FindTablePipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        self.finder = TableFinder()

    def item_completed(self, results, item, info):
        adapter = ItemAdapter(item)
        adapter["img_paths"] = []

        for ok, result in results:
            if not ok:
                continue

            pdf_path = os.path.join(self.store.basedir, result["path"])
            # info is pipeline.SpiderInfo
            img_paths = self.finder.find_tables(pdf_path, info)
            # TODO include page number
            adapter["img_paths"].extend(img_paths)

        return item
