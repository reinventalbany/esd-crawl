from esd_crawl.spiders.broken import process_response
import pytest
from scrapy.http import Request, HtmlResponse, Response


def html(body=""):
    html_str = f"""
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>{body}</body>
    </html>
    """

    return bytes(html_str, "utf-8")


def test_http_no_links():
    url = "https://esd.ny.gov"

    request = Request(url=url)
    response = HtmlResponse(
        url=url,
        status=200,
        headers={"Content-Type": "text/html"},
        body=html(),
        request=request,
    )

    items = list(process_response(response))
    assert items == []


@pytest.mark.parametrize("mime_type", ["text/html", "text/html; charset=utf-8"])
def test_http_pdf_link(mime_type):
    end_url = "https://esd.ny.gov"
    pdf_url = "https://esd.ny.gov/Reports/2015_2016/03312016_EXCELSIORJOBSPROGRAMQUARTERLYREPORT.pdf"
    body = html(f"""<a href="{pdf_url}">PDF</a>""")

    request = Request(url=end_url)
    response = HtmlResponse(
        url=end_url,
        status=200,
        headers={"Content-Type": mime_type},
        body=body,
        request=request,
    )

    items = list(process_response(response))
    assert len(items) == 1
    assert items[0].url == pdf_url


def test_pdf_404():
    url = "https://esd.ny.gov/broken.pdf"

    request = Request(url=url)
    response = Response(
        url=url,
        status=404,
        headers={"Content-Type": "application/html"},
        body=b"not found",
        request=request,
    )

    items = list(process_response(response))
    assert len(items) == 1
    assert items[0].url == url


def test_pdf_redirect_to_homepage():
    # arbitrary file
    file = open("tests/NYSTAR-2022-Annual-Report.pdf", "rb").read()
    pdf_url = "https://esd.ny.gov/some.pdf"
    end_url = "https://esd.ny.gov"

    request = Request(
        url=end_url,
        meta={"redirect_urls": [pdf_url]},
    )
    response = Response(
        url=end_url,
        status=200,
        headers={"Content-Type": "application/pdf"},
        body=file,
        request=request,
    )

    items = list(process_response(response))
    assert len(items) == 1
    assert items[0].url == pdf_url
