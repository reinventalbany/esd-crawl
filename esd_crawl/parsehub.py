from io import BufferedReader
import tempfile
from esd_crawl.tables import TableFinder
import requests


finder = TableFinder("parsehub_tables")
url = "https://esd.ny.gov/sites/default/files/news-articles/2021-NYSTAR-NY-MEP-Annual-Report.pdf"
with tempfile.NamedTemporaryFile(suffix=".pdf") as fp:
    response = requests.get(url)
    fp.write(response.content)
    fp.seek(0)

    finder.find_tables(fp, {})  # type: ignore
