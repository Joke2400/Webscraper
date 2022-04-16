from .foodie_selectors import SearchResultsPageLocators as SRPL
from .foodie_selectors import StoreListSearchLocators as SLSL
from .foodie_selectors import ProductListSearchLocators as PLSL
from .basic_pageclasses import Page, Element, NestedElement, ListElement

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

class StoreListPage(FoodiePage):

    def __init__(self, response, prev_page=None, next_page=None):
        super(StoreListPage, self).__init__(response, prev_page, next_page)
        self.navigation = Navigation(page=self, xpath=SLSL.NAVIGATION_BUTTONS)
        self.store_list = ListElement(
            page=self, 
            xpath=SLSL.STORE_LIST, 
            elements_xpath=SLSL.STORE_LIST_ELEMENTS,
            element_type=StoreElement
            )
        self.stores = self.store_list.get_list()

class ProductElement(NestedElement):

    def __init__(self, page, selector):
        super(ProductElement, self).__init__(page, selector)
        self.name           = self.get_element(xpath=PLSL.PRODUCT_NAME)
        self.name_str       = self.name.content.strip()
        self.name_match_str = self.name_str.lower()
        
        self.quantity       = self.get_element(xpath=PLSL.PRODUCT_QUANTITY)
        self.quantity_str   = self.quantity.content.replace(",", "")
        self.subname        = self.get_element(xpath=PLSL.PRODUCT_SUBNAME)
        
        self.price_whole    = self.get_element(xpath=PLSL.PRODUCT_PRICE_WHOLE)
        self.price_decimal  = self.get_element(xpath=PLSL.PRODUCT_PRICE_DECIMAL)
        self.price_str = self.price_whole.content + "." + self.price_decimal.content + "€"
        self.price = float(self.price_str[:-1])

        self.unit           = self.get_element(xpath=PLSL.PRODUCT_UNIT)
        self.unit_price     = self.get_element(xpath=PLSL.PRODUCT_UNIT_PRICE)
        self.unit_price_str = self.unit_price.content.strip()

        self.img            = self.get_element(xpath=PLSL.PRODUCT_IMG)
        self.shelf_name     = self.get_element(xpath=PLSL.PRODUCT_SHELF_NAME)
        self.shelf_href     = self.get_element(xpath=PLSL.PRODUCT_SHELF_HREF)

    def get_details(self):
        return {
            "name" :            self.name_str,
            "price" :           self.price,
            "quantity" :        self.quantity_str,
            "subname" :         self.subname.content,
            "price_whole" :     self.price_whole.content,
            "price_decimal" :   self.price_decimal.content,
            "unit" :            self.unit.content,
            "unit_price" :      self.unit_price_str,
            "img" :             self.img.content,
            "shelf_name" :      self.shelf_name.content,
            "shelf_href" :      self.shelf_href.content
        }

    def get_simple_details(self):
        return {
            "name"  : self.name_str, 
            "price" : self.price_str, 
            "quantity": self.quantity.content
            }

class ProductPage(FoodiePage):

    def __init__(self, response, prev_page=None, next_page=None):
        super(ProductPage, self).__init__(response, prev_page, next_page)
        self.product_list = ListElement(
            page=self, 
            xpath=SRPL.PRODUCT_LIST, 
            elements_xpath=SRPL.PRODUCT_LIST_ELEMENTS,
            element_type=ProductElement
            )
        self.products = self.product_list.get_list()

    def print_products(self, limit):
        if len(self.products) == 0:
            print(f"[PRINT_PRODUCTS]: No products were found on page '{self.response.url}'.")
        else:
            for i, product in enumerate(self.products):
                if i > limit:
                    break
                values = product.get_simple_details()
                print(f"\n{'':<5}Product: {values['name']}")
                print(f"{'':<10}Price: {values['price']}")
                print(f"{'':<10}Quantity: {values['quantity']}")