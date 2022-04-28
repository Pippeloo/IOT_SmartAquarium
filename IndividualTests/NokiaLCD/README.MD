# Nokia LCD
## Student
Name | Student Number | Class
-----|----------------|------
Jules Torfs | r0878800 | 1ITF05

## Specifications
Object | Type | Voltage | Input pins | Documentation
-------|------|---------|------------|--------------
Nokia 5110 LCD | Graphic LCD 84x48 - Nokia 5110 | 3V | 2 | [Link](https://robu.in/wp-content/uploads/2017/09/User_Manual_ET_LCD5110.pdf)

## Connections
Name | VCC | GND | Pin 1 | Pin 2 | Pin 3 | Pin 4 | Pin 5 | Pin 6 | 
-----|-----|-----|-------|-------|-------|-------|-------|-------|
Nokia 5110 LCD | 3V | GND | RST | CE | DC | DIN | CLK | BL |
RBPi| 3V | GND | GPIO 27 | GPIO 8 (CE0) | GPIO 22 | GPIO 10 (MOSI) | GPIO 11 (SCK) | VCC |

## Nokia LCD Class
Init the class by doing `nokiaLCD = NokiaLCD(busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO), board.D22, board.CE1, board.D27)`
Function | Parameters | Description
---------|------------|-------------
clear | (line **OPTIONAL**) | Clears the screen or the line of given. Line `0-4`
setText | (text, line) | Sets the given text on the given. Line `0-4`
showImage | (image) | Sets and shows the given image on the screen. image = path
show | () | Shows the configured text on the screen