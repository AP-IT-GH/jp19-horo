
import paho.mqtt.client as mqtt
import json

MQTT_SERVER = "192.168.0.69"
MQTT_PATH = "hololens"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    #more callbacks, etc
    #print the json in json format
    # print(json.dumps(msg.payload, sort_keys=True, indent=4))
    json_object=json.loads(str(msg.payload))
    print(json_object)
    print("dit is de x waarde " + str(json_object["x"]))
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, 1883, 60)


client.loop_forever()
