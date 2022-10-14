from io import BytesIO
import os
from PIL import Image
from scrapy import Request, Spider

PREVIEW = "PREVIEW" in os.environ


async def display_screenshot(page):
    screenshot = await page.screenshot(full_page=True)
    im = Image.open(BytesIO(screenshot))
    im.show()


class ReportsSpider(Spider):
    name = "reportsspider"
    allowed_domains = ["esd.ny.gov"]
    start_urls = ["https://esd.ny.gov/esd-media-center?tid[]=516"]
    # TODO limit to Reports / Media Center

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
                    "playwright_page_methods": [],
                },
            )

    async def parse(self, response):
        # find links to PDFs
        for link in response.css('a[href$=".pdf"]'):
            title = link.css("::text").get()
            url = link.css("::attr(href)").get()
            absolute_url = response.urljoin(url)
            print("LINK:", title, absolute_url)

        if PREVIEW:
            page = response.meta["playwright_page"]
            await display_screenshot(page)
