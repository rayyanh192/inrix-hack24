import requests
from PIL import Image
from io import BytesIO
from flask import send_file
from CamerasBox import get_camera_info, optimize_cameras, saveOutput
from Token import get_token
import os

min_id = saveOutput()

token = get_token()

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


def get_camera_image(min_id, token):
    url = f"https://na-api.beta.inrix.com/Traffic/Inrix.ashx?Action=GetTrafficCameraImage&Token={token}&CameraID={min_id}&DesiredWidth=640&DesiredHeight=480"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    image = Image.open(BytesIO(response.content))

    images_folder = check_dir_exists()
    save_path = os.path.join(images_folder, f"camera_image_{min_id}.jpg")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    image.save(save_path, "JPEG")
    return save_path



get_camera_image(min_id, token)
#print(f"Image saved at {save_path}")
