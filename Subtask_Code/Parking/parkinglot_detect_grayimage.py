import cv2  
import numpy as np  
  
img = cv2.imread("1.png")
img_c = img.copy()
img_hsv = cv2.cvtColor(img_c,cv2.COLOR_BGR2HSV)
img_gray = cv2.cvtColor(img_c,cv2.COLOR_BGR2GRAY)

lower = np.array([28,125,140])  
upper = np.array([32,155,180])  
  
mask = cv2.inRange(img_hsv,lower,upper)
mask = cv2.erode (mask,None,iterations=3)
mask = cv2.dilate(mask,None,iterations=3)
img_res =cv2.bitwise_and(img,img,mask=mask)
mask_c = mask.copy()
cnts = cv2.findContours(mask_c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]

area_max = 0
for c in cnts:
    if cv2.contourArea(c)>area_max:
        area_max = cv2.contourArea(c)
        cnts_max = c
M = cv2.moments(cnts_max)
center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))

##dst = cv2.cornerHarris(mask,2,3,0.04)
##img_c[dst>0.01*dst.max()]=[0,0,255]

cv2.drawContours(img_c,cnts_max,-1,(255,255,0),3)
cv2.circle(img_c, center, 3, (0, 0, 255), 8)


#cv2.imshow('img',img)  
cv2.imshow('mask',img_gray)  
cv2.imshow('img_res',img_c)

cv2.waitKey (0)  
cv2.destroyAllWindows()


 
 
