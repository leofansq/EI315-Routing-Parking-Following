import cv2
import time
import math
import imgRoadLotPark
import numpy as np
from driver import driver


x1_last,y1_last,x2_last,y2_last = 0,0,0,0
preParking = 0
trigger = 0
capTail = cv2.VideoCapture(0)
capHead = cv2.VideoCapture(1)
d = driver()
ser = 0
errDift = 0
lastErr = 0
lerr = 0
err = 0
lostSte = 0
cnt = 0
stopFlag = 0
parkErrSum = 0
avetheta = 5*[0]
isStop = 10*[0]


while(1):
    
    retTail,frameTail = capTail.read()
    retHead,frameHead = capHead.read()

    if(trigger==0):
        #flag = imgRoadLotPark.isParking3(frameHead)
        flag = 1
    if(flag==0 and trigger==0):
        #print "searching sign!!!"
        #follow the road trajectory
        keeplost = err
        [err,lostSte,lost] = imgRoadLotPark.roadTrajectory(frameHead,ser,lostSte,keeplost)

        err = 0.4*err + 0.6*lerr
        lerr = err
    
        errDift = err - lastErr
        lastErr = err

        ser = lost + 0.004*err + 0.001*errDift

        if(abs(ser)>1):
            ser = 1.0*ser/abs(ser)
    
        print(err,errDift,ser,lost)

        if(cnt==2):
            cnt = 0
            d.setStatus(mode="speed",motor=0.05,servo=ser)
        else:
            cnt =cnt+1
            

    else:
        print "find sign!!!"
        #park to the lot
        trigger = 1 #in this way, it dosenot occer to cruising any more
        
        #in this section,wanna adjust the posture of the car first
        if(preParking==0):
            preParking = preParking+1

        else:
            lotInfo = imgRoadLotPark.pLot(frameTail)
            #lotInfo = [check,mt_x,mt_y,mb_x,mb_y,stop,center_x,center_y]

            if(lotInfo[0]==0):#does not find the lot
                if(cnt==6):
                    cnt = 0
                    d.setStatus(mode="distance",dist=0x1000,motor=-0.05,servo=0)
                elif(cnt==3):
                    cnt =cnt+1
                    d.setStatus(mode="stop")
                else:
                    cnt = cnt+1
                    #time.sleep(1)
                    #d.setStatus(mode="stop")

            else:
                center_x,center_y = lotInfo[6],lotInfo[7]
                mt_x,mt_y,mb_x,mb_y = lotInfo[1],lotInfo[2],lotInfo[3],lotInfo[4]     
                x1,y1 = 0.6*mt_x+0.4*x1_last,0.6*mt_y+0.4*y1_last
                x2,y2 = 0.6*mb_x+0.4*x2_last,0.6*mb_y+0.4*y2_last
                x1_last,y1_last,x2_last,y2_last = x1,y1,x2,y2

                #judge if time to stop
                for i in range(9):
                    isStop[i]=isStop[i+1]
                isStop[9] = lotInfo[5]
                print(isStop)

                s = 0
                for i in range(10):
                    s = s+isStop[i]
                    
                if(s>=4):
                    stopFlag = 1
                    print "NOW STOP!!!"
                else:
                    stopFlag = 0
                
                height,width = cv2.cvtColor(frameTail,cv2.COLOR_BGR2GRAY).shape;        

                err_center = (center_x - 0.5*width)/(width/2)
                err_mt = (mt_x - 0.4*width)/(width/2)
                err_mb = (mb_x - 0.4*width)/(width/2)

                err = 0.5*err_mb + 0.4*err_center + 0.1*err_mt
                
                if(abs(parkErrSum)>10):
                    parkErrSum = 10*parkErrSum/abs(parkErrSum)
                ser = 1.5*err + 0.1*parkErrSum
                if ser>1:
                    ser=0.7
                elif ser<-1:
                    ser=-0.7
                else:
                    ser=ser

                print "err",err,"ser",ser
                
                if(cnt==4):
                    cnt = 0
                    parkErrSum = parkErrSum + err
                    d.setStatus(mode="distance",dist=0x2000,motor=-0.05,servo=ser)
                elif(cnt==1):
                    cnt = cnt+1
                    d.setStatus(mode="stop")
                else:
                    cnt = cnt+1
                    #time.sleep(1)
                    #d.setStatus(mode="stop")
                #time.sleep(1)

    if(stopFlag==1):
        d.setStatus(mode="stop")

    if cv2.waitKey(1) & stopFlag==1:#0xFF ==ord('q'):
        break
capHead.release()
capTail.release()
cv2.destroyAllWindows() 

       






















        
