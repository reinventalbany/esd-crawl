from scrapy.spiders import SitemapSpider


class ESDSpider(SitemapSpider):
    name = "esdspider"
    allowed_domains = ["esd.ny.gov"]
    sitemap_urls = ["https://esd.ny.gov/sitemap.xml"]

    def parse(self, response):
        # print(response)

        # find links to PDFs
        for link in response.css('a[href$=".pdf"]'):
            title = link.css("::text").get().strip()
            url = link.css("::attr(href)").get()

            yield {
                "title": title,
                "url": url,
            }

        # for next_page in response.css("a[href]::attr(href)").extract():
        #     yield response.follow(next_page, self.parse)
