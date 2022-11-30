from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
import shutil

baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome()
driver.get(url)

time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html)

imglist = []


for i in range(0, 2):

    insta = soup.select('._aabd._aa8k._aanf')

    for i in insta:

        print('https://www.instagram.com' + i.a['href'])
        imgUrl = i.select_one('._aagv').img['src']
        imglist.append(imgUrl)
        imglist = list(set(imglist))
        html = driver.page_source
        soup = BeautifulSoup(html)
        insta = soup.select('._aabd._aa8k._aanf')

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

n = 0

for i in range(len(imglist)-1):
    # This is the image url.
    image_url = imglist[n]
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)

    # Open a local file with wb ( write binary ) permission.
    local_file = open('/Users/jeongdaeyun/PycharmProjects/pythonProject/main/img/' +
                      plusUrl + str(n) + '.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    n += 1
    del resp

driver.close()