# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import requests

def qrDectector():
     
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
     
    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far
    csv = open("output.csv", "w")
    found = set()
    
    start = time.time()
    print("start: " , start)

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
            if barcodeData not in found:
                csv.write("{},{}\n".format(datetime.datetime.now(),
                    barcodeData))
                csv.flush()
                found.add(barcodeData)
                print("{},{}\n".format(datetime.datetime.now(),
                    barcodeData))
                qrFlag = True
                

                # show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF
        
        
        print("timer: ", time.time() - start)
        
        if (time.time() - start) > 10.0:
            cv2.destroyAllWindows()
            vs.stop()
            break
     
        if qrFlag is True:
            time.sleep(3.0)
            print("[INFO] cleaning up...")
            # close the output CSV file do a bit of cleanup
            csv.close()
            cv2.destroyAllWindows()
            vs.stop()
            return ("{},{}\n".format(datetime.datetime.now(),
                    barcodeData))

   
    return None

