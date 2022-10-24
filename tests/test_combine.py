from esd_crawl.combine import PdfSet
from esd_crawl.items import PDF


def test_duplicates():
    pdf_set = PdfSet()

    pdf1 = PDF(
        title="Test PDF 1",
        source="https://foo.com/",
        file_urls=["http://foo.com/test1.pdf"],
        img_paths=["123.png"],
    )
    pdf_set.add(pdf1)

    pdf2 = PDF(
        title="Test PDF 2",
        source="https://foo.com/",
        file_urls=["http://foo.com/test2.pdf"],
        img_paths=["456.png"],
    )
    pdf_set.add(pdf2)

    pdf3 = PDF(
        title="Test PDF 1 - other",
        source="https://foo.com/",
        file_urls=["http://foo.com/test1.pdf"],
        img_paths=["123.png"],
    )
    pdf_set.add(pdf3)

    pdfs = pdf_set.to_dict()
    assert len(pdfs) == 2

    pdf_result = pdfs["http://foo.com/test1.pdf"]
    assert pdf_result["titles"] == {"Test PDF 1", "Test PDF 1 - other"}
    assert pdf_result["sources"] == {"https://foo.com/"}
    assert pdf_result["img_paths"] == {"123.png"}
