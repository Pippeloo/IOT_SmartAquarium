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
echoPin = 24
trigPin = 23

# ====== CLASSES ======
class UltrasonicSensor:

    def __init__(self, echoPin, trigPin):
        self.echoPin = echoPin
        self.trigPin = trigPin
        # set the pins
        GPIO.setup(self.echoPin, GPIO.IN)
        GPIO.setup(self.trigPin, GPIO.OUT)
        # set the trigger to low
        GPIO.output(self.trigPin, GPIO.LOW)

    def getDistance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigPin, True)
 
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigPin, False)
 
        self.startTime = time.time()
        self.timeout = self.startTime + 0.04
        # save StartTime
        while GPIO.input(self.echoPin) == 0 and self.startTime < self.timeout:
            self.startTime = time.time()

        self.stopTime = time.time()
         # save time of arrival
        while GPIO.input(self.echoPin) == 1 and self.stopTime < self.timeout:
            self.stopTime = time.time()
 
        # time difference between start and arrival
        self.timeElapsed = self.stopTime - self.startTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        self.distance = (self.timeElapsed * 34300) / 2
 
        return self.distance
    




# ====== MAIN ======
ultrasonicSensor = UltrasonicSensor(echoPin, trigPin)

try:
    while True:
        distance = str(ultrasonicSensor.getDistance()) + " cm"
        print(distance)
        time.sleep(0.1)
        




except KeyboardInterrupt:
    GPIO.cleanup()
    pass


