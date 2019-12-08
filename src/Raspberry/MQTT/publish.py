import paho.mqtt.publish as publish
import json

MQTT_SERVER = "localhost"
MQTT_PATH = "robotarm"

x = input("geef x waarde: ")
y = input("geef y waarde: ")
z = input("geef z waarde: ")

msg = {"x" : x, "y" : y, "z" : 50}
print(json.dumps(msg, sort_keys=True, indent=4))

publish.single(MQTT_PATH,payload=json.dumps(msg),hostname=MQTT_SERVER) 