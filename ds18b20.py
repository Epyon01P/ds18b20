# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:52:55 2020
A minimalistic implementation of ds18b20 sensor interrogation and MQTT push
At least one ds18b20 1-Wire sensor is required.
Don't forget to activate the required 1-Wire kernel module!
As the sensor ID is unknown before runtime, this programme just reads in all
ds18b20 sensors it finds.
@author: Epyon
"""

from w1thermsensor import W1ThermSensor
import json
import time
import paho.mqtt.client as mqtt

brokers_out={"broker1":"localhost"}

#Scan for connected sensors, request their current value and publish it on the MQTT bus
for sensor in W1ThermSensor.get_available_sensors():
    attempts = 0
    while attempts < 10:
        try:
            var = sensor.get_temperature()
            resp = {'id': sensor.id, 'value': var, 'unit': '°C', 'timestamp' : int(time.time())}
            resp= json.dumps(resp, ensure_ascii=False)
            print(resp)
            topic="ds18b20/" + sensor.id
            client=mqtt.Client("ds18b20")
            client.connect(brokers_out["broker1"])
            client.publish(topic,resp)
            client.disconnect()
            break
        except:
            attempts += 1
            if attempts == 10: print("Read error for sensor " + sensor.id + ", skipping")
            time.sleep(0.05)
