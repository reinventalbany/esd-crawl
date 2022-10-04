# import json


# f = open("/Users/afeld/Downloads/run_results-3.json")
# data = json.load(f)


# num_pdfs = 0
# num_pages = 0
# for result in data["report"]:
#     if result["url"].endswith(".pdf"):
#         num_pdfs += 1
#     else:
#         num_pages += 1
#         print(result["url"])

# print("PDFs:", num_pdfs)
# print("Pages:", num_pages)


import csv

pdfs = {}


def add_pdf(url, title, source):
    if url.startswith("/"):
        url = f"https://esd.ny.gov{url}"

    if url not in pdfs:
        # first time being seen
        pdfs[url] = {
            "titles": set(),
            "sources": set(),
        }

    pdf_data = pdfs[url]
    pdf_data["titles"].add(title.strip())
    pdf_data["sources"].add(source)


with open("scrapy.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for entry in reader:
        add_pdf(entry["url"], entry["title"], entry["source"])

with open("parsehub.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for entry in reader:
        add_pdf(
            entry["report_url"],
            entry["report_name"],
            "https://esd.ny.gov/esd-media-center/reports?tid[0]=516",
        )


def list_cell(data):
    if len(data) > 5:
        return "(many)"
    else:
        return "\n".join(data)


with open("pdfs.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["titles", "url", "sources"])
    writer.writeheader()

    for url, info in pdfs.items():
        row = {"url": url}

        row["titles"] = list_cell(info["titles"])
        row["sources"] = list_cell(info["sources"])

        writer.writerow(row)
