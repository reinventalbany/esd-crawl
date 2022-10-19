import json
import os
from urllib.parse import urlparse
import requests


def table_api_url(table_name):
    return f"https://api.airtable.com/v0/appdrqXSd2JNXkLp7/{table_name}"


def perform_request(method: str, table_name: str, key: str, **kwargs):
    url = table_api_url(table_name)
    headers = {"Authorization": f"Bearer {key}"}

    return requests.request(method, url, headers=headers, **kwargs)


def find_record_by(key: str, table_name: str, column: str, val: str):
    response = perform_request(
        "GET",
        table_name,
        key,
        params={"maxRecords": 1, "filterByFormula": f"{{{column}}} = '{val}'"},
    )
    resp_data: dict = response.json()

    if response.status_code != 200:
        # failure
        print("")
        print(resp_data)
        raise RuntimeError("Unable to get records")

    records: list[dict] = resp_data["records"]
    if len(records) == 0:
        return None

    return records[0]


def create_record(key, table_name, record):
    data = {"records": [record]}
    response = perform_request("POST", table_name, key, json=data)
    resp_data = response.json()

    if response.status_code != 200:
        # failure
        print("")
        print(resp_data)
        raise RuntimeError("Unable to create record")

    id: str = resp_data["records"][0]["id"]
    return id


def update_record(key: str, table_name: str, record: dict):
    if "id" not in record:
        raise RuntimeError("Record must have an id specified")

    data = {"records": [record]}
    response = perform_request("PATCH", table_name, key, json=data)
    resp_data = response.json()

    if response.status_code != 200:
        # failure
        print("")
        print(resp_data)
        raise RuntimeError("Unable to update record")


def upsert_record(key: str, table_name: str, unique_column: str, record: dict):
    unique_val = record["fields"][unique_column]
    existing = find_record_by(key, table_name, unique_column, unique_val)
    if existing:
        id: str = existing["id"]
        new_record = record.copy()
        new_record["id"] = id

        update_record(key, table_name, new_record)

        return id

    return create_record(key, table_name, record)


def upsert_pdf(key, url, titles):
    record = {"fields": {"URL": url, "Titles": "\n".join(titles)}}
    return upsert_record(key, "PDFs", "URL", record)


def upsert_table(key, img_url, pdf_id):
    # https://airtable.com/appdrqXSd2JNXkLp7/api/docs#curl/table:tables:create

    table_name = "Tables"
    record = {
        "fields": {
            "Image": [{"url": img_url}],
            "PDF": [pdf_id],
        }
    }

    # since this is a computed/formula column, use a variation of the upsert logic
    path = urlparse(img_url).path
    filename = os.path.basename(path)
    existing = find_record_by(key, table_name, "Image filename", filename)
    if existing:
        id: str = existing["id"]
        record["id"] = id

        update_record(key, table_name, record)

        return id

    return create_record(key, table_name, record)


def run():
    key = os.environ["AIRTABLE_API_KEY"]
    img_prefix = os.environ["IMG_PREFIX"]

    with open("pdfs.json") as f:
        pdfs = json.load(f)

    for pdf_url, pdf in pdfs.items():
        pdf_id = upsert_pdf(key, pdf_url, pdf["titles"])

        for image in pdf["img_paths"]:
            img_url = img_prefix + image
            table_id = upsert_table(key, img_url, pdf_id)
            if table_id:
                print(".", end="", flush=True)


if __name__ == "__main__":
    run()
