**Intel realsense
Object detection** 

 1. Wat is een intel realsense?
 2. Hoe werkt object detectie?
 3. Waarom object detectie op deze manier?
 4. Voorbeeld toepassing

# Wat is een intel realsense?

De intel realsense is een RGB en een diepte camera in één. De camera zijn belangrijkste taak is het meten van de objecten in de ruimte. De camera kan namelijk op de x, y en z as meten. Als men de juiste verhoudingen ingeeft (schaal factor) (lengte horizontale as) kan men aan de hand van de lengte en breedte 1pixel = totaal pixels x-as/werkelijke lengte x-as de uiteindelijke werkelijke afstand bekomen. Door deze formule toe te passen kan men dus deze factor (lengte en breedte van 1 pixel) vermenigvuldigen met de x en y coördinaat(pixel van de camera) om de waarde in de realiteit te bekomen.

# Hoe werkt de object detectie?
Voor object detectie maak ik gebruik van de openCV library (je kan best ook de numphy library importeren). Deze library beschikt over veel mogelijkheden om foto's te bewerken en te interpreteren.

OpenCV is momenteel enkel toepasbaar in c++ en python. Ik heb persoonlijk voor python gekozen aangezien we dit ook bij raspberry pi gebruiken.

Het process van object detectie in een gecontroleerde environment (goede belichting (geen of zwakke schaduwen) en 1 bepaalde achtergrond kleur achter de objecten).

1.  Zet de camera stream op in python.

2.  Converteert de camera RGB naar GBR aangezien dat openCV met GBR kleuren interpreteert.
    
3.  Maak een mask zodanig dat de objecten wit zijn en de ondergrond zwart is. Deze kan men eventueel in een aparte window weergeven zodanig dat men de mask kan fine tunen.
Deze mask wordt bekomen door een bepaalde grenswaarde van het RGB spectrum in te stellen. Als men bijvoorbeeld een bepaalde kleur achtergrond heeft kan men deze weg krijgen door de bovenste en de onderste grenswateren in 2 RGB variabelen op te slaan en vervolgens te vergelijken met de RGB frame. In plaats van deze waardes aan de RGB stream te onttrekken maakt men met deze selectie van RGB een mask. Op deze mask zou men dan uiteindelijk de objecten in het wit moeten zien en de achtergrond in het zwart.
Als men de mask nog beter wilt maken kan men dit doen door voorafgaand een gaussiaanse vervaging toe te passen. Hierdoor gaan de randen van objecten soft worden (i.p.v. hard) en zal er dus een meer gelijkelijk gemiddelde worden gevormd. Als men alleen een zwarte / witte kleur wilt wegfilteren kan men eventueel ook de RGB nog eerst converteren naar een graag scale.

4.  Pas een contour detection toe op de mask. Hiermee zullen dus de randen van de objecten zichtbaar worden.
De contour detection gaat een lijn trekken op de rand tussen wit en zwart van de mask. Voor een goede visuele representatie kan men deze best op de RGB stream tekenen.

5.  Teken een box rond de contour.
Om de objecten in de ruimte te kunnen bepalen kan men best de contour omzetten in 4 punten. Aangezien men ander veel te veel data heeft. Deze punten worden bekomen door een rectangle rond elke contour te tekenen.

6.  Teken een gedraaide box zodanig dat hij nog de volledig contour omvat maar het kleinste totale oppervlakte bevat.
Om de positie van het object nauwkeuriger te kunnen bepalen kan men best de rectangle in de meeste gevallen een deeltje draaien. Als de rectangle namelijk zodanig draait dat hij de kleinste oppervlakte heeft maar toch nog de hele contour bevat zullen de 4 punten veel dichter bij de effectieve waarden liggen.

8.  Log de 4 punten/ het centrum van de gedraaide rectangle in de console.
    
9.  Extra: maak een filter zodanig enkel x aantal van de grootste objecten worden weergegeven. Dit zorgt ervoor dat wanneer er wat kleine ruis op het scherm is dit niet gedetecteerd wordt.
    
10.  Om ervoor te zorgen dat de robotarm niet gedetecteerd wordt als een object kan men hier nog een extra mask overtrekken. Dit doet men bijvoorbeeld door een rectangle in de gefilterde mask kleur voor dat de mask wordt gemaakt op de stream te plaatsen.
   
# Waarom object detectie op deze manier?

Ik ben begonnen met object detectie te doen met een deep learning algoritme. Bij het standaard project van de intel realsense wordt een klein deep aangeleerd netwerk meegeleverd (coffee table). Het goede aan een deep learn network is dat dit kan uitgevoerd worden in een ongecontroleerde omgeving. Het programma zal namelijk zoeken naar patronen als men de pixels van de photo afgaan. Het nadeel is echter dat men voor elk object dat men wilt detecteren, men dit eerst de computer moet aanleren door een hoop fotos te implementeren (bv mens => 50 foto’s van mensen). Een bijkomend nadeel is dat zo een algoritme enorm veel processing power (vooral grafisch) vereist aangezien hij eerst de afbeelding moet renderen en dan op elke object van zijn deep geleerd netwerk moet gaan testen (of er een overeenkomstig patroon is). Dit zorgt dus voor een niet real time toepassing.
Dit hebben we dus niet gebruikt in onze toepassing, we hebben besloten om contour detectie te gebruiken. Dit is een betere en snelleren manier om objecten te detecteren.

# Uitleg van de code

Voor we kunnen beginnen met programmeren moeten we eerst zorgen dat we de sdk hebben geinstalleerd van de realsense. (https://www.intelrealsense.com/developers/)

Voor we beginnen met onze code moeten we eerst alle libraries importen die we nodig hebben voor het project.
```python
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import pyrealsense2 as rs
    import math
```

1. We moeten beginnen een pipeline aan te maken die alle handelingen van de geconnecteerde realsense aparaten gaat bijhouden.
```python
    pipeline = rs.pipeline()
    pipeline.start()
    profile = pipeline.get_active_profile()
```
2. Als de pipeline gelukt is, kunnen we beginnen met het opvragen van de frames. Als we de frames hebben kunnen hieruit de diepte en color frames gehaald worden. Deze call wacht tot er een nieuwe samenhangende set van frames toegankelijk zijn op een apparaat. Als de diepte of color frames niet zijn aangekomen op tijd zal het programma nog steeds runnen door de continue in de if.

```python
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
            continue
```
3. We gaan gebruik maken van de numpy bibliotheek om de de data van de kleuren frame bij te houden, hiermee kunnen we laten dan bewerkingen mee gaan doen.

```python
    color = np.asanyarray(color_frame.get_data())
```

4. Uit de array die we in de vorige stap hebben aangemaakt kunnen we nu hoogte en de breedte halen. In deze stap gaan we ook de waardes instellen van de expected en de scale.

```python
    height, width = color.shape[:2]
    expected = 1000.0 #vermoedlijk is dit gelijk aan de breedte van de frame     
    aspect = width / height
    scale = int(math.ceil(height / expected))
```
5. Nu we de waardes hebben ingesteld die we nodig hebben kunnen we img maken die we willen weergeven in het venster met de grootte dat we willen hebben. Dit doen we met de resize functie die van de array die we gemaakt hebben in stap 3. We gaan de image die we gaan gebruiken voor contour herkenning opslagen in de crop_img variablen

```python
    resized_image = cv2.resize(color, (int(round(expected * aspect)),int( expected)))
    crop_start = round(expected * (aspect - 1) / 2)
    crop_img = resized_image[0:int(expected), int(crop_start):int(crop_start+expected)]
```

6. Voor de contour detectie beter te laten gaan maken we gebruik van een mask. Omdat onze plaat die we gebruiken als ondergrond wit is, gaan we enkel kijken naar de objecten die de kleur hebben van zwart naar bijna wit.

```python
    lower_red = np.array([0,0,0])           #houd de waarde tussen zwart
    upper_red = np.array([100,100,100])     #en bijna wit
    mask = cv2.inRange(crop_img, lower_red, upper_red)
```

7. De Robot staat in het midden van de area waarin gedetecteerd wordt en zal dus mee gedetecteerd worden. Dit is een probleem omdat we dit geen object is dat we willen detecteren. Wat wij gedaan hebben om de robot niet mee te detecteren is een mask over zetten zodat de camera denkt dat er niks staat.

```python
    robotWidth = 300 
    robotHeight = 350
    xRobot = 450 - (robotWidth/2)
    yRobot = 550 - (robotHeight/2)
    xRobotWidth = xRobot + robotWidth
    yRobotHeight = yRobot + robotHeight

    cv2.rectangle(mask,(xRobot,yRobot),(xRobotWidth,yRobotHeight),(0,0,0),-1)cv2.rectangle(crop_img,(xRobot,yRobot),(xRobotWidth,yRobotHeight),(255,255,0),-1)
```


8. Nu we dit allemaal hebben kunnen we de contouren gaan detecteren. Hier is een functie voor in de opencv bibliotheek, deze is findContours
Deze heeft drie parameters: de eerste is de mask die meegeven moet worden welke kleuren er moeten gevonden worden, de tweede parameter is voor de hierarchy( hiermee wordt er bedoeld welke contouren er worden gedecteerd enkel de uiterste met de hoogste hierarchy of allemaal dus ook contouren in contouren, het perfecte is RERT_TREE dit detecteerd alles en maakt een volledige hierarchy), de derde en laatste parameten is voor het opslagen van de punten ( je hebt twee keuzes none: hier worden alle punten opgeslagen, dit neemt veel plaats in beslag en Simple: hierbij worden enkel de hoekpunten opgeslagen en wordt er nadien tussen deze hoekpunten een lijn getrokken). Als we gaan kijken naar wat de functie teruggeeft, zien we dat het twee parameters teruggeeft. Contours hierin zit een array met de hoekpunten van de contours en hierarchy zit de hierarchy in dat je juist over gelezen hebt.

```python
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```
9. Als we de contouren hebben gedetecteerd gaan we deze nu tekenen op de image die we gaan weergeven op het einde zodat we een beeld hebben van wat de camera doet.

```python
    cv2.drawContours(crop_img, contours, -1, (0,255,0), 3)  
```
10. Het is op de hololens momenteel nog niet mogelijk om meer dan 4 objecten te verwerken. Op de Realsense gaan we dus een selectie maken van enkel de vier grootste objecten. Dit doen we met de functie sorted die in python zit en we kunnen in de cv2 de opervlakte van de area opvragen per object, hierop gaan we dus ook sorteren. Als we de gesorteerde aray hebben gaan we er de eerste vier uitpakken. Wat we hier als extra op gedaan hebben is enkel met de objecten verder gaan die groot genoeg zijn. Dit hebben we gedaan met een simpele for loop.
```python
    contours = sorted(contours, key = cv2.contourArea, reverse = True)

    u = 0
    teKort = False
    lengteArray = 0
    contourSorted = []
    for C in contours:
        if cv2.contourArea(C) > 1000:
            contourSorted.append(C)
            if len(contourSorted) == 4:
                break

        else:
            teKort = True
            lengteArray = len(contourSorted)
            break
        u=u+1 
```
11. We hebben nu de array met de objecten waar we de coördinaten moeten uithalen. We gaan dit object per object doen. Omdat we enkel maar de vier hoekpunten van elk object hebben moeten er eerst nog bewerkingen uitgevoerd worden. Wat er eerst gebeurt is dat er een circel rond de vier hoekpunten getrokken word zodat je het middelpunt kan krijgen dit doen we met de minEnclosingCircle functie in de cv2 library. Ook deze gaan we weergeven op de image die we op de computer te zien gaan krijgen. Om te weten hoe groot het object juist is, gaan we er eerst een rechthoek rond trekken die geen rekening houd met hoe het object georiënteerd is. Dit doen we door eerst de booglengte te weten te komen (arcLength) en deze lengtes met elkaar te verbinden en een rechthoek van te laten maken (approxPolyDP) hiervan kunnen we de x,y coördinaten en de breedte en lengte opvragen (boundingRect). Nu hebben we de x,y van de linkerboven hoek en de breedte en de hoogte. Dit is de blauwe rechthoek die je ziet. Nu gaan we deze rechthoeken draaien om dichterbij de contour van het echt object te zitten. We gaan eerst een rechthoek maken met minAreaRect, als we dit hebben gaan we met de functie boxPoints en np.int0 de rechthoek draaien om zo dichter bij de omtrek van de rechthoek te komen. Deze rechthoek geven we weer in het rood. 
```python
    #rects = []
    for c in contourSorted:
        (xc,yc),radius = cv2.minEnclosingCircle(c)
        center = (int(xc),int(yc))
        radius = int(radius)
        cv2.circle(crop_img,center,radius,(0,255,0),2)
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        #diepte = aligned_depth_frame.get_distance(int(xc),int(yc))
        # if height is enough
        # create rectangle for bounding
        rect = (x, y, w, h)
        #rects.append(rect)
        cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0,255), 4);   

        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(crop_img,[box],0,(255,0,0),4)
```
12. Nu we alles op de crop_img hebben gezet en de objecten hebben gedetecteerd is het tijd om ze weer te geven. Dit doen we met de volgende code.
```python
    cv2.namedWindow('RealSense5', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('RealSense5',640,480)
    cv2.imshow('RealSense5',cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
```
