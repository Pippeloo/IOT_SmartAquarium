# =============
# Jules Torfs
# r0878800
# =============

# import the necessary packages
import requests

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