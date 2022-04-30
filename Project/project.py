# =============
# Jules Torfs
# r0878800
# All rights reserved
# =============

# import the classes
from classes.stepper import Stepper
from classes.pushButton import PushButton
from classes.ultrasonicSensor import UltrasonicSensor
from classes.relay import Relay
from classes.nokiaLCD import NokiaLCD
from classes.ubeacSensor import UbeacSensor

# import the necessary packages
import RPi.GPIO as GPIO
import busio
import board
import json
import time

# ===== SETUP =====
# Setup the pins
STEPPER_PINS = [26, 19, 13, 6]
BUTTON_PINS = [21, 20, 16, 12]
ULTRASONIC_TRIGGER_PIN = 23
ULTRASONIC_ECHO_PIN = 24
RELAY_LAMP_PIN = 4
RELAY_PUMP_PIN = 17

# Setup the classes
stepper = Stepper(STEPPER_PINS)
buttonOne = PushButton(BUTTON_PINS[0])
buttonTwo = PushButton(BUTTON_PINS[1])
buttonThree = PushButton(BUTTON_PINS[2])
buttonFour = PushButton(BUTTON_PINS[3])
ultrasonic = UltrasonicSensor(ULTRASONIC_ECHO_PIN, ULTRASONIC_TRIGGER_PIN)
relayLamp = Relay(RELAY_LAMP_PIN)
relayPump = Relay(RELAY_PUMP_PIN)
nokiaLCD = NokiaLCD(busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO), board.D22, board.CE1, board.D27)
ubeacSensor = UbeacSensor("https://pippeloo.hub.ubeac.io/Station", "Raspberry-Pi")

# Set default pin states
relayLamp.set(False)
relayPump.set(False)

# --- Create the variables ---

# Create variables for the pump
lastWaterLevelMeasurement = 0
waterDistance = 0
pumping = False
refreshTime = 2000

# ===== FUNSTIONS =====
def millis():
    return round(time.time() * 1000)

# ====== MAIN ======
print('Starting...')

try:
    while True:
        if (millis() - lastWaterLevelMeasurement) > refreshTime:
            waterDistance = ultrasonic.getDistance()
            lastWaterLevelMeasurement = millis()
            print("Water distance: " + str(round(waterDistance, 2)) + " cm")
            if (waterDistance > 5) and (not pumping):
                print("=== START PUMPING ===")
                relayPump.set(True)
                pumping = True
                refreshTime = 200

            if pumping and (waterDistance < 3):
                print("=== STOP PUMPING ===")
                relayPump.set(False)
                pumping = False
                refreshTime = 2000


except KeyboardInterrupt:
    print('Stopped')
    GPIO.cleanup()