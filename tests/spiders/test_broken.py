from esd_crawl.spiders.broken import process_response
from scrapy.http import Request, HtmlResponse


def html(body: str = ""):
    html_str = f"""
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>{body}</body>
    </html>
    """

    return bytes(html_str, "utf-8")


def test_http_no_links():
    response = HtmlResponse(
        url="https://esd.ny.gov",
        status=200,
        headers={"Content-Type": "text/html"},
        body=html(),
        request=Request(url="https://esd.ny.gov"),
    )

    items = list(process_response(response))
    assert items == []


def test_http_pdf_link():
    pdf_url = "https://esd.ny.gov/Reports/2015_2016/03312016_EXCELSIORJOBSPROGRAMQUARTERLYREPORT.pdf"
    body = html(f"""<a href="{pdf_url}">PDF</a>""")

    response = HtmlResponse(
        url="https://esd.ny.gov",
        status=200,
        headers={"Content-Type": "text/html"},
        body=body,
        request=Request(url="https://esd.ny.gov"),
    )

    items = list(process_response(response))
    assert len(items) == 1
    assert items[0].url == pdf_url
