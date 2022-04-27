# Relay
## Student
Name | Student Number | Class
-----|----------------|------
Jules Torfs | r0878800 | 1ITF05

## Specifications
Object | Type | Voltage | Input pins | Documentation
-------|------|---------|------------|--------------
4 Relay Module | HW316 | 5V | 4 | [Link](http://wiki.sunfounder.cc/index.php?title=4_Channel_5V_Relay_Module)

## Connections
Name | VCC | GND | Pin 1 | Pin 2 | Pin 3 | Pin 4
-----|-----|-----|-------|-------|-------|-------
Relays | 5V | GND | IN1 | IN2 | IN3 | IN4
RBPi| 5V | GND | GPIO 4 | GPIO 17 |  | 

## Relay Class
Init the class by doing `relay = Relay(pin)`
Function | Parameters | Description
---------|------------|-------------
set | ( Boolean ) | Sets the status of the relay
toggle | () | Toggle the value of the relay
status | () | Returns the current status of the relay

**Warning:** The relays work inverted!