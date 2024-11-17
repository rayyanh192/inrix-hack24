from flask import Flask, request, jsonify
from Token import get_token
from CamerasBox import get_cameras_in_a_box
from CameraImage import get_camera_image

app = Flask(__name__)


# Example URL: localhost:3000/token
@app.route("/token")
def get_token_route():
    token = get_token()
    return jsonify({"token": token})


# Example URL: localhost:3000/cameras?token=TOKEN&corner1=LAT|LONG&corner2=LAT|LONG
@app.route("/cameras")
def get_cameras_route():
    token = request.args.get("token")
    corner1 = request.args.get("corner1")
    corner2 = request.args.get("corner2")
    if not token or not corner1 or not corner2:
        return jsonify({"error": "Token or geobox corners not found. Please provide."})
    cameras = get_cameras_in_a_box(token)
    return jsonify({"cameras": cameras})


# Example URL: localhost:3000/camera-image?camera_id=CAMERA_ID&token=TOKEN
@app.route("/camera-image")
def get_camera_image_route():
    # get image
    camera_id = request.args.get("camera_id")
    token = request.args.get("token")
    if not camera_id or not token:
        return jsonify({"error": "Camera ID or token not found. Please provide."})
    image = get_camera_image(camera_id, token)
     
     # anayling image
     #image
    
@app.route("/contact-frontend")
def contact_frontend():

    import requests
    from random import randint
    import googlemaps
    from dotenv import load_dotenv
    import time
    import os
    from test import get_rating

    load_dotenv()
    api_key = os.getenv("API_KEY")

    def main():
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


    main()

    return jsonify({"message": "Hello, frontend!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
