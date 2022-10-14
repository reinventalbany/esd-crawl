import json
import os
import requests

key = os.environ["AIRTABLE_API_KEY"]
img_prefix = os.environ["IMG_PREFIX"]

with open("scrapy.json") as f:
    pdfs = json.load(f)


def create_record(table_name, record):
    # https://airtable.com/appdrqXSd2JNXkLp7/api/docs#curl/table:tables:create
    base = f"https://api.airtable.com/v0/appdrqXSd2JNXkLp7/{table_name}"
    headers = {"Authorization": f"Bearer {key}"}
    data = {"records": [record]}

    return requests.post(base, headers=headers, json=data)


for pdf in pdfs:
    for image in pdf["img_paths"]:
        img_url = img_prefix + image
        record = {
            "fields": {
                "Image": [{"url": img_url}],
                "PDF": [],
            }
        }

        response = create_record("Tables", record)
        if response.status_code == 200:
            print(".", end="", flush=True)
        else:
            print("")
            print(response.json())
