import numpy as np
import cv2 
import os
from PIL import Image
from PIL import ImageColor
from collections import Counter
import collections


img = Image.open('C:\cap\grid\officelook24.png')

img = img.resize((500, 500))    #?��미�?? ?���? �?경하�?
#print(img.size)
pix = np.array(img)
#print(pix[0][0]) 
#li = pix.tolist()

max_bin = []
def rgb_to_hex(r, g, b):
    r, g, b = int(r), int(g), int(b)
    return '#' + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)

a=[]
x,y = 0,0
for _ in range(100):
    for k in range(100):
        arr = []
        for i in range(x,x+5):
            for j in range(y,y+5):
                arr.append(rgb_to_hex(pix[i][j][0],pix[i][j][1],pix[i][j][2]))
        cnt = Counter(arr).most_common(1)
        
        rgb_3color = ImageColor.getcolor(cnt[0][0], "RGB")
        max_bin.append(rgb_3color)

        y += 5
    x += 5
    y = 0
    
new_img = [[0 for col in range(500)] for row in range(500)]
count = 0
x,y =0,0
for e in range(100):
    for r in range(100):
        for q in range(x,x+5):
            for w in range(y,y+5):
                new_img[q][w] = max_bin[count]
        count += 1
        y += 5
    x+=5
    y=0

np_img = np.array(new_img)

pil_image = Image.fromarray((np_img*5).astype(np.uint8))
pil_image.show()