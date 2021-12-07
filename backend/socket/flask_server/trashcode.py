# from imutils.video import VideoStream
# from flask import Response
# from flask import Flask
# from flask import render_template
# import threading
# import argparse
# import datetime
# import imutils
# import time
# import cv2
# from flask_cors import CORS, cross_origin

# from flask import Flask, render_template
# from flask_socketio import SocketIO

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret!'
# app.config['CORS_HEADERS'] = 'Content-Type'
# socketio = SocketIO(app)

# if __name__ == '__main__':
#     socketio.run(app)

# import eventlet
# import socketio


# sio = socketio.Server()
# app = socketio.WSGIApp(sio)

# @sio.event
# def connect(sid, environ):
#     print('connect ', sid)
    
# if __name__ == '__main__':
#     eventlet.wsgi.server(eventlet.listen(('', 5000)), app)