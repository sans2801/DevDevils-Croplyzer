from flask import Flask
import os
import re
import operator
import requests
import json
import base64
from flask import request
import cv2
import numpy as np
import math
import sys
import tty
import termios
import pyimgur
import time
import pigpio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

imgur_client_id = os.environ['IMGUR_CLIENT']
imgur_client = pyimgur.Imgur(imgur_client_id)

imgur_headers = {"Authorization": "Client-ID my-client-id"}

imgur_api_key = os.environ['IMGUR_KEY']

imgur_url = "http://api.imgur.com/3/upload.json"

servo_1 = 4
servo_2 = 17
servo_3 = 4

MIN_WIDTH = 750
MAX_WIDTH = 2250

dit = pigpio.pi()
dit.set_servo_pulsewidth(servo_1, 1500)
dit.set_servo_pulsewidth(servo_2, 1500)
dit.set_servo_pulsewidth(servo_3, 1500)

debug = False
test = True

motor_1 = 26
motor_2 = 13
motor_3 = 6
motor_4 = 5

GPIO.setup(motor_1, GPIO.OUT)
GPIO.setup(motor_2, GPIO.OUT)
GPIO.setup(motor_3, GPIO.OUT)
GPIO.setup(motor_4, GPIO.OUT)

app = Flask(__name__)

def apply_mask(matrix, mask, fill_value):
    masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
    return masked.filled()


def apply_threshold(matrix, low_value, high_value):
    low_mask = matrix < low_value
    matrix = apply_mask(matrix, low_mask, low_value)

    high_mask = matrix > high_value
    matrix = apply_mask(matrix, high_mask, high_value)

    return matrix

def simplest_cb(img, percent):
    assert img.shape[2] == 3
    assert percent > 0 and percent < 100

    half_percent = percent / 200.0

    channels = cv2.split(img)

    out_channels = []
    for channel in channels:
        assert len(channel.shape) == 2
        # find the low and high precentile values (based on the input percentile)
        height, width = channel.shape
        vec_size = width * height
        flat = channel.reshape(vec_size)

        assert len(flat.shape) == 1

        flat = np.sort(flat)

        n_cols = flat.shape[0]

        low_val = flat[math.floor(n_cols * half_percent)]
        high_val = flat[math.ceil(n_cols * (1.0 - half_percent))]

        print("Lowval: ", low_val)
        print("Highval: ", high_val)

        # saturate below the low percentile and above the high percentile
        thresholded = apply_threshold(channel, low_val, high_val)
        # scale the channel
        normalized = cv2.normalize(
            thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
        out_channels.append(normalized)

    return cv2.merge(out_channels)


def motor1_forward():
    #Upward
    const_forward = 20
    start = dit.get_servo_pulsewidth(servo_1)
    delta = 10
    end = 1600
    incMove = (end-start)/100.0
    incTime = delta/100.0
    for x in range(1):
        dit.set_servo_pulsewidth(servo_1, int(1580))
        print(start+x*incMove, incTime)
        time.sleep(incTime)

    dit.set_servo_pulsewidth(servo_1, 0)
    print("motor1=1600")


def motor1_reverse():
    #Downward
    # dit.set_servo_pulsewidth(servos[0], 1500)
    const_reverse = 20
    start = dit.get_servo_pulsewidth(servo_1)
    print(start)
    delta = 10
    end = 750
    incMove = (end-start)/100.0
    incTime = delta/100.0
    for x in range(1):
        dit.set_servo_pulsewidth(servo_1, int(1440))
        print(start+x*incMove, incTime)
        time.sleep(incTime)

    dit.set_servo_pulsewidth(servo_1, 0)
    # print(dit.get_servo_pulsewidth(4))
    print("motor1=1400")


def motor1_stop():
    dit.set_servo_pulsewidth(servo_1, 1500)
    print(dit.get_servo_pulsewidth(servo_1))
    print("motor1=1500")


def motor2_forward():
    const_forward = 20
    start = dit.get_servo_pulsewidth(servo_2)
    delta = 10
    end = 1600
    incMove = (end-start)/100.0
    incTime = delta/100.0
    for x in range(2):
        dit.set_servo_pulsewidth(servo_2, int(1600))
        print(start+x*incMove, incTime)
        time.sleep(incTime)

    dit.set_servo_pulsewidth(servo_2, 0)
    print("motor2=1600")


def motor2_reverse():
    # dit.set_servo_pulsewidth(servos[0], 1500)
    const_reverse = 20
    start = dit.get_servo_pulsewidth(servo_2)
    print(start)
    delta = 10
    end = 1400
    incMove = (end-start)/100.0
    incTime = delta/100.0
    for x in range(1):
        dit.set_servo_pulsewidth(servo_2, int(1469))
        print(start+x*incMove, incTime)
        time.sleep(incTime)

    dit.set_servo_pulsewidth(servo_2, 0)
    # print(dit.get_servo_pulsewidth(4))
    print("motor2=1400")


def motor2_stop():
    dit.set_servo_pulsewidth(servo_2, 1500)
    print(dit.get_servo_pulsewidth(servo_2))
    print("motor2=1500")


def motor3_forward():
    start = dit.get_servo_pulsewidth(servo_3)
    print(start)
    delta = 100
    end = 2250
    # incMove=(end-start)/10.0
    incMove = 150
    incTime = delta/100.0
    for x in range(2):
        if int(start+x*incMove) >= MIN_WIDTH and int(start+x*incMove) <= MAX_WIDTH:
            # dit.set_servo_pulsewidth(17, int(start+x*incMove))
            dit.set_servo_pulsewidth(servo_3, int(start+x*incMove))
            # print(start+x*incMove, incTime)
            time.sleep(1)
        else:
            break

    dit.set_servo_pulsewidth(servo_3, 0)
    print(dit.get_servo_pulsewidth(servo_3))
    print("motor3=1600")


def motor3_reverse():

    start = dit.get_servo_pulsewidth(servo_3)
    print(start)
    delta = 100
    end = 750
    # incMove=(end-start)/10.0
    incMove = -150
    incTime = delta/100.0
    for x in range(2):
        if int(start+x*incMove) >= MIN_WIDTH and int(start+x*incMove) <= MAX_WIDTH:
            # dit.set_servo_pulsewidth(17, int(start+x*incMove))
            dit.set_servo_pulsewidth(servo_3, int(start+x*incMove))
            # print(start+x*incMove, incTime)
            time.sleep(1)
        else:
            break

    dit.set_servo_pulsewidth(servo_3, 0)
    print(dit.get_servo_pulsewidth(servo_3))
    print("motor3=1400")


def motor3_stop():
    dit.set_servo_pulsewidth(servo_3, 1500)
    print(dit.get_servo_pulsewidth(servo_3))
    print("motor3=1500")


def get_pwm(motor):
    print(dit.get_servo_pulsewidth(motor))

@app.route('/',  methods=['POST'])
def workflow():
    req = json.loads(request.data)
    val = req["service"]
    print(val)
    if val == "camera":
        cam = cv2.VideoCapture(0)
        ret, image = cam.read()
        # cv2.imshow('Imagetest', image)
        result = simplest_cb(image, 1)
        # cv2.imwrite('image2.jpg', image)
        cv2.imwrite('image-filtered.jpg', result)
        cam.release()
        uploaded_image = imgur_client.upload_image('image-filtered.jpg') 
        print(uploaded_image.link)  
        return uploaded_image.link

    if val == "footage":
        cam = cv2.VideoCapture(0)
        ret, image = cam.read()
        cv2.imwrite('image-normal.jpg', image)
        cam.release()
        # _, im_arr = cv2.imencode('.jpg', image)  # im_arr: image in Numpy one-dim array format.
        # im_bytes = im_arr.tobytes()
        # im_b64 = base64.b64encode(im_bytes)
        uploaded_image = imgur_client.upload_image('image-normal.jpg') 
        print(uploaded_image.link)     
        return uploaded_image.link

    if val == "forward":
        delay = req["time"]
        GPIO.output(motor_1, True)
        GPIO.output(motor_3, True)
        time.sleep(delay)
        GPIO.output(motor_1, False)
        GPIO.output(motor_3, False)
        time.sleep(1)
        return "Moved Forward"

    if val == "right":
        GPIO.output(motor_1, True)
        time.sleep(2)
        GPIO.output(motor_1, False)
        return "Moved Right"

    if val == "left":
        GPIO.output(motor_3, True)
        time.sleep(2)
        GPIO.output(motor_3, False)
        return "Moved Left"

    if val == "backward":
        delay = req["time"]
        GPIO.output(motor_2, True)
        GPIO.output(motor_4, True)
        time.sleep(delay)
        GPIO.output(motor_2, False)
        GPIO.output(motor_4, False)
        time.sleep(1)
        return "Moved Backward"

    if val == "motor1":
        direction = req["direction"]
        if direction == "upward":
            motor1_forward()
            return "Motor1 - Upward"
        elif direction == "downward":
            motor1_reverse()
            return "Motor1 - Downward"
        else:
            motor1_stop()
            return "Motor1 - Stop"

    if val == "motor2":
        direction = req["direction"]
        if direction == "backward":
            motor2_forward()
            return "Motor2 - Backward"
        elif direction == "forward":
            motor2_reverse()
            return "Motor2 - Forward"
        else:
            motor2_stop()
            return "Motor2 - Stop"

    if val == "motor3":
        direction = req["direction"]
        if direction == "right":
            motor3_forward()
            return "Motor3 - Right"
        elif direction == "left":
            motor3_reverse()
            return "Motor3 - Left"
        else:
            motor3_stop()
            return "Motor3 - Stop"

    print("Nothing specified")
    return "None"


if __name__ == "__main__":
    app.run()