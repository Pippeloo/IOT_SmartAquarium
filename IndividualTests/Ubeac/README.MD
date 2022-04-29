# Ubeac
## Student
Name | Student Number | Class
-----|----------------|------
Jules Torfs | r0878800 | 1ITF05

## Ubeac Class
Init the class by doing `ubeacSensor = UbeacSensor(url, device_id)`
Function | Parameters | Description
---------|------------|-------------
set | (id, data) | Creates/Updates a sensor.
send | () | Send the data to the server

**WARNING**: The send() function delays the script because it has to wait for the return response