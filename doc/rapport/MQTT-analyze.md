# MQTT

We hebben in dit project gekozen om de verbindingen tussen alle toestellen te doen met MQTT. Dit omdat het ons het gemakkelijkste leek om alles met 1 protocol te doen en over wifi wat sneller en betrouwbaarder is als bluetooth.

## Wat is MQTT?

MQTT is een Client Server publish/subcribe messaging transport protocol. Het is een licht, open, gemakkelijk en gemaakt om gemakkelijk te implementeren. Deze karaktereigenschappen maken het ideaal om ge gebruiken in heel veel situaties, inclusief omgeving met een beperkte mogelijkheid om te communiceren zoals bij Machine to Machine(M2M) en IOT.

De voordelen van MQTT zijn:
* gemakkelijk om te implementeren
* makkelijk schaalbaar
* neemt weinig bandbreedte van het netwerk

Het MQTT protocol is gebaseerd op het TCP/IP.

## Hoe werkt MQTT
### Het publish/subcribe patroon
De publish/subcribe patroon (pub/sub) geeft een alternatief voor de traditionele client-server architectuur.In de traditionele client-server architectuur, communiceert de client direct met het eindpunt. De publisher en subcriber staan nooit direct met elkaar in verbinding. De connectie wordt mogelijk gemaakt door de broker. De taak van de broker is de inkomende berichten filteren en deze afleveren aan de juiste subscribers. De connectie is altijd tussen één client en de broker.

#### Publish
Als een client verbonden is met een broker kan deze berichten publishen. Elke bericht moet een topic hebben dat de broker kan gebruiken om het bericht naar de geïnteresseerde clients te verzenden.

#### Subcribe
Een client moet verbonden worden met de broker anders heeft het geen zin om berichten te verzenden als niemand deze ontvangt. Om berichten te krijgen van een bepaalde topic moet de client een subcribe bericht sturen naar de broker.
Een client kan ook altijd unsubcribe van een topic als het geen berichten meer wil ontvangen in verband met een topic. Hiervoor moet de client een unsubcribe bericht schrijven naar de broker.

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
We moeten nu de hololens erbij betrekken. Deze moet ook de plaatsen krijgen waar er objecten liggen maar niet in x en y coördinaten maar in procenten dus wat we hiervoor moeten doen is het versturen in een andere topic. De hololens moet deze dan terug sturen naar de realsense, hiervoor hebben we nog een andere topic nodig. Als we nu op software die de realsense aanstuurt hebben nagegaan welk object we hebben geselecteerd moeten we dit dan nog verzenden naar de robotarm zodat deze dat voorwerp kan oppakken.

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
2. Hoe we verder te werk gaan is als volgend: de hololens krijgt per frame de middelpunten van elk object dat gedecteerd word. Als de hololens een object aanduid waar de robotarm naar toe moet gaat deze een bericht schrijven op de topic "hololens_send". Dit gaan we detecteren met de on_message functie van mqtt. Het bericht die de hololens stuurt is de actie + de plaats in de list van coordinaten van de objecten. We halen dit uit de lijst met coordinaten en sturen die dan door naar het object in json formaat.
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
6. Wat je ook merkt is dat we de coördinaten van voor de robot eerst gaan berekenen 