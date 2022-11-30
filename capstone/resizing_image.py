import os
import numpy as np
from PIL import Image
import numpy as np
import cv2
# 이미지 리 사이징 하기
targerdir = r"C:/Users/jeongdaeyun/PycharmProjects/pythonProject/main/img"  # 해당 폴더 설정 - 크롤링한 이미지

files = os.listdir(targerdir)

format = [".jpg", ".png", ".jpeg", "bmp", ".JPG", ".PNG", "JPEG", "BMP"]  # 지원하는 파일 형태의 확장자들
for (path, dirs, files) in os.walk(targerdir):
    for file in files:
        if file.endswith(tuple(format)):
            image = Image.open(path + "\\" + file)
            print(image.filename)
            print(image.size)

            h = image.height
            w = image.width
            # 가로 세로 16:9
            if h>w and h/w < 16/9:  
                image = image.convert('RGB') # 이미지를 색깔로 바꾸겠다
                img = image.resize((300,400))  # 이미지 사이즈 변경
                img.save("C:/Users/jeongdaeyun/PycharmProjects/pythonProject/main/sample_data1/" + file) # 이미지 저장 경로
            elif h < w and w/h < 16/9:
                image = image.convert('RGB')
                img = image.resize((400, 300))
                img.save("C:/Users/jeongdaeyun/PycharmProjects/pythonProject/main/sample_data2/" + file)
            elif h == w:
                image = image.convert('RGB')
                img = image.resize((300, 300))
                img.save("C:/Users/jeongdaeyun/PycharmProjects/pythonProject/main/sample_data3/" + file)
            else:
                image.save("C:/Users/jeongdaeyun/PycharmProjects/pythonProject/main/sample_data4/" + file)
            # image.save(file)

            print(image.size)

        else: # 이미지가 만족하지 않을 때 실행
            print(path)
            print("InValid", file)