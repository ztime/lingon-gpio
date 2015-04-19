import RPi.GPIO as io
import GpioController
import time
from sys import exit

class Sr04Controller(GpioController.GpioController):
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
        # call super class
        super(Sr04Controller, self).__init__([triggPin,echoPin],boardmode)
        # setup pins
        io.setup(triggPin,io.OUT)
        io.setup(echoPin,io.IN)
        io.output(triggPin, 0)
        #set pins to variables
        self.triggPin = triggPin
        self.echoPin = echoPin

    def measure(self):
        #wait for sensor to settle
        time.sleep(self.SETTLE_TIME)
        #send trigger signal
        io.output(self.triggPin, 1)
        time.sleep(self.TRIGGER_LENGTH)
        io.output(self.triggPin, 0)
        #start mesaure
        while io.input(self.echoPin) == 0:
            pulse_start = time.time()
        while io.input(self.echoPin) == 1:
            pulse_end = time.time()
        #calculating distance
        distance = (self.SPEED_OF_SOUND / 2) * (pulse_end - pulse_start)
        return round(distance, 2)

#    def cleanup(self):
#        io.cleanup()
        
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
    trigg = raw_input("What pin is the trigger pin? ")
    echo = raw_input("What pin is echo pin? ")

    #creating a new sr04
    sensor = Sr04Controller(int(trigg),int(echo))
    # starting mesauring
    while True:
        print("=================")
        print("Started mesaurement")

        dist = sensor.measure()
        print("Measured distance: " + str(dist) + "cm");
        another = raw_input("Do you want to measure again? Y/n : ")
        if another != "Y":
            break
        print("================")
    #done
    print("Cleaning up")
    sensor.cleanup()
    
