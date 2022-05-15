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
amountVerified = 0

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

# Create variables for the LCD
logoScreen = 2000
infoScreenOne = 5000
infoScreenTwo = 5000
lastScreenTime = 0
screenNumber = 0

# Create variables for the ubeac iot cloud
lastUbeac = 0
ubeacTime = 10000
oldUbeacJson = {}

# ====== MAIN ======
print('Starting...')

try:
    while True:
        # This must be done everytime the loop starts
        currentTime = time.strftime("%H:%M:%S")
        stepper.active()

        # --- WATER LEVEL ---
        # Check if button is not pressed
        if not buttonFour.isPressed():
            # check if the pump was forced to pump
            if forcePump:
                # Stop the pump
                print("=== STOP MANUAL PUMPING ===")
                forcePump = False
                relayPump.set(False)
            # return the water level every specific time
            if (millis() - lastWaterLevelMeasurement) > refreshTime:
                # Get the water level
                waterDistance = ultrasonic.getDistance()
                lastWaterLevelMeasurement = millis()
                # Print the water level in the console
                print("Water distance: " + str(round(waterDistance, 2)) + " cm")
                # Check if the water level is below the threshold
                if (waterDistance > 5) and (not pumping):
                    # Verify the water level 3 times
                    if amountVerified >= 3:
                        print("=== START PUMPING ===")
                        relayPump.set(True)
                        pumping = True
                    else:
                        amountVerified += 1
                    refreshTime = 200
                else:
                    amountVerified = 0
                    refreshTime = 2000
                # Check if the water level is above the threshold
                if pumping and (waterDistance < 3):
                    # Verify the water level 3 times
                    if amountVerified >= 3:
                        print("=== STOP PUMPING ===")
                        relayPump.set(False)
                        pumping = False
                        refreshTime = 2000
                    else:
                        amountVerified += 1
                    refreshTime = 200

        else:
            # check if the pump was not yet forced to pump
            if not forcePump:
                # Start the pump
                print("=== START MANUAL PUMPING ===")
                forcePump = True
                relayPump.set(True)
            # return the water level every specific time
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
                # toggle the lamp
                relayLamp.toggle()
                # check if the lamp is on
                if relayLamp.status():
                    print("=== LAMP ON ===")
                else:
                    print("=== LAMP OFF ===")
    

        # Check the time
        if toSeconds(currentTime) >= toSeconds(timeLampOn) and toSeconds(currentTime) < toSeconds(timeLampOff):
            # check if the lamp is not on
            if not checkedOn:
                # set the lamp on
                relayLamp.set(True)
                checkedOn = True
                checkedOff = False
        else:
            # check if the lamp is not off
            if not checkedOff:
                # set the lamp off
                relayLamp.set(False)
                checkedOn = False
                checkedOff = True

        # --- Stepper ---
        # Check if the time to feed the fish is reached
        if millis() - lastFeeder > feederTime:
            print("=== FEEDER ===")
            stepper.rotate(15.6521739, "CW")
            lastFeeder = millis()
        # Get the button status
        buttonOneStatus = buttonOne.isPressed(True)
        # Check if the button is pressed
        if lastButtonOne != buttonOneStatus:
            lastButtonOne = buttonOneStatus
            if buttonOneStatus:
                print("=== MANUAL FEEDING CW ===")
                stepper.rotate(15.6521739, "CW")
        # Get the button status
        buttonTwoStatus = buttonTwo.isPressed(True)
        # Check if the button is pressed
        if lastButtonTwo != buttonTwoStatus:
            lastButtonTwo = buttonTwoStatus
            if buttonTwoStatus:
                print("=== MANUAL FEEDING CCW ===")
                stepper.rotate(15.6521739, "CCW")
        
        # --- Display ---
        # Check if the time to display the logo is reached
        if screenNumber == 0:
            if (millis() - lastScreenTime) > infoScreenTwo:
                try:
                    nokiaLCD.showImage("assets/fish.jpg")
                except:
                    nokiaLCD.setText("ERR: IMG NOT", 0)
                    nokiaLCD.setText("FOUND", 1)
                    nokiaLCD.show()

                lastScreenTime = millis()
                # Set the next screen
                screenNumber = 1
        elif screenNumber == 1:
            if (millis() - lastScreenTime) > logoScreen:
                nokiaLCD.clear()
                nokiaLCD.setText(" === FISH === ", 0)
                nokiaLCD.setText("Time:" + time.strftime("%H:%M"), 1)
                nokiaLCD.setText("Water:" + str(round(waterDistance, 1)) + " cm", 2)
                timeTillFood = time.strftime("%M:%S", time.gmtime((millis() - lastFeeder - feederTime) * -1 / 1000)) 
                nokiaLCD.setText("Food:" + timeTillFood, 3)
                nokiaLCD.setText("==============", 4)
                nokiaLCD.show()
                lastScreenTime = millis()
                screenNumber = 2
        elif screenNumber == 2:
            if (millis() - lastScreenTime) > infoScreenOne:
                nokiaLCD.clear()
                nokiaLCD.setText("==== FISH ====", 0)
                nokiaLCD.setText("Time:" + time.strftime("%H:%M"), 1)
                #Show the current lamp status
                if relayLamp.status():
                    nokiaLCD.setText("Lamp: ON", 2)
                else:
                    nokiaLCD.setText("Lamp: OFF", 2)
                if relayLamp.status():
                    if toSeconds(currentTime) <= toSeconds(timeLampOff):
                        timeTillLampOff = toSeconds(timeLampOff) - toSeconds(currentTime)
                    else:
                        timeTillLampOff = toSeconds("23:59:59") - toSeconds(currentTime) + toSeconds(timeLampOff)
                    nokiaLCD.setText("Lamp OFF:" + time.strftime("%H:%M", time.gmtime(timeTillLampOff)), 3)
                else:
                    if toSeconds(currentTime) >= toSeconds(timeLampOn):
                        timeTillLampOn = toSeconds(timeLampOn) - toSeconds(currentTime)
                    else:
                        timeTillLampOn = toSeconds(timeLampOn) - toSeconds(currentTime)
                    nokiaLCD.setText("Lamp ON:" + time.strftime("%H:%M", time.gmtime(timeTillLampOn)), 3)
                nokiaLCD.setText("==============", 4)
                nokiaLCD.show()
                lastScreenTime = millis()
                screenNumber = 0

        # --- Ubeac ---
        # Post the data every postTime
        if (millis() - lastUbeac) > ubeacTime:
            # Check if the data changed
            if json.dumps(ubeacSensor.json) != oldUbeacJson:
                if relayLamp.status():
                    ubeacSensor.set("Lamp", 100)
                else:
                    ubeacSensor.set("Lamp", 0)

                if relayPump.status():
                    ubeacSensor.set("Pump", 100)
                else:
                    ubeacSensor.set("Pump", 0)

                ubeacSensor.set("Water Depth", round(waterDistance, 1))
                ubeacSensor.send()

                lastUbeac = millis()
        


except KeyboardInterrupt:
    print('Stopped')
    GPIO.cleanup()
    pass