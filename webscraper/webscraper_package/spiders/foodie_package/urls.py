class FoodieURLS():

    PAGE_BASE_URL               =   "https://www.foodie.fi/"
    PRODUCT_SEARH_BASE_URL      =   "https://www.foodie.fi/products/search2?term="
    PRODUCT_SEARH_BASE_URL_2    =   "https://www.foodie.fi/products/search?term="
    STORE_SEARH_BASE_URL        =   "https://www.foodie.fi/stores/?query=" #can be expanded with city name
    STORE_PAGE_URL              =   "https://www.foodie.fi/store/"
    STORE_SELECT_BASE_URL       =   "https://www.foodie.fi/store/select_store/"
    STORE_LIST_BASE_URL         =   "https://www.foodie.fi/store/list"    
    #Store list, can be navigated with next page
    #might want to avoid using it though since searching for the store might be quicker

    #THERE IS A SEARCH url without the num 2 in the url which can accept item tag_ids, 
    #might want to look into that