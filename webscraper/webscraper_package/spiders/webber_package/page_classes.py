from .basic_selectors import BasicPageSelectors as BPS
from .foodie_selectors import ProductListSearchLocators as PLSL
from .foodie_selectors import SearchResultsPageLocators as SRPL
from .foodie_selectors import StoreListSearchLocators as SLSL
from .page_base_classes import NestedPageElement, Page, PageElement

class StoreSearchPage(Page):

    def __init__(self, response, next_page=None, prev_page=None):
        super(StoreSearchPage, self).__init__(response, next_page, prev_page)
        self.store_list = None
        self.navigation = None

    #Forcing the need for a function to be called for the rest of the objects to
    #be created is meant to speed up the request phase. get_store_list() should 
    #therefore only be called once items are to be sent to the pipeline
    def get_store_list(self):
        if not isinstance(self.store_list, StoreList):
            self.store_list = StoreList(self, SLSL.STORE_LIST)
        return self.store_list

    def get_stores(self):
        self.get_store_list()
        stores = self.store_list.get_stores()
        return stores

    def get_navigation(self):
        if not isinstance(self.navigation, PageElement):
            self.navigation= PageElement(page=self, xpath=SLSL.NAVIGATION_BUTTONS, name="NAVIGATION" )
        return self.navigation

    def reset_store_list(self):
        self.store_list = None

class StoreList(PageElement):

    def __init__(self, page, xpath):
        super(StoreList, self).__init__(page, xpath)
        self.name = "STORE_LIST"
        self.stores = None
        
    def get_stores(self):
        if not isinstance(self.stores, list):
            self.stores = []
            selector_list = self.get_element(xpath=SLSL.STORE_LIST_ELEMENTS)[1]
            for selector in selector_list:
                self.stores.append(StoreElement(
                                page=self.page, 
                                store_selector=selector))
        return self.stores
    
    def reset_stores(self):
        self.stores = None

class StoreElement(NestedPageElement):

    def __init__(self, page, store_selector):
        super(StoreElement, self).__init__(page, store_selector)   
        self.store_details = {}

    def get_store_details(self):
        self.store_details["NAME"]    = self.get_selector_content(xpath=SLSL.STORE_NAME)
        self.store_details["ADDRESS"] = self.get_selector_content(xpath=SLSL.STORE_ADDRESS)
        self.store_details["HREF"]    = self.get_selector_content(xpath=SLSL.STORE_HREF)
        self.store_details["SELECT"]  = self.get_selector_content(xpath=SLSL.STORE_SELECT_BUTTON)

        return self.store_details



'''
class ProductPage(Page):
    
    def __init__(self, response, next_page=None, prev_page=None):
        super(ProductPage, self).__init__(response, next_page, prev_page)
        self.product_list = None

    def get_product_list(self):
        if not isinstance(self.product_list, ProductList):
            self.product_list = ProductList(self, SRPL.PRODUCT_LIST)
        return self.product_list

class ProductList(PageElement):

    def __init__(self, page, xpath):
        super(ProductList, self).__init__(page, xpath)
        self.name = "PRODUCT_LIST"
        self.products = self.fetch_product_elements()

    def fetch_product_elements(self):
        product_list = []
        product_selectors = self.fetch_request(
                    selector=self.selector, 
                    xpath_str=SRPL.PRODUCT_LIST_ELEMENTS
                    )
        for selector in product_selectors:
            product_list.append(Product(
                            page=self.page,
                            selector=selector, 
                            xpath=SRPL.PRODUCT_LIST_ELEMENTS))
        return product_list

class Product(NestedPageElement):

    def __init__(self, page, selector):
        self.page = page
        self.selector = selector
        self.fetch_product_details()
        
    def fetch_product_details(self):
        self.product_details = self.fetch_element(page=self.page, xpath=SRPL.PRODUCT_DETAILS)

class StorePage(Page):
    pass
'''