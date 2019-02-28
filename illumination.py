#coding:utf-8

import cv2
import numpy as np
import random

'''img=cv2.imread('0.jpg',0)
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v=cv2.split(img2)
matrix_255=np.ones(v.shape,dtype=v.dtype)*255
v=v+(matrix_255-v)/10
img_merged=cv2.merge([h,s,v])
img_result=cv2.cvtColor(img_merged,cv2.COLOR_HSV2BGR)
cv2.imwrite('a.jpg',img_result)'''

def change_illum(img):
    img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h,s,v=cv2.split(img_hsv)
    matrix_255=np.ones(v.shape,dtype=v.dtype)*255
    matrix_0=np.zeros(v.shape,dtype=v.dtype)
    if(random.randint(0,10)<5):
        num_temp=random.randint(2,10)
        v=v+(matrix_255-v)/num_temp
    else:
        num_temp=random.randint(2,10)
        v=v-(v-matrix_0)/num_temp
    img_merged=cv2.merge([h,s,v])
    img_result=cv2.cvtColor(img_merged,cv2.COLOR_HSV2BGR)
    return img_result
