from esd_crawl.combine import PdfSet


def test_duplicates():
    pdf_set = PdfSet()
    pdf_set.add(
        "http://foo.com/test1.pdf", "Test PDF 1", "https://foo.com/", ["123.png"]
    )
    pdf_set.add(
        "http://foo.com/test2.pdf", "Test PDF 2", "https://foo.com/", ["456.png"]
    )
    pdf_set.add(
        "http://foo.com/test1.pdf",
        "Test PDF 1 - other",
        "https://foo.com/",
        ["123.png"],
    )

    pdfs = pdf_set.to_dict()
    assert len(pdfs) == 2

    pdf1 = pdfs["http://foo.com/test1.pdf"]
    assert pdf1["titles"] == {"Test PDF 1", "Test PDF 1 - other"}
    assert pdf1["sources"] == {"https://foo.com/"}
    assert pdf1["img_paths"] == {"123.png"}
