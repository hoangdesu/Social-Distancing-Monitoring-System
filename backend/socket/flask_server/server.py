from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS, cross_origin
from imutils.video import VideoStream, WebcamVideoStream
import imutils
import time
import cv2
import base64

import json
import time
import random
import threading
import datetime

# Required for server-side emit() to work
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dreamchaser'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")

lock = threading.Lock()

vs = VideoStream(src=0).start() # SOMETHING WRONG HERE!!!!
# vs.stream.release()
time.sleep(2.0)

# vs = cv2.VideoCapture(src=0).start()


# @app.route("/")
# @cross_origin()
# def index():
#     title = "Example Chart"
#     # return render_template("index.html", title=title)
#     return "Hi!"

def produce_chart_data():
    ctr = 0
    while True:
        # Sleep for random duration to prove async working
        time.sleep(1/48)
        # socketio.sleep(1/24)

        # Get some data from source and emit to clients when recieved
        data = get_some_data()

        socketio.emit('chart-data', data)
        # emit('chart-data', data)
        socketio.emit('counter', ctr)
        print("Emit data", ctr)
        ctr += 1
        
        
def testingVideoStreamService():
    global vs, lock

    while True:
        with lock:
            # vs = VideoStream(src=0).start() # SOMETHING WRONG HERE!!!!
            time.sleep(1/5)
            frame = vs.read()
            
            if frame is None: 
                continue
            # if cv2.waitKey(1) & 0xFF == ord('q'): #exit if q-key pressed
            #         break #break safely
            
            # k = cv2.waitKey(30) & 0xff
            # if k == 27:  # press 'ESC' to quit
            #     break
            
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
            key = cv2.waitKey(1) & 0xFF
            
            socketio.emit('video-stream', b64_str)
            print("Video frame sent!")
    cv2.destroyAllWindows()
    vs.stop()


def sendBrianTest():
    while True:
        time.sleep(1/5)
        socketio.emit('brian', "BRian")


def get_some_data():
    data = {
            "series": [
                {
                    "name": 'Data 1',
                    "data": [
                            {"x": 143034652600, "y": random.random()*10+70},
                            {"x": 143134652600, "y": random.random()*10+70},
                            {"x": 143234652600, "y": random.random()*10+70},
                            {"x": 143334652600, "y": random.random()*10+70},
                            {"x": 143434652600, "y": random.random()*10+70},
                            {"x": 143534652600, "y": random.random()*10+70},
                            {"x": 143634652600, "y": random.random()*10+70},
                            {"x": 143734652600, "y": random.random()*10+70},
                            {"x": 143834652600, "y": random.random()*10+70},
                            {"x": 143934652600, "y": random.random()*10+70}
                    ]
                }, {
                    "name": 'Data 2',
                    "data": [
                            {"x": 143034652600, "y": random.random()*10+40},
                            {"x": 143134652600, "y": random.random()*10+40},
                            {"x": 143234652600, "y": random.random()*10+40},
                            {"x": 143334652600, "y": random.random()*10+40},
                            {"x": 143434652600, "y": random.random()*10+40},
                            {"x": 143534652600, "y": random.random()*10+40},
                            {"x": 143634652600, "y": random.random()*10+40},
                            {"x": 143734652600, "y": random.random()*10+40},
                            {"x": 143834652600, "y": random.random()*10+40},
                            {"x": 143934652600, "y": random.random()*10+40}
                    ]
                }, {
                    "name": 'Data 3',
                    "data": [
                            {"x": 143034652600, "y": random.random()*10+25},
                            {"x": 143134652600, "y": random.random()*10+25},
                            {"x": 143234652600, "y": random.random()*10+25},
                            {"x": 143334652600, "y": random.random()*10+25},
                            {"x": 143434652600, "y": random.random()*10+25},
                            {"x": 143534652600, "y": random.random()*10+25},
                            {"x": 143634652600, "y": random.random()*10+25},
                            {"x": 143734652600, "y": random.random()*10+25},
                            {"x": 143834652600, "y": random.random()*10+25},
                            {"x": 143934652600, "y": random.random()*10+25}
                    ]
                }, {
                    "name": 'Data 3',
                    "data": [
                            {"x": 143034652600, "y": random.random()*10+25},
                            {"x": 143134652600, "y": random.random()*10+25},
                            {"x": 143234652600, "y": random.random()*10+25},
                            {"x": 143334652600, "y": random.random()*10+25},
                            {"x": 143434652600, "y": random.random()*10+25},
                            {"x": 143534652600, "y": random.random()*10+25},
                            {"x": 143634652600, "y": random.random()*10+25},
                            {"x": 143734652600, "y": random.random()*10+25},
                            {"x": 143834652600, "y": random.random()*10+25},
                            {"x": 143934652600, "y": random.random()*10+25}
                    ]
                }
            ]}
    return data


if __name__ == '__main__':
    # default: basic counter
    t = threading.Thread(target=produce_chart_data)
    # t.start()
    
    # video stream service
    t2 = threading.Thread(target=testingVideoStreamService)
    t2.daemon = True
    t2.start()
    

    # PORT = json.load(open('config.json'))["PORT"]
    PORT = 5000
    print("Running on localhost:"+str(PORT))

    socketio.run(app, host='0.0.0.0', port=PORT)
    # app.run()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# --- from: https://github.com/JosephSamela/flask-socketio-chartist.js