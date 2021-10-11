from webscraper.webscraper_package.scraper_manager import SearchManager
from webscraper.gmaps_package.gmaps_api_manager import GMapsAPIManager

if __name__ == "__main__":
    
    #Be careful when running many searches at once, the spider doesn't have a speed limitation set at the moment and we don't want to annoy any devs
        #You can set several different limitations in the settings.py file or enable the scrapy autothrottling extension

    gmaps_api_manager = GMapsAPIManager(address="Siestankuja 16D", radius=5, language="sv", keypath=r"C:\Users\Joke\Desktop\google_cloud_api.txt")
    valid_stores = gmaps_api_manager.get_local_stores()

    print("\n")
    print(gmaps_api_manager.address)
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
        valid_stores = gmaps_api_manager.nearby_search(input_type)
        for item in valid_stores:
            print(f"Name: {item[0].name.title()}")
            print(f"{'':<20} Distance: {item[1]:.2f}km")
        stores = select_store(valid_stores)
    elif i == "select":
        stores = select_store(valid_stores)

    print("A product query can be a single item or several separated by commas")
    search_query = input("Please enter a product query: ").split(",")
    scraper_manager = SearchManager(stores=stores, product_search=search_query, spider_type="Foodie")
    scraper_manager.start_process()

#TODO: Search result fails if no search is provided
    #Nearby_search
    #Optimizing get_missing_locations()
    #parameters - missing conditions
    #Add asychronity?
    #replace start_search with more specific functions, create different operation functions
    #might want to rework all store list items to be named tuples instead of dicts when read into gmapsapi
    #Process manager will be the main manager in the future
    #Search manager need a revamp to be in line with process manager /also could use some better attribute handling
    #foodie scraper will be improved in the future
    #gmaps doesnt put date added/lastupdated
    #gmaps adds stores that are only named ex. s-market, chain name exists but no store name