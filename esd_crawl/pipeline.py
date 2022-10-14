from hashlib import md5
from io import BytesIO
from itemadapter import ItemAdapter
import os
import pdfplumber
from scrapy.pipelines.files import FSFilesStore, FilesPipeline


def pages_with_tables(path):
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            if len(tables) > 0:
                yield page


class FindTablePipeline(FilesPipeline):
    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        self.img_store = FSFilesStore("tables")

    def persist_img(self, img, info, extension="png"):
        # based on
        # https://github.com/scrapy/scrapy/blob/e4f6545fe952f1c1e3324340ade4e19bfb8a197e/scrapy/pipelines/files.py#L500-L503
        buf = BytesIO()
        img.save(buf, extension)
        buf.seek(0)

        # https://stackoverflow.com/a/53732141/358804
        checksum = md5(img.tobytes()).hexdigest()
        path = f"{checksum}.{extension}"

        self.img_store.persist_file(path, buf, info)

        return path

    def save_table_img(self, page, info):
        img = page.to_image()
        finder = img.debug_tablefinder()
        # preview
        # finder.show()

        img = finder.annotated
        return self.persist_img(img, info)

    def item_completed(self, results, item, info):
        adapter = ItemAdapter(item)
        adapter["img_paths"] = []

        for ok, result in results:
            if not ok:
                continue

            pdf_path = os.path.join(self.store.basedir, result["path"])
            pages = pages_with_tables(pdf_path)

            for page in pages:
                img_path = self.save_table_img(page, info)
                # TODO include page number
                adapter["img_paths"].append(img_path)

        return item
