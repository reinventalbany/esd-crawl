from esd_crawl.items import PDF


def find_pdf_links(response):
    for link in response.css('a[href$=".pdf"]'):
        title = link.css("::text").get()
        url = link.css("::attr(href)").get()
        absolute_url = response.urljoin(url)

        yield PDF(title=title, file_urls=[absolute_url], source=response.url)
