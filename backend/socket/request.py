import requests 

url = "http://localhost:3000/measurements/"
myobj = {'moisture': 22.7, 
        'celcius': 32, 
        'humidity': 0.45}

x = requests.post(url, data = myobj)

print(x.text)
