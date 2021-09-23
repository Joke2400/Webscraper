from webscraper.scraper_manager import SearchManager
from webscraper.gmaps_package.gmaps_api_manager import GMapsAPIManager

settings_path = 'webscraper.webscraper_package.settings' 

if __name__ == "__main__":
    
    #Be careful when running many searches at once, the spider doesn't have a speed limitation set at the moment and we don't want to annoy any devs
        #You can set several different limitations in the settings.py file or enable the scrapy autothrottling extension

    #Example uses:

    #manager = SearchManager(stores=["S-Market Grani", "Prisma Kirkkonummi"], product_search=["raejuusto", "kreikkalainen jogurtti"], ignore_store_data=False, spider_type="Foodie", settings=settings_path)
    #manager = SearchManager(stores=[("Prisma Olari","0563cf74f373b2250360e756060fdb59")], product_search="raejuusto", spider_type="Foodie", settings=settings_path)
    #manager = SearchManager(store_name="Prisma Olari", product_search="raejuusto", spider_type="Foodie", settings=settings_path)
    #manager = SearchManager(store_href="0563cf74f373b2250360e756060fdb59", product_search="raejuusto", spider_type="Foodie", settings=settings_path)
    google_api_manager = GMapsAPIManager()
    scraper_manager = SearchManager(stores=["S-Market Grani", "Prisma Olari"], product_search="maito", spider_type="Foodie", settings=settings_path)

    scraper_manager.start_process()