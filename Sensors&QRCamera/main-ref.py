from environment import *

import RPi.GPIO as GPIO

import seeed_dht

from grove.grove_moisture_sensor import GroveMoistureSensor

from MiniPIR import GroveMiniPIRMotionSensor

import peopleInRoom

import socket

import csv

import argparse

from UltrasonicSensor import *

import datetime

import imutils

import time

import cv2

import json

import unicodedata

from flask_cors import CORS, cross_origin

from flask_socketio import SocketIO

from flask import Response

from flask import request

from flask import Flask

from imutils.video import VideoStream

from pyzbar import pyzbar

import seeed_dht

#from grove.display import JHD1802

from flask import render_template

import threading

import base64



# Socket for Thread 2

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dreamchaser'

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

socketio = SocketIO(app, cors_allowed_origins="*")



# Socket for Thread 1

HOST = '10.247.207.228'

PORT = 4000

s = socket.socket()

host = socket.gethostname()



# Buzzer and GPIO for Task 1, 2

users = None

qrFlag = False

legitFlag = False

timeFlag = False

checkQR = False

Buzzer_sig = 12 #Buzzer PIN

GPIO_SIG = 5 # Ultrasonic PIN

DISTANCE = 68

entrance = 0

frame = None

lcd = JHD1802()

lcd.setCursor(0, 0)

global thread_count

global csvfile

numPeople = 0

sensor_sleep = False

startTime = 0



def getAndPrint():

    

    # Connection setup

    print("Waiting for connection to python socket server...")

    s.connect((HOST, 4000))

    s.sendall(bytes('resetPeopleCount', "utf8"))

    getUserList()



    print("SeeedStudio Grove Ultrasonic get data and print")

    # loop basically forever, until keyboardInterrupt Ctrl + C

    

    thread_count = 0

    while True:

        #thread_count = thread_count +1

        #(thread_count)

        miniPir() #this function is called first

        measurementInCM()

        time.sleep(1)

        

    # Reset GPIO settings

    GPIO.cleanup()



def air():    



    # for DHT11/DHT22

    PIN = 0 #Moisture sensor PIN

    sensor = seeed_dht.DHT("11",16) # Temperature and humidity sensor

    sensor2 = GroveMoistureSensor(PIN)



    #print('Detecting enviroment detail...')

    humi, temp = sensor.read()

    m = sensor2.moisture

    if not humi or not m is None:

        #print('humidity: {}%, temperature: {} C, moisture: {}'.format(humi, temp, m))

        s.sendall(bytes('humidity {} celcius {} moisture {} measurements:'.format(humi, temp, m), "utf8"))



def miniPir():

    pir = GroveMiniPIRMotionSensor(22) #Mini PIR Motion

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



def smallBuzzing(): # Sound of buzzer when the number of people does not exceed 5 

    GPIO.setup(Buzzer_sig, GPIO.OUT)

    GPIO.output(Buzzer_sig, GPIO.HIGH)

    time.sleep(0.2)

    GPIO.output(Buzzer_sig, GPIO.LOW)

    



def loudBuzzing(): # The sound of buzzer becomes loud and irritating when number of people exceed 5

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



    #GPIO.setup(LED, GPIO.OUT)

    GPIO.output(GPIO_SIG, GPIO.LOW)

    time.sleep(0.2)

    GPIO.output(GPIO_SIG, GPIO.HIGH)

    time.sleep(0.5)

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

    s.sendall(bytes('getUsers', "utf8"))

    data = s.recv(1024)

    #print("data: {}".format(data))

    users = data.decode("utf8")

    y = json.loads(users)

    with open('users.csv', 'w', newline='', encoding='UTF8') as f:

        # create the csv writer

        writer = csv.writer(f)

        for user in y:

            info = [user["student_id"], user["name"], user["phone_number"]]

            #print(info)

            writer.writerow(info) 



def measurementPulse(start, stop):

    global checkQR

    global sensor_sleep

    global numPeople

    global startTime

    global timeFlag

    #print("Ultrasonic Measurement")

    # Calculate pulse length

    elapsed = stop-start

    # Distance pulse travelled in that time is time

    # multiplied by the speed of sound (cm/s)

    distance = elapsed * 34300



    # That was the distance there and back so halve the value

    distance = distance / 2

    print("Distance : {:10.2f} CM".format(distance))



    if (sensor_sleep):

        sensor_sleep = False

        time.sleep(3)



    if (peopleInRoom.pendingUpdate == 1):

        peopleInRoom.pendingUpdate == 0

        #print("Number of people in the room: {}".format(peopleInRoom.pp))

        s.sendall(bytes('updateLeave :{}'.format(peopleInRoom.pp), "utf8"))

        time.sleep(3)



    if (distance < DISTANCE) and (peopleInRoom.leavingNoQR is 1 and peopleInRoom.full is 0):

        #if people passing through the ultrasonic and is leaving

        peopleInRoom.leavingNoQR = 0

        entrance = 1

        if (peopleInRoom.leavingUpdate == 1):

            peopleInRoom.leavingUpdate = 0



    elif (distance < DISTANCE) and ((peopleInRoom.leavingNoQR is 0) or peopleInRoom.full is 2):

        entrance = 0

        peopleInRoom.leavingDect = 1

        print("Leaving...")

        

    else:

        entrance = 0



    if entrance == 1:

        print("entry detected")

        numPeople = peopleInRoom.pp

        if (users == None):

           getUserList()

        #s.sendall(bytes('QR-Camera'.format(),"utf8"))

        UltrasonicSensor.smallBuzzing()

        checkQR = True

        s.sendall(bytes('message :QR Check!', "utf8"))

        startTime = time.time()

        timeFlag = True

        #print("QR Finish")

            

def startVideoStream():

    global checkQR

    global qrFlag

    global startTime

    global timeFlag

    count = 0

    print("[INFO] starting video stream...")

    vs = VideoStream(src=0).start()      

    time.sleep(3)

    print("Reading frame")

    

    try:

        while True:

            # grab the frame from the threaded video stream and resize it to

            # have a maximum width of 400 pixels

            frame = vs.read()

            frame = imutils.resize(frame, width=400)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # print("Frame Processed")

            # find the barcodes in the frame and decode each of the barcodes

            #Function should call here

            #print(checkQR)

            if (checkQR):

                lcd.clear()

                lcd.setCursor(0,0)

                lcd.write('Please scan QR')

                barcodes = pyzbar.decode(frame)

                for barcode in barcodes:

                    # extract the bounding box location of the barcode and draw

                    # the bounding box surrounding the barcode on the image

                    (x, y, w, h) = barcode.rect

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                

                    # the barcode data is a bytes object so if we want to draw it

                    # on our output image we need to convert it to a string first

                    barcodeData = barcode.data.decode("utf-8")

                    barcodeType = barcode.type

                    print(barcodeData)

                    # draw the barcode data and barcode type on the image

                    text = "{} ({})".format(barcodeData, barcodeType)

                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    csvfile = open("users.csv", "r+")

                    found = set()

                    x = (csvfile.read()).split('\n')

                    count = 0

                    for row in x:

                        print(row)

                        if barcodeData == row:

                            if numPeople < 5: # If QR Code is valid and there are still rooms for more

                                peopleInRoom.pp = peopleInRoom.pp + 1

                                lcd.setCursor(0,0)

                                lcd.write('Welcome to the')

                                lcd.setCursor(1,0)

                                lcd.write('room, ^_^!')

                                UltrasonicSensor.smallBuzzing() # Buzz small and cool

                                print("Welcome!")

                                legitFlag = True

                                qrFlag = True

                                print("peopleInRoom.pp: {}".format(peopleInRoom.pp))

                                s.sendall(bytes('updateJoin :{}:{}'.format(barcodeData, peopleInRoom.pp), "utf8"))

                                print(barcodeData)

                                break

                                

                            else:# Signal the room is currently full

                                lcd.setCursor(0,0)

                                lcd.write('Sorry, the room')

                                lcd.setCursor(1,0)

                                lcd.write('is full!')

                                print("Over 5 people in the room")

                                UltrasonicSensor.loudBuzzing() # Buzz loud and clear

                                qrFlag = True

                                peopleInRoom.full = 1

                                break

                            

                        elif (count == len(x) - 1):

                            UltrasonicSensor.smallBuzzing() # Buzz small and cool

                            lcd.setCursor(0, 0)

                            lcd.write('QR code is not')

                            lcd.setCursor(1, 0)

                            lcd.write('in the database')

                            print("QR code is not in the database")

                            peopleInRoom.leavingNoQR = 0

                            qrFlag = True

                            sensor_sleep = True

                            break



                        if (count == len(x) - 1):

                            break

                        count = count + 1

                        

            cv2.imshow("Barcode Scanner", frame)

            key = cv2.waitKey(1) & 0xFF

            #print("timer: ", time.time() - start)

            (flag, encodedImage) = cv2.imencode(".jpg", frame)

            #print("Image Frame Yield!")

            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 

                bytearray(encodedImage) + b'\r\n')

            

            if (timeFlag):

                if (time.time() - startTime) > 10.0:

                    peopleInRoom.leavingNoQR = 1

                    checkQR = False 

                    #UltrasonicSensor.loudBuzzing() # Buzz loud and clear

                    s.sendall(bytes('message :QR Scan is done', "utf8"))

                    startTime = 0

                    timeFlag = False



            if qrFlag is True:

                peopleInRoom.leavingDect = 0

                peopleInRoom.leavingNoQR = 0

                checkQR = False

                print("[INFO] cleaning up...")

                count = count + 1

                startTime = 0 

                timeFlag = False

                time.sleep(5)



                if (count > 1 and qrFlag == True):

                    qrFlag = False

                    lcd.clear()

                    lcd.setCursor(0,0)

                    lcd.write('Please scan QR')

                    s.sendall(bytes('message :QR Scan is done', "utf8"))

                    count = 0

                

    finally:

        print('QR Reading Ended')



def shutdown_server():

    func = request.environ.get('werkzeug.server.shutdown')

    if func is None:

        raise RunTimeError("Run Time Error")

    func()



# Flask Server Endpoints

@app.route("/video_feed")

@cross_origin()

def video_feed():

    # return the response generated along with the specific media

    # type (mime type)

    return Response(startVideoStream(),

        mimetype = "multipart/x-mixed-replace; boundary=frame")



@app.route("/shutdown")

@cross_origin()

def shutdown():

    shutdown_server()

    return 'QR Camera Shutting Down...'



if __name__ == '__main__':

     # GPIO Setup

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(12, GPIO.IN)

    GPIO.setup(5, GPIO.IN)

    GPIO.setup(0, GPIO.IN)



    t = threading.Thread(target=getAndPrint)

    t.start()



    ap = argparse.ArgumentParser()

    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",

        help="path to output CSV file containing barcodes")

    args = vars(ap.parse_args())

    

    #lcd = JHD1802()

    #lcd.setCursor(0, 0)



    print("Flask running on localhost:"+str(PORT))

    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True, use_reloader=False)



    # video stream service

    t2 = threading.Thread(target=startVideoStream)

    t2.daemon = True

    t2.start()



