#coding:utf-8

import cv2
import numpy as np
from math import *
from config import config_deal


class transform_deal(config_deal):
    def __init__(self):
        config_deal.__init__(self)
    
    #弧度角度切换
    def rad(self,x):
        return x*np.pi/180

    #绕坐标轴对图像进行旋转
    def trans(self,img,points,angle,flag,fov=42):
        w,h=img.shape[0:2]
        z=np.sqrt(w**2+h**2)/2/np.tan(self.rad(fov/2))
        #绕各个坐标轴不同的变换矩阵
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
        #变换过程中，原点由左上角变为图像中心点
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
        #为保证囊括原图的所有部分，将图像尺寸变换为原图的两倍，所以pcenter需要乘以2
        for i in range(4):
            dst[i, 0] = list_dst[i][0] * z / (z - list_dst[i][2]) + pcenter[0]*2
            dst[i, 1] = list_dst[i][1] * z / (z - list_dst[i][2]) + pcenter[1]*2
        #取得变换后坐标的取值范围
        max_x=int(max(dst[0,0],dst[1,0],dst[2,0],dst[3,0]))
        min_x=int(min(dst[0,0],dst[1,0],dst[2,0],dst[3,0]))
        max_y=int(max(dst[0,1],dst[1,1],dst[2,1],dst[3,1]))
        min_y=int(min(dst[0,1],dst[1,1],dst[2,1],dst[3,1]))
        #计算得到变换矩阵
        warpR = cv2.getPerspectiveTransform(org, dst)
        #根据变换矩阵对图像进行计算，长宽均为原图的2倍
        result=cv2.warpPerspective(img,warpR,(w*2,h*2))
        #原图变换后的真实宽高（正方形图像变换后会变为提醒，变换后图像会做padding将梯形补成矩形，真实宽高为梯形在x和y轴上的取值范围）
        w_pers=max_x-min_x
        h_pers=max_y-min_y
        #将梯形pandding为其最小的外接正方形
        padding=w_pers-h_pers
        if(padding>0):
            min_y-=padding/2
            max_y=max_y+padding/2+padding%2
        elif(padding<0):
            padding=-padding
            min_x-=padding/2
            max_x=max_x+padding/2+padding%2
        #截取此正方形
        result=result[min_y:max_y,min_x:max_x]
        points = np.asarray(points, dtype=np.float32)
        points = np.array([points])
        #对文字区域的四顶点坐标做变换
        points=cv2.perspectiveTransform(points,warpR)[0]
        #因为对变换后的图像做了截取，所以相应的坐标进行改变
        for i in range(len(points)):
            points[i,0]-=min_x
            points[i,1]-=min_y
        return result,points
 
