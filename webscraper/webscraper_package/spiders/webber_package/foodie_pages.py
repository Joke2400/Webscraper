from .foodie_selectors import SearchResultsPageLocators as SRPL
from .foodie_selectors import StoreListSearchLocators as SLSL
from .basic_page_classes import Page, Element, ListElement
from .foodie_page_elements import (
    NavigationElement,
    StoreElement,
    ProductElement
)


class FoodiePage(Page):

    def __init__(self, response, prev_page=None, next_page=None):
        super().__init__(response, prev_page, next_page)
        self.topmenu = Element(
            source=self,
            xpath=SRPL.STORES_TOPMENU)
        self.get_topmenu_store()

    def get_topmenu_store(self):
        self.store_display_name = self.topmenu.extract(
            xpath=SRPL.STORE_NAME).strip()
        self.store_name = self.store_display_name.lower()

        self.store_href = self.topmenu.extract(
            xpath=SRPL.STORE_HREF)
        self.store_address = self.topmenu.extract(
            xpath=SRPL.STORE_ADDRESS)
        self.store_open_times = self.topmenu.extract(
            xpath=SRPL.STORE_OPEN_TIMES)


class StoreListPage(FoodiePage):

    def __init__(self, response, prev_page=None, next_page=None):
        super().__init__(response, prev_page, next_page)
        self.navigation = NavigationElement(
            source=self,
            xpath=SLSL.NAVIGATION_BUTTONS)
        self.store_list = ListElement(
            source=self,
            xpath=SLSL.STORE_LIST,
            items_xpath=SLSL.STORE_LIST_ELEMENTS,
            element_type=StoreElement)
        self.stores = self.store_list.get_list()


class ProductPage(FoodiePage):

    def __init__(self, response, prev_page=None, next_page=None):
        super().__init__(response, prev_page, next_page)
        self.product_list = ListElement(
            source=self,
            xpath=SRPL.PRODUCT_LIST,
            items_xpath=SRPL.PRODUCT_LIST_ELEMENTS,
            element_type=ProductElement)
        self.products = self.product_list.get_list()

    def print_products(self, limit=5, condensed=False):
        if len(self.products) != 0:
            print("\n")
            for i, product in enumerate(self.products):
                if i > limit:
                    break
                if condensed:
                    self.print_details_condensed(product=product)
                else:
                    self.print_details(product=product)
        else:
            print(
                "[PRINT_PRODUCTS]: No products were found on page:",
                f"'{self.response.url}'")
        print("\n")



    def print_details(self, product):
        values = product.get_simple_details()
        print(f"\n{'':<5}Product: {values['name']}")
        print(f"{'':<10}Price: {values['price']}")
        print(f"{'':<10}Quantity: {values['quantity']}")

    def print_details_condensed(self, product):
        values = product.get_simple_details()
        if values["price"] is None:  # I am a lazy piece of shit :)
            values["price"] = ""
        if values["quantity"] is None:  # I am a lazy piece of shit :)
            values["quantity"] = ""
        if values["unit_price"] is None:  # I am a lazy piece of shit :)
            values["unit_price"] = ""
        print(f"[Product]: {values['name'] : ^70} Price: {values['price']  : <10} Quantity: {values['quantity'] : <5} Price/Unit: {values['unit_price'] : <5}")

    def print_products(self, limit, condensed=False):
        if len(self.products) == 0:
            print(f"[PRINT_PRODUCTS]: No products were found on page '{self.response.url}'.")
        else:
            print("\n")
            for i, product in enumerate(self.products):
                if i > limit:
                    break
                if condensed:
                    self.print_details_condensed(product=product)
                else:
                    self.print_details(product=product)
            print("\n")