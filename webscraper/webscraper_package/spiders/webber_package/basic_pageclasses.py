from .basic_selectors import BasicPageSelectors as BPS
from scrapy.selector import Selector

class Page:
    
    def __init__(self, response, prev_page=None, next_page=None):
        self.response = response
        self.url = response.url
        self.prev_page = prev_page
        self.next_page = next_page
    
class Element:
    
    def __init__(self, source, xpath):
        self.source = source
        self.xpath = xpath
        self.selector = self.extract_selector(
            source=self.source.response,
            xpath=self.xpath)

    def extract_selector(self, xpath, source=None):
        if source is None:
            source = self.selector
        selector = source.xpath(xpath)
        return selector

    def extract(self, xpath=None, source=None):
        if source is None:
            source = self.selector
        if xpath is not None:
            content = self.extract_selector(
                source=source,
                xpath=xpath).get()
        else:
            content = self.selector.get()
        return content

class NestedElement(Element):

    def __init__(self, source, selector, xpath=None):
        self.source = source
        self.selector = selector
        self.xpath = xpath

        if xpath is not None:
            selector_content = self.get_selector_content(selector=self.selector)
            self.content = self.get_content_from_text(text=selector_content, xpath=self.xpath)

class ListElement(Element):

    def __init__(self, source, xpath, items_xpath, element_type):
        super(ListElement, self).__init__(source, xpath)
        self.items_xpath = items_xpath
        self.element_type = element_type
        self.list_elements = self.extract(
            xpath=self.items_xpath)

    def get_list(self):
        store_list = []
        element_selectors = self.get_list_elements()
        for selector in element_selectors:
            store_list.append(self.element_type(
                page=self.source,
                selector=selector))
        return store_list

    '''
    def get_element(self, xpath):
        element = NestedElement(
            page=self.page,S
            selector=self.selector, 
            xpath=xpath
            )
        return element

    def get_content_from_text(self, text, xpath):
        selector = Selector(text=text).xpath(xpath).get()
        return selector
    '''