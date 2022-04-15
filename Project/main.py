from classes.stepper import Stepper
from classes.pushButton import PushButton
from classes.ultrasonicSensor import UltrasonicSensor
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

stepperPins = [26, 19, 13, 6]
buttonPins = [21, 20, 16, 12]
ultrasonicTriggerPin = 23
ultrasonicEchoPin = 24

stepper = Stepper(stepperPins)
buttonOne = PushButton(buttonPins[0])
buttonTwo = PushButton(buttonPins[1])
buttonThree = PushButton(buttonPins[2])
buttonFour = PushButton(buttonPins[3])
ultrasonic = UltrasonicSensor(ultrasonicEchoPin, ultrasonicTriggerPin)

shouldRun = True
lastButtonOne = False
lastButtonTwo = False
lastButtonThree = False
lastButtonFour = False

# ====== MAIN ======
print("Rotating CW")
stepper.rotate(360, "CW")

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
        if lastButtonThree != buttonThreeStatus:
            print("Button Three: " + str(buttonThreeStatus))
            lastButtonThree = buttonThreeStatus
        if lastButtonFour != buttonFourStatus:
            print("Button Four: " + str(buttonFourStatus))
            lastButtonFour = buttonFourStatus


except KeyboardInterrupt:
    GPIO.cleanup()
    pass