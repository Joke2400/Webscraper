from webscraper.utils.descriptors import ListContentValidator, SpecifiedOnlyValidator, SpecifiedOrNoneValidator
from .webber_package.foodie_pageclasses import StoreListPage, FoodiePage
from webscraper.data_manager_package.data_manager import DataManager
from webscraper.data_manager_package.commands import DBStoreRequest
from webscraper.data.urls import FoodieURLs as F_URLS
from .webber_package.base_spider import BaseSpider
import datetime

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
        self.url_source = F_URLS

    def print_response(self, callback):
        def wrapper(response, **kwargs):
            #Time calculation
            end_time = datetime.datetime.now()
            start_time = kwargs.get("start_time")
            duration = end_time - start_time
            duration_str = f"{duration.seconds}s {int(str(duration.microseconds)[:3])}ms"
            self.response_times.append(duration)

            store_name = kwargs.get("store_name")
            tag = kwargs.get("tag", "")
            del kwargs["tag"]
            if response is not None:
                print(f"\n[RECEIVED RESPONSE]: '{response.status}' from IP: '{response.ip_address}' (Took: {duration_str}).\
                    \n[{tag}]: Searched for '{store_name}', using '{response.url}'.")
            return callback(response, **kwargs)
        return wrapper

    def start_requests(self):
        if not self.store_unspecified:
            for store_str in self.requested_stores:
                result = self.db_search_store(
                    store_name=store_str, 
                    callback=self.search_products
                    )
                if result is not None:
                    print(f"[START_REQUESTS]: Found store {result.cb_kwargs['store_name']} locally...")
                    yield result
                else:
                    result = self.search_store(
                        store_name=store_str, 
                        callback=self.process_store_search
                        )
                    print(f"[START_REQUESTS]: Searching for store {result.cb_kwargs['store_name']} on (foodie.fi)...")
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
            kwargs["tag"] = "STORE_SELECT"
            request = self.scrape_page(url, callback, **kwargs)
            return request
        else:
            raise Exception("select_store() needs to be provided a search parameter")

    def search_store(self, store_name, callback=None, **kwargs):
        if store_name is not None:
            url = self.url_source.store_search_url + store_name
            if callback is None:
                callback = self.process_store_search
            kwargs["tag"] = "STORE_SEARCH"
            kwargs["store_name"] = store_name
            request = self.scrape_page(url, callback, **kwargs)
            return request
        else:
            raise Exception("store_search() needs to be provided a search parameter")

    def process_store_search(self, response, **kwargs):
        page = self.create_page(response, StoreListPage)
        page.get_store_list()
        print(f"[PROCESS_STORE_SEARCH]: Found {len(page.stores)} stores in page store list.")
        store_name = kwargs.get("store_name")
        store = self.validate_store(stores=page.stores, store_name=store_name)

        if store is None:
            print(f"[PROCESS_STORE_SEARCH]: Navigating to next page...")
            next_button = page.next_page
            if next_button is None:
                print("[PROCESS_STORE_SEARCH]: Couldn't navigate to the next page, ending search...")
                return None

            url = self.url_source.base_url + next_button.replace("/stores?", "/stores/?")
            callback = self.process_store_search
            kwargs["tag"] = "NEXT_PAGE"
            request = self.scrape_page(url, callback, **kwargs)
        else:
            print(f"[PROCESS_STORE_SEARCH]: Selecting store '{store_name}'...")
            request = self.select_store(
                store_select=store.select.content,
                callback=self.search_products,
                store_name=store.name.content
                )

        self.export_store_data(page.stores)
        return request

    def validate_store(self, stores, store_name):
        store_object = None
        store_match = store_name.strip().lower()
        for store in stores:
            if store_match == store.name_str:
                store_object = store
                print(f"[VALIDATE_STORE]: Found store '{store_name}'.")
                break
        if store_object is None:
            print(f"[VALIDATE_STORE]: Store '{store_name}' is missing.")
        return store_object

    def search_products(self, response, **kwargs):
        page = self.create_page(response, FoodiePage)
        selected_store = page.topmenu
        store_name = kwargs.get("store_name")
        store = self.validate_store(stores=[selected_store], store_name=store_name)
        
        if store is not None:
            for product in self.requested_products:
                url = f"{self.url_source.product_search_url}{product}"
                callback = self.process_product_search
                kwargs["tag"] = "PRODUCT_SEARCH"
                request = self.scrape_page(url, callback, **kwargs)
                yield request
        else:
            raise NotImplementedError("validate_store() returned False")
            #Check if saved_pages has a page with the correct url

    def process_product_search(self, response, **kwargs):
        print("-PROCESS PRODUCT SEARCH-")

    def export_product_data(self):
        print("-EXPORT PRODUCT DATA-")


    def export_store_data(self, stores):
        print("-EXPORT STORE DATA-")


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