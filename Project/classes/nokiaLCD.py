# =============
# Jules Torfs
# r0878800
# All rights reserved
# =============

# import the necessary packages
import os
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# ===== SETUP =====
file_path = os.path.realpath(__file__)


# ====== CLASSES ======
class NokiaLCD:
    textList = ["", "", "", "", ""]
    lines = [0, 8, 16, 24, 32]
    mode = "text" #text or image

    def __init__(self, spi, dc, cs1, reset, baudrate=1000000):
        dc = digitalio.DigitalInOut(dc)  # data/command
        cs1 = digitalio.DigitalInOut(cs1)  # chip select CE1 for display
        reset = digitalio.DigitalInOut(reset)  # reset
        # Setup the display
        self.display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate=baudrate)
        self.display.bias = 4
        self.display.contrast = 60
        self.display.invert = True
        # Clear the display.  Always call show after changing pixels to make the display update visible!
        self.display.fill(0)
        self.display.show()
        # Load default font.
        self.font = ImageFont.load_default()
        # Get drawing object to draw on image
        self.image = Image.new('1', (self.display.width, self.display.height)) 
        self.draw = ImageDraw.Draw(self.image)
        # Draw a white filled box to clear the image.
        self.draw.rectangle((0, 0, self.display.width, self.display.height), outline=255, fill=255)

    # This function shows the text on the display
    def show(self):
        # Check what if the last thing is an image, if so set the mode to text
        if self.mode == "image":
            self.mode = "text"
            self.image = Image.new('1', (self.display.width, self.display.height)) 
            self.draw = ImageDraw.Draw(self.image)
            self.draw.rectangle((0, 0, self.display.width, self.display.height), outline=255, fill=255)
        # Draw the text
        for i in range(len(self.textList)):
            self.draw.text((1, self.lines[i]), self.textList[i], font=self.font)
        self.display.image(self.image)
        # Show the display
        self.display.show()
    
    # This function clears the display, it is possible to clear a specific line
    def clear(self, line=None):
        # Check if a line number is given, if so check if the line exists and clear that line
        if line == None:
            for i in range(len(self.textList)):
                self.textList[i] = ""
            self.draw.rectangle((0, 0, self.display.width, self.display.height), outline=255, fill=255)
        elif line >= 0 and line < len(self.textList):
            self.textList[line] = ""
            self.draw.rectangle((0, self.lines[line], self.display.width, self.lines[line]+8), outline=255, fill=255)
        self.show()
    
    # This function sets the text on a specific line
    def setText(self, text, line):
        if line >= 0 and line <= 4:
            self.textList[line] = text
    
    # This function sets an image on the display
    def showImage(self, image):
        # Set the mode to image
        self.mode = "image"
        self.image = Image.open(image)
        self.display.image(self.image.resize((self.display.width, self.display.height), Image.ANTIALIAS).convert('1'))
        self.display.show()
        return file_path