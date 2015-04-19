import RPi.GPIO as io
import GpioController
from sys import exit


class MotorController(GpioController.GpioController):

    # constants
    FORWARD = "forward"
    REVERSE = "reverse"
    DEFAULT_FREQ = 100
    DEFAULT_MAX = 100

    def __init__(self, enablePin, in1pin, in2pin, direction="forward", boardmode="BCM"):
        super(MotorController, self).__init__([enablePin,in1pin,in2pin],boardmode)
        # check direction
        if(direction == self.FORWARD):
            self.direction = self.FORWARD
        elif(direction == self.REVERSE):
            self.direction = self.REVERSE
        else:
            super(MotorController, self).cleanup()
            raise ValueError('%s not allowed, use "forward" or "reverse"' % direction)
        self.enablePin = enablePin
        self.in1pin = in1pin
        self.in2pin = in2pin
        # setup pins
        io.setup(self.enablePin, io.OUT)
        io.setup(self.in1pin, io.OUT)
        io.setup(self.in2pin, io.OUT)
        # setup pwm
        self.pwm = io.PWM(enablePin, self.DEFAULT_FREQ)
        self.pwm.start(0)
        if(self.direction == self.FORWARD):
            self._goForward()
        else:
            self._goReverse()

    def _goForward(self):
        io.output(self.in1pin, 1)
        io.output(self.in2pin, 0)
        self.direction = self.FORWARD

    def _goReverse(self):
        io.output(self.in1pin, 0)
        io.output(self.in2pin, 1)
        self.direction = self.REVERSE

    def toggleDirection(self):
        if(self.direction == self.FORWARD):
            self._goReverse()
        else:
            self._goForward()

    def forward(self, speed=None):
        self._goForward()
        if speed is not None:
            self.changeSpeed(speed)

    def reverse(self, speed=None):
        self._goReverse()
        if speed is not None:
            self.changeSpeed(speed)

    def stop(self):
        io.output(self.in1pin, 0)
        io.output(self.in2pin, 0)

#    def cleanup(self):
#        self.pwm.stop()
#        io.cleanup()

    # takes a value from 0 -> 100 and scales it
    # with DEFAULT_MAX
    def changeSpeed(self, newSpeed):
        # first scale it
        scale = float(self.DEFAULT_MAX) / float(100)
        newSpeed = int(newSpeed * scale)
        self.pwm.ChangeDutyCycle(newSpeed)

# tests
if __name__ == '__main__':

    print("Running tests:")
    # run the usual tests (check that things fail)
    # test direction fail
    try:
        print("Inccorect Direction value fail:")
        motor = MotorController(4, 17, 18, "nonsense")
    except ValueError, e:
        print("OK")
    motor = None

    # board fail
    try:
        print("Incorrect Board value fail:")
        motor = MotorController(4, 17, 18, "forward", "nonsense")
    except ValueError, e:
        print("OK")
    motor = None

    # test pin fail
    try:
        print("Incorrect pin number fail:")
        motor = MotorController(0, 244, 75)
    except ValueError, e:
        print("OK")
    motor = None

    # test same pin fail
    try:
        print("Same pin number fail:")
        motor = MotorController(4, 4, 4)
    except ValueError, e:
        print("OK")
    motor = None

    # ask user what to test
    checkMotor = raw_input("Do you want to test with a real motor? Y/n: ")
    if checkMotor == "Y":
        checkMotor = True
    else:
        checkMotor = False
    # if we should check the motor we just quit
    if checkMotor is False:
        print("All tests passed!")
        exit(0)

    # check that everything is connected
    print("This test assumes that you have an L293D")
    print("connected to GPIO of Rpi")
    print("with the following connections:")
    print("BCM:    BOARD:  ->   L293D(Pin):")
    print("18      1            EN1 (1)")
    print("4       7            IN1 (2)")
    print("17      0            IN2 (7)")
    print("And ofcourse a motor connected to L293D with")
    print("connections to ground and power etc...")
    print("--------------------------------------------")
    checkAllIsGood = raw_input("Is everything connected and ready? Y/n: ")
    if checkAllIsGood != "Y":
        print("Aborting tests!")
        exit(0)
    # we proceed
    print("Creating a motor ...")
    try:
        motor = MotorController(18, 4, 17)
    except Exception, e:
        print("Error creating motor... Aborting with error:")
        print(e)
        exit(1)

    print("Done")
    print("Testing to create a motor with the same pins, should fail:")
    try:
        passedDoubleMotorTest = False
        motor2 = MotorController(4, 18, 17)
    except ValueError, e:
        print("OK")
        passedDoubleMotorTest = True
    if passedDoubleMotorTest is False:
        print("Failed! Was able to create second motor. Aborting")
        exit(0)
    motor2 = None

    print("Running motor with a low speed of 10 (forward)")
    motor.changeSpeed(10)
    ok = raw_input("Did it work? Y/n")
    if ok != "Y":
        print("Aborting...")
        motor.cleanup()
        exit(0)
    print("Increasing speed to 40")
    motor.changeSpeed(40)
    ok = raw_input("Did it work? Y/n")
    if ok != "Y":
        print("Aborting...")
        motor.cleanup()
        exit(0)
    print("Changing direction")
    motor.toggleDirection()
    ok = raw_input("Did it work? Y/n")
    if ok != "Y":
        print("Aborting...")
        motor.cleanup()
        exit(0)
    print("Stopping motor")
    motor.stop()
    ok = raw_input("Did it work? Y/n")
    if ok != "Y":
        print("Aborting...")
        motor.cleanup()
        exit(0)
    print("Reverse motor with speed of 50")
    motor.reverse(50)
    ok = raw_input("Did it work? Y/n")
    if ok != "Y":
        print("Aborting...")
        motor.cleanup()
        exit(0)
    print("Test all passed!")
    print("Cleaning up")
    motor.cleanup()



