#coding:utf-8

from generate import generate_image


a=generate_image(100)
a.check_font()
a.generate()
a.reset_config(text_mode='chinese',picnum=100,is_sample_from_corpus=False,dict_path='dic_num.txt')
a.generate()

#a=generate_image(0)
#a.check_font()
