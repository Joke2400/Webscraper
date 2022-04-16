from webscraper.utils.descriptors import ListContentValidator, SpecifiedOnlyValidator, SpecifiedOrNoneValidator
from .webber_package.foodie_pageclasses import StoreListPage, FoodiePage, ProductPage
from webscraper.data_manager_package.data_manager import DataManager
from webscraper.data_manager_package.commands import DBStoreRequest
from webscraper.data.urls import FoodieURLs as F_URLS
from .webber_package.spider import BaseSpider

class Webber(BaseSpider):

    name = "Webber"
    
    requested_products  = ListContentValidator(str)
    requested_stores    = ListContentValidator(str)
    limit               = SpecifiedOnlyValidator(int)
    data_manager        = SpecifiedOrNoneValidator(DataManager)
    requesting_old_site = SpecifiedOnlyValidator(bool)
    store_unspecified   = SpecifiedOnlyValidator(bool)

    def __init__(self, *args, **kwargs):
        super(Webber, self).__init__(*args, **kwargs)
        self.requested_products = kwargs.get(
                "requested_products", [])
        self.requested_stores = kwargs.get(
                "requested_stores", [])
        self.limit = kwargs.get(
                "limit")
        self.data_manager = kwargs.get(
                "data_manager")
        self.requesting_old_site = kwargs.get(
                "requesting_old_site", False)
        
        if len(self.requested_products) < 1:
            raise Exception("Webber needs to be provided a product for a query.")
        if len(self.requested_stores) == 0:
            self.store_unspecified = True
        else:
            self.store_unspecified = False
        self.url_source = F_URLS

    def start_requests(self):
        if not self.store_unspecified:
            for i, name in enumerate(self.requested_stores):
                result = self.db_search_store(store_name=name)
                
                if result is not None:
                    result = self.search_store(
                            callback=self.process_store_select,
                            meta={"cookiejar" : i},
                            store_name=name,
                            store_select=result.select
                            )
                    
                    print(f"[start_requests]: Found store {name} locally...")
                    yield result
                else:
                    result = self.search_store(
                        callback=self.process_store_search,
                        meta={"cookiejar" : i},
                        store_name=name
                        )

                    print(f"[start_requests]: Searching for store {name} on (foodie.fi)...")
                    yield result
       
        
        if self.store_unspecified:
            #Call GMapsAPI -> GMaps contains user address -> makes query
            raise NotImplementedError("self.store_unspecified is True")
            
    def db_search_store(self, store_name):
        query_result = self.database_query(DBStoreRequest, name=store_name)
        if 0 < len(query_result) < 2:
            return query_result[0]

        elif len(query_result) > 1:
            raise NotImplementedError("get_local_store_data() yielded more than one result...")
        else:
            return None
  
    def search_store(self, callback, meta, store_name, store_select=None, **kwargs):
        if not isinstance(store_name, str):
            raise ValueError("store_name parameter needs to be of type: (str).")
        kwargs["store_name"] = store_name

        if store_select is not None:
            if isinstance(store_select, str):
                url = self.url_source.base_url + store_select
                tag = "store_select"
        else:
            url = self.url_source.store_search_url + store_name
            tag = "store_search"
        
        request = self.scrape(url=url, callback=callback, meta=meta, tag=tag, **kwargs)
        return request

    def next_page(self, callback, meta, next_button, **kwargs):
        if next_button is None:
            print("[next_page]: Couldn't navigate to the next page, ending search...")
            return None
        
        url = self.url_source.base_url + next_button.replace("/stores?", "/stores/?")
        tag = "next_page"
        
        request = self.scrape(url=url, callback=callback, meta=meta, tag=tag, **kwargs)
        return request

    def search_products(self, callback, meta, product, **kwargs):
        if not isinstance(product, str):
            print("[search_products]: Couldn't navigate to the next page, ending search...")
            return None

        url = f"{self.url_source.product_search_url}{product}"
        tag = "search_products"
        
        request = self.scrape(url=url, callback=callback, meta=meta, tag=tag, **kwargs)

        return request
    
    def get_store_from_list(self, stores, name_str):
        name_str = name_str.strip().lower()  
        store = None
        for store_obj in stores:
            if name_str == store_obj.name_str:
                store = store_obj
                break
        
        return store

    def validate_store(self, selected_name, store_name):
        equal = True if selected_name == store_name.strip().lower() else False
        return equal

    def process_store_search(self, response, **kwargs):
        store_name = kwargs.get("store_name")
        page = self.create_page(response, StoreListPage)
        store = self.get_store_from_list(stores=page.stores, name_str=store_name)
        print(f"[process_store_search]: Found {len(page.stores)} stores in page store list.")

        if store is not None:
            print(f"[process_store_search]: Found store '{store_name}'.")
            request = self.search_store(
                callback=self.process_store_select,
                meta={"cookiejar" : response.meta["cookiejar"]},
                store_select=store.select.content,
                **kwargs
                )
            print(f"[process_store_search]: Selecting store '{store_name}'...")
        else:
            print(f"[process_store_search]: Store '{store_name}' is missing.")
            request = self.next_page(
                callback=self.process_store_search,
                meta={"cookiejar" : response.meta["cookiejar"]},
                next_button=page.next_page, 
                **kwargs
                )
            print(f"[process_store_search]: Navigating to next page...")

        self.export_store_data(page.stores)
        return request

    def process_store_select(self, response, **kwargs):
        store_name = kwargs.get("store_name")
        page = self.create_page(response, FoodiePage)

        if self.validate_store(selected_name=page.topmenu.name_str, 
                                store_name=store_name):
            print(f"[process_store_select]: '{store_name}' is selected on current page.")
            for product in self.requested_products:
                request = self.search_products(
                    callback=self.process_product_search,
                    meta={"cookiejar" : response.meta["cookiejar"]},
                    product=product,
                    **kwargs
                    )
                print(f"[process_store_select]: Searching for product: '{product}'.")
                yield request
        else:
            print(f"[process_store_select]: '{store_name}' is not selected on current page.")
            raise NotImplementedError("get_store_from_page() returned None")

    def process_product_search(self, response, **kwargs):
        store_name = kwargs.get("store_name")
        page = self.create_page(response, ProductPage)
        
        if self.validate_store(selected_name=page.topmenu.name_str, 
                        store_name=store_name):
            page.print_products(limit=self.limit)
        else:
            print(f"[process_store_select]: '{store_name}' is not selected on current page.")
            raise NotImplementedError("get_store_from_page() returned None")

    def export_product_data(self):
        print("-EXPORT PRODUCT DATA-")

    def export_store_data(self, stores):
        print("-EXPORT STORE DATA-")