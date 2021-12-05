#server.py 
import requests 
import socket
from typing import final 
import json


host = socket.gethostname()
print(host)
port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
url = "http://localhost:3000/"


s.listen(1)
print("Server listening on port", port)

c, addr = s.accept()
print("Connect from ", str(addr))
try:
    while True:
        data = c.recv(1024)
        str_data = data.decode("utf8")

        if (str_data == 'quit'):
            break

        if ("measurements" in str_data):
            x = str_data.split()
            #print(x)
            #sample output ['humidity', '42,', 'celcius', '35,', 'moisture', '0']
            data = json={
                x[0]: float(x[1]),
                x[2]: float(x[3]),
                x[4]: float(x[5])
            }
            measure = url + 'measurements/'
            z = requests.post(url = measure, json = data)
            #print(z)

        if (str_data == "getUsers"):
            users = url + 'users/all/'
            r = requests.get(url = users)
            data = r.text
            c.sendall(data.encode("utf8"))

        if ("LegitBarcode" in str_data):
            # Get data from output string
            x = str_data.split(":")
            # Get id from data
            x1 = x[1].split(",")
            data = json={
                "entry_number": int(x[2]),
                "entry_id": x1[0]
            }
            print(data)
            entry = url + 'entry/'
            z = requests.post(url = entry, json = data)
            print(z)
finally:
    c.close()