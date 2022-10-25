import os
import pytest
from responses import RequestsMock


@pytest.fixture
def r_mock():
    # https://github.com/getsentry/responses#requestmock-methods-start-stop-reset
    mock = RequestsMock(assert_all_requests_are_fired=True)
    mock.start()
    yield mock
    mock.stop()
    mock.reset()


@pytest.fixture
def pdf_path():
    return os.path.join("tests", "NYSTAR-2022-Annual-Report.pdf")
