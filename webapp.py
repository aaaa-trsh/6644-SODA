from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from lib.camera import VideoCapture
import base64
import cv2
import numpy as np

app = Flask(__name__)
socketio = SocketIO(app)
cap = VideoCapture('libcamerasrc ! video/x-raw,framerate=100/1,width=640,height=480 ! videoscale ! videoconvert ! appsink drop=true sync=false')

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("data")
def data(_):
    frame = cap.read() if cap else np.zeros((1, 1, 3), np.uint8)
    frame = cv2.resize(frame, (120, 80))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, buffer = cv2.imencode(".jpg", frame)
    emit("video_feed", base64.b64encode(buffer).decode("utf-8"))

def update_pose(left_dist, right_dist, x, y):
    emit("pose", {"left_dist": left_dist, "right_dist": right_dist, "x": x, "y": y})

@socketio.on("video_feed")
def video_feed(_):
    frame = cap.read() if cap else np.zeros((1, 1, 3), np.uint8)
    frame = cv2.resize(frame, (120, 80))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, buffer = cv2.imencode(".jpg", frame)
    emit("video_feed", {
            "img": base64.b64encode(buffer).decode("utf-8")
        }
    )
    
# if __name__ == "__main__":
socketio.run(app, host="0.0.0.0")