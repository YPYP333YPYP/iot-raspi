import paho.mqtt.client as mqtt
import time
import Adafruit_DHT as dht
import json
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

dht_type =22
dht_pin = 23

name = "SeungMyeong"
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27)
# Define Variables
MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "/dht/CCL"
# Define on_publish event function
def on_publish(client, userdata, mid):
    print ("Message Published...")
def on_connect ( client, userdata , flags, rc ):
    print("Connect with result code" + str (rc))
    client.subscribe("/cmd/CCL")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload.decode('utf-8')))
    x = str(msg.payload.decode('utf-8'))
    print(x)
    if name in x:
        if "on" in x:    
            lcd.clear()
            lcd.write_string('Temp High')
        if "off" in x:
            lcd.clear()
            lcd.write_string('Temp Noraml')

def on_pre_connect(client, data):
    return
# Initiate MQTT Client
client = mqtt.Client()
# Register publish callback function
client.on_pre_connect = on_pre_connect
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message
# Connect with MQTT Broker
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()


try:
    while True:
       
        humidity, temperature = dht.read_retry(22, 23)
        if humidity is not None and temperature is not None:
            data = {'temperature':round(temperature, 1), 'Serial' : f'{name}' }
            client.publish(MQTT_TOPIC, str(data))
            print('Published. Sleeping ...')
        else:
            print('Failed to get reading. Skipping ...')
            
except keyboardInterrupt:
    GPIO.cleanup()