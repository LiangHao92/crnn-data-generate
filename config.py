#coding:utf-8

import os
import numpy as np
import random

class config_deal(object):
    def __init__(self):
        #选取text的模式：False表示从字典随机选取字符，True表示从语料文件中选取
        self.is_sample_from_corpus=True
        #是否在字符间使用随机间距
        self.is_random_distance=False
        #是否做数据均衡,如果从字典中随机选取字符，则不做数据均衡，数据均衡只针对从语料文件中选取text
        self.is_balanced=True 
        #text的语言：'english' or 'chinese'，'english'表示为英语格式，'chinese'表示为中文格式
        self.text_mode='english'
        #语料文件路径，若is_sample_from_corpus为False，即从字典选取字符，则可以忽视此项设置
        self.corups_path='corups_english'
        #字典路径
        self.dict_path='dic_english_wanzheng.txt'
        #背景图像路径
        self.back_path='backimg'
        #字体路径
        self.font_path='fonts_english'
        #图像保存路径
        #self.save_pic_path='/home/seven/ocr/training/gen_english_20190226'
	self.save_pic_path='1'
        #图像label保存路径
        self.save_word_path='word.txt'
        
        #char出现的次数上限
        self.max_frequency=0
        #每幅图像的字符长度
        self.char_length=10
        #图像绕x轴最大旋转角度
        self.max_x_angle=50
        #图像绕y轴最大旋转角度
        self.max_y_angle=50
        #图像绕z轴最大旋转角度
        self.max_z_angle=8
        #背景图像初始的宽度
        self.width=1000
        #背景图像初始高度
        self.height=1000
        #字体最小尺寸
        self.min_font_size=20
        #字体最大尺寸
        self.max_font_size=50
        #低质量图像保存的质量下限
        self.quality_lower=40
        #低质量图像保存的质量上限
        self.quality_upper=80
        
        #将图像绕x轴旋转的概率
        self.ratio_rotate_x=0.80
        #将图像绕y轴旋转的概率
        self.ratio_rotate_y=0.80
        #将图像颜色反转的概率
        self.ratio_reverse_color=0.50
        #对图像进行模糊处理的概率
        self.ratio_blur=0.50
        #对图像进行加噪声处理的概率
        self.ratio_noise=0.50
        #对图像进行低质量保存的概率
        self.ratio_lowquality_pic=0.20

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
        

        
        
        



        

        
        

