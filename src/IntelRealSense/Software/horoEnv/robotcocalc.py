if timerBool: 
            #x_tussenwaarde = int(x_waarde/expected)
            #for punten in puntenDepth:
             #   x_temp = int(punten[0])
              #  y_temp = int(punten[1])
                #try_depth = aligned_depth_frame.get_distance(693,805)
                #depth = depthRef - try_depth

                #print "diepte van het punt op xy: " + str(try_depth)

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
