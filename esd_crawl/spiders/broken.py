from esd_crawl.items import BrokenLink
from urllib.parse import urlparse
from scrapy.http import Response, HtmlResponse
from scrapy.spiders import SitemapSpider

DOMAIN = "esd.ny.gov"


def is_pdf_url(url: str):
    return urlparse(url).path.endswith(".pdf")


def is_pdf(response: Response):
    return response.headers["Content-Type"] == b"application/pdf" or is_pdf_url(
        response.url
    )


def referer(response: Response) -> str:
    return response.request.headers.get("referer").decode("utf-8")


def process_response(response: Response):
    # broken PDF URLs redirect to the homepage
    url = urlparse(response.url)
    if url.hostname == DOMAIN and url.path in ["", "/"]:
        redirects = response.request.meta.get("redirect_urls")
        if redirects:
            initial_url = redirects[0]
            if is_pdf_url(initial_url):
                source = referer(response)
                yield BrokenLink(url=initial_url, source=source)

    if response.status == 404:
        if is_pdf(response):
            source = referer(response)
            yield BrokenLink(url=response.url, source=source)
        return

    if isinstance(response, HtmlResponse):
        # find links to PDFs
        for link in response.css('a[href$=".pdf"]'):
            url = link.css("::attr(href)").get()
            # no need to download the PDF
            yield response.follow(url, method="HEAD")

        # for next_page in response.css("a[href]::attr(href)").extract():
        #     yield response.follow(next_page, self.parse)


class BrokenSpider(SitemapSpider):
    name = "broken"
    allowed_domains = [DOMAIN]
    sitemap_urls = [f"https://{DOMAIN}/sitemap.xml"]
    # https://docs.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.httperror
    handle_httpstatus_list = [404]

    def parse(self, response: Response):
        for item in process_response(response):
            yield item
