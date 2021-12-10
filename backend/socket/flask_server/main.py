
from environment import *
import RPi.GPIO as GPIO
from qrReader import *
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor
from MiniPIR import GroveMiniPIRMotionSensor
import peopleInRoom
import socket
import csv
import argparse
import datetime
import imutils
import time
import cv2
import json
import unicodedata
import eventlet
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from flask import Response
from flask import request
from flask import Flask
from imutils.video import VideoStream
from pyzbar import pyzbar
import seeed_dht
from grove.display import JHD1802
import UltrasonicSensor
from flask import render_template
import threading
import base64

# Socket for Thread 2
eventlet.monkey_patch()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dreamchaser'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")
# Socket for Thread 1
HOST = '192.168.0.105'
PORT = 4000
s = socket.socket()
host = socket.gethostname()
# Buzzer and GPIO for Task 1, 2
outputFrame = None
Buzzer_sig = 12 #Buzzer PIN
GPIO_SIG = 5 # Ultrasonic PIN
DISTANCE = 20
entrance = 0
users = None

def getAndPrint():
    # Connection setup
    print("Estabilishing connection to server zZz...")
    s.connect((HOST, 4000))
    print("SeeedStudio Grove Ultrasonic get data and print")
    
    # loop basically forever, until keyboardInterrupt Ctrl + C
    #for i in range(10000):
    while True:
        miniPir() #this function is called first
        measurementInCM()
        
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
        print('humidity: {}%, temperature: {} C, moisture: {}'.format(humi, temp, m))
        s.sendall(bytes('humidity {} celcius {} moisture {} measurements'.format(humi, temp, m), "utf8"))
        
def miniPir():
    pir = GroveMiniPIRMotionSensor(22) #Mini PIR Motion

    def callback():
        print("The number of people who passed this area: {}".format(pir.count))
    
    pir.on_detect = callback        
    
    while True:
        try:
            measurementInCM() # this function is called after the miniPir function is called
            air()
            #time.sleep(0.5)
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
            print(info)
            writer.writerow(info) 

def measurementPulse(start, stop):

    #print("Ultrasonic Measurement")

    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distance / 2

    print("Distance : {:10.2f} CM".format(distance))
    
    if (distance < DISTANCE) and (peopleInRoom.leavingNoQR is 1 and peopleInRoom.full is 0):
        #if people passing through the ultrasonic and is leaving
        peopleInRoom.leavingNoQR = 0
        entrance = 1
        if (peopleInRoom.leavingUpdate == 1):
            peopleInRoom.leavingUpdate = 0
            s.sendall(bytes('Current No.:{}'.format(peopleInRoom.pp), "utf8"))
            print("Number of people in the room: {}".format(peopleInRoom.pp))
    elif (distance < DISTANCE) and (peopleInRoom.leavingNoQR is 0):
        entrance = 0
        peopleInRoom.leavingDect = 1
    else:
        entrance = 0
    
    if entrance is 1:
        print("entry detected")
        numPeople = peopleInRoom.pp
        if (users == None):
           getUserList()
        barcodeData = qrMain()
        print("QR Finish")
        if (barcodeData != None):
            if ("LegitBarcode" in barcodeData):
                print(barcodeData)
                #s.sendall(bytes('{}'.format(barcodeData), "utf8"))
                print("Number of people in the room: {}".format(peopleInRoom.pp))

def qrDectector():
 
    # construct the argument parser and parse the arguments
    print("QR detector started")
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
        help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())
    
    ### From there, let’s initialize our video stream and open our CSV file:
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")

    vs = VideoStream(src=0).start()                 
    time.sleep(2.0)

    qrFlag = False
    legitFlag = False
     
    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far
    csv = open("users.csv", "r+")
    found = set()
    
    lcd = JHD1802()
    lcd.setCursor(0, 0)
    print(csv)
     
    start = time.time()
    #print("start: " , start)
    
    ### Let’s begin capturing + processing frames:
    # loop over the frames from the video stream
    try:
        while True:
            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            # find the barcodes in the frame and decode each of the barcodes
            barcodes = pyzbar.decode(frame)

        ### Let’s proceed to loop over the detected barcodes
        # loop over the detected barcodes
            for barcode in barcodes:
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
        
                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode to disk and update the set
                
                #if 's3755614,Tran Kim Long,0797999956' in csv.read():
                if barcodeData in csv.read():
                    print("Users Get Successfully")
                    if peopleInRoom.pp < 2: # If QR Code is valid and there are still rooms for more
                        peopleInRoom.pp = peopleInRoom.pp + 1
                        lcd.setCursor(0,0)
                        lcd.write('Welcome to the')
                        lcd.setCursor(1,0)
                        lcd.write('room, bitches!')
                        UltrasonicSensor.smallBuzzing() # Buzz small and cool
                        print("Welcome!")
                        legitFlag = True
                        qrFlag = True
                    else:# Signal the room is currently full
                        lcd.setCursor(0,0)
                        lcd.write('Sorry, the room')
                        lcd.setCursor(1,0)
                        lcd.write('is full!')
                        print("Over 5 people in the room")
                        UltrasonicSensor.loudBuzzing() # Buzz loud and clear
                        time.sleep(4.5)
                        peopleInRoom.leavingNoQR = 0
                        qrFlag = True
                else: #If Invalid QR Code is scanned
                    """
                    csv.write("{}\n".format(barcodeData))
                    csv.flush()
                    found.add(barcodeData)
                    print("{}\n".format(barcodeData))
                        
                    """
                    UltrasonicSensor.smallBuzzing() # Buzz small and cool
                    lcd.setCursor(0, 0)
                    lcd.write('QR code is not')
                    lcd.setCursor(1, 0)
                    lcd.write('in the database')
                    print("QR code is not in the database")
                    time.sleep(4.5)
                    peopleInRoom.leavingNoQR = 0
                    qrFlag = True

                    # show the output frame
            cv2.imshow("Barcode Scanner", frame)
            key = cv2.waitKey(1) & 0xFF
            
            
            #print("timer: ", time.time() - start)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
                # if not flag:
                #     continue
            yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                bytearray(encodedImage) + b'\r\n')
            
            if (time.time() - start) > 10.0:
                peopleInRoom.leavingNoQR = 1
                cv2.destroyAllWindows()
                vs.stop()
                break
        
            if qrFlag is True:
                peopleInRoom.leavingDect = 0
                peopleInRoom.leavingNoQR = 0
                time.sleep(3.5)
                peopleInRoom.leavingNoQR = 0
                print("[INFO] cleaning up...")
                lcd.clear()
                lcd.setCursor(0,0)
                lcd.write('Please scan QR')
                # close the output CSV file do a bit of cleanup                
                csv.close()
                cv2.destroyAllWindows()
                vs.stop()
                break
                if legitFlag is True:
                    return ("LegitBarcode:{}:{}:\n".format(barcodeData,peopleInRoom.pp))
                else:
                    return ("{},{}\n".format(datetime.datetime.now(),barcodeData))
    finally:
        print('QR Reading Ended')
    return None

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RunTimeError("Run Time Error")
    func()

@app.route("/video_feed")
@cross_origin()
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(qrDectector(),
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

    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True, use_reloader=False)
    print("Flask running on localhost:"+str(PORT))

    t = threading.Thread(target=getAndPrint)
    t.start()
    
    # video stream service
    t2 = threading.Thread(target=qrDectector)
    t2.daemon = True
    t2.start()