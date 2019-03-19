# coding:utf-8

import requests
from bs4 import BeautifulSoup
import time

url='https://knewone.com/?page='

#获取页面的数据
def get_page(url,data=None):
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'lxml')
    imgs=soup.select('a.cover-inner > img') #图片src
    titles=soup.select('section.content > h4 > a') #名称
    links=soup.select('section.content > h4 > a')   #原始链接
    if data==None:
        for img,title,link in zip(imgs,titles,links):
            data={
                'img':img.get('src'),
                'title':title.get('title'),
                'link':link.get('href')
            }
            print(data)

def get_more(start,end):
    for one in range(start,end):
        get_page(url+str(one))
        print(url+str(one))
        time.sleep(2)

get_more(1,4)