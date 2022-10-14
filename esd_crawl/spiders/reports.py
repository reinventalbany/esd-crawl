import asyncio
from esd_crawl.spiders.utils import find_pdf_links
from io import BytesIO
import os
from PIL import Image
from scrapy import Request, Spider
from scrapy_playwright.page import PageMethod

PREVIEW = "PREVIEW" in os.environ


async def close_page(meta):
    page = meta["playwright_page"]
    await page.close()


async def display_screenshot(page):
    screenshot = await page.screenshot(full_page=True)
    im = Image.open(BytesIO(screenshot))
    im.show()


class ReportsSpider(Spider):
    name = "reportsspider"
    allowed_domains = ["esd.ny.gov"]
    start_urls = ["https://esd.ny.gov/esd-media-center?tid[]=516"]
    # TODO limit to Reports / Media Center

    NEXT_SELECTOR = "#page-next"

    custom_settings = {
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "DOWNLOAD_HANDLERS": {
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url=url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", ".result-card"),
                    ],
                },
                errback=self.errback,
            )

    async def parse(self, response):
        # await close_page(response.meta)

        # the Reports listing is paginated with AJAX, so loop through pages by clicking through them in a browser rather than sending separate Requests
        while True:
            for item in find_pdf_links(response):
                print(item)
                # TODO yield

            if PREVIEW:
                page = response.meta["playwright_page"]
                await display_screenshot(page)

            next_page = response.css(self.NEXT_SELECTOR).get()
            if next_page is None:
                # last page
                break

            await page.click(selector=self.NEXT_SELECTOR)
            await asyncio.sleep(1)

    async def errback(self, failure):
        await close_page(failure.request.meta)
