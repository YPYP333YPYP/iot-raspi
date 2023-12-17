import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
normal_temp = 25.0 #원하는 온도 설정
MQTT_Broker = "test.mosquitto.org" #자신의 RP(broker) ip
name = "Lee"

def on_connect ( client, userdata , flags, rc ):
    print("Connect with result code" + str (rc) )
    client.subscribe("dht/CCL") #Topic
def on_message ( client, userdata , msg ) :
    x = str(msg.payload.decode('utf-8')) #dht 센서 데이터
    print(msg.topic + " " + x)
    if (x not in "on" and x not in "off" and x not in "serial"):
        y = eval(x) #dht 센서 데이터를 Dic타입으로 변환 파싱
        if y["Serial"] == name:
            if y["temperature"] > normal_temp:
                publish.single("cmd/CCL", f'{name}-on',hostname =MQTT_Broker)
            elif y["temperature"] <= normal_temp:
                publish.single("cmd/CCL", f'{name}-off',hostname =MQTT_Broker)
def on_publish(client, userdata, mid):
    print("message publish..")
def on_disconnect(client, userdata, rc):
    print("Disconnected")

def on_pre_connect(cleint,data):
    return

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_Broker, 1883, 60)
client.on_message = on_message
client.on_publish = on_publish
client.on_pre_connect = on_pre_connect
client.on_disconnect = on_disconnect
client.loop_forever()