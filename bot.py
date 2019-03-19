# coding:utf-8

import qqbot
import datetime

@qqbot.QQBotSlot #是一个钩子,可以监控qq消息
def onQQMessage(bot,contact,member,content):
    """
    :param bot: 机器人实例,用来收发信息
    :param contact: 发送消息的人活着群
    :param member: 如果是群消息,代表个人
    :param content: 发送的内容
    """
    if "@ME" in content:
        user_qq=member.qq
        user_name=member.name
        if "hello" in content:
            sendData="""
                 咋的了？
            """
            bot.SendTo(contact,sendData)
if __name__=="__main__":
    qqbot.RunBot()