from scrapy.spiders import SitemapSpider


class ESDSpider(SitemapSpider):
    name = "esdspider"
    allowed_domains = ["esd.ny.gov"]
    sitemap_urls = ["https://esd.ny.gov/sitemap.xml"]

    # https://docs.scrapy.org/en/latest/topics/settings.html#built-in-settings-reference
    custom_settings = {
        # throttle the crawl to reduce load on the site
        "DOWNLOAD_DELAY": 0.25
    }

    def parse(self, response):
        # find links to PDFs
        for link in response.css('a[href$=".pdf"]'):
            title = link.css("::text").get()
            url = link.css("::attr(href)").get()

            yield {"title": title, "url": url, "source": response.url}

        # for next_page in response.css("a[href]::attr(href)").extract():
        #     yield response.follow(next_page, self.parse)
