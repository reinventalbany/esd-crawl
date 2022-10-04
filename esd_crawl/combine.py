import csv

ORIGIN = "https://esd.ny.gov"
pdfs = {}


def add_pdf(url, title, source):
    if url.startswith("/"):
        # use absolute URLs
        url = ORIGIN + url

    if url not in pdfs:
        # first time being seen
        pdfs[url] = {
            "titles": set(),
            "sources": set(),
        }

    info = pdfs[url]
    info["titles"].add(title.strip())
    info["sources"].add(source)


with open("scrapy.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for entry in reader:
        add_pdf(entry["url"], entry["title"], entry["source"])

with open("parsehub.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for entry in reader:
        url = entry["report_url"]

        # The report will contain links to both PDFs and other pages. The latter will be covered by the sitemap crawl, so we can ignore them here.
        if url.endswith(".pdf"):
            add_pdf(
                url,
                entry["report_name"],
                "https://esd.ny.gov/esd-media-center/reports?tid[0]=516",
            )


def list_cell(data):
    """Format a list for entry in a data cell"""

    if len(data) > 5:
        # don't bother squishing in a zillion entries
        return "(many)"
    else:
        return "\n".join(data)


with open("pdfs.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["titles", "url", "sources"])
    writer.writeheader()

    for url, info in pdfs.items():
        titles = list_cell(info["titles"])
        sources = list_cell(info["sources"])
        row = {"url": url, "titles": titles, "sources": sources}

        writer.writerow(row)
