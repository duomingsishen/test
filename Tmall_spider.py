# -*- coding:utf-8 -*-

from suds.client import Client
import requests
import sys
import json
import pymysql
import cx_Oracle
import os
import time
import socket

#<editor-fold desc="MES发货查询">
#0
def get_data():
    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决乱码问题
    conn = cx_Oracle.connect('NMKMESSUPPORT', '123@Nmgd.com', '10.10.1.249:1521/mesdb')   #这步不报错就是连上啦
    cursor = conn.cursor()
    sql =''' select a.ppo,a.sn,a.mo,c.LOGISTICSTYPE,STATE from mes_snjoin a left join WMS_ONHAND b on A.SN=b.sn and a.mo=b.mo and a.del=0 left join MES_MO_PPO c on a.mo=c.mo and a.ppo=c.ppo  and c.del=0 where STATE in (0,1,2,3,5,6,7,8) and c.LOGITICSCOMPANY not in ('顺丰','驿动','中通','EMS','京东') and B.SENDTIME>to_date('2018-11-05 0:00:00','yyyy-mm-dd hh24:mi:ss')  order by B.SENDTIME '''
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

#<editor-fold desc="快递查询">

class Express100(object):

    company_url = "http://www.kuaidi100.com/autonumber/autoComNum"
    trace_url = "http://www.kuaidi100.com/query"

    @classmethod
    def get_json_data(cls, url, payload):
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        # proxy={
        #     'http':'118.190.95.35:9001'
        # } ,proxies=proxy

        r = requests.get(url=url, params=payload,headers=headers)
        return r.json()

    @classmethod
    def get_company_info(cls, express_code):
        payload = {'text': express_code}
        data = cls.get_json_data(cls.company_url, payload)
        return data

    @classmethod
    def get_express_info(cls, express_code):
        company_info = cls.get_company_info(express_code)
        company_code = ""

        if company_info.get("auto", ""):
            company_code = company_info.get("auto", "")[0].get("comCode", "")

        if company_code=='jd' and 'VE' not in express_code:
            company_code='yuantong'

        if company_code=='youzhengguonei':
            company_code='ems'

        payload = {'type': company_code, 'postid': express_code, 'id': 1}

        data = cls.get_json_data(cls.trace_url, payload)

        data.update(company_info)

        return data

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

#<editor-fold desc="检查是否退款">

def get_Refund(mo):
    url='http://192.168.50.222:8000/mayn-erp/api/open/resaleForMes/{}/CheckRefund.do'.format(mo)
    response=requests.post(url)
    data=response.json()
    return data['result']

#</editor-fold>

#<editor-fold desc="订单是否退货">
def get_back(mo):
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
    sql="select count(1)qty,max(SR_CREATE_DATETIME)CREATE_DATETIME from service_register where SR_TYPE=2 and SR_SO_TRADE_ACTIVE_ID={}".format(mo)
    cursor.execute(sql)
    back = cursor.fetchone()
    cursor.close()  #关闭游标
    return back

#</editor-fold>

#<editor-fold desc="执行函数">

if __name__ == "__main__":
    # <editor-fold desc="执行函数">
    # """
    while True:
        for data in get_data():
            ppo=data[0]     #邮单号
            sn = data[1]    #产品SN
            mo=data[2]      #订单号
            status = data[4]  #MES邮单状态

            if data[3]=='京东快递':
                ppo=ppo.split('-')[0]
            res = Express100.get_express_info(str(ppo).strip())
            # print(json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4))
            if res['status']=='200':    #查询是否成功
                state=res['state']    #邮单的状态0:运输中 1:揽件 2:疑难 3:已签收 4:退回签收 5:派送中 6:退回中
                com=res['com']      #快递类型  京东 jd EMS快递 ems  中通 zhongtong

                # json_list=json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4)
                # print(res)
                info_list=''
                for info in res['data']:
                    res_list=json.dumps(info, ensure_ascii=False, sort_keys=True, indent=4)
                    info_list=info_list+res_list

                # json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4)
                update_data(sn,mo,int(state)+1)
                ppo_routing(mo,sn,ppo,com,info_list)
                if status==0:
                    if state=='3':
                        if res['data']:
                            ftime=res['data'][0]['ftime']           #签收时间
                            package_time=res['data'][-1]['ftime']   #揽件时间
                            get_server(mo,'15',package_time)
                            get_server_Receipt(mo, ftime, 21)
                            print('插入成功',mo,ppo)
                        else:
                            continue

                    # elif state=='0':
                    #     if res['data']:
                    #         package_time = res['data'][-1]['ftime']  # 揽件时间
                    #         get_server(mo, '15', package_time)
                    #         print('揽件时间插入成功', mo, ppo)
                    #     else:
                    #         continue
                    #
                    # elif state=='1':
                    #     if res['data']:
                    #         package_time = res['data'][-1]['ftime']  # 揽件时间
                    #         get_server(mo, '15', package_time)
                    #         print('揽件时间插入成功', mo, ppo)
                    #     else:
                    #         continue
                    else:
                        if res['data']:
                            package_time = res['data'][-1]['ftime']  # 揽件时间
                            get_server(mo, '15', package_time)
                            print('揽件时间插入成功', mo, ppo)
                        else:
                            continue

                        # print(res['status'])
                        # print(res['state'])
                        # for i in res['data']:
                        #     print(i['context'])
                else:
                    if state == '3':
                        ftime = res['data'][0]['ftime']  # 签收时间
                        get_server_Receipt(mo, ftime, 21)
                        print('插入成功', mo, ppo)
                    #EMS代收的
                    # elif state=='0':
                    #     if '代理' in res['data'][0]['context']:
                    #         ftime=res['data'][0]['ftime']  # 签收时间
                    #         get_server_Receipt(mo, ftime, 21)
                    #         update_data(sn, mo, 4)
                    #         print('代收成功', mo, ppo)
                    #     else:
                    #         if res['data']:
                    #             print('记录未更新', mo, ppo, res['data'][0]['context'])
                    #         else:
                    #             print('记录未更新', mo, ppo, res)
                    # 京东代收
                    # elif state=='0':
                    #     if '代收' in res['data'][0]['context']:
                    #         ftime=res['data'][0]['ftime']  # 签收时间
                    #         get_server_Receipt(mo, ftime, 21)
                    #         update_data(sn, mo, 4)
                    #         print('代收成功', mo, ppo)
                    #     else:
                    #         if res['data']:
                    #             print('记录未更新', mo, ppo, res['data'][0]['context'])
                    #         else:
                    #             print('记录未更新', mo, ppo, res)
                    # elif state == '1':
                    #     if '代收' in res['data'][0]['context']:
                    #         ftime = res['data'][0]['ftime']  # 签收时间
                    #         get_server_Receipt(mo, ftime, 21)
                    #         update_data(sn, mo, 4)
                    #         print('代收成功', mo, ppo)
                    #     else:
                    #         if res['data']:
                    #             print('记录未更新', mo, ppo, res['data'][0]['context'])
                    #         else:
                    #             print('记录未更新', mo, ppo, res)
                    else:
                        if  res['data']:
                            print('记录未更新', mo, ppo,res['data'][0]['context'])
                        else:
                            print('记录未更新', mo, ppo,res)

            elif res['status'] == '201':
                if get_Refund(mo):
                    update_data(sn, mo, 9)
                    print('退款成功', mo, ppo)
                else:
                    print('未发快递', mo, ppo)
                    continue
            else:
                print('插入失败', mo, ppo)
                print(json.dumps(res, ensure_ascii=False, sort_keys=True, indent=4))
                time.sleep(30)
            time.sleep(10)
        break
    # """
    # </editor-fold>

#</editor-fold>

