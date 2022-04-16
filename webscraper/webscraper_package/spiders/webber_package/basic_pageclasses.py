from .basic_selectors import BasicPageSelectors as BPS
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
    
    def __init__(self, page, xpath):
        self.page = page
        self.xpath = xpath

        self.selector = self.get_selector(source=self.page.response, xpath=self.xpath)
        self.content = self.get_selector_content(selector=self.selector)

    def get_element(self, xpath):
        element = NestedElement(
            page=self.page,
            selector=self.selector, 
            xpath=xpath
            )
        return element

    def get_selector(self, source, xpath):
        selector = source.xpath(xpath)
        return selector

    def get_selector_content(self, selector):
        content = selector.get()
        return content

    def get_content_from_text(self, text, xpath):
        selector = Selector(text=text).xpath(xpath).get()
        return selector

class NestedElement(Element):

    def __init__(self, page, selector, xpath=None):
        self.page = page
        self.selector = selector
        self.xpath = xpath

        if xpath is not None:
            selector_content = self.get_selector_content(selector=self.selector)
            self.content = self.get_content_from_text(text=selector_content, xpath=self.xpath)

class ListElement(Element):

    def __init__(self, page, xpath, elements_xpath, element_type):
        super(ListElement, self).__init__(page, xpath)
        self.elements_selector = elements_xpath
        self.element_type = element_type

    def get_list_elements(self):
        element_selectors = self.get_selector(
            source=self.selector, 
            xpath=self.elements_selector
            )
        return element_selectors

    def get_list(self):
        store_list = []
        element_selectors = self.get_list_elements()
        for selector in element_selectors:
            store_list.append(self.element_type(
                page=self.page,
                selector=selector))
        return store_list