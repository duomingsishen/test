# -*- coding:utf-8 -*-

#<editor-fold desc="进程的使用">
"""
from multiprocessing import Process
import os
import time

def run_proc(name):
    time.sleep(3)
    print('Run child process %s (%s)...' % (name, os.getpid()))


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    processes = list()
    for i in range(5):
        p = Process(target=run_proc, args=('test',))
        print('Process will start.')
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    print('Process end.')
"""
#</editor-fold>

#<editor-fold desc="进程池的使用">
"""
from multiprocessing import Pool
import os,time,random

def run_task(name):
    print('Task %s (pid=%s) is running...' %(name,os.getpid()))
    time.sleep(random.random()*3)
    print('Task %s end.'%name)

if __name__ == '__main__':
    print('Current process %s.' %os.getpid())
    p=Pool(processes=3)
    for i in range(5):
        p.apply_async(run_task,args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
"""
#</editor-fold>

#<editor-fold desc="进程的通信">
"""
from multiprocessing import Process,Queue
import os,time,random
#写数据进程执行的代码
def proc_write(q,urls):
    print('Process(%s) is writing...'%os.getpid())
    for url in urls:
        q.put(url)
        print('Put %s to queue...'%url)
        time.sleep(random.random())
#读数据进程执行的代码
def proc_read(q):
    print('Process(%s) is reading...'%os.getpid())
    while True:
        url=q.get(True)
        print('Get %s from queue.'%url)

if __name__ == '__main__':
    #父进程创建Queue，并传给各个子进程：
    q=Queue()
    proc_writer1=Process(target=proc_write,args=(q,['url_1','url_2','url_3']))
    proc_writer2=Process(target=proc_write,args=(q,['url_4','url_5','url_6']))
    proc_reader=Process(target=proc_read,args=(q,))
    #启动子进程proc_writer，写入：
    proc_writer1.start()
    proc_writer2.start()
    #启动子进程proc_reader，读取
    proc_reader.start()
    #等待proc_writer结束
    proc_writer1.join()
    proc_writer2.join()
    #proc_reader进程里是死循环，无法等待其结束，只能强行终止：
    proc_reader.terminate()

"""
#</editor-fold>

#<editor-fold desc="进程Pipe的使用">
"""
import multiprocessing
import random
import time,os

def proc_send(pipe,urls):
    for url in urls:
        print("Process(%s) send: %s" %(os.getpid(),url))
        pipe.send(url)
        time.sleep(random.random())
def proc_recv(pipe):
    while True:
        print("Process(%s) rev: %s"%(os.getpid(),pipe.recv()))
        time.sleep(random.random())

if __name__ == '__main__':
    pipe=multiprocessing.Pipe()
    p1=multiprocessing.Process(target=proc_send,args=(pipe[0],['url_'+str(i) for i in range(10)]))
    p2=multiprocessing.Process(target=proc_recv,args=(pipe[1],))
    p1.start()
    p2.start()
    p1.join()
    p2.join()


"""
#</editor-fold>

#<editor-fold desc="线程直接的使用">
"""
import random
import time,threading
#新线程执行的代码:
def thread_run(urls):
    print('Current %s is running...'%threading.current_thread().name)  #获取当前线程的名称
    for url in urls:
        print('%s----->>>%s'%(threading.current_thread().name,url))
        time.sleep(random.random())
    print('%s ended.'%threading.current_thread().name)

print('%s is running...'%threading.current_thread().name)
t1=threading.Thread(target=thread_run,name='Thread_1',args=(['url_1','url_2','url_3'],))
t2=threading.Thread(target=thread_run,name='Thread_2',args=(['url_4','url_5','url_6'],))
t1.start()
t2.start()
t1.join()
t1.join()
print('%s ended.'%threading.current_thread().name)
"""
#</editor-fold>

#<editor-fold desc="继承线程类的使用">
"""
import random
import threading
import time
class myThread(threading.Thread):
    def __init__(self,name,urls):
        threading.Thread.__init__(self,name=name)
        self.urls=urls
    def run(self):
        print('Current %s is running...'%threading.current_thread().name)
        for url in self.urls:
            print('%s----->>>%s' % (threading.current_thread().name, url))
            time.sleep(random.random())
        print('%s ended.' % threading.current_thread().name)
print('%s is running...'%threading.current_thread().name)
t1=myThread(name='Thread_1',urls=['url_1','url_2','url_3'])
t2=myThread(name='Thread_2',urls=['url_4','url_5','url_6'])
t1.start()  #线程启动
t2.start()
t1.join()
t1.join()
print('%s ended.'%threading.current_thread().name)

"""
#</editor-fold>

#<editor-fold desc="线程同步">
"""
import threading
mylock=threading.RLock()
num=0
class myThread(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self,name=name)

    def run(self):
        global num
        while True:
            mylock.acquire()
            print('%s locked,Number: %d'%(threading.current_thread().name,num))
            if num>=4:
                mylock.release()
                print('%s released,Number: %d'%(threading.current_thread().name,num))
                break
            num+=1
            print('%s released,Number: %d' % (threading.current_thread().name, num))
            mylock.release()
if __name__ == '__main__':
    thread1=myThread('Thread_1')
    thread2=myThread('Thread_2')
    thread1.start()
    thread2.start()
"""
#</editor-fold>

#<editor-fold desc="协程的使用">
"""
from gevent import monkey;monkey.patch_all()
import gevent
from urllib.request import urlopen
# import urllib
def run_task(url):
    print('Visit ---> %s'%url)
    try:
        response=urlopen(url)
        data=response.read()
        print('%d bytes received from %s.'%(len(data),url))
    except Exception as e:
        print(e)
if __name__ == '__main__':
    urls=['https://github.com/','https://www.python.org/','http://www.cnblogs.com/']
    greenlets=[gevent.spawn(run_task,url) for url in urls]
    gevent.joinall(greenlets)
# """
#</editor-fold>

#<editor-fold desc="协程池的使用">
"""
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
from urllib.request import urlopen
# import urllib
def run_task(url):
    print('Visit ---> %s'%url)
    try:
        response=urlopen(url)
        data=response.read()
        print('%d bytes received from %s.'%(len(data),url))
    except Exception as e:
        print(e)
    return 'url:%s ---->finish'%url
if __name__ == '__main__':
    pool=Pool(2)
    urls=['https://github.com/','https://www.python.org/','http://www.cnblogs.com/']
    results=pool.map(run_task,urls)
    print(results)

"""
#</editor-fold>

#<editor-fold desc="Linux版 服务进程">
"""
import random,time,queue
from multiprocessing.managers import BaseManager
#第一步：建立task_queue和result_queue,用来存放任务和结果
task_queue=queue.Queue()
result_queue=queue.Queue()

class Queuemanager(BaseManager):
    pass
#第二步：把创建的两个队列注册到网络上，利用register方法,callable参数关联了Queue对象，
#将Queue对象在网络中暴露
Queuemanager.register('get_task_queue',callable=lambda :task_queue)
Queuemanager.register('get_result_queue',callable=lambda :result_queue)

#第三步:绑定端口8001，设置验证口令'qiye'。这个相当于对象的初始化
manager=Queuemanager(address=('',8001),authkey='qiye')

#第四步：启动管理，监听信息通道
manager.start()

#第五步：通过管理实例的方法获得通过网络访问的Queue对象
task=manager.get_task_queue()
result=manager.get_result_queue()

#第六步：添加任务
for url in ["ImageUrl_"+i for i in range(10)]:
    print('put task %s ...'%url)
    task.put(url)
#获取返回结果
print('try get result...')
for i in range(10):
    print('result is %s'%result.get(timeout=10))
#关闭管理
manager.shutdown()

"""
#</editor-fold>

#<editor-fold desc="windows/Linux 任务进程">
"""
import time
from multiprocessing.managers import BaseManager
#创建类似的QueueManager：
class QueueManager(BaseManager):
    pass
#第一步:使用QueueManager注册用于获取Queue的方法名称
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
#第二步:连接到服务器：
server_addr='127.0.0.1'
print('Connect to server %s...'%server_addr)
#端口和验证口令注意保持与服务进程完全一致
m=QueueManager(address=(server_addr,8001),authkey=b'qiye') #python2的写法
# m=QueueManager(address=(server_addr,8001),authkey=b'qiye') #python3的写法
#从网络连接
m.connect()
#第三步：获取Queue的对象
task=m.get_task_queue()
result=m.get_result_queue()
#第四步：从task队列获取任务，并把结果写入result队列：
while(not task.empty()):
    image_url=task.get(True,timeout=5)
    print('run task download %s...'%image_url)
    time.sleep(1)
    result.put('%s--->success'%image_url)

#处理结束：
print('worker exit.')
"""
#</editor-fold>

#<editor-fold desc="windows 服务进程">
"""
#taskManager.py for windows
import queue
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support
#任务个数
task_number=10
task_queue=queue.Queue(task_number)
result_queue=queue.Queue(task_number)
def get_task():
    return task_queue
def get_result():
    return result_queue
#创建类似的QueueManager：
class QueueManager(BaseManager):
    pass
def win_run():
    #Windows下绑定调用接口不能使用lambda，所以只能先定义函数在绑定
    QueueManager.register('get_task_queue',callable=get_task)
    QueueManager.register('get_result_queue',callable=get_result)
    #绑定端口并设置验证口令，Windows下需要填写IP地址,linux下不填默认为本地
    manager=QueueManager(address=('127.0.0.1',8001),authkey=b'qiye')
    #启动
    manager.start()
    try:
        #通过网络获取任务队列和结果队列
        task=manager.get_task_queue()
        result=manager.get_result_queue()
        #添加任务
        for url in ["ImageUrl_"+str(i) for i in range(10)]:
            print('put task %s'%url)
            task.put(url)
        print('try get result')
        for i in range(10):
            print('result is %s'%result.get(timeout=10))
    except:
        print('Manager error')
    finally:
        #一定要关闭，否则会报管道未关闭的错误
        manager.shutdown()
if __name__ == '__main__':
    #windows下多进程可能会有问题，添加这句可以缓解
    freeze_support()
    win_run()

"""
#</editor-fold>

#<editor-fold desc="TCP编程服务端">
"""
import socket
import threading
import time
def dealClient(sock,addr):
    #第四步：接收传来的数据，并发送给对方数据
    print("Accept new connection from %s:%s..."%addr)
    sock.send(b'Hello,I am server!')
    while True:
        data=sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8')=='exit':
            break
        print('-->>%s!'%data.decode('utf-8'))
        sock.send(('Loop_Msg:%s!'%data.decode('utf-8')).encode('utf-8'))
    #第五步：关闭Socket
    sock.close()
    print('Connection from %s:%s closed.'%addr)
if __name__ == '__main__':
    #第一步：创建一个基于IPv4和TCP协议的Socket
    #Socket绑定的IP(127.0.0.1为本机IP)与端口
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(('127.0.0.1',9999))
    #第二步：监听连接
    s.listen(5)
    print('Waiting for connection...')
    while True:
        #第三步：接收一个新连接：
        sock,addr=s.accept()
        #创建新线程来处理TCP连接：
        t=threading.Thread(target=dealClient,args=(sock,addr))
        t.start()
"""
#</editor-fold>

#<editor-fold desc="TCP编程客户端">
"""
import socket
#初始化Socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#连接目标的IP和端口
s.connect(('127.0.0.1',9999))
#接收消息
print('-->>'+s.recv(1024).decode('utf-8'))
#发送消息
s.send(b'Hello,I am a Client')
print('-->>'+s.recv(1024).decode('utf-8'))
s.send(b'exit')
#关闭Socket
s.close()
"""
#</editor-fold>

#<editor-fold desc="UDP服务端">
"""
import socket
#创建Socket，绑定指定的IP和端口
#SOCK_DGRAM指定了这个Socket的类型是UDP，绑定端口和TCP示例一样
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(('127.0.0.1',9999))
print('Bind UDP on 9999...')
while True:
    #直接发送数据和接收数据
    data,addr=s.recvfrom(1024)
    print('Received from %s:%s.'%addr)
    s.sendto(b'Hello,%s!'%data,addr)

"""
#</editor-fold>

#<editor-fold desc="UDP客户端">
"""
import socket
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
for data in [b'Hello',b'World']:
    #发送数据：
    s.sendto(data,('127.0.0.1',9999))
    #接收数据：
    print(s.recv(1024).decode('utf-8'))
s.close()
"""
#</editor-fold>

#<editor-fold desc="re.match的使用">
"""
import re
pattern=re.compile(r'\d+')
result1=re.match(pattern,'192abc')
if result1:
    print(result1.group())
else:
    print('匹配失败1')
result2=re.match(pattern,'abc192')
print(result2)
if result2:
    print(result2.group())
else:
    print('匹配失败2')
"""
#</editor-fold>

#<editor-fold desc="re.search的使用">
"""
import re
#将正则表达式编译成pattern对象
pattern=re.compile(r'\d+')
#使用re.search匹配文本，获得匹配结果，无法匹配时将返回None
result1=re.search(pattern,'abc192edf')
if result1:
    print(result1.group())
else:
    print('匹配失败1')
"""
#</editor-fold>

#<editor-fold desc="re.split的使用">
"""
import re
pattern=re.compile(r'\d+')
print(re.split(pattern,'A1B2C3D4',maxsplit=2))
"""
#</editor-fold>

#<editor-fold desc="re.findall的使用">
"""
import re
pattern=re.compile(r'\d+')
print(re.findall(pattern,'A1B2C3D4'))
"""
#</editor-fold>

#<editor-fold desc="re.finditer的使用">
"""
import re
pattern=re.compile(r'\d+')
matchiter=re.finditer(pattern,'A1B2C3D4')
for match in matchiter:
    print(match.group())
"""
#</editor-fold>

#<editor-fold desc="re.sub的使用">
"""
import re
p=re.compile(r'(?P<word1>\w+) (?P<word2>\w+)')#使用名称引用
s='i say,hello world!'
print(p.sub(r'\g<word2> \g<word1>',s))
p=re.compile(r'(\w+) (\w+)')#使用编号
print(p.sub(r'\2 \1',s))
def func(m):
    return m.group(1).title()+' '+m.group(2).title()
print(p.sub(func,s))

"""
#</editor-fold>

#<editor-fold desc="re.subn的使用">
"""
import re
s='i say,hello world!'
p=re.compile(r'(\w+) (\w+)')
print(p.subn(r'\2 \1',s))
def func(m):
    return m.group(1).title()+' '+m.group(2).title()
print(p.subn(func,s))
"""
#</editor-fold>

#<editor-fold desc="match的使用">
"""
import re
pattern=re.compile(r'(\w+) (\w+) (?P<word>.*)')
match=pattern.match( 'I love you!')
print("match.string:",match.string)
print("match.re:",match.re)
print("match.pos:",match.pos)
print("match.endpos:",match.endpos)
print("match.lastindex:",match.lastindex)
print("match.lastgroup:",match.lastgroup)

print("match.group(1,2):",match.group(1,2))
print("match.groups():",match.groups())
print("match.groupdict():",match.groupdict())
print("match.start(2):",match.start(2))
print("match.end(2):",match.end(2))
print("match.span(2):",match.span(2))
print(r"match.expand(r'\2 \1 \3'):",match.expand(r'\2 \1 \3'))
"""
#</editor-fold>

#<editor-fold desc="BeautifulSoup的使用和CSS选择器">
'''
from bs4 import BeautifulSoup
html_str = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!--Elsie--></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
soup=BeautifulSoup(html_str,'lxml')
# soup=BeautifulSoup(open('index.html'))  #打开html文件读取
# print(soup.prettify())  #将数据进行美化
# print(soup.title)       #抽取title标记
# print(soup.a)           #抽取a标记
# print(soup.p)           #抽取p标记
# print(soup.name)        #获取Tag的名字
# print(soup.title.name)  #获取title标记的名字
# soup.title.name='mytitle' #修改title标记的名字
# print(soup.title)
# print(soup.mytitle)

# #获取Tag的属性
# print(soup.p['class'])
# print(soup.p.get('class'))
#
# #"点"取属性  .attrs获取所有的Tag属性
# print(soup.p.attrs)

#修改属性和内容
# soup.p['class']="myClass"
# print(soup.p)

#获取标记内部的文字
# print(soup.p.string)
# print(type(soup.p.string))

# unicode_string=unicode(soup.p.string)         #python2 转换
# unicode_string=str(soup.p.string)               #python3 转换
# print(type(unicode_string))

# print(type(soup.name))
# print(soup.name)
# print(soup.attrs)

# import bs4
# print(soup.a.string)            #获取内容的注释
# print(type(soup.a.string))
# if type(soup.a.string)==bs4.element.Comment:   #判断是否为Comment类型
#     print(soup.a.string)

# print(soup.head.contents)        #生成一个列表
# print(len(soup.head.contents))
# print(soup.head.contents[0].string)

# for child in soup.head.children:      #生成一个生成器
#     print(child)

# for child in soup.head.descendants:
#     print(child)

# print(soup.head.string)
# print(soup.title.string)
# print(soup.html.string)

# for string in soup.strings:
#     print(repr(string))

# for string in soup.stripped_strings:
#     print(repr(string))

# print(soup.title)
# print(soup.title.parent)

# print(soup.a)
# for parent in soup.a.parents:
#     if parent is None:
#         print(parent)
#     else:
#         print(parent.name)

# print(soup.p.next_sibling)
# print(soup.p.prev_sibling)
# print(soup.p.next_sibling.next_sibling)

# for sibling in soup.p.next_siblings:
#     print(repr(sibling))

# print(soup.head)
# print(soup.head.next_element)

# for element in soup.head.next_elements:
#     print(repr(element))


# print(soup.find_all('b'))
#
# import re
# for tag in soup.find_all(re.compile("^b")):
#     print(tag.name)
#
# print(soup.find_all(["a","b"]))

# for tag in soup.find_all(True):
#     print(tag.name)
#
# def hasClass_Id(tag):
#     return tag.has_attr('class') and tag.has_attr('id')
# print(soup.find_all(hasClass_Id))

# print(soup.find_all(id='link2'))   #搜索Tag的id='link2'
#
import re
# print(soup.find_all(href=re.compile('elsie')))   #正则查找
#
# print(soup.find_all(id=True))     #id什么值都可以

# print(soup.find_all('a',class_='sister'))  #class是关键字  需要class后面加下划线

# print(soup.find_all(href=re.compile('elsie'),id='link1')) #多个属性

# data_soup=BeautifulSoup('<div data-foo="value">foo!</div>','lxml')
# # data_soup.find_all(data-foo="value")    #tag属性不能搜索
# print(data_soup.find_all(attrs={"data-foo":"value"}))  #通过attrs参数定义一个字典参数搜索特殊属性

# print(soup.find_all(text="Elsie"))
# print(soup.find_all(text=["Tillie","Elsie","Lacie"]))
# print(soup.find_all(text=re.compile('Dormouse')))
#
# print(soup.find_all('a',text='Elsie'))

# print(soup.find_all('a',limit=2))

# print(soup.find_all('title'))
# print(soup.find_all('title',recursive=False))

# #直接查找title标记
# print(soup.select("title"))
# #逐层查找title标记
# print(soup.select("html head title"))
# #查找直接子节点
# #查找head下的title标记
# print(soup.select("head > title"))
# #查找p下的id="link1"的标记
# print(soup.select("p > #link1"))
# #查找兄弟节点
# #查找id="link1"之后class=sister的所有兄弟标记
# print(soup.select("#link1 ~ .sister"))
# #查找紧跟着id="link1"之后class=sister的子标记
# print(soup.select("#link1 + .sister"))

# print(soup.select(".sister"))
# print(soup.select("[class~=sister]"))

# print(soup.select("#link1"))
# print(soup.select("a#link2"))

# print(soup.select('a[href]'))

# print(soup.select('a[href="http://example.com/elsie"]'))   #完全等于
# print(soup.select('a[href^="http://example.com/"]'))        #开头等于
# print(soup.select('a[href$="tillie"]'))                     #结尾等于
# print(soup.select('a[href*=".com/el"]'))                    #部分等于

'''
#</editor-fold>

#<editor-fold desc="lxml的xpath的使用">
'''
from lxml import etree
html_str = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
html=etree.HTML(html_str)
result=etree.tostring(html)
print(result)

# from lxml import etree
# html=etree.parse('index.html')
# result=etree.tostring(html,pretty_print=True)
# print(result)

html=etree.HTML(html_str)
urls=html.xpath(".//*[@class='sister']/@href")
print(urls)


'''
#</editor-fold>

#<editor-fold desc="json的使用">
"""
import json
str=[{"username":"七夜","age":24},(2,3),1]
json_str=json.dumps(str,ensure_ascii=False)
# print(json_str)
# with open('qiye.txt','w') as fp:
#     json.dump(str,fp=fp,ensure_ascii=False)

new_str=json.loads(json_str)
print(new_str)
with open('qiye.txt','r') as fp:
    print(json.load(fp))

"""
#</editor-fold>

#<editor-fold desc="csv的使用">
# """
# import csv
# headers=['ID','UserName','Password','Age','Country']
# rows=[(1001,'qiye','qiye_pass',24,'China'),
#       (1002,'Mary','Mary_pass',20,'USA'),
#       (1003,'Jack','Jack_pass',20,'USA')]
# with open('qiye.csv','w') as f:
#     f_csv=csv.writer(f)
#     f_csv.writerow(headers)
#     f_csv.writerows(rows)

# import csv
# headers = ['ID', 'UserName', 'Password', 'Age', 'Country']
# rows=[{'ID':1001,'UserName':'qiye','Password':'qiye_pass','Age':24,'Country':'China'},
#       {'ID':1002,'UserName':'Mary','Password':'Mary_pass','Age':20,'Country':'USA'},
#       {'ID':1003,'UserName':'Jack','Password':'Jack_pass','Age':20,'Country':'USA'}]
# with open('qiye.csv','w') as f:
#     f_csv=csv.DictWriter(f,headers)
#     f_csv.writeheader()
#     f_csv.writerows(rows)

# import csv
# with open('qiye.csv') as f:
#     f_csv=csv.reader(f)
#     headers=next(f_csv)
#     print(headers)
#     for row in f_csv:
#         print(row)

# from collections import namedtuple   #命名元组
# import csv
# with open('qiye.csv') as f:
#     f_csv=csv.reader(f)
#     headings=next(f_csv)
#     Row=namedtuple('Row',headings)
#     for r in f_csv:
#         row=Row(*r)
#         print(row.UserName,row.Password)
#         print(row)

# import csv
# with open('qiye.csv') as f:
#     f_csv=csv.DictReader(f)
#     for row in f_csv:
#         print(row.get('UserName'),row.get('Password'))

# """
#</editor-fold>

#<editor-fold desc="文件下载">
"""
from urllib.request import urlretrieve
from lxml import etree
import requests
def Schedule(blocknum,blocksize,totalsize):
    '''
    blocknum: 已经下载的数据块
    blocksize: 数据块的大小
    totalsize: 远程文件的大小
    '''
    per=100.0*blocknum*blocksize/totalsize
    print(blocknum,blocksize,totalsize)
    if per>100:
        per=100
    print('当前下载进度：%d'%per)
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
r=requests.get('http://www.ivsky.com/tupian/ziranfengguang/',headers=headers)
html=etree.HTML(r.text)
img_urls=html.xpath('.//img/@src')
i=0
for img_url in img_urls:
    urlretrieve(img_url,'img'+str(i)+'.jpg',dule)
    i+=1
"""
#</editor-fold>

#<editor-fold desc="pyppeteer百度查询">
"""
import time
import asyncio
from pyppeteer import launch


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    await page.setViewport({'width': 1200, 'height': 800})
    await page.goto('https://www.baidu.com')
    # 在搜索框中输入python
    await page.type('input#kw.s_ipt', 'python')
    # 点击搜索按钮
    await page.click('input#su')

    # 等待元素加载，第一种方法，强行等待5秒
    # await asyncio.sleep(5)

    # 第二种方法，在while循环里强行查询某元素进行等待
    while not await page.querySelector('.t'):
        pass

    # 滚动到页面底部
    await page.evaluate('window.scrollBy(0, window.innerHeight)')

    title_elements = await page.xpath('//h3[contains(@class,"t")]/a')
    for item in title_elements:
        title_str = await (await item.getProperty('textContent')).jsonValue()
        print(title_str)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

"""
#</editor-fold>

#<editor-fold desc="pyppeterr登陆淘宝">
"""
import asyncio
import time, random
from pyppeteer.launcher import launch  # 控制模拟浏览器用
from retrying import retry  # 设置重试次数用的


async def main(username, pwd, url):  # 定义main协程函数，
    # 以下使用await 可以针对耗时的操作进行挂起

    browser = await launch({'headless': False, 'args': ['--no-sandbox'], })  # 启动pyppeteer 属于内存中实现交互的模拟器
    page = await browser.newPage()  # 启动个新的浏览器页面

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')


    await page.goto(url)  # 访问登录页面
    # 替换淘宝在检测浏览时采集的一些参数。
    # 就是在浏览器运行的时候，始终让window.navigator.webdriver=false
    # navigator是windiw对象的一个属性，同时修改plugins，languages，navigator 且让
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    # 使用type选定页面元素，并修改其数值，用于输入账号密码，修改的速度仿人类操作，因为有个输入速度的检测机制
    # 因为 pyppeteer 框架需要转换为js操作，而js和python的类型定义不同，所以写法与参数要用字典，类型导入
    await page.type('.J_UserName', username, {'delay': input_time_random() - 50})
    await page.type('#J_StandardPwd input', pwd, {'delay': input_time_random()})

    # await page.screenshot({'path': './headless-test-result.png'})    # 截图测试
    time.sleep(2)

    # 检测页面是否有滑块。原理是检测页面元素。
    slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 是否有滑块

    if slider:
        print('当前页面出现滑块')
        # await page.screenshot({'path': './headless-login-slide.png'}) # 截图测试
        flag, page = await mouse_slide(page=page)  # js拉动滑块过去。
        if flag:
            await page.keyboard.press('Enter')  # 确保内容输入完毕，少数页面会自动完成按钮点击
            print("print enter", flag)
            await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')  # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。

            time.sleep(2)
            # cookies_list = await page.cookies()
            # print(cookies_list)
            await get_cookie(page)  # 导出cookie 完成登陆后就可以拿着cookie玩各种各样的事情了。
    else:
        print("")
        await page.keyboard.press('Enter')
        print("print enter")
        await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')
        await page.waitFor(20)
        await page.waitForNavigation()

        try:
            global error  # 检测是否是账号密码错误
            print("error_1:", error)
            error = await page.Jeval('.error', 'node => node.textContent')
            print("error_2:", error)
        except Exception as e:
            error = None
        finally:
            if error:
                print('确保账户安全重新入输入')
                # 程序退出。
                loop.close()
            else:
                print(page.url)
                await get_cookie(page)
                # time.sleep(100)


# 获取登录后cookie
async def get_cookie(page):
    # res = await page.content()
    cookies_list = await page.cookies()
    cookies = ''
    for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
    print(cookies)
    return cookies


def retry_if_result_none(result):
    return result is None


@retry(retry_on_result=retry_if_result_none, )
async def mouse_slide(page=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        await page.hover('#nc_1_n1z')  # 不同场景的验证码模块能名字不同。
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        if slider_again != '验证通过':
            return None, page
        else:
            # await page.screenshot({'path': './headless-slide-result.png'}) # 截图测试
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    username = '15927244596'  # 淘宝用户名
    pwd = 'worinima0514'  # 密码
    url = 'https://login.taobao.com/member/login.jhtml'
    loop = asyncio.get_event_loop()  # 协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。
    loop.run_until_complete(main(username, pwd, url))  # 将协程注册到事件循环，并启动事件循环

"""
#</editor-fold>

#<editor-fold desc="">
# """
# """
#</editor-fold>

#<editor-fold desc="">
# """

# """
#</editor-fold>


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


options=webdriver.ChromeOptions()
# options = Options()
options.add_argument('--proxy-server=http://127.0.0.1:8080')
url='https://ad.alimama.com/index.htm'
# driver=webdriver.Chrome()
driver=webdriver.Chrome(options=options)
driver.get(url)
driver.maximize_window()
login_frame=driver.find_element_by_name('taobaoLoginIfr')
driver.switch_to.frame(login_frame)
driver.find_element_by_id('J_Quick2Static').click()
driver.find_element_by_id('TPL_username_1').send_keys('15927244596')
driver.find_element_by_id('TPL_password_1').send_keys('worinima0514')
driver.find_element_by_id('J_SubmitStatic').click()



