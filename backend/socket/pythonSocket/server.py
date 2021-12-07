import socket
import threading
import time

HEADER = 1024
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = 'utf-8'
DISCONNECTED_MSG = "!DISCONNECT"

ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handleClient(conn, addr):
    print(f'NEW CONNECTION from {addr}')
    
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECTED_MSG:
                connected = False
            print(f'Address [{addr}]: Message: {msg}')
            conn.send(f"Server got the message '{msg}'!".encode(FORMAT))
    conn.close()    
    
        

def counter():
    counter = 0
    while True:
        print("Client process:", counter)
        counter += 1
        time.sleep(0.5)


def start():
    server.listen()
    print(f"SERVER STARTING AT {ADDR}...")
    t1 = threading.Thread(target=counter)
    # t1.start()
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"ACTIVE CONNECTIONS: {threading.active_count() - 1}")
    
    
    
if __name__ == '__main__':
    start()
    
    
# REFERENCE: https://www.youtube.com/watch?v=3QiPPX-KeSc