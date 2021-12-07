import socketio
import time
import asyncio
import threading

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

ctr = 0

async def task1(sid):
    ctr = 1
    await sio.emit('t1', f'Your sid is {sid}', to=sid)
    for i in range(5):
        await sio.emit('t1', f'{i}')
        await time.sleep(1)
    # await setInterval(foo, 0.5)
    # while True:
    #     sio.emit('t1', str(ctr))
    #     ctr+=1
    #     print("Hi")
    #     time.sleep(1)
        
# async def setInterval(func,time):
#     e = threading.Event()
#     while not e.wait(time):
#         await func()
        
# async def foo():
#     global ctr
#     ctr+=1
#     print("hello", ctr)
#     await sio.emit('t1', ctr)

@sio.event
async def connect(sid, env):
    print(sid, ' connected')
    # sio.emit("msg", "from server")
    await sio.send("Hi")
    await sio.emit("msg", {"resp": "haha"})
    await sio.start_background_task(task1, sid)
    # t = threading.Thread(target=task1, args=(sid))
    # await t.start()
    
    
@sio.event
async def disconnect(sid):
    print(sid, ' disconnected')
    # print(env)
    
@sio.event
async def t1(sid):
    sio.emit('t1', "hi back")

# if __name__ == '__main__':
#     eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

# COMMAND: 
# uvicorn --reload async_server:app
# uvicorn async_server:app