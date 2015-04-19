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

    def isRunning():
        return self._running

    def _updateAngle():
        self._pwm.ChangeDutyCycle(self._currentDirection)

    def _convertDegrees(degrees):
        k = (self.ANGLE_180 - self.ANGLE_ZERO) / (self.DEGREE_180 - self.DEGREE_ZERO)
        #y = kx + m
        returnValue = ( k * degress ) + self.ANGLE_ZERO
        return returnValue

# Tests
if __name__ == '__main__':
    print("======= ServoController ========")
    print("Please ensure that you have nothing connected on pin 21 (BCM)  of your RasPi")
    print("as this script will use that pin for tests!")
    sure == raw_input("Are you sure nothing is connected to pin 21? Y/n :")
    if sure == "Y":
        print("")
    else:
        print("Aborting tests.")
        exit(0)
    print("Starting tests:")
    print("Creating servo")
    # Creating a servo that does not start when creating it
    servo = ServoController(21, False)
    print("Ensure that it isn't started since we passed directStart = False")
    if servo.isRunning() == True:
        print("isRunning failed")
        exit(1)
    print("OK")
    print("Check that degrees = 90") 
    if servo.getDegrees() != 90:
        print("Was not in neutral angle from beginning")
        exit(1)
    print("OK")
    print("Start it and check that its running")
    servo.start()
    if servo.isRunning() == False:
        print("Started but isRunning was false.")
        exit(1)
    print("OK")
    print("Rotate it to 0 and check the getDegrees")
    servo.rotateToZero()
    if servo.getDegrees() != 0:
        print("It was not 0 degrees")
        exit(1)
    print("OK")
    print("Rotate it to 180 degrees and check")
    servo.rotateTo180()
    if servo.getDegrees() != 180:
        print("Could not rotate to 180 degrees")
        exit(1)
    print("OK")
    print("Rotate it back to neutral")
    servo.rotateToNeutral()
    if servo.getDegrees() != 90:
        print("Could not rotate back to neutral")
        exit(1)
    print("OK")
    print("Use rotateBy to rotate another 10 degrees to 100")
    servo.rotateBy(10)
    if servo.getDegrees() != 100:
        print("Could not rotate to 100")
        exit(1)
    print("OK")
    print("Use rotateBy to rotate back 20 degrees to 80")
    servo.rotateBy(-20)
    if servo.getDegrees() != 80:
        print("Could not rotateback to 80")
        exit(1)
    print("OK")
    print("Use rotateBy to go under 0 , should stay at 0")
    servo.rotateBy(-120)
    if servo.getDegrees() != 0:
        print("rotateBy(-120) did not give 0 degrees")
        exit(1)
    print("OK")
    print("Use rotateBy to go over 180 , should stay at 180")
    servo.rotateTo(300)
    if servo.getDegrees() != 180:
        print("RotateBy(300) did not give 180")
        exit(1)
    print("Use rotateTo to 45 degrees")
    servo.rotateTo(45)
    if servo.getDegrees() != 45:
        print("Could not rotateTo 45 degrees")
        exit(1)
    print("OK")
    print("Test stopping the servo")
    servo.stop()
    if servo.isRunning() != False:
        print("Stop did not cause is running to be false")
        exit(1)
    print("testing Rotate to with bad values, should produce ValueError")
    print("testing with negative value")
    passed = False
    try:
        servo.rotateTo(-20)
    except ValueError, e:
        print("OK")
        passed = True

    if passed != False:
       print("Could not set negative value")
       exit(1)
    passed = False
    try:
        servo.rotateTo(300)
    except ValueError, e:
        print("OK")
        passed = True
    if passed is False:
        print("Could not set to 300")
        exit(1)
    print("All tests passed")
    print("===============")

