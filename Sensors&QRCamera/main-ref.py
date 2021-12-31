from environment import *
import RPi.GPIO as GPIO
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor
import peopleInRoom
import socket
from qrReader import *
import csv
from requestService import *
import argparse
#from UltrasonicSensor import *
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

# # Socket for Thread 1
# HOST = '192.168.137.1'
# PORT = 4000
# s = socket.socket()
# host = socket.gethostname()

# Buzzer and GPIO for Task 1, 2
debounceFlag = False
users = None
qrFlag = False
legitFlag = False
reLaunch = False
timeFlag = False
checkQR = False
Buzzer_sig = 12 #Buzzer PIN
GPIO_SIG = 5 # Ultrasonic PIN
GPIO_SIG2 = 22
DISTANCE = 68
entrance = 0
lcd = JHD1802()
lcd.setCursor(0, 0)
global thread_count
global csvfile
numPeople = 0
startTime = 0
time_counter = [0.0,0.0]
range = [0.0,0.0]
peopleInRoom.welcomeIn = 0
peopleInRoom.welcomeOut = 0
freezeSensors = 0

def getAndPrint():
    # Connection setup
    # print("Waiting for connection to python socket server...")
    # s.connect((HOST, 4000))
    # s.sendall(bytes('resetPeopleCount', "utf8"))
    # getUserList()

    print("SeeedStudio Grove Ultrasonic get data and print")
    # loop basically forever, until keyboardInterrupt Ctrl + C
    
    thread_count = 0
    while True:
        measurementInCM()
        
    # Reset GPIO settings
    GPIO.cleanup()

def air():    
    # for DHT11/DHT22
    PIN = 0 #Moisture sensor PIN
    sensor = seeed_dht.DHT("11",16) # Temperature and humidity sensor
    sensor2 = GroveMoistureSensor(PIN)

    #print('Detecting enviroment detail...')
    while True:
        humi, temp = sensor.read()
        m = sensor2.moisture
        if not humi or not m is None:
            #print('humidity: {}%, temperature: {} C, moisture: {}'.format(humi, temp, m))
            save_measurements('humidity: {}, temperature: {}, moisture: {}'.format(humi, temp, m))
            # if (s != None):
            #     s.sendall(bytes('humidity {} celcius {} moisture {} measurements:'.format(humi, temp, m), "utf8"))

def smallBuzzing(): # Sound of buzzer when the number of people does not exceed 5 
    GPIO.setup(Buzzer_sig, GPIO.OUT)
    GPIO.output(Buzzer_sig, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(Buzzer_sig, GPIO.LOW)

def invalidBuzzing():
    GPIO.setup(Buzzer_sig, GPIO.OUT)
    GPIO.output(Buzzer_sig, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(Buzzer_sig, GPIO.LOW)
    time.sleep(0.1)
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

def getUserList():
    # 9Calling Socket 
    #s.sendall(bytes('getUsers', "utf8"))
    # data = s.recv(1024)
    # print("data: {}".format(data))
    # users = data.decode("utf8")
    users = get_all_users()
    y = json.loads(users)
    with open('users.csv', 'w', newline='', encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)
        for user in y:
            info = [user["student_id"], user["name"], user["phone_number"]]
            #print(info)
            writer.writerow(info) 

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
    global stop

    # setup GPIO_SIG as input
    GPIO.setup(GPIO_SIG, GPIO.IN)

    # get duration from Ultrasonic SIG pin
    while GPIO.input(GPIO_SIG) == 0:
        start = time.time()

    while GPIO.input(GPIO_SIG) == 1:
        stop = time.time()

    elapsed = stop - start
    distance = (elapsed * 34300)/2

    if (distance < 65):
        debounceFlag = True
        time_counter[0] = 1
        print("time1 : {:10.2f}".format(time_counter[0]))
        time.sleep(1)
        measurementPulse()

    # setup the GPIO_SIG as output
    GPIO.setup(GPIO_SIG2, GPIO.OUT)
    # GPIO.setup(LED, GPIO.OUT)

    GPIO.output(GPIO_SIG2, GPIO.LOW)
    time.sleep(0.0001)
    GPIO.output(GPIO_SIG2, GPIO.HIGH)
    time.sleep(0.0001)
    GPIO.output(GPIO_SIG2, GPIO.LOW)
    start2 = time.time()
    global stop2
    
    # setup GPIO_SIG as input
    GPIO.setup(GPIO_SIG2, GPIO.IN)

    # get duration from Ultrasonic SIG pin
    while GPIO.input(GPIO_SIG2) == 0:
        start2 = time.time()

    while GPIO.input(GPIO_SIG2) == 1:
        stop2 = time.time()
    
    elapsed2 = stop2 - start2
    distance2 = (elapsed2 * 34300)/2
    time.sleep(0.3)
    range[1] = distance2

    if (distance2 < 65):
        debounceFlag = True
        time_counter[1] = 1 #float(time.time() - count)
        print("time2 : {:10.2f}".format(time_counter[1]))
        time.sleep(1)
        measurementPulse()

def measurementPulse():
    global freezeSensors
    global checkQR
    global numPeople
    global startTime
    global timeFlag
    if time_counter[0] is 1:
        #if people passing through the ultrasonic and is leaving
        entrance = 1
        print("Entering...")
        time_counter[0] = 0
        time_counter[1] = 0
        time.sleep(2)
        peopleInRoom.welcomeIn = peopleInRoom.welcomeIn + 1 # Number of people coming in
        updatePeopleEntry()
        #print("In: {}".format(peopleInRoom.welcomeIn))

    elif time_counter[1] is 1 and freezeSensors is 0:
        entrance = 0
        time_counter[0] = 0
        time_counter[1] = 0
        time.sleep(1)
        print("Leaving...")
        peopleInRoom.pp = peopleInRoom.pp - 1
        print("People currently in room: {}".format(peopleInRoom.pp))
        peopleInRoom.welcomeOut = peopleInRoom.welcomeOut + 1 # Number of people going out
        updatePeopleEntry()
        #print("Out: {}".format(peopleInRoom.welcomeOut))

    elif time_counter[1] is 1 and freezeSensors is 1:
        peopleInRoom.welcomeOut = peopleInRoom.welcomeOut + 1
        print("Out: {}".format(peopleInRoom.welcomeOut))
        entrance = 0
        time_counter[0] = 0
        time_counter[1] = 0
        time.sleep(1)
        
    else:
        entrance = 0

    if entrance == 1:
        freezeSensors = 1
        entrance = 0
        print("entry detected")
        numPeople = peopleInRoom.pp
        if (users == None):
            getUserList()
        # s.sendall(bytes('QR-Camera'.format(),"utf8"))
        checkQR = True
        post_message('message :QR Check!')
        # s.sendall(bytes('message :QR Check!', "utf8"))
        startTime = time.time()
        timeFlag = True
    
    if (qrFlag is True) or (timeFlag is True):
        freezeSensors = 0

def updatePeopleEntry():
    save_entry('{} {} {}'.format(peopleInRoom.pp, peopleInRoom.welcomeIn, peopleInRoom.welcomeOut))

def debouncing():
    global debounceFlag
    while True:
        if debounceFlag is True:
            time.sleep(0.75)
            debounceFlag = False

def startVideoStream():
    global checkQR
    global qrFlag
    global startTime
    global timeFlag
    startTime = time.time()
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1)
    print("Reading frame")
    count = 0
    try:
        while True:
            if (checkQR):
                # grab the frame from the threaded video stream and resize it to
                # have a maximum width of 400 pixels
                frame = vs.read()
                frame = imutils.resize(frame, width=400)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # print("Frame Processed")
                # find the barcodes in the frame and decode each of the barcodes
                #Function should call here
                #print(checkQR)
                lcd.clear()
                lcd.setCursor(0,0)
                lcd.write('Please scan your')
                lcd.setCursor(1,0)
                lcd.write('QR or leave ^_^')
                barcodes = pyzbar.decode(frame)

                # Decoding barcode
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
                        if barcodeData == row:
                            if numPeople < 5: # If QR Code is valid and there are still rooms for more
                                peopleInRoom.pp = peopleInRoom.pp + 1
                                lcd.clear()
                                lcd.setCursor(0,0)
                                lcd.write('Welcome to the')
                                lcd.setCursor(1,0)
                                lcd.write('room, ^_^!')
                                UltrasonicSensor.smallBuzzing() # Buzz small and cool
                                print("Welcome!")
                                legitFlag = True
                                qrFlag = True
                                print("People currently in room: {}".format(peopleInRoom.pp))
                                updatePeopleEntry()
                                #post_join('updateJoin :{}:{}'.format(barcodeData, peopleInRoom.pp))
                                print(barcodeData)
                                break
                                
                            else:# Signal the room is currently full
                                peopleInRoom.pp = peopleInRoom.pp + 1 # Intended do not delete
                                lcd.setCursor(0,0)
                                lcd.write('Sorry, the room')
                                lcd.setCursor(1,0)
                                lcd.write('is full!')
                                print("Over 5 people in the room")
                                loudBuzzing() # Buzz loud and clear
                                qrFlag = True
                                break
                            
                        elif (count == len(x) - 1):
                            peopleInRoom.pp = peopleInRoom.pp + 1 # this is intended do not delete
                            invalidBuzzing() # Buzz small and cool
                            lcd.clear()
                            lcd.setCursor(0, 0)
                            lcd.write('QR code is not')
                            lcd.setCursor(1, 0)
                            lcd.write('in the database')
                            time.sleep(1.5)
                            lcd.clear()
                            lcd.setCursor(0,0)
                            lcd.write('Please Leave!')
                            time.sleep(5)
                            print("QR code is not in the database")
                            qrFlag = True
                            break

                        if (count == len(x) - 1):
                            break
                        count = count + 1
                            
                cv2.imshow("Barcode Scanner", frame)
                key = cv2.waitKey(1) & 0xFF
                (flag, encodedImage) = cv2.imencode(".jpg", frame)
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                    bytearray(encodedImage) + b'\r\n')
                
                if (time.time() - startTime) > 20.0:
                    checkQR = False
                    peopleInRoom.leavingNoQR = 1
                    cv2.destroyAllWindows()
                    break

                # if (timeFlag):
                #     if (time.time() - startTime) > 20.0:
                #         lcd.clear()
                #         lcd.setCursor(0, 0)
                #         lcd.write("Hello!")
                #         checkQR = False 
                #         s.sendall(bytes('message :QR Scan going to idle mode', "utf8"))
                #         startTime = 0
                #         timeFlag = False

                if qrFlag is True:
                    print("[INFO] cleaning up...")
                    qrFlag = False
                    post_message('message :QR Scan is done')
                    lcd.clear()
                    lcd.setCursor(0, 0)
                    lcd.write("Hello!")
                    startTime = 0 
                    timeFlag = False
                    time.sleep(5)
                    checkQR = False
                    #csv.close()
                    cv2.destroyAllWindows()
            # else:
            #     print("Nothing to do here")
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
    return Response(startVideoStream(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/shutdown")
@cross_origin()
def shutdown():
    shutdown_server()
    return 'QR Camera Shutting Down...'

if __name__ == '__main__':
     # LCD Setup
    lcd.setCursor(0, 0)
    lcd.write("Hello!")
     # GPIO Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(5, GPIO.IN)
    GPIO.setup(0, GPIO.IN)

    t = threading.Thread(target=getAndPrint)
    t.start()

    t2 = threading.Thread(target=air)
    t2.start()

    t4 = threading.Thread(target=debouncing)
    t4.start()
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
        help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())
    
    #lcd = JHD1802()
    #lcd.setCursor(0, 0)
    
    #print("Flask running on localhost:"+str(PORT))
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=False, use_reloader=False)

    # video stream service
    t3 = threading.Thread(target=startVideoStream)
    t3.daemon = True
    t3.start()
