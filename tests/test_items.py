from esd_crawl.items import PDF


def test_pdf_abs_file_url_relative():
    pdf = PDF(title="", source="", file_urls=["/foo.pdf"])
    assert pdf.abs_file_url() == "https://esd.ny.gov/foo.pdf"


def test_pdf_abs_file_url_absolute():
    url = "https://other.gov/foo.pdf"
    pdf = PDF(title="", source="", file_urls=[url])
    assert pdf.abs_file_url() == url
