# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import peopleInRoom
import seeed_dht
from grove.display import JHD1802
import UltrasonicSensor
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import base64

def qrDectector(value):
    numPeople = value
    print("Num People: {}".format(numPeople))
    # construct the argument parser and parse the arguments
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
                if numPeople < 2: # If QR Code is valid and there are still rooms for more
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
            if legitFlag is True:
                return ("LegitBarcode:{}:{}:\n".format(barcodeData,peopleInRoom.pp))
            else:
                return ("{},{}\n".format(datetime.datetime.now(),barcodeData))

    return None

