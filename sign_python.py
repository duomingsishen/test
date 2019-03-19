# coding:utf-8
# from tkinter import *
import requests
import json


# #创建窗口
# root=Tk()
# #标题
# root.title('签名设计')
# # #窗口大小
# # root.geometry('600x300')
# # #窗口位置
# # root.geometry('+500+300')
# #可合并为root.geometry('600x300+700+500')
# root.geometry('600x300+500+300')
# label=Label(root,text='签名',font=('华文行楷',20),fg='red')
# #pack place       grid网格布局
# label.grid()
# #输入框
# entry=Entry(root,font=('微软雅黑',20))
# entry.grid(row=0,column=1)
# #点击按钮
# button=Button(root,text='设计签名',font=('微软雅黑',20))
# # button['width']=10
# # button['height']=1
# button.grid(row=1,column=1,sticky=E)
#
# root.mainloop()

# import requests
# import re
# from bs4 import BeautifulSoup
# import time
#
#
# def get_book_url():
#     url = 'https://www.biqiuge.com/book/1795/'
#     response = requests.get(url, timeout=5)
#     response.encoding = 'gbk'
#     html=response.text
#     reg=re.compile('<dd><a href ="(.*?)">(.*?)</a></dd>')
#     res=re.findall(reg,html)
#     return res
#
# def get_content(url):
#     response=requests.get(url,timeout=20)
#     text = response.content.decode('gbk')
#     soup=BeautifulSoup(text,'html5lib')
#     conMidtab = soup.find('div', class_='showtxt')
#     return conMidtab.text
#     # reg=re.compile('<div id="content" class="showtxt">(.*?)</div>')
#     # res=re.findall(reg,html)
#     # return res
#
# if __name__ == '__main__':
#     for i in get_book_url()[3909:]:
#         domain_url = "https://www.biqiuge.com"
#         content_url=domain_url+i[0]
#         content_label=i[1]
#         print(content_url,content_label)
#         content_text=get_content(content_url).replace(u'\xa0', u' ')
#         with open('万古天帝3.txt','a+',encoding='gbk') as f:
#             f.write(content_label)
#             f.write('\n')
#             f.write(content_text)
#             f.write('\n')
#         time.sleep(10)

from suds.client import Client
import requests
import sys
import json
import pymysql
import cx_Oracle
import os
import time
import threading

#<editor-fold desc="MES发货查询">

def get_data():
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决乱码问题
    conn = cx_Oracle.connect('NMKMESSUPPORT', '123@Nmgd.com', '10.10.1.249:1521/mesdb')   #这步不报错就是连上啦
    cursor = conn.cursor()
    sql ='''select a.ppo,a.sn,a.mo,b.STATE,c.LOGISTICSTYPE from mes_snjoin a left join WMS_ONHAND b on A.SN=b.sn and a.mo=b.mo and a.del=0 left join MES_MO_PPO c on a.ppo=c.ppo  and c.del=0 and C.ISREVOKE=0 where STATE in(0,1,2,6,3)  and c.LOGITICSCOMPANY='圆通' and B.SENDTIME>to_date('2018-11-05 0:00:00','yyyy-mm-dd hh24:mi:ss')  order by B.SENDTIME '''
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

#</editor-fold>

#<editor-fold desc="webserver的服务">

def get_server(mo,status,time):
    url = 'http://open.nmgd.cn:8000/mayn-erp/api/service/OrderProcessBoard?wsdl'
    # url = 'http://192.168.50.222:8000/mayn-erp/api/service/OrderProcessBoard?wsdl'
    cilent=Client(url)
    # print(cilent)
    cilent.service.updateOrderProcessBoardDataState(mo,status,time,0)
    # soap_rep=getattr(cilent.service, 'updateOrderProcessBoardDataState')('13618110165856','16','2018-11-30 9:30:20',0) # 需要一一对应
    # print(soap_rep)

#</editor-fold>

#<editor-fold desc="webserver的服务">

def get_server_Receipt(mo,time,status):
    url = 'http://open.nmgd.cn:8000/mayn-erp/api/service/OrderProcessBoard?wsdl'
    # url = 'http://192.168.50.222:8000/mayn-erp/api/service/OrderProcessBoard?wsdl'
    cilent=Client(url)
    # print(cilent)
    cilent.service.UserConfirmsReceipt(mo,time,status)

#</editor-fold>

#<editor-fold desc="ERP数据库">
def ppo_routing(mo,sn,ppo,type,data):
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
    searchsql="select count(1) from dat_ppo_routing where mo='{}' and sn='{}' and ppo='{}'".format(mo,sn,ppo)
    cursor.execute(searchsql)
    results=cursor.fetchone()
    if results[0]==0:
        sql="insert dat_ppo_routing(mo,sn,ppo,ppo_type,data) values('{}','{}','{}','{}','{}')".format(mo,sn,ppo,type,data)
    else:
        sql = "update dat_ppo_routing set data='{}' where mo='{}' and sn='{}' and ppo='{}'".format(data,mo,sn,ppo)
    cursor.execute(sql)
    conn.commit()

    #插入数据
    # sql="insert into user(username,age,password) values('王五',20,'123789')"
    # cursor.execute(sql)
    # conn.commit()   #更新表数据的提交
    # conn.rollback() #撤销更新表的数据

    cursor.close()  #关闭游标

#</editor-fold>

#<editor-fold desc="MES发货状态修改">
def update_data(sn,mo,state):
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决乱码问题
    conn = cx_Oracle.connect('NMKMESSUPPORT', '123@Nmgd.com', '10.10.1.249:1521/mesdb')   #这步不报错就是连上啦
    cursor = conn.cursor()
    sql ="update WMS_ONHAND set STATE={} where sn='{}' and mo='{}'".format(state,sn,mo)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
#</editor-fold>

#<editor-fold desc="查询快递">
def get_json_data(ppo):
    url='https://www.lyyto.cn/api/trace/waybill'
    headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    data={
        'waybillNo':ppo
    }

    response=requests.post(url,headers=headers,data=data,timeout=20)
    data=response.json()
    # print(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))
    return data
#</editor-fold>

#<editor-fold desc="13位时间戳转换时间">

# 输入毫秒级的时间，转出正常格式的时间
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime
#</editor-fold>
#
# data=get_json_data(816794878563)
# print(data['data'][0]['traces'][-1])

if __name__ == '__main__':
    while True:
        for data in get_data():
            ppo=data[0]
            sn=data[1]
            mo=data[2]
            status=data[3]
            res=get_json_data(ppo)
            if res['code']=="success":
                if res['data']:
                    if status==0:
                        if res['data'][0]['isQ']:
                            content=res['data'][0]['traces'][0]['info']      #签收日志
                            sigtime=timeStamp(res['data'][0]['traces'][0]['time']) #签收时间
                            packtime=timeStamp(res['data'][0]['traces'][-1]['time']) #揽件时间
                            update_data(sn, mo, 4)
                            get_server(mo, '15', packtime)
                            get_server_Receipt(mo, sigtime, 21)
                            print(mo,ppo,'已签收')
                        else:
                            if res['data'][0]['isS']:
                                packtime = timeStamp(res['data'][0]['traces'][-1]['time'])  # 揽件时间
                                update_data(sn, mo, 1)
                                get_server(mo, '15', packtime)
                                print(mo,ppo,'快递已揽件')
                            else:
                                print(mo,ppo,'快递未揽件')
                                continue

                    else:
                        if res['data'][0]['isQ']:
                            sigtime = timeStamp(res['data'][0]['traces'][0]['time'])  # 签收时间
                            update_data(sn, mo, 4)
                            get_server_Receipt(mo, sigtime, 21)
                            print(mo, ppo, '更新已签收')
                        else:
                            content = res['data'][0]['traces'][0]['info']  # 快递最新日志
                            print(mo,ppo,content)
                            continue
                else:
                    print(mo,ppo,'无快递信息')
                    continue
            else:
                print(mo,ppo,'查询异常')
                break

            time.sleep(1)

