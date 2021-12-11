from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
from pyzbar import pyzbar
import cv2
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import base64
# from imutils.video import VideoStream
# from pyzbar import pyzbar
# import argparse
import datetime
# import imutils
# import time
# import cv2
import peopleInRoom
import seeed_dht
from grove.display import JHD1802
import UltrasonicSensor

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")

#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)

@app.route("/")
@cross_origin()
def index():
    
    return "Visit http://localhost:5000/video_feed";

def detect_motion(frameCount):

    global vs, outputFrame, lock
    # md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    
    while True:
    # grab the frame from the threaded video stream and resize it to
    # have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # find the barcodes in the frame and decode each of the barcodes
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
    
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    
    
    
    
    
    
    


    # while True:
    #     frame = vs.read()
    #     frame = imutils.resize(frame, width=400)
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #     gray = cv2.GaussianBlur(gray, (7, 7), 0)
    #     # grab the current timestamp and draw it on the frame
    #     timestamp = datetime.datetime.now()
    #     cv2.putText(frame, timestamp.strftime(
    #         "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
    #         cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    #     # if the total number of frames has reached a sufficient
    #     # number to construct a reasonable background model, then
    #     # continue to process the frame
    #     # if total > frameCount:
    #     # 	# detect motion in the image
    #     # 	motion = md.detect(gray)
    #     # 	# check to see if motion was found in the frame
    #     # 	if motion is not None:
    #     # 		# unpack the tuple and draw the box surrounding the
    #     # 		# "motion area" on the output frame
    #     # 		(thresh, (minX, minY, maxX, maxY)) = motion
    #     # 		cv2.rectangle(frame, (minX, minY), (maxX, maxY),
    #     # 			(0, 0, 255), 2)
        
    #     # update the background model and increment the total number
    #     # of frames read thus far
    #     # md.update(gray)
    #     total += 1
    #     # acquire the lock, set the output frame, and release the
    #     # lock
    #     with lock:
    #         outputFrame = frame.copy()

def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            # (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # # ensure the frame was successfully encoded
            # if not flag:
            # 	continue
   
   
            frame = outputFrame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.GaussianBlur(frame, (7, 7), 0)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
   
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
@cross_origin()
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")
        
@app.route("/test")
def test():
    global outputFrame

    # while True:
    # 	frame = cv2.cvtColor(outputFrame, cv2.COLOR_BGR2GRAY)
      # 	encodedImage = cv2.imencode(".jpg", outputFrame)
    # 	yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
    # 		bytearray(encodedImage) + b'\r\n')
     
     
def testingVideoStreamService():
    global vs, lock

    while True:
        with lock:
            # vs = VideoStream(src=0).start() # SOMETHING WRONG HERE!!!!
            # time.sleep(1/5)
            frame = vs.read()
            
            if frame is None: 
                continue
            #         <your code/do something with frame>
            # if cv2.waitKey(1) & 0xFF == ord('q'): #exit if q-key pressed
            #         break #break safely
            
            k = cv2.waitKey(30) & 0xff
            if k == 27:  # press 'ESC' to quit
                break
            
            frame = imutils.resize(frame, width=500)
            timestamp = datetime.datetime.now()
            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            # if not flag:
            #     continue 
            
            jpg_as_text = base64.b64encode(encodedImage)
            b64_str = jpg_as_text.decode()
            
            cv2.imshow("Barcode Scanner", frame)
            k = cv2.waitKey(1) & 0xFF
            
            socketio.emit('video-stream', b64_str)
            print("Video frame sent!" + '\n')
    cv2.destroyAllWindows()
    vs.stop()

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=32,
        help="# of frames used to construct the background model")
    args = vars(ap.parse_args())
    
    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=(
        args["frame_count"],))
    
    # t = threading.Thread(target=testingVideoStreamService)
    t.daemon = True
    t.start()
    
    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)
    
    # socketio.run(app, host='0.0.0.0', port=5000)
    
# release the video stream pointer
vs.stop()

# testingVideoStreamService


# NOTES:
#     - Command to run: py webstreaming.py  --ip 0.0.0.0 --port 5000
#     (can enforce host + port later)
#     - point the <img src"...""> to video_feed URL