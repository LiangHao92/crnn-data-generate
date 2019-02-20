#coding:utf-8

import os

class config_deal(object):
    def __init__(self):
        self.text_mode_list=['english','chinese']
        self.sample_mode_list=['dict','corups']
        self.char_gap_mode_list=['space','random_distance']
        
        #text_mode:'english' or 'chinese',show the language used in corrups 
        self.text_mode=self.text_mode_list[0]
        #sample_mode: 'corups' or 'dict','corups' means get the char from text in corups,'dict' means get the char randomly in dict
        self.sample_mode=self.sample_mode_list[1]
        #char_gap_mode: 'space' or 'random_distance',random_distance means the dis between two char is random
        self.char_gap_mode=self.char_gap_mode_list[0]

        self.corups_path='corups_english'
        self.dict_path='dic_chiandeng.txt'
        self.back_path='backimg'
        self.font_path='fonts_hanyi'
        self.save_pic_path='1'
        self.save_label_path='label.txt'
        self.bg_list=os.listdir(self.back_path)
        self.font_list=os.listdir(self.font_path)
        
        self.char_length=10
        self.max_x_angle=50
        self.max_y_angle=50
        self.max_z_angle=8
        #self.pers_angle=0
        self.width=1000
        self.height=1000
        #self.x_start=100
        #self.x_end=500
        #self.y_start=100
        #self.y_end=900
        self.min_font_size=20
        self.max_font_size=50
        self.quality_lower=40
        self.quality_upper=80
        

        self.ratio_genback_pic=1.00 #ratio of generating backgroud using pic:0~1
        self.ratio_rotate_x=0.80
        self.ratio_rotate_y=0.80
        self.ratio_reverse_color=0.50
        self.ratio_blur=0.50
        self.ratio_noise=0.50
        self.ratio_lowquality_pic=0.20
        
        

