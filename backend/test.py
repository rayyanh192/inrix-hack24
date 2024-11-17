import boto3
import base64
from PIL import Image
import io
import os
from dotenv import load_dotenv

load_dotenv()


def get_rating():
    access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    client = boto3.client(
        service_name="bedrock-runtime",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        region_name="us-west-2",
    )

    camera_branch
    image_path = '/Users/rayyan/Downloads/postmantraffic4.jpeg'
    with open(image_path, 'rb') as image_file:
        image_binary = image_file.read()

    #input_text = "Take the image provided, and count the number of cars that you see on the road in the image. Then, output an integer value that says the number of cars. Only output one singular integer value and no text messages. Count the cars on the right side of the road. If you see two red dots that are almost parallel with each other, count that pair as a car."
    input_text = """
    Take the image provided, and count the number of cars that you see on the road in the image. Then, output an integer value that says
    the number of cars. Only output one singular integer value and no text messages. Count the cars on the right side of the road. If you
    see two red dots that are almost parallel with each other, count that pair as a car.
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

    #print(f"Role: {output['role']}")

    for content in output['content']:
        rating = content['text']
        #print(f"Text: {content['text']}")

    return rating


rating = get_rating()
print(rating)