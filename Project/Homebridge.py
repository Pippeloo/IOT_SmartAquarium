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
    def do_GET(self):
        global timerBusy, timerStart, timeUntillLightOff
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        #self.wfile.write(bytes("<html><body>"+ json.dumps(json_data) +"</body></html>", "utf-8"))
        if self.path == "/light/status":
            if relayLamp.status():
                json_data["status"] = "on"
            else:
                json_data["status"] = "off"
                timerBusy = False

            if timerBusy and (millis() - timerStart > timeUntillLightOff):
                timerBusy = False
                relayLamp.set(False)
                json_data["status"] = "off"

            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        if self.path == "/light/on":
            json_data["status"] = "on"
            relayLamp.set(True)
            if not timerBusy:
                timerBusy = True
                timerStart = millis()
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        if self.path == "/light/off":
            json_data["status"] = "off"
            relayLamp.set(False)
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))

    def log_message(self, format, *args):
        pass


# ===== MAIN =====    
if __name__ == "__main__":        
    webServer = HTTPServer((HOSTNAME, SERVER_PORT), MyServer)
    print("Server started http://%s:%s" % (HOSTNAME, SERVER_PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass

    webServer.server_close()
    print("Server stopped.")