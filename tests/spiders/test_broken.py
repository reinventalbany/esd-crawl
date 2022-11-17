from esd_crawl.spiders.broken import process_response
from scrapy.http import Request, HtmlResponse


def test_http_200():
    body = b"""
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
    </body>
    </html>
    """

    response = HtmlResponse(
        url="https://esd.ny.gov",
        status=200,
        headers={"Content-Type": "text/html"},
        body=body,
        request=Request(url="https://esd.ny.gov"),
    )

    items = process_response(response)
    assert list(items) == []
