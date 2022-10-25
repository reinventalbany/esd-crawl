import pytest
from esd_crawl.combine import PdfSet
from esd_crawl.items import PDF, Table


def test_duplicates():
    pdf_set = PdfSet()

    table1 = Table(img_path="123.png", page_num=4)
    table2 = Table(img_path="456.png", page_num=7)

    pdf1 = PDF(
        title="Test PDF 1",
        source="https://foo.com/",
        file_urls=["http://foo.com/test1.pdf"],
        tables=[table1],
    )
    pdf_set.add(pdf1)

    pdf2 = PDF(
        title="Test PDF 2",
        source="https://foo.com/",
        file_urls=["http://foo.com/test2.pdf"],
        tables=[table2],
    )
    pdf_set.add(pdf2)

    pdf3 = PDF(
        title="Test PDF 1 - other",
        source="https://foo.com/",
        file_urls=["http://foo.com/test1.pdf"],
        tables=[table1],
    )
    pdf_set.add(pdf3)

    assert pdf_set.len() == 2

    pdf_result = pdf_set.get("http://foo.com/test1.pdf")
    assert pdf_result["titles"] == {"Test PDF 1", "Test PDF 1 - other"}
    assert pdf_result["sources"] == {"https://foo.com/"}
    assert pdf_result["tables"] == [table1]

    assert pdf_set.num_pdfs_with_tables() == 2
    assert pdf_set.num_tables() == 2


def test_file_without_urls():
    pdf_set = PdfSet()
    pdf = PDF(
        title="Test PDF",
        source="https://foo.com/",
        file_urls=[],
        tables=[],
    )
    with pytest.raises(RuntimeError):
        pdf_set.add(pdf)


def test_make_url_absolute():
    pdf_set = PdfSet()
    pdf = PDF(
        title="Test PDF",
        source="https://foo.com/",
        file_urls=["/test1.pdf"],
        tables=[],
    )
    pdf_set.add(pdf)

    assert pdf_set.urls() == ["https://esd.ny.gov/test1.pdf"]
