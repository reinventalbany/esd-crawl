from scrapy.spiders import SitemapSpider


class ESDSpider(SitemapSpider):
    name = "esdspider"
    allowed_domains = ["esd.ny.gov"]
    sitemap_urls = ["https://esd.ny.gov/sitemap.xml"]

    # https://docs.scrapy.org/en/latest/topics/settings.html#built-in-settings-reference
    custom_settings = {
        # https://docs.scrapy.org/en/latest/topics/media-pipeline.html#enabling-your-media-pipeline
        "ITEM_PIPELINES": {"esd_crawl.pipelines.FindTablePipeline": 300},
        "FILES_STORE": "downloads",
    }

    def parse(self, response):
        # find links to PDFs
        for link in response.css('a[href$=".pdf"]'):
            title = link.css("::text").get()
            url = link.css("::attr(href)").get()
            absolute_url = response.urljoin(url)

            # https://docs.scrapy.org/en/latest/topics/media-pipeline.html#using-the-files-pipeline
            yield {"title": title, "file_urls": [absolute_url], "source": response.url}

        # for next_page in response.css("a[href]::attr(href)").extract():
        #     yield response.follow(next_page, self.parse)
