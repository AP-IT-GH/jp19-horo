
# First import the library

import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
import math

import paho.mqtt.publish as publish
import json
import time

import thread


# install cv2 and numpy : pip install opencv-pyhton
# install matplotlib : python -m pip install -U matplotlib

#timer functie voor in een thread te laten lopen voor elke vijf seconden cordinaten door te sturen
timerBool = False

def timer():
    global timerBool
    while True:
        if timerBool == False : 
            print "Start : %s" % time.ctime()
            time.sleep( 10)
            timerBool = True
            print "End : %s" % time.ctime()

#White balance
####################################################################################################

#video stream
####################################################################################################
try:
    thread.start_new_thread(timer,())
    MQTT_SERVER = "192.168.0.69"
    MQTT_ROBOT = "robotarm"
    MQTT_HOLO = "hololens"
    MQQT_HOLO_RECIEVE = "hololens_send"

    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()
    pipeline.start()
    profile = pipeline.get_active_profile()

    ##depth_sensor = profile.get_device().first_depth_sensor()
    ##depth_scale = depth_sensor.get_depth_scale()
    ##print ("scale is : ",depth_scale)

    while True:

        global timerBool
        
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        

        color = np.asanyarray(color_frame.get_data())

        ##no clue wat dit doet?? Michiel
        ##plt.rcParams["axes.grid"] = False
        ##plt.rcParams['figure.figsize'] = [12, 6]
        ##plt.rcParams['figure.figsize'] = [9, 6]     #figure(figsize=(1,1)) would create an inch-by-inch image, which would be 80-by-80 pixels unless you also give a different dpi argument.

        #dit is enkel nodig voor de diepte.
        colorizer = rs.colorizer()

        # Create alignment primitive with color as its target stream:
        align = rs.align(rs.stream.color)
        frameset = align.process(frames)

        aligned_depth_frame = frameset.get_depth_frame().as_depth_frame()
        try_depth = aligned_depth_frame.get_distance(0,0)

        #scale to frame of the color view
        #colorized_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data()) 
        
        #print (try_depth)
        #depth = colorized_depth[0,0].astype(float)
        #print (depth)
        #distance = depth * depth_scale

        # print ("distance is:" , distance)
        
        # Standard OpenCV boilerplate for running the net:
        
        height, width = color.shape[:2]
        expected = 1000.0 #vermoedlijk is dit gelijk aan de breedte van de frame     
        aspect = width / height
        scale = int(math.ceil(height / expected))
       
        resized_image = cv2.resize(color, (int(round(expected * aspect)),int( expected)))
        crop_start = round(expected * (aspect - 1) / 2)
        crop_img = resized_image[0:int(expected), int(crop_start):int(crop_start+expected)]

        ##blurred_frame = cv2.GaussianBlur(crop_img, (5, 5), 0) #removes noise

        lower_red = np.array([0,0,0])           #houd de waarde tussen zwart
        upper_red = np.array([100,100,100])     #en bijna wit
        mask = cv2.inRange(crop_img, lower_red, upper_red)

        ##res = cv2.bitwise_and(crop_img,crop_img, mask= mask)
        
        #CREATE DEAD ZONE (MASK) -> robot arm word hierdoor niet gedetecteerd
        #robotWidth = 250 
        #robotHeight = 600 
        #xRobot = 500 - (robotWidth/2)
        #yRobot = 650 - (robotHeight/2)
        #xRobotWidth = xRobot + robotWidth
        #yRobotHeight = yRobot + robotHeight

        #cv2.rectangle(mask,(xRobot,yRobot),(xRobotWidth,yRobotHeight),(0,0,0),-1)              
        #cv2.rectangle(crop_img,(xRobot,yRobot),(xRobotWidth,yRobotHeight),(255,255,0),-1)
        #https://docs.opencv.org/3.3.1/d4/d73/tutorial_py_contours_begin.html
        #https://www.youtube.com/watch?v=_aTC-Rc4Io0


        ##imgray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        ##ret, thresh = cv2.threshold(imgray, 127, 255, 0)

        #thresh gebruikt een waarde uit de grayscale en mask gebruikt een kleur grens uit de rgb scale
        #probeer hier eens RETR_EXTERNAL dit gaat enkel de uiterste contours weergeven.
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  

        cv2.drawContours(crop_img, contours, -1, (0,255,0), 3)              
        #cv2.drawContours(crop_img, contours, contourCnt, (0,255,0), 3)     #all contours

        contours = sorted(contours, key = cv2.contourArea, reverse = True) # get the largest contour 
        u = 0
        teKort = False
        lengteArray = 0
        contourSorted = []
        # print (contourSorted)
        global stringCoordinaten
        stringCoordinaten = ""
        for C in contours:
           # print str(u)+":"+str(cv2.contourArea(C))
            if cv2.contourArea(C) > 1000:
                contourSorted.append(C)
                if len(contourSorted) == 4:
                    break

            else:
                teKort = True
                lengteArray = len(contourSorted)
                break
            u=u+1
        
                
       
        
        rects = []
        for c in contourSorted:
            (xc,yc),radius = cv2.minEnclosingCircle(c)
            center = (int(xc),int(yc))
            radius = int(radius)
            cv2.circle(crop_img,center,radius,(0,255,0),2)
            #print "center: " + str(center)
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            print type(xc)
            #diepte = aligned_depth_frame.get_distance(int(xc),int(yc))
            # if height is enough
            # create rectangle for bounding
            rect = (x, y, w, h)
            rects.append(rect)
            cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0,255), 4);   

            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(crop_img,[box],0,(255,0,0),4)
            
            x_waarde = (x + (w/2))
            y_waarde = (y + (h/2))

            #print("----------------------------------")
            #print("x center" + str(x_waarde))
            #print("y center" + str(y_waarde))

            #print("----------------------------------")
            #print("blauwe coordinaten")
            #print(box * expected)

            #alle coordinaten sturen naar de hololens

            kommaX = ((x + (w/2))*expected)/1000000000*expected
            kommaY = ((y + (h/2))*expected)/1000000000*expected

            
            stringCoordinaten += str(kommaX)+","+str(kommaY)+";"
                
        if timerBool: 
            x_tussenwaarde = int(x_waarde/expected)

            #Q1
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

        #versturen naar de robot
            #msg = {"x" : x_robot, "y" : y_robot, "z" : 50}
            #print(json.dumps(msg, sort_keys=True, indent=4))
            #publish.single(MQTT_ROBOT,payload=json.dumps(msg),hostname=MQTT_SERVER)
            timerBool = False

            #print("----------------------------------")
            #print("x center" + str(((x + (w/2))*expected)/1000) + "mm " + str(((x + (w/2))*expected)/10000000*expected) + "%")
            #print("y center" + str(((y + (h/2))*expected)/1000) + "mm " + str(((y + (h/2))*expected)/10000000*expected) + "%")
            #print("----------------------------------")
            
            
            
        
        print (stringCoordinaten)
        publish.single(MQTT_HOLO,payload = stringCoordinaten,hostname = MQTT_SERVER)
        cv2.namedWindow('RealSense5', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('RealSense5',640,480)
        cv2.imshow('RealSense5',cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))

         #OVERLAY DEPTH MAP ON CAMERA
        cv2.namedWindow('RealSense3', cv2.WINDOW_AUTOSIZE)
        Transparancy = 0.5
        width = 640
        height = 480
        dim = (width, height)

        # resize image
        resizedRGB = cv2.resize(crop_img, dim, interpolation = cv2.INTER_AREA)
        resizedDepth = cv2.resize(colorized_depth, dim, interpolation = cv2.INTER_AREA)

        beta = 1 - Transparancy
        dst = cv2.addWeighted(resizedDepth,Transparancy,resizedRGB,beta,0)
        cv2.resizeWindow('RealSense3',640,480)
        cv2.imshow('RealSense3',dst)

        #cv2.namedWindow('thresh grey', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('thresh grey',640,480)
        #cv2.imshow('thresh grey',thresh)

        #cv2.namedWindow('mask rgb', cv2.WINDOW_NORMAL)
        #cv2.resizeWindow('mask rgb',640,480)
        #cv2.imshow('mask rgb',mask)

        cv2.waitKey(1)
    exit(0)
           

except Exception as e:
    print(e)
    pass