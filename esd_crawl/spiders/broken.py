from esd_crawl.items import BrokenLink
from urllib.parse import urlparse

# from scrapy.spiders import SitemapSpider
from scrapy.spiders import Spider


def is_pdf_url(url: str):
    return urlparse(url).path.endswith(".pdf")


def is_pdf(response):
    return response.headers["Content-Type"] == b"application/pdf" or is_pdf_url(
        response.url
    )


# class BrokenSpider(SitemapSpider):
#     name = "brokenspider"
#     allowed_domains = ["esd.ny.gov"]
#     sitemap_urls = ["https://esd.ny.gov/sitemap.xml"]
class BrokenSpider(Spider):
    name = "broken"
    start_urls = [
        "https://esd.ny.gov",
        "https://esd.ny.gov/12312015-excelsior-jobs-program-quarterly-report",
        "https://esd.ny.gov/broken.html",
        "https://esd.ny.gov/broken.pdf",
        "https://esd.ny.gov/Reports/2015_2016/03312016_EXCELSIORJOBSPROGRAMQUARTERLYREPORT.pdf",
        "https://esd.ny.gov/Reports/2015_2016/EXCELSIORJOBSPROGRAMQUARTERLYREPORT_12312015.pdf",
        "https://esd.ny.gov/Reports/2015_2016/RetentionChartA_BusinessesAdmittedToProgram_03312016.pdf",
        "https://esd.ny.gov/Reports/2015_2016/RetentionChartB_CreditsIssued_03312016.pdf",
    ]
    # https://docs.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.httperror
    handle_httpstatus_list = [404]

    def parse(self, response):
        print("RESPONSE:", response)

        # broken PDF URLs redirect to the homepage
        if response.url == "https://esd.ny.gov":
            redirects = response.request.meta.get("redirect_urls")
            if redirects:
                initial_url = redirects[0]
                if is_pdf_url(initial_url):
                    yield BrokenLink(url=initial_url)

        if response.status == 404:
            if is_pdf(response):
                yield BrokenLink(url=response.url)
            return

        # find links to PDFs
        for link in response.css('a[href$=".pdf"]'):
            url = link.css("::attr(href)").get()
            yield response.follow(url)

        # for next_page in response.css("a[href]::attr(href)").extract():
        #     yield response.follow(next_page, self.parse)
