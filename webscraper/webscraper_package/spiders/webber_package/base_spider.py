from webscraper.utils.descriptors import SpecifiedOnlyValidator
from ....data.filepaths import FilePaths
from .foodie_pageclasses import Page
from scrapy import Spider, Request
import datetime

class BaseSpider(Spider):

    name = "Base Spider"

    performed_searches  = SpecifiedOnlyValidator(list)
    saved_pages         = SpecifiedOnlyValidator(list)

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.performed_searches = []
        self.saved_pages = []
        self.response_times = []

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
        kwargs["start_time"] = datetime.datetime.now()
        request = Request(url=url, callback=wrap_callback, cb_kwargs=kwargs, dont_filter=True)
        return request

    def print_response(self, callback):
        def wrapper(response, **kwargs):
            end_time = datetime.datetime.now()
            start_time = kwargs.get("start_time")
            duration = end_time - start_time
            self.response_times.append(duration)
            if response is not None:
                print(f"[Received response]: '{response.status}', from IP: '{response.ip_address}'  (Took: {duration}).\
                    \n\tusing '{response.url}'")
            callback(response, **kwargs)
        return wrapper

    def parse(self, response, **kwargs):
        page = self.create_page(response, Page)
        print(page.source_url)
        with open(FilePaths.response_path, 'w') as file:
            file.write(response.text)

