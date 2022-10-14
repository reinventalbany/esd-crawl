# Empire State Development data scraper

The goal of this tool is to find data on the [Empire State Development website](https://esd.ny.gov/), either in web pages or PDFs. [Running notes document.](https://docs.google.com/document/d/1HaWvHlpCYcD1SRmZn9DbsQoFCkvywBifcyME4cvjT-k/edit)

## Technical overview

The site-wide crawl is done via [Scrapy](https://scrapy.org/). The crawl of the [Reports page](https://esd.ny.gov/esd-media-center/reports?tid[0]=516) is done via [ParseHub](https://parsehub.com/), as that was easier to get working for the AJAX pagination.

## Usage

1. Crawl HTML pages

   1. Install Python 3
   1. Install [Poetry](https://python-poetry.org/)
   1. Clone repository
   1. From repository directory, run `poetry init`
   1. Run `poetry shell`
   1. Run the scraper. This will take a few minutes.

      ```sh
      scrapy runspider esd_crawl/spiders/esd.py -L INFO -O scrapy.csv
      ```

   1. View the list of discovered PDFs in `scrapy.csv`. Note there will be duplicate URLs present.

1. Crawl [Reports page](https://esd.ny.gov/esd-media-center/reports?tid[0]=516)
   1. Install [ParseHub](https://parsehub.com/)
   1. [Import](https://help.parsehub.com/hc/en-us/articles/115001733294-Export-Import-Projects) the Project, which is the `esd.ny.gov_Project.phj` file in this directory
   1. Run the Project
   1. Download Data as CSV
   1. Save as `parsehub.csv` in this directory
1. Combine the data
   1. Run `python esd_crawl/combine.py`
1. View `pdfs.csv`
1. Extract the tables
   1. [Install visual debugging dependencies](https://github.com/jsvine/pdfplumber#visual-debugging)
   1. Open [`extract.ipynb`](esd_crawl/extract.ipynb) in Visual Studio Code
   1. Click `Run All`

There will be one row per PDF URL, and multiple titles and source URLs for each will be combined with newlines within each row.

## Troubleshooting

[The spider](esd_crawl/spiders/esd.py) can be tested on a particular URL with:

```sh
scrapy parse --pipelines <url>
```

[More info on `parse`](https://docs.scrapy.org/en/latest/topics/commands.html#parse), and [general debugging info](https://docs.scrapy.org/en/latest/topics/debug.html).
