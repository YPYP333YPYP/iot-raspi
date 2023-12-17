# settings
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# pin 
button_pin = 12 # 32
pir_pin = 24 # 18
buzzer_pin = 25 # 22
dht_type = 22 
dht_pin = 23 # 16
red_led_pin = 16 # 36
blue_led_pin = 20 # 38
green_led_pin = 21 # 40

# led pwm
pwm_led = GPIO.PWM(16, 500)
pwm_led.start(0)
try:
    while True:
        for i in range(0,101,5):
            pwm_led.ChangeDutyCycle(i) 
            time.sleep(0.02)
        for i in range(100,-1,-5): 
            pwm_led.ChangeDutyCycle(i) 
            time.sleep(0.02)
except KeyboardInterrupt:
    pass
finally:
    pwm_led.stop()
    GPIO.cleanup()


# button
def button_callback(chaneel):
    pass

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback)


# pir
def pir_callback(chaneel):
    pass

GPIO.setup(pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(pir_pin, GPIO.FALLING, callback=pir_callback)


# buzzer
GPIO.setup(buzzer_pin, GPIO.OUT)
def buzz(): 
    pitch = 1000 
    duration = 0.1 
    period = 1.0 / pitch 
    delay = period / 2 
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(buzzer_pin,True)
        time.sleep(delay)
        GPIO.output(buzzer_pin,False)
        time.sleep(delay)

# buzzer pwm
pwm=GPIO.PWM(buzzer_pin, 261) 
pwm.start(90.0) 
time.sleep(3.0) 
pwm.stop()


# lcd
# SDA 3, SCL 5
from RPLCD.i2c import CharLCD
lcd = CharLCD('PCF8574', 0x27) 
lcd.write_string() 
lcd.crlf() 
lcd.clear()
lcd.cursor_pos = (0,0)


# dht
import Adafruit_DHT
humidity, temperature = Adafruit_DHT.read_retry(dht_type, dht_pin) 
if humidity is not None and temperature is not None: 
    humid = str(round(humidity,1)) 
    temp = str(round(temperature,1)) 


# camera
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.capture('example.jpg') 
camera.close()


# mqtt - rp
import paho.mqtt.client as mqtt
import time

import json
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_TOPIC = "dht/CCL"

def on_publish(client, userdata, mid):
    print ("Message Published...")
def on_connect ( client, userdata , flags, rc ):
    print("Connect with result code" + str (rc))
    client.subscribe("dht/CCL")
def on_message(client, userdata, msg):
    x = str(msg.payload.decode('utf-8'))
    if x == "on": 
        GPIO.output(16, True)
    elif x == "off":
        GPIO.output(16, False)
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
        data = {'key1':'value1', 'key2' : 'value2'}
        client.publish(MQTT_TOPIC, str(data))
        print('Published. Sleeping ...')
        
except keyboardInterrup:
    GPIO.cleanup()


# mqtt - pc
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
normal_temp = 25.0 
MQTT_Broker = "test.mosquitto.org" 
def on_connect ( client, userdata , flags, rc ):
    print("Connect with result code" + str (rc) )
    client.subscribe("dht/CCL") 
def on_message ( client, userdata , msg ) :
    x = str(msg.payload.decode('utf-8')) 
    print(msg.topic + " " + x)
    if (x!= "on" and x != "off"):
        y = eval(x) 
        if y["temperature"] > normal_temp:
            publish.single("dht/CCL", "on",hostname = 
            MQTT_Broker)
        elif y["temperature"] <= normal_temp:
            publish.single("dht/CCL", "off",hostname = 
            MQTT_Broker)

def on_publish(client, userdata, mid):
    print("message publish..")
def on_disconnect(client, userdata, rc):
    print("Disconnected")
def on_pre_connect(client, data):
    return

client = mqtt.Client ()
client.on_connect = on_connect
client.connect(MQTT_Broker, 1883, 60)
client.on_message = on_message
client.on_publish = on_publish
client.on_pre_connect = on_pre_connect 
client.on_disconnect = on_disconnect
client.loop_forever()


"""
1. rp(pub) data를 publish (while True) ex. DHT
2. pc(sub) data를 subcsribe 
    2-1. on_connet 함수에서 subscribe 함수로 sub
    2-2. on_message 함수에서 pub msg를 받아서 처리
3. pc(pub) data를 publish.single (in on_message) 
    3-1. eval 함수를 사용하기 때문에 if문으로 적절한 유효성 검증 필요
4. rp(sub) data를 subscribe -> 센서 조작 ex. led, lcd
"""


# stt
import speech_recognition as sr
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""/home/pi/git/iot-programming-with-raspi/iot-p-405100-4d785ea5814e.json"""
r = sr.Recognizer()
mic = sr.Microphone()
try:
    while True:
        with mic as source:
            print("Say something!")
            audio = r.listen(source)
        gcSTT = r.recognize_google_cloud(audio, language = 'ko',credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))
except KeyboardInterrupt:
    GPIO.cleanup()

