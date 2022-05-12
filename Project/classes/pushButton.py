# =============
# Jules Torfs
# r0878800
# All rights reserved
# =============

# import the necessary packages
import RPi.GPIO as GPIO
import time

# ====== CLASSES ======
class PushButton:
    lastMillis = 0
    lastState = False
    # debounce time in milliseconds
    debounce = 100

    def __init__(self, pin):
        self.pin = pin
        # set the pin as input
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.lastState = not GPIO.input(self.pin)

    # this function returns the current time in milliseconds
    def currentMillis(self):
        return round(time.time() * 1000)
    
    # this function returns the state of the button
    def isPressed(self, debounceActive=False):

        # check if debounce is active
        if debounceActive:
            self.currentState = not GPIO.input(self.pin)
            # Check if the state changes with debounce
            if self.currentState != self.lastState:
                if self.currentMillis() - self.lastMillis > self.debounce:
                    self.lastState = self.currentState
                    self.lastMillis = self.currentMillis()
                    # return the state of the button
                    return self.currentState
            # return the last state of the button
            return self.lastState
        else:
            # return the state of the button
            return not GPIO.input(self.pin)
