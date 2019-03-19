# coding:utf-8

import urllib2
from json import loads
import re

def getlist():
    response=urllib2.urlopen('https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8')
    html=response.read().decode('gbk').encode('utf-8')
    dict=loads(html)
    return dict['data']['searchDOList']

def getPhoto(url):
    res=urllib2.urlopen('https://%s' %url)
    html=res.read().decode('gbk').encode('utf-8')
    print html

def getAlbumList(userId):
    res=urllib2.urlopen('https://mm.taobao.com/self/album/open_album_list.htm?charset=utf-8&user_id%%20=%s'%userId)
    html=res.read().decode('gbk').encode('utf-8')
    reg=r'<a class="mm-first" href="//(.*?)" target="_blank">'
    albumUrl=re.findall(reg,html)
    for url in albumUrl[::2]:
        getPhoto(url)

for i in getlist():
    userId=i['userId']
    getAlbumList(userId)
