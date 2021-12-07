from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

sio = SocketIO(app)

def task(sid):
    sio.sleep(1)
    emit("testingg", sid)
    

@sio.on('connect')
def connected(sid):
    print(sid, 'Connected')
    sio.start_background_task(task, sid)
    return "hi"
    
# @sio.on('stream')
# def getStreamData(data):
#     print(data)
    
# @sio.on('fromServer')
    
    
# @sio.on('message')
# def handle_message(message):
#     send(message)

if __name__ == '__main__':
    sio.run(app)