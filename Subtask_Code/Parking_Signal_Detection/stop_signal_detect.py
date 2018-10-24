import cv2  
import numpy as np

img = cv2.imread("stop.jpg")
img1 = img.copy()
#转灰度图与二值化
img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret,img3 = cv2.threshold(img2, 80, 255, cv2.THRESH_BINARY)
#轮廓提取
img4 = np.zeros(img.shape, np.uint8)
cnts1 = cv2.findContours(img3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
cnts2 = []
centerx = []
centery = []
#轮廓筛选
for i in cnts1:
    area = cv2.contourArea(i)
    if area > 500 and area < 500000:
        cnts2.append(i)
        M = cv2.moments(i)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        centerx.append(center[0])
        centery.append(center[1])
delx = []
dely = []
for j in range(len(centerx)):
    print centerx[j],
    print centery[j];
    delx.append(abs(centerx[j] - centerx[0]))
    dely.append(abs(centery[j] - centery[0]))

if len(centerx)==4 and sum(delx) < 10 and sum(dely) < 30:
    print "停止！"
cv2.drawContours(img4,cnts2,-1,(255,255,255),1)

cv2.imshow("img2", img4)
cv2.waitKey(0)
#cv2.destoryAllWindows()
