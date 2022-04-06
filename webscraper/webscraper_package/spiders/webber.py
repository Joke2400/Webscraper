from webscraper.utils.descriptors import ListContentValidator, SpecifiedOnlyValidator, SpecifiedOrNoneValidator
from webscraper.data.urls import FoodieURLs as F_URLS, SkaupatURLs as S_URLS
from webscraper.data_manager_package.data_manager import DataManager
from webscraper.data_manager_package.commands import DBStoreChainRequest, DBStoreRequest, DBStoreProductRequest

from .webber_package.foodie_page_classes import StoreSearchPage
from .webber_package.foodie_selectors import ProductListSearchLocators as PLSL
from .webber_package.foodie_selectors import SearchResultsPageLocators as SRPL
from .webber_package.foodie_selectors import StoreListSearchLocators as SLSL
from .webber_package.base_spider import BaseSpider


#Site-specific scraper, will initially be built specifially for s-kaupat.fi/foodie.fi.
class Webber(BaseSpider):

    name = "Webber"
    
    requested_products  = ListContentValidator(str)
    requested_stores    = ListContentValidator(str)
    data_manager        = SpecifiedOrNoneValidator(DataManager)
    requesting_old_site = SpecifiedOnlyValidator(bool)
    store_unspecified   = SpecifiedOnlyValidator(bool)

    def __init__(self, *args, **kwargs):
        super(Webber, self).__init__(*args, **kwargs)
        self.requested_products = kwargs.get(
                "requested_products", [])
        self.requested_stores = kwargs.get(
                "requested_stores", [])
        self.data_manager = kwargs.get(
                "data_manager", None)
        self.requesting_old_site = kwargs.get(
                "requesting_old_site", False)
        
        if len(self.requested_products) < 1:
            raise Exception("Webber needs to be provided a product for a query.")
        if len(self.requested_stores) == 0:
            self.store_unspecified = True
        else:
            self.store_unspecified = False
        
        #Lazy implementation, temporary
        if self.requesting_old_site:
            self.url_source = F_URLS
            self.selector_source = (PLSL, SRPL, SLSL) 
        else:
            self.url_source= S_URLS
            self.selector_source = None

    def start_requests(self):
        if not self.store_unspecified:
            for store_str in self.requested_stores:
                result = self.db_search_store(
                        store_name=store_str, 
                        callback=self.search_products
                        )
                if result is not None:
                    yield result
                else:
                    result = self.search_store(
                        store_name=store_str, 
                        callback=self.process_store_search
                        )
                    yield result
        else:
            pass
            #Call GMapsAPI -> GMaps contains user address -> makes query
            
    def db_search_store(self, store_name, callback=None):
        query_result = self.database_query(DBStoreRequest, name=store_name)
        if 0 < len(query_result) < 2:
            if callback is None:
                callback = self.search_products
            store = query_result[0]
            request = self.select_store(
                store_select=store.select,
                callback=callback,
                store_name=store_name
                )
            return request
        elif len(query_result) > 1:
            raise NotImplementedError("get_local_store_data() yielded more than one result...")
        else:
            return None
  
    def select_store(self, store_select=None, callback=None, **kwargs):
        if store_select is not None:
            url = self.url_source.base_url + store_select
            if callback is None:
                callback = self.search_products
            request = self.scrape_page(url, callback, **kwargs)
            return request
        else:
            raise Exception("select_store() needs to be provided a search parameter")

    def search_store(self, store_name, callback=None, **kwargs):
        if store_name is not None:
            url = self.url_source.store_search_url + store_name
            if callback is None:
                callback = self.process_store_search
            kwargs["store_name"] = store_name
            request = self.scrape_page(url, callback, **kwargs)
            return request
        else:
            raise Exception("store_search() needs to be provided a search parameter")

    def process_store_search(self, response, **kwargs):
        page = self.create_page(response, StoreSearchPage)
        requested_store = kwargs.get("store_name")
        stores = page.get_stores()
        store_obj = None
        for store in stores:
            if store.get_name() == requested_store:
                store_obj = store
                break

        if store_obj is None:
            next_button = page.get_next_button()
            url = self.url_source.base_url + next_button.replace("/stores?", "/stores/?")
            callback = self.process_store_search
            request = self.scrape_page(url, callback, **kwargs)
        else:
            request = self.select_store(
                store_select=store_obj.select,
                callback=self.search_product,
                store_name=store_obj.get_name()
                )

        self.export_store_data(stores)
        return request

    def validate_store(self, page, store_name):
        store = page.get_store()
        if store.get_name().strip().lower() == store_name.strip().lower():
            return True
        else:
            return False

    def search_products(self, response, **kwargs):
        page = self.create_page(response, StorePage)
        store_name = kwargs.get("store_name")
        if self.validate_store(page, store_name):
            for product in self.requested_products:
                url = f"{self.URL_SOURCE.product_search_url}{product.name}"
                callback = self.process_product_search
                request = self.scrape_page(url, callback, kwargs)
                yield request
        else:
            raise NotImplementedError("get_products() validation failed")
            #Check if saved_pages has a page with the correct url

    def process_product_search(self, response, **kwargs):
        page = self.create_page(response, ProductPage)
        validation = self.validate_store(page)


    def export_product_data(self):
        pass

    def export_store_data(self):
        pass

'''

Lets make some assumptions:
    By the time Webber starts doing his diligent spidery work:

        One of the stores or products requested by the user cant be found locally
                        (or both)

        if it's relevant to the search, user location will have been fetched:
            -> This is the most common scenario
            -> WEBBER CAN IGNORE LOCATION ENTIRELY

        Product and store data will already have been queried from the database:
            -> Product records that are up to date and accurate will have
                been pruned from webbers search list

        All relevant store data will be known already:
            -> True:
                -> Webber only needs to search the stores for products

            -> False:
                -> Webber has to first find the relevant stores

General/Initial webber flow:
    -> init

        - Store found locally
            -> Scrape website for products using webpage search
            -> Send scraped product data to Data Manager

        -> No store found locally
            -> Scrape website for stores using webpage search
            -> Increment pages until result is found
                -> Send all encountered store data to Data Manager
            -> Scrape website for products using webpage search
            -> Send scraped product data to Data Manager



Spider params ->
    product_search    | lst, tup | (Required) |
    
    Leaving either of the following empty -> Any store will be used,
        or closest store will be used...

    store_name        | lst, tup       | (Optional) | 
    store_object      | href(str), obj | (Optional) | 
        | Implement as secondary search method,     |
        | ex. If stores exist in database           |

Core functionality ->

    Spider ->
        Locations ->
            Locations are handled elsewhere, 
            scraper should be able to ask for a location however

        Search ->
            Scraper should be able to scrape a specific website secondhand

        Data management ->
            Asking Data manager for store data
            Sending store and product data Data manager


Webber requirements

Generalisation

* classes for pages
* classes for key page elements

Optimization

* No more repeated recursive functions like the last one -_-


'''