from flask import Flask, request, jsonify
from Token import get_token
from CamerasBox import get_cameras_in_a_box
from CameraImage import get_camera_image

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


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
    



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
