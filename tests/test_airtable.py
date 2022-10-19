from esd_crawl import airtable
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


def mock_create_record(r_mock, table_name):
    r_mock.post(
        f"https://api.airtable.com/v0/appdrqXSd2JNXkLp7/{table_name}",
        json={"records": [{"id": "456"}]},
    )


def test_create_record_success(r_mock):
    table_name = "Fake"
    mock_create_record(r_mock, table_name)

    id = airtable.create_record("123", table_name, {})
    assert id is not None


def test_create_record_fail(r_mock):
    table_name = "Fake"
    r_mock.post(
        f"https://api.airtable.com/v0/appdrqXSd2JNXkLp7/{table_name}",
        json={},
        status=404,
    )

    id = airtable.create_record("123", table_name, {})
    assert id is None
