# coding:utf-8

#<editor-fold desc="bs4的使用">
'''
# from bs4 import BeautifulSoup
# import bs4
#
# html_str = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
# <p class="story">...</p>
# """
#
# soup=BeautifulSoup(html_str,'lxml',from_encoding='utf-8')
# soup=BeautifulSoup(open('index.html'))  #打开html文件读取
# print soup.prettify()
# print soup.title
# print soup.a
# print soup.p
# print soup.name
# print soup.title.name

# soup.title.name='mytitle'
# print soup.title
# print soup.mytitle

# print soup.p['class']
# print soup.p.get('class')
# print soup.p.attrs

# soup.p["class"]="myClass"
# print soup.p


# print soup.p.string
# print type(soup.p.string)

# unicode_string=unicode(soup.p.string)

# print type(soup.name)
# print soup.name
# print soup.attrs

# print soup.a.string
# print type(soup.a.string)

# if type(soup.a.string)==bs4.element.Comment:
#     print soup.a.string

# print soup.head.contents
# print len(soup.head.contents)
# print soup.head.contents[0].string

# for child in soup.head.children:
#     print child

# for child in soup.head.descendants:
#     print child

# print soup.head.string
# print soup.title.string
# print soup.html.string

# for string in soup.strings:
#     print repr(string)


# for string in soup.stripped_strings:
#     print repr(string)

# print soup.title
# print soup.title.parent


# print soup.a
# for parent in soup.a.parents:
#     if parent is None:
#         print parent
#     else:
#         print parent.name

# print soup.p.next_sibling
# print soup.p.prev_sibling
# print soup.p.next_sibling.next_sibling

# for sibling in soup.a.next_siblings:
#     print repr(sibling)

# print soup.head
# print soup.head.next_element

# for element in soup.a.next_elements:
#     print repr(element)

# print soup.find_all('b')

# import re
# for tag in soup.find_all(re.compile("^b")):
#     print tag.name

# print soup.find_all(["a","b"])

# for tag in soup.find_all(True):
#     print tag.name

# def hasClass_Id(tag):
#     return tag.has_attr('class') and tag.has_attr('id')
# print soup.find_all(hasClass_Id)
#
# print soup.find_all(id='link2')

# import re
# print soup.find_all(href=re.compile("elsie"))

# print soup.find_all(id=True)

# print soup.find_all("a",class_="sister")

# print soup.find_all(href=re.compile("elsie"),id='link1')

# data_soup=BeautifulSoup('<div> data-foo="value">foo!</div>')
# data_soup.find_all(attrs={"data-foo":"value"})

# print soup.find_all(text="Elsie")
# print soup.find_all(text=["Tillie","Elsie","Lacie"])
# print soup.find_all(text=re.compile("Dormouse"))

# print soup.find_all("a",text="Elsie")

# print soup.find_all("a",limit=2)

# print soup.find_all("title")
# print soup.find_all("title",recursive=False)


# #直接查找title标记
# print soup.select("title")
# #逐层查找title标记
# print soup.select("html head title")
# #查找直接子节点
# #查找head下的title标记
# print soup.select("head > title")
# #查找p下的id="link1"的标记
# print soup.select("p > #link1")
# #查找兄弟节点
# #查找id="link1"之后class=sister的所有兄弟标记
# print soup.select("#link1 ~ .sister")
# #查找紧跟着id="link1"之后class=sister的子标记
# print soup.select("#link1 + .sister")


# print soup.select(".sister")
# print soup.select("[class~=sister]")


# print soup.select("#link1")
# print soup.select("a#link2")

# print soup.select('a[href]')

# print soup.select('a[href="http://example.com/elsie"]')
# print soup.select('a[href^="http://example.com/"]')
# print soup.select('a[href$="tillie"]')
# print soup.select('a[href*=".com/el"]')
'''
#</editor-fold>

#<editor-fold desc="Email的发送">
'''
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr

import smtplib

def _format_addr(s):
    name,addr=parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))

#发货人地址
from_addr='wuxu@iningmei.com'
#邮箱密码
password='Ningmei2016'
#收件人地址
to_addr='360361689@qq.com'
#企业邮箱服务器地址
smtp_server='smtp.exmail.qq.com'
#设置邮件信息
# msg=MIMEText('Python爬虫运行异常,异常信息为遇到HTTP 403','plain','utf-8')
#发送HTML邮件的异常网页信息时
msg=MIMEText('<html><body><h1>Hello</h1>'+'<p>异常网页<a href="http://www.cnblogs.com">cnblogs</a>...</p>'+'</body></html>','html','utf-8')
msg['From']=_format_addr('一号爬虫<%s>' % from_addr)
msg['To']=_format_addr('管理员 <%s>' % to_addr)
msg['Subject']=Header('一号爬虫运行状态','utf-8').encode()
#发送邮件
server=smtplib.SMTP(smtp_server,25)
server.login(from_addr,password)
server.sendmail(from_addr,[to_addr],msg.as_string())
server.quit()
'''
#</editor-fold>

#<editor-fold desc="HTML下载器">
"""
import requests
class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None
        user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        headers={'User-Agent':user_agent}
        r=requests.get(url,headers=headers)
        if r.status_code==200:
            r.encoding='utf-8'
            return r.text
        return None
"""
#</editor-fold>

#<editor-fold desc="HTML解析器">
"""
import re
import urlparse
from bs4 import BeautifulSoup


class HtmlParser(object):

    def parser(self,page_url,html_cont):
        '''
        用于解析网页内容,抽取URL和数据
        :param page_url:下载页面的URL
        :param html_cont:下载的网页内容
        :return:返回URL和数据
        '''
        if page_url is None or html_cont is None:
            return
        soup=BeautifulSoup(html_cont,'html.parser')
        new_urls=self._get_new_urls(page_url,soup)
        new_data=self._get_new_data(page_url,soup)
        return new_urls,new_data

    def _get_new_urls(self,page_url,soup):
        '''
        抽取新的URL集合
        :param page_url:下载页面的URL
        :param soup: soup
        :return: 返回新的URL集合
        '''
        new_urls=set()
        #抽取符合要求的a标记
        links=soup.find_all('a',herf=re.compile(r'/view/\d+\.htm'))
        for link in links:
            #提取href属性
            new_url=link['href']
            #拼接成完整网址
            new_full_url=urlparse.urljoin(page_url,new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self,page_url,soup):
        '''
        抽取有效数据
        :param page_url: 下载页面的URL
        :param soup:
        :return: 返回有效数据
        '''
        data={}
        data['url']=page_url
        title=soup.find('dd',class_='lemmaWgt-lemmaTitle-title').find('h1')
        data['title']=title.get_text()
        summary=soup.find('div',class_='lemma-summary')
        #获取tag中包含的所有文本内容,包括子孙tag中的内容,并将结果作为Unicode字符串返回
        data['summary']=summary.get_text()
        return data
"""
#</editor-fold>

#<editor-fold desc="爬虫调度器">
"""
import time
class SpiderMan(object):
    def __init__(self):
        self.downloader=HtmlDownloader()
        self.parser=HtmlParser()

    def crawl(self,root_url):
        content=self.downloader.download(root_url)
        urls = self.parser.parser_url(root_url, content)
        # 构造一个获取评分和票房链接
        for url in urls:
            try:
                t = time.strftime("%Y%m%d%H%M%S3282", time.localtime())
                rank_url ='http://service.library.mtime.com/Movie.api' \
                        '?Ajax_CallBack=true' \
                        '&Ajax_CallBackType=Mtime.Library•Services' \
                        '&Ajax„CallBackMethod=GetMovieOverviewRating' \
                        '& Ajax_CrossDomain = 1' \
                        '& Ajax—RequestUrl = %s' \
                        '&t=%s' \
                        '&Ajax_CallBackArgument0 = % s' % (url[0], t, url[1])
                rank_content = self.downloader.download(rank_url)
                data = self.parser.parser_json(rank_url,rank_content)

            except Exception, e:
                print "Crawl failed"
        print "Crawl finish"

if __name__ == '__main__':
    spider = SpiderMan()
    spider .crawl ('http://theater.mtime.com/China _ Beijing/')
"""
#</editor-fold>

#<editor-fold desc="selenium的使用">
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver=webdriver.Chrome()
driver.get('http://www.baidu.com')
assert u"百度" in driver.title
elem=driver.find_element_by_name("wd")
elem.clear()
elem.send_keys(u"网络爬虫")
elem.send_keys(Keys.RETURN)
time.sleep(3)
assert u"网络爬虫." not in driver.page_source
driver.close()
"""
#</editor-fold>

#<editor-fold desc="selenium的爬取实例">
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import codecs
import datetime

class QunaSpider(object):

    def get_hotel(self, driver, to_city, fromdate, todate):

        ele_toCity = driver.find_element_by_name('toCity')
        ele_fromDate = driver.find_element_by_id('fromDate')
        ele_toDate = driver.find_element_by_id('toDate')
        ele_search = driver.find_element_by_class_name('search-btn')
        ele_toCity.clear()
        ele_toCity.send_keys(to_city)
        ele_toCity.click()
        ele_fromDate.clear()
        ele_fromDate.send_keys(fromdate)
        ele_toDate.clear()
        ele_toDate.send_keys(todate)
        ele_search.click()
        page_num = 0
        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.title_contains(unicode(to_city))
                )
            except Exception, e:
                print e
                break
            time.sleep(5)

            js = "window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(js)
            time.sleep(5)

            htm_const = driver.page_source
            soup = BeautifulSoup(htm_const,"html.parser")
            infos = soup.find_all(class_="item_hotel_info")
            f = codecs.open(unicode(to_city)+unicode(fromdate) + u'.html','a','utf-8')
            for info in infos:
                f.write(str(page_num) + '--'*20)
                content = info.get_text().replace(" ","").replace("\t","").strip()
                for line in [ln for ln in content.splitlines() if ln.strip()]:
                    f.write(line)
                    f.write('\r\n')
            f.close()
            try:
                next_page = WebDriverWait(driver, 10).until(
                EC.visibility_of(driver.find_element_by_css_selector(".item.next"))
                )
                next_page.click()
                page_num += 1
                time.sleep(10)
            except Exception, e:
                print e
                break

    def crawl(self, root_url, to_city):

        today = datetime.date.today().strftime('%Y-%m-%d')
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tomorrow.strftime('%Y-%m-%d')
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(50)
        driver.get(root_url)
        driver.maximize_window()  # 将浏览器最大化显示
        driver.implicitly_wait(10) #控制间隔时间，等待浏览器反映
        self.get_hotel(driver,to_city,today,tomorrow)

if __name__ == '__main__':
    spider=QunaSpider()
    spider.crawl('http://hotel.qunar.com/',u'上海')
"""
#</editor-fold>

#<editor-fold desc="post登陆百度云">
"""
import base64
import json
import re
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import PyV8
from urllib import quote
import requests
import time

if __name__ == '__main__':
    s=requests.Session()
    s.get('http://yun.baidu.com')
    js='''
    function callback(){
        return 'bd__cbs__'+Math.floor(2147483648 * Math.random()).toString(36)
    }
    function gid(){
        return 'xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (e) {
        var t = 16 * Math.random() | 0,
        n= 'x' ==e?t : 3&t | 8;
        return n.toString(16)
        }).toUpperCase()
    }
    '''
    ctxt = PyV8.JSContext()
    ctxt.enter()
    ctxt.eval(js)
    ########### 获取 gid############################# 3
    gid = ctxt.locals.gid()
    ###########	callback############################# 3
    callback1 = ctxt.locals.callback()
    ########### 获取 token############################# 3
    tokenUrl = "https://passport.baidu.com/v2/api/?getapi&tpl=netdisk&subpro=netdisk__web&apiver=v3" \
               "&tt=%d&class =login&gid=%s&logintype=basicLogin&callback=%s"%(time.time()*1000,gid,callback1)

    token_response = s.get(tokenUrl)
    pattern = re.compile(r'"token"\s*:\s*"(\w+)"')
    match = pattern.search(token_response.text)
    if match:
        token = match.group(1)
    else:
        raise Exception
    ###########	callback############################# 3
    callback2 = ctxt.locals.callback()
    ########### 获取 rsakey 和 pubkey############################# 3
    rsaUrl = "https://passport.baidu.com/v2/getpublickey?token=%s&" \
            "tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=%d&gid=%s&callback=%s"%(token,time.time()*1000,gid,callback2)
    rsaResponse = s.get(rsaUrl)
    pattern = re.compile("\"key\"\s*:\s*'(\w+)'")
    match = pattern.search(rsaResponse.text)
    if match:
        key = match.group(1)
        print key
    else:
        raise Exception
    pattern = re.compile("\"pubkey\":'(.+?)'")
    match = pattern.search(rsaResponse.text)
    if match:
        pubkey = match.group(1)
        print pubkey
    else:
        raise Exception
    ################ 加密 password######################## 3
    password = 'worinima0514' #填上自己的密码
    pubkey = pubkey.replace('\\n','\n').replace('\\','')
    rsakey = RSA.importKey(pubkey)
    cipher = PKCS1_v1_5.new(rsakey)
    password = base64.b64encode(cipher.encrypt(password))
    print password
    ########### 获取 callback############################# 3
    callback3 = ctxt.locals.callback()
    data = {
    'apiver':'v3',
    'charset':'utf-8',
    'countrycode':'',
    'crypttype':12,
    'detect':1,
    'foreignusername':'',
    'idc':'',
    'isPhone':'',
    'logLoginType':'pc_loginBasic',
    'loginmerge':True,
    'logintype':'basicLogin',
    'mem_pass':'on',
    'quick_user':0,
    'safeflg':0,
    'staticpage':'http://yun.baidu.com/res/static/thirdparty/pass_v3_jump.html',
    'subpro':'netdisk_web',
    'tpl':'netdisk',
    'u':'http://yun.baidu.com/',
    'username':'qqqqq360361689',  # 填上自己的用户名
    'callback':'parent.'+callback3,
    'gid':gid,'ppui_logintime':71755,
    'rsakey':key,
    'token':token,
    'password':password,
    'tt':'%d'%(time.time()*1000),
    }
    ########### 第一次 post############################# 3
    post1_response = s.post('https://passport.baidu.com/v2/api/?login' ,data=data)
    pattern = re.compile("codeString=(\w+)&")
    match = pattern.search(post1_response.text)
    if match:
        ########### 获取 codestring############################# 3
        codeString = match.group(1)
        print codeString
    else:
        raise Exception
    data['codestring']= codeString
    ############# 获取验证码###################################
    verifyFail = True
    while verifyFail:
        genimage_param = ''
        if len(genimage_param) == 0:
            genimage_param = codeString
        verifycodeUrl = "https://passport.baidu.com/cgi-bin/genimage?%s"%genimage_param
        verifycode = s.get(verifycodeUrl)
        ############# 下载验证码###################################
        with open('verifycode.png','wb') as codeWriter:
            codeWriter.write(verifycode.content)
            codeWriter.close()
        ############# 输入验证码###################################
        verifycode = raw_input("Enter your input verifycode：")
        callback4 = ctxt.locals.callback()
        ############# 检验验证码###################################
        checkVerifycodeUrl ='https://passport.baidu.com/v2/?' \
                'checkvcode&token=%s' \
                '&tpl=netdisk&subpro=netdisk_web&apiver=v3&tt=%d' \
                '&verifycode=%s&codestring=%s' \
                '&callback=%s'%(token,time.time()*1000,quote(verifycode),
                codeString, callback4)
        print checkVerifycodeUrl
        state = s.get(checkVerifycodeUrl)
        print state.text
        if state.text.find(u'验证码错误')!=-1:
            print '验证码输入错误...已经自动更换...'
            callback5 = ctxt.locals.callback()
            changeVerifyCodeUrl = "https://passport.baidu.com/v2/?reggetcodestr" \
                                  "&token=%s" \
                                  "&tpl=netdisk&subpro=netdisk_web&apiver=v3" \
                                  "&tt=%d&fr=login&" \
                                  "vcodetype=de94eTRcVzlGvhJFsiK5G+ni2k2Z78PYR xUaRJLEmxdJ05ftPhviQ3/JiT9vezbFtwCyqdkNWSP29oeOvYE0SYPocOGL+iTafSv8pw" \
                                  "&callback=%s"%(token,time.time()*1000, callback5)
            print changeVerifyCodeUrl
            verifyString = s.get(changeVerifyCodeUrl)
            pattern = re.compile('"verifyStr"\s*:\s*"(\w+)"')
            match = pattern.search(verifyString.text)
            if match:
            ########### 获取 verifyString############################# 3
                verifyString = match.group(1)
                genimage_param = verifyString
                print verifyString
            else:
                verifyFail = False
                raise Exception
        else:
            verifyFail = False
        data['verifycode'] = verifycode
        ########### 第二次 post############################# 3
        data['ppui_logintime']=81755
        ####################################################
        # 特地说明，大家会发现第二次的post出去的密码是改变的，为什么我这里没有变化呢？
        # 是因为RSA加密，加密密钥和密码原文即使不变，每次加密后的密码都是改变的，RSA有随机因子 的关系
        # 所以我这里不需要在对密码原文进行第二次加密了，直接使用上次加密后的密码即可，是没有问题的。
        ###########################################################################
        post2_response = s.post('https://passport.baidu.com/v2/api/?login',data=data)
        if post2_response.text.find('err_no=0')!=-1:
            print '登录成功'
        else:
            print '登录失败'
"""
#</editor-fold>

#<editor-fold desc="验证码识别">
"""
from pytesseract import *
from PIL import Image

image=Image.open('code.png')
#设置tesseract的安装路径
pytesseract.tesseract_cmd='D:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
code=pytesseract.image_to_string(image)
print code
"""
#</editor-fold>

#<editor-fold desc="爬虫">
"""
import requests
class SpiderDownloader(object):
    def download(self,url):
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (WindowsNT 6.1; WOW64) AppleWebKit/537 - 36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36'
        headers={'User-Agent':user_agent}
        r = requests.get(url,headers=headers)
        if r.status_code==200:
            r. encoding='utf-8'
            return r.text
        return None



import json
class SpiderParser(object):

    def get_kw_cat(self, response):
        '''
        获取分类下的曲目
        :param response:
        :return:
        '''
        try:
            kw_json = json.loads(response, encoding='utf-8')
            cat_info = []
            if kw_json["sign"] is not None:
                if kw_json["list"] is not None:
                    for data in kw_json["list"]:
                        id = data["Id"]
                        name= data["Name"]
                        cat_info.append({'id':id,'cat_name':name})
                    return cat_info
        except Exception,e:
            print e

    def get_kw_detail(self,response):
        '''
        获取某一曲目的详细信息
        :param response:
        :return:
        '''
        detail_json = json.loads(response, encoding='utf-8')
        details=[]
        for data in detail_json["Chapters"]:
            if data is None:
                return
            else:
                try:
                    file_path = data["Path"]
                    name =data["Name"]
                    file_id =str(data["Id"])
                    details.append ({'file_id':file_id,'name':name,'file_path':file_path})
                except Exception,e:
                    print e
        return details


import codecs
class SpiderDataOutput(object):
    def __init__(self):
        self.filepath='kuwo.html'
        self.output_head(self.filepath)

    def output_head(self,path):
        '''
        将HTML头写进去
        :param path:
        :return:
        '''
        fout=codecs.open(path,'w',encoding='utf-8')
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        fout.close()

    def output_html(self,path,datas):
        '''
        将数据写入HTML文件中
        :param self:
        :param path: 文件路径
        :param datas:
        :return:
        '''
        if datas==None:
            return
        fout=codecs.open(path,'a',encoding='utf-8')
        for data in datas:
            fout.write("<tr>")
            fout.write ("<td>%s</td>"%data['file_id'])
            fout.write ("<td>%s</td>"%data['name'])
            fout.write("<td>%s</td>"%data['file_path'])
            fout.write("</tr>")
        fout.close()

    def ouput_end(self,path):
        '''
        输出HTML结束
        :param self:
        :param path: 文件存储路径
        :return:
        '''
        fout=codecs.open(path,'a',encoding='utf-8')
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()


class SpiderMan(object):

    def __init__(self):
        self.downloader = SpiderDownloader()
        self.parser = SpiderParser()
        self.output = SpiderDataOutput()
    def crawl(self,root_url):
        content = self.downloader.download(root_url)
        for info in self.parser.get_kw_cat(content):
            print info
            cat_name=info['cat_name']
            detail_url ='http://ts.kuwo.cn/service/getlist.v31.php?act=detail&id=%s'%info['id']
            content = self.downloader.download(detail_url)
            details = self.parser.get_kw_detail(content)
            print detail_url
            self.output.output_html(self.output.filepath,details)
        self.output.ouput_end(self.output.filepath)


if __name__ == '__main__':
    spider = SpiderMan()
    spider.crawl('http://ts.kuwo.cn/service/getlist.v31.php?act=cat&id=50')
"""
#</editor-fold>

# import cx_Oracle                                          #引用模块cx_Oracle
# conn=cx_Oracle.connect('NMKMESSUPPORT/123@Nmgd.com@10.10.1.249:1521/MESDB')    #连接数据库
# c=conn.cursor()                                           #获取cursor
# x=c.execute('select sysdate from dual')                   #使用cursor进行各种操作
# x.fetchone()
# c.close()                                                 #关闭cursor
# conn.close()                                              #关闭连接

# from pybloom import BloomFilter
# f=BloomFilter(capacity=1000,error_rate=0.001)
# print [f.add(x) for x in range(10)]
# print 11 in f
# print 4 in f

# from pybloom import ScalableBloomFilter
# sbf=ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
# count=10000
# for i in xrange(0,count):
#     sbf.add(i)
# print 10001 in sbf
# print 4 in sbf

#<editor-fold desc="redis建立连接">
"""
import redis
r=redis.Redis(host='127.0.0.1',port=6379)
r.set('name','qiye')
print r.get('name')
pool=redis.ConnectionPool(host='127.0.0.1',port=6379)
r=redis.Redis(connection_pool=pool)
r.set('name','qiye')
print r.get('name')
"""
#</editor-fold>

#<editor-fold desc="redis的使用">
"""
import time
import redis
pool=redis.ConnectionPool(host='127.0.0.1',port=6379)
r=redis.Redis(connection_pool=pool)
r.set('name','qiye',ex=3)
r.setnx('name','hah')
r.setex('name','qiye',5)
r.psetex('name',5000,'qiye')
print r.getset('name','hello')
r.set('name','qiye安全博客')
print r.getrange('name',4,9)

r.setrange('name',1,'python')
print r.get('name')

from binascii import hexlify
r.set('name','qiye')
print bin(int(hexlify('qiye'),16))
r.setbit('name',2,0)
print r.get('name')
print bin(int(hexlify(r.get('name')),16))
print r.getbit('name',2)
print r.bitcount('name',0,1)
print r.strlen('name')
r.append('name','python')
r.hset('student','name','qiye')
r.hmset('student',{'name':'qiye','age':20})
r.hget('student','name')
print r.hmget('student',['name','age'])
print r.hmget('student','name',)

r.lpush('digit',11,22,33)
r.linsert('digit','before','22','aa')
r.lset('digit',4,44)
r.lrem('digit','22',1)
r.lpop('digit')
r.sadd('num',33,44,55,66)
r.scard(name)
r.smembers(name)
print (r.sdiff('num1','num2'))
print (r.sinter('num1','num2'))
print (r.sunion('num1','num2'))

r.zadd('z_num',num1=11,num2=22)

print r.zcard('z_num')

print r.zrange('z_num',0,10)
r.zrem('z_num',['num1','num2'])

print (r.zscore('z_num','num1'))
"""
#</editor-fold>

#<editor-fold desc="学习记录">
"""
# import urllib.request
# import urllib.parse
#
# data=bytes(urllib.parse.urlencode({'word':'hello'}),encoding='utf-8')
#
# print(data)
# response=urllib.request.urlopen('http://httpbin.org/post',data=data)
# print(response.read())

# import urllib.request
# response=urllib.request.urlopen('http://httpbin.org/get',timeout=1)
# print(response.read())

# import socket
# import urllib.request
# import urllib.error
#
# try:
#     response=urllib.request.urlopen('http://httpbin.org/get',timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason,socket.timeout):
#         print('TIME OUT')
"""
#</editor-fold>

#<editor-fold desc="ERP数据转到MES">
"""
# import os
# import pymysql
# import cx_Oracle
# import threading


def get_data():
    conn=pymysql.connect(
        host="192.168.50.220",
        user='mayn-erp',
        password='mayn',
        database='db-mayn-erp-prd',
        port=3306,
        charset='utf8'  #针对中文数据
    )
    cursor=conn.cursor()  #创建游标
    #查询数据
    sql='SELECT MP_ID,MP_MATERIALS_ID,MP_MATERIALS_CODE,MP_PICTURE,MP_DEL from materials_picture'
    cursor.execute(sql)
    data=cursor.fetchall()
    #插入数据
    # sql="insert into user(username,age,password) values('王五',20,'123789')"
    # cursor.execute(sql)
    # conn.commit()   #更新表数据的提交
    # conn.rollback() #撤销更新表的数据
    cursor.close()  #关闭游标
    return data


def update_data(*args):
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决乱码问题
    conn = cx_Oracle.connect('NMKMESSUPPORT', '123@Nmgd.com', '10.10.1.249:1521/mesdb')   #这步不报错就是连上啦
    cursor = conn.cursor()
    sql ="insert into BAS_MATERIAL_PICTURE (MP_ID,MP_MATERIALS_ID,MP_MATERIALS_CODE,MP_PICTURE,MP_DEL) VALUES ('{}','{}','{}','{}','{}')".format(args[0],args[1],args[2],args[3],args[4])
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()



for infos in get_data():
    i=[]
    # id=i[0]
    # name=i[1]
    # grpid=i[2]
    # rmdel=i[3]
    # dttime=i[4]
    # by=i[5]
    # mu=i[6]
    # type=i[7]
    for info in infos:
        if info==None:
            info=''
        i.append(info)
    id=i[0]
    name=i[1]
    grpid=i[2]
    rmdel=i[3]
    dttime=i[4]
    # by=i[5]
    # mu=i[6]
    # type=i[7]
    # cu=i[8]
    t1=threading.Thread(target=update_data,args=(id,name,grpid,rmdel,dttime,))
    t1.start()
    t1.join()

"""
#</editor-fold>

#<editor-fold desc="数据导入">
"""
# import pandas as pd
# from pandas import Series,DataFrame
# import numpy as np
# import matplotlib.pyplot as plt
# import pymysql
# from sqlalchemy import create_engine
#
# from tkinter import *
# from tkinter import filedialog
# import tkinter.messagebox
#
# root=Tk()
# root.title('导入工具')
# # file_path=filedialog.askopenfile()
# e1=Entry(root,font=('Arial', 14),width=25)
# e1.grid(row=0,column=0)
# def get_file():
#     file_path=filedialog.askopenfile(filetypes=[("excel file",["*.xls","*.xlsx"])])
#     if file_path!=None:
#         e1.insert('insert',file_path.name)
#
# def Add_file(filename):
#     df=pd.read_excel(r'%s'%filename,header=0)
#     connect=create_engine('mysql+pymysql://mayn-erp:mayn@192.168.50.210:3306/db_mayn_erp_int?charset=utf8')
#     df.to_sql(name='purchase_stock_20190115',con=connect,if_exists='append',index=False)
#     tkinter.messagebox.showinfo(title='提示', message='导入成功')
#
# b1 =Button(root, text='选择文件', width=10,height=2,command=get_file)
# b1.grid(row=0,column=1)
#
# b2=Button(root,text='导入',width=10,height=2,command=lambda :Add_file(e1.get()))
# b2.grid()
# sw = root.winfo_screenwidth()
# sh = root.winfo_screenheight()
# x = (sw-380) / 2
# y = (sh-100) / 2
# root.geometry("%dx%d+%d+%d" %(380,100,x,y))
# # root.geometry('380x100')
# root.mainloop()

"""
#</editor-fold>

#<editor-fold desc="oracle插入图片">
'''
# import requests
# #<editor-fold desc="MES发货查询">
#
# import os
# import cx_Oracle
# def get_data():
#     os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决乱码问题
#     conn = cx_Oracle.connect('NMKMESSUPPORT', '123@Nmgd.com', '10.10.1.249:1521/mesdb')   #这步不报错就是连上啦
#     cursor = conn.cursor()
#     sql ="""select *from BAS_MATERIAL_PICTURE where MP_MATERIALS_CODE='105INN0750TI2G0' """
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return data
#
# #</editor-fold>
#
# def Add_item(itemno,bytes):
#     os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 解决乱码问题
#     conn = cx_Oracle.connect('NMKMESSUPPORT', '123@Nmgd.com', '10.10.1.249:1521/mesdb')  # 这步不报错就是连上啦
#     cursor = conn.cursor()
#     sql = """insert into BAS_ITEMIMG(ID,ITEMNO,LMG) VALUES (1,'{}',:blobData)""".format(itemno)
#     cursor.setinputsizes(blobData=cx_Oracle.BLOB)
#     cursor.execute(sql, {'blobData':bytes})
#     conn.commit()
#     cursor.close()
#     conn.close()
#
# for i in get_data():
#     response=requests.get(i[3])
#     imgbytes=response.content
#     Add_item(i[2],imgbytes)
#     break
'''
#</editor-fold>

#<editor-fold desc="pandas数据库写入和读取">
# '''
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
import pymysql
from sqlalchemy import create_engine

#销售额订单
sql="""
SELECT  	so.SO_TRADE_ACTIVE_ID,
  SUM(so.SO_PAYMENT_TOTAL) AS TOTAL
 ,sum(so.SO_COST)  as COST
FROM
shop_order so
left JOIN shop_order_sale sos ON sos.SOS_SO_IS_SALES = so.SO_IS_SALES
left JOIN shop_order_trade_status sots ON so.SO_SOTS_ID = sots.SOTS_NAME
left join shop s on so.SO_SHOP_ID=s.SHOP_ID
WHERE
so.SO_DEL = 0
AND sots.SOTS_LIBRAY= 1
and so.SO_TRADE_ACTIVE_ID not in(
select DISTINCT(SO_TRADE_ACTIVE_ID) from shop_order so  LEFT JOIN shop_order_detail_materials sodm on sodm.SODM_SO_ID=so.SO_ID AND sodm.SODM_SO_TRADE_ACTIVE_ID=so.SO_TRADE_ACTIVE_ID AND sodm.SODM_DEL=0
where so.SO_OPERATE_TIME BETWEEN "2019-03-12 00:00:00" AND "2019-03-12 23:59:59" and SODM_MATERIALS_CODE='401XF0000000001'

)
and SOTS_COLSE=0
AND SOS_SO_IS_SALES in(0,6,8,10)
and s.SHOP_COMPANY_ID<>3
AND so.SO_OPERATE_TIME BETWEEN "2019-03-12 00:00:00" AND "2019-03-12 23:59:59"
GROUP BY so.SO_TRADE_ACTIVE_ID

UNION ALL


SELECT
so.SO_TRADE_ACTIVE_ID,
 so.SO_PAYMENT_TOTAL AS TOTAL
 , SUM(sodm.SODM_MATERIALS_QUANTITY*sc.SC_MATERIALS_COST)  as COST
FROM
shop_order so
left join shop s on so.SO_SHOP_ID=s.SHOP_ID
left join shop_company scp on s.SHOP_COMPANY = scp.SC_NAME
left JOIN shop_order_sale sos ON sos.SOS_SO_IS_SALES = so.SO_IS_SALES
left JOIN shop_order_trade_status sots ON so.SO_SOTS_ID = sots.SOTS_NAME
LEFT JOIN shop_order_detail_materials sodm ON sodm.SODM_SO_ID=so.SO_ID AND sodm.SODM_SO_TRADE_ACTIVE_ID=so.SO_TRADE_ACTIVE_ID AND sodm.SODM_DEL=0
LEFT JOIN stock_cost sc ON sc.SC_MATERIALS_CODE=sodm.SODM_MATERIALS_CODE  AND s.SHOP_COMPANY_ID=sc.SC_COMPANY_ID AND sc.SC_DEL=0
WHERE
so.SO_DEL = 0
 AND SOTS.SOTS_TRANSFER=1
 and SOTS_COLSE=0
 and s.SHOP_COMPANY_ID<>3
and so.SO_TRADE_ACTIVE_ID not in(
select DISTINCT(SO_TRADE_ACTIVE_ID) from shop_order so  LEFT JOIN shop_order_detail_materials sodm on sodm.SODM_SO_ID=so.SO_ID AND sodm.SODM_SO_TRADE_ACTIVE_ID=so.SO_TRADE_ACTIVE_ID AND sodm.SODM_DEL=0
where so.SO_OPERATE_TIME BETWEEN  "2019-03-12 00:00:00" AND "2019-03-12 23:59:59" and SODM_MATERIALS_CODE='401XF0000000001'

)
AND SOS_SO_IS_SALES in(0,6,8,10)
AND so.SO_OPERATE_TIME BETWEEN "2019-03-12 00:00:00" AND "2019-03-12 23:59:59"
GROUP BY so.SO_TRADE_ACTIVE_ID
"""

#内部结算的订单数量
sqls="""
select
t.SHOP_NAME as  店铺
,t.PLACE_TITLE as 生产地
,t.ddh as 订单号
,t.网名 as 网名
,t.LT_NAME as 快递方式
,t.邮单号 as 邮单号
,t.type  as 订单类型
,t.lx as 代工类型
,t.COST as 代工费
,t.time as 出库时间

FROM
((SELECT
 sr.SR_NO AS ddh
  ,sr.SR_CUSTOM_ID as  网名
  ,lt.LT_NAME  as LT_NAME
  ,li.LI_NO  AS  邮单号
  ,so.SO_PRODUCTION_COST as COST
 ,sr.SR_SEND_GOODS_DATETIME as time ,
  sp.SP_PLATFORM_NAME AS PLATFORM_NAME
,s.SHOP_NAME AS SHOP_NAME
,pl.PL_PRODUCTION_PLACE_TITLE AS PLACE_TITLE
,CASE so.SO_IS_MAIN
WHEN 1 THEN '主机'
WHEN 2 THEN '显示器'
WHEN 3 THEN '配件'
WHEN 5 THEN '散件'
END as type
,CASE when  so.SO_TYPE=1 then '售前'
 when so.SO_TYPE=2 then '售后'
end AS lx
FROM sales_order so
LEFT JOIN service_register sr ON sr.SR_NO=so.SO_TYPE_ORDER_NO AND sr.SR_ID=so.SO_TYPE_ORDER_ID AND sr.SR_DEL=0
LEFT  JOIN  production_line pl ON pl.PL_ID=so.SO_PL_ID AND pl.PL_DEL=0
LEFT JOIN shop s ON sr.SR_SHOP_ID=s.SHOP_ID AND s.SHOP_DEL=0
LEFT JOIN shop_platform sp ON sp.SP_ID=s.SHOP_PLATFORM_ID AND sp.sp_del=0
left join logistics_type lt  on sr.SR_LOGISTICS_TYPE=lt.LT_ID and lt.lt_del=0
LEFT JOIN print_post_order ppo ON  ppo.PPO_SO_ID=so.SO_ID
AND ppo.PPO_DEL = 0
LEFT JOIN logistics_info li ON li.LI_ID = ppo.PPO_ID
	AND li.LI_DEL = 0
WHERE so.SO_DEL=0
AND sr.SR_SEND_GOODS_DATETIME>='2019-02-01 00:00:00'
AND sr.SR_SEND_GOODS_DATETIME<='2019-02-28 23:59:59'
AND so.SO_TYPE=2
AND sr.SR_STATUS !=15
AND sr. SR_SEND_GOODS_DATETIME is not NULL
AND so.SO_PL_ID>0
)
UNION ALL
(
SELECT
so1.SO_TRADE_ACTIVE_ID as ddh
,so1.SO_NICKNAME as 网名
,lt.LT_NAME  as LT_NAME
,li.LI_NO  AS  邮单号
  ,so.SO_PRODUCTION_COST as COST
,so1.SO_SND_TIME as time
 ,sp.SP_PLATFORM_NAME AS PLATFORM_NAME
,s.SHOP_NAME AS SHOP_NAME
,pl.PL_PRODUCTION_PLACE_TITLE AS PLACE_TITLE
,CASE so.SO_IS_MAIN
		WHEN 1 THEN '主机'
		WHEN 2 THEN '显示器'
		WHEN 3 THEN '配件'
   	WHEN 5 THEN '散件'
END as type
,CASE when  so.SO_TYPE=1 then '售前'
 when so.SO_TYPE=2 then '售后'
end AS lx
FROM sales_order so
LEFT JOIN shop_order so1 ON so1.SO_TRADE_ACTIVE_ID=so.SO_TYPE_ORDER_NO AND so1.SO_ID=so.SO_TYPE_ORDER_ID AND so1.SO_DEL=0
LEFT JOIN shop_order_sale sos ON sos.SOS_SO_IS_SALES=so1.SO_IS_SALES
LEFT  JOIN  production_line pl ON pl.PL_ID=so.SO_PL_ID AND pl.PL_DEL=0
LEFT JOIN shop s ON so1.SO_SHOP_ID=s.SHOP_ID AND s.SHOP_DEL=0
LEFT JOIN shop_platform sp ON sp.SP_ID=s.SHOP_PLATFORM_ID AND sp.sp_del=0
left join logistics_type lt  on so1.SO_LOGISTICS_TYPE_ID=lt.LT_ID and lt.lt_del=0
LEFT JOIN print_post_order ppo ON  ppo.PPO_SO_ID=so.SO_ID
AND ppo.PPO_DEL = 0
LEFT JOIN logistics_info li ON li.LI_ID = ppo.PPO_ID
	AND li.LI_DEL = 0
WHERE so.SO_DEL=0
 AND so.SO_TYPE=1
AND so1.SO_SOTS_ID in(19,20,21,22,41,42)
and SOS_IS_PRODUCTION =1
AND so1.SO_SND_TIME>='2019-02-01 00:00:00'
AND so1.SO_SND_TIME<='2019-02-28 23:59:59'
)
UNION ALL
(
SELECT
so.SO_TYPE_ORDER_NO  as ddh
,'-'  AS 网名
,'菜鸟发货' as LT_NAME
,'-' AS  邮单号
,so.SO_PRODUCTION_COST AS COST
,so.SO_CREATE_DATETIME  AS time
,case   pl.PL_ID
		WHEN 7 THEN '天猫'
		WHEN 6 THEN '名龙堂'
END  AS PLATFORM_NAME
,case  pl.PL_ID
		WHEN 7 THEN '宁美国度官方旗舰店'
		WHEN 6 THEN '名龙堂官方旗舰店'
END AS SHOP_NAME
,pl.PL_PRODUCTION_PLACE_TITLE  AS PLACE_TITLE
,CASE so.SO_IS_MAIN
	WHEN 1 THEN '主机'
	WHEN 2 THEN '显示器'
	WHEN 3 THEN '配件'
   WHEN 5 THEN '散件'
END as type
,CASE when  so.SO_TYPE=1 then '售前'
 when so.SO_TYPE=2 then '售后'
 when so.SO_TYPE=5 then '菜鸟'
end AS lx

FROM  sales_order  so
	LEFT  JOIN  production_line pl ON pl.PL_ID=so.SO_PL_ID AND pl.PL_DEL=0
WHERE so.SO_DEL=0
and so.SO_TYPE=5
AND SO_STOCKOUT_DATETIME>='2019-02-01 00:00:00'
AND SO_STOCKOUT_DATETIME<='2019-02-28 23:59:59'
)
UNION ALL
(
SELECT
so.SO_TYPE_ORDER_NO  as ddh
,'-'  AS 网名
,'' as LT_NAME
,'-' AS  邮单号
,'0'  AS COST
,so.SO_MODIFY_DATETIME as time
,sp.SP_PLATFORM_NAME AS PLATFORM_NAME
,s.SHOP_NAME AS SHOP_NAME
,pl.PL_PRODUCTION_PLACE_TITLE AS PLACE_TITLE
,CASE so.SO_IS_MAIN
WHEN 1 THEN '主机'
WHEN 2 THEN '显示器'
WHEN 3 THEN '配件'
WHEN 5 THEN '散件'
END as type
,'撤单' AS lx
FROM sales_order so
LEFT  JOIN  production_line pl ON pl.PL_ID=so.SO_PL_ID AND pl.PL_DEL=0
LEFT JOIN shop s ON so.SO_SHOP_ID=s.SHOP_ID AND s.SHOP_DEL=0
LEFT JOIN shop_platform sp ON sp.SP_ID=s.SHOP_PLATFORM_ID AND sp.sp_del=0
WHERE so.SO_DEL=1
AND SO_ISREWORK=1
AND so.SO_MODIFY_DATETIME>='2019-02-01 00:00:00'
AND so.SO_MODIFY_DATETIME<='2019-02-28 23:59:59'
))t
where 1=1


"""

sql2="""
SELECT SOOD_SOO_NO,PRODUCT_SHOP_GOODS_NO,SOOD_PRODUCT_NAME,SOOD_QUANTITY from shop_orig_order soo
LEFT JOIN shop_orig_order_detail sood on soo.SOO_ID=sood.SOOD_SOO_ID
LEFT JOIN product p on sood.SOOD_PRODUCT_CODE=p.PRODUCT_CODE
LEFT JOIN product_category pc on pc.PC_ID=p.PRODUCT_CATEGORY_ID
WHERE soo.SOO_DEL=0
and SOO_STATUS not in ('TRADE_CLOSED','WAIT_BUYER_PAY')
and soo.SOO_SHOP_ID=5
and soo.SOO_PAY_DATE_TIME >= '2019-03-12 00:00:00'
and soo.SOO_PAY_DATE_TIME <= '2019-03-12 23:59:59'
and PRODUCT_SHOP_GOODS_NO='13652564547'
"""
sql3="""
SELECT SOO_ADDRESSEE_PROVINCE,SOO_ADDRESSEE_CITY,SOO_ADDRESSEE_DISTRICT,
SOO_ADDRESSEE_TOWN,PRODUCT_SHOP_GOODS_NO,pc.PC_TITLE,SOOD_PRODUCT_NAME,LENGTH(SOOD_PRODUCT_NAME),sum(SOOD_QUANTITY)qty
from shop_orig_order soo
LEFT JOIN shop_orig_order_detail sood on soo.SOO_ID=sood.SOOD_SOO_ID
LEFT JOIN product p on sood.SOOD_PRODUCT_CODE=p.PRODUCT_CODE
LEFT JOIN product_category pc on pc.PC_ID=p.PRODUCT_CATEGORY_ID
WHERE soo.SOO_DEL=0
and SOO_STATUS not in ('TRADE_CLOSED','WAIT_BUYER_PAY')
and soo.SOO_SHOP_ID=5
and soo.SOO_PAY_DATE_TIME >= '2019-02-01 00:00:00'
and soo.SOO_PAY_DATE_TIME <= '2019-02-28 23:59:59'
and SOO_ADDRESSEE_CITY='武汉市'
and PC_TITLE is not NULL

GROUP BY SOO_ADDRESSEE_PROVINCE,SOO_ADDRESSEE_CITY,SOO_ADDRESSEE_DISTRICT,SOO_ADDRESSEE_TOWN,
PRODUCT_SHOP_GOODS_NO,pc.PC_TITLE,SOOD_PRODUCT_NAME
"""

sql4="""
    SELECT datetime,SOO_ADDRESSEE_PROVINCE,SOO_ADDRESSEE_CITY,SOO_ADDRESSEE_DISTRICT,
PC_TITLE,sum(SOOD_QUANTITY)qty from (
SELECT date_format(soo.SOO_PAY_DATE_TIME,'%%Y-%%m')datetime,SOO_ADDRESSEE_PROVINCE,
SOO_ADDRESSEE_CITY,SOO_ADDRESSEE_DISTRICT,pc.PC_TITLE,SOOD_QUANTITY
from shop_orig_order soo
LEFT JOIN shop_orig_order_detail sood on soo.SOO_ID=sood.SOOD_SOO_ID
LEFT JOIN product p on sood.SOOD_PRODUCT_CODE=p.PRODUCT_CODE
LEFT JOIN product_category pc on pc.PC_ID=p.PRODUCT_CATEGORY_ID
WHERE soo.SOO_DEL=0
and SOO_STATUS not in ('TRADE_CLOSED','WAIT_BUYER_PAY')
and soo.SOO_SHOP_ID=5
and soo.SOO_PAY_DATE_TIME >= '2018-01-01 00:00:00'
and soo.SOO_PAY_DATE_TIME <= '2019-02-28 23:59:59'
and PC_TITLE is not NULL) a
GROUP BY datetime,SOO_ADDRESSEE_PROVINCE,SOO_ADDRESSEE_CITY,SOO_ADDRESSEE_DISTRICT,PC_TITLE
    """

sql5="""
SELECT SOO_NO,SOO_ADDRESSEE_PROVINCE,
SOO_ADDRESSEE_CITY,SOO_ADDRESSEE_DISTRICT,pc.PC_TITLE,PRODUCT_SHOP_GOODS_NO,SOOD_PRODUCT_NAME,SOOD_QUANTITY
from shop_orig_order soo
LEFT JOIN shop_orig_order_detail sood on soo.SOO_ID=sood.SOOD_SOO_ID
LEFT JOIN product p on sood.SOOD_PRODUCT_CODE=p.PRODUCT_CODE
LEFT JOIN product_category pc on pc.PC_ID=p.PRODUCT_CATEGORY_ID
WHERE soo.SOO_DEL=0
and SOO_STATUS not in ('TRADE_CLOSED','WAIT_BUYER_PAY')
and soo.SOO_SHOP_ID=5
and soo.SOO_PAY_DATE_TIME >= '2018-01-01 00:00:00'
and soo.SOO_PAY_DATE_TIME <= '2018-01-31 23:59:59'
and PC_TITLE is not NULL
and PC_TITLE='主机'
and PRODUCT_SHOP_GOODS_NO='16109378213'
"""

sql6="""
SELECT datetime,SO_ADDRESSEE_PROVINCE,SO_ADDRESSEE_CITY,PC_TITLE,COUNT(1)qty from (
SELECT date_format(SO_SND_TIME,'%%Y-%%m')datetime,SO_ADDRESSEE_PROVINCE,SO_ADDRESSEE_CITY,PC_TITLE from shop_order so LEFT JOIN shop_order_detail sod on so.SO_TRADE_ACTIVE_ID=sod.SOD_SO_TRADE_ACTIVE_ID and SOD_DEL=0
LEFT JOIN product p  on p.PRODUCT_CODE=sod.SOD_SP_CODE and PRODUCT_DEL=0
LEFT JOIN product_category pc on pc.PC_ID=p.PRODUCT_CATEGORY_ID
WHERE SO_SND_TIME>='2018-01-01 00:00:00' and SO_SND_TIME<='2019-02-28 23:59:59'
and SO_SHOP_ID=5 and SO_DEL=0
and PC_TITLE is not null)a GROUP BY datetime,SO_ADDRESSEE_PROVINCE,SO_ADDRESSEE_CITY,PC_TITLE
"""

sql7="""
SELECT SO_TRADE_ACTIVE_ID,SO_NO,SO_ADDRESSEE_PROVINCE,SO_ADDRESSEE_CITY,PRODUCT_CODE,PRODUCT_NAME,PC_TITLE
from shop_order so LEFT JOIN shop_order_detail sod on so.SO_TRADE_ACTIVE_ID=sod.SOD_SO_TRADE_ACTIVE_ID and SOD_DEL=0
LEFT JOIN product p  on p.PRODUCT_CODE=sod.SOD_SP_CODE and PRODUCT_DEL=0
LEFT JOIN product_category pc on pc.PC_ID=p.PRODUCT_CATEGORY_ID
WHERE SO_SND_TIME>='2019-01-01 00:00:00' and SO_SND_TIME<='2019-01-31 23:59:59'
and SO_SHOP_ID=5 and SO_DEL=0
and PC_TITLE is not null
and PC_TITLE in ('外设','软件服务','周边产品','硬件')
"""

sql8="""
SELECT DISTINCT(SO_NO),SO_PAY_DATE_TIME from shop_order so LEFT JOIN shop_order_detail sod on so.SO_TRADE_ACTIVE_ID=sod.SOD_SO_TRADE_ACTIVE_ID and SOD_DEL=0
LEFT JOIN product p  on p.PRODUCT_CODE=sod.SOD_SP_CODE and PRODUCT_DEL=0
LEFT JOIN product_category pc on pc.PC_ID=p.PRODUCT_CATEGORY_ID
WHERE SO_SND_TIME>='2019-02-01 00:00:00' and SO_SND_TIME<='2019-02-28 23:59:59'
and SO_SHOP_ID=5 and SO_DEL=0
and PC_TITLE='主机'
"""


connect = create_engine('mysql+pymysql://mayn-erp:mayn@192.168.50.220:3306/db-mayn-erp-prd?charset=utf8')
# connect = create_engine('mssql+pymssql://sa:ym.12345@192.168.50.50:1433/YMB-NM?charset=utf8')

df=pd.read_sql(sql=sql,con=connect)
df.to_excel(r'C:\\Users\\admin\Desktop\s.xlsx',index=False)

# '''
#</editor-fold>

#<editor-fold desc="期初价格修改">
'''
import pandas as pd
import pymysql
import datetime
DataNow=datetime.datetime.now().strftime('%Y%m%d')

def get_sql(sql):
    conn=pymysql.connect(
        host="192.168.50.220",
        user='mayn-erp',
        password='mayn',
        database='db-mayn-erp-prd',
        port=3306,
        charset='utf8'  #针对中文数据
    )
    cursor=conn.cursor()  #创建游标
    #查询数据
    cursor.execute(sql)
    conn.commit()   #更新表数据的提交
    cursor.close()  #关闭游标

df=pd.read_excel('C:/Users/admin/Desktop/1.xlsx',header=0)
for i in range(len(df)):
    code=df.iloc[i]["code"]
    price=df.iloc[i]["price"]
    # sqlmonth="""
    # update stock_history_month shm
    # set shm.SHM_MATERIALS_COST='{}',shm.SHM_STOCK_AMOUNT=shm.SHM_MATERIALS_COST*shm.SHM_STOCK_CAPACITY
    # where shm.SHM_DEL=0 and shm.SHM_COMPANY_ID=3
    # and shm.SHM_MATERIALS_CODE='{}'
    # and shm.SHM_MONTH='201902'
    # """.format(price,code)
    # get_sql(sqlmonth)
    # print("修改物料期初月价格",code,price)
    sqlday="""
    update stock_history_day shd
set shd.SHD_MATERIALS_COST='{}',shd.SHD_STOCK_AMOUNT=shd.SHD_MATERIALS_COST*shd.SHD_STOCK_CAPACITY
where shd.SHD_DEL=0 and shd.SHD_COMPANY_ID=3
and shd.SHD_MATERIALS_CODE='{}'
and shd.SHD_DAY='{}'
    """.format(price,code,DataNow)
    get_sql(sqlday)
    print("修改物料期初日价格", code, price)
'''
#</editor-fold>

#<editor-fold desc="FTP上传和下载">
"""
import os
import ftplib
import datetime

class myFtp:
    ftp = ftplib.FTP()
    bIsDir = False
    path = ""

    def __init__(self, host, port=21):
        # self.ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
        # self.ftp.set_pasv(0)      #0主动模式 1 #被动模式
        self.ftp.connect(host, port)

    def Login(self, user, passwd):
        self.ftp.login(user, passwd)
        print(self.ftp.welcome)

    def DownLoadFile(self, LocalFile, RemoteFile):  # 下载当个文件
        file_handler = open(LocalFile, 'wb')
        print(file_handler)
        self.ftp.retrbinary("RETR %s" % (RemoteFile), file_handler.write)  # 接收服务器上文件并写入本地文件
        file_handler.close()
        return True

    def UpLoadFile(self, LocalFile, RemoteFile):
        if os.path.isfile(LocalFile) == False:
            return False
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary('STOR %s' % RemoteFile, file_handler, 8192)  # 上传文件
        file_handler.close()
        return True

    def UpLoadFileTree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            return False
        print("LocalDir:", LocalDir)
        LocalNames = os.listdir(LocalDir)
        print("list:", LocalNames)
        print(RemoteDir)
        self.ftp.cwd(RemoteDir)
        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                self.UpLoadFileTree(src, Local)
            else:
                self.UpLoadFile(src, Local)

        self.ftp.cwd("..")
        return

    def DownLoadFileTree(self, LocalDir, RemoteDir):  # 下载整个目录下的文件
        print("remoteDir:", RemoteDir)
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        self.ftp.cwd(RemoteDir)
        RemoteNames = self.ftp.nlst()
        print("RemoteNames", RemoteNames)
        print(self.ftp.nlst("/del1"))
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            if self.isDir(file):
                self.DownLoadFileTree(Local, file)
            else:
                self.DownLoadFile(Local, file)
        self.ftp.cwd("..")
        return

    def show(self, list):
        result = list.lower().split(" ")
        if self.path in result and "<dir>" in result:
            self.bIsDir = True

    def isDir(self, path):
        self.bIsDir = False
        self.path = path
        # this ues callback function ,that will change bIsDir value
        self.ftp.retrlines('LIST', self.show)
        return self.bIsDir

    def close(self):
        self.ftp.quit()

    # def get_size(self,buf):
    #     print(len(buf))

# os.walk()遍历文件夹下的所有文件
# os.walk()获得三组数据(rootdir, dirname,filnames)
def file_path(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # print(root, end=' ')    # 当前目录路径
        # print(dirs, end=' ')    # 当前路径下的所有子目录
        return files           # 当前目录下的所有非目录子文件

if __name__ == "__main__":
    try:
        data = file_path(r"\\10.10.1.249\e\rman_backup\data")
        rar_list = []
        if data:
            for i in data:
                if i.endswith('.rar'):
                    rar_list.append(i)
        ftp = myFtp('10.10.3.200')
        ftp.Login('admin', '123456')  # 登录，如果匿名登录则用空串代替即可
        # ftp.DownLoadFileTree('E:/study', '/owt/20170504')  # 从目标目录下载到本地目录E盘
        # ftp.UpLoadFileTree(r'D:\IIS','/MES/dbfile')
        # ftp.DownLoadFile('E:/study/r2101-ROOT-20170428.zip','/owt/20170504/r2101-ROOT-20170428.zip')
        for rar in rar_list:
            print(datetime.datetime.now())
            print(rar)
            ftp.UpLoadFile(r'\\10.10.1.249\e\rman_backup\data\{}'.format(rar),'/MES/dbfile/{}'.format(rar))
            print(datetime.datetime.now())
        ftp.close()
        print("ok!")

    except Exception as e:
        print(e)
"""
#</editor-fold>

#<editor-fold desc="获取目录的文件">
"""
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
"""
#</editor-fold>

#<editor-fold desc="rar打包">
'''
# #导入库
# import os
# import time
# #全局变量
# # List_Fname=[]
# # D:\test>"C:\Program Files (x86)\WinRAR\WinRAR.exe" a MyData.rar -m5 -s -df -r D:\tes
# # t\1.txt D:\test\win2012.txt
#
#
# """函数区"""
# #获取文件夹下的文件名
# def listdir(path, list_name):
#     for file in os.listdir(path):
#          if file[-4:] == ".txt":#字符串切片
#             list_name.append(file)
#     return  list_name
#
# def TimeStampToTime(timestamp):
#     timeStruct = time.localtime(timestamp)
#     return time.strftime('%m.%d',timeStruct)
#
# def get_FileModifyTime(filePath):
#     # filePath = filePath,'utf8')
#     t = os.path.getmtime(filePath)
#     return TimeStampToTime(t)
#
# # """主函数区"""
# # def main():
# #     source_dir="D:\\test\\"
# #     listdir(source_dir, List_Fname)
# #
# #     #创建压缩包文件存储路径及文件名
# #     unzip_dir=source_dir+"unr\\"
# #     #window RAR解压缩命令
# #     for file in List_Fname:
# #         #必须使用这种格式,使用+进行字符连接时，因为语言中转义字符的存在会出现路径识别时的错误。
# #         rar_command ='"C:\Program Files (x86)\WinRAR\WinRAR.exe" x %s * %s\\'%(source_dir+file, unzip_dir+file)
# #         print(rar_command)
# #         os.system(rar_command)
# #
# #
# # """主函数调用"""
# # main()
#
# s=get_FileModifyTime(r'\\10.10.1.249\e\rman_backup\data\ARCH_MESDB_20190131_998969907_U0TOM4HJ_1_1_4032_1')
# print(s)
'''
#</editor-fold>

#<editor-fold desc="降维的使用">
"""
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import datetime
#
# #导入数据和标签
# filename_data=""
# df=pd.read_csv(filename_data)
# df_feature=df[(df.columns)[1:]]
#
# filename_label=""
# df_label=pd.read_csv(filename_label)
#
# #统计一下样本的分布情况
# from collections import Counter
# count=Counter(df_label["Class"])
#
# #划分训练集和测试集
# from sklearn.cross_validation import train_test_split
# feature_train,feature_test,label_train,label_test=train_test_split(df_feature,df_label["Class_num"],test_size=0.2)
#
# def test_algo(model):
#     import time
#     starttime=time.time()
#     model.fit(feature_train,label_train)
#     label_prediction=model.predict(feature_test)
#     labels_dalta=label_test-label_prediction
#
#     endtime=time.time()
#     time_cosumed=endtime-starttime
#     print("time cosumed"+" "+str(time_cosumed))
#
#     from collections import Counter
#     count = Counter(labels_dalta)
#     bingo=count[0]
#
#     accuracy=bingo/len(label_test)
#     print('accuracy'+"="+str(accuracy))
#
#     return accuracy,time_cosumed
#
# from sklearn.svm import SVC
# model=SVC(kernel='sigmoid')
# accuracy_ori,time_ori=test_algo(model)
#
# from sklearn.decomposition import PCA
# n_components=50
# pca=PCA(n_components)
# pca.fit(df_feature)
# df_pca=pca.fit_transform(df_feature)
# print(pca.explained_variance_ratio_)
# print(sum(pca.explained_variance_ratio_))
#
# plt.figure()
# plt.bar(range(n_components),pca.explained_variance_ratio_)
# plt.title('info')
# plt.ylim([0,0,15])
# plt.show()
"""
#</editor-fold>

#<editor-fold desc="下载网络视频">
"""
import re
import os,shutil
import requests,threading
from urllib.request import urlretrieve
from pyquery import PyQuery as pq
from multiprocessing import Pool

'''
Python学习资料或者需要代码、视频加Python学习群：516107834
'''

class video_down():
    def __init__(self,url):
        # 拼接全民解析url
        self.api='https://jx.618g.com'
        self.get_url = 'https://jx.618g.com/?url=' + url
        #设置UA模拟浏览器访问
        self.head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        #设置多线程数量
        self.thread_num=32
        #当前已经下载的文件数目
        self.i = 0
        # 调用网页获取
        html = self.get_page(self.get_url)
        if html:
            # 解析网页
            self.parse_page(html)
    def get_page(self,get_url):
        try:
            print('正在请求目标网页....',get_url)
            response=requests.get(get_url,headers=self.head)
            if response.status_code==200:
                #print(response.text)
                print('请求目标网页完成....\n 准备解析....')
                self.head['referer'] = get_url
                return response.text
        except Exception:
            print('请求目标网页失败，请检查错误重试')
            return None

    def parse_page(self,html):
        print('目标信息正在解析........')
        doc=pq(html)
        self.title=doc('head title').text()
        print(self.title)
        url = doc('#player').attr('src')[14:]
        html=self.get_m3u8_1(url).strip()
        #self.url = url + '800k/hls/index.m3u8'
        self.url = url[:-10] +html
        print('解析完成，获取缓存ts文件.........')
        self.get_m3u8_2(self.url)
    def get_m3u8_1(self,url):
        try:
            response=requests.get(url,headers=self.head)
            html=response.text
            print('获取ts文件成功，准备提取信息')
            return html[20:]
        except Exception:
            print('缓存文件请求错误1，请检查错误')

    def get_m3u8_2(self,url):
        try:
            response=requests.get(url,headers=self.head)
            html=response.text
            print('获取ts文件成功，准备提取信息')
            self.parse_ts_2(html)
        except Exception:
            print('缓存文件请求错误2，请检查错误')
    def parse_ts_2(self,html):
        pattern=re.compile('.*?(.*?).ts')
        self.ts_lists=re.findall(pattern,html)
        print('信息提取完成......\n准备下载...')
        self.pool()
    def pool(self):
        print('经计算需要下载%d个文件' % len(self.ts_lists))
        self.ts_url = self.url[:-10]
        if self.title not in os.listdir():
            os.makedirs(self.title)
        print('正在下载...所需时间较长，请耐心等待..')
        #开启多进程下载
        pool=Pool(16)
        pool.map(self.save_ts,[ts_list for ts_list in self.ts_lists])
        pool.close()
        pool.join()
        print('下载完成')
        self.ts_to_mp4()
    def ts_to_mp4(self):
        print('ts文件正在进行转录mp4......')
        str='copy /b '+self.title+'\*.ts '+self.title+'.mp4'
        print(str)
        os.system(str)
        filename=self.title+'.mp4'
        if os.path.isfile(filename):
            print('转换完成，祝你观影愉快')
            shutil.rmtree(self.title)



    def save_ts(self,ts_list):
        try:
            ts_urls = self.ts_url + '{}.ts'.format(ts_list)
            self.i += 1
            print('当前进度%d/%d'%(self.i,len(self.ts_lists)))
            urlretrieve(url=ts_urls, filename=self.title + '/{}.ts'.format(ts_list))
        except Exception:
            print('保存文件出现错误')


if __name__ == '__main__':
    #电影目标url：狄仁杰之四大天王
    url='https://v.qq.com/x/cover/r6ri9qkcu66dna8.html'
    #电影碟中谍5：神秘国度
    url1='https://v.qq.com/x/cover/5c58griiqftvq00.html'
    #电视剧斗破苍穹
    url2='https://v.qq.com/x/cover/lcpwn26degwm7t3/z0027injhcq.html'
    url3='https://v.qq.com/x/cover/33bfp8mmgakf0gi.html'
    url4='https://v.qq.com/x/cover/lcpwn26degwm7t3/a002708679j.html'
    video_down(url3)
"""
#</editor-fold>




