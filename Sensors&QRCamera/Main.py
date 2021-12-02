#from qrReader import *
from UltrasonicSensor import *
from environment import *
#from MiniPIR import *

if __name__ == '__main__':
    #main()
    # rpi board gpio or bcm gpio
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.IN)
    GPIO.setup(5, GPIO.IN)
    GPIO.setup(0, GPIO.IN)
    # loop method
    getAndPrint()
        


    
    
    