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

    #generate the background randomly
    def genback_rand(self):
        bg_high=random.uniform(60,255)
        bg_low=bg_high-random.uniform(1,60)
        bg=np.random.randint(bg_low,bg_high,(self.height,self.width)).astype(np.uint8)
        bg=self.gauss_blur(bg)
        return bg

    #choose the background pic from the folder
    def genback_pic(self):
        bg_name=random.choice(self.bg_list)
        bg_path=os.path.join(self.back_path,bg_name)
        bg_img=cv2.imread(bg_path)
        bg_img=cv2.resize(bg_img,(self.width,self.height))
        return bg_img
    
    #generate the background
    def genback(self):
        if(random.randint(0,10)>self.ratio_genback_pic*10):
            return self.genback_rand()
        else:
            return self.genback_pic()

    #choose the font
    def choose_font(self):
        font_size=random.randint(self.min_font_size,self.max_font_size)
        font_name=random.choice(self.font_list)
        font_name=os.path.join(self.font_path,font_name)
        font_use=ImageFont.truetype(font_name,font_size)
        #space is too wide, so use the smaller size of space 
        #ratio=random.randint(50,70)
        ratio=100
        print ratio,font_name
        font_space=ImageFont.truetype(font_name,font_size*ratio/100)
        return font_use,font_space,font_size

    #decide the color of the text
    def choose_textcolor(self,roi):
        bg_mean=int((roi.mean())+128)%256
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

    #draw the text
    def drawtext(self,word):
        bg=self.genback()
        bg_image=Image.fromarray(np.uint8(bg))
        font_use,font_space,font_size=self.choose_font()
        drawer=ImageDraw.Draw(bg_image)
        #leave the certain distance to avoid text get out of the range of pic size
        #x_start,y_start is the left_top corner of text
        '''x_start=random.randint(self.x_start,self.x_end)
        y_start=random.randint(self.y_start,self.y_end)'''
        x_start=random.randint(0,self.width-font_size*15)
        y_start=random.randint(0,self.height-font_size*2)
        #x_start,y_start is the right_bottom corner of text
        y_end=y_start
        x_end=x_start
        #height is height of the highest char
        height=0
        #y_offset is the min offset of all the char
        y_offset=10**5
        #char_dis is the dis between two char
        char_dis=[]
        #decide the loc of every char, and get the height of pic 
        for i,char in enumerate(word):
            if(char==' '):
                size=font_space.getsize(char)
            else:
                size=font_use.getsize(char)
                char_offset=font_use.getoffset(char)
                #print char_offset
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
                print 'drawtext: char_gap_model is wrong'
            char_dis.append(size[0]+char_space)
            x_end=x_end+size[0]+char_space
        #y_start-=y_offset
        y_start=max(0,y_start-y_offset)
        y_end=y_start+height
        roi=bg[y_start:y_end,x_start:x_end]
        #print  y_start,y_end,x_start,x_end
        color=self.choose_textcolor(roi)
        char_dis.append(0)
        #draw the text
        char_x=x_start
        char_y=y_start
        for i,char in enumerate(word):
            if(char==' '):
                drawer.text((char_x,char_y),char,fill=color,font=font_space)
            else:
                drawer.text((char_x,char_y),char,fill=color,font=font_use)
            char_x+=char_dis[i]
        img=np.array(bg_image,dtype=np.uint8)
        cord=[[x_start,y_start],[x_start,y_end],[x_end,y_end],[x_end,y_start]]
        return img,cord

    #reverse the pic(make the color of text change to white from black)
    def reverse(self,img):
        offset=np.random.randint(-10,10)
        result=255+offset-img
        np.clip(result,0.,255.)
        return 255+offset-img

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

                   


