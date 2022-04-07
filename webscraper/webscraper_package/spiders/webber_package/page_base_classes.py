from webscraper.utils.descriptors import SpecifiedOnlyValidator
from .basic_selectors import BasicPageSelectors as BPS
from scrapy.selector.unified import SelectorList
from scrapy.selector import Selector

class Page:
    
    def __init__(self, response, next_page=None, prev_page=None):
        self.response = response
        self.next_page = next_page
        self.prev_page = prev_page

        self.head = PageElement(page=self, xpath=BPS.HEAD)
        self.body = PageElement(page=self, xpath=BPS.BODY)
        self.url = response.url

class PageElement:
    
    selector = SpecifiedOnlyValidator(SelectorList)

    def __init__(self, page, xpath, selector=None, other_xpath=None):
        self.page = page
        self.xpath = xpath
        
        if selector is not None and other_xpath is not None:
            self.outer_selector, self.other_xpath = selector, other_xpath
            self.selector = self.get_nested_selector(
                            selector=self.outer_selector, 
                            xpath=self.xpath )
            self.content = self.get_content(xpath=self.other_xpath)

        else:
            self.selector = self.get_selector()
            self.content = self.get_content(xpath=self.xpath)

    def get_selector(self):
        selector = self.page.response.xpath(self.xpath)
        return selector

    def get_content(self, xpath, selector=None):
        if selector is None:
            selector = self.get_selector(xpath)
            self.selector = selector
        content = selector.getall()[0]
        return content

    def get_nested_selector(self, selector, xpath):
        selector = selector.xpath(xpath)
        #selector = Selector(text=self.element_content).xpath(xpath)
        return selector