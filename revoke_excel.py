# -*- coding:utf-8 -*-

import os
import cx_Oracle
import xlsxwriter
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox


#<editor-fold desc="Email的发送">
"""
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import smtplib

def _format_addr(s):
    name,addr=parseaddr(s)
    return formataddr((Header(name,'utf-8').encode(),addr))


def sen_email():
    #发货人地址
    from_addr='wuxu@iningmei.com'
    #邮箱密码
    password='Ningmei2016'
    #收件人地址
    to_addr='360361689@qq.com'
    #企业邮箱服务器地址
    smtp_server='smtp.exmail.qq.com'
    #设置邮件信息

    # 创建要发送的邮件正文及附件对象
    # related 使用邮件内嵌资源，可以把附件中的图片等附件嵌入到正文中
    msg = MIMEMultipart()
    msg.attach(MIMEText('撤单数据请查看附件','plain','utf-8'))
    msg['From']=_format_addr('无恤<%s>' % from_addr)
    msg['To']=_format_addr('李晓峰<%s>' % to_addr)
    msg['Subject']=Header('撤单数据','utf-8')

    xlsxpart = MIMEApplication(open('撤单数据.xls', 'rb').read())
    xlsxpart.add_header('Content-Disposition', 'attachment', filename=('gbk', '', '撤单数据.xls'))
    msg.attach(xlsxpart)

    #发送邮件
    server=smtplib.SMTP(smtp_server,25)
    server.login(from_addr,password)
    server.sendmail(from_addr,[to_addr],msg.as_string())
    server.quit()
"""
#</editor-fold>


def get_excel(name):
    #工作表
    work_sheet=work_book.add_worksheet(name)
    ColumnNames=['订单号','产品SN','工艺路线','撤单工序','撤单时间','是否回仓','公司','店铺','机型']
    work_sheet.write_row(0,0,ColumnNames)
    i=1
    for data in get_data(name):
        work_sheet.write_row(i,0,data)
        i+=1

#<editor-fold desc="MES撤单数据查询">
# """
def get_data(name):
    if name=='撤单统计':
        where='1=1'
    else:
        where="d.CLASSNAME='{}'".format(name)

    os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'   #解决乱码问题
    conn = cx_Oracle.connect('NMKMESSUPPORT', '123@Nmgd.com', '10.10.1.249:1521/mesdb')   #这步不报错就是连上啦
    cursor = conn.cursor()
    sql ='''
      select a.mo,b.sn,c.ROUTENAME,d.CLASSNAME,to_char(a.REVOKETIME,'yy-mm-dd hh24:mi:ss')REVOKETIME,case b.ISRESTORE when 0 then '未接收'  when 1 then '已回仓' end ISRESTORE,
            H.ORGCNAME,SHOP,(CASE a.WORKTYPE WHEN 1 THEN '主机' WHEN 2 THEN '小件' ELSE '显示器' END) WORKTYPE
            from mes_mo a left join mes_snjoin  b on a.mo=b.mo
            LEFT JOIN BAS_ROUTE c ON b.ROUTEID = c.id
            LEFT JOIN BAS_PROCESSCLASS d  ON b.WORKINGPROCESS = d.id
            LEFT JOIN MES_SCHEDULING e ON b.MO = E.MO
            left join SYS_ORGANIZE  h on E.ORGANIZEID=H.ID
            WHERE b.del = 0 AND A.STATUSID = 6  and a.REVOKETIME > to_date('2018-12-01 0:00:00','yyyy-mm-dd Hh24:mi:ss')   and  a.REVOKETIME < to_date('2019-01-01 0:00:00','yyyy-mm-dd Hh24:mi:ss')
            and {} '''.format(where)
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data
# """
#</editor-fold>

def get_tk():
    root = Tk()
    root.title('撤单导出')
    root.resizable(0,0)
    l1=Label(root,text="年",).place(x=0,y=0)
    e1=Entry(root,).place(x=20,y=0,width=40, height=20)
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - 450) / 2
    y = (sh - 200) / 2
    root.geometry("%dx%d+%d+%d" % (450, 200, x, y))
    root.mainloop()


if __name__ == '__main__':
    get_tk()
    try:
        class_name = ['撤单统计', '配主显', '测试', '已扫码', '外观检验', '包装称重', '独立组装', '内观检验', '线前五大件', '小件配货', '配三大件']
        file_name = '撤单数据.xls'
        #工作簿
        work_book = xlsxwriter.Workbook(file_name)
        for name in class_name:
            get_excel(name)
        work_book.close()
        # if os.path.exists('撤单数据.xls'):
        #     sen_email()
    except Exception as e:
        print(e)

