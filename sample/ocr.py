# -*- coding: utf-8 -*-
import cv2
from numpy import *
import time
import thread
import os

def threshold(img): #二值化
    out = zeros((img.shape[0],img.shape[1]),dtype = uint8)
    r = 0
    for x in img:
        c = 0
        for y in x:
            if y < 150:  ##R通道
                out[r,c] = 0
            else:
                out[r,c] = 255
            c = c + 1
        r = r + 1
    return out

def row(img,wb): #横向划分
    rows = int(img.shape[0])
    if wb == 'b': #查找第一个黑行
        for n in range(rows):
            for x in img[n]:
                if x < 150:##R通道
                    return n
    if wb == 'w': #查找第一个白行
        for n in range(rows):
            flag = 0
            for x in img[n]:
                if x < 150:
                    flag = 1
                    break
            if flag == 0:
                return n

def col(img,wb): #纵向划分
    cols = int(img.shape[1])
    if wb == 'b': #查找第一个黑行
        for n in range(cols):
            for x in img[:,n]:
                if x < 150:
                    return n
    if wb == 'w': #查找第一个白行
        for n in range(cols):
            flag = 0
            for x in img[:,n]:
                if x < 150:
                    flag = 1
                    break
            if flag == 0:
                return n

def letter(img): #分割出第一个字，返回分割出和剩下

    y_1 = col(img,'b')
    img_c = img[:,y_1:]
    y_2 = col(img_c,'w')
    img_c = img_c[:,:y_2]
    x_1 = row(img_c,'b')
    img_c = img_c[x_1:,:]
    x_2 = row(img_c,'w')
    img_c = img_c[:x_2,:]
    try:
        img_r = img[:,y_1+y_2:]
    except(TypeError):
        #print 'meet an end'
        img_r = img[:,y_1:]    
    return img_c,img_r

def sample(img): #沉降标准化
    rows = img.shape[0]
    cols = img.shape[1]
    c = 0
    while c <= cols -1:
        n = 0 #blank
        
        for x in img[::-1,c]:
            if x >150:
                n = n + 1
            else:
                break
        if n != 0:
            i = n #3
            while i<= rows-1:
                img[::-1,c][i-n] = img[::-1,c][i]
                i = i+1
            j = rows - n
            while j <= rows-1:
                img[::-1,c][j] = 255
                j = j+1
        c = c + 1
        
    s = row(img,'b')
    img = img[s:,:]
    return img

def match(std,img): #标准全匹配黑色
    flag = 1
    a = 0
    for x in img:
        b = 0
        for y in x:
            if y < 150 :
                if std[a,b] > 150:
                    flag = 0
                    
                    return flag
            b = b + 1
        a = a + 1
    return flag



def ocr_s(img): #识别已标准化的单字
    img = sample(img)
    if img.shape[0] < 10 and img.shape[1] < 10:
        return ''
    flag = 0
    for n in range(len(matdic)):
        if ( img.shape[0] == matdic[n]['rows'] and img.shape[1] == matdic[n]['cols'] ):
            flag = match(matdic[n]['mat'],img)
            if flag:
                #print ocrdic[n]
                return ocrdic[n]
    if not flag:
        #检验上边界
        if attr[0] == -1:
            for y in fimg[1]: #第0行始终全白
                if y < 150:
                    attr[0] = 1
                    
                    break
                attr[0] = 0

        #确认上黑，开始识别，W、Y上黑不可识别
        if attr[0] == 1:
            for n in range(len(matdic)-1):
                if matdic[n]['cols'] >= img.shape[1]: #否则溢出
                    #print 'indic',ocrdic[n]
                    flag1 = 1
                    a = 0
                    for x in img[::-1]:
                        b = 0
                        for y in x:  
                            if y < 150:
                                #print a,b
                                #print matdic[n]['rows']-a-1,b
                                #print 'y',y
                                #print 'sample',matdic[n]['mat'][matdic[n]['rows']-a-1]
                                if matdic[n]['mat'][matdic[n]['rows']-a-1,b] > 150:
                                    flag1 = 0
                            b = b + 1
                        a = a + 1
                    if flag1:
                        return ocrdic[n]
            print 'attr[0]=1,dic out'

        #检验右边界
        if attr[2] == -1:
            for x in fimg[:,-1]:                
                if x < 150:
                    attr[2] = 1
                    break
                attr[2] = 0

        #确认右黑，开始识别
        if attr[2] == 1:
            for n in range(len(matdic)-1):
                if (matdic[n]['rows'] >= img.shape[0] and matdic[n]['cols'] >= img.shape[1]):
                    flag2 = match(matdic[n]['mat'],img)
                    if flag2:
                        return ocrdic[n]
            print 'attr[2]=1,dic out'
        return ''

                    




def ocr(pic):  
    #initialize
    cv2.imwrite('ocr.jpg',pic)
    global matdic,fimg,ocrdic,attr
    matdic = {}
    ocrdic = {}
    for n in range(19):
        img = cv2.imread("sample_"+str(n)+".jpg",0)
        matdic[n] = {'mat':img,'rows':img.shape[0],'cols':img.shape[1]}
    ocrdic = {0:'2',1:'3',2:'4',3:'5',4:'6',5:'7',6:'8',7:'b',8:'c',9:'d',10:'e',11:'f',12:'m',13:'n',14:'p',15:'w',16:'x',17:'y',18:'fy'}
    #if len(ocrdic) == len(matdic):
        #print 'Initialized',len(matdic),'samples'


    #split into 4 letters
    img = cv2.imread('ocr.jpg',0)
    fimg = pic[::]
    
    
    attr = [-1,-1,-1,-1] #上 左 右 下

    (img_a,img_bcde) = letter(img)
    (img_b,img_cde) = letter(img_bcde)
    (img_c,img_de) = letter(img_cde)
    (img_d,img_e) = letter(img_de)

    ans_a = ocr_s(img_a)
    ans_b = ocr_s(img_b)
    ans_c = ocr_s(img_c)
    ans_d = ocr_s(img_d)
    ans = ans_a+ans_b+ans_c+ans_d
    if len(ans) == 3:
        (img_e,img_f) = letter(img_e)
        ans_e = ocr_s(img_e)
        ans = ans + ans_e
    return ans


for n in range(600):
    pic = str(n+1)+'.jpg'
    pic = cv2.imread(pic,0)
    print ocr(pic)
os.remove('ocr.jpg')

