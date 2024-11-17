import requests
from random import randint
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDHNeKahrDnpQJ7Wb-i6tTrSviE6S7nYfA')
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

print(reverse_geocode_result)
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