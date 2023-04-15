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


if __name__ == "__main__":
    app.run()