import requests
from random import randint
import googlemaps
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

api_key = os.getenv("API_KEY")

gmaps = googlemaps.Client(key=api_key)
addressdata = gmaps.reverse_geocode((37.301153, -121.981205))
formatted_addy = []
addressdata2 = gmaps.reverse_geocode((37.7680, -122.3879))
formatted_addy2 = []

address_arr = []
for item in addressdata:
    address_arr.append(item['formatted_address'])

address_arr2 = []
for item in addressdata2:
    address_arr2.append(item['formatted_address'])

formatted_location_dest = address_arr[0]
print(formatted_location_dest)
formatted_location_origin = address_arr2[0]
print(formatted_location_origin)

origin = (formatted_location_origin)  # Latitude and Longitude of Saratoga & Payne, San Jose
destination = (formatted_location_dest)

result = gmaps.distance_matrix(origin, destination, mode="driving")


distance = result['rows'][0]['elements'][0]['distance']['text']
duration = result['rows'][0]['elements'][0]['duration']['text']

print(f"Distance: {distance}")
print(f"Duration: {duration}")

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