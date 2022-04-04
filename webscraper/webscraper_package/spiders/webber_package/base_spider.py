from scrapy import Spider, Request

from .page_classes import Page
from ....data.filepaths import FilePaths
from webscraper.utils.descriptors import SpecifiedOnlyValidator

class BaseSpider(Spider):

    name = "Base Spider"

    performed_searches  = SpecifiedOnlyValidator(list)
    saved_pages         = SpecifiedOnlyValidator(list)

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.performed_searches = []
        self.saved_pages = []

    def start_requests(self):
        if self.start_urls is not None:
            for url in self.start_urls:
                request = self.scrape_page(url, self.parse)
                yield request

    def database_query(self, command, **kwargs):
        func = command(receiver=self.data_manager, payload=kwargs)
        result = func.execute()
        return result

    def create_page(self, response, page_class):
        page = page_class(response)
        self.saved_pages.append(page)
        return page

    def scrape_page(self, url, callback=None, **kwargs):
        wrap_callback = self.print_response(callback=callback)
        self.performed_searches.append(url)
        request = Request(url=url, callback=wrap_callback, cb_kwargs=kwargs, dont_filter=True)
        return request

    def print_response(self, callback):
        def wrapper(response, **kwargs):
            if response is not None:
                print(f"\n[Received response: {response.status}, from IP: {response.ip_address}]\
                    \n\t(using {response.url})")
            callback(response, **kwargs)
        return wrapper

    def parse(self, response, **kwargs):
        page = self.create_page(response, Page)
        print(page.source_url)
        with open(FilePaths.response_path, 'w') as file:
            file.write(response.text)

