# PC와 RP 사이에 mqtt로 통신하고 통신 내용에 따라 LED 및 카메라 조작


import paho.mqtt.client as mqtt
import time

import json
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

name = "SeungMyeong"

MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "/CCL/test1"

from picamera import PiCamera
camera = PiCamera()
camera.resolution = (2592, 1944)


def on_publish(client, userdata, mid):
    print ("Message Published...")
def on_connect ( client, userdata , flags, rc ):
    print("Connect with result code" + str (rc))
    client.subscribe("/CCL/test2")
def on_message(client, userdata, msg):
    x = str(msg.payload.decode('utf-8'))
    if x in name:
        if x in "led":
            if x == "on": 
                GPIO.output(16, True)
            elif x == "off":
                GPIO.output(16, False)
        if x in "camera":
            if x == "on": 
                camera.capture('example.jpg')
            elif x == "off":
                camera.close()
           
            
def on_pre_connect(client, data):
    return

client = mqtt.Client()

client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message
client.on_pre_connect = on_pre_connect

client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()
try:
    while True:
        user_input = input("user input wating....")
        data = {'name':name, 'control' : user_input}
        client.publish(MQTT_TOPIC, str(data))
        
except keyboardInterrup:
    GPIO.cleanup()