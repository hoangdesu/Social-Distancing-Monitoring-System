import RPi.GPIO as GPIO
from qrReader import *
import time
import seeed_dht
from grove.grove_moisture_sensor import GroveMoistureSensor
import sys
#sys.path.append(".")
from MiniPIR import GroveMiniPIRMotionSensor
import peopleInRoom

GPIO_SIG = 12
#LED = 15
entrance = 0
  

def getAndPrint():

    print("SeeedStudio Grove Ultrasonic get data and print")

    # test 100 times
    for i in range(10000):
        miniPir() #this function is called first
        #measurementInCM()
        
    

    # Reset GPIO settings
    GPIO.cleanup()
    
    
    
def air():
 
    # for DHT11/DHT22
    PIN = 0
    sensor = seeed_dht.DHT("11",5)
    sensor2 = GroveMoistureSensor(PIN)
    
    #print('Detecting enviroment detail...')
    humi, temp = sensor.read()
    m = sensor2.moisture
    if not humi or not m is None:
        print('humidity: {}%, temperature: {} C, moisture: {}'.format(humi, temp, m))
    else:
        print('humidity & temperature: {}'.format(temp))
        time.sleep(2)
        
def miniPir():
    pir = GroveMiniPIRMotionSensor(22)

    def callback():
        print("The number of people who passed this area: {}".format(pir.count))
    
    pir.on_detect = callback
    
    while True:
        try:
            measurementInCM() # this function is called after the miniPir function is called
            time.sleep(0.5)
        finally:
            GPIO.cleanup
        

def measurementInCM():

    # setup the GPIO_SIG as output
    GPIO.setup(GPIO_SIG, GPIO.OUT)
    #GPIO.setup(LED, GPIO.OUT)

    GPIO.output(GPIO_SIG, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(GPIO_SIG, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GPIO_SIG, GPIO.LOW)
    start = time.time()

    # setup GPIO_SIG as input
    GPIO.setup(GPIO_SIG, GPIO.IN)

    # get duration from Ultrasonic SIG pin
    while GPIO.input(GPIO_SIG) == 0:
        start = time.time()

    while GPIO.input(GPIO_SIG) == 1:
        stop = time.time()

    measurementPulse(start, stop)


def measurementPulse(start, stop):

    #print("Ultrasonic Measurement")

    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    distance = distance / 2

    print("Distance : {:10.2f} CM".format(distance))
    air()
    
    if distance <= 15:
        #GPIO.output(LED, GPIO.HIGH)
        entrance = 1
    elif distance > 15 and distance < 55:
        #if people passing through the ultrasonic
        entrance = 0
        peopleInRoom.leavingDect = 1
    else:
        #GPIO.output(LED, GPIO.LOW)
        entrance = 0

#     if distance <= 35:
#         entrance = 0
#         start = time.time()
#         while True:
#             if (time.time() - start) > 3.5:
#                 if distance <= 35:
#                     entrance = 1
#                     break
#                 else:
#                     leavingDect = 1
#                     break
#             else:
#                 elapsed = stop-start
#                 distance = elapsed * 34300
#                 distance = distance / 2
#     else:
#         entrance = 0
    
    if entrance is 1:
        print("entry detected")
        qrDectector()
        print("Number of people in the room: {}".format(peopleInRoom.pp))
