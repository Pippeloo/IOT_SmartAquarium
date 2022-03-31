# =============
# Jules Torfs
# r0878800
# All rights reserved
# =============

class Stepper:
    coils = [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 1]
    ]
    steps = 0
    # According to the source below the gear ratio is 1/63.68395 instead of 1/64. I calculated it at 63.6875, this way it's 0 degrees after a full rotation. (4076 steps)
    # https://www.makerguides.com/28byj-48-stepper-motor-arduino-tutorial/
    degreesPerHalfStep = 5.625 / 63.6875
    oneRevolutuion = 4076
    delay = 0.001
    lastMillis = 0
    running = False
    direction = "CW"
    degreesCurrentRotation = 0
    requestedRotation = 0

    def __init__(self, pins):
        self.pins = pins
        # set the pins as output
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, self.coils[0][self.pins.index(pin)])

    def active(self):
        if self.running:
            if self.requestedRotation >= round(self.degreesCurrentRotation, 2):
                if self.lastMillis < self.currentMillis() - (self.delay*1000):
                    self.lastMillis = self.currentMillis()
                    self.doSteps(self.direction)
                    self.degreesCurrentRotation += self.degreesPerHalfStep
            else:
                self.running = False

    def currentMillis(self):
        return int(round(time.time() * 1000))
    
    def doSteps(self, direction):
        if direction == "CW":
            self.steps += 1
        elif direction == "CCW":
            self.steps -= 1
        
        # calculate the current coil
        coil = self.coils[self.steps % len(self.coils)]

        # set the pins
        for i in range(len(self.pins)):
            GPIO.output(self.pins[i], coil[i])

    def getDegrees(self):
        return (self.steps * self.degreesPerHalfStep) % 360
    
    def rotate(self, degrees, direction):
        if direction == "CW" or direction == "CCW":
            self.direction = direction
            self.requestedRotation = degrees
            self.degreesCurrentRotation = 0
            self.running = True
    
    def stop(self):
        self.running = False