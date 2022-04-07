from .basic_selectors import BasicPageSelectors as BPS
from .foodie_selectors import ProductListSearchLocators as PLSL
from .foodie_selectors import SearchResultsPageLocators as SRPL
from .foodie_selectors import StoreListSearchLocators as SLSL
from .page_base_classes import NestedPageElement, Page, PageElement
from webscraper.data.filepaths import FilePaths

class StoreSearchPage(Page):

    def __init__(self, response, next_page=None, prev_page=None):
        super(StoreSearchPage, self).__init__(response, next_page, prev_page)
        self.store_list = None
        self.next = None

    #Forcing the need for a function to be called for the rest of the objects to
    #be created is meant to speed up the request phase. get_store_list() should 
    #therefore only be called once items are to be sent to the pipeline
    def get_store_list(self):
        if not isinstance(self.store_list, StoreList):
            self.store_list = StoreList(page=self, xpath=SLSL.STORE_LIST)
        return self.store_list

    def get_stores(self):
        self.get_store_list()
        stores = self.store_list.get_stores()
        return stores

    def get_next_button(self):
        if not isinstance(self.next, PageElement):
            self.next = PageElement(page=self, xpath=SLSL.STORE_LIST_NEXT_BUTTON)
        return self.next

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
            content_list = self.get_element(xpath=SLSL.STORE_LIST_ELEMENTS)[1]
            for selector_content in content_list:
                self.stores.append(StoreElement(
                                page=self.page, 
                                selector_content=selector_content))
        return self.stores
    
    def reset_stores(self):
        self.stores = None

class StoreElement(NestedPageElement):

    def __init__(self, page, selector_content):
        super(StoreElement, self).__init__(page, selector_content)   
        self.store_details = {}

    def get_store_details(self):
        self.store_details["NAME"]      = self.get_name()
        self.store_details["ADDRESS"]   = self.get_address()
        self.store_details["SELECT"]    = self.get_select()
        return self.store_details

    def get_name(self):
        value = self.get_element(xpath=SLSL.STORE_NAME)[1]
        if len(value) > 1:
            raise Exception("Selector returned multiple values when only one was expected.")
        return value[0]

    def get_address(self):
        value = self.get_element(xpath=SLSL.STORE_ADDRESS)[1]
        if len(value) > 1:
            raise Exception("Selector returned multiple values when only one was expected.")
        return value[0]

    def get_select(self):
        value = self.get_element(xpath=SLSL.STORE_SELECT_BUTTON )[1]
        if len(value) > 1:
            raise Exception("Selector returned multiple values when only one was expected.")
        return value[0]
class StorePage(Page):

    def __init__(self, response, next_page=None, prev_page=None):
        super(StorePage, self).__init__(response, next_page, prev_page)
        self.topmenu = None

    def get_store(self):
        if not isinstance(self.topmenu, StoreTopmenu):
            content = self.response.xpath(SRPL.STORES_TOPMENU).getall()[0]
            with open(FilePaths.response_path, 'w') as file:
                file.write(content)
            self.topmenu = StoreTopmenu(page=self, xpath=SRPL.STORES_TOPMENU)
        return self.topmenu

class StoreTopmenu(PageElement):

    def __init__(self, page, xpath):
        super(StoreTopmenu, self).__init__(page, xpath) 


        self.name =     NestedPageElement(self.page, self.content[0]).get_element(xpath=SRPL.STORE_NAME)[1]
        self.href =     NestedPageElement(self.page, self.content[0]).get_element(xpath=SRPL.STORE_HREF)[1]  
        self.address =  NestedPageElement(self.page, self.content[0]).get_element(xpath=SRPL.STORE_ADDRESS)[1]
        self.open_times = NestedPageElement(self.page, self.content[0]).get_element(xpath=SRPL.STORE_OPEN_TIMES )[1]




















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
'''