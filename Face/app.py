from flask import Flask, request, jsonify, render_template
from fer import FER
import cv2
import numpy as np
import base64
import os

# Define the Flask app
app = Flask(__name__, 
            static_folder="static",  # Folder for static files
            template_folder="templates"  # Folder for template files
            )

# Emotion detector setup
detector = FER()

# Route to render the main page (index.html)
@app.route("/")
def index():
    return render_template("Face-Expression.html")  # Ensure this file exists in the 'templates' folder

# Route to process the frame and detect emotions
@app.route("/process_frame", methods=["POST"])
def process_frame():
    frame_data = request.data
    frame_data = base64.b64decode(frame_data.split(b",")[1])  # Decode the image data
    np_image = np.frombuffer(frame_data, np.uint8)
    frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

    emotions = detector.detect_emotions(frame)
    if emotions:
        dominant_emotions = emotions[0]['emotions']
        dominant_emotion = max(dominant_emotions, key=dominant_emotions.get)
        return jsonify({"dominant_emotion": dominant_emotion})

    return jsonify({"error": "No emotions detected"})

if __name__ == "__main__":
    # Flask will automatically look for templates in the 'templates' folder
    app.run(debug=True)
