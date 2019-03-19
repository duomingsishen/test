# coding:utf-8

# from Tkinter import *
#
# root=Tk()
#
# root.title("文件搜索器")
# root.geometry("300x600")
# root.mainloop()

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
    sql ='''select a.ppo,a.sn,a.mo,b.STATE,c.LOGISTICSTYPE from mes_snjoin a left join WMS_ONHAND b on A.SN=b.sn and a.mo=b.mo and a.del=0 left join MES_MO_PPO c on a.ppo=c.ppo  and c.del=0 and C.ISREVOKE=0 where STATE in(0,1,2,6,8)  and c.LOGITICSCOMPANY='中通' and B.SENDTIME>to_date('2018-11-05 0:00:00','yyyy-mm-dd hh24:mi:ss')  order by B.SENDTIME '''
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
    cursor.executemany()
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
    url='https://hdgateway.zto.com/WayBill_GetDetail'
    headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    data={
        'billCode':ppo
    }
    try:
        response=requests.post(url,headers=headers,data=data,timeout=5)
        data=response.json()
        # print(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))
        return data
    except Exception as e:
        data={
            "message":"快递信息查询成功",
            "result":None,
            "status":True,
            "statusCode":None
        }
        return data

#</editor-fold>

#<editor-fold desc="Email的发送">
"""
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
"""
#</editor-fold>

#<editor-fold desc="检查是否退款">

def get_Refund():
    url='http://192.168.50.222:8000/mayn-erp/api/open/resaleForMes/{0}/CheckRefund.do'.format('13618110569514')
    response=requests.post(url)
    data=response.json()
    return data['result']

#</editor-fold>

# prescriptionStatus
# case 1:t = "已取件",
#  case 2:t = "运输中",
# case 3:t = "派件中",
# case 4:t = "已送达",
# case 5:t = "已签收",

if __name__ == '__main__':
    while True:
        for data in get_data():
            ppo = data[0]  # 邮单号
            sn = data[1]  # 产品SN
            mo = data[2]  # 订单号
            status=data[3] #快递状态
            res=get_json_data(ppo)
            if res['status']==True:
                if res['result']!=None:
                    state=res["result"]['prescriptionStatus']
                    info_list = json.dumps(res['result'], ensure_ascii=False, sort_keys=True, indent=4)
                    try:
                        ppo_routing(mo, sn, ppo, 'zhongtong', info_list)
                    except Exception as e:
                        print(ppo,mo)
                        print(e)
                        break
                    if status==0:
                        if state==3:
                            update_data(sn, mo,6)
                            package_time = res["result"]['logisticsRecord'][-1][-1]['scanDate']  # 揽件时间
                            get_server(mo, '15', package_time)
                            print('派送成功', mo, ppo)

                        elif state==5:
                            update_data(sn, mo, 4)
                            signing_time = res["result"]['logisticsRecord'][0][0]['scanDate']  # 签收时间
                            package_time = res["result"]['logisticsRecord'][-1][-1]['scanDate']  # 揽件时间
                            get_server(mo, '15', package_time)
                            get_server_Receipt(mo,signing_time,21)
                            print('签收成功', mo, ppo)

                        elif state==4:
                            update_data(sn, mo, 4)
                            signing_time = res["result"]['logisticsRecord'][0][0]['scanDate']  # 签收时间
                            package_time = res["result"]['logisticsRecord'][-1][-1]['scanDate']  # 揽件时间
                            get_server(mo, '15', package_time)
                            get_server_Receipt(mo, signing_time, 21)
                            print('已送达插入成功', mo, ppo)

                        else:
                            update_data(sn, mo, state)
                            package_time = res["result"]['logisticsRecord'][-1][-1]['scanDate']  # 揽件时间
                            get_server(mo, '15', package_time)
                            print('揽件和运输插入成功', mo, ppo)
                    else:
                        if state==5:
                            update_data(sn, mo, 4)
                            signing_time = res["result"]['logisticsRecord'][0][0]['scanDate']  # 签收时间
                            get_server_Receipt(mo, signing_time, 21)
                            print('签收成功', mo, ppo)
                        else:
                            print('记录未更新', mo, ppo)
                else:
                    if get_Refund():
                        update_data(sn, mo, 9)
                    else:
                        print('未发快递', mo, ppo)
                        continue
            else:
                print('数据异常', mo, ppo)
                print(res)
                break
            time.sleep(1)
        break




