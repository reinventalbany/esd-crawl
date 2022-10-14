from esd_crawl.spiders.utils import find_pdf_links
from scrapy.spiders import SitemapSpider


class ESDSpider(SitemapSpider):
    name = "esdspider"
    allowed_domains = ["esd.ny.gov"]
    sitemap_urls = ["https://esd.ny.gov/sitemap.xml"]

    def parse(self, response):
        yield from find_pdf_links(response)

        # for next_page in response.css("a[href]::attr(href)").extract():
        #     yield response.follow(next_page, self.parse)
