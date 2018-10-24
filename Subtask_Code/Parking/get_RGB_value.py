import cv2  
import numpy as np  
from matplotlib import pyplot as plt
image=cv2.imread('0.png')  
HSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
RGB=image
def getpos(event,x,y,flags,param):  
    if event==cv2.EVENT_LBUTTONDOWN:  
        print(RGB[y,x])
cv2.imshow("imageRGB",RGB)
cv2.setMouseCallback("imageRGB",getpos) 
cv2.waitKey(0) 
