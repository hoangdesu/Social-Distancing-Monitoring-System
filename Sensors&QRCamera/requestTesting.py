import requests
from qrReader import *

while True:
    data = qrDectector()
    res = requests.get(f'http://192.168.137.114:3001/hiback/{data}')
    print("RECEIVED REQUEST:", res.content)