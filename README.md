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
   1. Run the spider. This will take a few minutes.

      ```sh
      scrapy runspider esd_crawl/spiders/esd.py -L INFO -O scrapy.json
      ```

   1. View the list of discovered PDFs in `scrapy.json`. Note there will be duplicate URLs present.

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
1. Put table images somewhere publicly accessible. Example for [Google Cloud Storage](https://cloud.google.com/storage):
   1. [Create a bucket](https://cloud.google.com/storage/docs/creating-buckets)
   1. [Upload the `tables/` folder](https://cloud.google.com/storage/docs/uploading-objects)
   1. [Make the bucket publicly readable](https://cloud.google.com/storage/docs/access-control/making-data-public#buckets)
   1. [Get the public URL](https://cloud.google.com/storage/docs/access-public-data#console) from one of the objects
1. Create the Airtable records

   1. [Get your Airtable API key](https://airtable.com/account)
   1. Set the key as an environment variable:

      ```sh
       export AIRTABLE_API_KEY=...
      ```

   1. Run the script. `IMG_PREFIX` will be the public object URL, minus the filename. Example:

      ```sh
      IMG_PREFIX=https://storage.googleapis.com/esd-data/tables/ python esd_crawl/airtable.py
      ```

There will be one row per PDF URL, and multiple titles and source URLs for each will be combined with newlines within each row.

## Troubleshooting

### Limit the crawl

See the [close spider settings](https://docs.scrapy.org/en/latest/topics/extensions.html#module-scrapy.extensions.closespider). For example:

```sh
scrapy runspider esd_crawl/spiders/esd.py -s CLOSESPIDER_ITEMCOUNT=5
```

### Test a particular URL

```sh
scrapy parse --pipelines <url>
```

[More info on `parse`](https://docs.scrapy.org/en/latest/topics/commands.html#parse), and [general debugging info](https://docs.scrapy.org/en/latest/topics/debug.html).
