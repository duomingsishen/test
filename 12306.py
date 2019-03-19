# -*- coding:utf-8 -*-

import urllib,urllib2
import ssl
import cookielib
from json import loads
from cons import station
from time import sleep

stationDict={}
for i in station.split('@')[1:]:
    stationList=i.split('|')
    stationDict[stationList[1]]=stationList[2]



c=cookielib.LWPCookieJar()#生成一个存储cookie的对象
cookie=urllib2.HTTPCookieProcessor(c)
opener=urllib2.build_opener(cookie)
urllib2.install_opener(opener)


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}
ssl._create_default_https_context=ssl._create_unverified_context
train_date='2018-08-30'  #出发的时间
fromstation='长沙'
from_station=stationDict[fromstation]  #出发的城市
tostation='北京'
to_station=stationDict[tostation]           #到达的城市

def login():
    req=urllib2.Request('https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.16096980920228487')
    req.headers = headers
    imgCode=opener.open(req).read()
    with open('code.png','wb') as fn:
        fn.write(imgCode)

    req=urllib2.Request('https://kyfw.12306.cn/passport/captcha/captcha-check')
    req.headers=headers
    code=raw_input('请输入验证码:')
    data={
        'answer':code,
        'login_site':'E',
        'rand':'sjrand'
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data).read()
    req=urllib2.Request('https://kyfw.12306.cn/passport/web/login')
    data={
        'username':'cai345408904',
        'password':'cai15928021496',
        'appid':'otn'
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data).read()
    result=loads(html)
    if result['result_code']==0:
        print '登录成功'
        return True
    print '登陆失败,正在重新登录'
    sleep(5)
    login()

login()

def check():
    req=urllib2.Request('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT'%(train_date,from_station,to_station))
    req.headers=headers
    html=opener.open(req).read()
    reslut=loads(html)
    return reslut['data']['result']


index=0
for i in check():
    tmpList=i.split('|')
    # print tmpList
    # for n in tmpList:
    #     print index,n
    #     index+=1
    # break

    try:
        if tmpList[23]==u'有' or int(tmpList[23])>0:
            print u'''
            该车次有票
            车次:%s
            出发时间:%s
            到达时间:%s
            历时:%s
            余票:%s
            '''%(tmpList[3],tmpList[8],tmpList[9],tmpList[10],tmpList[23])
            break
    except:
        continue


def buyTickets():
    req=urllib2.Request('https://kyfw.12306.cn/passport/web/auth/uamtk')
    req.headers=headers
    data={
        'appid':'otn'
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    reslut=loads(html)
    print reslut
    req=urllib2.Request('https://kyfw.12306.cn/otn/uamauthclient')
    req.headers=headers
    data={
        'tk':reslut['newapptk']
    }
    data = urllib.urlencode(data)
    html = opener.open(req, data=data).read()
    print 1003,html

    req=urllib2.Request('https://kyfw.12306.cn/otn/login/checkUser')
    req.headers=headers
    data={
        '_json_att':''
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    print 1001,html

    req=urllib2.Request('https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest')
    req.headers=headers
    data={
        'secretStr':tmpList[0],
        'train_date':train_date,
        'back_train_date':'2018-08-10',
        'tour_flag':'dc',
        'purpose_codes':'ADULT',
        'query_from_station_name':fromstation,
        'query_to_station_name':tostation,
        'undefined':'',
    }
    data = urllib.urlencode(data)
    html = opener.open(req, data=data)
    print 1002,html.geturl()
buyTickets()




