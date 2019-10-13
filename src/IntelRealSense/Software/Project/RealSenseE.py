
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
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

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

#UI
################################################################################################
class Window(Frame):
    def __init__(self, master=None):

        Frame.__init__(self, master)        
        self.master = master

        # widget can take all window
        self.pack(fill=BOTH, expand=1)

        # create button, link it to clickExitButton()
        exitButton = Button(self, text="Exit", command=self.clickExitButton)
        rgbButton = Button(self, text="RGB CAM", command=self.clickRgbButton)
        depthButton = Button(self, text="depth CAM", command=self.clickDepthButton)
        overlayButton = Button(self, text="overlay CAM", command=self.clickOverlayButton)
        colorFilterButton = Button(self, text="colorFilter CAM", command=self.clickColorFilterButton)
        contourButton = Button(self, text="contourDetection CAM", command=self.clickContourButton)
        boxContourButton = Button(self, text="boxContourDetection CAM", command=self.clickBoxContourButton)

        # place button at (0,0)
        rgbButton.grid(row=1, column=0)
        depthButton.grid(row=2, column=0)
        overlayButton.grid(row=3, column=0)
        colorFilterButton.grid(row=4,column=0)
        contourButton.grid(row=5, column=0)
        boxContourButton.grid(row=6, column=0)
        exitButton.grid(row=10, column=0)

    def clickExitButton(self):
        exit()
    
    def clickRgbButton(self):
        global windowSelector
        windowSelector = 1
        root.destroy()
        print(windowSelector)

    def clickDepthButton(self):
        global windowSelector
        windowSelector = 2
        root.destroy()
        print(windowSelector)

    def clickOverlayButton(self):
        global windowSelector
        windowSelector = 3
        root.destroy()
        print(windowSelector)

    def clickColorFilterButton(self):
        global windowSelector
        windowSelector = 4
        root.destroy()
        print(windowSelector)

    def clickContourButton(self):
        global windowSelector
        windowSelector = 5
        root.destroy()
        print(windowSelector)
    
    def clickBoxContourButton(self):
        global windowSelector
        windowSelector = 6
        root.destroy()
        print(windowSelector)

windowSelector = 1    
root = Tk()
app = Window(root)
root.wm_title("Robo CAM")
root.config(background="#FFFFFF")
root.geometry("320x200")
global windowSelector
windowSelector =6  #voor de gemakkelijkheid veranderd naar 6
root.mainloop()

contourCnt = 0      #alleen voor windowselector 5


#White balance
####################################################################################################

#video stream
####################################################################################################
try:
    thread.start_new_thread(timer,())
    MQTT_SERVER = "192.168.0.69"
    MQTT_ROBOT = "robotarm"
    MQTT_HOLO = "hololens"
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()
    pipeline.start()
    profile = pipeline.get_active_profile()

    while True:

        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        color = np.asanyarray(color_frame.get_data())
        plt.rcParams["axes.grid"] = False
        #plt.rcParams['figure.figsize'] = [12, 6]
        plt.rcParams['figure.figsize'] = [9, 6]     #figure(figsize=(1,1)) would create an inch-by-inch image, which would be 80-by-80 pixels unless you also give a different dpi argument.

        colorizer = rs.colorizer()
        colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())

        # Create alignment primitive with color as its target stream:
        align = rs.align(rs.stream.color)
        frameset = align.process(frames)

        # Update color and depth frames:
        aligned_depth_frame = frameset.get_depth_frame()
        colorized_depth = np.asanyarray(colorizer.colorize(aligned_depth_frame).get_data())

        # Show the two frames together: gewoon en depth naast elkaar
        images = np.hstack((color, colorized_depth))
        
        # Standard OpenCV boilerplate for running the net:
        
        height, width = color.shape[:2]
        #expected = 300.0 #spelen met dit om tot de nauwkeurigste meting te gaan. 
        expected = 1000.0 #vermoedlijk is dit gelijk aan de breedte van de frame     
        aspect = width / height
        #print(height,expected)
        scale = int(math.ceil(height / expected))
       

        resized_image = cv2.resize(color, (int(round(expected * aspect)),int( expected)))
        crop_start = round(expected * (aspect - 1) / 2)
        crop_img = resized_image[0:int(expected), int(crop_start):int(crop_start+expected)]
            
        inScaleFactor = 0.007843
        meanVal       = 127.53
        
        if windowSelector < 3:
            net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")
            classNames = ("background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair",
                        "cow", "diningtable", "dog", "horse",
                        "motorbike", "person", "pottedplant",
                        "sheep", "sofa", "train", "tvmonitor")

            blob = cv2.dnn.blobFromImage(crop_img, inScaleFactor, (int(expected), int(expected)), meanVal, False)
            net.setInput(blob, "data")
            detections = net.forward("detection_out")
            #print(detections)
            length = int(detections.size / 7)
            print("detected objects: " + str(length))
            print("----------------------")
        if windowSelector < 3:
            if length < 10:
                for x in range(length):

                    label = detections[0,0,x,1]            #class Name     
                    conf  = detections[0,0,x,2]            
                    xmin  = detections[0,0,x,3]
                    ymin  = detections[0,0,x,4]
                    xmax  = detections[0,0,x,5]
                    ymax  = detections[0,0,x,6]

                    print("object nr.: " + str(x))
                    print("class name: " + str(label))
                    print("x min: " + str(xmin * expected))
                    print("y min: " + str(ymin * expected))
                    print("x max: " + str(xmax * expected))
                    print("y max: " + str(ymax * expected))
                    print("----------------------")

                    className = classNames[int(label)]
                    xmin_depth = int((xmin * expected + crop_start) * scale)
                    ymin_depth = int((ymin * expected) * scale)
                    xmax_depth = int((xmax * expected + crop_start) * scale)
                    ymax_depth = int((ymax * expected) * scale)
                    xmin_depth,ymin_depth,xmax_depth,ymax_depth

                    cv2.rectangle(crop_img, (int(xmin * expected), int(ymin * expected)), 
                                (int(xmax * expected), int(ymax * expected)), (255, 255, 255), 2)
                    cv2.putText(crop_img, className, 
                                (int(xmin * expected), int(ymin * expected) - 5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
                    depth = np.asanyarray(aligned_depth_frame.get_data())
                    # Crop depth data:
                    depth = depth[xmin_depth:xmax_depth,ymin_depth:ymax_depth].astype(float)

                    # Get data scale from the device and convert to meters
                    depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
                    depth = depth * depth_scale
                    dist,_,_,_ = cv2.mean(depth)
                    
                    cv2.rectangle(colorized_depth, (xmin_depth, ymin_depth), 
                                (xmax_depth, ymax_depth), (255, 255, 255), 2)

                    cv2.putText(colorized_depth, className, 
                                (xmin_depth, ymin_depth - 5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
                    cv2.putText(colorized_depth, str(round(dist,2)), 
                                (xmin_depth, ymin_depth + 20),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
                        

        if windowSelector == 1:
            #cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)   #cv2.Window normal -> window scaled mee met volgende lijn
            cv2.resizeWindow('RealSense', 640,480)     #de 2 getallen geven de resolutie van de window weer (= de maximale camera resolutie)
            cv2.imshow('RealSense', crop_img)
        
        if windowSelector == 2:
            cv2.namedWindow('RealSense2', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('RealSense2',640,480)
            cv2.imshow('RealSense2',colorized_depth)
        
        if windowSelector == 3:
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

        if windowSelector == 4:

            blurred_frame = cv2.GaussianBlur(crop_img, (5, 5), 0) #removes noise

            lower_red = np.array([000,000,000])
            upper_red = np.array([120,120,120])

            mask = cv2.inRange(crop_img, lower_red, upper_red)
            res = cv2.bitwise_and(crop_img,crop_img, mask= mask)

            cv2.namedWindow('RealSense4', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('RealSense4',640,480)
            cv2.imshow('RealSense4',res)

            cv2.namedWindow('RealSense6', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('RealSense6',640,480)
            cv2.imshow('RealSense6',mask)

        if windowSelector == 5:
            
            blurred_frame = cv2.GaussianBlur(crop_img, (5, 5), 0) #removes noise

            lower_red = np.array([0,0,0])           #houd de waarde tussen zwart
            upper_red = np.array([100,100,100])     #en bijna wit

            mask = cv2.inRange(crop_img, lower_red, upper_red)
            res = cv2.bitwise_and(crop_img,crop_img, mask= mask)

            #https://docs.opencv.org/3.3.1/d4/d73/tutorial_py_contours_begin.html
            #https://www.youtube.com/watch?v=_aTC-Rc4Io0

            imgray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 127, 255, 0)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #thresh gebruikt een waarde uit de grayscale en mask gebruikt een kleur grens uit de rgb scale

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 3)              
            #cv2.drawContours(crop_img, contours, contourCnt, (0,255,0), 3)     #all contours
            
            #print(contourCnt)
            #contourCnt = contourCnt + 1
            #if contourCnt > 20:
            #    contourCnt = 0

            cv2.namedWindow('RealSense5', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('RealSense5',640,480)
            cv2.imshow('RealSense5',crop_img)

            cv2.namedWindow('thresh grey', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('thresh grey',640,480)
            cv2.imshow('thresh grey',thresh)

            cv2.namedWindow('mask rgb', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('mask rgb',640,480)
            cv2.imshow('mask rgb',mask)

        if windowSelector == 6:
            global timerBool

            blurred_frame = cv2.GaussianBlur(crop_img, (5, 5), 0) #removes noise

            lower_red = np.array([0,0,0])           #houd de waarde tussen zwart
            upper_red = np.array([100,100,100])     #en bijna wit

            mask = cv2.inRange(crop_img, lower_red, upper_red)
            res = cv2.bitwise_and(crop_img,crop_img, mask= mask)
            
            #CREATE DEAD ZONE (MASK) -> robot arm word hierdoor niet gedetecteerd
            robotWidth = 250 
            robotHeight = 600 
            xRobot = 500 - (robotWidth/2)
            yRobot = 650 - (robotHeight/2)
            xRobotWidth = xRobot + robotWidth
            yRobotHeight = yRobot + robotHeight

            cv2.rectangle(mask,(xRobot,yRobot),(xRobotWidth,yRobotHeight),(0,0,0),-1)              
            cv2.rectangle(crop_img,(xRobot,yRobot),(xRobotWidth,yRobotHeight),(255,255,0),-1)
            #https://docs.opencv.org/3.3.1/d4/d73/tutorial_py_contours_begin.html
            #https://www.youtube.com/watch?v=_aTC-Rc4Io0

            imgray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray, 127, 255, 0)

            contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  #thresh gebruikt een waarde uit de grayscale en mask gebruikt een kleur grens uit de rgb scale

            cv2.drawContours(crop_img, contours, -1, (0,255,0), 3)              
            #cv2.drawContours(crop_img, contours, contourCnt, (0,255,0), 3)     #all contours

            contours = sorted(contours, key = cv2.contourArea, reverse = True)[:1] # get the largest contour area
            (xc,yc),radius = cv2.minEnclosingCircle(contours[0])
            center = (int(xc),int(yc))
            radius = int(radius)
            cv2.circle(crop_img,center,radius,(0,255,0),2)
            print "center: " + str(center)
            rects = []
            for c in contours:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)
                x, y, w, h = cv2.boundingRect(approx)

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
                msg = {"x" : x_robot, "y" : y_robot, "z" : 50}
                print(json.dumps(msg, sort_keys=True, indent=4))
                publish.single(MQTT_ROBOT,payload=json.dumps(msg),hostname=MQTT_SERVER)
                timerBool = False

                #print("----------------------------------")
                #print("x center" + str(((x + (w/2))*expected)/1000) + "mm " + str(((x + (w/2))*expected)/10000000*expected) + "%")
                #print("y center" + str(((y + (h/2))*expected)/1000) + "mm " + str(((y + (h/2))*expected)/10000000*expected) + "%")
                #print("----------------------------------")
                
                
                
            kommaX = ((x + (w/2))*expected)/1000000000*expected
            kommaY = ((y + (h/2))*expected)/1000000000*expected
            publish.single(MQTT_HOLO,payload = str(kommaX) + ","+str(kommaY),hostname = MQTT_SERVER)
            cv2.namedWindow('RealSense5', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('RealSense5',640,480)
            cv2.imshow('RealSense5',cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))

            #cv2.namedWindow('thresh grey', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('thresh grey',640,480)
            #cv2.imshow('thresh grey',thresh)

            #cv2.namedWindow('mask rgb', cv2.WINDOW_NORMAL)
            #cv2.resizeWindow('mask rgb',640,480)
            #cv2.imshow('mask rgb',mask)

        cv2.waitKey(1)
        


    exit(0)
        
#except rs.error as e:
#    # Method calls agaisnt librealsense objects may throw exceptions of type pylibrs.error
#    print("pylibrs.error was thrown when calling %s(%s):\n", % (e.get_failed_function(), e.get_failed_args()))
#    print("    %s\n", e.what())
#    exit(1)
except Exception as e:
    print(e)
    pass