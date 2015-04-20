import RPIO as io
from RPIO import PWM
import GpioController
import time
from sys import exit

class ServoController(GpioController.GpioController):
    """
   Handles general servos (not continuos ones)
   """

   #constants
    # DEFAULT_FREQ = 50
    ANGLE_NEUTRAL=1600
    DEGREE_NEUTRAL=90
    ANGLE_ZERO=700
    DEGREE_ZERO = 0
    ANGLE_180=2500
    DEGREE_180 = 180

    def __init__(self,controllPin,directStart=True,boardmode="BCM"):
        super(ServoController, self).__init__([controllPin], boardmode)
        # Setup
        io.setwarnings(False)
        # io.setup(controllPin, io.OUT)
        self._servo = PWM.Servo() 
        self._pin = controllPin
        # self._pwm = io.PWM(controllPin, self.DEFAULT_FREQ)
        self._currentDirection = self.ANGLE_NEUTRAL
        self._currentDirectionDegrees = self.DEGREE_NEUTRAL 
        self._running = False
        if directStart is True:
            self.start()

    def start(self):
        if self._running is False:
            # self._pwm.start(self._currentDirection)
            self._servo.set_servo(self._pin, self._currentDirection)
            self._running = True

    def stop(self):
        if self._running is True:
            # self._pwm.stop()
            self._servo.stop_servo(self._pin)
            self._running = False

    def rotateToNeutral(self):
        self._currentDirection = self.ANGLE_NEUTRAL
        self._currentDirectionDegrees = self.DEGREE_NEUTRAL
        self._updateAngle()

    def rotateToZero(self):
        self._currentDirection = self.ANGLE_ZERO
        self._currentDirectionDegrees = self.DEGREE_ZERO
        self._updateAngle()

    def rotateTo180(self):
        self._currentDirection = self.ANGLE_180
        self._currentDirectionDegrees = self.DEGREE_180
        self._updateAngle()

    def rotateTo(self,degrees):
        if(int(degrees) < 0 or int(degrees) > 180):
            raise ValueError ("input should be between 0 and 180 degrees (int), got: %s" % degrees)
        convDegrees = self._convertDegrees(degrees)
        self._currentDirection = convDegrees
        self._currentDirectionDegrees = degrees
        self._updateAngle()

    def rotateBy(self,degrees):
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

    def getDegrees(self):
        return self._currentDirectionDegrees

    def isRunning(self):
        return self._running

    def _updateAngle(self):
        # self._pwm.ChangeDutyCycle(self._currentDirection)
        self._servo.set_servo(self._pin, self._currentDirection)

    def _convertDegrees(self,degrees):
        k = (self.ANGLE_180 - self.ANGLE_ZERO) / (self.DEGREE_180 - self.DEGREE_ZERO)
        #y = kx + m
        returnValue = ( k * int(degrees) ) + self.ANGLE_ZERO
        return returnValue

# Tests
if __name__ == '__main__':
    sleepTime = 2
    print("======= ServoController ========")
    print("Please ensure that you have nothing connected on pin 21 (BCM)  of your RasPi")
    print("as this script will use that pin for tests!")
    sure = raw_input("Are you sure nothing is connected to pin 21? Y/n :")
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
    time.sleep(sleepTime)
    if servo.isRunning() == False:
        print("Started but isRunning was false.")
        exit(1)
    print("OK")
    print("Rotate it to 0 and check the getDegrees")
    servo.rotateToZero()
    time.sleep(sleepTime)
    if servo.getDegrees() != 0:
        print("It was not 0 degrees")
        exit(1)
    print("OK")
    print("Rotate it to 180 degrees and check")
    servo.rotateTo180()
    time.sleep(sleepTime)
    if servo.getDegrees() != 180:
        print("Could not rotate to 180 degrees")
        exit(1)
    print("OK")
    print("Rotate it back to neutral")
    servo.rotateToNeutral()
    time.sleep(sleepTime)
    if servo.getDegrees() != 90:
        print("Could not rotate back to neutral")
        exit(1)
    print("OK")
    print("Use rotateBy to rotate another 10 degrees to 100")
    servo.rotateBy(10)
    time.sleep(sleepTime)
    if servo.getDegrees() != 100:
        print("Could not rotate to 100")
        exit(1)
    print("OK")
    print("Use rotateBy to rotate back 20 degrees to 80")
    servo.rotateBy(-20)
    time.sleep(sleepTime)
    if servo.getDegrees() != 80:
        print("Could not rotateback to 80")
        exit(1)
    print("OK")
    print("Use rotateBy to go under 0 , should stay at 0")
    servo.rotateBy(-120)
    time.sleep(sleepTime)
    if servo.getDegrees() != 0:
        print("rotateBy(-120) did not give 0 degrees")
        exit(1)
    print("OK")
    print("Use rotateBy to go over 180 , should stay at 180")
    servo.rotateBy(300)
    time.sleep(sleepTime)
    if servo.getDegrees() != 180:
        print("RotateBy(300) did not give 180")
        exit(1)
    print("OK")
    print("Use rotateTo to 45 degrees")
    servo.rotateTo(45)
    time.sleep(sleepTime)
    if servo.getDegrees() != 45:
        print("Could not rotateTo 45 degrees")
        exit(1)
    print("OK")
    print("Test stopping the servo")
    servo.stop()
    time.sleep(sleepTime)
    if servo.isRunning() != False:
        print("Stop did not cause is running to be false")
        exit(1)
    print("OK")
    print("testing Rotate to with bad values, should produce ValueError")
    print("testing with negative value")
    passed = False
    try:
        servo.rotateTo(-20)
    except ValueError, e:
        print("OK")
    servo.cleanup()
    print("testing with a big postive value")
    #new servo
    servo = ServoController(21)
    try:
        servo.rotateTo(300)
    except ValueError, e:
        print("OK")

    print("All tests passed")
    print("===============")
    servo.cleanup()

