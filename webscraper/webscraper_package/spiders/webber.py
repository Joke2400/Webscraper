from .webber_package.base_classes import BaseSpider
from ...utils.descriptors import SpecifiedOnlyValidator

#Site-specific scraper, will initially be built specifially for s-kaupat.fi/foodie.fi.
class Webber(BaseSpider):

    name = "Webber"
    
    requested_products  = SpecifiedOnlyValidator(list)
    requested_stores    = SpecifiedOnlyValidator(list)
    ignore_store_data   = SpecifiedOnlyValidator(bool)

    def __init__(self, *args, **kwargs):
        super(Webber, self).__init__(*args, **kwargs)
        self.requested_products = kwargs.get(
                "requested_products", [])
        self.requested_stores = kwargs.get(
                "requested_stores", [])
        if len(self.requested_products) < 1:
            raise Exception("Webber needs to be provided a product for a query.")
        if len(self.requested_stores) == 0:
            self.ignore_store_data = True
'''

Lets make some assumptions:
    By the time Webber starts doing his diligent spidery work:

        One of the stores or products requested by the user cant be found locally
                        (or both)

        if it's relevant to the search, user location will have been fetched:
            -> This is the most common scenario
            -> WEBBER CAN IGNORE LOCATION ENTIRELY

        Product and store data will already have been queried from the database:
            -> Product records that are up to date and accurate will have
                been pruned from webbers search list

        All relevant store data will be known already:
            -> True:
                -> Webber only needs to search the stores for products

            -> False:
                -> Webber has to first find the relevant stores

General/Initial webber flow:
    -> init

        - Store found locally
            -> Scrape website for products using webpage search
            -> Send scraped product data to Data Manager

        -> No store found locally
            -> Scrape website for stores using webpage search
            -> Increment pages until result is found
                -> Send all encountered store data to Data Manager
            -> Scrape website for products using webpage search
            -> Send scraped product data to Data Manager



Spider params ->
    product_search    | lst, tup | (Required) |
    
    Leaving either of the following empty -> Any store will be used,
        or closest store will be used...

    store_name        | lst, tup       | (Optional) | 
    store_object      | href(str), obj | (Optional) | 
        | Implement as secondary search method,     |
        | ex. If stores exist in database           |

Core functionality ->

    Spider ->
        Locations ->
            Locations are handled elsewhere, 
            scraper should be able to ask for a location however

        Search ->
            Scraper should be able to scrape a specific website secondhand

        Data management ->
            Asking Data manager for store data
            Sending store and product data Data manager

    Data manager ->
        Standalone manager for database queries and commits
        Receiving and sending data to spider

        Centralised storage for all store/product/location data

        ALL DATA FLOWS THROUGH THIS NEW CLASS AT LEAST ONCE BEFORE
        ITS DISPLAYED TO THE USER

Webber requirements

Generalisation

* classes for pages
* classes for key page elements

Optimization

* No more repeated recursive functions like the last one -_-

Data Manager

* Event driven pattern
* Initially synchronous, later maybe async


'''