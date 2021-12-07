# import socketio

# sio = socketio.AsyncServer()
# app = socketio.ASGIApp(sio)

# @sio.event
# async def 

# THIS PART COPIED EXACTLY THE SAME FROM THE SOCKETIO BUT IT DONT WORK???
# import eventlet
# import socketio

# sio = socketio.Server()
# app = socketio.WSGIApp(sio)

# @sio.event
# def connect(sid, environ):
#     print('connect ', sid)


# @sio.event
# def disconnect(sid, environ):
#     print('disconnect ', sid)

# eventlet.wsgi.server(eventlet.listen(('', 5000)), app)


# ------- this shit works... ---------

import socketio
import eventlet
import time

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

def task1(sid):
    c=0
    while True:
        print("serverr sync", (c))
        c+=1
        sio.send('task1 COUNTER:', c)
        sio.sleep(3)

@sio.event
def connect(sid, env):
    print(sid, ' connected')
    print(env)
    sio.send("Server saw you")
    sio.emit('t1', 'from server', to=sid)
    sio.start_background_task(task1, sid)
    # sio.emit("msg", "from server")
    # task1()
    
@sio.event()
def msg(sid, env):
    sio.send("hi")    
    print("hi msg")

    
@sio.event
def disconnect(sid, env):
    print(sid, ' disconnected')
    
    
@sio.event
def sum(sid, data):
    print(sid, data)
    return f"Result from server: {data['num'][0] + data['num'][1]}"
    
    

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)



