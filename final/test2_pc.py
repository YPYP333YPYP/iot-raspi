# PC와 RP 사이에 mqtt로 통신하고 통신 내용에 따라 LED 및 카메라 조작
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
name = "SeungMyenog"
MQTT_Broker = "test.mosquitto.org" 
def on_connect ( client, userdata , flags, rc ):
    print("Connect with result code" + str (rc) )
    client.subscribe("/CCL/test1") 
def on_message ( client, userdata , msg ) :
    x = str(msg.payload.decode('utf-8')) 
    print(msg.topic + " " + x)
    if (x in "on" and x in "off"):
        y = eval(x) 
        if y["name"] == name:
            if y["control"] in "camera":
                publish.single("/CCL/test2", f'{name}-camera-on',hostname = 
                MQTT_Broker)
            elif y["control"] in "len":
                publish.single("/CCL/test2", f'{name}-led-on',hostname = 
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