from webscraper.scraper_manager import SearchManager
from webscraper.gmaps_package.gmaps_api_manager import GMapsAPIManager

if __name__ == "__main__":
    
    #Be careful when running many searches at once, the spider doesn't have a speed limitation set at the moment and we don't want to annoy any devs
        #You can set several different limitations in the settings.py file or enable the scrapy autothrottling extension

    gmaps_api_manager = GMapsAPIManager(address="Siestankuja 16D")
    #gmaps_api_manager.key_path  = r"C:\Users\Joke\Desktop\google_cloud_api.txt"
    print(gmaps_api_manager.__dict__)
    
    gmaps_api_manager.address = "x"
    
    print(gmaps_api_manager.address)
    
    print(type(gmaps_api_manager.address))
    
    print(gmaps_api_manager.__dict__)
    
    #gmaps_api_manager.radius    = 5
    #gmaps_api_manager.language  = "sv"
    #gmaps_api_manager.search()
    #gmaps_api_manager.best_match(limit=5)

    scraper_manager = SearchManager(stores=["S-Market Grani", "Prisma Olari"], product_search="maito", spider_type="Foodie")

    scraper_manager.start_process()

#TODO:
#Rework scraper_manager to have similar interface to gmaps_api_manager
#Rework how attributes are managed in foodie_spider, perhaps make use of attributes
