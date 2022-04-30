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

# ===== FUNSTIONS =====
def millis():
    return round(time.time() * 1000)

def toSeconds(t):
    h, m, s = [int(i) for i in t.split(':')]
    return 3600*h + 60*m + s

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
forcePump = False
refreshTime = 2000

# Create variables for the lamp
lastLampState = False
lastButtonThree = False
buttonThreeStatus = False
debounceButtonThree = 0
timeLampOn = "08:00:00"
timeLampOff = "20:00:00"
checkedOn = False
checkedOff = False

# Create variables for the feeder
lastFeeder = millis() - 840000 # - 14 minutes
feederTime = 900000 # 15 minutes
buttonTwoStatus = False
buttonOneStatus = False
lastButtonOne = False
lastButtonTwo = False

# ====== MAIN ======
print('Starting...')

try:
    while True:
        currentTime = time.strftime("%H:%M:%S")
        stepper.active()

        # --- WATER LEVEL ---
        if not buttonFour.isPressed():
            if forcePump:
                print("=== STOP MANUAL PUMPING ===")
                forcePump = False
                relayPump.set(False)
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
        else:
            if not forcePump:
                print("=== START MANUAL PUMPING ===")
                forcePump = True
                relayPump.set(True)
            if (millis() - lastWaterLevelMeasurement) > 200:
                waterDistance = ultrasonic.getDistance()
                lastWaterLevelMeasurement = millis()
                print("Water distance: " + str(round(waterDistance, 2)) + " cm")

        # --- LAMP ---
        # Toggle button
        currentButtonThree = buttonThree.isPressed()
        if buttonThreeStatus != currentButtonThree:
            buttonThreeStatus = currentButtonThree
            # toggle the lamp when a pulse is detected
            if buttonThreeStatus:
                relayLamp.toggle()
                if relayLamp.status():
                    print("=== LAMP ON ===")
                    print(millis())
                else:
                    print("=== LAMP OFF ===")
    

        # Check the time
        if toSeconds(currentTime) >= toSeconds(timeLampOn) and toSeconds(currentTime) < toSeconds(timeLampOff):
            if not checkedOn:
                relayLamp.set(True)
                checkedOn = True
                checkedOff = False
        else:
            if not checkedOff:
                relayLamp.set(False)
                checkedOn = False
                checkedOff = True

        # --- Stepper ---
        if millis() - lastFeeder > feederTime:
            print("=== FEEDER ===")
            stepper.rotate(36, "CW")
            lastFeeder = millis()

        buttonOneStatus = buttonOne.isPressed(True)
        if lastButtonOne != buttonOneStatus:
            lastButtonOne = buttonOneStatus
            if buttonOneStatus:
                print("=== MANUAL FEEDING CW ===")
                stepper.rotate(36, "CW")

        buttonTwoStatus = buttonTwo.isPressed(True)
        if lastButtonTwo != buttonTwoStatus:
            lastButtonTwo = buttonTwoStatus
            if buttonTwoStatus:
                print("=== MANUAL FEEDING CCW ===")
                stepper.rotate(36, "CCW")

except KeyboardInterrupt:
    print('Stopped')
    GPIO.cleanup()