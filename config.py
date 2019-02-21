#coding:utf-8

import os
import numpy as np

class config_deal(object):
    def __init__(self):
        self.text_mode_list=['english','chinese']
        self.sample_mode_list=['dict','corups']
        self.char_gap_mode_list=['space','fixed_distance','random_distance']
        
        #text_mode:'english' or 'chinese',设置语料是中文还是英文 
        self.text_mode=self.text_mode_list[1]
        #sample_mode: 'corups' or 'dict','corups' 表示从语料文件中选取word，dict表示直接从dict里面随机选取组成word
        self.sample_mode=self.sample_mode_list[0]
        #char_gap_mode: 'space' or 'random_distance',random_distance表示字符之间的间距随机，space表示字符之间间距固定且需要检测空格符号
        self.char_gap_mode=self.char_gap_mode_list[1]

        #语料文件夹路径
        self.corups_path='corups'
        #字典路径
        self.dict_path='dic_chiandeng.txt'
        #背景图像路径
        self.back_path='backimg'
        #字体路径
        self.font_path='fonts_chinese'
        #图像保存路径
        self.save_pic_path='1'
        #图像label保存路径
        self.save_word_path='word.txt'
        #训练集label list
        self.train_label_path='label_train.txt'
        #验证集label_list
        self.val_label_path='label_val.txt'
        #背景图像list
        self.bg_list=os.listdir(self.back_path)
        #字体list
        self.font_list=os.listdir(self.font_path)
        #读取字典
        dic_file=open(self.dict_path,'r')
        self.dic=[ch.strip('\n').decode('utf-8') for ch in dic_file.readlines()]
        #词频率统计
        self.frequency=np.zeros(len(self.dic),dtype=np.uint8)
        self.frequency=list(self.frequency)
        #
        if(self.text_mode=='english'):
            self.dic_alpha_path='dic_alpha.txt'
            dic_file=open(self.dic_alpha_path,'r')
            self.dic_alpha=[ch.strip('\n').decode('utf-8') for ch in dic_file.readlines()]
            self.dic_biaodian_path='dic_biaodian.txt'
            dic_file=open(self.dic_biaodian_path,'r')
            self.dic_biaodian=[ch.strip('\n').decode('utf-8') for ch in dic_file.readlines()]
            self.frequency=np.zeros(len(self.dic_alpha),dtype=np.uint8)
            self.frequency=list(self.frequency)

           
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
        #验证集数量
        self.valset_num=10000
        
        #使用图像作为背景的比例（0表示全部用随机背景，1表示全部用图像作为背景）
        self.ratio_genback_pic=1.00 
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

        
        

