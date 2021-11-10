# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodieStoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NAME = scrapy.Field()
    CHAIN = scrapy.Field()
    OPEN_TIMES = scrapy.Field()

    ADDRESS = scrapy.Field()
    LOCATION = scrapy.Field()

    DATE_ADDED = scrapy.Field()
    LAST_UPDATED = scrapy.Field()

    HREF = scrapy.Field()
    SELECT = scrapy.Field()
    
class FoodieProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    STORE_NAME = scrapy.Field()
    NAME = scrapy.Field()
    SUBNAME = scrapy.Field()
    IMG = scrapy.Field()
    HREF = scrapy.Field()
    QUANTITY = scrapy.Field()
    PRICE = scrapy.Field()
    UNIT = scrapy.Field()
    UNIT_PRICE = scrapy.Field()
    SHELF_NAME = scrapy.Field()
    SHELF_HREF = scrapy.Field()