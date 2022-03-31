# Stepper Motor
## Student
Name | Student Number | Class
-----|----------------|------
Jules Torfs | r0878800 | 1ITF05

## Specifications
Object | Type | Voltage | Input pins | Documentation
-------|------|---------|------------|--------------
Stepper Motor | 28BYJ-48 | 5V | 4 | [Link](https://components101.com/sites/default/files/component_datasheet/28byj48-step-motor-datasheet.pdf)
Driver | Stepper Motor Driver ULN2003A | 5V | 4 | [Link](https://www.electronicoscaldas.com/datasheet/ULN2003A-PCB.pdf)

## Connections
Name | VCC | GND | Pin 1 | Pin 2 | Pin 3 | Pin 4
-----|-----|-----|-------|-------|-------|------
Driver | 6V Battery Pack | GND | IN 1 | IN 2 | IN 3 | IN 4 
RBPi| / | GND | GPIO 26 | GPIO 19 | GPIO 13 | GPIO 06

## Stepper Class
Init the class by doing `stepper = Stepper(<pins>)`
Function | Parameters | Description
---------|------------|-------------
active | () | Put this in your main loop, this way the class is activated.
rotate | (degrees, direction) | <ul><li>degrees must be greater then 0</li><li>direction must be `CW` or `CCW`</li></ul>
stop | () | Stops the motor from rotating.
doSteps | (direction) | Does one step (`0.08832...°`) in the direction of choice: `CW` or `CCW`.
getDegrees | () | returns the current rotation (`0 - 359.99°`)

**WARNING**: You can not use any delays in the script!