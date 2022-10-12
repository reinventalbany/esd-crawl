from scrapy.spiders import SitemapSpider


class ESDSpider(SitemapSpider):
    name = "esdspider"
    allowed_domains = ["esd.ny.gov"]
    sitemap_urls = ["https://esd.ny.gov/sitemap.xml"]

    # https://docs.scrapy.org/en/latest/topics/settings.html#built-in-settings-reference
    custom_settings = {
        # throttle the crawl to reduce load on the site
        "DOWNLOAD_DELAY": 0.25,
        # https://docs.scrapy.org/en/latest/topics/media-pipeline.html#enabling-your-media-pipeline
        "ITEM_PIPELINES": {"scrapy.pipelines.files.FilesPipeline": 1},
        "FILES_STORE": "downloads",
    }

    def parse(self, response):
        # find links to PDFs
        for link in response.css('a[href$=".pdf"]'):
            title = link.css("::text").get()
            url = link.css("::attr(href)").get()

            # https://docs.scrapy.org/en/latest/topics/media-pipeline.html#using-the-files-pipeline
            yield {"title": title, "file_urls": [url], "source": response.url}

        # for next_page in response.css("a[href]::attr(href)").extract():
        #     yield response.follow(next_page, self.parse)
