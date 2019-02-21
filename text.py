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
                #filt the meaningless char
                line=line.strip()
                line=line.replace('\u3000','')
                line=line.replace('&nbsp', '')
                line=line.replace('\00', '')
                if(line!=u'' and len(line)>1):
                    dataline.append(line)
            wholeline=''.join(dataline)
            self.corups.append(wholeline)
    
    #从语料中选取word
    def get_sample_fromcorups(self):
        if(self.corups==[]):
            self.loadcorups()
        line=random.choice(self.corups)
        start=random.randint(0,len(line)-self.char_length)
        word=line[start:start+self.char_length]
        #print word
        word_filter=''
        for i,char in enumerate(word):
            #print char
            #char_temp=char.encode('utf-8')
            char_temp=char
            if(not char in self.dic):
                if(self.text_mode=='english'):
                    char_temp=random.choice(self.dic_biaodian)
                else:
                    char_temp=random.choice(self.dic)
            if(self.text_mode=='english'):
                if(char in self.dic_alpha):
                    dic_index=self.dic_alpha.index(char_temp)
                    if(self.frequency[dic_index]>self.max_frequency):
                        dic_index=self.frequency.index(min(self.frequency))
                        char_temp=self.dic_alpha[dic_index]
                        #print word,char_temp
                    self.frequency[dic_index]+=1
                word_filter+=char_temp
                print self.frequency
                
            else:
                dic_index=self.dic.index(char_temp)
                if(self.frequency[dic_index]>self.max_frequency):
                    dic_index=self.frequency.index(min(self.frequency))
                    char_temp=self.dic[dic_index]
                    #print word,char_temp
                word_filter+=char_temp
                self.frequency[dic_index]+=1
        #print word_filter
        return word_filter
    


    #从dict中选取word  
    def get_sample_fromdict(self):
        word=''
        if(self.text_mode=='english'):
            special_loc_1=random.randint(1,self.char_length-3)
            special_loc_2=random.randint(special_loc_1+2,self.char_length-1)
            for _ in range(special_loc_1):
                temp=random.choice(self.dic_alpha)
                word+=temp
            flag_1=random.randint(0,100)
            if(flag_1<80):
                word+=' '
            elif(flag_1<90):
                temp=random.choice(self.dic_biaodian)
                word+=temp
            else:
                temp=random.choice(self.dic_alpha)
                word+=temp
            for _ in range(special_loc_1+1,special_loc_2):
                temp=random.choice(self.dic_alpha)
                word+=temp
            flag_2=random.randint(0,100)
            if(flag_2<80):
                word+=' '
            elif(flag_2<90):
                temp=random.choice(self.dic_biaodian)
                word+=temp
            else:
                temp=random.choice(self.dic_alpha)           
                word+=temp
            for _ in range(special_loc_2+1,self.char_length):
                temp=random.choice(self.dic_alpha)
                word+=temp
        else:
            for _ in range(self.char_length):
                temp=random.choice(self.dic)
                word+=temp
        return word
        '''for _ in range(self.char_length):
            temp=random.choice(self.dic)
            word+=temp
        word=unicode(word,'utf-8')
        return word'''

    #提取语料主函数
    def get_sample(self):
        if(self.sample_mode=='corups'):
            word=self.get_sample_fromcorups()
            #因为中文语料中很少空格，所以如果为’chinese‘和’space‘需要手动添加空格
            if(self.sample_mode=='chinese' and self.char_gap_mode=='space'):
                is_add_space=random.randint(0,10)
                if(is_add_space<5):
                    #避免空格出现在行首行尾。以免和留白混淆
                    space_loc=random.randint(1,self.char_length-1)
                    word =word[:space_loc]+' '+word[space_loc:self.char_length-1]
            if(self.text_mode=='english'):
                while(word[0]==' ' or word[self.char_length-1]==' '):
                    #避免空格出现在行首行尾。以免和留白混淆
                    for char in word:
                        if(char in self.dic_alpha):
                            char_index=self.dic_alpha.index(char)
                            self.frequency[char_index]-=1
                    word=self.get_sample_fromcorups()
            return word
        elif(self.sample_mode=='dict'):
            word=self.get_sample_fromdict()
            if(self.char_gap_mode=='space'):
                while(word[0]==' ' or word[self.char_length-1]==' '):
                    #避免空格出现在行首行尾。以免和留白混淆
                    word=self.get_sample_fromdict()
            return word
        else:
            print 'sample mode is not defined'
            return ''