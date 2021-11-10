from webscraper.process_manager import ProcessManager

if __name__ == "__main__":

    #Be careful when running many searches at once, the spider doesn't have a speed limitation set at the moment and we don't want to annoy any devs
        #You can set several different limitations in the settings.py file or enable the scrapy autothrottling extension
    manager = ProcessManager()
    manager.start(terminal_only=True)

    #TODO:
    #Process manager will be the main manager in the futurem, SearchManager also needs a rewrite
    
    #SearchManager should be in charge of managing stores.json 
    #   / it should be able to use both gmaps and the scraper to manage data
    
    #Foodie scraper will be improved in the future, 
    #   / better attribute handling(descriptors), simplified code
    #   / use custom_data_classes.StoreItem for store list (decided i don't like the scrapy.item system)
    #       /returning items from the scraper is easiest through a scrapy item pipeline however
    #   / create similar class for product items  

    #Some parts of GMaps API could be asynchronous like scrapy
    #   /While foodie spider might be dependent on the results
    #   /further integration with ex. a discord bot might be troublesome idk

    #Make certain parts of the code asynchronous?

    #Cases for get request error status codes

    #TODO:
    #IMPORTANT:
    #   /Optimizing get_store_location_data()
    #       /Currently very slow when there are several stores
    #       /with missing locations... Either connection-related or 
    #       /code-related, probably the latter...

    #UP NEXT:
    #   /1. Process Manager - SearchManager Revamp
    #   /2. Basic discord bot integration