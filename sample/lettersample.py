# -*- coding: utf-8 -*-
import cv2
import numpy
'''
RGB通道
1.fy
2.f在最上面的时候会被识别两次（414）
3.最右
'''
def row(img,wb):
    rows = int(img.shape[0])
    if wb == 'b':
        for n in range(rows):
            for x in img[n]:
                if x[0] < 150:
                    return n
    if wb == 'w':
        for n in range(rows):
            flag = 0
            for x in img[n]:
                if x[0] < 150:
                    flag = 1
                    break
            if flag == 0:
                return n

            
img = cv2.imread("a.jpg")
#print img[:,0]
rows = img.shape[0]
cols = img.shape[1]
sample = numpy.ones(img.shape, numpy.uint8)

c = 0
while c <= cols -1:
    n = 0 #blank
    
    for x in img[::-1,c,0]:
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
            img[::-1,c][j] = [255,255,255]
            j = j+1
    c = c + 1
    
s = row(img,'b')
img = img[s:,:,:]
cv2.imwrite('sample_a.jpg',img)

