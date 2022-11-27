from esd_crawl.items import BrokenLink
from urllib.parse import urlparse
from scrapy.http import Response, HtmlResponse
from scrapy.spiders import SitemapSpider

DOMAIN = "esd.ny.gov"
HTTP_ERROR_CODE_RANGE = range(400, 500)


def referer(response: Response):
    ref: bytes | None = response.request.headers.get("referer")
    return ref.decode("utf-8") if ref else None


def is_catch_all_page(url: str):
    """esd.ny.gov seems to have certain pages that many PDFs redirect to, and thus they should be considered broken links."""

    url_obj = urlparse(url)
    return url_obj.hostname == DOMAIN and url_obj.path in ["", "/", "/corporate-info"]


def process(response: Response):
    title = response.request.meta.get("title")
    source = referer(response)

    # handle 40x errors
    if response.status in HTTP_ERROR_CODE_RANGE:
        yield BrokenLink(url=response.url, source=source, title=title, reason="404")
    else:
        # check for URLs that redirect to the homepage, or to the page that linked to them
        redirects: list[str] = response.request.meta.get("redirect_urls", [])
        if redirects:
            initial_url = redirects[0]
            if is_catch_all_page(response.url):
                yield BrokenLink(
                    url=initial_url, source=source, title=title, reason="catch-all"
                )
            # TODO normalize URL
            elif response.url == source:
                yield BrokenLink(
                    url=initial_url,
                    source=source,
                    title=title,
                    reason="circular-redirect",
                )

        if isinstance(response, HtmlResponse):
            # find links
            for link in response.css("a[href]"):
                title = link.css("::text").get()
                url = link.css("::attr(href)").get()
                absolute_url = response.urljoin(url)

                if not absolute_url.startswith("http"):
                    continue

                # no need to download a PDF
                method = "HEAD" if absolute_url.lower().endswith(".pdf") else "GET"

                yield response.follow(
                    absolute_url,
                    method=method,
                    # allow for redirects to the same page
                    # https://docs.scrapy.org/en/latest/topics/settings.html#dupefilter-class
                    dont_filter=True,
                    meta={"title": title},
                )


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
        yield from process(response)
