# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodieStoreItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    NAME = scrapy.Field()
    HREF = scrapy.Field()
    ADDRESS = scrapy.Field()
    DATE_ADDED = scrapy.Field()
    LAST_UPDATED = scrapy.Field()
    OPEN_TIMES = scrapy.Field()
    SELECT = scrapy.Field()

class FoodieProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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