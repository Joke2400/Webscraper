'''
The website html on foodie.fi is absolute garbage to read and navigate. 
So that's why there's a bunch of locators, cause whoever created that site didn't bother to spam id tags on useful XML elements
'''

class SearchResultsPageLocators:
    ''' A class that contains XPATH selectors for key elements on the search results page.'''

    STORES_TOPMENU          =   "//div[@id='topmenu-stores']"                        
    STORE_NAME              =   (STORES_TOPMENU, "/a//div[@class='store-name']//b/text()")
    STORE_HREF              =   (STORES_TOPMENU, "/a/@href")
    STORE_ADDRESS           =   (STORES_TOPMENU, "/div//div[@class='store-row row']/div/div[2]/text()")
    STORE_OPEN_TIMES        =   (STORES_TOPMENU, "/div//div[@class='store-row row']/div/div[3]/text()")

    PRODUCT_LIST            =   "//ul[@class='shelf js-shelf products-shelf clear clearfix']"
    PRODUCT_LIST_ELEMENTS   =   "//li[@class='relative item effect fade-shadow js-shelf-item js-entrylist-item']"
    PRODUCT_HREF_ELEMENT    =   (PRODUCT_LIST_ELEMENTS, "//a[@class='js-link-item']")
    PRODUCT_DETAILS         =   (PRODUCT_LIST_ELEMENTS, "//div[@class='info relative clear']")
    PRODUCT_PRICE_DETAILS   =   (PRODUCT_DETAILS, "//div[@class='price-and-quantity']")

class ProductListSearchLocators:
    """A class that contains selectors for the product details, all of these are for use within the <li> element for the product
        This is a relic from how I used to store similar locators in my selenium version of this scraper i created while initially learning webscraping.
        However i still think it's easier on you mentally to have the strings segmented into parts when developing (easier to ensure which parts work, and which don't).

        #TODO:
            Currently calling unpack_nested_strings() needlessly in foodie_spider.py
            A smart thing to do might be to create a function that uses unpack_nested_strings() to compile the tuples into singular strings
            and then store them into a text/json file, and then create variables on runtime instead.
            This avoids the calling of unpack_nested_strings() on each search term, for each product search, each time the program is run...
            How unpack_nested_strings() is used in the spider might also need to be changed. Maybe call it once in the beginning of
            the program instead...
    """

    PRODUCT_LIST            =   SearchResultsPageLocators.PRODUCT_LIST
    PRODUCT_LIST_ELEMENTS   =   SearchResultsPageLocators.PRODUCT_LIST_ELEMENTS
    PRODUCT_DETAILS         =   SearchResultsPageLocators.PRODUCT_DETAILS
    PRODUCT_PRICE_DETAILS   =   SearchResultsPageLocators.PRODUCT_PRICE_DETAILS
    PRODUCT_HREF_ELEMENT    =   SearchResultsPageLocators.PRODUCT_HREF_ELEMENT
    #The above is shit... should do it differently later, or you know just put them under the same class like a sane person would

    #Selectors for the product data contained within PRODUCT_DETAILS
    PRODUCT_NAME            =   (PRODUCT_DETAILS, "/div[@class='name']/text()")
    PRODUCT_QUANTITY        =   (PRODUCT_DETAILS, "//span[@class='quantity']/text()")
    PRODUCT_SUBNAME         =   (PRODUCT_DETAILS, "//span[@class='subname']/text()")
    PRODUCT_SHELF_NAME      =   (PRODUCT_DETAILS, "//span[@class='indoor-location-name']/text()")
    PRODUCT_SHELF_HREF      =   (PRODUCT_DETAILS, "//a[@class='indoor-location js-indoor-location']/@href")

    #Selectors for the product data contained within PRODUCT_PRICE_DETAILS
    PRODUCT_PRICE_WHOLE     =   (PRODUCT_PRICE_DETAILS, "//span[@class='whole-number ']/text()")
    PRODUCT_PRICE_DECIMAL   =   (PRODUCT_PRICE_DETAILS, "//span[@class='decimal']/text()")
    PRODUCT_UNIT            =   (PRODUCT_PRICE_DETAILS, "//span[@class='unit']/text()")
    PRODUCT_UNIT_PRICE      =   (PRODUCT_PRICE_DETAILS, "//div[@class='unit-price clear js-comp-price ']/text()")

    #Selectors for the product data contained within PRODUCT_HREF_ELEMENT
    PRODUCT_IMG             =   (PRODUCT_HREF_ELEMENT, "//img[@class='img-responsive']/@src")
    PRODUCT_HREF            =   (PRODUCT_HREF_ELEMENT, "/@href")

    IDENTIFIER_LIST         =   [PRODUCT_NAME, PRODUCT_SUBNAME, PRODUCT_IMG, PRODUCT_HREF]
    DATA_LIST               =   [PRODUCT_QUANTITY, PRODUCT_PRICE_WHOLE, PRODUCT_PRICE_DECIMAL, PRODUCT_UNIT, PRODUCT_UNIT_PRICE]
    DETAIL_LIST             =   [PRODUCT_SHELF_NAME, PRODUCT_SHELF_HREF]

class StoreListSearchLocators:

    STORE_LIST              = "//ul[@id='js-search-store-list']"
    STORE_LIST_ELEMENTS     = "//li[@class='store-row relative clearfix js-store-row']"
    STORE_NAME              = (STORE_LIST_ELEMENTS, "//a[@class='no-underline inline-block']/div[@class='name']/text()")
    STORE_ADDRESS           = (STORE_LIST_ELEMENTS, "//a[@class='no-underline inline-block']/div[@class='address']/text()")
    STORE_HREF              = (STORE_LIST_ELEMENTS, "//a[@class='no-underline inline-block']/@href")
    STORE_SELECT_BUTTON     = (STORE_LIST_ELEMENTS, "//div[@class='inline-block']/div[@class='row']/div[@class='item-actions js-item-actions']/div[@class='btn-group btn-group-sm']/a/@href")
    NAVIGATION_BUTTONS      = "//ul[@class='pagination pagination-lg']"
    STORE_LIST_NEXT_BUTTON  = (NAVIGATION_BUTTONS, "//a[@rel='next']/@href")
