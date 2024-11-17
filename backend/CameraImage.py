import requests
from PIL import Image
from io import BytesIO
from flask import send_file


def get_camera_image(camera_id, token):
    url = f"https://na-api.beta.inrix.com/Traffic/Inrix.ashx?Action=GetTrafficCameraImage&Token={token}&CameraID={camera_id}&DesiredWidth=640&DesiredHeight=480"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    image = Image.open(BytesIO(response.content))
    img_io = BytesIO()
    image.save(img_io, "JPEG")
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")
