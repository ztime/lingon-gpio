import RPi.GPIO as io
import GpioController
import time
from sys import exit

class StepController(GpioController.GpioController):
    #constants

    def __init__(self, triggPin, pinkPin, orangePin, yellowPin,bluePin, boardmode="BCM")
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
        self.punkPin = pinkPin
        self.orangePin = orangePin
        self.yellowPin = yellowPin
        self.bluePin = bluePin


