# coding:utf-8

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

wd=webdriver.Chrome()
wd.implicitly_wait(10)
email_list=[]

qq='2019982159'
password='woqunima0514'


def main():
    wd.get('https://mail.qq.com/')
    login_frame=wd.find_element_by_id('login_frame') #frame或者iframe标签里的内容需要先切换过来才能找到
    wd.switch_to.frame(login_frame)
    wd.find_element_by_id('switcher_plogin').click()

    #输入用户名和密码然后登陆
    wd.find_element_by_id('u').send_keys(qq)
    wd.find_element_by_id('p').send_keys(password)
    wd.find_element_by_id('login_button').click()
    wd.find_element_by_id('skip_btn').click()


    #点击收件箱,然后去获取邮件列表
    wd.find_element_by_id('folder_1').click()
    main_frame=wd.find_element_by_id('mainFrame')
    wd.switch_to.frame(main_frame)

    #获取页码
    page_text=wd.find_element_by_css_selector('.right, .qm_right').text
    page_num=int(page_text.replace('/',' ').split()[1])


    #遍历页获取邮件
    for i in range(page_num):
        store_page_emails()

def store_page_emails():
    #获取当前页的邮件，如果有下一页，就点击下一页，如果没有就不点击
    h=wd.current_window_handle
    email_eles=wd.find_elements_by_css_selector('table.M, table.F')
    email_eles_count=len(email_eles)
    for i in range(email_eles_count):
        email_ele=wd.find_elements_by_css_selector('table.M, table.F')[i]
        ActionChains(wd).context_click(email_ele).perform()
        wd.find_elements_by_css_selector('.menu_item')[1].click()

        #获取邮件详情页的句柄,并切换过去
        email_handle=wd.window_handles[1]
        wd.switch_to.window(email_handle)

        #获取邮件内容
        main_frame=wd.find_element_by_id('mainFrame')
        wd.switch_to.frame(main_frame)

        subject=wd.find_element_by_class_name('sub_title').text
        nickname=wd.find_element_by_class_name('grn').text
        from_email=wd.find_element_by_id('tipFromAddr_readmail').text
        content=wd.find_element_by_id('qm_con_body').text


        email_list.append({'subject':subject,'nickname':nickname,'from_email':from_email,'content':content})

        wd.close()
        wd.switch_to.window(h)
        main_frame = wd.find_element_by_id('mainFrame')
        wd.switch_to.frame(main_frame)

    try:
        next_page=wd.find_element_by_id('netpage')
    except NoSuchElementException:
        print('获取完成')
    else:
        next_page.click()
        time.sleep(0.2)






if __name__ == '__main__':
    main()



