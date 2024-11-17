import boto3
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv
from CameraImage import get_camera_image
from CamerasBox import saveOutput
from Token import get_token
import re

load_dotenv()

min_id = saveOutput()
token = get_token()

save_path = get_camera_image(min_id, token)

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



rating = get_rating()
print(rating)