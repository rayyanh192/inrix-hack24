import requests
from PIL import Image
from io import BytesIO
from flask import send_file
from CamerasBox import get_camera_info, optimize_cameras, saveOutput
from Token import get_token
import os

min_id = saveOutput()

token = get_token()
save_dir = "/Users/rayyan/Documents/inrix-hack24/images"


def get_camera_image(min_id, token):
    url = f"https://na-api.beta.inrix.com/Traffic/Inrix.ashx?Action=GetTrafficCameraImage&Token={token}&CameraID={min_id}&DesiredWidth=640&DesiredHeight=480"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    image = Image.open(BytesIO(response.content))
    save_path = os.path.join(save_dir, f"camera_image_{min_id}.jpg")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    image.save(save_path, "JPEG")
    return save_path



get_camera_image(min_id, token)
#print(f"Image saved at {save_path}")
