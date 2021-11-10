import scrapy
from .foodie_package.locators import SearchResultsPageLocators as SRPL
from .foodie_package.locators import ProductListSearchLocators as PLSL
from .foodie_package.locators import StoreListSearchLocators as SLSL
from .foodie_package.urls import FoodieURLS as URLS
from ...data.helper_functions import fetch_local_data2, prepare_search_string, unpack_nested_strings, check_consistency, lower_iterable
from ...data.fpaths import FilePaths
from ..items import FoodieStoreItem, FoodieProductItem
from datetime import datetime
import json

class FoodieSpider(scrapy.Spider):
    '''
    A scrapy.Spider specifically designed to crawl foodie.fi using a provided product query.
    Can accept a list of products, however the spider is only designed to search for a single store
    scraper_manager.SearchManager can instead be called in the project root dir to search for products in several stores

    Params:
        product_search    | str, lst, tup | (Required) |
        store_name        | str           | (Optional) | 
        store_href        | str           | (Optional) | 
        ignore_store_data | bool          | (Optional) | 
    '''
    name = 'Foodie Spider'

    def __init__(self, *args, **kwargs):
        super(FoodieSpider, self).__init__(*args, **kwargs)
        self.validation_subjects = []
        self.session_verified_stores = []
        self.session_refuted_stores = []
        self.scraped_products = []
        self.stores = []
        self.local_store_object = None
        self.name_search_performed = False
        self.href_search_performed = False
        self.local_store_search_performed = False
        self.complete_search_performed = False
        self.perform_dual_validation = False
        self.yield_local_data = False

        self.store_name = kwargs.get("store_name", None)
        self.store_name = self.store_name.lower() if isinstance(self.store_name, str) else None

        self.store_href = kwargs.get("store_href", None)
        self.store_href = self.store_href.lower() if isinstance(self.store_href, str) else None

        self.ignore_store_data = kwargs.get("ignore_store_data", False)
        self.ignore_store_data = False if not isinstance(self.ignore_store_data, bool) else self.ignore_store_data
        
        self.product_query = kwargs.get("product_search", None)
        if not isinstance(self.product_query, str):
            if isinstance(self.product_query, tuple) or isinstance(self.product_query, list):
                try:
                    self.product_query = [str(i) for i in self.product_query]
                except:
                    raise Exception("[ERROR]: Could not convert search query to a list of strings")
            else:
                raise TypeError("[ERROR]: product_search parameter is mandatory and must be one of the following types: str, tuple, list")

        self.store_query_dict = {"NAME" : self.store_name, "HREF" : self.store_href}

        if self.store_name is None and self.store_href is None:
            self.ignore_store_data = True
            print("[INTERNAL]: Neither a store name or a href has been provided, assuming the user wants to ignore which store is to be searched...")

        if not self.ignore_store_data:
            self.process_local_store_data()

    def process_local_store_data(self):
        self.stores_json = fetch_local_data2(FilePaths.stores_path, "stores")
        #Issue when using this as a generator, json.load loads the entire file     

        if len(self.stores_json["stores"]) > 0:
            for store in self.stores_json["stores"]:
                item = self.create_store_item(store)
                self.filter_store_appendables(item)
        del self.stores_json

    def filter_store_appendables(self, store):
        in_list = False
        for item in self.stores:
            if item["NAME"].lower() == store["NAME"].lower():
                in_list = True
                break
        if not in_list:
            self.stores.append(store)

    def create_store_item(self, store_dict):
        item = FoodieStoreItem()

        for key, value in store_dict.items():
            if isinstance(value, str):
                store_dict[key] = value.lower()

        item["NAME"] = store_dict["NAME"]
        item["HREF"] = store_dict["HREF"]
        item["ADDRESS"]= store_dict["ADDRESS"]
        item["DATE_ADDED"] = store_dict["DATE_ADDED"]
        item["LAST_UPDATED"] = store_dict["LAST_UPDATED"]
        item["OPEN_TIMES"] = store_dict["OPEN_TIMES"]
        item["SELECT"] = store_dict["SELECT"]
        item["LOCATION"] = store_dict["LOCATION"]
        return item

    def start_requests(self):
        '''
        By default scrapy will start by asking this function for a scrapy.Request()
        This function could be used to launch other smaller operations such as only running a store search, or manually updating the store list
        '''
        if self.ignore_store_data:
            request_data = scrapy.Request(url=URLS.PAGE_BASE_URL, callback=self.schedule_requests)
        else:
            request_data = self.perform_search_by_local_data()
            request_data = scrapy.Request(url=request_data["URL"], callback=request_data["CALLBACK"])

        return [request_data] #So scrapy requires that the return value of this function is an iterable, but apparently it only wants a list, and not a tuple??

    def schedule_requests(self, response):
        #Search precedence... -> [Local Data (SEARCH BY HREF, SEARCH BY NAME)] -> [GET request (utilizing provided name)]
        check = self.check_store_info(response)
        if check["SPECIFY"] != "NEITHER" or self.ignore_store_data:
            if check["SPECIFY"] == "BOTH":
                request_data = self.perform_product_search(response)
                for request in request_data:
                    yield scrapy.Request(url=request["URL"], callback=request["CALLBACK"], dont_filter=True)
                return

            if check["SPECIFY"] == "FIRST" and (self.store_href is None or self.local_store_search_performed) or check["SPECIFY"] == "SECOND" and self.store_name is None:
                request_data = self.perform_product_search(response)
                for request in request_data:
                    yield scrapy.Request(url=request["URL"], callback=request["CALLBACK"], dont_filter=True)
                return #<-- To me this feels like a strange thing to do, but it works

            print("[INTERNAL]: Store data check confirmed a value was correct on the current page,\nhowever one of the conditions failed, completing internal checks...")
            
        if not self.local_store_search_performed:
            request_data = self.perform_search_by_local_data()
            yield scrapy.Request(url=request_data["URL"], callback=request_data["CALLBACK"])
           
        elif not self.complete_search_performed:
            if URLS.STORE_SEARH_BASE_URL not in response.url:
                request_data = self.query_website_for_store()
            else:
                request_data = self.query_website_for_store(response)
                yield scrapy.Request(url=request_data["URL"], callback=request_data["CALLBACK"], dont_filter=True)

        else:
            raise Exception("[ERROR]: Could not find the correct store based on provided and local data.")
            
    def perform_product_search(self, response):
        print("[INTERNAL]: Performing product search...\n")
        if not self.ignore_store_data:
            self.fill_store_fields(response)
            self.save_store_data()

        if type(self.product_query) is str:
            if self.product_query is not None:
                search = {"URL" : prepare_search_string(URLS.PRODUCT_SEARH_BASE_URL, self.product_query), "CALLBACK" : self.process_product_search}
                return [search]
            else:
                raise TypeError("[ERROR]: Attempted to perform website search but search query was of type: 'None'")           
        
        elif isinstance(self.product_query, tuple) or isinstance(self.product_query, list):
            if self.product_query is not None:
                search_list = []
                for item in self.product_query:
                    search = {"URL" : prepare_search_string(URLS.PRODUCT_SEARH_BASE_URL, item), "CALLBACK" : self.process_product_search}
                    search_list.append(search)
                return search_list
            else:                               
                raise TypeError("Attempted to perform website search but search query was of type: 'None'")        

        else:
            raise TypeError(f"[ERROR]: Attempted to perform a website search. Query is of type: {type(self.product_query)}, must be of the following types: str, tuple, list")

    def check_store_info(self, response):
        self.store_data = {
            "NAME" : response.xpath(unpack_nested_strings(SRPL.STORE_NAME)).get(), 
            "HREF" : response.xpath(unpack_nested_strings(SRPL.STORE_HREF)).get().replace("/store/", "")
            } #ADD ADDRESS HERE
            #Might want to call a function to check if store address is not in local file and add it...
        provided_tuple = (self.store_name, self.store_href) if not self.store_name is None else ("", self.store_href)
        response_tuple = self.store_data["NAME"], self.store_data["HREF"]
        
        consistency = check_consistency(provided_tuple, response_tuple)
        consistent_name = True if consistency["RESULT"] or consistency["SPECIFY"] == "FIRST" else False
        consistent_href = True if consistency["RESULT"] or consistency["SPECIFY"] ==  "SECOND" else False
        
        print(f"\n[CURRENT STORE]: STORE NAME: '{self.store_data['NAME']}' | STORE HREF: '{self.store_data['HREF']}'")
                                                     
        affirmative = lambda x, response, provided: print(f'[{x} CHECK]: {response} is consistent with search: {provided}')
        negative = lambda x, response, provided: print(f'[{x} CHECK]: {response} is not consistent with search: {provided}')

        if consistent_name:
            affirmative("NAME", self.store_data["NAME"], self.store_name.title())
        else:
            if self.store_name is not None:
                negative("NAME", self.store_data["NAME"], self.store_name.title())
            else:
                negative("NAME", self.store_data["NAME"], "None")

        if consistent_href:
            affirmative("HREF", self.store_data["HREF"], self.store_href)
        else:
            if self.store_href is not None:
                negative("HREF", self.store_data["HREF"], self.store_href)
            else:
                negative("HREF", self.store_data["HREF"], "None")        
    
        return consistency

    def perform_search_by_local_data(self):
        self.yield_local_data = False
        
        if not self.href_search_performed:
            self.href_search_performed = True
            print("[INTERNAL]: Performing local data search by href...")
            params = (self.store_href, self.store_name) if self.store_name is not None else (self.store_href, None)
            search_url = self.perform_local_search_by(params, "HREF")
            if self.yield_local_data == True:
                return search_url
        
        if not self.name_search_performed:
            self.name_search_performed = True
            print("[INTERNAL]: Performing local data search by name...")
            params = (self.store_name, self.store_href) if self.store_href is not None else (self.store_name, None)
            search_url = self.perform_local_search_by(params, "NAME")
            if self.yield_local_data == True:
                return search_url

        if self.href_search_performed and self.name_search_performed:
            self.local_store_search_performed = True
            print("[INTERNAL]: Local data search failed, querying website for store using available data...")
            search_url = self.query_website_for_store()
            return search_url

    def perform_local_search_by(self, values, search_type):
        value = values[0]                                               
        compare_value = values[1]
        search_url = None

        if value is not None:
            for store in self.stores:
                if value in store.values():
                    self.local_store_object = store
                    break
            
            if compare_value is not None:
                if self.local_store_object is not None:
                    provided_tuple = self.store_query_dict["NAME"], self.store_query_dict["HREF"]
                    local_tuple = self.local_store_object["NAME"], self.local_store_object["HREF"]
                    search_url = self.local_data_consistency_check(provided_tuple, local_tuple, search_type)
            
            if search_type == "HREF":
                if self.store_name is None:
                    search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, self.store_href), "CALLBACK" : self.schedule_requests}
            if search_type == "NAME":
                if self.store_href is None:
                    if self.local_store_object is not None:
                        if self.local_store_object["HREF"] is not None:
                            search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, self.local_store_object["HREF"]), "CALLBACK" : self.schedule_requests}

            if search_url is not None:
                self.yield_local_data = True
            return search_url

        return search_url

    def local_data_consistency_check(self, provided_tuple, local_tuple, search_type=None):
        consistency = check_consistency(provided_tuple, local_tuple)
        if not consistency["RESULT"]:
            self.validation_subjects.append({"NAME" : provided_tuple[0], "HREF" : provided_tuple[1],  "TYPE" : "PROVIDED_DATA"})
            self.validation_subjects.append({"NAME" : local_tuple[0], "HREF" : provided_tuple[1],     "TYPE" : "LOCAL_DATA"})
        else:
            print("[INTERNAL]: Consistency check was successful. Proceeding to fetch website...")
            search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, provided_tuple[1]), "CALLBACK" : self.schedule_requests}
            return search_url
        
        if consistency["SPECIFY"] == "SECOND":
            search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, provided_tuple[1]), "CALLBACK" : self.validation_check}
        elif consistency["SPECIFY"] == "FIRST":
            if search_type == "NAME":
                self.perform_dual_validation = True
                search_url = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, local_tuple[1]), "CALLBACK" : self.validation_check}
        else:
            raise Exception("[INTERNAL]: Consistency check during local search returned: (False, 'NEITHER'), this should not be possible during normal operation.")

        return search_url 

    def validation_check(self, response):
        check= self.check_store_info(response)
        if check["RESULT"]:
            self.sort_validation_results()
            self.evaluate_validation_results(response)
            self.validation_subjects = []
            request_data = self.perform_product_search(response)
            return scrapy.Request(url=request_data["URL"], callback=request_data["CALLBACK"])
    
        if self.perform_dual_validation:
            for item in self.validation_subjects:
                if item["TYPE"] == "PROVIDED_DATA":
                    self.sort_validation_results()
                    self.perform_dual_validation = False
                    request_data = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, item["HREF"]), "CALLBACK" : self.validation_check}
                    return scrapy.Request(url=request_data["URL"], callback=request_data["CALLBACK"], dont_filter=True)
        else:
            self.sort_validation_results()
            self.evaluate_validation_results(response)
            self.validation_subjects = []
            for refuted_item in self.session_refuted_stores:
                self.delete_store_data(store_dict=refuted_item)
            self.local_store_search_performed = True
            request_data = self.query_website_for_store()
            return scrapy.Request(url=request_data["URL"], callback=request_data["CALLBACK"])

    def sort_validation_results(self):
        for item in self.validation_subjects:
            item_tuple = item["NAME"], item["HREF"]
            response_tuple = self.store_data["NAME"], self.store_data["HREF"]
            if lower_iterable(item_tuple) == lower_iterable(response_tuple):
                self.session_verified_stores.append(item)
            else:
                if not self.perform_dual_validation:
                    self.session_refuted_stores.append(item)

    def evaluate_validation_results(self, response):
        self.session_verified_stores = [dict(t) for t in {tuple(d.items()) for d in self.session_verified_stores}]
                                        #This even needed? I mean validation shouldn't be creating duplicates anyway?
                                        #Nvm it does, and it doesn't even work like i want it to..

        for item in self.session_verified_stores:
            if item["TYPE"] == "PROVIDED_DATA":
                if self.store_query_dict["NAME"] == item["NAME"] and self.store_query_dict["HREF"] == item["HREF"]:
                    store_dict = self.store_query_dict
                    now = datetime.now()
                    store_dict["DATE_ADDED"]    = now.strftime("%d/%m/%Y %H:%M:%S")
                    store_dict["LAST_UPDATED"]  = now.strftime("%d/%m/%Y %H:%M:%S")
                    store_dict["ADDRESS"]       = response.xpath(unpack_nested_strings(SRPL.STORE_ADDRESS)).get()
                    store_dict["OPEN_TIMES"]    = response.xpath(unpack_nested_strings(SRPL.STORE_OPEN_TIMES)).get()
                    store_dict["SELECT"]        = f"/store/select_store/{store_dict['HREF']}"
                    store_dict["LOCATION"] = None

                    store = self.create_store_item(store_dict)
                    
                    print("[INTERNAL]: Local data was inconsistent with data from website, deleting local data...")
                    for refuted_item in self.session_refuted_stores:
                        self.delete_store_data(store_dict=refuted_item)
                    self.stores.append(store)
                
            if item["TYPE"] == "LOCAL_DATA":
                if self.local_store_object["NAME"] == item["NAME"] and self.local_store_object["HREF"] == item["HREF"]:
                    for store in self.stores:
                        if store is self.local_store_object:
                            now = datetime.now()
                            store["LAST_UPDATED"] = now.strftime("%d/%m/%Y %H:%M:%S")
                            print("[INTERNAL]: Used locally stored href to find store page.\nIf the name of the the store crawled still doesn't match up with what you're looking for, please ensure that both the name and href match up, or you can search only by store name.")
                            break

    def query_website_for_store(self, response=None):
        if response is None:
            if self.store_name is not None:
                request_data = {"URL" : prepare_search_string(URLS.STORE_SEARH_BASE_URL, self.store_name), "CALLBACK" : self.schedule_requests}
                return request_data
            else:
                raise Exception("A store name is required if a search for a store is to be possible.")
        else:
            print("[INTERNAL]: Scraping store list...")
            self.scrape_store_list(response)
            for store in self.stores:
                if store["NAME"] == self.store_name:
                    self.local_store_object = store
                    break
            if self.local_store_object is not None:
                request_data = {"URL" : prepare_search_string(URLS.STORE_SELECT_BASE_URL, self.local_store_object["HREF"]), "CALLBACK" : self.schedule_requests}
                return request_data
            else:
                print("[INTERNAL]: Fetching next page...")
                request_data = self.get_next_page(response)
                if request_data is None:
                    print("Could not find store through website query. ending search...")
                    self.complete_search_performed = True
                    request_data = {"URL" : URLS.PAGE_BASE_URL, "CALLBACK" : self.schedule_requests}
                    return request_data
                return request_data

    def get_next_page(self, response):
        search_term = unpack_nested_strings(SLSL.STORE_LIST_NEXT_BUTTON)
        next_button = response.xpath(search_term).get()
        if next_button == None:
            return None
        else:
            search = URLS.PAGE_BASE_URL[:-1] + next_button.replace("/stores?", "/stores/?")
            search_url = {"URL" : search, "CALLBACK" : self.schedule_requests}
            return search_url   

    def scrape_store_list(self, response):
        search_list = [SLSL.STORE_NAME, SLSL.STORE_HREF, SLSL.STORE_ADDRESS, SLSL.STORE_SELECT_BUTTON]
        store_dict = {}
        found_stores = []

        for search_term in search_list:
            search_list[search_list.index(search_term)] = unpack_nested_strings(search_term)

        store_dict["NAMES"]       = response.xpath(search_list[0]).getall()
        store_dict["HREFS"]       = response.xpath(search_list[1]).getall()
        store_dict["ADDRESSES"]   = response.xpath(search_list[2]).getall()
        store_dict["SELECTS"]     = response.xpath(search_list[3]).getall()
        
        list_lengths = [
            len(store_dict["NAMES"]),
            len(store_dict["HREFS"]),
            len(store_dict["ADDRESSES"]),
            len(store_dict["SELECTS"])
            ]
        if len(set(list_lengths)) == 1:
            for name, href, address, select in zip(store_dict["NAMES"], store_dict["HREFS"], store_dict["ADDRESSES"], store_dict["SELECTS"]):
                item_dict = {}
                now = datetime.now()
                item_dict["NAME"] = name
                item_dict["HREF"] = href.replace("/store/", "")
                item_dict["ADDRESS"] = address
                item_dict["DATE_ADDED"] = now.strftime("%d/%m/%Y %H:%M:%S")
                item_dict["LAST_UPDATED"] = now.strftime("%d/%m/%Y %H:%M:%S")
                item_dict["OPEN_TIMES"] = None
                item_dict["SELECT"] = select
                item_dict["LOCATION"] = None
                
                item = self.create_store_item(item_dict)
                self.delete_store_data(item)
                found_stores.append(item)
        else:
            raise Exception("[ERROR]: List lengths were inconsistent after the scraping of store data, please ensure that the page selectors are correct...")
        
        for item in found_stores:
            prevent_append = False
            for store in self.stores:
                if store["NAME"].lower() == item["NAME"].lower():
                    prevent_append = True
                    store["HREF"] = item["HREF"]
                    store["ADDRESS"] = item["ADDRESS"]
                    store["DATE_ADDED"] = item["DATE_ADDED"]
                    store["LAST_UPDATED"] = item["LAST_UPDATED"]
                    store["SELECT"] = item["SELECT"]
                    break
            if not prevent_append:
                self.stores.append(item)

    def save_store_data(self):
        self.process_local_store_data()
        stores_dict = {"stores" : []}
        valid_store_chains = [
            "s-market",
            "sale",
            "prisma",
            "alepa",
            "abc",
        ]
        for item in self.stores:
            for x in valid_store_chains:
                if x in item["NAME"].lower():
                    chain = x
            stores_dict["stores"].append({
                "NAME" : item["NAME"].title(),
                "CHAIN" : chain,
                "OPEN_TIMES" : item["OPEN_TIMES"].title() if isinstance(item["OPEN_TIMES"], str) else item["OPEN_TIMES"],
                
                "LOCATION" : item["LOCATION"],
                "ADDRESS" : item["ADDRESS"].title() if isinstance(item["ADDRESS"], str) else item["ADDRESS"],
                
                "DATE_ADDED" : item["DATE_ADDED"],
                "LAST_UPDATED" : item["LAST_UPDATED"],
                
                "HREF" : item["HREF"],
                "SELECT" : item["SELECT"]
                })    

        print("[INTERNAL]: Saving store data...")
        with open(FilePaths.stores_path, "w") as f:                                     
            json.dump(stores_dict, f, indent=2)

    def delete_store_data(self, store_dict=None):
        if store_dict is not None:  
            for store in self.stores:
                if store["NAME"] == store_dict["NAME"] and store["HREF"] == store_dict["HREF"]:
                    self.stores.remove(store)

    def fill_store_fields(self, response):
        store = None
        for item in self.stores:
            if self.store_data["NAME"].lower() == item["NAME"] and self.store_data["HREF"].lower() == item["HREF"]:
                store = item
                inx = self.stores.index(item)
                break
        if store is not None:
            now = datetime.now()
            store["HREF"] = response.xpath(unpack_nested_strings(SRPL.STORE_HREF)).get().replace("/store/", "")
            store["LAST_UPDATED"] = now.strftime("%d/%m/%Y %H:%M:%S")
            if store["DATE_ADDED"] == None or store["DATE_ADDED"] == "":
                store["DATE_ADDED"] = now.strftime("%d/%m/%Y %H:%M:%S") 

            if store["ADDRESS"] == None or store["ADDRESS"] == "":
                store["ADDRESS"] = response.xpath(unpack_nested_strings(SRPL.STORE_ADDRESS)).get()

            if store["OPEN_TIMES"] == None or store["OPEN_TIMES"] == "":
                open_times = response.xpath(unpack_nested_strings(SRPL.STORE_OPEN_TIMES)).get().replace("\n", "").replace("\r", "")
                open_times = ' '.join(open_times.split())
                store["OPEN_TIMES"] = open_times
            self.stores[inx] = store
        
    def process_product_search(self, response):
        search_lists = {"IDENTIFIER" : PLSL.IDENTIFIER_LIST, "DATA" : PLSL.DATA_LIST, "DETAIL" : PLSL.DETAIL_LIST}
        data_dict = {}

        for lst in search_lists.values():
            for item in lst:
                lst[lst.index(item)] = unpack_nested_strings(item)  #Yeah this operation is way too expensive to do every time

        data_dict["NAME"]           = response.xpath(search_lists["IDENTIFIER"][0]).getall()
        data_dict["SUBNAME"]        = response.xpath(search_lists["IDENTIFIER"][1]).getall()
        data_dict["IMG"]            = response.xpath(search_lists["IDENTIFIER"][2]).getall()
        data_dict["HREF"]           = response.xpath(search_lists["IDENTIFIER"][3]).getall()

        data_dict["QUANTITY"]       = response.xpath(search_lists["DATA"][0]).getall()
        data_dict["PRICE_WHOLE"]    = response.xpath(search_lists["DATA"][1]).getall()
        data_dict["PRICE_DECIMAL"]  = response.xpath(search_lists["DATA"][2]).getall() #This seems like an incredible violation of DRY to me
        data_dict["UNIT"]           = response.xpath(search_lists["DATA"][3]).getall()  #Can't bother to think of a smarter solution
        data_dict["UNIT_PRICE"]     = response.xpath(search_lists["DATA"][4]).getall()  

        data_dict["SHELF_NAME"]     = response.xpath(search_lists["DETAIL"][0]).getall()
        data_dict["SHELF_HREF"]     = response.xpath(search_lists["DETAIL"][1]).getall()
        self.process_data_dict(data_dict)

        #This is where a scrapy item exporter or similar would be called, 
        #it's not implemented yet so it's just printing all the stuff out for now
        for item in self.scraped_products:  
            #print(f"NAME: {item['NAME'].title():<60} STORE_NAME: {self.store_data['NAME'].title()}\n")
            #print(f"{'':<5}PRICE: {item['PRICE']}€\n")
            #for x in item.keys():
                #if x != "NAME" and x != "PRICE":
                    #print(f"{'':<20}{x:<15}:  {item[x]}")
            #print("\n")
            yield item

    def process_data_dict(self, data):
        for name, subname, img, href, quantity, price_whole, price_decimal, unit, unit_price, shelf_name, shelf_href in zip(
            data["NAME"], data["SUBNAME"], data["IMG"], data["HREF"], data["QUANTITY"], 
            data["PRICE_WHOLE"], data["PRICE_DECIMAL"], data["UNIT"], data["UNIT_PRICE"],
            data["SHELF_NAME"], data["SHELF_HREF"]):        #yes, my eyes hate it
            
            #(in identifier list)
            item_dict = {}
            item_dict["STORE_NAME"] = self.store_data['NAME']
            item_dict["NAME"]       = name
            item_dict["SUBNAME"]    = subname   
            item_dict["IMG"]        = img
            item_dict["HREF"]       = href
            
            #(in data list)
            item_dict["QUANTITY"]   = quantity
            item_dict["PRICE"]      = float(f"{price_whole}.{price_decimal}")
            item_dict["UNIT"]       = unit
            item_dict["UNIT_PRICE"] = ' '.join(unit_price.split()) #Unit prices has lots of spaces for some reason
            
            #(in detail list)
            item_dict["SHELF_NAME"] = shelf_name
            item_dict["SHELF_HREF"] = shelf_href

            item = self.create_product_item(item_dict)
            self.scraped_products.append(item)

    def create_product_item(self, product_dict):
        item = FoodieProductItem()
        for product in product_dict.items():
            if isinstance(product[1], str):
                product_dict[product[0]] = product[1].lower()

        item["STORE_NAME"]  = product_dict["STORE_NAME"]
        item["NAME"]        = product_dict["NAME"]
        item["SUBNAME"]     = product_dict["SUBNAME"]
        item["IMG"]         = product_dict["IMG"]
        item["HREF"]        = product_dict["HREF"]
        item["QUANTITY"]    = product_dict["QUANTITY"]
        item["PRICE"]       = product_dict["PRICE"]
        item["UNIT"]        = product_dict["UNIT"]
        item["UNIT_PRICE"]  = product_dict["UNIT_PRICE"]
        item["SHELF_NAME"]  = product_dict["SHELF_NAME"]
        item["SHELF_HREF"]  = product_dict["SHELF_HREF"]
        return item