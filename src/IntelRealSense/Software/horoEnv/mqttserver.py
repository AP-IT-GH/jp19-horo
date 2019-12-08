import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
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
        print (test)
        Coordinaten = test.split(',')

        x = Coordinaten[0]
        y = Coordinaten[1]
        z = Coordinaten[2]

        print x
        #publish.single(MQTT_ROBOT,payload=json.dumps(msg),hostname=MQTT_SERVER)


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()

def setCoordinatenList(clist):
    global CL
    CL = clist


def calcRobot(xc,yc):
    if int(xc) <500 and int(yc)< 500:
        print "Q1"
        #x waardes
        if int(yc) < 200:
            if int (xc) < 100:
                x_robot = (int(xc) - 670)
            elif int(xc) >= 100 and int(xc) <200:
                x_robot = (int(xc)-500)
            elif int(xc) >= 200 and int(xc) < 300:
                x_robot = (int(xc)-500)
            elif int(xc) >= 300 and int(xc) < 400:
                x_robot = (int(xc) - 450)
            else:
                x_robot = (int(xc) - 450)
            y_robot = (int(yc) - 500)
        else:
            if int (xc) < 100:
                x_robot = (int(xc) - 670)
            elif int(xc) >= 100 and int(xc) <200:
                x_robot = (int(xc)-600)
            elif int(xc) >= 200 and int(xc) < 300:
                x_robot = (int(xc)-550)
            elif int(xc) >= 300 and int(xc) < 400:
                x_robot = (int(xc) - 450)
            else:
                x_robot = (int(xc) - 450)
            y_robot = (int(yc) - 550)
        #y waardes
        
    #Q2
    elif int(xc) >= 500 and int(yc) < 500:
        print "Q2"
        #x waardes
        if int(xc) < 600:
            x_robot =(int(xc)-450)
            y_robot = (int(yc)-550)
        elif int (xc) >=600 and int(xc) < 700 :
            x_robot = (int(xc) - 400)
            y_robot = (int(yc)-550)
        elif int(xc) >=700 and int(xc) < 800:
            x_robot = (int(xc)-350)
            y_robot = (int(yc)-550)
        else:
            x_robot = (int(xc)-300)
            y_robot = (int(yc)-450)
        
    #Q3
    elif int(xc) >= 500 and int(yc) >= 500:
        print "Q3"
        #x waardes
        if int (xc) >=600 and int(xc) < 700 :
            x_robot = (int(xc) - 450)
            y_robot = (int(yc)-400)
        elif int(xc) >=700 and int(xc) < 750:
            x_robot = (int(xc)-400)
            y_robot = (int(yc)-350)
        elif int(xc) >=750 and int(xc) < 800:
            x_robot = (int(xc)-350)
            y_robot = (int(yc)-350)
        else:
            x_robot = (int(xc)-300)
            y_robot = (int(yc)-400)
        
    #Q4
    else:
        print " Q4"
        if int (xc) < 100:
            x_robot = (int(xc) - 670)
        elif int(xc) >= 100 and int(xc) <200:
            x_robot = (int(xc)-670)
        elif int(xc) >= 200 and int(xc) < 300:
            x_robot = (int(xc)-650)
        elif int(xc) >= 300 and int(xc) < 400:
            x_robot = (int(xc) - 550)
        else:
            x_robot = (int(xc) - 500)
        y_robot = (int(yc)-500)