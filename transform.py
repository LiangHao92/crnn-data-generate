#coding:utf-8

import cv2
import numpy as np
from math import *
from config import config_deal


class transform_deal(config_deal):
    def __init__(self):
        config_deal.__init__(self)
    

    def rad(self,x):
        return x*np.pi/180

    def trans(self,img,points,angle,flag,fov=42):
        w,h=img.shape[0:2]
        z=np.sqrt(w**2+h**2)/2/np.tan(self.rad(fov/2))
        if(flag=='x'):
            x_angle=angle
            r=np.array([[1, 0, 0, 0],
                      [0, np.cos(self.rad(x_angle)), -np.sin(self.rad(x_angle)), 0],
                      [0, -np.sin(self.rad(x_angle)), np.cos(self.rad(x_angle)), 0, ],
                      [0, 0, 0, 1]], np.float32)
        elif(flag=='y'):
            y_angle=angle
            r=np.array([[np.cos(self.rad(y_angle)), 0, np.sin(self.rad(y_angle)), 0],
                      [0, 1, 0, 0],
                      [-np.sin(self.rad(y_angle)), 0, np.cos(self.rad(y_angle)), 0, ],
                      [0, 0, 0, 1]], np.float32)
        else:
            z_angle=angle
            r=np.array([[np.cos(self.rad(z_angle)), np.sin(self.rad(z_angle)), 0, 0],
                      [-np.sin(self.rad(z_angle)), np.cos(self.rad(z_angle)), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]], np.float32)
        pcenter = np.array([h / 2, w / 2, 0, 0], np.float32)
        p1 = np.array([0, 0, 0, 0], np.float32) - pcenter
        p2 = np.array([w, 0, 0, 0], np.float32) - pcenter
        p3 = np.array([0, h, 0, 0], np.float32) - pcenter
        p4 = np.array([w, h, 0, 0], np.float32) - pcenter
        dst1 = r.dot(p1)
        dst2 = r.dot(p2)
        dst3 = r.dot(p3)
        dst4 = r.dot(p4)
        list_dst = [dst1, dst2, dst3, dst4]
        org = np.array([[0, 0],[w, 0],[0, h],[w, h]], np.float32)
        dst = np.zeros((4, 2), np.float32)
        for i in range(4):
            dst[i, 0] = list_dst[i][0] * z / (z - list_dst[i][2]) + pcenter[0]*2
            dst[i, 1] = list_dst[i][1] * z / (z - list_dst[i][2]) + pcenter[1]*2
        max_x=int(max(dst[0,0],dst[1,0],dst[2,0],dst[3,0]))
        min_x=int(min(dst[0,0],dst[1,0],dst[2,0],dst[3,0]))
        max_y=int(max(dst[0,1],dst[1,1],dst[2,1],dst[3,1]))
        min_y=int(min(dst[0,1],dst[1,1],dst[2,1],dst[3,1]))
        warpR = cv2.getPerspectiveTransform(org, dst)
        result=cv2.warpPerspective(img,warpR,(w*2,h*2))
        w_pers=max_x-min_x
        h_pers=max_y-min_y
        padding=w_pers-h_pers
        if(padding>0):
            min_y-=padding/2
            max_y=max_y+padding/2+padding%2
        elif(padding<0):
            padding=-padding
            min_x-=padding/2
            max_x=max_x+padding/2+padding%2
        result=result[min_y:max_y,min_x:max_x]
        points = np.asarray(points, dtype=np.float32)
        points = np.array([points])
        points=cv2.perspectiveTransform(points,warpR)[0]
        for i in range(len(points)):
            points[i,0]-=min_x
            points[i,1]-=min_y
        return result,points
        

    '''def get_warpR(self,img,x_angle,y_angle,z_angle,fov=42):
        w,h=img.shape[0:2]
        z=np.sqrt(w**2+h**2)/2/np.tan(self.rad(fov/2))

        r_x=np.array([[1, 0, 0, 0],
                      [0, np.cos(self.rad(x_angle)), -np.sin(self.rad(x_angle)), 0],
                      [0, -np.sin(self.rad(x_angle)), np.cos(self.rad(x_angle)), 0, ],
                      [0, 0, 0, 1]], np.float32)
        r_y=np.array([[np.cos(self.rad(y_angle)), 0, np.sin(self.rad(y_angle)), 0],
                      [0, 1, 0, 0],
                      [-np.sin(self.rad(y_angle)), 0, np.cos(self.rad(y_angle)), 0, ],
                      [0, 0, 0, 1]], np.float32)
        r_z=np.array([[np.cos(self.rad(z_angle)), np.sin(self.rad(z_angle)), 0, 0],
                      [-np.sin(self.rad(z_angle)), np.cos(self.rad(z_angle)), 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]], np.float32)
        #r=r_x*r_y*r_z
        r=r_y
        pcenter = np.array([h / 2, w / 2, 0, 0], np.float32)

        p1 = np.array([0, 0, 0, 0], np.float32) - pcenter
        p2 = np.array([w, 0, 0, 0], np.float32) - pcenter
        p3 = np.array([0, h, 0, 0], np.float32) - pcenter
        p4 = np.array([w, h, 0, 0], np.float32) - pcenter

        dst1 = r.dot(p1)
        dst2 = r.dot(p2)
        dst3 = r.dot(p3)
        dst4 = r.dot(p4)

        list_dst = [dst1, dst2, dst3, dst4]

        org = np.array([[0, 0],
                        [w, 0],
                        [0, h],
                        [w, h]], np.float32)

        dst = np.zeros((4, 2), np.float32)

        # 投影至成像平面
        for i in range(4):
            dst[i, 0] = list_dst[i][0] * z / (z - list_dst[i][2]) + pcenter[0]
            dst[i, 1] = list_dst[i][1] * z / (z - list_dst[i][2]) + pcenter[1]
        warpR = cv2.getPerspectiveTransform(org, dst)
        return warpR

    def transform_rot(self,img,points):
        h,w=img.shape[0:2]
        x_angle=np.random.randint(-self.x_angle,self.x_angle+1)
        y_angle=np.random.randint(-self.y_angle,self.y_angle+1)
        z_angle=np.random.randint(-self.z_angle,self.z_angle+1)
        x_angle=50
        y_angle=50
        z_angle=0
        points=np.asarray(points,dtype=np.float32)
        points=np.array([points])
        warpR=self.get_warpR(img,x_angle,y_angle,z_angle)
        result=cv2.warpPerspective(img,warpR,(w,h))
        dst=cv2.perspectiveTransform(points,warpR)[0]
        cv2.imwrite('c.jpg',result)
        top=int(floor(max(min(dst[0][0],dst[1][0],dst[2][0],dst[3][0]),0)))
        bot=int(ceil(min(max(dst[0][0],dst[1][0],dst[2][0],dst[3][0]),w)))
        left=int(floor(max(min(dst[0][1],dst[1][1],dst[2][1],dst[3][1]),0)))
        right=int(ceil(min(max(dst[0][1],dst[1][1],dst[2][1],dst[3][1]),h)))
        result=result[left:right,top:bot]
        height,width=result.shape[0:2]
        points=[[0,0],[width,0],[0,height],[width,height]]
        return result,points

    def transform_pers(self,img,points):
        angle=np.random.randint(-self.pers_angle,self.pers_angle+1)
        height,width=img.shape[0:2]
        pointset1=np.array([[0,0],[width,0],[0,height],[width,height]],dtype='float32')
        if(angle>0):
            pointset2=np.array([[0,0],[width,0],[height*tan((float(angle)/180) * 3.14),height],[width+height*tan((float(angle)/180) * 3.14),height]],dtype='float32')
        elif(angle<0):
            angle=-angle
            pointset2=np.array([[height*tan((float(angle)/180) * 3.14),0],[height*tan((float(angle)/180)* 3.14)+width,0],[0,height],[width,height]],dtype='float32')
        else:
            pointset2=np.array([[0,0],[width,0],[0,height],[width,height]],dtype='float32')
        matrix=cv2.getPerspectiveTransform(pointset1,pointset2)
        points = np.asarray(points, dtype=np.float32)
        points = np.array([points])
        dst = cv2.perspectiveTransform(points, matrix)[0]
        img_temp=np.array(img)
        result = cv2.warpPerspective(img_temp,matrix,(width,height))
        return result,dst'''
