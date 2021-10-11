from webscraper.data.descriptors import StringAttribute
from webscraper.webscraper_package.scraper_manager import SearchManager

class ProcessManager:
    query = StringAttribute()

    def __init__(self):
        pass
    
    def start(self):
        pass

    def get_search_query(self):
        print("A product query can be a single item or several separated by a ','")
        self.query = input("Please enter a product query: ").split(',')