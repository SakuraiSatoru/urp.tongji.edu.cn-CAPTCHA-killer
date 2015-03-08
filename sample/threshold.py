import cv2
from numpy import *

def threshold(img):
    out = zeros((img.shape[0],img.shape[1]),dtype = uint8)
    r = 0
    for x in img:
        c = 0
        for y in x:
            if y[0]<150:
                out[r,c] = 0
            else:
                out[r,c] = 255
            c = c + 1
        r = r + 1
    return out


img = cv2.imread("d.jpg")
print img

img = threshold(img)
cv2.imwrite("11111d.jpg",img)
print img


