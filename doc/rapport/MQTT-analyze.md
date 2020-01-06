# MQTT

We hebben in dit project gekozen om de verbindingen tussen alle toestellen te doen met MQTT. Om de simpele reden dat het makkelijker is om alles met 1 protocol te doen. Nog een voordeel van MQTT is dat dit over wifi gaat, wat sneller en betrouwbaarder is dan bluetooth.

## Wat is MQTT?

MQTT is een Client Server publish/subcribe messaging transport protocol. Het is een licht, open en gemakkelijk protocol dat ook nog eens eenvoudig te implementeren is. Deze karaktereigenschappen maken het ideaal om ge gebruiken in heel veel situaties, inclusief in een omgeving met een beperkte mogelijkheid om te communiceren zoals bij Machine to Machine(M2M) en IOT.

De voordelen van MQTT zijn:
* gemakkelijk om te implementeren
* makkelijk schaalbaar
* neemt weinig bandbreedte van het netwerk

Het MQTT protocol is gebaseerd op het TCP/IP.

## Hoe werkt MQTT
### Het publish/subcribe patroon
Het publish/subcribe patroon (pub/sub) geeft een alternatief voor de traditionele client-server architectuur.In de traditionele client-server architectuur, communiceert de client direct met het eindpunt. De publisher en subcriber staan nooit direct met elkaar in verbinding. Bij MQTT wordt de connectie echter mogelijk gemaakt door gebruik te maken van een middelman, de broker. De taak van de broker is de inkomende berichten filteren en deze afleveren aan de juiste subscribers. De connectie met MQTT is er dus altijd één tussen een client en een broker.

#### Publish
Als een client verbonden is met een broker kan deze berichten publishen. Elke bericht moet een topic hebben dat de broker kan gebruiken om het bericht naar de geïnteresseerde clients te verzenden.

#### Subcribe
Een client moet verbonden worden met de broker. Indien dit niet het geval is heeft het geen zin om berichten te verzenden aangezien dat niemand deze zal ontvangen. Om berichten te krijgen van een bepaald topic moet de client een subcribe bericht sturen naar de broker.
Een client kan ook altijd een unsubcribe van een topic indien het geen berichten meer wil ontvangen in verband met een topic. Hiervoor moet de client een unsubcribe bericht schrijven naar de broker.

#### Topics
De broker gebruikt topics voor het filteren van berichten(topics) voor iedere connectie. De topics kunnen bestaan van één of meerdere topics levels. Elk level is gescheiden door een forward slash (dit worde de topic level separator genoemd).

> myhome/groundfloor/livingroom/temprature
> - Dit is een voorbeeld van ene topic met meerdere levels

De client moet de topics niet creëren voor dat ze er iets op kunnen publishen of aan kunnen subcriben. De broker accepteert elke geldige topic.
Merk op dat elke topic minstens één karakter moet hebben en ze geen spaties mogen bevatten. Ze zijn ook hoofdletter gevoelig.

## Waarom MQTT
We hebben voor mqtt gekozen omdat dit een makkelijke manier is om alle apparaten met elkaar te verbinden. We kunnen hierdoor ze allemaal berichten tegelijk sturen of apart door met verschillende topics te werken.

###structuur van de MQTT
#### basis project (zonder input van de hololens)
Hierbij is er enkel een verbinding nodig tussen de realsense camera en de robotarm. Wat we willen verwezelijken is dat van de objecten die de realsense detecteert we de coördinaten doorsturen naar de robotarm zodat deze zich naar de objecten beweegt.
Dit hebben we gedaan door de x,y en z coördinaten in een json bestand weg te schrijven en deze te versturen naar de robotarm waar ze daar de coördinaten uit de json kunnen halen.

Voor de topic van de robotarm gaan we "robotarm" gebruiken hier wordt json naar gestuurd


#### Eindproject
We moeten nu de Hololens erbij betrekken. Deze moet ook de plaatsen krijgen waar objecten liggen. Echter moeten deze locaties niet in x en y coördinaten, maar in procenten worden verstuurd. Dit doen we door deze informatie te versturen in een ander topic. De hololens moet deze dan terug sturen naar de realsense, hiervoor hebben we nog een ander topic nodig. Als we nu op software die de realsense aanstuurt hebben nagegaan welk object we hebben geselecteerd moeten we dit dan nog verzenden naar de robotarm zodat deze dat voorwerp kan oppakken.

De topic van de robotarm blijft hetzelfde.
Voor het versturen van de realsense naar de hololens gaan we de topic "ToHololens" gebruiken.
Het versturen van de hololens naar de realsense gaan we de topic "FromHololens gebruiken.

## Code
Het script dat het meeste regelt van de mqtt verbindingen staat op de computer waar de realsense is aan verbonden. 
We hebben een paar vaste variablen die je vaak gaat terug zien komen ivm de topics en de server:
```Python
    MQTT_SERVER = "192.168.0.69"
    MQTT_ROBOT = "robotarm"
    MQTT_HOLO = "hololens"
    MQTT_HOLO_RECIEVE = "hololens_send"
```

1. Wat we hierin gaan doen is eerst en vooral een verbinding opzetten met de mqtt server. Dit doen we met de volgende code.
```Python
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER, 1883, 60)
    client.loop_forever()
```
2. Hoe we verder te werk gaan is als volgend: de hololens krijgt per frame de middelpunten van elk object dat gedecteerd word. Als de hololens een object aanduid waar de robotarm naar toe moet gaat deze een bericht schrijven op de topic "hololens_send". Dit gaan we detecteren met de on_message functie van mqtt. Het bericht die de hololens stuurt is de actie + de plaats in de list van coordinaten van de objecten. We halen dit uit de lijst met coordinaten en sturen die dan door naar de robotarm in json formaat.
```Python
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        print(msg.payload)
        actie = msg.payload[:1]
        c = msg.payload[2:]
        print ("actie : "+actie)
        print ("c : "+c)
        
        test = CL.split(';')[int(c)]
        test += ",50"
        Coordinaten = test.split(',')

        x = Coordinaten[0]
        y = Coordinaten[1]
        z = int(Coordinaten[2])

        x_R, y_R = robotcocalc.calcCoordinaten(x,y)
        print (x_R)
        RobotMsg = {"x" : x_R, "y" : y_R, "z" : z}
        print (json.dumps(RobotMsg))

        publish.single(MQTT_PATH_ROBOT,payload=json.dumps(RobotMsg),hostname=MQTT_SERVER)
```
3. In dit script staat er ook een functie die de coördinaten list altijd set. Dit wordt aangeroepen in het Realsense script. 
```Python
    def setCoordinatenList(clist):
        global CL
        CL = clist
```
4. In het script van de Realsense gaan we twee strings maken met coördinaten van de objecten hun middelpunten. Dit voor de hololens en voor de robotarm. De string voor de robotarm moeten we doorgeven aan het script van de mqtt verbinding. Hierin staan momenteel enkel nog maar de middelpunten van de gedetecteerde objecten. Dit doen we in de for lus waarin we de rechthoeken gaan maken rond de objecten.
```Python
    xcI = int(xc)
    ycI = int(yc)
    stringRobot += str(xcI) +","+str(ycI)+";"

    kommaX = ((x + (w/2))*expected)/1000000000*expected
    kommaY = ((y + (h/2))*expected)/1000000000*expected

    puntenDepth.append([xc,yc])

    stringCoordinaten += str(kommaX)+","+str(kommaY)+";"
```
5. Als we beide strings hebben gaan we deze doorsturen naar hololens en naar het mqtt script.
```Python
    mqttserver.setCoordinatenList(stringRobot)
    publish.single(MQTT_HOLO,payload = stringCoordinaten,hostname = MQTT_SERVER)
```
6. Wat je ook merkt is dat we de coördinaten van voor de robot eerst gaan berekenen vanuit een ander scriptje. Dit was nodig om de assenstelsels van de robot gelijk te laten lopen met dat van de camera. De robotarm is ook niet zo nauwkeurig dit hebben we proberen op te lossen met het assenstelsel in zoveel mogelijk kleine deeltjes onder te verdelen. Zo ziet het script voor het berekenen van de coördinaten van het assenstelsel eruit:
```Python
def calcCoordinaten(xc,yc):
    print ("kom ik hier")
    print xc,yc
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
        return x_robot, y_robot
        
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
        return x_robot, y_robot
        
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
        return x_robot, y_robot
        
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

        return x_robot, y_robot
```