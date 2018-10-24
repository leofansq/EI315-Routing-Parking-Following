#--coding:UTF-8--
import cv2
import time
import math
import numpy as np

lostSte = 0
kernel = np.uint8([[ 0.,  0.,  1.,  0.,  0.],
                       [ 0.,  0.,  1.,  0.,  0.],
                       [ 1.,  1.,  1.,  1.,  1.],
                       [ 0.,  0.,  1.,  0.,  0.],
                       [ 0.,  0.,  1.,  0.,  0.]])

def roadTrajectory(frame,ser,lostSte,keeplost):
    img1 = cv2.flip(frame,0)
    img2 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    height,width = img2.shape;
    img2 = img2[0*height/5:height,1*width/6:5*width/6]

    ret,img4 = cv2.threshold(img2,0,255,cv2.THRESH_OTSU)
    #ret,img4 = cv2.threshold(img2,80,255,cv2.THRESH_BINARY)
    
    #img5 = cv2.blur(img4,(3,5)) 
    #ret,img6 = cv2.threshold(img3,50,255,cv2.THRESH_BINARY)

    img5 = cv2.erode(img4,kernel)
    img6 = cv2.dilate(img4,kernel)
    img6 = cv2.erode(img6,kernel)

    error = []
    err = 0

    Fflag,Lflag = 0,0
    lineSum = 0
    height,width = img6.shape;
    
    if abs(ser)<0.7:
        #aim = 3*height/4 + abs(ser)*(height/4-15)/0.7
        aim = height - 25
    else:
        aim = height-25
        
    #for i in range(height-1):
    for i in range(10):
        i = int(aim) + i
        for j in range(width-1):
            #print(img6[i,j])
            lineSum = lineSum+img6[i,j]
            if (img6[i,j]==255 and img6[i,j+1]==0):
                Fflag = j
            if (img6[i,j]==255 and img6[i,j-1]==0):
                Lflag =j
                
        if lineSum >= 255*(width-5):
            lineSum = 0
            #error.append(0)
            #print(i,0)
        else: 
            error.append((Lflag+Fflag)/2-width/2)
            #print(i,(Lflag+Fflag)/2-width/2)
            
    if(error==[]):
        lostFlag = 1
    else:
        lostFlag = 0
    
    #formor error small shre        
    for i in range(len(error)):
        err = err+error[i]*(1-0*i)/len(error)
    
    if(keeplost<0):
        lostSte = -0.9
    elif(keeplost>0):
        lostSte = 0.9
    else:
        lostSte = lostSte
        
    cv2.imshow("roadTrajectory",img6)
    roadTraj = [err,lostSte,lostFlag*lostSte]
    return roadTraj



def pLot(frame):
    img = frame
    img_c = img.copy()
    img_hsv = cv2.cvtColor(img_c,cv2.COLOR_BGR2HSV)
    img_gray = cv2.cvtColor(img_c,cv2.COLOR_BGR2GRAY)
    #img_th = cv2.threshold(img_gray,0,255,cv2.THRESH_OTSU)

    #HSV
    #2
##    lower = np.array([160,130,100])  
##    upper = np.array([180,210,220])
    #3
    lower = np.array([30,90,110])
    upper = np.array([40,180,180])

    #HSV颜色块提取&边框提取  
    mask = cv2.inRange(img_hsv,lower,upper)
    #mask = cv2.erode (mask,None,iterations=3)
    mask = cv2.dilate(mask,None,iterations=3)
    #img_res =cv2.bitwise_not(mask,mask)
    mask_c = mask.copy()
    cnts = cv2.findContours(mask_c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    if cnts==[]:
        check = 0
        #d.setStatus(mode="speed",motor=-0.05,dist=0x1000)
        #d.setStatus(servo=0)
        print "该阈值范围内无指定车库"
        pInfo = [check]
    else:
        check = 1
        #根据最大边框获得视野中车库中心
        c = max(cnts,key = cv2.contourArea)
        #cv2.drawContours(img_c,c,-1,(255,255,0),3)
        ##M = cv2.moments(c)
        ##center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        ##print "method_1:",center
        ##cv2.circle(img_c, center, 1, (0, 0, 255), 8)
        #根据最小矩形获得车库中心
        rect = cv2.minAreaRect(c)
        center_x,center_y = rect[0]
        width, height = rect[1]
        theta = rect[2]
##        print "width",width
##        print "height",height
##        print "center",rect[0]
##        print "angle:",rect[2]

        box = cv2.cv.BoxPoints(rect)
        box = np.int0(box)
        #cv2.drawContours(img_c, [box], 0, (255,0,0), 2)
        #左上 左下 右上 右下坐标
        lt_x,lt_y= box[1]
        lb_x,lb_y= box[0]
        rt_x,rt_y= box[2]
        rb_x,rb_y= box[3]    
    ##    cv2.circle(img_c,(lt_x,lt_y), 1, (255, 255,0), 8)
    ##    cv2.circle(img_c,(lb_x,lb_y), 1, (255, 255,0), 8)
    ##    cv2.circle(img_c,(rt_x,rt_y), 1, (255, 255,0), 8)
    ##    cv2.circle(img_c,(rb_x,rb_y), 1, (255, 255,0), 8)
        #上下边中点
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
        #print "上边中点",mt_x,mt_y
        #print "下边中点",mb_x,mb_y
        cv2.circle(img_gray,(mt_x,mt_y), 1, (0,255,0), 8)
        cv2.circle(img_gray,(mb_x,mb_y), 1, (0, 255,0), 8)
        cv2.circle(img_gray,(int(center_x),int(center_y)), 1, (0, 0, 255), 8)

        if(center_y>410):
            stop = 1
        else:
            stop = 0
            
        pInfo = [check,mt_x,mt_y,mb_x,mb_y,stop,center_x,center_y]
        #cv2.imshow('mask',mask)  
        cv2.imshow('pLot',img_gray)

        
    return pInfo
    

##def isParking(img1):
##    #转灰度图与二值化
##    img1 = cv2.flip(img1,0)
##    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
##    ret,img3 = cv2.threshold(img2, 80, 255, cv2.THRESH_BINARY)
##    #轮廓提取
##    img4 = np.zeros(img1.shape, np.uint8)
##    cnts1 = cv2.findContours(img3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
##    cnts2 = []
##    centerx = []
##    centery = []
##    #轮廓筛选
##    for i in cnts1:
##        area = cv2.contourArea(i)
##        if area > 500 and area < 100000:
##            cnts2.append(i)
##            M = cv2.moments(i)
##            center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
##            if abs(center[0]-320) < 250 and abs(center[1]-240) < 200:
##                centerx.append(center[0])
##                centery.append(center[1])
##            else:
##                cnts2.pop()
##    delx = []
##    dely = []
##    flag = 0
##    for j in range(len(centerx)):
##        #print centerx[j],
##        #print centery[j];
##        delx.append(abs(centerx[j] - centerx[0]))
##        dely.append(abs(centery[j] - centery[0]))
##
##    if len(centerx)==4 and sum(delx) < 10 and sum(dely) < 30:
##        flag = 1
####        print "停止！"
####    else:
####        print "no!"
##    #cv2.drawContours(img4,cnts2,-1,(255,255,255),1)
##
##    #cv2.imshow("img2", img4)
##    #cv2.waitKey(0)
##    #cv2.destoryAllWindows()
##    return flag



def isParking1(img1):
    img1 = cv2.flip(img1,0)
    #转灰度图与二值化
    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    ret,img3 = cv2.threshold(img2, 80, 255, cv2.THRESH_BINARY)
    #轮廓提取
    img4 = np.zeros(img1.shape, np.uint8)
    cnts1 = cv2.findContours(img3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    cnts2 = []
    centerx = []
    centery = []
    #轮廓筛选
    for i in cnts1:
        area = cv2.contourArea(i)
        if area > 500 and area < 120000:
            cnts2.append(i)
            M = cv2.moments(i)
            center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
            if abs(center[0]-320) < 250 and abs(center[1]-240) < 200:
                centerx.append(center[0])
                centery.append(center[1])
            else:
                cnts2.pop()
    delx = []
    dely = []
    flag = False
    for j in range(len(centerx)):
        #print centerx[j],
        #print centery[j];
        delx.append(abs(centerx[j] - centerx[0]))
        dely.append(abs(centery[j] - centery[0]))

    if len(centerx)>2 and sum(delx) < 10 and sum(dely) < 30:
        #print "停止！"
        flag = True
    #cv2.drawContours(img4,cnts2,-1,(255,255,255),1)

    #cv2.imshow("img1", img1)
##    cv2.waitKey(0)
    #cv2.destoryAllWindows()
    return flag


#霍夫变换，不能识别同心圆
def isParking2(img1):
    img1 = cv2.flip(img1,0)
    #cv2.imshow("img1", img1)
    #转HSV图
    img2 = cv2.medianBlur(img1,3)
    img_hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
    #HSV阈值
    lower = np.array([108,200,150])  
    upper = np.array([118,255,255])  
    #HSV颜色块提取&边框提取  
    mask = cv2.inRange(img_hsv,lower,upper)
    
    img4 = np.zeros(img1.shape, np.uint8)
    
    mask = cv2.dilate(mask,None,iterations=2)
    mask = cv2.medianBlur(mask,7)
    cv2.imshow("mask",mask)
    #img_res =cv2.bitwise_and(img,img,mask=mask)
    mask_c = mask.copy()
    cnts1 = cv2.findContours(mask_c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    #根据最大边框获得中心
##    c = max(cnts1,key = cv2.contourArea)
##    M = cv2.moments(c)
##    center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
##    cv2.circle(img4, center, 1, (0, 0, 255), 5)

    centerx = []
    centery = []
    #轮廓筛选
    try:
        for i in cnts1:
                M = cv2.moments(i)
                center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
                centerx.append(center[0])
                centery.append(center[1])
                #cv2.circle(img4, center, 1, (0, 0, 255), 5)
        delx = []
        dely = []
        #flag = False
        for j in range(len(centerx)):
            #print centerx[j],
            #print centery[j];
            delx.append(abs(centerx[j] - centerx[0]))
            dely.append(abs(centery[j] - centery[0]))

        if len(centerx)>0 and sum(delx) < 20 and sum(dely) < 50:
            #print "停止！"
            #flag = True
            return True
        return False
    except:
        return False

#HSV
def isParking3(img1):
    img1 = cv2.flip(img1,0)
    #cv2.imshow("img1", img1)
    #转HSV图
    img2 = cv2.medianBlur(img1,3)
    img_hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
    #HSV阈值
    lower = np.array([108,200,150])  
    upper = np.array([118,255,255])  
    #HSV颜色块提取&边框提取  
    mask = cv2.inRange(img_hsv,lower,upper)
    
    img4 = np.zeros(img1.shape, np.uint8)
    
    mask = cv2.dilate(mask,None,iterations=2)
    mask = cv2.medianBlur(mask,7)
    #cv2.imshow("mask",mask)
    #img_res =cv2.bitwise_and(img,img,mask=mask)
    mask_c = mask.copy()
    cnts1 = cv2.findContours(mask_c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    #根据最大边框获得中心
##    c = max(cnts1,key = cv2.contourArea)
##    M = cv2.moments(c)
##    center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
##    cv2.circle(img4, center, 1, (0, 0, 255), 5)

    centerx = []
    centery = []
    #轮廓筛选
    try:
        for i in cnts1:
                M = cv2.moments(i)
                center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
                centerx.append(center[0])
                centery.append(center[1])
                #cv2.circle(img4, center, 1, (0, 0, 255), 5)
        delx = []
        dely = []
        #flag = False
        for j in range(len(centerx)):
            #print centerx[j],
            #print centery[j];
            delx.append(abs(centerx[j] - centerx[0]))
            dely.append(abs(centery[j] - centery[0]))

        if len(centerx)>2 and sum(delx) < 20 and sum(dely) < 50:
            #print "停止！"
            #flag = True
            return True
        return False
    except:
        return False

    #########
##    cv2.drawContours(img4,cnts1,-1,(255,255,0),1)
##    cv2.imshow('mask',mask)  
##    cv2.imshow('HSV',img_hsv)  
##    cv2.imshow('img_res',img4)
##
##    cv2.waitKey (0)
    #cv2.destroyAllWindows()
    #return flag

##print function3(img1)
##HSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
##for i in range(80):
##    print(HSV[350,10*i]);


def follow(img1):
    img1 = cv2.flip(img1,0)
    #cv2.imshow("img1", img1)
    #转HSV图
    img2 = cv2.medianBlur(img1,3)
    img_hsv = cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)
    #HSV阈值
    lower = np.array([108,200,80])  
    upper = np.array([118,255,150])  
    #HSV颜色块提取&边框提取  
    mask = cv2.inRange(img_hsv,lower,upper)
    
    img4 = np.zeros(img1.shape, np.uint8)
    
    mask = cv2.dilate(mask,None,iterations=2)
    mask = cv2.medianBlur(mask,7)
    cv2.imshow("mask",mask)
    #img_res =cv2.bitwise_and(img,img,mask=mask)
    mask_c = mask.copy()
    cnts1 = cv2.findContours(mask_c,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]
    

##    centerx = []
##    centery = []
##
##    flag = 0
##    #轮廓筛选
##    try:
##        for i in cnts1:
##            M = cv2.moments(i)
##            center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
##            centerx.append(center[0])
##            centery.append(center[1])
##                #cv2.circle(img4, center, 1, (0, 0, 255), 5)
##        delx = []
##        dely = []
##        #flag = False
##        for j in range(len(centerx)):
##            #print centerx[j],
##            #print centery[j];
##            delx.append(abs(centerx[j] - centerx[0]))
##            dely.append(abs(centery[j] - centery[0]))
##
##        if len(centerx)>1 and sum(delx) < 20 and sum(dely) < 50:
##            #print "停止！"
##            flag = 1
##        else:
##            flag = 0
##    except:
##        flag = 0
    
    flag = 0
    try:
        c = max(cnts1,key = cv2.contourArea)
        area = cv2.contourArea(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        flag = 1
    except:
        flag = 0
        
    if flag==1 and area > 1000:
#根据最大边框获得中心
        
##        #根据最大边框获得中心
##        c = max(cnts1,key = cv2.contourArea)
##        area = cv2.contourArea(c)
##        M = cv2.moments(c)
##        center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        #cv2.imshow('mask',mask)
        print center,"area",area
        #(x,y)=center[0,1],S=pi*r*r=area
        err=[center[0]-320,area-3000]
        return err
    else:
        return [0,0]
