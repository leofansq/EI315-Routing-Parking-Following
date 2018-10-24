import cv2
import time
import math
import imgRoadLotPark 
import numpy as np
from driver import driver

cap = cv2.VideoCapture(1)
d = driver()
cnt = 0
ser=0
errDift = 0
lastErr = 0
err,lerr = 0,0
lostSte = 0
d.setStatus(mode="speed",dist=0x1000,motor=0.05)
while(1):
    ret,frame = cap.read()
    
    keeplost = err
    [err,lostSte,lost] = imgRoadLotPark.roadTrajectory(frame,ser,lostSte,keeplost)

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
        if(abs(lost)>0.5):
            d.setStatus(servo=ser,motor=0.05)
        else:
            d.setStatus(servo=ser,motor=0.05)
    else:
        cnt =cnt+1
            
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 
