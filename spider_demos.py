# coding:utf-8

import urllib,urllib2
import cookielib
from json import loads

c=cookielib.LWPCookieJar()
cookie=urllib2.HTTPCookieProcessor(c)
opener=urllib2.build_opener(cookie)
urllib2.install_opener(opener)

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Referer': 'http://cx.cnca.cn/rjwcx/cxAuthenticationResult/index.do',
}

def getList():
    req=urllib2.Request('http://cx.cnca.cn/rjwcx/cxAuthenticationResult/queryOrg.do?progId=10')
    req.headers=headers
    with open('code.png','wb')as f:
        f.write(opener.open('http://cx.cnca.cn/rjwcx/checkCode/rand.do?d=1526092382982','code.png').read())
    code=input('请输入验证码:')
    data={
        'certNumber':'',
        'orgName':'漳州灿坤实业有限公司',
        'queryType':'public',
        'checkCode':code,
    }
    data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    result=loads(html)
    return result['data'],code

def getCertList(orgName,orgCode,checkC,code):
    req=urllib2.Request('http://cx.cnca.cn/rjwcx/cxAuthenticationResult/list.do?progId=10')
    req.headers=headers
    data={
        'orgName':orgName,
        'orgCode':orgCode,
        'method':'queryCertByOrg',
        'needCheck':'false',
        'checkC':checkC,
        'randomCheckCode':code,
        'queryType':'public',
        'page': '1',
        'rows': '10',
        'checkCode':'',
    }
    data=data=urllib.urlencode(data)
    html=opener.open(req,data=data).read()
    result=loads(html)
    return result['rows']

def getCertInfo(rzjgId,certNo,checkC):
    req=urllib2.Request('http://cx.cnca.cn/rjwcx/cxAuthenticationResult/show.do?rzjgId={}&certNo={}&checkC={}'.format(rzjgId,certNo,checkC))
    req.headers=headers
    html=opener.open(req).read()
    print html


c_list,code=getList()
for i in c_list:
    for n in getCertList(i['orgName'].encode('utf-8'),i['orgCode'],i['checkC'],code):
        getCertInfo(n['rzjgId'],n['certNumber'],n['checkC'])
        break
