import RPi.GPIO as io
import GpioController
from sys import exit

class ServoController(GpioController.GpioController):
   """
   Handles general servos (not continuos ones)
   """

   #constants

   def __init__(self,controllPin,):
       
