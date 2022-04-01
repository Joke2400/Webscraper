from .basic_selectors import BasicPageSelectors as BPS
from .foodie_selectors import ProductListSearchLocators as PLSL
from .foodie_selectors import SearchResultsPageLocators as SRPL
from .foodie_selectors import StoreListSearchLocators as SLSL
from .page_base_classes import NestedPageElement, Page, PageElement



class ProductPage(Page):
    
    def __init__(self, response, next_page=None, prev_page=None):
        super(ProductPage, self).__init__(response, next_page, prev_page)
        print(self.head)
        print(self.body)

    def fetch_product_list(self):
        self.product_list = ProductList(self, SRPL.PRODUCT_LIST)

class ProductList(PageElement):

    def __init__(self, page, xpath_str):
        super(ProductPage, self).__init__(page, xpath_str)
        self.name = "PRODUCT_LIST"
        self.products = self.get_product_elements()

    def get_product_elements(self):
        product_list = []
        product_selectors = self.fetch_request(
                    selector=self.selector, 
                    xpath_str=SRPL.PRODUCT_LIST_ELEMENTS
                    )
        for selector in product_selectors:
            product_list.append(Product(
                            page=self.page,
                            selector=selector, 
                            xpath_str=SRPL.PRODUCT_LIST_ELEMENTS))
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

class StoreSearchPage(Page):
    pass