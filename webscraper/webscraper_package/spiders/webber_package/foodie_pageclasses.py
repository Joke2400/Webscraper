from .foodie_selectors import SearchResultsPageLocators as SRPL
from .foodie_selectors import StoreListSearchLocators as SLSL
from .base_pageclasses import Page, Element, NestedElement

class Topmenu(Element):
    
    def __init__(self, page, xpath):
        super(Topmenu, self).__init__(page, xpath)
        self.name = self.get_element(xpath=SRPL.STORE_NAME)
        self.name_str = self.name.content.strip().lower()

        self.href = self.get_element(xpath=SRPL.STORE_HREF)
        self.address = self.get_element(xpath=SRPL.STORE_ADDRESS)
        self.open_times = self.get_element(xpath=SRPL.STORE_OPEN_TIMES)

class Navigation(Element):

    def __init__(self, page, xpath):
        super(Navigation, self).__init__(page, xpath)
        if self.content is not None:
            self.next = self.get_element(xpath=SLSL.NAV_NEXT)
            self.prev = self.get_element(xpath=SLSL.NAV_PREV)
            self.page.next_page = self.next.content
            if self.prev.content.split("&page")[1] != '':
                self.page.prev_page = self.prev.content

class FoodiePage(Page):

    def __init__(self, response, prev_page=None, next_page=None):
        super(FoodiePage, self).__init__(response, prev_page, next_page)
        self.topmenu = Topmenu(page=self, xpath=SRPL.STORES_TOPMENU)

class StoreElement(NestedElement):

    def __init__(self, page, selector):
        super(StoreElement, self).__init__(page, selector)
        self.name           = self.get_element(xpath=SLSL.STORE_NAME)
        self.name_str       = self.name.content.strip().lower()
        
        self.href           = self.get_element(xpath=SLSL.STORE_HREF)
        self.select         = self.get_element(xpath=SLSL.STORE_SELECT)
        self.address        = self.get_element(xpath=SLSL.STORE_ADDRESS)

class StoreList(Element):

    def __init__(self, page, xpath, elements_xpath):
        super(StoreList, self).__init__(page, xpath)
        self.elements_selector = elements_xpath

    def get_stores(self):
        self.store_list = []
        element_selectors = self.get_selector(
            source=self.selector, 
            xpath=self.elements_selector
            )
        for selector in element_selectors:
            self.store_list.append(StoreElement(
                page=self.page,
                selector=selector))
        return self.store_list

class StoreListPage(FoodiePage):

    def __init__(self, response, prev_page=None, next_page=None):
        super(StoreListPage, self).__init__(response, prev_page, next_page)
        self.navigation = Navigation(page=self, xpath=SLSL.NAVIGATION_BUTTONS)
        self.stores = []
       
    def get_store_list(self):
        store_list = StoreList(page=self, xpath=SLSL.STORE_LIST, elements_xpath=SLSL.STORE_LIST_ELEMENTS)
        self.stores = store_list.get_stores()

class ProductPage:
    pass