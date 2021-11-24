import time
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor

def air():
 
    # for DHT11/DHT22
    PIN = 0
    sensor = seeed_dht.DHT("11",5)
    sensor2 = GroveMoistureSensor(PIN)
    
    print('Detecting enviroment detail...')
    humi, temp = sensor.read()
    m = sensor2.moisture
    if not humi or not m is None:
        print('humidity: {}%, temperature: {} C, moisture: {}'.format(humi, temp, m))
    else:
        print('humidity & temperature: {}'.format(temp))
        time.sleep(2)

