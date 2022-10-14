import json
import os
import requests

key = os.environ["AIRTABLE_API_KEY"]
img_prefix = os.environ["IMG_PREFIX"]


def create_record(table_name, record):
    # https://airtable.com/appdrqXSd2JNXkLp7/api/docs#curl/table:tables:create
    base = f"https://api.airtable.com/v0/appdrqXSd2JNXkLp7/{table_name}"
    headers = {"Authorization": f"Bearer {key}"}
    data = {"records": [record]}

    response = requests.post(base, headers=headers, json=data)
    resp_data = response.json()

    if response.status_code != 200:
        # failure
        print("")
        print(resp_data)
        return None

    return resp_data["records"][0]["id"]


def create_pdf(url, titles):
    record = {"fields": {"URL": url, "Titles": "\n".join(titles)}}
    return create_record("PDFs", record)


def create_table(img_url, pdf_id):
    record = {
        "fields": {
            "Image": [{"url": img_url}],
            "PDF": [pdf_id],
        }
    }
    return create_record("Tables", record)


with open("pdfs.json") as f:
    pdfs = json.load(f)

for pdf_url, pdf in pdfs.items():
    pdf_id = create_pdf(pdf_url, pdf["titles"])
    if pdf_id is None:
        continue

    for image in pdf["img_paths"]:
        img_url = img_prefix + image
        table_id = create_table(img_url, pdf_id)
        if table_id:
            print(".", end="", flush=True)