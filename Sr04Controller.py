import RPi.GPIO as io
import time
from sys import exit

class Sr04Controller:
    """
    Beware! RasPi gpio cannot handle them 5v from echo pin , so if you use this
    please use a voltage divider to bring it down to 3.3v 

    This is based on the tutorial from :
    http://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

    How we calculate the distance:
    Speed = Distance / Time
    Speed = 34300 (340m/s)
    The mesaured time will be half of what the pin reads (since signal goes 
    back and forth) 
    Distance = ( 34300 / 2 ) * TimeInSeconds
    """

    #constants
    SPEED_OF_SOUND = 34300
    TRIGGER_LENGTH = 0.00001
    SETTLE_TIME = 2

    def __init__(self,triggPin,echoPin,boardmode="BCM"):
        if boardmode=="BCM":
            io.setmode(io.BCM)
        else:
            io.setmode(io.BOARD)
        io.setwarnings(False)
        # setup pins
        io.setup(triggPin,io.OUT)
        io.setup(echoPin,io.IN)
        io.output(triggPin, 0)

    def measure(self):
        #wait for sensor to settle
        time.sleep(SETTLE_TIME)
        #send trigger signal
        io.output(triggPin, 1)
        time.sleep(TRIGGER_LENGTH)
        io.output(triggPin, 0)
        #start mesaure
        while io.input(echoPin) == 0:
            pulse_start = time.time()
        while io.input(echoPin) == 1:
            pulse_end = time.time()
        #calculating distance
        distance = (SPEED_OF_SOUND / 2) * (pulse_end - pulse_start)
        return round(distance, 2)

    def cleanup(self):
        io.cleanup()
        
if __name__ == '__main__':
    print("========== SR-04 Controller ==============================")
    print("Please check that everything is properly connected")
    print("the rasPi cannot handle 5v to its input pins")
    print("Running this without protecting input pin with a voltage")
    print("divider can ruin your RasPi!")
    sure = raw_input("Are you SURE you want to continue? Y/n: ")
    if sure  == "Y":
        print("")
    else:
        print("Aborting:")
        exit(0)

    print("Running a test:")
    trigg = raw_input("What pin is the trigger pin?")
    echo = raw_input("What pin is echo pin?")
    
