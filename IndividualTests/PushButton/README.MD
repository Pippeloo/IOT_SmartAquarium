# Push Button
## Student
Name | Student Number | Class
-----|----------------|------
Jules Torfs | r0878800 | 1ITF05

## Connections
Name | GND | Pin 1 
-----|-----|-------
Button | GND | GPIO 21

**NOTE:** No resistor is needed between the Raspberry Pi and the button!

## Push Button
Init the class by doing `pushButton = PushButton(<pin>)`

**NOTE:** This class uses the input pullop of the raspberry pi

Function | Parameters | Description
---------|------------|-------------
isPressed | ( **OPTIONAL** debounceActive ) | Looks if the button is pressed. When debounceActive is `TRUE` it uses a debounce, when `FALSE` it reads directly.

**WARNING**: You can not use any delays in the script!