from responses import RequestsMock


def mock_pdf_download(r_mock: RequestsMock, url: str, file_path: str):
    with open(file_path, "rb") as f:
        contents = f.read()
        r_mock.get(url, body=contents, content_type="application/pdf")
