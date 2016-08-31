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

