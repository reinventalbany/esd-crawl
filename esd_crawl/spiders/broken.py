from esd_crawl.items import BrokenLink
from urllib.parse import urlparse
from scrapy.http import Response, HtmlResponse
from scrapy.spiders import SitemapSpider

DOMAIN = "esd.ny.gov"
HTTP_ERROR_CODE_RANGE = range(400, 500)


def is_pdf_url(url: str):
    return urlparse(url).path.endswith(".pdf")


def is_pdf(response: Response):
    return response.headers.get("Content-Type") == b"application/pdf" or is_pdf_url(
        response.url
    )


def referer(response: Response):
    ref: bytes | None = response.request.headers.get("referer")
    return ref.decode("utf-8") if ref else None


def is_homepage(url: str):
    url_obj = urlparse(url)
    return bool(url_obj.hostname == DOMAIN and url_obj.path in ["", "/"])


def process_response(response: Response):
    # check for PDF URLs that redirect to the homepage, or to the page that linked to them
    redirects: list[str] | None = response.request.meta.get("redirect_urls")
    if redirects:
        initial_url = redirects[0]
        source = referer(response)
        # TODO normalize URL for latter
        if (
            is_pdf_url(initial_url) and is_homepage(response.url)
        ) or response.url == source:
            yield BrokenLink(url=initial_url, source=source)

    # handle PDF 40x errors
    if response.status in HTTP_ERROR_CODE_RANGE:
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
    # not all of these are valid status codes, but that's ok
    handle_httpstatus_list = list(HTTP_ERROR_CODE_RANGE)

    # keep the referer, even for redirects through HTTP
    # https://docs.scrapy.org/en/latest/topics/spider-middleware.html#acceptable-values-for-referrer-policy
    custom_settings = {"REFERRER_POLICY": "unsafe-url"}

    def parse(self, response: Response):
        for item in process_response(response):
            yield item
