from classes.stepper import Stepper
from classes.pushButton import PushButton
from classes.ultrasonicSensor import UltrasonicSensor
from classes.relay import Relay
from classes.nokiaLCD import NokiaLCD
from classes.ubeacSensor import UbeacSensor
import time
import RPi.GPIO as GPIO
import busio
import board
import json

GPIO.setmode(GPIO.BCM)

stepperPins = [26, 19, 13, 6]
buttonPins = [21, 20, 16, 12]
ultrasonicTriggerPin = 23
ultrasonicEchoPin = 24
relayLampPin = 4
relayPumpPin = 17

stepper = Stepper(stepperPins)
buttonOne = PushButton(buttonPins[0])
buttonTwo = PushButton(buttonPins[1])
buttonThree = PushButton(buttonPins[2])
buttonFour = PushButton(buttonPins[3])
ultrasonic = UltrasonicSensor(ultrasonicEchoPin, ultrasonicTriggerPin)
relayLamp = Relay(relayLampPin)
relayPump = Relay(relayPumpPin)
nokiaLCD = NokiaLCD(busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO), board.D22, board.CE1, board.D27)
ubeacSensor = UbeacSensor("https://pippeloo.hub.ubeac.io/Station", "Raspberry-Pi")

shouldRun = True
lastButtonOne = False
lastButtonTwo = False
lastButtonThree = False
lastButtonFour = False
counter = 0
ubeac_json = json.dumps(ubeacSensor.json)
print('Starting...')

# ====== MAIN ======
relayLamp.set(True)
relayPump.set(True)

print("Rotating CW")
stepper.rotate(360, "CW")
nokiaLCD.setText("==== FISH ====", 0)

try:
    while True:
        stepper.active()

        if shouldRun:
            if not stepper.running:
                if stepper.direction == "CW":
                    print("Rotating CCW")
                    stepper.rotate(360, "CCW")
                else:
                    print("Stopped")
                    stepper.stop()
                    shouldRun = False
        
        buttonOneStatus = buttonOne.isPressed(True)
        buttonTwoStatus = buttonTwo.isPressed(True)
        buttonThreeStatus = buttonThree.isPressed(True)
        buttonFourStatus = buttonFour.isPressed(True)
        
        if lastButtonOne != buttonOneStatus:
            print("Button One: " + str(buttonOneStatus))
            lastButtonOne = buttonOneStatus
            if buttonOneStatus:
                print("Distance measured: " + str(ultrasonic.getDistance()) + " cm")
        if lastButtonTwo != buttonTwoStatus:
            print("Button Two: " + str(buttonTwoStatus))
            lastButtonTwo = buttonTwoStatus
            if buttonTwoStatus:
                relayLamp.toggle()
                ubeacSensor.set("Lamp", int(relayLamp.status())*100)
        if lastButtonThree != buttonThreeStatus:
            print("Button Three: " + str(buttonThreeStatus))
            lastButtonThree = buttonThreeStatus
            if buttonThreeStatus:
                relayPump.toggle()
                ubeacSensor.set("Pump", int(relayPump.status())*100)
        if lastButtonFour != buttonFourStatus:
            print("Button Four: " + str(buttonFourStatus))
            lastButtonFour = buttonFourStatus
            if buttonFourStatus:
                counter += 1
                nokiaLCD.clear(1)
                nokiaLCD.setText("Push Count: " + str(counter), 1)
                nokiaLCD.show()
                ubeacSensor.set("Water Depth", counter)
        
        if json.dumps(ubeacSensor.json) != ubeac_json:
            ubeac_json = json.dumps(ubeacSensor.json)
            print("Sending data to Ubeac")
            ubeacSensor.send()



except KeyboardInterrupt:
    GPIO.cleanup()
    pass