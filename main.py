import requests
from random import randint
from latlon import LatLon
from geopy import geopy

output = randint(1,100) # will be replaced by the LLM and output from the INIRIX API
threshold = 30 #subject to change depending on data analysis


def evaluate_congestion (score):
    if (score > threshold):
        return True

    else:
        return False

print(evaluate_congestion(output))


speed_threshold = 10
def id_car(speed): #NOTE: cars in traffic have speed of 0 (edge-case for this function)
    if (speed > speed_threshold):
        return True