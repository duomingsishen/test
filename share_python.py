# coding:utf-8

import urllib2
import re
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#打开一个Excel文件
data=xlwt.Workbook(encoding = 'utf-8')
#获取其中的一个sheet
table=data.add_sheet('sheet1',cell_overwrite_ok=True)


#获取源码
def get_html(url):
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }
    request=urllib2.Request(url,headers=header)
    response=urllib2.urlopen(request)
    html=response.read().decode('gbk').encode('utf-8')
    return html

#获取商品id
def get_shop_id(html):
    reg=re.compile('<div class="product  " data-id="(.*?)"')
    id=re.findall(reg,html)
    return id

#获取价格
def get_shop_price(html):
    reg=re.compile('<p class="productPrice">.*?<em title=.*?><b>&yen;</b>(.*?)</em>',re.S)
    price=re.findall(reg,html)
    return price

#获取名称和地址
def get_shop_name(html):
    reg=re.compile('<p class="productTitle">.*?<a href="//(.*?)" target="_blank" title="(.*?)"',re.S)
    name=re.findall(reg,html)
    return name

#获取成交数和评论
def get_shop_status(html):
    reg=re.compile('<p class="productStatus" >.*?<span>月成交 <em>(.*?)</em></span>.*?<span>评价 <a href=".*?" target="_blank" data-p=".*?">(.*?)</a></span>',re.S)
    status=re.findall(reg,html)
    return status

if __name__ == '__main__':
    row = 0
    col = 0
    for j in range(0,181,60):
        url = 'https://list.tmall.com/search_product.htm?spm=a220m.1000858.0.0.6b0d20299bejcQ&s={}&q=%C4%FE%C3%C0%B9%FA%B6%C8&sort=s&style=g&search_condition=7&from=sn_1_rightnav&type=pc#J_Filter'.format(j)
        html=get_html(url)
        id=get_shop_id(html)
        price=get_shop_price(html)
        name=get_shop_name(html)
        status=get_shop_status(html)
        for i in zip(id,name,price,status):
            table.write(row, col, i[0])
            table.write(row, col + 1,i[1][0])
            table.write(row, col + 2,i[1][1])
            table.write(row, col + 3,i[2])
            table.write(row, col + 4,i[3][0])
            table.write(row, col + 5,i[3][1])
            row = row + 1
            col = 0

    data.save('E:\\shop1.xls')