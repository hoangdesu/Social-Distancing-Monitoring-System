#server.py 
import requests 
import json
url = "http://localhost:7000/"

def save_measurements(data):
    x = data.split()
    #print(x)
    #sample output ['humidity', '42,', 'celcius', '35,', 'moisture', '0']
    if (x[1] != "0" or x[3] != "0"):
        measure_data = json={
            x[0]: float(x[1]),
            x[2]: float(x[3]),
            x[4]: float(x[5])
        }
        measure = url + 'measurements/'
        p = requests.post(url = measure, json = measure_data)
        print("Measurement status: {}".format(p))

def get_all_users():
    users = url + 'users/all/'
    g = requests.get(url = users)
    data = g.text
    return data

def reset_people_count():
    data = json={
        "entry_number": int(0),
        "entry_id": "None"
    }
    print("Posting Reset")
    entry = url + 'entry/'
    p = requests.post(url = entry, json = data)
    print(p)

def post_message(str_data):
    x = str_data.split(":")
    # Get id from data
    data = json={
        "content": x[1],
    }            
    entry = url + 'message/'
    p = requests.post(url = entry, json = data)
    print(p)

def post_leave(str_data):
    x = str_data.split(":")
    data = json={
        "entry_number": int(x[1]),
        "entry_id": "None"
    }
    print("Posting Leaving")
    
    entry = url + 'entry/'
    p = requests.post(url = entry, json = data)
    print(p)

def post_join(str_data):
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
    p = requests.post(url = entry, json = data)
    print(p)