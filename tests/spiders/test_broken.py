from esd_crawl.spiders.broken import process
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

    items = list(process(response))
    assert items == []


def test_http_mailto_link():
    page_url = "https://esd.ny.gov"
    body = html(f"""<a href="mailto:some@email.com">Email</a>""")

    request = Request(url=page_url)
    response = HtmlResponse(
        url=page_url,
        status=200,
        body=body,
        request=request,
    )

    items = list(process(response))
    assert items == []


@pytest.mark.parametrize("mime_type", ["text/html", "text/html; charset=utf-8"])
def test_http_pdf_link(mime_type):
    page_url = "https://esd.ny.gov"
    pdf_url = "https://esd.ny.gov/Reports/2015_2016/03312016_EXCELSIORJOBSPROGRAMQUARTERLYREPORT.pdf"
    title = "Some PDF"
    body = html(f"""<a href="{pdf_url}">{title}</a>""")

    request = Request(url=page_url)
    response = HtmlResponse(
        url=page_url,
        status=200,
        headers={"Content-Type": mime_type},
        body=body,
        request=request,
    )

    items = list(process(response))
    assert len(items) == 1
    pdf_request = items[0]
    assert pdf_request.url == pdf_url
    assert pdf_request.meta["title"] == title
    assert pdf_request.method == "HEAD"

    # TODO fix
    # referer = pdf_request.headers["referer"].decode("utf-8")
    # assert referer == page_url


def test_http_pdf_link_caps():
    page_url = "https://esd.ny.gov"
    pdf_url = "https://esd.ny.gov/Reports/2015_2016/03312016_EXCELSIORJOBSPROGRAMQUARTERLYREPORT.PDF"
    title = "Some PDF"
    body = html(f"""<a href="{pdf_url}">{title}</a>""")

    request = Request(url=page_url)
    response = HtmlResponse(
        url=page_url,
        status=200,
        body=body,
        request=request,
    )

    items = list(process(response))
    assert len(items) == 1
    pdf_request = items[0]
    assert pdf_request.url == pdf_url
    assert pdf_request.meta["title"] == title
    assert pdf_request.method == "HEAD"

    # TODO fix
    # referer = pdf_request.headers["referer"].decode("utf-8")
    # assert referer == page_url


def test_html_404():
    url = "https://esd.ny.gov/broken.html"

    request = Request(url=url, headers={"Referer": "https://esd.ny.gov/some.html"})
    response = HtmlResponse(
        url=url,
        status=404,
        body=b"not found",
        request=request,
    )

    items = list(process(response))
    assert len(items) == 1
    assert items[0].url == url


def test_pdf_404():
    url = "https://esd.ny.gov/broken.pdf"

    request = Request(url=url, headers={"Referer": "https://esd.ny.gov/some.html"})
    response = Response(
        url=url,
        status=404,
        headers={"Content-Type": "application/html"},
        body=b"not found",
        request=request,
    )

    items = list(process(response))
    assert len(items) == 1
    assert items[0].url == url


def test_html_redirect_to_homepage():
    source_url = "https://esd.ny.gov/some.html"
    redirect_url = "https://esd.ny.gov/other.html"
    end_url = "https://esd.ny.gov"

    request = Request(
        url=end_url,
        meta={"redirect_urls": [redirect_url]},
        headers={"Referer": source_url},
    )
    response = HtmlResponse(
        url=end_url,
        status=200,
        request=request,
    )

    items = list(process(response))
    assert len(items) == 1
    item = items[0]
    assert item.url == redirect_url
    assert item.source == source_url


def test_pdf_redirect_to_homepage():
    source_url = "https://esd.ny.gov/some.html"
    pdf_url = "https://esd.ny.gov/some.pdf"
    end_url = "https://esd.ny.gov"

    request = Request(
        url=end_url,
        meta={"redirect_urls": [pdf_url]},
        headers={"Referer": source_url},
    )
    response = Response(
        url=end_url,
        status=200,
        headers={"Content-Type": "application/pdf"},
        request=request,
    )

    items = list(process(response))
    assert len(items) == 1
    item = items[0]
    assert item.url == pdf_url
    assert item.source == source_url


def test_circular_html_redirect():
    source_url = "https://esd.ny.gov/some.html"
    redirect_url = "https://esd.ny.gov/other.html"

    request = Request(
        url=source_url,
        meta={"redirect_urls": [redirect_url]},
        headers={"Referer": source_url},
    )
    response = HtmlResponse(
        url=source_url,
        status=200,
        request=request,
    )

    items = list(process(response))
    assert len(items) == 1
    item = items[0]
    assert item.url == redirect_url
    assert item.source == source_url


def test_circular_pdf_redirect():
    source_url = "https://esd.ny.gov/some.html"
    pdf_url = "https://esd.ny.gov/some.pdf"

    request = Request(
        url=source_url,
        meta={"redirect_urls": [pdf_url]},
        headers={"Referer": source_url},
    )
    response = Response(
        url=source_url,
        status=200,
        headers={"Content-Type": "application/pdf"},
        request=request,
    )

    items = list(process(response))
    assert len(items) == 1
    item = items[0]
    assert item.url == pdf_url
    assert item.source == source_url
