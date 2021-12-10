import RPi.GPIO as GPIO
from qrReader import *
import time
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor
from MiniPIR import GroveMiniPIRMotionSensor
import peopleInRoom
import socket
import csv
import json
import unicodedata
import threading
import argparse
import datetime
import imutils
import time
import cv2
import json
import unicodedata

HOST = '192.168.137.1'
PORT = 4000
s = socket.socket()
host = socket.gethostname()

# CONST
Buzzer_sig = 12  # Buzzer PIN
GPIO_SIG = 5  # Ultrasonic PIN
DISTANCE = 68
entrance = 0
users = None


def getAndPrint():
    # Connection setup
    print("Estabilishing connection to server...")
    # s.connect((HOST, 4000))
    print("SeeedStudio Grove Ultrasonic get data and print")

    # loop basically forever, until keyboardInterrupt Ctrl + C
    # for i in range(10000):
    while True:
        miniPir()  # this function is called first
        measurementInCM()

    # Reset GPIO settings
    GPIO.cleanup()


def air():
    # for DHT11/DHT22
    PIN = 0  # Moisture sensor PIN
    sensor = seeed_dht.DHT("11", 16)  # Temperature and humidity sensor
    sensor2 = GroveMoistureSensor(PIN)

    # print('Detecting enviroment detail...')
    humi, temp = sensor.read()
    m = sensor2.moisture
    # if not humi or not m is None:
    # print('humidity: {}%, temperature: {} C, moisture: {}'.format(humi, temp, m))
    # s.sendall(bytes('humidity {} celcius {} moisture {} measurements'.format(humi, temp, m), "utf8"))
    # s.sendall(bytes('Hello from Pi, collecting data!', "utf8"))


def miniPir():
    pir = GroveMiniPIRMotionSensor(22)  # Mini PIR Motion

    def callback():
        print("The number of people who passed this area: {}".format(pir.count))

    pir.on_detect = callback

    while True:
        try:
            measurementInCM()  # this function is called after the miniPir function is called
            time.sleep(0.7)
            air()
        finally:
            GPIO.cleanup


def smallBuzzing():  # Sound of buzzer when the number of people does not exceed 5
    GPIO.setup(Buzzer_sig, GPIO.OUT)
    GPIO.output(Buzzer_sig, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(Buzzer_sig, GPIO.LOW)


def loudBuzzing():  # The sound of buzzer becomes loud and irritating when number of people exceed 5
    GPIO.setup(Buzzer_sig, GPIO.OUT)
    GPIO.output(Buzzer_sig, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(Buzzer_sig, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(Buzzer_sig, GPIO.HIGH)
    time.sleep(1.5)
    GPIO.output(Buzzer_sig, GPIO.LOW)


def measurementInCM():
    # setup the GPIO_SIG as output
    GPIO.setup(GPIO_SIG, GPIO.OUT)
    # GPIO.setup(LED, GPIO.OUT)

    GPIO.output(GPIO_SIG, GPIO.LOW)
    time.sleep(0.0001)
    GPIO.output(GPIO_SIG, GPIO.HIGH)
    time.sleep(0.0001)
    GPIO.output(GPIO_SIG, GPIO.LOW)
    start = time.time()

    # setup GPIO_SIG as input
    GPIO.setup(GPIO_SIG, GPIO.IN)

    # get duration from Ultrasonic SIG pin
    while GPIO.input(GPIO_SIG) == 0:
        start = time.time()

    while GPIO.input(GPIO_SIG) == 1:
        stop = time.time()

    measurementPulse(start, stop)


def getUserList():
    # Calling Socket
    # s.sendall(bytes('getUsers', "utf8"))
    data = s.recv(1024)
    # print("data: {}".format(data))
    users = data.decode("utf8")
    y = json.loads(users)
    with open('users.csv', 'w', newline='', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)
        for user in y:
            info = [user["student_id"], user["name"], user["phone_number"]]
            print(info)
            writer.writerow(info)


def measurementPulse(start, stop):
    # print("Ultrasonic Measurement")

    # Calculate pulse length
    elapsed = stop - start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distance / 2

    print("Distance : {:10.2f} CM".format(distance))

    if (distance < DISTANCE) and (peopleInRoom.leavingNoQR is 1 and peopleInRoom.full is 0):
        # if people passing through the ultrasonic and is leaving
        peopleInRoom.leavingNoQR = 0
        entrance = 1
        # if (peopleInRoom.leavingUpdate == 1):
        # peopleInRoom.leavingUpdate = 0
        # s.sendall(bytes('Current No.:{}'.format(peopleInRoom.pp), "utf8"))
        # print("Number of people in the room: {}".format(peopleInRoom.pp))
    elif (distance < DISTANCE) and ((peopleInRoom.leavingNoQR is 0) or peopleInRoom.full is 2):
        entrance = 0
        peopleInRoom.leavingDect = 1
        print("Leaving...")
    else:
        entrance = 0

    if entrance is 1:
        print("entry detected")
        numPeople = peopleInRoom.pp
        # if (users == None):
        # print("Get User List")
        # getUserList()
        barcodeData = qrDectector(numPeople)
        print("QR Finish")
        if (barcodeData != None):
            if ("LegitBarcode" in barcodeData):
                # print(barcodeData)
                # s.sendall(bytes('{}'.format(barcodeData), "utf8"))
                print("Number of people in the room: {}".format(peopleInRoom.pp))
