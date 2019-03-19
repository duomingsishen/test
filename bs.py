# coding:utf-8

import requests
import re
import urllib
import os

def get_response(url):
    hd = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    response=requests.get(url,headers=hd).text
    return response #返回网页源代码


def get_content(html): #在这个函数里面解析出来包含视频的html
    reg=re.compile(r'(<div class="j-r-list-c">.*?</div>.*?</div>)',re.S)
    return re.findall(reg,html)

def get_mp4_url(response):
    reg=r'data-mp4="(.*?)"'
    return re.findall(reg,response)

def get_mp4_name(response):
    reg=re.compile('<a href="/detail-.{8}?.html">(.*?)</a>')
    return re.findall(reg,response)

def download_mp4(mp4_url,path):
    path=' '.join(path.split())
    path='D:\\video\\{}.mp4'.format(path.decode('utf-8').encode('gbk'))#视频的存储路径
    if not os.path.exists(path):
        urllib.urlretrieve(mp4_url,path)#下载视频 第一种方法
        print 'ok...'
    # content=get_response(mp4_url)
    # with open(path,'wb') as f:
    #     f.write(content)
    else:
        print 'no...'

def get_url_name(start_url):
    content = get_content(get_response(start_url))
    for i in content:
        mp4_url = get_mp4_url(i)
        if mp4_url:
            mp4_name = get_mp4_name(i)
            download_mp4(mp4_url[0], mp4_name[0])

def main():
    for start_url in start_urls:
        get_url_name(start_url)


if __name__=="__main__":
    start_urls=['http://www.budejie.com/video/{}'.format(i) for i in range(1,10)]
    main()


