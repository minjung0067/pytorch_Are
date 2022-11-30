from selenium import webdriver as wb
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs
import pandas
import os #파일이나 폴더를 생성,삭제 해주는 라이브러리 filesystem lib
from urllib.request import urlretrieve
from tqdm import tqdm as tq

driver = wb.Chrome()
driver.get('https://www.naver.com')
search = driver.find_element(By.CSS_SELECTOR, '#query')
search.click()
search.send_keys('보문 콜로세움 인생샷')
search.send_keys(Keys.ENTER)

button = driver.find_element(By.CSS_SELECTOR, '#lnb > div.lnb_group > div > ul > li:nth-child(3) > a')
button.click()

body = driver.find_element(By.TAG_NAME, 'body')
try:
    for i in range(5):
        driver.execute_script("winow.scrollBy(0,10000)")
except Exception as e:
    print(e)
try:
    for i in tq(range(20)):
        body.send_keys(Keys.PAGE_DOWN)
except Exception as e:
    print(e)
    # time.sleep(1.5)

soup = bs(driver.page_source, 'html.parser') # html.parser
imgs = soup.select('div.thumb img')

img_list = []
for img in imgs:
    img_list.append(img['src'])
    # time.sleep(1)

if not os.path.isdir('/Users/mant/Desktop/project/school/capstone/pytorch_Are/capstone/naver_crawling_img'):
    os.mkdir('/Users/mant/Desktop/project/school/capstone/pytorch_Are/capstone/naver_crawling_img')
else:
    print('이미 존재하는 폴더입니다.')

for idx, img in enumerate(img_list):
    urlretrieve(img, '/Users/mant/Desktop/project/school/capstone/pytorch_Are/capstone/naver_crawling_img/crawling{0}.jpg'.format(idx))