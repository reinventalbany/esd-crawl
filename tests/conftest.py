import pytest
import responses


@pytest.fixture
def r_mock():
    # https://github.com/getsentry/responses#requestmock-methods-start-stop-reset
    mock = responses.RequestsMock(assert_all_requests_are_fired=True)
    mock.start()
    yield mock
    mock.stop()
    mock.reset()
