#coding:utf-8

import random
import cv2
import numpy as np


def blurimg(img,flag):
    if(flag==0):
        return apply_gauss_blur(img, [3, 5])
    else:
        return apply_norm_blur(img)

def addnoise(img,flag):
    if(flag==0):
        return apply_gauss_noise(img)
    elif(flag==1):
        return apply_uniform_noise(img)
    elif(flag==2):
        return apply_sp_noise(img)
    else:
        return apply_poisson_noise(img)


#高斯模糊
def apply_gauss_blur(img, ks=None):
    if ks is None:
        ks = [7, 9, 11, 13]
    ksize = random.choice(ks)
    sigmas = [0, 1, 2, 3, 4, 5, 6, 7]
    sigma = 0
    if ksize <= 3:
        sigma = random.choice(sigmas)
    img = cv2.GaussianBlur(img, (ksize, ksize), sigma)
    return img

#blur
def apply_norm_blur(img, ks=None):
    # kernel == 1, the output image will be the same
    if ks is None:
        ks = [2, 3]
    kernel = random.choice(ks)
    img = cv2.blur(img, (kernel, kernel))
    return img

#Gaussian-distributed additive noise.
def apply_gauss_noise(img):
    row, col = img.shape
    mean = 0
    stddev = np.sqrt(15)
    gauss_noise = np.zeros((row, col))
    cv2.randn(gauss_noise, mean, stddev)
    out = img + gauss_noise
    return out

#Apply zero-mean uniform noise
def apply_uniform_noise(img):
    row, col = img.shape
    alpha = 0.05
    gauss = np.random.uniform(0 - alpha, alpha, (row, col))
    gauss = gauss.reshape(row, col)
    out = img + img * gauss
    return out

#Salt and pepper noise. Replaces random pixels with 0 or 255.
def apply_sp_noise(img):
    row, col = img.shape
    s_vs_p = 0.5
    amount = np.random.uniform(0.004, 0.01)
    out = np.copy(img)
    ##Salt mode
    num_salt = np.ceil(amount * img.size * s_vs_p)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img.shape]
    out[tuple(coords)] = 255
    # Pepper mode
    num_pepper = np.ceil(amount * img.size * (1. - s_vs_p))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img.shape]
    out[tuple(coords)] = 0
    return out

#Poisson-distributed noise generated from the data.
def apply_poisson_noise(img):
    vals = len(np.unique(img))
    vals = 2 ** np.ceil(np.log2(vals))
    if vals < 0:
        return img
    noisy = np.random.poisson(img * vals) / float(vals)
    return noisy




