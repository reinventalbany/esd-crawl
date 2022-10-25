import tempfile
from esd_crawl.tables import TableFinder
import requests


finder = TableFinder("parsehub_tables")
url = "https://esd.ny.gov/sites/default/files/news-articles/2021-NYSTAR-NY-MEP-Annual-Report.pdf"
with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
    response = requests.get(url)
    f.write(response.content)
    pdf_path = f.name

finder.find_tables(pdf_path, {})
