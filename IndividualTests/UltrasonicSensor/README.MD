# Ultrasonic Sensor
## Student
Name | Student Number | Class
-----|----------------|------
Jules Torfs | r0878800 | 1ITF05

## Specifications
Object | Type | Voltage | Input pins | Documentation
-------|------|---------|------------|--------------
Ultrasonic Sensor | HC-SR04 | 5V | 2 | [Link](https://pdf1.alldatasheet.com/datasheet-pdf/view/1132203/ETC2/HC-SR04.html)

## Connections
Name | VCC | GND | Pin 1 | Pin 2 
-----|-----|-----|-------|-------
Ultrasonic Sensor | 5V | GND | TRIG | ECHO
RBPi| 5V | GND | GPIO 23 | GPIO 24 

**NOTE**: There has to be a voltage devider for the echo pin! View the schema below!

![Voltage-Devider](assets/hc-sr04_connections.jpg?raw=true)

## Ultrasonic Sensor Class
Init the class by doing `ultrasonic = UltrasonicSensor(<pins>)`
Function | Parameters | Description
---------|------------|-------------
getDistance | () | This returns the distance that is measured in cm

**WARNING**: This script contains a delay of 1ms