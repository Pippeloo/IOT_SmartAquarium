import requests
from random import randrange
import time

while True:
	url = "https://pippeloo.hub.ubeac.io/Station"
	data = {
				"id": "Raspberry-Pi",
				"sensors":[{
					'id': 'Lamp',
					'data': 100
				},
				{
					"id": "Water Depth",
					"data": 20
				},
				{
					"id": "Pump",
					"data": 100
				}]
			}
	response = requests.request("POST", url, json=data)
	print(response.text)
	time.sleep(1)
