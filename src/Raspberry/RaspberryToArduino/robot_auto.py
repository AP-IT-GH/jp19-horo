import RPi.GPIO as gpio
import smbus
from time import sleep
import sys
import paho.mqtt.client as mqtt
import json

MQTT_SERVER = "192.168.0.69"
MQTT_PATH = "robotarm"

global Flag
Flag = False
global json_object
def on_connect(client,userdata,flags,rc):
    print("connected with result code " +str(rc))
    client.subscribe(MQTT_PATH)

def on_message(client, userdata,msg):
    global json_object
    global Flag
    print(msg.topic+" " + str(msg.payload))
    json_object=json.loads(str(msg.payload))
    Flag = True
    print(json_object)
    print("dit is de x waarde " + str(json_object["x"]))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER,1883,60)





bus = smbus.SMBus(1)
address = 0x04
sleep(2)

def main():
    global json_object
    global Flag
    client.loop()
    print("Flag is " + str(Flag))
    while Flag:
        count = int(json_object["x"])
        print(count)
        if(count > 0):
            Sign = 1
            
        else:
            Sign = 0
            count = count*-1
            
        if(count > 255 and count < 510):
            count = count-255
            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,count)
            sleep(0.05)
            bus.write_byte(address,0)
            
        elif(count >= 510):
            count = count-255-255

            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,count)

        else:
            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,count)
            sleep(0.05)
            bus.write_byte(address,0)
            sleep(0.05)
            bus.write_byte(address,0)
            
        count = int(json_object["y"])
        print(count)
        if(count > 0):
            Sign = 1
            
        else:
            Sign = 0
            count = count*-1
            
        if(count > 255 and count < 510):
            count = count-255
            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,count)
            sleep(0.05)
            bus.write_byte(address,0)
            
        elif(count >= 510):
            count = count-255-255
            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,count)
        else:
            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,count)
            sleep(0.05)
            bus.write_byte(address,0)
            sleep(0.05)
            bus.write_byte(address,0)
            
        count = int(json_object["z"])
        print(count)
        if(count > 0):
            Sign = 1
            
        else:
            Sign = 0
            count = count*-1
            
        if(count > 255 and count < 510):
            count = count-255
            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,count)
            sleep(0.05)
            bus.write_byte(address,0)
            
        elif(count > 510):
            count = count-255-255
            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,255)
            sleep(0.05)
            bus.write_byte(address,count)
        else:
            bus.write_byte(address,Sign)
            sleep(0.05)
            bus.write_byte(address,count)
            sleep(0.05)
            bus.write_byte(address,0)
            sleep(0.05)
            bus.write_byte(address,0)
        sleep(0.01)
        count = 50#input("geef grijp hoek :")
        bus.write_byte(address,count)
        sleep(0.01)
        count = 50#input("geef knijp kracht (20-60) :")
        if(count > 60 or count < 20):
            count = 45
        bus.write_byte(address,count)
        Flag = False
        sleep(0.01)
        
        sleep(5)
    

while True:
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupt'
        gpio.cleanup()
        sys.exit(0)

