from ..data.fpaths import FilePaths
from ..data.helper_functions import fetch_local_data2, filter_duplicates_and_append
from ..data.descriptors import StringAttribute
from .urls import GMapsAPIUrls as GMAPS_URLS
import requests

class GMapsAPIManager:

    address = StringAttribute()

    def __init__(self, address):
        self.address = address

'''
        @StringAttribute
        def key_path(self, value):
            pass

        @AddressAttribute
        def address(self, value):
            pass

        @StringAttribute
        def language(self, value):
            pass

        @NumberAttribute
        def radius(self, value):
            pass

        self._key = None

        self._nearby_search_type = "store"
        self._nearby_search_keyword = "s-market"
        self._location = None
        self._stores = None


    def perform_api_request(self, url, payload, callback=None):
        #payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
        #TODO:
        #Cases for error status codes
        response = requests.get(url, params=payload)
        if callback is not None:
            callback(response)
        return response

    @property
    def address(self):
        return self._address.title()

    @address.setter
    def address(self, value):
        if isinstance(value, str):
            self._address = value.lower()
            payload = {
                "address" : self.address,
                "key" : self.key,
                "language" : self.language
             }
            self.location = self.perform_api_request(GMAPS_URLS.GEOCODE, payload)
        else:
            raise TypeError("Address can only be a string")

    @address.deleter
    def address(self):
        self._address = None

    @property
    def location(self):
        #Named tuple for this shit
        pass

    @location.setter
    def location(self):
        pass

    @location.deleter
    def location(self):
        pass




    @property
    def stores(self):
        if self._stores is None or not isinstance(self._stores, list):
            stores_json = fetch_local_data2(FilePaths.stores_path, "stores")
            
            if len(stores_json["stores"]) > 0:
                for store_dict in stores_json["stores"]:
                    for key, value in store_dict.items():
                        if isinstance(value, str):
                            store_dict[key] = value.lower()
                    
                    self._stores = filter_duplicates_and_append(self._stores, store_dict)


        return self._stores

    @stores.setter
    def stores(self, lst):
        if isinstance(lst, (list, tuple)):
            self._stores = lst

    @stores.deleter
    def stores(self):
        self._stores = None






Step 1:
    -User inputs location
Step 2:
    -Gather all local data coordinates
Step 3:
    -Use haversine function to calculate great circle distance
    -Return list of results present within a given radius

Step 4:
    -Use distance api to find stores within area
        -Ensure it's a distance by radius on map, not distance by driving distance

Step 5:
    -Update stores list with any new data
    -Ensure coords, place id and global code are all saved

Step 6:
    -Scrape in stores within radius

'''

'''
https://maps.googleapis.com/maps/api/place/nearbysearch/json

?location=60.22359058303004,24.717009459380908
&language=fi
&radius=2000
&type=store
&keyword=s-market
&key=AIzaSyAD30MYjcy83QAnyNLNwIIiRtK-znORMWs
'''

'''
#https://maps.googleapis.com/maps/api/place/findplacefromtext/json

?input=s-market
&inputtype=textquery
&locationbias=circle:1000@60.22359058303004, 24.717009459380908
&fields=formatted_address,name,opening_hours,geometry
&key=AIzaSyAD30MYjcy83QAnyNLNwIIiRtK-znORMWs
'''