import requests
import xml.etree.ElementTree as ET


def get_camera_info(xml):
    cameras = []
    for camera in xml.findall(".//Camera"):
        camera_id = camera.get("id")
        point = camera.find("Point")
        latitude = point.get("latitude")
        longitude = point.get("longitude")
        cameras.append({"id": camera_id, "latitude": latitude, "longitude": longitude})
    return cameras


def get_cameras_in_a_box(token, corner1, corner2):
    # Assumes corner1 and corner2 are strings in the format "latitude|longitude"
    # corner1 = "47.636521|-122.321498"
    # corner2 = "47.648940|-122.280300"
    url = f"https://na-api.beta.inrix.com/Traffic/Inrix.ashx?action=GetTrafficCamerasInBox&locale=en-US&corner1={corner1}&corner2={corner2}&token={token}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    root = ET.fromstring(response.text)
    camera_info = get_camera_info(root)

    print(camera_info)
    return camera_info
