# lingon-gpio

Files that i use with my Raspberry pi and it's gpio 

Beware if you use this, it's only for my model (model B) and has not been tested for other models.
As soon as i get my hands on a Raspi2 i will be updating these scripts

## MotorController

Intended to be used with the L239D-chipset that need 3 gpio pins
- Enable
- In 1
- In 2

### Usage
Example:
```python

import MotorController

#setup
enablePin = 18
in1Pin = 4
in2Pin = 17

motor = MotorController.MotorController(enablePin, in1Pin, in2Pin)

#Go forward at half-speed
motor.forward(50)

#stop
motor.cleanup()
```

See the manual page for MotorController for more information

## Sr04Controller

For use with HC-SR04 ultrasonic range sensor, and it uses two pins
- Trigger
- Echo

**Warning**

The sensor sends back a response to echo pin but with a 5v voltage, if you do not use
a voltage divider to bring this down to 3.3v you may break youre RasPi! 

Please read this tutorial (which this class is based on) if you are unsure what that means:

http://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

### Usage
Example:
```python

import Sr04Controller

#setup
triggerPin = 21
echoPin = 25

sensor = Sr04Controller(triggerPin, echoPin)

dist = sensor.measure()
print('Distance: %s cm' % dist)
```

See the manual page for Sr04Controller for more information
