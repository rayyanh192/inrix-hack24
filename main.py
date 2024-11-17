import requests
from random import randint
import googlemaps
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

api_key = os.getenv("API_KEY")

# print("DEBIGU:" + api_key)

gmaps = googlemaps.Client(key=api_key)
addressdata = gmaps.reverse_geocode((40.714224, -73.961452))
formatted_addy = []

streetnum = ""
road = ""
city = ""
state = ""
zip = ""

for item in addressdata:
    types = item.get("types", [])
    if "street_number" in types:
        streetnum = item.get("long_name", "")
    elif "route" in types:
        road = item.get("long_name", "")
    elif "sublocality" in types or "sublocality_level_1" in types:
        city = item.get("long_name", "")
    elif "administrative_area_level_1" in types:
        state = item.get("short_name", "")

formatted_addy = streetnum + " " + road + ", " + city + ", " + state
print(addressdata)
print(formatted_addy)


#origin = reverse_geocode_result
destination = "New York City, NY"

#result = gmaps.distance_matrix(origin, destination, mode="driving")

#distance = result['rows'][0]['elements'][0]['distance']['text']
#duration = result['rows'][0]['elements'][0]['duration']['text']

#print(f"Distance: {distance}")
#print(f"Duration: {duration}")
output = randint(1,100) # will be replaced by the LLM and output from the INIRIX API
threshold = 30 #subject to change depending on data analysis


def evaluate_congestion (score):
    if (score > threshold):
        return True

    else:
        return False

#print(evaluate_congestion(output))


speed_threshold = 10
def id_car(speed): #NOTE: cars in traffic have speed of 0 (edge-case for this function)
    if (speed > speed_threshold):
        return True