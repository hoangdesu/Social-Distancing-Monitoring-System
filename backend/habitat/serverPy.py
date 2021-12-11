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
url = "http://localhost:7000/"


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

        if ("measurements:" in str_data):
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
            #print("Measurement Posting:")
            #print(z)

        if (str_data == "getUsers"):
            users = url + 'users/all/'
            r = requests.get(url = users)
            data = r.text
            c.sendall(data.encode("utf8"))
        
        if (str_data == "resetPeopleCount"):
            data = json={
                "entry_number": int(0),
                "entry_id": "None"
            }
            print("Posting Reset")
            entry = url + 'entry/'
            z = requests.post(url = entry, json = data)
            print(z)

        if (str_data == "showCamera"):
            f = open("message.txt", "w")
            f.write("showCamera")
            f.close()
        
        if (str_data == "hideCamera"):
            f = open("message.txt", "w")
            f.write("hideCamera")
            f.close()
        
        if ("message" in str_data):
            x = str_data.split(":")
            # Get id from data
            data = json={
                "content": x[1],
            }            
            entry = url + 'message/'
            z = requests.post(url = entry, json = data)
            print(z)

        if ("updateLeave" in str_data):
            x = str_data.split(":")
            # Get id from data
            print(data)
            data = json={
                "entry_number": int(x[1]),
                "entry_id": "None"
            }
            print("Posting Leaving")
            
            entry = url + 'entry/'
            z = requests.post(url = entry, json = data)
            print(z)

        if ("updateLeave" in str_data):
            x = str_data.split(":")
            # Get id from data
            print(data)
            data = json={
                "entry_number": int(x[1]),
                "entry_id": "None"
            }
            print("Posting Leaving")
            
            entry = url + 'entry/'
            z = requests.post(url = entry, json = data)
            print(z)

        if ("updateJoin" in str_data):
            # Get data from output string
            x = str_data.split(":")
            # Get id from data
            x1 = x[1].split(",")
            data = json={
                "entry_number": int(x[2]),
                "entry_id": x1[0]
            }
            print("Posting Enter")
            #print(data)
            entry = url + 'entry/'
            z = requests.post(url = entry, json = data)
            print(z)
finally:
    c.close()