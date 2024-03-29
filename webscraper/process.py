import os
from webscraper.data.filepaths import FilePaths
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webscraper.webscraper_package.spiders.webber import Webber
from webscraper.data_manager_package.data_manager import DataManager

def start(products, stores):
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', FilePaths.settings_path)
    try:
        os.remove(FilePaths.log_path) #Remove scrapy log file from previous run
    except:
        pass
    process = CrawlerProcess(get_project_settings())

    data_manager = DataManager()
    data_manager.reset_database()
    data_manager.start_session()
    
    process.crawl(Webber, 
            requested_products=products,
            requested_stores=stores, 
            data_manager=data_manager,
            requesting_old_site=True
            )
    
    process.start()