import cv2  
import numpy as np  
from matplotlib import pyplot as plt

image=cv2.imread('2.png')
img = image.copy()

HSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
def getpos(event,x,y,flags,param):  
    if event==cv2.EVENT_LBUTTONDOWN:  
        print(HSV[y,x])
cv2.imshow("imageHSV",HSV)
#cv2.imshow('image',img)  
cv2.setMouseCallback("imageHSV",getpos)
cv2.waitKey(0) 
