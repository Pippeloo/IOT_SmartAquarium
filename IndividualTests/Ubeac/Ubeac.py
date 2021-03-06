# =============
# Jules Torfs
# r0878800
# =============

# import the necessary packages
import requests
import time

# ====== CLASSES ======
class UbeacSensor:
    json = {'id': '', 'sensors': []}

    def __init__(self, url, deviceId):
        self.url = url
        self.deviceId = deviceId
        self.json['id'] = deviceId

    def set(self, sensor, value):
        for i in range(0, len(self.json['sensors'])):
            if sensor == self.json['sensors'][i]['id']:
                self.json['sensors'][i]['data'] = value
                return

        self.json['sensors'].append({'id': sensor, 'data': value})
    
    def send(self):
        requests.request("POST", self.url, json=self.json)


# ====== MAIN ======
ubeacSensor = UbeacSensor("https://pippeloo.hub.ubeac.io/Station", "Raspberry-Pi")

try:
    ubeacSensor.set("Lamp", 100)
    ubeacSensor.set("Water Depth", 20)
    ubeacSensor.set("Pump", 100)
    ubeacSensor.send()
    time.sleep(2)
    ubeacSensor.set("Lamp", 0)
    ubeacSensor.set("Water Depth", 0)
    ubeacSensor.set("Pump", 0)
    ubeacSensor.send()
    time.sleep(2)

except KeyboardInterrupt:
    pass


