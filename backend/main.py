import requests
from random import randint
import googlemaps
from dotenv import load_dotenv
import time
import os
from test import get_rating

load_dotenv()
api_key = os.getenv("API_KEY")
rating = int(get_rating())
gmaps = googlemaps.Client(key=api_key)

def get_distance():
    addressdata = gmaps.reverse_geocode((37.3489, -121.9368)) # temp coords
    formatted_addy = []
    addressdata2 = gmaps.reverse_geocode((37.5679, -122.0524)) # temp coords
    formatted_addy2 = []

    address_arr = []
    for item in addressdata:
        address_arr.append(item['formatted_address'])

    address_arr2 = []
    for item in addressdata2:
        address_arr2.append(item['formatted_address'])

    formatted_location_dest = address_arr[0]
    formatted_location_origin = address_arr2[0]

    origin = (formatted_location_origin)  # Latitude and Longitude of Saratoga & Payne, San Jose
    destination = (formatted_location_dest)

    result = gmaps.distance_matrix(origin, destination, mode="driving")


    distance = result['rows'][0]['elements'][0]['distance']['text']
    duration = result['rows'][0]['elements'][0]['duration']['text']

    distancenum = round(((float(distance.split()[0]))/1.609),2)

    return distancenum

output = randint(1,100) # will be replaced by the LLM and output from the INIRIX API
threshold = 10 #subject to change depending on data analysis


def evaluate_congestion (congestion_threshold):
    if (rating > congestion_threshold):
        return True
    else:
        return False

def checkdistance(dist):
    while True:
        time.sleep(1)
        dist-=1
        if (dist <= 10):
            break
    print("Move over, ambulance is coming!")

if (evaluate_congestion(threshold)):
    print(f"{get_distance()} mi")

if (not evaluate_congestion(threshold)):
    print("There is not enough traffic")

checkdistance(get_distance())


