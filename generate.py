#coding:utf-8

from draw import draw_deal
from text import text_deal
from transform import transform_deal
import cv2
import random
import noise
import os
import math
import numpy as np
import illumination
import multiprocessing 
import time


class generate_image(draw_deal,text_deal,transform_deal):
    def __init__(self,picnum,index=0):
        draw_deal.__init__(self)
        text_deal.__init__(self)
        transform_deal.__init__(self)
        self.index=index
        self.picnum=picnum+index
        self.isblured=False
        if(self.text_mode=='english'):
            self.max_frequency=int(picnum*self.char_length/len(self.dict_alpha))
        else:   
            self.max_frequency=np.ceil(1.1*picnum*self.char_length/len(self.dict))


    def reset_config(self,picnum,is_sample_from_corpus=None,is_random_distance=None,is_balanced=None,text_mode=None,corups_path=None,dict_path=None,back_path=None,font_path=None):
        if(is_sample_from_corpus!=None):
            self.is_sample_from_corpus=is_sample_from_corpus
        if(is_random_distance!=None):
            self.is_random_distance=is_random_distance
        if(is_balanced!=None):
            self.is_balanced=is_balanced
        if(text_mode!=None):
            self.text_mode=text_mode
        if(corups_path!=None):
            self.corups_path=corups_path
        if(dict_path!=None):
            self.dict_path=dict_path
        if(back_path!=None):
            self.back_path=back_path
        if(font_path!=None):
            self.font_path=font_path

        #读取字典文件，并形成字典list
        temp_file=open(self.dict_path,'r')
        self.dict=[ch.strip('\n').decode('utf-8') for ch in temp_file.readlines()]
        #如果要做数据均衡需要有字符出现次数统计表
        if(self.is_balanced==True):
            #如果text的语言为english且要做数据均衡，则生成dict_alpha和dict_biaodian，因为英文字母的数量较少，如果和标点一起均衡，那么标点的数量将过多
            if(self.text_mode=='english'):
                self.dict_alpha=[]
                self.dict_biaodian=[]
                for char in self.dict:
                    if char.isalpha():
                        self.dict_alpha.append(char)
                    else:
                        self.dict_biaodian.append(char)
                random.shuffle(self.dict_alpha)
                random.shuffle(self.dict_biaodian)
                #因为只针对字母做数据均衡，所以重定义字频表，只统计字母
                self.frequency=np.zeros(len(self.dict_alpha),dtype=np.uint8)
                self.frequency=list(self.frequency)
            #中文的话直接统计整个字典中元素的出现频次
            else:
                #字符频率表，统计各个字符出现的次数
                self.frequency=np.zeros(len(self.dict),dtype=np.uint8)
                self.frequency=list(self.frequency)
        #背景图片list
        self.bg_list=os.listdir(self.back_path)
        #字体list
        self.font_list=os.listdir(self.font_path)
        #重置预料列表 
        self.corups=[]
        #更新picnum
        self.picnum=picnum+self.index
        #根据重设的值，重新确定字符出现的最大次数
        if(self.text_mode=='english'):
            self.max_frequency=int(picnum*self.char_length/len(self.dict_alpha))
        else:   
            self.max_frequency=np.ceil(1.1*picnum*self.char_length/len(self.dict))


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
    
        wordtxt=open(self.save_word_path,'a')
        word=word.encode('utf-8')
        wordtxt.write(str(self.index)+'.jpg '+word+'\n')
        self.index+=1

    
    def generate_onepic(self):
        #选取word用于生成字符图像
        word=self.get_sample()
        #将word在背景图上画出来
        img,points=self.drawtext(word)
        #按一定的概率将图像绕x轴旋转设定范围内任意度数
        if(random.randint(0,100)<self.ratio_rotate_x*100):
            angle_x=random.randint(-self.max_x_angle,self.max_x_angle+1)
            img,points=self.trans(img,points,angle_x,'x')
        #按一定的概率将图像绕y轴旋转设定范围内任意度数
        if(random.randint(0,100)<self.ratio_rotate_y*100):
            angle_y=random.randint(self.max_y_angle,self.max_y_angle+1)
            img,points=self.trans(img,points,angle_y,'y')
        #绕x和y轴转动后，文字可能在水平方向上出现倾斜，求其倾斜的角度
        angle_z=(math.atan((points[3][1]-points[0][1])/(points[3][0]-points[0][0])))/np.pi*180
        #如果倾斜角度过大，则将文字行旋转回水平正方向，即不让其旋转角度过大
        if(angle_z>self.max_z_angle or angle_z<-self.max_z_angle ):
            img,points=self.trans(img,points,angle_z,'z')
        #从整个图像中crop下文字区域
        img,points=self.croproi(img,points)
        #在hsv颜色空间下做变换以模拟光照亮度的变化
        img=illumination.change_illum(img)
        #将图像转化为灰度图
        img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #按照一定的概率将图像颜色反转，即白底黑字变为黑底白字
        if(random.randint(0,100)<self.ratio_reverse_color*100):
            img=self.reverse(img)
        #以一定的概率对图像做模糊，如果做了模糊则不做之后的低质量图像保存，以免字符肉眼不可分辨
        if(random.randint(0,100)<self.ratio_blur*100):
            blur_flag=random.randint(0,2)
            img=noise.blurimg(img,blur_flag)
            self.isblured=True 
        #以一定的概率对图像加噪声
        if(random.randint(0,100)<self.ratio_noise*100):
            noise_flag=random.randint(0,4)
            img=noise.addnoise(img,noise_flag)
        #将图像按比例resize到固定的高度  
        img=self.resize_img(img)
        #保存图像和对应的label
        self.save_result(img,word)
    
    def generate(self):
        time_start=time.time()
        while(self.index<self.picnum):
            if(self.index%5000==0):
                print self.index,time.time()-time_start
                time_start=time.time()
            self.generate_onepic()
        


