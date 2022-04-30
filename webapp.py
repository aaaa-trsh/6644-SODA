from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
# from lib.camera import VideoCapture
import base64
import cv2
import numpy as np
from subsystems.drive import Drivetrain
from lib.pid import PID
import pigpio
import atexit

pi = pigpio.pi()
drivetrain = Drivetrain(pi)
atexit.register(lambda: pi.stop())
l_controller = PID(0.5, 0.06, 0, 0) 
r_controller = PID(0.5, 0.06, 0, 0) 
app = Flask(__name__)
# app.debug = False
socketio = SocketIO(app)
cap = None#VideoCapture('libcamerasrc ! video/x-raw,framerate=100/1,width=640,height=480 ! videoscale ! videoconvert ! appsink drop=true sync=false')

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("update_pose")
def update_pose(_):
    def clamp(x, _min, _max):
        return max(_min, min(x, _max))
    drivetrain.tank_drive(
        clamp(l_controller.calculate(-drivetrain.get_left_distance(), 0), -.2, .2), 
        clamp(r_controller.calculate(-drivetrain.get_right_distance(), 0), -.2, .2)
    )
    drivetrain.periodic()
    emit("pose", {
        "left_dist":drivetrain.get_left_distance(),
        "right_dist":drivetrain.get_right_distance()
    })

# def update_pose(left_dist, right_dist, x, y):
#     emit("pose", {"left_dist": left_dist, "right_dist": right_dist, "x": x, "y": y})

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

socketio.run(app, host="0.0.0.0")