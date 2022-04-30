# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import RPi.GPIO as GPIO

from classes.relay import Relay

hostName = "localhost"
serverPort = 6969

RELAY_LAMP_PIN = 4

json_data = {"status": "off"}

relayLamp = Relay(RELAY_LAMP_PIN)

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        #self.wfile.write(bytes("<html><body>"+ json.dumps(json_data) +"</body></html>", "utf-8"))
        if self.path == "/light/status":
            if relayLamp.status():
                json_data["status"] = "on"
            else:
                json_data["status"] = "off"
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        if self.path == "/light/on":
            json_data["status"] = "on"
            relayLamp.set(True)
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        if self.path == "/light/off":
            json_data["status"] = "off"
            relayLamp.set(False)
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass

    webServer.server_close()
    print("Server stopped.")