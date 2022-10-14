from esd_crawl.items import PDF
from io import BytesIO
from PIL import Image


def find_pdf_links(response):
    for link in response.css('a[href$=".pdf"]'):
        title = link.css("::text").get()
        url = link.css("::attr(href)").get()
        absolute_url = response.urljoin(url)

        yield PDF(title=title, file_urls=[absolute_url], source=response.url)


async def display_screenshot(page):
    """Requires playwright_include_page=True"""

    screenshot = await page.screenshot(full_page=True)
    im = Image.open(BytesIO(screenshot))
    im.show()
