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
buttonPin = 21

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

    def currentMillis(self):
        return round(time.time() * 1000)
    
    def isPressed(self, debounceActive=False):
        if debounceActive:
            self.currentState = not GPIO.input(self.pin)
            # Check if the state changes with debounce
            if self.currentState != self.lastState:
                if self.currentMillis() - self.lastMillis > self.debounce:
                    self.lastState = self.currentState
                    self.lastMillis = self.currentMillis()
                    return self.currentState
            return self.lastState
        else:
            return not GPIO.input(self.pin)

# ====== MAIN ======
button = PushButton(buttonPin)

try:
    last = False
    while True:
        current = button.isPressed()
        if last != current:
            print(current)
            last = current

except KeyboardInterrupt:
    GPIO.cleanup()
    pass


