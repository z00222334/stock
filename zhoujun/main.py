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
from codemap import Codemap


"""
调用所有规则，并发送邮件通知
"""

def sendDuotou(daylist, stocklist):
    irule = Rule()
    for stockid in stocklist:
        irule.isDuotou(stockid, daylist)
    resultFile = Common.REPORTPATH + Common.sep + "多头排列.csv"
    write_result_and_mail(irule.duotouCodeList, resultFile, subjectname="多头股票推荐")

def sendYiyangsanxian(daylist,stocklist):
    irule = Rule()
    for stockid in stocklist:
        irule.yiyangsanxian(stockid, daylist)
    resultFile = Common.REPORTPATH + Common.sep + "一阳三线.csv"
    write_result_and_mail(irule.yiyangsanxianCodeList, resultFile, subjectname="多头股票推荐")

def sendTurnaround(daylist,stocklist):
    irule = Rule()
    for stockid in stocklist:
        irule.turnAround(stockid, daylist)
    resultFile = Common.REPORTPATH + Common.sep + "均线拐点.csv"
    write_result_and_mail(irule.turnAroundCodeList, resultFile, subjectname="多头股票推荐")


if __name__ == '__main__':
    tradeDays = tradeDate()
    daylist = tradeDays.get_last_trade_days()
    stockdata = Stockdata(daylist[2])
    stocklist = Codemap.getStocklistFromCodemap()
    sendDuotou(daylist, stocklist)
    sendYiyangsanxian(daylist, stocklist)
    sendTurnaround(daylist,stocklist)
    # stockdata.createEndFlag()

