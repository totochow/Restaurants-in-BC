#API Key
YELP_API = 'your long yelp api key'


#well.... import all the lib we need....

import requests
import time
import pandas as pd
import json

#define a new function for creating the search parameters, as well as the offset

def get_search_parameters(lat,long, offset):
    #See the Yelp API for more details
    params = {}
    params["term"] = "restaurant"
    params["location"] = "{},{}".format(str(lat),str(long))
    params["radius_filter"] = "2000000"
    params["limit"] = "50"
    params["offset"] = offset
    return params

#define a new funtion for calling the API and get results, returning the data in Pandas DataFrame format

def get_results(params):
 
    #Obtain these from Yelp's manage access page
    HEADERS = {'Authorization': 'Bearer %s' % YELP_API}
    respond = requests.get("https://api.yelp.com/v3/businesses/search?",params=params, headers = HEADERS)
    #Transforms the JSON API response into a Python dictionary
    data = respond.json()
    df = pd.json_normalize(data['businesses'])
    respond.close()
    return df

# the main function to use the previous two functions
def main(loc):
    locations = loc
    api_calls = pd.DataFrame()
    for lat,long in locations:
        for offset in range(0, 1000, 50):
            params = get_search_parameters(lat,long, offset)
            api_calls = api_calls.append(get_results(params), ignore_index=True)
            print(str(offset) + " of 1000")
            time.sleep(1.0) #be a good boy!
    return api_calls


#alright! give coordinates of Richmond, Vancouver, Surrey, Coquitlam... and start searching!
df = pd.DataFrame(main([(49.1942946, -123.0879533),(49.283764, -122.793205),(49.177070, -122.801201),(49.356993, -123.098152),(49.278325, -123.131459)]))
df

#save the results
df.to_excel('C:\\Users\\tchow\\Desktop\\VanRest.xlsx') 

