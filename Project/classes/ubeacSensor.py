# =============
# Jules Torfs
# r0878800
# =============

# import the necessary packages
import requests

# ====== CLASSES ======
class UbeacSensor:
    # create a the json
    json = {'id': '', 'sensors': []}

    def __init__(self, url, deviceId):
        self.url = url
        self.deviceId = deviceId
        self.json['id'] = deviceId

    # add 
    def set(self, sensor, value):
        # check if the sensor is already in the json
        for i in range(0, len(self.json['sensors'])):
            if sensor == self.json['sensors'][i]['id']:
                # set the value to the sensor
                self.json['sensors'][i]['data'] = value
                return
        # add the sensor to the json
        self.json['sensors'].append({'id': sensor, 'data': value})
    
    # send the data to the server
    def send(self):
        requests.request("POST", self.url, json=self.json)