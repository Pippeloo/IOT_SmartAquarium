# =============
# Jules Torfs
# r0878800
# All rights reserved
# =============

# import the necessary packages
import RPi.GPIO as GPIO
import time

#  ====== SETUP ======
# set the gpio mode
GPIO.setmode(GPIO.BCM)

# define the pins of the modules
relayPin = 4

# ====== CLASSES ======
class Relay:

    def __init__(self, pin):
        self.pin = pin
        # set the pin as output
        GPIO.setup(pin, GPIO.OUT)
    
    # This function sets the state of the relay
    def set(self, state):
        GPIO.output(self.pin, not state)

    # This function toggles the state of the relay
    def toggle(self):
        self.set(GPIO.input(self.pin))
    
    # This function returns the state of the relay
    def status(self):
        return not GPIO.input(self.pin)
