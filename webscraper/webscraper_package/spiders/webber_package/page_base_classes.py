from webscraper.utils.descriptors import SpecifiedOnlyValidator, SpecifiedOrNoneValidator
from .basic_selectors import BasicPageSelectors as BPS
from scrapy.selector.unified import SelectorList
from scrapy.http.response.html import HtmlResponse


class Page:

    response    = SpecifiedOnlyValidator(HtmlResponse)
    url         = SpecifiedOnlyValidator(str)
    next_page   = SpecifiedOrNoneValidator(bool)
    prev_page   = SpecifiedOrNoneValidator(bool)
    
    def __init__(self, response, next_page=None, prev_page=None):
        self.response = response
        self.url = response.url

        self.next_page = next_page
        self.prev_page = prev_page
  
    def fetch_head(self):
        self.head = PageElement(page=self, xpath=BPS.HEAD, name="HEAD" )

    def fetch_body(self):
        self.body = PageElement(page=self, xpath=BPS.BODY, name="BODY")

class PageElement:

    page            = SpecifiedOnlyValidator(Page)
    xpath           = SpecifiedOnlyValidator(str)
    selector        = SpecifiedOnlyValidator(SelectorList)
    content         = SpecifiedOnlyValidator((list, str))

    def __init__(self, page, xpath, name=None):
        self.page = page
        self.xpath = xpath
        self.name = f"{name.strip().upper()}_ELEMENT"
        self.get_response_content()

    def fetch_response_content(self):
        response = self.page.response
        self.selector = response.xpath(self.xpath)
        self.content = self.selector.getall()

class NestedPageElement(PageElement):

    def __init__(self, page, xpath, selector):
        self.page = page
        self.xpath = xpath
        self.selector = selector

    def fetch_element(self, selector, xpath_str):
        selector = selector.xpath(xpath_str)
        return selector