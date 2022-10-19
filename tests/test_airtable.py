import responses
from esd_crawl import airtable


@responses.activate
def test_create_record_success():
    table_name = "Fake"
    response = responses.Response(
        method="POST",
        url=f"https://api.airtable.com/v0/appdrqXSd2JNXkLp7/{table_name}",
        json={"records": [{"id": "456"}]},
    )
    responses.add(response)

    id = airtable.create_record("123", table_name, {})
    assert id is not None


@responses.activate
def test_create_record_fail():
    table_name = "Fake"
    response = responses.Response(
        method="POST",
        url=f"https://api.airtable.com/v0/appdrqXSd2JNXkLp7/{table_name}",
        json={},
        status=404,
    )
    responses.add(response)

    id = airtable.create_record("123", table_name, {})
    assert id is None
