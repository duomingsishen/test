# coding:utf-8

import xlwt
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#打开excel文件
data=xlwt.Workbook()
#获取其中的一个sheet
table=data.add_sheet('made')

# table.put_cell(0,2,1,'why',0)
# nrows=table.nrows
# ncols=table.ncols
# for i in range(nrows):
#  print table.row_values(i)
r=requests.get('http://html-color-codes.info/color-names/')
html=r.text
#print html
soup=BeautifulSoup(html,'html.parser')
trs=soup.find_all('tr')
row=0
col=0
for tr in trs:
    style=tr.get('style')
    tds=tr.find_all('td')
    td=[x for x in tds]
    name=td[1].text.strip()
    hex=td[2].text.strip()
    table.write(row,col,name)
    table.write(row,col+1,hex)
    table.write(row,col+2,style)
    row=row+1
    col=0
data.save('MADE.xls')