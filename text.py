#coding:utf-8

import os
import random
from config import config_deal

class text_deal(config_deal):
    def __init__(self):
        config_deal.__init__(self)
        self.corups=[]
    #载入语料文件
    def loadcorups(self):
        for files in os.listdir(self.corups_path):
            with open(os.path.join(self.corups_path,files)) as f:
                data=f.read().decode('utf-8')
            dataline=[]
            for line in data.split(u'\n'):
                #滤除一些无意义的符号
                line=line.strip()
                line=line.replace('\u3000','')
                line=line.replace('&nbsp', '')
                line=line.replace('\00', '')
                if(line!=u'' and len(line)>1):
                    dataline.append(line)
            #将一个文件的所有文字连接为一行
            wholeline=''.join(dataline)
            self.corups.append(wholeline)
    
    #从语料中选取word
    def get_sample_fromcorups(self):
        #防止重复导入
        if(self.corups==[]):
            self.loadcorups()
        #随机选取一个文件
        line=random.choice(self.corups)
        #每个文件的文字被拉成了一行，随机从行中选取固定长度的文字
        start=random.randint(0,len(line)-self.char_length)
        word=line[start:start+self.char_length]
        #对选取的文字进行迭代判断
        word_filter=''
        for i,char in enumerate(word):
            char_temp=char
            #不做数据均衡
            if(not self.is_balanced):
                #如果字符不在字典中，那么从字典中任意选一个进行替换
                if(char not in self.dict):
                    char_temp=random.choice(self.dict)
            #做数据均衡
            else:
                #如果为英文模式，则数据平衡只考虑字母，忽略符号
                if(self.text_mode=='english'):
                    if(char not in self.dict):
                        #如果字符不在字典中，则从标点中随机选取进行替换
                        char_temp=random.choice(self.dict_biaodian)
                    if(char in self.dict_alpha):
                        #得到该字符对应字典中的序号
                        dict_index=self.dict_alpha.index(char_temp)
                        #如果该字符出现的次数大于了最大出现次数，则需要进行替换
                        if(self.frequency[dict_index]>self.max_frequency):
                            #先把字符进行大小写更改
                            char_temp=char_temp.swapcase()
                            dict_index=self.dict_alpha.index(char_temp)
                            #如果更改了大小写后，字符出现的次数仍然大于最大次数，则选取出现次数最少的进行替换
                            if(self.frequency[dict_index]>self.max_frequency):
                                dict_index=self.frequency.index(min(self.frequency))
                                char_temp=self.dict_alpha[dict_index]
                        self.frequency[dict_index]+=1
                #如果为中文模式，则数据平衡考虑字典中的所有元素，包括汉字、字母、数字、符号
                else:
                    if(char not in self.dict):
                        #如果字符不在字典中，则从整个字典中随机选取一个进行替换
                        char_temp=random.choice(self.dict)
                    dict_index=self.dict.index(char_temp)
                    if(self.frequency[dict_index]>self.max_frequency):
                        dict_index=self.frequency.index(min(self.frequency))
                        char_temp=self.dict[dict_index]
                    self.frequency[dict_index]+=1
            word_filter+=char_temp
        return word_filter

    #从dict中选取word  
    def get_sample_fromdict(self):
        word=''
        #如果是英文，直接从dict随机选取的话会造成标点占比过大
        if(self.text_mode=='english'):
            #随机选取两个位置作为符号（标点和空白）位置，两个位置不连续，且不出现在行首和行尾
            special_loc_1=random.randint(1,self.char_length-4)
            special_loc_2=random.randint(special_loc_1+2,self.char_length-2)
            #符号位置以外的位置都用字母填充
            for _ in range(special_loc_1):
                temp=random.choice(self.dict_alpha)
                word+=temp
            #按照常识，符号位置百分之八十的概率为空格，百分之十为标点符号，剩余百分之十以字母填充
            flag_1=random.randint(0,100)
            if(flag_1<80):
                word+=' '
            elif(flag_1<90):
                temp=random.choice(self.dict_biaodian)
                word+=temp
            else:
                temp=random.choice(self.dict_alpha)
                word+=temp
            for _ in range(special_loc_1+1,special_loc_2):
                temp=random.choice(self.dict_alpha)
                word+=temp
            #按照常识，符号位置百分之八十的概率为空格，百分之十为标点符号，剩余百分之十以字母填充
            flag_2=random.randint(0,100)
            if(flag_2<80):
                word+=' '
            elif(flag_2<90):
                temp=random.choice(self.dict_biaodian)
                word+=temp
            else:
                temp=random.choice(self.dict_alpha)           
                word+=temp
            for _ in range(special_loc_2+1,self.char_length):
                temp=random.choice(self.dict_alpha)
                word+=temp
        #如果为中文，则直接从字典中选取即可
        else:
            for i in range(self.char_length):
                temp=random.choice(self.dict)
                #保证行首和行尾不是空格
                if(i==0 or i==self.char_length-1):
                    while(temp==' '):
                        temp=random.choice(self.dict)
                word+=temp
        return word

    #提取语料主函数
    def get_sample(self):
        if(self.is_sample_from_corpus):
            word=self.get_sample_fromcorups()
            #避免行首和行尾出现空格，以免和留白混淆
            while(word[0]==' ' or word[self.char_length-1]==' '):
                #若出现行首行尾为空格，则重新选取text，并把放弃的字符对应的频率表更新
                for char in word:
                    #中文对应的是整个字典
                    if(self.text_mode=='chinese'):
                        char_index=self.dict.index(char)
                        self.frequency[char_index]-=1
                    #英文只对应字母字典
                    else:
                        if(char in self.dict_alpha):
                            char_index=self.dict_alpha.index(char)
                            self.frequency[char_index]-=1
                word=self.get_sample_fromcorups()
        else:
            #因为是从字典随机选取，默认是比较均衡的数据
            word=self.get_sample_fromdict()
        return word
