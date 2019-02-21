#coding:utf-8

from draw import draw_deal
from text import text_deal
from transform import transform_deal
import config
import cv2
import random
import noise
import os
import math
import numpy as np


class generate_image(draw_deal,text_deal,transform_deal):
    def __init__(self,picnum):
        draw_deal.__init__(self)
        text_deal.__init__(self)
        transform_deal.__init__(self)
        self.index=0
        self.picnum=picnum
        self.isblured=False
        if(self.text_mode=='english'):
            self.max_frequency=int(self.picnum*self.char_length/len(self.dic_alpha))
        else:   
            self.max_frequency=np.ceil(1.1*self.picnum*self.char_length/len(self.dic))
            #print self.max_frequency

    def reset_config(self,picnum=None,text_mode=None,sample_mode=None,corups_path=None,dict_path=None,font_path=None):
        if(picnum!=None):
            self.picnum=self.index+picnum
            self.max_frequency=np.ceil(picnum*self.char_length/len(self.dic)*1.1)
        if(text_mode!=None):
            self.text_mode=self.text_mode_list[text_mode]
            if(self.text_mode=='english'):
                self.dic_alpha_path='dic_alpha.txt'
                dic_file=open(self.dic_alpha_path,'r')
                self.dic_alpha=[ch.strip('\n').decode('utf-8') for ch in dic_file.readlines()]
                self.dic_biaodian_path='dic_biaodian.txt'
                dic_file=open(self.dic_biaodian_path,'r')
                self.dic_biaodian=[ch.strip('\n').decode('utf-8') for ch in dic_file.readlines()]
        if(sample_mode!=None):
            self.sample_mode=self.sample_mode_list[sample_mode]
        if(corups_path!=None):
            self.corups_path=corups_path
            self.corups=[]
            self.loadcorups()
        if(dict_path!=None):
            self.dict_path=dict_path
            if(self.text_mode=='english'):
                self.frequency=np.zeros(len(self.dic_alpha),dtype=np.uint8)
                self.frequency=list(self.frequency)
                self.max_frequency=int(picnum*self.char_length/len(self.dic_alpha))
            else:
                self.frequency=np.zeros(len(self.dic),dtype=np.uint8)
                self.frequency=list(self.frequency)
                self.max_frequency=np.ceil(1.1*picnum*self.char_length/len(self.dic))
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
        wordtxt=open(self.save_word_path,'a')
        word=word.encode('utf-8')
        wordtxt.write(str(self.index)+'.jpg '+word+'\n')

    def generate_trainandval_list(self):
        wordfile=open(self.save_word_path,'r')
        train_list=open(self.train_label_path,'w')
        val_list=open(self.val_label_path,'w')
        wordlist=wordfile.readlines()
        random.shuffle(wordlist)
        i=0
        for line in wordlist:
            line=line.strip('\n')
            line_list=line.split('.jpg')
            text=line_list[0]+'.jpg'
            labelstr=line_list[1][1:]
            labelstr=unicode(labelstr,'utf-8')
            for label in labelstr:
                index=self.dic.index(label)
                text=text+' '+str(index)
            if(i<self.valset_num):
                val_list.write(text+'\n')
            else:
                train_list.write(text+'\n')
            i+=1
        wordfile.close()
        train_list.close()
        val_list.close()
        

    def generate_onepic(self):
        word=self.get_sample()
        img,points=self.drawtext(word)
        if(random.randint(0,100)<self.ratio_rotate_x*100):
            angle_x=random.randint(-self.max_x_angle,self.max_x_angle+1)
            img,points=self.trans(img,points,angle_x,'x')
        if(random.randint(0,100)<self.ratio_rotate_y*100):
            angle_y=random.randint(self.max_y_angle,self.max_y_angle+1)
            img,points=self.trans(img,points,angle_y,'y')
        angle_z=(math.atan((points[3][1]-points[0][1])/(points[3][0]-points[0][0])))/np.pi*180
        #print angle_z
        if(angle_z>self.max_z_angle or angle_z<-self.max_z_angle ):
            img,points=self.trans(img,points,angle_z,'z')
        img,points=self.croproi(img,points)
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
    
    def generate(self):
        while(self.index<self.picnum):
            self.generate_onepic()
        

a=generate_image(1000)
a.generate()
#a.generate_trainandval_list()
a.reset_config(text_mode=0,picnum=1000,corups_path='corups_english',dict_path='dic_english.txt')
a.generate()
