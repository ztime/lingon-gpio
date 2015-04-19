import RPi.GPIO as io
import GpioController
from sys import exit

class ServoController(GpioController.GpioController):
    """
   Handles general servos (not continuos ones)
   """

   #constants
    DEFAULT_FREQ = 50
    ANGLE_NEUTRAL=7.5
    DEGREE_NEUTRAL=90
    ANGLE_ZERO=2.5
    DEGREE_ZERO = 0
    ANGLE_180=12.5
    DEGREE_180 = 180

    def __init__(self,controllPin,directStart=True,boardmode="BCM"):
        super(ServoController, self).__init__([controllPin], boardmode)
        # Setup
        io.setup(controllPin, io.OUT)
        self._pwm = io.PWM(controllPin, DEFAULT_FREQ)
        self._currentDirection = ANGLE_NEUTRAL
        self._currentDirectionDegrees = DEGREE_NEUTRAL 
        self._running = False
        if directStart is True:
            self.start()

    def start():
        if self._running is False:
            self._pwm.start(self._currentDirection)
            self._running = True

    def stop():
        if self._running is True:
            self._pwm.stop()
            self._running = False

    def rotateToNeutral():
        self._currentDirection = ANGLE_NEUTRAL
        self._currentDirectionDegrees = DEGREE_NEUTRAL
        self._updateAngle()

    def rotateToZero():
        self._currentDirection = ANGLE_ZERO
        self._currentDirectionDegrees = DEGREE_ZERO
        self._updateAngle()

    def rotateTo180():
        self._currentDirection = ANGLE_180
        self._currentDirectionDegrees = DEGREE_180
        self._updateAngle()
    
    def rotateTo(degrees):
        if(int(degrees) < 0 or int(degrees) > 180):
            raise ValueError ("input should be between 0 and 180 degrees (int), got: %s" % degrees)
        convDegrees = self._convertDegrees(degrees)
        self._currentDirection = convDegrees
        self._currentDirectionDegrees = degrees
        self._updateAngle()

    def rotateBy(degrees):
        if degrees != 0:
            absDegrees = abs(degrees)
            if degrees < 0:
                newDeg = self._currentDirectionDegrees - absDegrees
            else:
                newDeg = self._currentDirectionDegrees + absDegrees
            if newDeg < 0:
                newDeg = 0
            elif newDeg > 180:
                newDeg = 180
            convDeg = self._convertDegrees(newDeg)
            self._currentDirection = convDeg
            self._currentDirectionDegrees = newDeg
            self._updateAngle()
    
    def getDegrees():
        return self._currentDirectionDegrees

    def _updateAngle():
        self._pwm.ChangeDutyCycle(self._currentDirection)

    def _convertDegrees(degrees):
        #todo 
        return degrees
