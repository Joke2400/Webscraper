class GMapsAPIUrls:

    PLACE_FROM_TEXT = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    NEARBY_SEARCH = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json"

class FoodieURLs:

    base_url                    =   "https://www.foodie.fi"
    product_search_url          =   "https://www.foodie.fi/products/search2?term="
    product_search_url2         =   "https://www.foodie.fi/products/search?term="
    store_search_url            =   "https://www.foodie.fi/stores/?query=" #can be expanded with city name
    store_page_url              =   "https://www.foodie.fi/store/"
    store_select_url            =   "https://www.foodie.fi/store/select_store/"
    store_list_url              =   "https://www.foodie.fi/store/list"    
    #Store list, can be navigated with next page
    #might want to avoid using it though since searching for the store might be quicker

    #THERE IS A SEARCH url without the num 2 in the url which can accept item tag_ids, 
    #might want to look into that

class SkaupatURLs:
    pass