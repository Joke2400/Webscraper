from .foodie_selectors import (
    ProductListSearchLocators as PLSL,
    StoreListSearchLocators as SLSL
)
from .basic_page_classes import Element


class NavigationElement(Element):

    def __init__(self, source, xpath):
        super().__init__(source, xpath)
        if self.extract(source=self.selector) is not None:
            self.next = self.extract(xpath=SLSL.NAV_NEXT)
            self.prev = self.extract(xpath=SLSL.NAV_PREV)
            self.source.next_page = self.next
            if self.prev.split("&page")[1] != '':
                self.source.prev_page = self.prev


class StoreElement(Element):

    def __init__(self, page, selector):
        super().__init__(page, selector)
        self.store_display_name = self.extract(
            xpath=SLSL.STORE_NAME).strip()
        self.store_name = self.store_display_name.lower()
        self.store_chain = self.store_name.split(" ")[0]

        self.store_select = self.extract(xpath=SLSL.STORE_SELECT)
        self.store_address = self.extract(xpath=SLSL.STORE_ADDRESS)
        self.store_open_times = self.extract(xpath=SLSL.STORE_OPEN_TIMES)

    def fetch_data(self):
        return {
            "chain": self.store_chain,
            "display_name": self.store_display_name,
            "name": self.store_name,
            "select": self.store_select,
            "address": self.store_address,
            "open_times": self.store_open_times
            }

class ProductElement(NestedElement):

    def __init__(self, page, selector):
        super().__init__(page, selector)
        self.name           = self.get_element(xpath=PLSL.PRODUCT_NAME)
        self.ean            = self.get_element(xpath=PLSL.PRODUCT_EAN)
        self.name_str       = self.name.content.strip()
        self.name_match_str = self.name_str.lower()
        
        self.quantity       = self.get_element(xpath=PLSL.PRODUCT_QUANTITY)
        if self.quantity.content is not None:
            self.quantity_str   = self.quantity.content.replace(",", "")
        else:
            self.quantity_str = None

        self.subname        = self.get_element(xpath=PLSL.PRODUCT_SUBNAME)
        
        self.price_whole    = self.get_element(xpath=PLSL.PRODUCT_PRICE_WHOLE)
        self.price_decimal  = self.get_element(xpath=PLSL.PRODUCT_PRICE_DECIMAL)
        if self.price_whole.content is not None:
            self.price_str = self.price_whole.content + "." + self.price_decimal.content + "€"
        elif self.price_decimal.content is not None:
            self.price_str = "." + self.price_decimal.content + "€"
        else:
            self.price_str = None
        self.price = float(self.price_str[:-1]) if self.price_str is not None else None

        self.unit           = self.get_element(xpath=PLSL.PRODUCT_UNIT)
        self.unit_price     = self.get_element(xpath=PLSL.PRODUCT_UNIT_PRICE)
        if self.unit_price.content is not None:
            self.unit_price_str = self.unit_price.content.strip()
        else:
            self.unit_price_str = None

        self.img            = self.get_element(xpath=PLSL.PRODUCT_IMG)
        self.shelf_name     = self.get_element(xpath=PLSL.PRODUCT_SHELF_NAME)
        self.shelf_href     = self.get_element(xpath=PLSL.PRODUCT_SHELF_HREF)

    def get_details(self):
        return {
            "name" :            self.name_str,
            "ean" :             int(self.ean.content),
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
            "unit_price" : self.unit_price_str,
            "quantity": self.quantity.content
            }

