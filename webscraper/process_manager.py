from typing import Union
from webscraper.data.descriptors import BooleanAttribute
from webscraper.webscraper_package.scraper_manager import SearchManager
from webscraper.gmaps_package.gmaps_api_manager import GMapsAPIManager
from webscraper.webscraper_package.pipelines import FoodieWebscraperPipeline as pipeline

class ProcessManager:
    terminal_only = BooleanAttribute()

    def __init__(self):
        self.gmaps_manager = GMapsAPIManager(radius=5, language="sv", keypath=r"C:\Users\Joke\Desktop\API_KEYS\google_cloud_api.txt")
        #self.search_manager = SearchManager()
    
    def start(self, **kwargs):
        self.terminal_only = kwargs.get("terminal", False)
        
        #TEMPORARY:
        del kwargs["terminal"]

        if self.terminal_only:
            result = self.start_terminal_only()
        else:
            result = self.start_default(**kwargs) 

    def start_default(self, **kwargs):
        #WILL CURRENTLY ONLY WORK WITH A SINGLE STORE AS A FIRST ITERATION
        #ALSO SKIPPING GMAPS API FOR NOW

        address = kwargs.get("address", None)
        stores= kwargs.get("stores", None)
        search_query = kwargs.get("search_query", None)
        
        if search_query is None:
            raise TypeError("start_default() requires a store_query to be passed as a string")
        if stores is None:
            raise TypeError("start_default() requires a store_name to be passed as a string")
        if address is not None:
            self.gmaps_manager.address = address

        #valid_stores = self.gmaps_manager.fetch_eligible_stores()                   
        
        scraper_manager = SearchManager(stores=stores, product_search=search_query, spider_type="Foodie")
        scraper_manager.start_process()

        for item in pipeline.product_list:
            yield item

    def start_terminal_only(self):
        print("Process started...")
        commands = '''\nCommands:\n
        '''
        print(commands)

        #------TEMP-----
        '''
        valid_stores = self.gmaps_manager.fetch_eligible_stores()

        print("\n")
        print(self.gmaps_manager.address)
        print("Stores fetched from local data that are within range:\n")
        for item in valid_stores:
            print(f"Name: {item[0].name.title()}")
            print(f"{'':<20} Distance: {item[1]:.2f}km")
        print("\nPlease select desired store or initiate nearby search...")
        i = input("\nCommands: nearby_search, select: ")
                                            
        def select_store(valid_stores):
            stores = []
            input_stores = input("Please input store names separated by | if more than one: ").lower().split("|")
            print(input_stores)
            for item in input_stores:
                for store in valid_stores:
                    if store[0].name == item.lower():
                        stores.append(item)
                        break
            return stores
        if i == "nearby_search":
            input_type = input("Nearby search works better if you provide a keyword: ")
            valid_stores = self.gmaps_manager.nearby_search(input_type)
            for item in valid_stores:
                print(f"Name: {item[0].name.title()}")
                print(f"{'':<20} Distance: {item[1]:.2f}km")
            stores = select_store(valid_stores)
        elif i == "select":
            stores = select_store(valid_stores)

        print("A product query can be a single item or several separated by commas")
        '''
        stores = ["prisma olari", "s-market nihtisilta", "s-market grani"]
        search_query = input("Please enter a product query: ").split(",")
        scraper_manager = SearchManager(stores=stores, product_search=search_query, spider_type="Foodie")
        scraper_manager.start_process()

        #Scraped products get stored in a classvariable in the pipeline
        #Items do not get exported into a text file as of this moment
        for item in pipeline.product_list:
            print(f"NAME: {item['NAME'].title():<60} STORE_NAME: {item['STORE_NAME'].title()}\n")
            print(f"{'':<5}PRICE: {item['PRICE']}€\n")
            for x in item.keys():
                if x != "NAME" and x != "PRICE" and x != "STORE_NAME":
                    print(f"{'':<20}{x:<15}:  {item[x]}")
            print("\n")

        #---------------