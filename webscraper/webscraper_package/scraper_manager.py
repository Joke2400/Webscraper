import os
from webscraper.data.fpaths import FilePaths
from scrapy.crawler import CrawlerProcess
from .spiders.foodie_spider import FoodieSpider
from scrapy.utils.project import get_project_settings

class SearchManager:
    def __init__(self, **kwargs):
        self.settings_path = kwargs.get("settings", None)
        if self.settings_path is not None:
            os.environ.setdefault('SCRAPY_SETTINGS_MODULE', self.settings_path)
        else:
            os.environ.setdefault('SCRAPY_SETTINGS_MODULE', FilePaths.settings_path)
        try:
            os.remove(FilePaths.log_path) #Remove scrapy log file from previous run
        except:
            pass

        self.spider_type = kwargs.get("spider_type", None)
        self.stores = kwargs.get("stores", None)
        self.product_search = kwargs.get("product_search", None)
        self.store_ignore_bool = kwargs.get("ignore_store_data", False)
        self.stores = [] if not isinstance(self.stores, list) else self.stores
        self.stores_pairs_dict = {}

        if len(self.stores) >= 1:
            for item in self.stores:
                if isinstance(item, tuple):
                    if len(item) == 2:
                        self.stores_pairs_dict[item[0]] = item[1]
                        self.stores.remove(item)
                    else:
                        raise Exception("[ERROR]: Stores param requires a list containing names or a list containing tuples that contain only a single name and href")
        else:
            self.store_name = kwargs.get("store_name", None)
            self.store_href = kwargs.get("store_href", None)

        self.process = CrawlerProcess(get_project_settings())
        self.prepare_search()

    def prepare_search(self):
        if self.spider_type.lower() == "foodie":
            self._spider_type = FoodieSpider
        else:
            raise NotImplementedError("Spider types other than 'Foodie' are not supported yet")
        
        if len(self.stores) < 1 and len(self.stores_pairs_dict) < 1:
           self.process.crawl(self._spider_type, product_search=self.product_search, store_name=self.store_name, store_href=self.store_href, ignore_store_data=self.store_ignore_bool)
        else:
            if len(self.stores) > 0:
                for store in self.stores:
                    self.process.crawl(self._spider_type, product_search=self.product_search, store_name=store, ignore_store_data=self.store_ignore_bool)
            if len(self.stores_pairs_dict) > 0:
                for key, value in self.stores_pairs_dict.items():
                    self.process.crawl(self._spider_type, product_search=self.product_search, store_name=key, store_href=value, ignore_store_data=self.store_ignore_bool)

    def start_process(self):
        print("Starting scraping process...")
        self.process.start()