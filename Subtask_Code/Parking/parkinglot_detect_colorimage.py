import cv2  
import numpy as np
import math
#ͼƬת��  
img = cv2.imread("2.png")
img_c = img.copy()
img_hsv = cv2.cvtColor(img_c,cv2.COLOR_BGR2HSV)
img_gray = cv2.cvtColor(img_c,cv2.COLOR_BGR2GRAY)
#img_th = cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU)

cv2.imshow("img",img_c)
cv2.imshow("hsv",img_hsv)

#RGB
#test
##lower = np.array([135,30,230])  
##upper = np.array([145,35,240])
#2.png��ɫ
##lower = np.array([0,20,00])  
##upper = np.array([60,50,100])
#1.png��ɫ
##lower = np.array([30,5,100])  
##upper = np.array([50,30,140])
#2.png��ɫ
##lower = np.array([85,45,130])  
##upper = np.array([105,75,170])
#3.png��ɫ
##lower = np.array([0,0,160])  
##upper = np.array([5,10,210])

##mask = cv2.inRange(img_c,lower,upper)

#HSV
#1
##lower = np.array([90,0,0])  
##upper = np.array([110,255,255])
#2
lower = np.array([160,0,0])  
upper = np.array([175,255,255])
#3 ��̫�� ���׺Ͱ�ɫHSV����
##lower = np.array([20,0,0])  
##upper = np.array([40,255,255])
#4
##lower = np.array([80,0,0])  
##upper = np.array([90,255,255])

mask = cv2.inRange(img_hsv,lower,upper)


#HSV��ɫ����ȡ&�߿���ȡ  

#mask = cv2.erode (mask,None,iterations=3)
mask = cv2.dilate(mask,None,iterations=3)
#img_res =cv2.bitwise_not(mask,mask)
mask_c = mask.copy()
cnts = cv2.findContours(mask_c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
if cnts==[]:print "����ֵ��Χ����ָ������"
else:
    #�������߿�����Ұ�г�������
    c = max(cnts,key = cv2.contourArea)
    cv2.drawContours(img_c,c,-1,(255,255,0),3)
    ##M = cv2.moments(c)
    ##center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
    ##print "method_1:",center
    ##cv2.circle(img_c, center, 1, (0, 0, 255), 8)
    #������С���λ�ó�������
    rect = cv2.minAreaRect(c)
    center_x,center_y = rect[0]
    width, height = rect[1]
    theta = rect[2]
    print "width",width
    print "height",height
    print "center",rect[0]
    print "angle:",rect[2]

    box = cv2.cv.BoxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(img_c, [box], 0, (255,0,0), 2)
    #���� ���� ���� ��������
    lt_x,lt_y= box[1]
    lb_x,lb_y= box[0]
    rt_x,rt_y= box[2]
    rb_x,rb_y= box[3]    
##    cv2.circle(img_c,(lt_x,lt_y), 1, (255, 255,0), 8)
##    cv2.circle(img_c,(lb_x,lb_y), 1, (255, 255,0), 8)
##    cv2.circle(img_c,(rt_x,rt_y), 1, (255, 255,0), 8)
##    cv2.circle(img_c,(rb_x,rb_y), 1, (255, 255,0), 8)
    #���±��е�
    y = [lt_y,lb_y,rt_y,rb_y]
    y.sort()
    x = []
    for i in range (4):
        for j in range (4):
            if box[j][1]==y[i]:
                x.append(box[j][0])
                box[j][1]=-1
                break
    mt_x = (x[3]+x[2])/2
    mt_y = (y[3]+y[2])/2
    mb_x = (x[1]+x[0])/2
    mb_y = (y[1]+y[0])/2
    print "�ϱ��е�",mt_x,mt_y
    print "�±��е�",mb_x,mb_y
    cv2.circle(img_c,(mt_x,mt_y), 1, (0,255,0), 8)
    cv2.circle(img_c,(mb_x,mb_y), 1, (0, 255,0), 8)
    cv2.circle(img_c,(int(center_x),int(center_y)), 1, (0, 0, 255), 8)
     
    #cv2.imshow('mask',mask)  

    cv2.imshow('img_res',img_c)



###HSV��ֵ
##lower = np.array([170,120,140])  
##upper = np.array([180,170,170])  
###HSV��ɫ����ȡ&�߿���ȡ  
##mask = cv2.inRange(img_hsv,lower,upper)
###mask = cv2.erode (mask,None,iterations=3)
##mask = cv2.dilate(mask,None,iterations=3)
##img_res =cv2.bitwise_and(img,img,mask=mask)
##mask_c = mask.copy()
##cnts = cv2.findContours(mask_c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
###�������߿�����Ұ�г�������
##c = max(cnts,key = cv2.contourArea)
##M = cv2.moments(c)
##center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
##
##print "method_1:",center
##cv2.circle(img_c, center, 1, (0, 0, 255), 8)
###������С���λ�ó�������
##rect = cv2.minAreaRect(c)
##x,y = rect[0]
##width, height = rect[1]    
##p1 = (int(x+width/2),int(y-height/2))
##
##print "method_1:",rect[0]
##cv2.circle(img_c,(int(x),int(y)), 1, (0, 0, 255), 8)
###cv2.circle(img_c,p1, 1, (0, 0, 255), 8)
##
###########
##cv2.drawContours(img_c,c,-1,(255,255,0),3)
###cv2.imshow('img',img)  
###cv2.imshow('mask',mask)  
##
##cv2.imshow('img_res',img_c)

cv2.waitKey (0)  
cv2.destroyAllWindows()
