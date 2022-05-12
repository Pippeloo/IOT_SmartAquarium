# =============
# Jules Torfs
# r0878800
# All rights reserved
# =============

# import the classes
from classes.relay import Relay

# import the necessary packages
from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
import time
import json

# ===== FUNSTIONS =====
# This function returns the time in milliseconds
def millis():
    return round(time.time() * 1000)

# ===== SETUP =====
# Setup the pins
RELAY_LAMP_PIN = 4

# Setup the classes
relayLamp = Relay(RELAY_LAMP_PIN)

# --- Create the variables ---
# Create variables for the webserver
HOSTNAME = "localhost"
SERVER_PORT = 6969
json_data = {"status": "off"}

# Create variables for the timers
timerBusy = False
timerStart = 0
timeUntillLightOff = 9000 # 15 minutes

# --- SETUP CLASS ---
class MyServer(BaseHTTPRequestHandler):
    # This function is called when the server receives a GET request
    def do_GET(self):
        # Use the global variables
        global timerBusy, timerStart, timeUntillLightOff
        # Return that the request was successful
        self.send_response(200)
        # Return the content type
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # Check the requested path
        if self.path == "/light/status":
            # Save the state of the relay
            if relayLamp.status():
                json_data["status"] = "on"
            else:
                json_data["status"] = "off"
                timerBusy = False

            if timerBusy and (millis() - timerStart > timeUntillLightOff):
                timerBusy = False
                relayLamp.set(False)
                json_data["status"] = "off"

            # Return the json data
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        if self.path == "/light/on":
            # Set the state of the relay
            json_data["status"] = "on"
            relayLamp.set(True)
            # Check if the timer is busy
            if not timerBusy:
                timerBusy = True
                timerStart = millis()
            # Return the json data
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        if self.path == "/light/off":
            # Set the state of the relay
            json_data["status"] = "off"
            relayLamp.set(False)
            # Return the json data
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))

    def log_message(self, format, *args):
        pass


# ===== MAIN =====    
if __name__ == "__main__":
    # Create the server
    webServer = HTTPServer((HOSTNAME, SERVER_PORT), MyServer)
    print("Server started http://%s:%s" % (HOSTNAME, SERVER_PORT))

    try:
        # Start the server
        webServer.serve_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass

    webServer.server_close()
    print("Server stopped.")