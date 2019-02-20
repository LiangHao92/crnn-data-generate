#coding:utf-8

import os
import random
from config import config_deal

class text_deal(config_deal):
    def __init__(self):
        config_deal.__init__(self)
        self.corups=[]
        self.dic=[]
    #loading the corups
    ##corups_path is a folder which has many files, everyfile is  exacted as a line
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
    
    #choose the text from corups
    def get_sample_fromcorups(self):
        self.loadcorups()
        line=random.choice(self.corups)
        start=random.randint(0,len(line)-self.char_length)
        word=line[start:start+self.char_length]
        return word
    
    #loading the dict
    def loaddict(self):
        dic_file=open(self.dict_path)
        #self.dic=[ch.strip('\n') for ch in dic_file.readlines()]
        self.dic=[ch.strip() for ch in dic_file.readlines()]

    #choose the text from dict    
    def get_sample_fromdict(self):
        word=''
        self.loaddict()
        for _ in range(self.char_length):
            temp=random.choice(self.dic)
            word+=temp
        word=unicode(word,'utf-8')
        return word

    #sample func
    def get_sample(self):
        if(self.sample_mode=='corups'):
            word=self.get_sample_fromcorups()
            if(self.sample_mode=='chinese' and self.char_gap_mode=='space'):
                #there is no space or less space in chinese corups,so we need to add the space
                is_add_space=random.randint(0,10)
                if(is_add_space<5):
                    space_loc=random.randint(1,self.char_length-1)#we do not allow space appear in the start and end
                    word =word[:space_loc]+' '+word[space_loc:self.char_length-1]
            if(self.text_mode=='english'):
                while(word[0]==' ' or word[self.char_length-1]==' '):
                    #avoid space appearing in th start or the end
                    word=self.get_sample_fromcorups()
            return word
        elif(self.sample_mode=='dict'):
            word=self.get_sample_fromdict()
            if(self.char_gap_mode=='space'):
                while(word[0]==' ' or word[self.char_length-1]==' '):
                    #avoid space appearing in th start or the end
                    word=self.get_sample_fromdict()
            return word
        else:
            print 'sample mode is not defined'
            return ''