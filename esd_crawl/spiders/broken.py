from esd_crawl.items import BrokenLink
from urllib.parse import urlparse
from scrapy.http import Response, HtmlResponse
from scrapy.spiders import SitemapSpider
from scrapy.utils.request import referer_str

DOMAIN = "esd.ny.gov"
HTTP_ERROR_CODE_RANGE = range(400, 500)


def is_catch_all_page(url: str):
    """esd.ny.gov seems to have certain pages that many PDFs redirect to, and thus they should be considered broken links."""

    url_obj = urlparse(url)
    return url_obj.hostname == DOMAIN and url_obj.path in ["", "/", "/corporate-info"]


def process(response: Response):
    req = response.request
    title = req.meta.get("title")
    source = referer_str(req)

    # handle 40x errors
    if response.status in HTTP_ERROR_CODE_RANGE:
        yield BrokenLink(url=response.url, source=source, title=title, reason="404")
    else:
        # check for URLs that redirect to the homepage, or to the page that linked to them
        redirects: list[str] = req.meta.get("redirect_urls", [])
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

                scheme = urlparse(absolute_url).scheme
                if scheme not in ["http", "https"]:
                    # mailto, etc.
                    continue

                # no need to download a PDF
                method = "HEAD" if absolute_url.lower().endswith(".pdf") else "GET"

                yield response.follow(
                    absolute_url,
                    method=method,
                    # allow for redirects to the same page
                    # https://docs.scrapy.org/en/latest/topics/settings.html#dupefilter-class
                    dont_filter=is_catch_all_page(absolute_url),
                    meta={"title": title},
                )


class BrokenSpider(SitemapSpider):
    name = "broken"
    allowed_domains = [DOMAIN]
    sitemap_urls = [f"https://{DOMAIN}/sitemap.xml"]

    # https://docs.scrapy.org/en/latest/topics/spider-middleware.html#module-scrapy.spidermiddlewares.httperror
    # not all of these are valid status codes, but that's ok
    handle_httpstatus_list = list(HTTP_ERROR_CODE_RANGE)

    custom_settings = {
        "HTTPCACHE_ENABLED": True,
        "HTTPCACHE_EXPIRATION_SECS": 60 * 60 * 24 * 7,  # 1 week
        "HTTPCACHE_POLICY": "scrapy.extensions.httpcache.RFC2616Policy",
        # keep the referer, even for redirects through HTTP
        # https://docs.scrapy.org/en/latest/topics/spider-middleware.html#acceptable-values-for-referrer-policy
        "REFERRER_POLICY": "unsafe-url",
    }

    def parse(self, response: Response):
        yield from process(response)
