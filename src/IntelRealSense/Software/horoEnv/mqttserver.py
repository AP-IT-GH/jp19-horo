import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import robotcocalc
import json

MQTT_SERVER = "192.168.0.69"
MQTT_PATH_HOLO = "hololens_send"
MQTT_PATH_ROBOT = "robotarm"
CL =""

def start():
    global CL
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(MQTT_PATH_HOLO)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        print(msg.payload)
        actie = msg.payload[:1]
        c = msg.payload[2:]
        print ("actie : "+actie)
        print ("c : "+c)
        
        test = CL.split(';')[int(c)]
        test += ",50"
        #print (test)
        Coordinaten = test.split(',')

        x = Coordinaten[0]
        y = Coordinaten[1]
        z = int(Coordinaten[2])

        x_R, y_R = robotcocalc.calcCoordinaten(x,y)
        print (x_R)
        RobotMsg = {"x" : x_R, "y" : y_R, "z" : z}
        print (json.dumps(RobotMsg))

        publish.single(MQTT_PATH_ROBOT,payload=json.dumps(RobotMsg),hostname=MQTT_SERVER)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()

def setCoordinatenList(clist):
    global CL
    CL = clist