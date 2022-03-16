from scrapy import Spider, Request

class BaseSpider(Spider):

    name = "Base Spider"

    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)

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
            callback(response, **kwargs)
        return wrapper

    def parse(self, response, **kwargs):
        pass

class Page:

    def __init__(self, next, prev):
        pass


class PageElement:

    def __init__(self, name, selector):
        pass