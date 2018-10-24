import cv2
import time
import math
import imgRoadLotPark
import numpy as np
from driver import driver

#capTail = cv2.VideoCapture(0)
capHead = cv2.VideoCapture(1)
d = driver()
cnt = 0
errSum,errDiff,lastErr = [0,0],[0,0],[0,0]

while(1):
    
    #retTail,frameTail = capTail.read()
    retHead,frameHead = capHead.read()
    frameHead= cv2.flip(frameHead,0)
    err = imgRoadLotPark.follow(frameHead)

    errSum[0],errSum[1] = errSum[0]+err[0],errSum[1]+err[1]
    errDiff[0],errDiff[1] = err[0] - lastErr[0],err[1] - lastErr[1]
    servo1 = 1.0*err[0]+0.0*errSum[0]+0*errDiff[0]
    motor1 = 0.0003*(1.0*err[1]+0.1*errSum[1]+0*errDiff[1])

    lastErr = err

    print "err",err
    if(cnt==7):
        cnt = 0
        d.setStatus(mode="speed",motor=0.05,servo=servo1)
    else:
        cnt = cnt+1
        
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
capHead.release()
capTail.release()
cv2.destroyAllWindows() 
