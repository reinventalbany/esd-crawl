import base64
from io import BytesIO
import os
from PIL import Image
from scrapy import Spider
from scrapy_splash import SplashRequest

PREVIEW = "PREVIEW" in os.environ


class ReportsSpider(Spider):
    name = "reportsspider"
    allowed_domains = ["esd.ny.gov"]
    start_urls = ["https://esd.ny.gov/esd-media-center?tid[]=516"]
    # TODO limit to Reports / Media Center

    # https://github.com/scrapy-plugins/scrapy-splash#configuration
    custom_settings = {
        "SPLASH_URL": "http://localhost:8050",
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_splash.SplashCookiesMiddleware": 723,
            "scrapy_splash.SplashMiddleware": 725,
            "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware": 810,
        },
        "SPIDER_MIDDLEWARES": {
            "scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
        },
        "DUPEFILTER_CLASS": "scrapy_splash.SplashAwareDupeFilter",
    }

    def start_requests(self):
        for url in self.start_urls:
            splash_args = {"wait": 1.0}
            if PREVIEW:
                splash_args.update(
                    {
                        "html": 1,
                        "png": 1,
                        "width": 600,
                        "render_all": 1,
                    }
                )

            yield SplashRequest(
                url, self.parse, endpoint="render.json", args=splash_args
            )

    def parse(self, response):
        # find links to PDFs
        for link in response.css('a[href$=".pdf"]'):
            title = link.css("::text").get()
            url = link.css("::attr(href)").get()
            absolute_url = response.urljoin(url)
            print("LINK:", title, absolute_url)

        if PREVIEW:
            png_bytes = base64.b64decode(response.data["png"])
            im = Image.open(BytesIO(png_bytes))
            im.show()
