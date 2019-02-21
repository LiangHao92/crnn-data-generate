#coding:utf-8

import cv2
from PIL import Image,ImageFont,ImageDraw
import random
import os
import numpy as np
from config import config_deal
from math import *



class draw_deal(config_deal):
    def __init__(self):
        config_deal.__init__(self)

    #高斯模糊图像
    def gauss_blur(self,img, ks=None):
        if ks is None:
            ks = [7, 9, 11, 13]
        ksize = random.choice(ks)
        sigmas = [0, 1, 2, 3, 4, 5, 6, 7]
        sigma = 0
        if ksize <= 3:
            sigma = random.choice(sigmas)
        img = cv2.GaussianBlur(img, (ksize, ksize), sigma)
        return img

    #随机生成背景
    def genback_rand(self):
        bg_high=random.uniform(60,255)
        bg_low=bg_high-random.uniform(1,60)
        bg=np.random.randint(bg_low,bg_high,(self.height,self.width)).astype(np.uint8)
        bg=self.gauss_blur(bg)
        return bg

    #选取图片作为背景
    def genback_pic(self):
        bg_name=random.choice(self.bg_list)
        bg_path=os.path.join(self.back_path,bg_name)
        bg_img=cv2.imread(bg_path)
        bg_img=cv2.resize(bg_img,(self.width,self.height))
        return bg_img
    
    #生成背景图像
    def genback(self):
        if(random.randint(0,10)>self.ratio_genback_pic*10):
            return self.genback_rand()
        else:
            return self.genback_pic()

    #选择字体
    def choose_font(self):
        font_size=random.randint(self.min_font_size,self.max_font_size)
        font_name=random.choice(self.font_list)
        font_name=os.path.join(self.font_path,font_name)
        font_use=ImageFont.truetype(font_name,font_size)
        #space is too wide, so use the smaller size of space 
        #ratio=random.randint(50,70)
        '''ratio=100
        print ratio,font_name
        font_space=ImageFont.truetype(font_name,font_size*ratio/100)
        return font_use,font_space,font_size'''
        return font_use,font_size

    #根据roi的颜色均值，选取字体的颜色
    def choose_textcolor(self,roi):
        bg_mean=int((roi.mean())+128)%256
        #保证颜色取值不越过255
        if(bg_mean>245):
            if(random.randint(0,2)<2):
                word_color_1=random.randint((bg_mean-10),255)
                word_color_2=random.randint((bg_mean-10),255)
                word_color_3=random.randint((bg_mean-10),255)
            else:
                word_color_1=random.randint(0,(bg_mean+10)%256)
                word_color_2=random.randint(0,(bg_mean+10)%256)
                word_color_3=random.randint(0,(bg_mean+10)%256)
        elif(bg_mean<10):
            if(random.randint(0,2)<2):
                word_color_1=random.randint(0,bg_mean+10)
                word_color_2=random.randint(0,bg_mean+10)
                word_color_3=random.randint(0,bg_mean+10)
            else:
                word_color_1=random.randint((bg_mean-10)%256,255)
                word_color_2=random.randint((bg_mean-10)%256,255)
                word_color_3=random.randint((bg_mean-10)%256,255)
        else:
            word_color_1=random.randint((bg_mean-10),(bg_mean+10))
            word_color_2=random.randint((bg_mean-10),(bg_mean+10))
            word_color_3=random.randint((bg_mean-10),(bg_mean+10))
        word_color=(word_color_1,word_color_2,word_color_3)
        #print roi.mean(),word_color
        return word_color

    #在背景图上画出字符
    def drawtext(self,word):
        bg=self.genback()
        bg_image=Image.fromarray(np.uint8(bg))
        #font_use,font_space,font_size=self.choose_font()
        font_use,font_size=self.choose_font()
        drawer=ImageDraw.Draw(bg_image)
        #末尾留够空间，以免字符越界
        #x_start,y_start为字符区域的左上角坐标
        x_start=random.randint(0,self.width-font_size*15)
        y_start=random.randint(0,self.height-font_size*2)
        #x_start,y_start为字符区域的右下角坐标
        y_end=y_start
        x_end=x_start
        #记录所有字符的最大高度
        height=0
        #y_offset表示所有字符在高度上最小的offset
        y_offset=10**5
        #char_dis记录两个字符之间的距离
        char_dis=[]
        #遍历各个字符，确定各个字符在图中的位置以及所有字符的最大高度和最小offset 
        for i,char in enumerate(word):
            '''if(char==' '):
                size=font_space.getsize(char)
            else:
                size=font_use.getsize(char)
                char_offset=font_use.getoffset(char)
                #print char_offset
                if(y_offset>char_offset[1]):
                    y_offset=char_offset[1]'''
            size=font_use.getsize(char)
            char_offset=font_use.getoffset(char)
            if(y_offset>char_offset[1]):
                y_offset=char_offset[1]
            if(height<size[1]):
                height=size[1]
            if(self.char_gap_mode=='random_distance'):
                if(random.randint(0,100)<95):
                    char_space=0
                else:
                    if(i==len(word)-1):
                        char_space=0
                    else:
                        char_space=int(height*np.random.uniform(0,1.0))
            elif(self.char_gap_mode=='space'):
                char_space=0
            else:
                char_space=0
            char_dis.append(size[0]+char_space)
            x_end=x_end+size[0]+char_space
        y_start=max(0,y_start-y_offset)
        y_end=y_start+height
        #取文字区域
        roi=bg[y_start:y_end,x_start:x_end]
        #根据文字区域的颜色均值，确定字符颜色
        color=self.choose_textcolor(roi)
        #保证char_dis的size和word一样
        char_dis.append(0)
        #循环迭代在图像画字符
        char_x=x_start
        char_y=y_start
        for i,char in enumerate(word):
            '''if(char==' '):
                drawer.text((char_x,char_y),char,fill=color,font=font_space)
            else:
                drawer.text((char_x,char_y),char,fill=color,font=font_use)'''
            drawer.text((char_x,char_y),char,fill=color,font=font_use)
            char_x+=char_dis[i]
        #画上了字符的图像
        img=np.array(bg_image,dtype=np.uint8)
        #字符区域的四个顶点坐标
        cord=[[x_start,y_start],[x_start,y_end],[x_end,y_end],[x_end,y_start]]
        return img,cord

    #反转图像颜色（白底黑字变成黑底白字）
    def reverse(self,img):
        offset=np.random.randint(-10,10)
        result=255+offset-img
        np.clip(result,0.,255.)
        return 255+offset-img
    
    #截取roi
    def croproi(self,img,points):
        h,w=img.shape[0:2]
        top=int(floor(max(min(points[0][0],points[1][0],points[2][0],points[3][0]),0)))
        bot=int(ceil(min(max(points[0][0],points[1][0],points[2][0],points[3][0]),w)))
        left=int(floor(max(min(points[0][1],points[1][1],points[2][1],points[3][1]),0)))
        right=int(ceil(min(max(points[0][1],points[1][1],points[2][1],points[3][1]),h)))
        result=img[left:right,top:bot]
        height,width=result.shape[0:2]
        points=[[0,0],[width,0],[0,height],[width,height]]
        return result,points

                   


