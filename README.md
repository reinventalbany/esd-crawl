# Empire State Development data scraper

The goal of this tool is to find data on the [Empire State Development website](https://esd.ny.gov/), either in web pages or PDFs.

[Running notes document](https://docs.google.com/document/d/1HaWvHlpCYcD1SRmZn9DbsQoFCkvywBifcyME4cvjT-k/edit)

## Usage

1. Install Python 3
1. Install [Poetry](https://python-poetry.org/)
1. Clone repository
1. From repository directory, run `poetry init`.
1. Run `poetry shell`.
1. Run the scraper. This will take a few minutes.

   ```sh
   scrapy runspider esd_crawl/scraper.py -O pdfs.csv
   ```

1. View the list of discovered PDFs in `pdfs.csv`.
