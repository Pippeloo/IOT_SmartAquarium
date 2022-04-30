# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = "localhost"
serverPort = 6969

json_data = {"status": "off"}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        #self.wfile.write(bytes("<html><body>"+ json.dumps(json_data) +"</body></html>", "utf-8"))
        if self.path == "/light/status":
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        if self.path == "/light/on":
            json_data["status"] = "on"
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        if self.path == "/light/off":
            json_data["status"] = "off"
            self.wfile.write(bytes(json.dumps(json_data), "utf-8"))

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")