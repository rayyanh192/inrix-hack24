import base64
from PIL import Image
import io
from io import BytesIO
import os
import requests
import json

from random import randint
import time
from dotenv import load_dotenv
import re
import xml.etree.ElementTree as ET
import math

import boto3
import googlemaps
from flask import send_file

load_dotenv()

api_key = os.getenv("API_KEY")

def get_token():
    url = "https://na-api.beta.inrix.com/Traffic/Inrix.ashx?Action=GetSecurityToken&vendorId=1680049421&consumerId=3466e4ef-329b-474f-b52b-a3818e9df6b6&format=json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    token = json.loads(response.text)["result"]["token"]
    return token

token = get_token()

def get_min_id(token, c1lat, c1long):

#     corner1 = "37.458781|-123.213041" # car loc
    corner1 = f"{c1lat}|{c1long}"
    corner2 = "38.446329|-122.146655"

    corner1lat = float(corner1[0:9])
    corner1long = float(corner1[10:21])

    url = f"https://na-api.beta.inrix.com/Traffic/Inrix.ashx?action=GetTrafficCamerasInBox&locale=en-US&corner1={corner1}&corner2={corner2}&token={token}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    root = ET.fromstring(response.text)

    def get_camera_info(xml):
        cameras = []
        for camera in xml.findall(".//Camera"):
            camera_id = camera.get("id")
            point = camera.find("Point")
            latitude = point.get("latitude")
            longitude = point.get("longitude")

            status = camera.find("Status")


            if status is not None:
                out_of_service = status.get("outOfService")
            else:
                out_of_service = "Unknown"


            cameras.append({"id": camera_id, "latitude": latitude, "longitude": longitude, "outOfService": out_of_service})

        #print(cameras)
        return cameras

    def optimize_cameras(cameras):
        optimized_cameras = {}
        for camera in cameras:
            if camera["outOfService"] == "false":
                id = camera["id"]
                lat = float(camera["latitude"])
                long = float(camera["longitude"])

                vector = math.sqrt((lat - corner1lat)**2 + (long - corner1long)**2)
                optimized_cameras[id] = vector
        min = 2**31
        for camera in optimized_cameras:
            if optimized_cameras[camera] < min:
                min = optimized_cameras[camera]
                min_id = camera
        return min_id

    get_camera_info(root)

    return optimize_cameras(get_camera_info(root))


def check_dir_exists():
    cur_dir = os.getcwd()
    images = os.path.join(cur_dir, "images")
    if (os.path.exists(images)):
        for filename in os.listdir(images):
                file_path = os.path.join(images, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
    else:
        os.makedirs(images)


    return images


def get_camera_image(token):
    min_id = get_min_id(token, "37.458781","-123.213041")
    url = f"https://na-api.beta.inrix.com/Traffic/Inrix.ashx?Action=GetTrafficCameraImage&Token={token}&CameraID={min_id}&DesiredWidth=640&DesiredHeight=480"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    image = Image.open(BytesIO(response.content))
#
    images_folder = check_dir_exists()
    save_path = os.path.join(images_folder, f"camera_image_{min_id}.jpg")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    image.save(save_path, "JPEG")
    return save_path

return_data = ""

def find_substring(string, start_char, end_char):
    start_index = string.find(start_char)
    end_index = string.find(end_char, start_index + 1)
    if start_index != -1 and end_index != -1:
        return string[start_index + 1:end_index]
    return None

def get_last_integer(string):
    matches = re.findall(r'\d+', string)
    return int(matches[-1]) if matches else None


def get_rating():
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    client = boto3.client(
        service_name="bedrock-runtime",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name="us-west-2",
    )

    save_path = get_camera_image(token)

    image_path = save_path
    with open(image_path, 'rb') as image_file:
        image_binary = image_file.read()

    #input_text = "Take the image provided, and count the number of cars that you see on the road in the image. Then, output an integer value that says the number of cars. Only output one singular integer value and no text messages. Count the cars on the right side of the road. If you see two red dots that are almost parallel with each other, count that pair as a car."
    input_text = """
    Analyze the given image of a road with some level of traffic or the absence of traffic. Perform the following tasks:
	1.	Preprocessing:
	•	If the image orientation is incorrect (e.g., the camera is flipped), analyze it with the correct orientation.
	•	If no road or cars are visible, set the traffic congestion rating to 100.
	2.	Detection:
	•	Count all visible cars, including those farther away that may appear as black blobs.
	•	Identify the type of road in the image (e.g., highway, city street, rural road).
	3.	Environment Identification:
	•	Deduce the time of day (e.g., morning, afternoon, evening, or night) based on lighting conditions.
        If you see two red dots that are almost parallel with each other, count that pair as a car. This will usually occur in the night,
        where the average gradient of the image will be very low, and the red dots will be very close to each other.
	4.	Rating:
	•	Compute a traffic congestion rating from 0 (no congestion) to 100 (max congestion) based on the density and distribution of cars on the road.

    Output the analysis in the following JSON format only:
    {
        "number_of_cars": <integer>,
        "road_type": "<string>",
        "time_of_day": "<string>",
        "traffic_congestion_rating": <integer>
    }

    Example output given an image with a lot of cars in a small area in a city street:
    {
        "number_of_cars": 35,
        "road_type": "city street",
        "time_of_day": "daytime",
        "traffic_congestion_rating": 85
    }

    """

    message = {
            "role": "user",
            "content": [
                {
                    "text": input_text
                },
                {
                        "image": {
                            "format": 'jpeg',
                            "source": {
                                "bytes": image_binary
                            }
                        }
                }
            ]
        }

    messages = [message]

    model_id = "us.meta.llama3-2-90b-instruct-v1:0"

    response = client.converse(
        modelId=model_id,
        messages=messages
    )

    output = response['output']['message']

    for content in output['content']:
        rating = content['text']

    cleaned_rating = find_substring(rating, "{", "}")
    final_rating = get_last_integer(cleaned_rating)
    return_data = cleaned_rating
    return final_rating



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
            print("Move over, ambulance is coming!")
            break


if (evaluate_congestion(threshold)):
    print(f"{get_distance()} mi")

if (not evaluate_congestion(threshold)):
    print("There is not enough traffic")
else:
    checkdistance(get_distance())