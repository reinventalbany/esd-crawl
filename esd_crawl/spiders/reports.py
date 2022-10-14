import asyncio
from esd_crawl.spiders.utils import display_screenshot, find_pdf_links
import os
from scrapy import Request, Spider
from scrapy_playwright.page import PageMethod

PREVIEW = "PREVIEW" in os.environ


class ReportsSpider(Spider):
    name = "reportsspider"
    allowed_domains = ["esd.ny.gov"]
    start_urls = ["https://esd.ny.gov/esd-media-center?tid[]=516"]

    NEXT_SELECTOR = "#page-next"
    DELAY_SECONDS = 0.5

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

    async def go_to_next_page(self, page):
        await page.click(selector=self.NEXT_SELECTOR)
        await asyncio.sleep(self.DELAY_SECONDS)

    async def parse(self, response):
        # since coroutines can't yield, need to return all the items combined as one
        pdfs = []

        # the Reports listing is paginated with AJAX, so loop through pages by clicking through them in a browser rather than sending separate Requests
        while True:
            page = response.meta["playwright_page"]
            self.logger.debug(f"URL: {page.url}")

            for item in find_pdf_links(response):
                pdfs.append(item)

            if PREVIEW:
                await display_screenshot(page)

            next_page = response.css(self.NEXT_SELECTOR).get()
            if next_page is None:
                # last page
                await page.close()
                return pdfs

            await self.go_to_next_page(page)

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
