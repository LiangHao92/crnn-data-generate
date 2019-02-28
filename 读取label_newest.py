#coding:utf-8

import os
import random

a=open('word.txt','r')
dicfile=open('dic_english.txt','r')
dic=[ch.strip('\n') for ch in dicfile.readlines()]
imglist=a.readlines()
random.shuffle(imglist)
b=open('train.txt','w')
c=open('val.txt','w')
#valnum=len(imglist)/10
valnum=10001
i=0
for line in imglist:
    line=line.strip('\n')
    line_list=line.split('.jpg')
    text=line_list[0]+'.jpg'
    #text=str(int(line_list[0])-1)+'.jpg'
    #print line_list[0],text
    labelstr=line_list[1][1:]
    labelstr=unicode(labelstr,'utf-8')
    for label in labelstr:
        label=label.encode('utf-8')
        if(label not in dic):
            if label.isalpha():
                label=label.lower()
            else:
                print label
        index=dic.index(label)
        text=text+' '+str(index)
    i=i+1
    if(text==''):
        continue
    if(len(text.split(' '))!=11):
        print text
        continue
    if(i<valnum):
        c.write(text+'\n')
    else:
        b.write(text+'\n')
a.close()
b.close()
c.close()
