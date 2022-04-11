from .foodie_selectors import SearchResultsPageLocators as SRPL
from .foodie_selectors import StoreListSearchLocators as SLSL
from .base_pageclasses import Page, Element, NestedElement

class StoreList(Element):

    def __init__(self):
        self.store_list = []
        self.fields_added = False

    def __get__(self, obj, objtype=None):
        if not self.fields_added or objtype == None:
            self.fields_added = True
            return self
        if len(self.store_list) == 0:
            self.get_stores()
        return self.store_list

    def __getitem__(self, fields):
        self.elements_selector = fields["elements_xpath"]
        super(StoreList, self).__init__(fields["page"], fields["xpath"])

    def __set__(self, obj, value):
        if isinstance(value, list):
            self.store_list = value

    def get_stores(self):
        element_selectors = self.get_selector(
            source=self.selector, 
            xpath=self.elements_selector
            )
        for selector in element_selectors:
            self.store_list.append(StoreElement(
                page=self.page,
                selector=selector))

class StoreListPage(Page):

    stores = StoreList()

    def __init__(self, response, prev_page=None, next_page=None):
        super(StoreListPage, self).__init__(response, prev_page, next_page)
        fields = {"page" : self, "xpath" : SLSL.STORE_LIST, "elements_xpath" : SLSL.STORE_LIST_ELEMENTS}
        self.stores[fields] #<-- Had some fun with descriptors, 
                                    # pointless way of doing it really

class StoreElement(NestedElement):

    def __init__(self, page, selector):
        super(StoreElement, self).__init__(page, selector)
        self.name       = self.get_element(xpath=SLSL.STORE_NAME)
        self.href       = self.get_element(xpath=SLSL.STORE_HREF)
        self.select     = self.get_element(xpath=SLSL.STORE_SELECT)
        self.address    = self.get_element(xpath=SLSL.STORE_ADDRESS)

    def get_element(self, xpath):
        element = NestedElement(
            page=self.page,
            selector=self.selector, 
            xpath=xpath
            )
        return element