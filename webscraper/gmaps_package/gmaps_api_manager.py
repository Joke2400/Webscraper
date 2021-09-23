from ..foodie_webscraper.spiders.fpaths import FilePaths
from ..foodie_webscraper.spiders.foodie_package.helper_functions import fetch_local_data2

class GMapsAPIManager:

    def __init__(self):
        pass

    def gather_locally_stored_coords(self):
        pass

    def send_api_request(self):
        pass

    def parse_api_request(self):
        pass

    def parser_function(self):
        pass
'''
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