# coding:utf-8


import logging
import os
import common
import time
from common import Common
from data import Stockdata
from mail import *
from rules import Rule
from stockdates import tradeDate

"""
调用所有规则，并发送邮件通知
"""

def sendDuotou(daylist, stocklist):
    irule = Rule()
    for stockid in stocklist:
        irule.is_duotou(stockid, daylist)
    result_file = Common.REPORTPATH + Common.sep + "多头排列.csv"
    write_result_and_mail(irule.duotouCodeList, result_file, subjectname="多头股票推荐")
    print("*" * 100)
    print(irule.duotouCodeList)
    print("Total number is : %d" % len(irule.duotouCodeList))


def send_yiyangsanxian(daylist,stocklist):
    irule = Rule()
    for stockid in stocklist:
        irule.yiyangsanxian(stockid, daylist)
    result_file = Common.REPORTPATH + Common.sep + "一阳三线.csv"
    write_result_and_mail(irule.yiyangsanxianCodeList, result_file, subjectname="多头股票推荐")
    print("*" * 100)
    print(irule.yiyangsanxianCodeList)
    print("Total number is : %d" % len(irule.yiyangsanxianCodeList))


if __name__ == '__main__':
    tradeDays = tradeDate()
    daylist = tradeDays.get_last_trade_days()
    stockdata = Stockdata(daylist[2])
    stocklist = stockdata.getStocklistFromCodemap()
    sendDuotou(daylist, stocklist)
    send_yiyangsanxian(daylist, stocklist)
    stockdata.createEndFlag()
