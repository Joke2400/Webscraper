from webscraper.utils.descriptors import SpecifiedOrNoneValidator
from .basic_selectors import BasicPageSelectors as BPS
from scrapy.selector.unified import SelectorList
from scrapy.selector import Selector

class Page:
    
    def __init__(self, response, prev_page=None, next_page=None):
        self.response = response
        self.prev_page = prev_page
        self.next_page = next_page
        self.url = response.url

        self.head = Element(page=self, xpath=BPS.HEAD)
        self.body = Element(page=self, xpath=BPS.BODY)
    
class Element:
    
    selector = SpecifiedOrNoneValidator(SelectorList)

    def __init__(self, page, xpath):
        self.page = page
        self.xpath = xpath

        self.selector = self.get_selector(source=self.page.response, xpath=self.xpath)
        self.content = self.get_selector_content(selector=self.selector)

    def get_selector(self, source, xpath):
        selector = source.xpath(xpath)
        return selector

    def get_selector_content(self, selector):
        content = selector.getall()
        return content

    def get_selector_from_text(self, text, xpath):
        selector = Selector(text=text).xpath(xpath)
        return selector

class NestedElement(Element):

    def __init__(self, page, xpath, base_selector):
        self.page = page
        self.xpath = xpath
        self.base_selector = base_selector

        self.selector = self.get_selector(source=self.base_selector, xpath=self.xpath)
        self.content = self.get_selector_content(selector=self.selector)