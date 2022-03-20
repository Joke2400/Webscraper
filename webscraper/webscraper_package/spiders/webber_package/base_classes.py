from scrapy import Spider, Request
from scrapy.selector.unified import SelectorList
from scrapy.http.response.html import HtmlResponse

from ....data.filepaths import FilePaths
from .selectors import BasicPageElementSelectors as BPS
from webscraper.utils.descriptors import SpecifiedOnlyValidator, SpecifiedOrNoneValidator

class BaseSpider(Spider):

    name = "Base Spider"

    saved_pages = SpecifiedOnlyValidator(list)

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.saved_pages = []

    def start_requests(self):
        if self.start_urls is not None:
            for url in self.start_urls:
                request = self.scrape_page(url, self.parse)
                yield request

    def scrape_page(self, url, callback=None, **kwargs):
        wrap_callback = self.print_response(callback=callback)
        request = Request(url=url, callback=wrap_callback, cb_kwargs=kwargs)
        return request

    def print_response(self, callback):
        def wrapper(response, **kwargs):
            if response is not None:
                print(f"\nReceived response: {response.status}, from IP: {response.ip_address}\
                    \n\tusing {response.url}")
            self.saved_pages.append(Page(response))
            callback(response, **kwargs)
        return wrapper

    def parse(self, response, **kwargs):
        with open(FilePaths.response_path, 'w') as file:
            file.write(response.text)

class Page:

    response    = SpecifiedOnlyValidator(HtmlResponse)
    next_page   = SpecifiedOrNoneValidator(bool)
    prev_page   = SpecifiedOrNoneValidator(bool)
    source_url  = SpecifiedOnlyValidator(str)

    def __init__(self, response, next_page=None, prev_page=None):
        self.response = response
        self.next_page = next_page
        self.prev_page = prev_page
        self.source_url = self.response.url
        self.head = PageElement("HEAD", self, BPS.HEAD)
        self.body = PageElement("BODY", self, BPS.BODY)

class PageElement:

    name            = SpecifiedOnlyValidator(str)
    page            = SpecifiedOnlyValidator(Page)
    selector_str    = SpecifiedOnlyValidator(str)

    selector        = SpecifiedOnlyValidator(SelectorList)
    content         = SpecifiedOnlyValidator((list, str))

    def __init__(self, name, page, selector_str):
        self.name = name.strip().upper() + "_ELEMENT"
        self.page = page
        self.selector_str = selector_str
        self.fetch_content()

    def fetch_content(self):
        response = self.page.response
        self.selector = response.xpath(self.selector_str)
        self.content = self.selector.getall()