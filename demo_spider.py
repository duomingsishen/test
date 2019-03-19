# -*- coding:utf-8 -*-

# from urllib import request,parse
import json
from http.cookiejar import CookieJar,MozillaCookieJar
import requests
import ssl
from lxml import etree
from bs4 import BeautifulSoup
from pyecharts import Bar
import re
import csv
import pymysql
import pymongo
import threading
import time
import datetime
import random
from queue import Queue
import os
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.select import Select
# import urllib2,urllib
# import pymssql
import cx_Oracle

#urlopen打开网址
# response=request.urlopen('http://www.baidu.com')
# print(response.getcode())

#下载图片或视频
# request.urlretrieve('http://www.baidu.com','index.html')

#urlencode() 将字典转换为URL编码的数据  parse_qs 解码
# data={'name':'张三','key':12}
# result=parse.urlencode(data)
# print(parse.parse_qs(result))

#urlsplit 和urlparse 对url进行分割
# url='http://www.baidu.com/s?username=zhiliao'
# # result=parse.urlsplit(url)
# result=parse.urlparse(url)
# print(result)
# print('scheme:',result.scheme)
# print('netloc:',result.netloc)
# print('path:',result.path)
# print('query:',result.query)


#Request传请求头
# url='https://www.lagou.com/jobs/positionAjax.json?city=%E6%AD%A6%E6%B1%89&needAddtionalResult=false'
# headers={
#     'Referer':'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# }
# data={
#     'first': 'true',
#     'pn': 1,
#     'kd': 'python爬虫'
# }
# data=parse.urlencode(data).encode(encoding='utf-8')
# req=request.Request(url,data=data,headers=headers,method='POST')
# rq=request.urlopen(req).read().decode('utf-8')
# print(json.loads(rq))

#使用代理访问
# resp=request.urlopen('http://httpbin.org/get')
# print(resp.read().decode('utf-8'))

# handler=request.ProxyHandler({"http:":"27.191.234.69:9999"}) #构建代理
# opener=request.build_opener(handler)    #绑定代理
# resp=opener.open('http://httpbin.org/ip')
# print(resp.read())


#使用cookie登录人人网
# url='http://www.renren.com/880151247/profile'
# headers={
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
# 'Cookie':'anonymid=jkvyo68vhq0z8s; depovince=HUB; _r01_=1; JSESSIONID=abcC8RV_dSXwCgBhNNavw; ick_login=13907562-6c54-4a7c-9789-fef36a93a1a0; jebe_key=152e1d98-686f-4f70-aa6a-77be26110add%7C4a8b364cb2ae4c5d3aa891ff47a21308%7C1534387511347%7C1%7C1534387491961; _ga=GA1.2.1706607058.1534388165; _gid=GA1.2.1195234929.1534388165; BAIDU_SSP_lcr=https://www.baidu.com/link?url=UfaUuwsYAcz5zG0Zn7D_xpanTKQS6ZqttoKArlBIYpO&wd=&eqid=890b5b8b000493cb000000055b750d53; wp_fold=0; t=1ccf99d925d62ea97b85852de63faeb97; societyguester=1ccf99d925d62ea97b85852de63faeb97; id=967485697; xnsid=beae2092; jebecookies=a57bc255-2732-4eda-85ed-a915aa406bf1|||||'
#
# }
# req=request.Request(url,headers=headers)
# resp=request.urlopen(req)
# print(resp.read().decode('utf-8'))

#定义全局Cookie登录
# cookiejar=CookieJar()
# cookie=request.HTTPCookieProcessor(cookiejar)
# opener=request.build_opener(cookie)
#
# headers={
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# }
# data={
#     # 'email':'970138074@qq.com',
#     # 'password':'pythonspider'
#     'email': '970138074@qq.com',
# 'icode': '',
# 'origURL':'http://www.renren.com/home',
# 'domain':'renren.com',
# 'key_id': 1,
# 'captcha_type':'web_login',
# 'password':'c6f1b63b7ba05d1caff69600407c0ce146e89f79eae928d23021018d6705824c',
# 'rkey': '08b3e099075b882db0075c6b1163a1f3',
# 'f': ''
# }
# data=parse.urlencode(data).encode('utf-8')
# login_url='http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2018741948456'
# req=request.Request(login_url,data=data,headers=headers)
# opener.open(req)
#
# dapeng_url='http://www.renren.com/880151247/profile'
# resp=opener.open(dapeng_url)
# print(resp.read().decode('utf-8'))

#cookie的保存和加载
# cookiejar=MozillaCookieJar('cookie.txt')
# c=request.HTTPCookieProcessor(cookiejar)
# opener=request.build_opener(c)
#
#
# url='http://www.baidu.com'
# cookiejar.load(ignore_discard=True) #加载本地cookie信息
# rsq=opener.open(url)
# # print(rsq.read().decode('utf-8'))
#
#
# cookiejar.save(ignore_discard=True,ignore_expires=True)  #保存cookie信息到本地

# url='https://www.lagou.com/jobs/positionAjax.json?city=%E6%AD%A6%E6%B1%89&needAddtionalResult=false'
# headers={
#     'Referer':'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# }
# data={
#     'first': 'true',
#     'pn': 1,
#     'kd': 'python爬虫'
# }
#
# resp=requests.post(url,headers=headers,data=data)
# #返回的是json数据可直接使用json方法
# print(resp.json())

#requests的代理
# proxy={
#     'http':'61.145.194.26:8080'
# }
# response=requests.get('http://httpbin.org/ip',proxies=proxy)
# print(response.text)

#获取cookies的信息
# resp=requests.get('http://www.baidu.com')
# print(resp.cookies)
# print(resp.cookies.get_dict())

#建立回话使用与登录操作其他功能
# url='http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2018741948456'
# headers={
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# }
# data={
#     # 'email':'970138074@qq.com',
#     # 'password':'pythonspider'
#     'email': '970138074@qq.com',
#     'icode': '',
#     'origURL':'http://www.renren.com/home',
#     'domain':'renren.com',
#     'key_id': 1,
#     'captcha_type':'web_login',
#     'password':'c6f1b63b7ba05d1caff69600407c0ce146e89f79eae928d23021018d6705824c',
#     'rkey': '08b3e099075b882db0075c6b1163a1f3',
#     'f': ''
# }
#
# session=requests.session()
# session.post(url,data=data,headers=headers)
#
# resp=session.get('http://www.renren.com/880151247/profile')
# print(resp.text)

#处理不信任的SSL证书
# resp=requests.get('http://www.12306.cn/mormhweb/',verify=False)
# print(resp.content.decode('utf-8'))

#lmxl的使用
# url='https://www.lagou.com/jobs/4578862.html'
# headers={
#     'Referer':'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# }
#
# req=request.Request(url,headers=headers)
# html=request.urlopen(req)
# xml=etree.HTML(html.read())
# ht=xml.xpath("//h3[@class='description']/text()")[0]
# print(ht)

# text='''
# <div>
#     <ul>
#          <li class="item-0"><a href="link1.html">first item</a></li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-inactive"><a href="link3.html">third item</a></li>
#          <li class="item-1"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
#      </ul>
#  </div>
# '''
# #读取html转换为xml
# # html=etree.HTML(text)
# # print(etree.tostring(html,encoding='utf-8').decode('utf-8'))
#
# #读取文件html转成html  默认转的时候html不规范导致报错
# parser=etree.HTMLParser(encoding='utf-8')
# html=etree.parse('login.html',parser=parser)
# print(etree.tostring(html,encoding='utf-8').decode('utf-8'))

# url='https://movie.douban.com/cinema/nowplaying/ezhou/'
# headers={
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
#     'Referer': 'https://movie.douban.com/'
# }
#
# response=requests.get(url,headers=headers)
# text=response.text
# html=etree.HTML(text)
# xml=html.xpath('//ul[@class="lists"]')[0]
# lis=xml.xpath('./li')
# for li in lis:
#     print(etree.tostring(li,encoding='utf-8').decode('utf-8'))
#     break

# Basic_domain='http://www.dytt8.net'
#
# headers={
# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# }
# def get_detail_urls(url):
#     response=requests.get(url,headers=headers)
#     text=response.text
#     html=etree.HTML(text)
#     detail_urls=html.xpath('//table[@class="tbspan"]//a/@href')
#     detail_urls=map(lambda url:Basic_domain+url,detail_urls)
#     return detail_urls
#
# def parse_detail_page(url):
#     pass
#
# def spider():
#     url ='http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
#     for i in range(1,5):
#         url=url.format(i)
#         print(url,i)
#         # for detail_url in get_detail_urls(url):
#         #     print(url)
#
#
# if __name__ == '__main__':
#     spider()

# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
#
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
#
# <p class="story">
# ...
# </p>
# """
#
# soup=BeautifulSoup(html_doc,'html.parser')
# #find_all和find使用的方法
# # soup.find_all("a",id='link2')
# # soup.find("a",attrs={"id":"link2"})
# a=soup.find_all('p',class_='story')
#
# print(a)

# ALL_DATA=[]
# headers={
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# }
#
# def parse_page(url):
#     response = requests.get(url, headers=headers)
#     text=response.content.decode('utf-8')
#     soup = BeautifulSoup(text, 'html5lib') #当html不规范使用
#     conMidtab=soup.find('div',class_='conMidtab')
#     tables=conMidtab.find_all('table')
#     for table in tables:
#         trs=table.find_all('tr')[2:]
#         for tr in trs:
#             tds=tr.find_all('td')
#             city_td=tds[-8]
#             city=list(city_td.stripped_strings)[0]
#             temp_td=tds[-5]
#             max_temp=list(temp_td.stripped_strings)[0]
#             ALL_DATA.append({'city':city,'max_temp':max_temp})
#             # print({'city':city,'max_temp':max_temp})
#
#
#
# def main():
#     urls = ['http://www.weather.com.cn/textFC/hb.shtml', 'http://www.weather.com.cn/textFC/db.shtml','http://www.weather.com.cn/textFC/hd.shtml','http://www.weather.com.cn/textFC/hz.shtml','http://www.weather.com.cn/textFC/hn.shtml','http://www.weather.com.cn/textFC/xb.shtml','http://www.weather.com.cn/textFC/xn.shtml','http://www.weather.com.cn/textFC/gat.shtml']
#     for url in urls:
#         parse_page(url)
#     ALL_DATA.sort(key=lambda data:data['max_temp'],reverse=True)
#     data=ALL_DATA[0:10]
#     cities=list(map(lambda x:x['city'],data))
#     temps=list(map(lambda x:x['max_temp'],data))
#     chart=Bar("中国天气最高气温排行榜")
#     chart.add('',cities,temps)
#     chart.render('temperature.html')
#
# if __name__ == '__main__':
#     main()

# text = "apple price is $99,orange price is $10"
# ret = re.search(r".*(\$\d+).*(\$\d+)",text)
# print(ret.groups())

# html = """
# <div>
# <p>基本要求：</p>
# <p>1、精通HTML5、CSS3、 JavaScript等Web前端开发技术，对html5页面适配充分了解，熟悉不同浏览器间的差异，熟练写出兼容各种浏览器的代码；</p>
# <p>2、熟悉运用常见JS开发框架，如JQuery、vue、angular，能快速高效实现各种交互效果；</p>
# <p>3、熟悉编写能够自动适应HTML5界面，能让网页格式自动适应各款各大小的手机；</p>
# <p>4、利用HTML5相关技术开发移动平台、PC终端的前端页面，实现HTML5模板化；</p>
# <p>5、熟悉手机端和PC端web实现的差异，有移动平台web前端开发经验，了解移动互联网产品和行业，有在Android,iOS等平台下HTML5+CSS+JavaScript（或移动JS框架）开发经验者优先考虑；6、良好的沟通能力和团队协作精神，对移动互联网行业有浓厚兴趣，有较强的研究能力和学习能力；</p>
# <p>7、能够承担公司前端培训工作，对公司各业务线的前端（HTML5\CSS3）工作进行支撑和指导。</p>
# <p><br></p>
# <p>岗位职责：</p>
# <p>1、利用html5及相关技术开发移动平台、微信、APP等前端页面，各类交互的实现；</p>
# <p>2、持续的优化前端体验和页面响应速度，并保证兼容性和执行效率；</p>
# <p>3、根据产品需求，分析并给出最优的页面前端结构解决方案；</p>
# <p>4、协助后台及客户端开发人员完成功能开发和调试；</p>
# <p>5、移动端主流浏览器的适配、移动端界面自适应研发。</p>
# </div>
# """
#
# ret = re.sub('</?[a-zA-Z0-9]+>',"",html)
# print(ret)

# text = "the number is 20.50"
# r = re.compile(r"""
#                 \d+ # 小数点前面的数字
#                 \.? # 小数点
#                 \d* # 小数点后面的数字
#                 """,re.VERBOSE)
# ret = re.search(r,text)
# print(ret.group())

# def write_csv():
#     headers = ['name','age','classroom']
#     values = [
#         ('zhiliao',18,'111'),
#         ('wena',20,'222'),
#         ('bbc',21,'111')
#     ]
#     with open('test.csv','w',newline='') as fp:
#         writer = csv.writer(fp)
#         writer.writerow(headers)
#         writer.writerows(values)
#
# def dicwriter_csv():
#     headers = ['name','age','classroom']
#     values = [
#         {"name":'wenn',"age":20,"classroom":'222'},
#         {"name":'abc',"age":30,"classroom":'333'}
#     ]
#     with open('test.csv','w',newline='') as fp:
#         writer = csv.DictWriter(fp,headers)
#         writer.writeheader()  #写入表头的数据
#         writer.writerow({'name':'zhiliao',"age":18,"classroom":'111'})
#         writer.writerows(values)
#
#
# if __name__ == '__main__':
#     dicwriter_csv()

# mysql连接
# conn=pymysql.connect(
#     host="10.10.3.123",
#     user='root',
#     password='360361689',
#     database='papertest',
#     port=3306,
#     charset='utf8'  #针对中文数据
# )
# cursor=conn.cursor()  #创建游标
# #查询数据
# # cursor.execute('select *from user')
# # results=cursor.fetchall()
# # for result in results:
# #     print result
#
# #插入数据
# # sql="insert into user(username,age,password) values('王五',20,'123789')"
# # cursor.execute(sql)
# # conn.commit()   #更新表数据的提交
# # conn.rollback() #撤销更新表的数据
#
# cursor.close()  #关闭游标
#
# #获取连接mongodb对象
# client=pymongo.MongoClient('10.10.3.123',port=27017)
#
# #获取数据库
# db=client.mesdb
#
# #获取数据库中的集合
# collection=db.message
#
# #写入数据
# collection.insert({"username":'aaaa'})

#线程的使用
# def coding():
#     for x in range(3):
#         print('%s正在写代码' % threading.current_thread())
#         time.sleep(1)
#
# def drawing():
#     for x in range(3):
#         print('%s正在画图' % threading.current_thread())
#         time.sleep(1)
#
#
# def single_thread():
#     coding()
#     drawing()
#
# def multi_thread():
#     t1 = threading.Thread(target=coding)
#     t2 = threading.Thread(target=drawing)
#
#     t1.start()
#     t2.start()
#
#
# if __name__ == '__main__':
#     multi_thread()

# import threading
# import time
#
# class CodingThread(threading.Thread):
#     def run(self):
#         for x in range(3):
#             print('%s正在写代码' % threading.current_thread())
#             time.sleep(1)
#
# class DrawingThread(threading.Thread):
#     def run(self):
#         for x in range(3):
#             print('%s正在画图' % threading.current_thread())
#             time.sleep(1)
#
# def multi_thread():
#     t1 = CodingThread()
#     t2 = DrawingThread()
#
#     t1.start()
#     t2.start()
#
# if __name__ == '__main__':
#     multi_thread()

# tickets = 0
# glock=threading.Lock()
#
# def get_ticket():
#     global tickets
#     glock.acquire()
#     for x in range(1000000):
#         tickets += 1
#     glock.release()
#     print('tickets:%d'%tickets)
#
# def main():
#     for x in range(2):
#         t = threading.Thread(target=get_ticket)
#         t.start()
#
# if __name__ == '__main__':
#     main()

# gMoney=1000
# gLock=threading.Lock()
# # 记录生产者生产的次数，达到10次就不再生产
# gTimes = 0
#
# class Producer(threading.Thread):
#     def run(self):
#         global gMoney
#         global gLock
#         global gTimes
#         while True:
#             money = random.randint(100, 1000)
#             gLock.acquire()
#             # 如果已经达到10次了，就不再生产了
#             if gTimes >= 10:
#                 gLock.release()
#                 break
#             gMoney += money
#             print('%s当前存入%s元钱，剩余%s元钱' % (threading.current_thread(), money, gMoney))
#             gTimes += 1
#             time.sleep(0.5)
#             gLock.release()
#
#
#
# class Consumer(threading.Thread):
#     def run(self):
#         global gMoney
#         global gLock
#         global gTimes
#         while True:
#             money = random.randint(100, 500)
#             gLock.acquire()
#             if gMoney > money:
#                 gMoney -= money
#                 print('%s当前取出%s元钱，剩余%s元钱' % (threading.current_thread(), money, gMoney))
#                 time.sleep(0.5)
#             else:
#                 # 如果钱不够了，有可能是已经超过了次数，这时候就判断一下
#                 if gTimes >= 10:
#                     gLock.release()
#                     break
#                 print("%s当前想取%s元钱，剩余%s元钱，不足！" % (threading.current_thread(), money, gMoney))
#             gLock.release()
#
#
#
# def main():
#     for x in range(5):
#         Consumer(name='消费者线程%d'%x).start()
#
#     for x in range(5):
#         Producer(name='生产者线程%d'%x).start()
#
# if __name__ == '__main__':
#     main()


# gMoney = 1000
# gCondition = threading.Condition()
# gTimes = 0
# gTotalTimes = 5
#
# class Producer(threading.Thread):
#     def run(self):
#         global gMoney
#         global gCondition
#         global gTimes
#         while True:
#             money = random.randint(100, 1000)
#             gCondition.acquire()
#             if gTimes >= gTotalTimes:
#                 gCondition.release()
#                 print('当前生产者总共生产了%s次'%gTimes)
#                 break
#             gMoney += money
#             print('%s当前存入%s元钱，剩余%s元钱' % (threading.current_thread(), money, gMoney))
#             gTimes += 1
#             time.sleep(0.5)
#             gCondition.notify_all()
#             gCondition.release()
#
# class Consumer(threading.Thread):
#     def run(self):
#         global gMoney
#         global gCondition
#         while True:
#             money = random.randint(100, 500)
#             gCondition.acquire()
#             # 这里要给个while循环判断，因为等轮到这个线程的时候
#             # 条件有可能又不满足了
#             while gMoney < money:
#                 if gTimes >= gTotalTimes:
#                     gCondition.release()
#                     return
#                 print('%s准备取%s元钱，剩余%s元钱，不足！'%(threading.current_thread(),money,gMoney))
#                 gCondition.wait()
#             gMoney -= money
#             print('%s当前取出%s元钱，剩余%s元钱' % (threading.current_thread(), money, gMoney))
#             time.sleep(0.5)
#             gCondition.release()
#
# def main():
#     for x in range(5):
#         Consumer(name='消费者线程%d'%x).start()
#
#     for x in range(2):
#         Producer(name='生产者线程%d'%x).start()
#
# if __name__ == '__main__':
#     main()

# class Producer(threading.Thread):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
#     }
#     def __init__(self,page_queue,img_queue,*args,**kwargs):
#         super(Producer, self).__init__(*args, **kwargs)
#         self.page_queue = page_queue
#         self.img_queue = img_queue
#
#
#     def run(self):
#         while True:
#             if self.page_queue.empty():
#                 break
#             url = self.page_queue.get()
#             self.parse_page(url)
#
#     def parse_page(self,url):
#         response = requests.get(url,headers=self.headers)
#         text = response.text
#         html = etree.HTML(text)
#         imgs = html.xpath("//div[@class='page-content text-center']//a//img")
#         for img in imgs:
#             if img.get('class') == 'gif':
#                 continue
#             img_url = img.xpath(".//@data-original")[0]
#             suffix = os.path.splitext(img_url)[1]
#             alt = img.xpath(".//@alt")[0]
#             alt = re.sub(r'[，。？?,/\\·]','',alt)
#             img_name = alt + suffix
#             self.img_queue.put((img_url,img_name))
#
# class Consumer(threading.Thread):
#     def __init__(self,page_queue,img_queue,*args,**kwargs):
#         super(Consumer, self).__init__(*args,**kwargs)
#         self.page_queue = page_queue
#         self.img_queue = img_queue
#
#     def run(self):
#         while True:
#             if self.img_queue.empty():
#                 if self.page_queue.empty():
#                     return
#             img = self.img_queue.get(block=True)
#             url,filename = img
#             request.urlretrieve(url,'images/'+filename)
#             print(filename+'  下载完成！')
#
# def main():
#     page_queue = Queue(100)
#     img_queue = Queue(500)
#     for x in range(1,101):
#         url = "http://www.doutula.com/photo/list/?page=%d" % x
#         page_queue.put(url)
#
#     for x in range(5):
#         t = Producer(page_queue,img_queue)
#         t.start()
#
#     for x in range(5):
#         t = Consumer(page_queue,img_queue)
#         t.start()
#
# if __name__ == '__main__':
#     main()

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument('--headless')    #设置不显示浏览器
# # chrome_options.add_argument('--disable-gpu')
# #
# # driver=webdriver.Chrome(chrome_options=chrome_options)
# driver=webdriver.Chrome()
# driver.get('https://www.baidu.com/')
# elem=driver.find_element_by_name('wd')
# elem.send_keys(u'python')
# elem.send_keys(Keys.RETURN)
# time.sleep(5)
# for cookie in driver.get_cookies():  #获取所有的cookie
#     print cookie
# # driver.save_screenshot('1.png') #浏览器截图保存
# print '='*20
# print driver.get_cookie('BD_HOME')  #根据cookie的key获取value
#
# driver.delete_all_cookies()    #删除所有的cookie信息

# driver.delete_cookie('BD_HOME')  #删除某个cookie信息


# driver = webdriver.Chrome()
# driver.get("http://somedomain/url_that_delays_loading")
# driver.implicitly_wait(10)  #隐式等待
#
#
# try:
#     element = WebDriverWait(driver, 10).until(
#          EC.presence_of_element_located((By.ID, "myDynamicElement"))   #显示等待
#     )
# finally:
#     driver.quit()
#

# driver=webdriver.Chrome()
# driver.get('http://open.nmgd.cn:8000/mayn-erp/login.do;JSESSIONID=b9ea006a-9538-45fc-bee2-7996f58a9458')
# driver.maximize_window()
# driver.implicitly_wait(10)
# driver.find_element_by_name('username').send_keys('00853')
# driver.find_element_by_name('password').send_keys('360361689')
# driver.find_element_by_id('loginBtn').click()
#
#
# btn=driver.find_element_by_class_name('icon-shop')
# menu=driver.find_element_by_xpath('//div[@id="menu-336"]/div[last()-1]')
#
# actions = ActionChains(driver)
# actions.move_to_element(btn)
# actions.perform()
# time.sleep(2)
# actions.move_to_element(menu).click()
# actions.perform()


#使用代理IP
# options = webdriver.ChromeOptions()
# options.add_argument("--proxy-server=http://180.118.247.229:9000")
# driver = webdriver.Chrome(chrome_options=options)
#
# driver.get('http://httpbin.org/ip')


# positions=[]
# driver=webdriver.Chrome()
# driver.get('https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=')
# # driver.find_element_by_xpath('//ul[@class="clearfix"]/li[last()]').click()
# # driver.find_element_by_id('search_input').send_keys('python')
# # driver.find_element_by_id('search_button').click()
# driver.maximize_window()
# h=driver.current_window_handle
# list_count=len(driver.find_elements_by_xpath('//li[contains(@class,"default_list")]//h3'))
# for i in range(2):
#     list=driver.find_elements_by_xpath('//li[contains(@class,"default_list")]//h3')[i]
#     actions = ActionChains(driver)
#     actions.move_to_element(list).click()
#     actions.perform()
#
#     list_url=driver.window_handles[1]
#     driver.switch_to.window(list_url)
#     html=driver.page_source
#     text=etree.HTML(html)
#     position_list=text.xpath('//div[@class="position-content-l"]//span/text()')
#     contents=text.xpath('//dd[@class="job_bt"]/div/p/text()|//dd[@class="job_bt"]/div/text()')
#     position=position_list[0]
#     pay=position_list[1]
#     address=position_list[2].replace('/','').strip()
#     experience=position_list[3].replace('/','').strip()
#     education=position_list[4].replace('/','').strip()
#     content=''.join(contents)
#     list={
#         "position":position,
#         "pay":pay,
#         "address":address,
#         "experience":experience,
#         "education":education,
#         "content":content
#     }
#     positions.clear()
#     positions.append(list)
#     print(positions)
#     print("=" * 30)
#
#     driver.close()
#     driver.switch_to.window(h)
#     time.sleep(2)


# 导入pytesseract库

# import pytesseract
# # 导入Image库
# from PIL import Image
#
# # 指定tesseract.exe所在的路径
# pytesseract.pytesseract.tesseract_cmd = r'D:\tesseract-ocr\Tesseract-OCR\tesseract.exe'
#
# # 打开图片
# image = Image.open("a.png")
# # 调用image_to_string将图片转换为文字
# text = pytesseract.image_to_string(image)
# print(text)

# import pytesseract
# from urllib import request
# from PIL import Image
# import time
#
#
# pytesseract.pytesseract.tesseract_cmd = r"D:\tesseract-ocr\Tesseract-OCR\tesseract.exe"
#
#
# while True:
#     captchaUrl = "https://passport.lagou.com/vcode/create?from=register&refresh=1513081451891"
#     request.urlretrieve(captchaUrl,'captcha.png')
#     image = Image.open('captcha.png')
#     text = pytesseract.image_to_string(image,lang='eng')  #lang='eng' 指定中文还是英文
#     print(text)
#     time.sleep(2)

# class Grab_votes(object):
#     def __init__(self):
#         self.login_url='https://kyfw.12306.cn/otn/login/init'
#         self.driver=webdriver.Chrome()
#         self.username="cai345408904"
#         self.password="cai15928021496"
#         self.initMy='https://kyfw.12306.cn/otn/index/initMy12306'
#
#     def login(self):
#         self.driver.get(self.login_url)
#         self.driver.find_element_by_id('username').send_keys(self.username)
#         self.driver.find_element_by_id('password').send_keys(self.password)
#         WebDriverWait(self.driver,1000).until(
#             EC.url_to_be(self.initMy)
#         )
#         print '登录成功'
#
#     def order_ticket(self):
#         self.driver.maximize_window()
#         self.driver.find_element_by_link_text('车票预订').click()
#         print self.driver.current_url
#
#
#     def run(self):
#         self.login()
#         self.order_ticket()
#
# if __name__ == '__main__':
#     spider=Grab_votes()
#     spider.run()


# url='http://192.168.50.222:8000/mayn-erp/api/open/resaleForMes/{0}/CheckRefund.do'
# url=url.format('10518092194111')
# response=requests.post(url)
# print response.text

# import requests
# import json
#
# import requests
# import sys
# import json
#
# reload(sys)
# sys.setdefaultencoding('utf-8')
#


# conn=pymysql.connect(
#     host="10.10.3.123",
#     user='root',
#     password='360361689',
#     database='jianshu',
#     port=3306,
#     charset='utf8'  #针对中文数据
# )
# cursor=conn.cursor()  #创建游标
# #查询数据
# cursor.execute('select mo from Winning where STATUS=0')
# results=cursor.fetchall()
# for mo in results:
#     if get_html(mo)==5:
#         sql="update Winning set STATUS=1 where mo='{}'".format(mo[0])
#         cursor.execute(sql)
#         conn.commit()
# cursor.close()  #关闭游标

# def get_oracle():
#     os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决乱码问题
#
#     conn = cx_Oracle.connect('NMKMESSUPPORT', '123@Nmgd.com', '10.10.1.249:1521/mesdb')   #这步不报错就是连上啦
#     cursor = conn.cursor()
#     sql ='select * from BAS_LINE'
#     cursor.execute(sql)
#     data = cursor.fetchone()
#     print(data)
#     cursor.close()
#     conn.close()
#
#
# def sever_sql(keyid):
#     sql="select ProductKey from ProductKeyInfo where ProductKeyID='{}'".format(keyid)
#     conn = pymssql.connect('10.10.3.85:1433', 'sa', '123@Nmgd.com', 'MDOS_FFKI_KeyStore')
#     #10.10.3.85:1433  可加端口号 可不加
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     row = cursor.fetchone()
#     conn.close()
#     return row[0]
#
#
# print sever_sql('3423499917224')

#<editor-fold desc="socket爬取豆瓣">
"""
import socket
import ssl

def findall_in_html(html,startpart,endpart):
    all_strings=[]
    start=html.find(startpart)+len(startpart)
    end=html.find(endpart,start)
    string=html[start:end]
    while html.find('</html>')>start>html.find('<html'):
        all_strings.append(string)
        start = html.find(startpart,end) + len(startpart)
        end = html.find(endpart, start)
        string = html[start:end]
    return all_strings

def movie_name(html):
    name=findall_in_html(html,'<span class="title">','</span>')
    for i in name:
        if 'bsp' in i:
            name.remove(i)
    return name

def movie_score(html):
    score=findall_in_html(html,'<span class="rating_num" property="v:average">','</span>')
    return score

def movie_infq(html):
    infq=findall_in_html(html,'<span class="inq">','</span>')
    return infq

def number_comment(html):
    temp=findall_in_html(html,'<div class="star">','</div>')
    num=[]
    for item in temp:
        start=item.find('<span>')+len('<span>')
        end=item.find('</span>',start)
        n=item[start:end]
        num.append(n)
    return num

def movie_data_from_html(htmls):
    movie=[]
    score=[]
    infq=[]
    number=[]
    for h in htmls:
        m=movie_name(h)
        s=movie_score(h)
        i=movie_infq(h)
        n=number_comment(h)
        movie.extend(m)
        score.extend(s)
        infq.extend(i)
        number.extend(n)
    data=zip(movie,score,infq,number)
    return data

def htmls_from_douban():
    html=[]
    for index in range(0,250,25):
        url ='https://movie.douban.com/top250?start={}&filter='
        url=url.format(index)
        r=get(url)
        html.append(r)
    return html

def get(url):
    protocol=url.split("://")[0]
    u=url.split("://")[1]
    i=u.find('/')
    host=u[:i]
    path=u[i:]

    if protocol=='https':
        s=ssl.wrap_socket(socket.socket())
        port=443
        print('use https')
    else:
        s=socket.socket()
        port=80
        print('use http')
    s.connect((host,port))

    request='GET {} HTTP/1.1\r\nhost:{}\r\n\r\n'.format(path,host)
    print('request',request)
    encoding='utf-8'
    s.send(request.encode(encoding))

    response=b''
    while True:
        r=s.recv(1024)
        response+=r
        if len(r)<1024:
            break
    response=response.decode(encoding)
    print('response',response)
    return response

def movie_log(*args,**kwargs):
    with open('movie.txt','a',encoding='utf-8') as f:
        print (*args,file=f,**kwargs)

def main():
    htmls=htmls_from_douban()
    movie_data=movie_data_from_html(htmls)
    counter=0
    for item in movie_data:
        counter=counter+1
        movie_log('No.'+str(counter))
        movie_log('电影名:' + item[0])
        movie_log('评分:' + item[1])
        movie_log('引用语:' + item[2])
        movie_log('评价人数:' + item[3],'\n\n')

main()
"""
#</editor-fold>

# import requests
# import urllib
#
# # 函数: 承运公司名到文本
# def GetComName(comCode):
#     if comCode=='shentong':
#         return '申通快递'
#     elif comCode=='zhontong':
#         return '中通快递'
#     elif comCode=='ems':
#         return 'EMS'
#     elif comCode=='huitongkuaidi':
#         return '汇通快运'
#     else:
#         return comCode
#
# # 函数: 取状态文本
# def GetStateText(num):
#     if num==0:
#         return '运输中'
#     elif num==1:
#         return '揽件'
#     elif num==2:
#         return '疑难'
#     elif num==3:
#         return '已签收'
#     elif num==4:
#         return '退回签收'
#     elif num==5:
#         return '派送中'
#     elif num==6:
#         return '退回中'
#
# p = {}
# p['text'] = input("请输入快递运单编号: ")  #比如: 227728570825
# autoComNum = requests.get("http://www.kuaidi100.com/autonumber/autoComNum", params=p)
# com = autoComNum.json()
# if com['auto'] == []:
#     print("这是一个错误的运单编号!")
#
# else:
#     print("\n---------------- 承运公司 ------------------\n")
#     i=0
#     for this in com['auto']:
#         i = i + 1
#         print( str(i) + ". " + GetComName(this['comCode']) + "\n")
#
#
#     num = input("承运公司序号: ")
#     print("\n---------------- 正在查询, 请稍等... ------------------\n")
#     data = {}
#     data['type'] = com['auto'][int(num)-1]['comCode']
#     data['postid'] =  p['text']
#     data['valicode'] = ''
#     data['id'] = 1
#     data['temp'] = '0.14881871496191512'
#     query = requests.get("http://www.kuaidi100.com/query", params=data)
#     res = query.json()
#
#     print("\n运单编号 --> " + res['nu'])
#     print("\n承运公司 --> " + GetComName(res['com']))
#     print("\n当前状态 --> " + GetStateText(int(res['state'])))
#     print("\n---------------- 跟踪信息 ------------------\n")
#     for this in res['data']:
#         print(this['time'] + "\t" + this['context'] + "\n")

#<editor-fold desc="快递查询">
'''
class Express100(object):

    company_url = "http://www.kuaidi100.com/autonumber/autoComNum"
    trace_url = "http://www.kuaidi100.com/query"

    @classmethod
    def get_json_data(cls, url, payload):
        r = requests.get(url=url, params=payload)
        return r.json()

    @classmethod
    def get_company_info(cls, express_code):

        """
        {
            comCode: "",
            num: "3351419285305",
            auto: [
                {
                    comCode: "shentong",
                    id: "",
                    noCount: 13852,
                    noPre: "33514",
                    startTime: ""
                }
            ]
        }
        """

        payload = {'text': express_code}
        data = cls.get_json_data(cls.company_url, payload)
        return data

    @classmethod
    def get_express_info(cls, express_code):
        """
        {
            message: "ok",
            nu: "3351419285305",
            ischeck: "0",
            condition: "00",
            com: "shentong",
            status: "200",
            state: "0",
            data: [
                {
                    time: "2018-01-21 22:19:45",
                    ftime: "2018-01-21 22:19:45",
                    context: "淄博市 山东淄博公司-已发往-辽宁盘锦中转部",
                    location: ""
                },
            ]
        }
        """

        company_info = cls.get_company_info(express_code)

        company_code = ""

        if company_info.get("auto", ""):
            company_code = company_info.get("auto", "")[0].get("comCode", "")

        payload = {'type': company_code, 'postid': express_code, 'id': 1}

        data = cls.get_json_data(cls.trace_url, payload)

        data.update(company_info)

        return data


if __name__ == "__main__":
    while True:
        code = input("请输入快递单号：")
        res = Express100.get_express_info(str(code).strip())
        print(json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4))
'''
# </editor-fold>

#<editor-fold desc="快递查询">
"""
import urllib2
from bs4 import BeautifulSoup
import urllib
import socket

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

'''
获取所有代理IP地址
'''


def getProxyIp():
    proxy = []
    for i in range(1, 2):
        try:
            url = 'http://www.xicidaili.com/nn/' + str(i)
            req = urllib2.Request(url, headers=header)
            res = urllib2.urlopen(req).read()
            soup = BeautifulSoup(res,'lxml')
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + "\t" + tds[2].contents[0]
                proxy.append(ip_temp)
        except:
            continue
    return proxy


'''
验证获得的代理IP地址是否可用
'''


def validateIp(proxy):
    url = "http://ip.chinaz.com/getip.aspx"
    f = open("E:\ip.txt", "w")
    socket.setdefaulttimeout(3)
    for i in range(0, len(proxy)):
        try:
            ip = proxy[i].strip().split("\t")
            proxy_host = "http://" + ip[0] + ":" + ip[1]
            proxy_temp = {"http": proxy_host}
            res = urllib.urlopen(url, proxies=proxy_temp).read()
            f.write(proxy[i] + '\n')
            print(proxy[i])
        except Exception, e:
            continue
    f.close()


if __name__ == '__main__':
    proxy = getProxyIp()
    validateIp(proxy)
"""
# </editor-fold>

# import hashlib
# import base64
# import datetime
# import json
#
# userName = 'test'  #"ZTO_1001224218"
# userPwd = 'ZTO123' #"92W64YRSV7"
# DataNow=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# # url='http://partner.zto.cn/client/interface.php'
# url='http://testpartner.zto.cn/client/interface.php'
# conten='{\"mailno\": \"73106112827648\"}'
# # conten='73106112827648'
# content=str(base64.b64encode(conten.encode('utf-8')),'utf-8')
# verify=userName+DataNow+content+userPwd
# h1 = hashlib.md5()
# h1.update(verify.encode(encoding='utf-8'))
# verify = h1.hexdigest()
#
# data={
#     'style':'json',
#     'func':'mail.trace',
#     'partner':userName,
#     'datetime':DataNow,
#     'content':content,
#     'verify':verify
# }
# response=requests.post(url,data=data)
# res=response.json()
# print(json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4))


# import os
#
# # os.walk()遍历文件夹下的所有文件
# # os.walk()获得三组数据(rootdir, dirname,filnames)
# def file_path(file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         # print(root, end=' ')    # 当前目录路径
#         # print(dirs, end=' ')    # 当前路径下的所有子目录
#         return files           # 当前目录下的所有非目录子文件
#
# data=file_path(r"\\10.10.1.249\e\rman_backup\data")
#
# rar_list=[]
#
# for i in data:
#     if i.endswith('.rar'):
#         rar_list.append(i)
#
# os.remove(r'\\10.10.1.249\e\rman_backup\data\Program_Interval_Log.txt')

# import os,shutil
# import time

# source = r'D:\test'
#
# target_dir = r'D:\\test\\'
#
# target = target_dir + time.strftime('%Y%m%d%H%M%S') + '.rar'
#
#
# rar_command = '"C:\Program Files (x86)\WinRAR\WinRAR.exe" a {0} {1}'.format(target, source)
#
# if os.system(rar_command) == 0:
#     print("成功")
# else:
#     print("失败")



# target_dir=r'\\10.10.1.249\e\rman_backup\data\\'
# target=target_dir+"data"+"1.23"+ '.rar'
# def TimeStampToTime(timestamp):
#     timeStruct = time.localtime(timestamp)
#     return time.strftime('%m.%d',timeStruct)
#
# def get_FileModifyTime(filePath):
#     t = os.path.getmtime(filePath)
#     return TimeStampToTime(t)
#
# def listdir(path):
#     filenames=" "
#     for file in os.listdir(path):
#          if get_FileModifyTime(''.join([path,"\\",file]))=="01.23":
#             filename=path+"\\"+file+" "
#             filenames+=filename
#
#     return filenames
#
# list_dir=listdir(r"\\10.10.1.249\e\rman_backup\data")
# # print(list_dir)
#
# rar_command = '"C:\Program Files (x86)\WinRAR\WinRAR.exe" a -m0 -ep1 -s -r {0} {1}'.format(target, list_dir)
# if os.system(rar_command) == 0:
#     print("成功")
# else:
#     print("失败")
# import requests
# url='https://doubanzyv1.tyswmp.com/2018/08/03/GZp3tHZkpGbQOh4W/playlist.m3u8'
# response=requests.get(url)
# print(response.text)

#<editor-fold desc="制作地图">
"""
from pyecharts import Geo
data = [
    ("海门", 9),("鄂尔多斯", 12),("招远", 12),("舟山", 12),("齐齐哈尔", 14),("盐城", 15),
    ("赤峰", 16),("青岛", 18),("乳山", 18),("金昌", 19),("泉州", 21),("莱西", 21),
    ("日照", 21),("胶南", 22),("南通", 23),("拉萨", 24),("云浮", 24),("梅州", 25)]
geo = Geo("全国主要城市空气质量", "data from pm2.5", title_color="#fff", title_pos="center",
width=1200, height=600, background_color='#404a59')
attr, value = geo.cast(data)
geo.add("", attr, value, visual_range=[0, 200], visual_text_color="#fff", symbol_size=15, is_visualmap=True)
geo.show_config()
geo.render()
"""
# </editor-fold>

# from pyecharts import Map, Geo
# # 世界地图数据
# value = [95.1, 23.2, 43.3, 66.4, 88.5]
# attr = ["China", "Canada", "Brazil", "Russia", "United States"]
#
# # 省和直辖市
# province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16, '湖南': 9,
#                          '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7, '内蒙古': 3, '重庆': 3,
#                          '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1, '舵主科技，质量保证': 1, '天津': 1,
#                          '其他': 1}
# provice = list(province_distribution.keys())
# values = list(province_distribution.values())
#
# # 城市 -- 指定省的城市 xx市
# city = ['郑州市', '安阳市', '洛阳市', '濮阳市', '南阳市', '开封市', '商丘市', '信阳市', '新乡市']
# values2 = [1.07, 3.85, 6.38, 8.21, 2.53, 4.37, 9.38, 4.29, 6.1]
#
# # 区县 -- 具体城市内的区县  xx县
# quxian = ['夏邑县', '民权县', '梁园区', '睢阳区', '柘城县', '宁陵县']
# values3 = [3, 5, 7, 8, 2, 4]
# map0 = Map("世界地图示例", width=1200, height=600)
# map0.add("世界地图", attr, value, maptype="world",  is_visualmap=True, visual_text_color='#000')
# map0.render(path="C:/Users/admin/Desktop/04-00世界地图.html")



