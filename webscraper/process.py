import os
from webscraper.data.filepaths import FilePaths
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webscraper.webscraper_package.spiders.webber import Webber

def start():
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', FilePaths.settings_path)
    try:
        os.remove(FilePaths.log_path) #Remove scrapy log file from previous run
    except:
        pass
    process = CrawlerProcess(get_project_settings())

    process.crawl(Webber, start_urls=["https://s-kaupat.fi/kauppa"], requested_products=["Maito"])
    process.start()