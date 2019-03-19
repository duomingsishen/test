# coding:utf-8

# import urllib2
# import re
# import threading
# import time
#
# def getlist():
#     html=urllib2.urlopen('http://www.biqugeso.com/book/10130/')
#     text=html.read().decode('gbk').encode('utf-8')
#     reg=r'<dd class="col-md-3"><a href=[\"\'](.*?)[\"\'] title=.*?>(.*?)</a></dd>'
#     reg=re.compile(reg)
#     urls=re.findall(reg,text)
#     return urls
#
# def getcontent(url,filename):
#     html=urllib2.urlopen('http://www.biqugeso.com/book/10130/%s' %url).read().decode('gbk').encode('utf-8')
#     reg=r'<div class="panel-body" id="htmlContent">(.*?)<script'
#     reg=re.compile(reg,re.S)
#     text=re.findall(reg,html)[0]
#     f = open('xiaoshuo.txt', 'ab+')
#     f.write(filename)
#     f.write('\n')
#     f.write(text)
#     f.close()
#     print url
#
#
# for i in getlist():
#     t=threading.Thread(target=getcontent,args=(i[0],i[1]))
#     t.start()
#     time.sleep(0.7)
#     # getcontent(i[0],i[1])

