import math
import cv2  
import numpy as np

img = cv2.imread("1.png")
img1 = img.copy()
#转灰度图与二值化
#img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret,img3 = cv2.threshold(img2, 0, 255, cv2.THRESH_OTSU)
##for i in range(15):
##    img3 = cv2.erode (img3,None,iterations=1)
##    img3 = cv2.dilate(img3,None,iterations=1)

cv2.imshow("img3", img3)
#ret,img3 = cv2.threshold(img2, 80, 255, cv2.THRESH_BINARY)

#轮廓提取
img4 = np.zeros(img.shape, np.uint8)
cnts1 = cv2.findContours(img3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
cnts2 = []

#轮廓筛选
for i in cnts1:
    area = cv2.contourArea(i)
    #print area
    if area > 0 and area < 100000:
        cnts2.append(i)
c = max(cnts2,key = cv2.contourArea)
M = cv2.moments(c)
center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
cv2.circle(img4,center, 1, (255, 0, 0), 8)#blue

rect = cv2.boundingRect(c)
cv2.circle(img4,(rect[0],rect[1]), 1, (0, 255,0), 8)
#green
cv2.rectangle(img4, (rect[0],rect[1]), (rect[0]+rect[2],rect[1]+rect[3]), (0,255,0), 2)

rect2 = cv2.minAreaRect(c)
x,y = rect2[0]
width, height = rect2[1]
theta = rect2[2]
x_1 = height/2*math.sin(theta)
y_1 = height/2*math.cos(theta)
#横矩形
p1 = (int(x-y_1),int(y+x_1))
p2 = (int(x+y_1),int(y-x_1))
#立矩形
##p1 = (int(x+x_1),int(y-y_1))
##p2 = (int(x-x_1),int(y+y_1))

#red
cv2.circle(img4,(int(x),int(y)), 1, (0, 0, 255), 8)
cv2.circle(img4,p1, 1, (0, 0,255), 8)
cv2.circle(img4,p2, 1, (0, 0,255), 8)

box = cv2.cv.BoxPoints(rect2)
box = np.int0(box)
#print box
cv2.drawContours(img4, [box], 0, (0, 0, 255), 2)



cv2.drawContours(img4,cnts2,-1,(255,255,255),1)

cv2.imshow("img4", img4)
cv2.waitKey(0)
#cv2.destoryAllWindows()
