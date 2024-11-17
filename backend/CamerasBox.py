import requests
import xml.etree.ElementTree as ET
from Token import get_token
import math

token = get_token()
corner1 = "37.458781|-123.213041"
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
def saveOutput():
    return optimize_cameras(get_camera_info(root))
