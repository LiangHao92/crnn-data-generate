#coding:utf-8

import draw
import text
import transform
import config
import cv2
import random
import noise
import os
import math
import numpy as np


class generate_image(config.config_deal):
    def __init__(self,picnum):
        config.config_deal.__init__(self)
        self.text_deal=text.text_deal()
        self.transform_deal=transform.transform_deal()
        self.draw_deal=draw.draw_deal()
        self.index=0
        self.picnum=picnum
        self.isblured=False   

    def reset_config(self,picnum=None,text_mode=None,sample_mode=None,corups_path=None,dict_path=None,font_path=None):
        if(picnum!=None):
            self.picnum=self.index+picnum
        if(text_mode!=None):
            self.text_mode=self.text_mode_list[text_mode]
        if(sample_mode!=None):
            self.sample_mode=self.sample_mode_list[sample_mode]
        if(corups_path!=None):
            self.corups_path=corups_path
        if(dict_path!=None):
            self.dict_path=dict_path
        if(font_path!=None):
            self.font_path=font_path
            self.font_list=os.listdir(self.font_path)
        

    def resize_img(self,img):
        height,width=img.shape
        ratio=float(1.0*32/height)
        width=int(ratio*width)
        if(width>256):
            img=cv2.resize(img,(256,32))
        else:
            img=cv2.resize(img,(width,32))
            a=random.randint(0,256-width)
            img=cv2.copyMakeBorder(img,0,0,a,256-width-a,cv2.BORDER_CONSTANT,value=0)
        return img
    
    def save_result(self,img,word):
        if(random.randint(0,100)<self.ratio_lowquality_pic*100 and self.isblured==False):
            quality=random.randint(self.quality_lower,self.quality_upper)
            cv2.imwrite(os.path.join(self.save_pic_path,str(self.index)+'.jpg'),img,[int(cv2.IMWRITE_JPEG_QUALITY),quality])
        else:
            cv2.imwrite(os.path.join(self.save_pic_path,str(self.index)+'.jpg'),img)
        self.isblured=False
        self.index+=1
        labeltxt=open(self.save_label_path,'a')
        word=word.encode('utf-8')
        labeltxt.write(str(self.index)+'.jpg '+word+'\n')

    def generate_onepic(self):
        print self.index
        word=self.text_deal.get_sample()
        img,points=self.draw_deal.drawtext(word)
        if(random.randint(0,100)<self.ratio_rotate_x*100):
            angle_x=random.randint(-self.max_x_angle,self.max_x_angle+1)
            img,points=self.transform_deal.trans(img,points,angle_x,'x')
        if(random.randint(0,100)<self.ratio_rotate_y*100):
            angle_y=random.randint(self.max_y_angle,self.max_y_angle+1)
            img,points=self.transform_deal.trans(img,points,angle_y,'y')
        angle_z=(math.atan((points[3][1]-points[0][1])/(points[3][0]-points[0][0])))/np.pi*180
        #print angle_z
        if(angle_z>self.max_z_angle or angle_z<-self.max_z_angle ):
            img,points=self.transform_deal.trans(img,points,angle_z,'z')
        img,points=self.draw_deal.croproi(img,points)
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        '''if(random.randint(0,100)<self.ratio_reverse_color*100):
            img=self.draw_deal.reverse(img)'''
        if(random.randint(0,100)<self.ratio_blur*100):
            blur_flag=random.randint(0,2)
            img=noise.blurimg(img,blur_flag)
            self.isblured=True 
        if(random.randint(0,100)<self.ratio_noise*100):
            noise_flag=random.randint(0,4)
            img=noise.addnoise(img,noise_flag)  
        img=self.resize_img(img)
        self.save_result(img,word)
        #return img,word
    
    def generate(self):
        while(self.index<self.picnum):
            #print self.index
            self.generate_onepic()
        

a=generate_image(100)

a.generate()
#print word
#cv2.imwrite('a.jpg',img)