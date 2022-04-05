from webscraper.utils.descriptors import SpecifiedOnlyValidator, SpecifiedOrNoneValidator
from .basic_selectors import BasicPageSelectors as BPS
from scrapy.selector.unified import SelectorList
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector


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
        self.head = None
        self.body = None

    def get_head(self):
        if not isinstance(self.head, PageElement):
            self.head = PageElement(page=self, xpath=BPS.HEAD, name="HEAD" )
        return self.head

    def get_body(self):
        if not isinstance(self.body, PageElement):
            self.body = PageElement(page=self, xpath=BPS.BODY, name="BODY")
        return self.body

class PageElement:

    page            = SpecifiedOnlyValidator(Page)
    xpath           = SpecifiedOnlyValidator(str)
    selector        = SpecifiedOnlyValidator(SelectorList)
    content         = SpecifiedOnlyValidator((list, str))

    def __init__(self, page, xpath, name=None):
        self.page = page
        self.xpath = xpath
        if name is not None: 
            self.name = f"{name.strip().upper()}_ELEMENT"
        self.selector, self.content = self.get_element(xpath=self.xpath)
            
    def get_element(self, xpath):
        selector = self.page.response.xpath(xpath)
        content = selector.getall()
        return selector, content

class NestedPageElement:

    def __init__(self, page, element_content):
        self.page = page
        self.element_content = element_content
        self.selector_content = None

    def get_selector_content(self, xpath):
        self.selector_content = Selector(text=self.element_content).xpath(xpath).getall()
        return self.selector_content