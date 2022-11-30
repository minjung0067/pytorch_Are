import os 
from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import pandas
from urllib.request import urlretrieve
from tqdm import tqdm as tq
import path_setting as PATH # 경로 설정 관련 파일 
import numpy as np
from PIL import Image
import cv2

driver = wb.Chrome()
driver.get('https://www.naver.com')
search = driver.find_element(By.CSS_SELECTOR, '#query')
search.click()
search.send_keys('보문 콜로세움 인생샷')
search.send_keys(Keys.ENTER)

button = driver.find_element(By.CSS_SELECTOR, '#lnb > div.lnb_group > div > ul > li:nth-child(3) > a')
button.click()

body = driver.find_element(By.TAG_NAME, 'body')
for i in tq(range(20)):
    body.send_keys(Keys.END)
    time.sleep(0.5)

soup = bs(driver.page_source, 'html.parser') # html.parser
imgs = soup.select('div.thumb img')

img_list = []
for img in imgs:
    img_list.append(img['src'])

if not os.path.isdir(PATH.crawling_save_dir):
    os.mkdir(PATH.crawling_save_dir)
else:
    print('이미 존재하는 폴더입니다.')

for idx, img in enumerate(img_list):
    urlretrieve(img, PATH.crawling_save_dir + '/crawling{0}.jpg'.format(idx))

targerdir = PATH.crawling_save_dir  # 해당 폴더 설정 - 크롤링한 이미지

files = os.listdir(targerdir)

format = [".jpg", ".png", ".jpeg", "bmp", ".JPG", ".PNG", "JPEG", "BMP"]  # 지원하는 파일 형태의 확장자들
for (path, dirs, files) in os.walk(targerdir):
    for file in files:
        if file.endswith(tuple(format)):
            image = Image.open(path + "/" + file)
            print(image.filename)
            print(image.size)

            h = image.height
            w = image.width
            # 가로 세로 16:9
            if h>w and h/w < 16/9:  
                image = image.convert('RGB') # 이미지를 색깔로 바꾸겠다
                img = image.resize((300,400))  # 이미지 사이즈 변경
                img.save(PATH.save_dir1 + file) # 이미지 저장 경로
            elif h < w and w/h < 16/9:
                image = image.convert('RGB')
                img = image.resize((400, 300))
                img.save(PATH.save_dir2 + file)
            elif h == w:
                image = image.convert('RGB')
                img = image.resize((300, 300))
                img.save(PATH.save_dir3 + file)
            else:
                image.save(PATH.save_dir4+ file)
            # image.save(file)

            print(image.size)

        else: # 이미지가 만족하지 않을 때 실행
            print(path)
            print("InValid", file)