import RPi.GPIO as io
from sys import exit

class gpioController:

    #constants
    BOARD_MODE=""
    BCM = "BCM"
    BOARD = "BOARD"
    ALLOWED_PINS_BCM = [4, 17, 18, 21, 22, 23, 24, 25]
    ALLOWED_PINS_BOARD = [0, 1, 2, 3, 4, 5, 6, 7]
    ALLOWED_PINS = []
    USED_PINS = []
    INITIATED = False

    def __init__(self, pins, boardmode="BCM", showWarnings=False):
        #set warnings in io
        if showWarnings is False:
            io.setwarnings(False)
        else:
            io.setwarnings(True)
        #initiate the board
        if self.INITIATED is False:
            if boardmode=="BCM":
                self.BOARD_MODE="BCM"
                self.ALLOWED_PINS = self.ALLOWED_PINS_BCM
                io.setmode(io.BCM)
                self.INITIATED = True
            elif boardmode=="BOARD":
                self.BOARD_MODE="BOARD"
                self.ALLOWED_PINS = self.ALLOWED_PINS_BOARD
                io.setmode(io.BOARD)
                self.INITIATED = True
            else:
                raise ValueError('%s is not an allowed, use "BCM" or "BOARD"' % boardmode)
        else: #INITIATED == TRUE
            # check that we dont have two conflicting modes
            if(boardmode != self.BOARD_MODE):
                raise ValueError('Board mode is already set to %s , cannot use another mode' % self.BOARD_MODE)
        # Check pins
        for pin in pins:
            if(pin not in self.ALLOWED_PINS):
                raise ValueError('%s is not an allowed pin for %s' % (pin, self.BOARD_MODE))
            if(pin in self.USED_PINS):
                raise ValueError('Pin %s is already in use by another device' % pin)
            # Pin is ready to use
            self.USED_PINS.append(pin)

# Tests
if __name__ == '__main__':

    print("==== gpioController - tests ====")
    # test pins
    try:
        print("-------------------------------")
        print("Wrong pin numbers")
        t1 = gpioController([777,444,333])
    except ValueError, e:
        print("OK")
        print(e)
    t1 = None
    try:
        print("-------------------------------")
        print("Wrong boardname")
        t1 = gpioController([4],"NOTABOARD")
    except ValueError, e:
        print("OK")
        print(e)
    t1 = None
    try:
        print("-------------------------------")
        print("Same pin numbers in the same init")
        t1 = gpioController([4,4,4])
    except ValueError, e:
        print("OK")
        print(e)
    t1 = None
    try:
        print("-------------------------------")
        print("Using the same pin in two different controllers")
        print("the second init should fail")
        print("First one")
        t1 = gpioController([4,17,18])
    except ValueError, e:
        print("Failed to create first one!")
        print(e)
        sys.exit(1)
    try:
        print("Second one")
        t2 = gpioController([21,22,4])
    except ValueError, e:
        print("OK")
        print(e)
    t1 = None
    t2 = None
    try:
        print("-------------------------------")
        print("Try using two different boardmodes")
        print("Creating first one with BCM")
        t1 = gpioController([4],"BCM")
    except ValueError, e:
        print("First one failed!")
        print(e)
        sys.exit(1)
    try:
        print("Creating second one with BOARD")
        t2 = gpioController([1],"BOARD")
    except ValueError, e:
        print("OK")
        print(e)
