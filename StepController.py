import RPi.GPIO as io
import GpioController
import time
from sys import exit

# Connected with an L293D 

class StepController(GpioController.GpioController):
    #constants

    def __init__(self, triggPin, pinkPin, orangePin, yellowPin,bluePin, boardmode="BCM"):
        # call super
        super(StepController, self).__init__([triggPin,pinkPin,orangePin,yellowPin,bluePin],boardmode)
        # setup pins
        io.setup(triggPin,io.OUT)
        io.setup(pinkPin,io.OUT)
        io.setup(orangePin,io.OUT)
        io.setup(yellowPin,io.OUT)
        io.setup(bluePin,io.OUT)
        io.output(triggPin, 1)
        # to variables
        self.triggPin = triggPin
        self.pinkPin = pinkPin
        self.orangePin = orangePin
        self.yellowPin = yellowPin
        self.bluePin = bluePin

    def setStep(a1, a2, a3, a4):
        io.output(self.pinkPin, a1)
        io.output(self.orangePin, a2)
        io.output(self.yellowPin, a3)
        io.output(self.bluePin, a4)

    def forward(self,delay,steps): 
        for i in range(0, steps):
            setStep(1, 0, 1, 0)
            time.sleep(delay)
            setStep(0, 1, 1, 0)
            time.sleep(delay)
            setStep(0, 1, 0, 1)
            time.sleep(delay)
            setStep(1, 0, 0, 1)
            time.sleep(delay)

    def backward(self,delay,steps): 
        for i in range(0, steps):
            setStep(1, 0, 0, 1)
            time.sleep(delay)
            setStep(0, 1, 0, 1)
            time.sleep(delay)
            setStep(0, 1, 1, 0)
            time.sleep(delay)
            setStep(1, 0, 1, 0)
            time.sleep(delay)

if __name__ == '__main__':
    print("============= Stepper motor controller ===============")
    print("Is everything connected? Observe that trigger pin is ")
    print("live directly at startup")
    sure = raw_input("Do you want to continue? Y/n: ")
    if sure == "Y":
        print("")
    else:
        print("Aborting")
        exit(0)

    print("Running test:")
    trigger = raw_input("What is the trigger pin?")
    pink = raw_input("What is the pink pin?")
    orange = raw_input("What is the orange pin?")
    yellow = raw_input("What is the yellow pin?")
    blue = raw_input("What is the blue pin?")

    # create new controller
    print("Starting up...")
    time.sleep(1000)
    stepper = StepController(int(trigger),int(pink),int(orange),int(yellow),int(blue))
    #driving forward 
    print("Going forward 100 steps, 5 mil delay")
    stepper.forward(5, 100)
    print("Going backwards 100 steps, 5 mil delay")
    stepper.backward(5, 100)
    #done
    stepper.cleanup()

